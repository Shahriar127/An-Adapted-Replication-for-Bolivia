"""
Phase 2 — A9/A10 sensitivity audit (one factor at a time). Separate from the
repeated-split CV-QR comparison. Does not modify the frozen pipeline.

A9  QRF leaf storage: paper text (Meinshausen, "retain the value of all
    observation", p.544) vs cited software quantregForest 1.3-5 (one response
    per leaf drawn from all n training rows; type-7 quantile over trees;
    evidence/r_source/quantregForest_1.3-5_R_*.R, lines 51-53, 69-72, 31).
A10 node size: frozen min_samples_leaf=5 vs R randomForest 4.6-12 nodesize=5
    (regTree.c lines 124/139: a child with nodepop <= 5 becomes terminal;
    nodepop counts BOOTSTRAP DRAWS, duplicates included).

Configurations (seeds 42 and 1000-1019, published split protocol):
  B0                frozen: quantile-forest, all in-bag leaf obs (weighted), min_samples_leaf=5
  A9-qf1            B0 with quantile-forest max_samples_leaf=1
  A9-software       quantregForest 1.3-5 procedure, frozen node rule
  A10-approx        B0 leaf storage, sklearn min_samples_split=6/min_samples_leaf=1
                    (counts DISTINCT rows; approximates R)
  A9sw+A10-approx   software procedure + approximate R node rule (A8 E4)
  A9sw+A10-exact    software procedure + EXACT R node rule (trees grown on the
                    explicitly duplicated bootstrap sample, so node counts
                    include duplicates as in R)
A10 effect under the software procedure is isolated by
  A9-software -> A9sw+A10-approx -> A9sw+A10-exact.
"""
import os
import sys
import time

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.tree import DecisionTreeRegressor

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
ROOT = os.path.dirname(AUDIT)
sys.path.insert(0, ROOT)
import common as C  # noqa: E402
from a8_qrf_audit import RQuantregForest, FROZEN_NODE, R_NODE, qf, rf_model  # noqa: E402

OUT = os.path.join(AUDIT, "outputs", "a9_a10")
os.makedirs(OUT, exist_ok=True)
GRID = C.QRF_QUANTILE_GRID
SEEDS = [C.RANDOM_STATE] + list(range(1000, 1020))
TOL = 0.010


def _grow(X, y, n, mtry, seed):
    rng = np.random.RandomState(seed)
    idx = rng.randint(0, n, n)                                    # bootstrap draw, with replacement
    t = DecisionTreeRegressor(max_features=mtry, min_samples_split=6, min_samples_leaf=1,
                              random_state=rng.randint(2**31 - 1)).fit(X[idx], y[idx])
    return t, np.bincount(idx, minlength=n)


class ExactRForest:
    """randomForest 4.6-12 regression trees with the exact nodesize semantics
    (nodepop counts duplicated bootstrap rows) + quantregForest 1.3-5 leaf values."""

    def __init__(self, seed, ntree=C.N_TREES):
        self.seed, self.ntree = seed, ntree
        self.rng = np.random.RandomState(seed + 7)

    def fit(self, X, y):
        X = np.asarray(X, np.float32); y = np.asarray(y, float); n, p = X.shape
        mtry = max(int(np.floor(p / 3)), 1)
        ss = np.random.RandomState(self.seed).randint(2**31 - 1, size=self.ntree)
        res = Parallel(n_jobs=-1)(delayed(_grow)(X, y, n, mtry, int(s)) for s in ss)
        self.trees = [r[0] for r in res]
        self.inbag = np.column_stack([r[1] for r in res])
        self.train_leaves = np.column_stack([t.apply(X) for t in self.trees])
        self.values = []
        for b in range(self.ntree):                                  # quantregForest.R l.51-53
            perm = self.rng.permutation(n)
            lp = self.train_leaves[perm, b]
            u, first = np.unique(lp, return_index=True)
            v = np.full(self.train_leaves[:, b].max() + 1, np.nan); v[u] = y[perm[first]]
            self.values.append(v)
        P = np.column_stack([t.predict(X) for t in self.trees]).astype(float)
        P[self.inbag > 0] = np.nan
        self.rf_oob = np.nanmean(P, 1)                               # RF OOB (mean over OOB trees)
        return self

    def rf_predict(self, X):
        return np.mean([t.predict(np.asarray(X, np.float32)) for t in self.trees], axis=0)

    def _vals(self, leaves):
        return np.column_stack([self.values[b][leaves[:, b]] for b in range(self.ntree)])

    def predict(self, X, q):
        L = np.column_stack([t.apply(np.asarray(X, np.float32)) for t in self.trees])
        return np.quantile(self._vals(L), q, axis=1, method="linear").T

    def predict_oob(self, q):
        vals = self._vals(self.train_leaves); vals[self.inbag > 0] = np.nan
        minoob = int((~np.isnan(vals)).sum(1).min())
        sub = np.stack([self.rng.choice(r[~np.isnan(r)], minoob, replace=False) for r in vals])
        return np.quantile(sub, q, axis=1, method="linear").T

    def structure(self):
        leaf_n, internal_n = [], []
        for t in self.trees:
            tr = t.tree_
            leaf = tr.children_left == -1
            leaf_n.append(tr.n_node_samples[leaf]); internal_n.append(tr.n_node_samples[~leaf][1:])
        leaf_n = np.concatenate(leaf_n); internal_n = np.concatenate(internal_n)
        return dict(min_nonroot_internal=int(internal_n.min()), min_leaf=int(leaf_n.min()),
                    share_leaves_below5=float((leaf_n < 5).mean()), mean_leaves_per_tree=len(leaf_n) / self.ntree)


