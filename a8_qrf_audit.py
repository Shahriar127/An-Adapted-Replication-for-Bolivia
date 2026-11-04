"""
a8_qrf_audit.py — Phase 1: audit of ambiguity A8 (our QRF vs the published SE QRF).

Does NOT modify the frozen methodology (common.py) or any existing result.
Writes only to results/a8_audit/.

Published target (Table A1 row 9, p.545): SE QRF(0.41), bootstrap means
  TA 80.17  PA 55.33  UC 44.67  LE 40.44  BPAC 50.18  [CI 39.26, 58.57]

Each configuration changes exactly ONE factor relative to the frozen baseline
(B0), except E4/E9, which are labelled combinations. Evaluated on the published
split protocol (two N/2 draws with replacement) for seed 42 plus 20 further seeds.

R reference behaviour (verbatim source, quantregForest 1.3-5 and randomForest regTree.c):
  * quantregForest stores ONE response per leaf per tree, drawn at random from
    ALL n training rows falling in that leaf (not only in-bag rows);
    prediction = R quantile() type 7 over the ntree per-tree values.
  * OOB (keep.inbag=TRUE): per row, keep trees where the row is out-of-bag,
    subsample `minoob` values, quantile type 7. The stored leaf value can be
    the row's own y (leak).
  * randomForest nodesize=5: a child with <= 5 rows becomes terminal; children
    may be smaller than 5  ==  sklearn min_samples_split=6, min_samples_leaf=1.
"""
import os
import sys
import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble._forest import _generate_sample_indices

import common as C

OUT = os.path.join(C.RESULTS_DIR, "a8_audit")
os.makedirs(OUT, exist_ok=True)
GRID = C.QRF_QUANTILE_GRID
SEEDS = [C.RANDOM_STATE] + list(range(1000, 1000 + int(os.environ.get("A8_SPLITS", 20))))
PUBLISHED = dict(TA=0.8017, PA=0.5533, UC=0.4467, LE=0.4044, BPAC=0.5018)
FROZEN_NODE = dict(min_samples_leaf=5)
R_NODE = dict(min_samples_split=6, min_samples_leaf=1)


# ──────────────────────────────────────────────────────────────────────────────
#  Faithful emulation of R quantregForest 1.3-5 on top of an sklearn forest
# ──────────────────────────────────────────────────────────────────────────────
class RQuantregForest:
    def __init__(self, node, seed):
        self.rf = RandomForestRegressor(n_estimators=C.N_TREES, max_features=1 / 3,
                                        bootstrap=True, n_jobs=-1, random_state=seed, **node)
        self.rng = np.random.RandomState(seed + 7)

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32); y = np.asarray(y, float)
        self.rf.fit(X, y)
        n = len(y)
        leaves = self.rf.apply(X)                                  # (n, B)
        self.values = []
        for b in range(leaves.shape[1]):
            perm = self.rng.permutation(n)                         # sample(1:n, n)
            lp = leaves[perm, b]
            uniq, first = np.unique(lp, return_index=True)         # first row in permuted order per leaf
            v = np.full(leaves[:, b].max() + 1, np.nan)
            v[uniq] = y[perm[first]]
            self.values.append(v)
        # in-bag counts, exactly as sklearn drew them
        inbag = np.zeros((n, len(self.rf.estimators_)), dtype=int)
        for b, est in enumerate(self.rf.estimators_):
            idx = _generate_sample_indices(est.random_state, n, n)
            inbag[:, b] = np.bincount(idx, minlength=n)
        self.inbag = inbag
        self.train_leaves = leaves
        return self

    def _vals(self, leaves):
        return np.column_stack([self.values[b][leaves[:, b]] for b in range(leaves.shape[1])])

    def predict(self, X, quantiles):
        vals = self._vals(self.rf.apply(np.asarray(X, dtype=np.float32)))
        return np.quantile(vals, quantiles, axis=1, method="linear").T   # R type 7

    def predict_oob(self, quantiles):
        vals = self._vals(self.train_leaves)
        vals[self.inbag > 0] = np.nan
        counts = (~np.isnan(vals)).sum(1)
        minoob = int(counts.min())
        if minoob < 10:
            raise RuntimeError("too few OOB trees")
        sub = np.empty((vals.shape[0], minoob))
        for i in range(vals.shape[0]):
            v = vals[i][~np.isnan(vals[i])]
            sub[i] = self.rng.choice(v, minoob, replace=False)
        return np.quantile(sub, quantiles, axis=1, method="linear").T


# ──────────────────────────────────────────────────────────────────────────────
#  Configurations
# ──────────────────────────────────────────────────────────────────────────────
def qf(node, msl, seed):
    from quantile_forest import RandomForestQuantileRegressor
    return RandomForestQuantileRegressor(n_estimators=C.N_TREES, max_features=1 / 3,
                                         max_samples_leaf=msl, n_jobs=-1,
                                         random_state=seed, **node)


def rf_model(node, seed):
    return RandomForestRegressor(n_estimators=C.N_TREES, max_features=1 / 3, oob_score=True,
                                 n_jobs=-1, random_state=seed, **node)


