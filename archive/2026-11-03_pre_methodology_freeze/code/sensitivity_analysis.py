"""
sensitivity_analysis.py — Steps 2 & 3 of the robustness extension.

  Step 2  QRF(40) vs QRF(45), controlled: same data, same split, same
          preprocessing, same bootstrap indices. Quantiles are PRE-SPECIFIED
          (0.40 = paper benchmark, 0.45 = our earlier test-selected value);
          in addition we report a quantile chosen by CV on the training data
          only (honest) and one chosen on the test data (paper-style,
          optimistic) to measure the selection optimism.

  Step 3  Poverty-threshold sensitivity: 189.09 / 189.05 / 194.10 Bs.
          Same fitted models; only the classification threshold changes.
          Paired bootstrap differences (same resample indices) give CIs for
          the effect of the threshold change.

  Both steps are run under two validation protocols:
    paper     two independent N/2 draws WITH replacement (train/test overlap)
    disjoint  50/50 partition, untouched test set (no shared households)

  Plus a repeated-split robustness check (N_SPLITS seeds) to show how much
  of each number is due to the particular random split.

Outputs → results/sensitivity/
"""

import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

import common as C

warnings.filterwarnings("ignore")

OUT = os.path.join(C.RESULTS_DIR, "sensitivity")
os.makedirs(OUT, exist_ok=True)

N_SPLITS = int(os.environ.get("N_SPLITS", 30))
# label -> value. "full" = P24.2 of the FULL sample (189.09 Bs);
# "train" = P24.2 of the TRAINING sample of each split (test never used).
# 189.05 / 194.10 = median expenditure of the officially-poor (IRIS 2005
# method) under official lines ~320 / ~328 Bs — also computed on this sample.
THRESHOLDS = {
    "189.09 (full-sample P24.2)": "full",
    "189.05 (IRIS recon., official ~320 Bs)": 189.05,
    "194.10 (IRIS recon., official ~328 Bs)": 194.10,
    "train-sample P24.2": "train",
}


def resolve_line(tval, base_line, y_tr):
    if tval == "full":
        return base_line
    if tval == "train":
        return C.reconstructed_poverty_line(y_tr)
    return float(tval)
FIXED_Q = (0.40, 0.45)
PROTOCOLS = {"paper": C.paper_split_idx, "disjoint": C.disjoint_split_idx}
GRID = C.QRF_QUANTILE_GRID


def fit_predict(X, y, tr, te, seed):
    """Fit every model once on the training rows; return test predictions."""
    Xtr, ytr, Xte = X[tr], y[tr], X[te]
    preds = {}
    dt = C.make_model("DecisionTree", seed).fit(Xtr, ytr)
    preds["DecisionTree"] = dt.predict(Xte)
    rf = C.make_model("RandomForest", seed).fit(Xtr, ytr)
    preds["RandomForest"] = rf.predict(Xte)
    Xd = C.iris_design(X)
    iris = C.make_model("IRIS_QR").fit(Xd[tr], ytr)
    preds["IRIS_Q42"] = iris.predict(Xd[te])
    qrf = C.make_model("QRF", seed).fit(Xtr, ytr)
    qgrid = qrf.predict(Xte, quantiles=list(GRID))           # (n_te, len(GRID))
    oof = C.qrf_oof_predictions(Xtr, ytr, groups=tr, seed=seed)
    return preds, qgrid, oof


def qcol(q):
    return GRID.index(round(q, 2))


def model_preds_for_threshold(preds, qgrid, oof, y_tr, y_te, line):
    """Model set evaluated at one threshold, incl. the three QRF selection rules."""
    out = dict(preds)
    for q in FIXED_Q:
        out[f"QRF(q={q:.2f}) fixed"] = qgrid[:, qcol(q)]
    q_cv, _ = C.best_quantile(y_tr, oof, line)
    q_te, _ = C.best_quantile(y_te, qgrid, line)
    out["QRF CV-selected"] = qgrid[:, qcol(q_cv)]
    out["QRF test-selected"] = qgrid[:, qcol(q_te)]
    return out, q_cv, q_te