CONFIGS = ["B0", "A9-qf1", "A9-software", "A10-approx", "A9sw+A10-approx", "A9sw+A10-exact"]


def fit_config(name, Xtr, ytr, Xte, seed):
    """Returns (rf_oob, rf_test, qrf_oob[n,G], qrf_test[n,G], structure dict)."""
    if name == "A9sw+A10-exact":
        m = ExactRForest(seed).fit(Xtr, ytr)
        return m.rf_oob, m.rf_predict(Xte), m.predict_oob(GRID), m.predict(Xte, GRID), m.structure()
    node = R_NODE if "A10-approx" in name else FROZEN_NODE
    rf = rf_model(node, seed).fit(Xtr, ytr)
    if name in ("A9-software", "A9sw+A10-approx"):
        m = RQuantregForest(node, seed).fit(Xtr, ytr)
        qo, qt = m.predict_oob(GRID), m.predict(Xte, GRID)
        est = m.rf.estimators_
    else:
        m = qf(node, 1 if name == "A9-qf1" else None, seed).fit(Xtr, ytr)
        qo, qt = m.predict(Xtr, quantiles=GRID, oob_score=True), m.predict(Xte, quantiles=GRID)
        est = m.estimators_
    leaf_n, internal_n = [], []
    for e in est:   # sklearn n_node_samples counts DISTINCT rows (weights carry duplicates)
        tr = e.tree_; leaf = tr.children_left == -1
        leaf_n.append(tr.n_node_samples[leaf]); internal_n.append(tr.n_node_samples[~leaf][1:])
    leaf_n = np.concatenate(leaf_n); internal_n = np.concatenate(internal_n)
    st = dict(min_nonroot_internal=int(internal_n.min()), min_leaf=int(leaf_n.min()),
              share_leaves_below5=float((leaf_n < 5).mean()), mean_leaves_per_tree=len(leaf_n) / len(est),
              note="sklearn counts distinct rows")
    return rf.oob_prediction_, rf.predict(Xte), qo, qt, st


def main():
    t0 = time.time()
    X, y, line = C.load_bolivia(verbose=False)
    X, y = X.values.astype(float), y.values
    rows, structs = [], []
    for seed in SEEDS:
        tr, te = C.paper_split_idx(len(y), seed)
        idx = C.boot_indices(len(te)) if seed == C.RANDOM_STATE else None
        for name in CONFIGS:
            rfo, rft, qo, qt, st = fit_config(name, X[tr], y[tr], X[te], seed)
            lab, col, _ = C.select_se(y[tr], np.column_stack([rfo, qo]), line)
            preds = {"SE (OOB-selected)": (lab, np.column_stack([rft, qt])[:, col]),
                     "QRF(0.41) fixed": ("QRF(0.41)", qt[:, GRID.index(0.41)])}
            for model, (chosen, p) in preds.items():
                pt = C.targeting_metrics(y[te], p, line)
                r = dict(seed=seed, config=name, model=model, chosen=chosen, **{m: pt[m] for m in C.METRICS})
                if idx is not None:
                    b = C.bootstrap_metrics(y[te], p, line, idx)
                    r.update({f"{m}_boot_mean": float(b[m].mean()) for m in C.METRICS})
                    r.update({f"BPAC_boot_{k}": v for k, v in zip(("lo", "hi"), C.ci(b["BPAC"]))})
                rows.append(r)
            if seed in (C.RANDOM_STATE, 1000):
                structs.append(dict(seed=seed, config=name, **st))
        print(f"seed {seed} done ({time.time()-t0:.0f}s)", flush=True)
    df = pd.DataFrame(rows); df.to_csv(os.path.join(OUT, "a9_a10_per_split.csv"), index=False)
    pd.DataFrame(structs).to_csv(os.path.join(OUT, "a9_a10_tree_structure.csv"), index=False)

    rep = df[df.seed != C.RANDOM_STATE]
    piv = rep.pivot_table(index=["model", "seed"], columns="config", values=list(C.METRICS))
    summ = []
    for model in rep.model.unique():
        for name in CONFIGS:
            for m in C.METRICS:
                v = piv.loc[model][(m, name)]; d = v - piv.loc[model][(m, "B0")]
                better = d if m not in ("UC", "LE") else -d
                summ.append(dict(model=model, config=name, metric=m, mean=v.mean(), sd=v.std(ddof=1),
                                 diff_vs_B0_mean=d.mean(), diff_vs_B0_sd=d.std(ddof=1),
                                 n_better=int((better > TOL).sum()), n_worse=int((better < -TOL).sum()),
                                 n_tie=int((better.abs() <= TOL).sum()), n_splits=len(d)))
    pd.DataFrame(summ).to_csv(os.path.join(OUT, "a9_a10_summary.csv"), index=False)
    s = pd.DataFrame(summ)
    pd.set_option("display.width", 220)
    print(s[s.metric == "BPAC"].round(4).to_string(index=False))
    print(pd.DataFrame(structs).to_string(index=False))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