CONFIGS = {
    # name: (description, settings)
    "B0 frozen":            ("frozen primary (quantile-forest, min_samples_leaf=5, all leaf obs)", {}),
    "E1 one value/leaf":    ("quantile-forest max_samples_leaf=1 (one in-bag value per leaf)", dict(msl=1)),
    "E2 R node rule":       ("RF+QRF: min_samples_split=6, min_samples_leaf=1 (R nodesize=5)", dict(node=R_NODE)),
    "E3 R qrf procedure":   ("R quantregForest 1.3-5 leaf values + type-7 + R OOB (frozen node rule)", dict(rqrf=True)),
    "E4 full R emulation":  ("E2 + E3 combined", dict(node=R_NODE, rqrf=True)),
    "E5 OOB dedup":         ("frozen, but OOB treats duplicated households as one (selection only)", dict(dedup=True)),
    "E6 regions one-hot":   ("frozen, regions as 9 binary columns for forests", dict(onehot=True)),
    "E7 log target":        ("frozen, forests trained on log(1+y), quantiles back-transformed", dict(logy=True)),
    "E8 line P24.03":       ("frozen, poverty line = P24.03 (188.77 Bs)", dict(p2403=True)),
    "E9 R emulation+P24.03": ("E4 + E8 combined", dict(node=R_NODE, rqrf=True, p2403=True)),
}


def onehot_regions(X):
    ri = C.FEATURE_COLS.index("regions")
    reg = X[:, ri].astype(int)
    return np.column_stack([np.delete(X, ri, axis=1)] + [(reg == r).astype(float) for r in range(1, 10)])


def run_config(cfg, X, y, line_full, tr, te, seed):
    node = cfg.get("node", FROZEN_NODE)
    line = float(np.percentile(y, 24.03)) if cfg.get("p2403") else line_full
    Xf = onehot_regions(X) if cfg.get("onehot") else X
    ytr_fit = np.log1p(y[tr]) if cfg.get("logy") else y[tr]
    inv = np.expm1 if cfg.get("logy") else (lambda v: v)
    Xtr, Xte = Xf[tr], Xf[te]

    rf = rf_model(node, seed).fit(Xtr, ytr_fit)
    rf_oob, rf_te = inv(rf.oob_prediction_), inv(rf.predict(Xte))
    if cfg.get("rqrf"):
        m = RQuantregForest(node, seed).fit(Xtr, ytr_fit)
        q_oob, q_te = inv(m.predict_oob(GRID)), inv(m.predict(Xte, GRID))
    else:
        m = qf(node, cfg.get("msl", None), seed).fit(Xtr, ytr_fit)
        kw = {}
        if cfg.get("dedup"):
            groups = pd.Series(np.arange(len(tr))).groupby(tr).apply(list)
            kw["duplicates"] = [g for g in groups if len(g) > 1]
        q_oob = inv(m.predict(Xtr, quantiles=GRID, oob_score=True, **kw))
        q_te = inv(m.predict(Xte, quantiles=GRID))
    oob = np.column_stack([rf_oob, q_oob]); test = np.column_stack([rf_te, q_te])
    label, col, _ = C.select_se(y[tr], oob, line)
    out = {"SE": (label, test[:, col]), "QRF(0.41)": ("QRF(0.41)", q_te[:, GRID.index(0.41)]),
           "QRF(0.40)": ("QRF(0.40)", q_te[:, GRID.index(0.40)])}
    return out, line


def main():
    t0 = time.time()
    X, y, line_full = C.load_bolivia(verbose=False)
    X, y = X.values.astype(float), y.values
    rows = []
    for seed in SEEDS:
        tr, te = C.paper_split_idx(len(y), seed)
        idx = C.boot_indices(len(te)) if seed == C.RANDOM_STATE else None
        for name, (desc, cfg) in CONFIGS.items():
            out, line = run_config(cfg, X, y, line_full, tr, te, seed)
            for model, (label, pred) in out.items():
                pt = C.targeting_metrics(y[te], pred, line)
                r = dict(config=name, seed=seed, model=model, chosen=label,
                         **{m: pt[m] for m in C.METRICS})
                if idx is not None:
                    b = C.bootstrap_metrics(y[te], pred, line, idx)
                    r.update({f"{m}_boot": float(np.mean(b[m])) for m in C.METRICS})
                rows.append(r)
        print(f"seed {seed} done ({time.time()-t0:.0f}s)", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "a8_raw.csv"), index=False)

    rep = df[df.seed != C.RANDOM_STATE]
    summ = (rep.groupby(["config", "model"])[list(C.METRICS)].agg(["mean", "std"]))
    summ.columns = [f"{a}_{b}" for a, b in summ.columns]
    summ = summ.reset_index()
    base = summ[summ.config == "B0 frozen"].set_index("model")
    for m in C.METRICS:
        summ[f"d{m}_vs_B0"] = summ.apply(lambda r: r[f"{m}_mean"] - base.loc[r.model, f"{m}_mean"], axis=1)
    summ["BPAC_gap_to_published"] = summ["BPAC_mean"] - PUBLISHED["BPAC"]
    summ["gap_in_SDs"] = summ["BPAC_gap_to_published"] / summ["BPAC_std"]
    choice = (rep[rep.model == "SE"].groupby("config").chosen
              .agg(lambda s: dict(s.value_counts().sort_index())).rename("SE_choices"))
    summ = summ.merge(choice, left_on="config", right_index=True, how="left")
    summ.to_csv(os.path.join(OUT, "a8_summary.csv"), index=False)
    primary = df[df.seed == C.RANDOM_STATE]
    primary.to_csv(os.path.join(OUT, "a8_primary_seed42.csv"), index=False)
    with open(os.path.join(OUT, "a8_configs.txt"), "w") as f:
        for k, (d, c) in CONFIGS.items():
            f.write(f"{k}: {d}  {c}\n")
    pd.set_option("display.width", 250)
    print(summ[["config", "model", "TA_mean", "PA_mean", "UC_mean", "LE_mean", "BPAC_mean",
                "BPAC_std", "dBPAC_vs_B0", "gap_in_SDs"]].round(3).to_string(index=False))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    sys.exit(main())