def run_primary(X, y, base_line):
    """Seed-42 run: bootstrap CIs, confusion matrices, paired differences."""
    rows, cm_rows, diff_rows, qsel_rows = [], [], [], []
    for proto, split_fn in PROTOCOLS.items():
        tr, te = split_fn(len(y), C.RANDOM_STATE)
        overlap = np.isin(np.unique(te), tr).mean()
        print(f"\n[{proto}] train={len(tr)} test={len(te)} "
              f"unique-test-HH-also-in-train={overlap:.1%}")
        t0 = time.time()
        preds, qgrid, oof = fit_predict(X, y, tr, te, C.RANDOM_STATE)
        print(f"  fitted in {time.time()-t0:.1f}s")
        y_tr, y_te = y[tr], y[te]
        idx = C.boot_indices(len(te))
        boots = {}   # (threshold_label, model) -> boot dict
        for tlab, tval in THRESHOLDS.items():
            line = resolve_line(tval, base_line, y_tr)
            mp, q_cv, q_te = model_preds_for_threshold(preds, qgrid, oof, y_tr, y_te, line)
            qsel_rows.append(dict(protocol=proto, threshold=tlab, line=line,
                                  q_cv_selected=q_cv, q_test_selected=q_te))
            for name, yp in mp.items():
                b = C.bootstrap_metrics(y_te, yp, line, idx)
                boots[(tlab, name)] = b
                s = C.summarise(b)
                pt = C.targeting_metrics(y_te, yp, line)
                label = name
                if name == "QRF CV-selected":
                    label += f" (q={q_cv:.2f})"
                if name == "QRF test-selected":
                    label += f" (q={q_te:.2f})"
                r = dict(protocol=proto, threshold=tlab, line=round(line, 4),
                         test_poverty_rate=float((y_te < line).mean()),
                         model=label)
                for m in C.METRICS:
                    r[m], r[f"{m}_lo"], r[f"{m}_hi"] = s[m]
                    r[f"{m}_point"] = pt[m]
                rows.append(r)
                cm_rows.append(dict(protocol=proto, threshold=tlab, model=label,
                                    **{k: pt[k] for k in ("TP", "FP", "FN", "TN")}))

        # Step 2: paired difference QRF(40) − QRF(45) at every threshold
        for tlab in THRESHOLDS:
            a = boots[(tlab, "QRF(q=0.40) fixed")]
            b = boots[(tlab, "QRF(q=0.45) fixed")]
            for m in C.METRICS:
                d = a[m] - b[m]
                lo, hi = C.ci(d)
                diff_rows.append(dict(protocol=proto, comparison="QRF(40) - QRF(45)",
                                      threshold=tlab, metric=m, diff=float(d.mean()),
                                      lo=lo, hi=hi, excludes_zero=bool(lo > 0 or hi < 0)))
        # Step 3: paired difference alt-threshold − 189.09 for every model
        base_lab = list(THRESHOLDS)[0]
        models = [k[1] for k in boots if k[0] == base_lab]
        for tlab in list(THRESHOLDS)[1:]:
            for name in models:
                for m in C.METRICS:
                    d = boots[(tlab, name)][m] - boots[(base_lab, name)][m]
                    lo, hi = C.ci(d)
                    diff_rows.append(dict(protocol=proto, comparison=f"{name}: threshold",
                                          threshold=f"{tlab} minus 189.09", metric=m,
                                          diff=float(d.mean()), lo=lo, hi=hi,
                                          excludes_zero=bool(lo > 0 or hi < 0)))
    return (pd.DataFrame(rows), pd.DataFrame(cm_rows),
            pd.DataFrame(diff_rows), pd.DataFrame(qsel_rows))


def run_repeated(X, y, base_line):
    """Point metrics on the full test sample for N_SPLITS different seeds."""
    rows = []
    for proto, split_fn in PROTOCOLS.items():
        for s in range(N_SPLITS):
            seed = 1000 + s
            tr, te = split_fn(len(y), seed)
            preds, qgrid, oof = fit_predict(X, y, tr, te, seed)
            for tlab, tval in THRESHOLDS.items():
                line = resolve_line(tval, base_line, y[tr])
                mp, q_cv, q_te = model_preds_for_threshold(
                    preds, qgrid, oof, y[tr], y[te], line)
                for name, yp in mp.items():
                    pt = C.targeting_metrics(y[te], yp, line)
                    rows.append(dict(protocol=proto, seed=seed, threshold=tlab, line=line,
                                     model=name, q_cv=q_cv, q_test=q_te,
                                     **{m: pt[m] for m in C.METRICS}))
            print(f"  [{proto}] split {s+1}/{N_SPLITS} done", flush=True)
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    X, y, base_line = C.load_bolivia()
    X, y = X.values, y.values
    C.save_config(os.path.join(OUT, "config.json"))

    print("\n=== PRIMARY RUN (seed 42) ===")
    summ, cms, diffs, qsel = run_primary(X, y, base_line)
    summ.to_csv(os.path.join(OUT, "primary_metrics_bootstrap_ci.csv"), index=False)
    cms.to_csv(os.path.join(OUT, "primary_confusion_matrices.csv"), index=False)
    diffs.to_csv(os.path.join(OUT, "primary_paired_differences.csv"), index=False)
    qsel.to_csv(os.path.join(OUT, "primary_quantile_selection.csv"), index=False)

    if N_SPLITS > 0:
        print(f"\n=== REPEATED SPLITS (n={N_SPLITS} per protocol) ===")
        rep = run_repeated(X, y, base_line)
        rep.to_csv(os.path.join(OUT, "repeated_splits_raw.csv"), index=False)
        agg = (rep.groupby(["protocol", "threshold", "model"])[list(C.METRICS)]
               .agg(["mean", "std"]).round(4))
        agg.columns = [f"{a}_{b}" for a, b in agg.columns]
        agg.reset_index().to_csv(os.path.join(OUT, "repeated_splits_summary.csv"),
                                 index=False)
        qfreq = (rep.drop_duplicates(["protocol", "seed", "threshold"])
                 .groupby(["protocol", "threshold"])
                 .agg(q_cv_mode=("q_cv", lambda s: s.mode().iloc[0]),
                      q_cv_values=("q_cv", lambda s: dict(s.value_counts().sort_index())),
                      q_test_values=("q_test", lambda s: dict(s.value_counts().sort_index()))))
        qfreq.reset_index().to_csv(os.path.join(OUT, "repeated_splits_quantile_choice.csv"),
                                   index=False)
    print(f"\nDone in {time.time()-t0:.0f}s → {OUT}")


if __name__ == "__main__":
    sys.exit(main())
