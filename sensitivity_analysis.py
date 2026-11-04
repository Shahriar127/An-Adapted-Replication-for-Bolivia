"""
sensitivity_analysis.py — Steps 2 & 3 of the robustness extension.

  Step 2  QRF(40) vs QRF(45), controlled: same data, same split, same
          preprocessing, same bootstrap indices. Quantiles are PRE-SPECIFIED
          (0.40 = 2015-draft benchmark, 0.41 = published SE choice,
          0.45 = our earlier result). We also report the stochastic-ensemble
          model chosen by OOB BPAC on the training data (published rule
          [S7]) and a quantile chosen on the test data (optimistic, reported
          only to measure selection optimism).

  Step 3  Poverty-threshold sensitivity: 189.09 / 188.77 / 189.05 / 194.10 Bs
          and a training-sample threshold.
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
    "188.77 (full-sample P24.03, published Table 3)": "full2403",
    "189.05 (IRIS recon., official ~320 Bs)": 189.05,
    "194.10 (IRIS recon., official ~328 Bs)": 194.10,
    "train-sample P24.2": "train",
}


def resolve_line(tval, base_line, y_tr):
    if tval == "full":
        return base_line
    if tval == "full2403":
        return float(np.percentile(FULL_Y, 24.03))     # ambiguity A2
    if tval == "train":
        return C.reconstructed_poverty_line(y_tr)
    return float(tval)


FULL_Y = None                       # set in main(); used for the P24.03 threshold
FIXED_Q = (0.40, 0.41, 0.45)
PROTOCOLS = {"paper": C.paper_split_idx, "disjoint": C.disjoint_split_idx}
GRID = C.QRF_QUANTILE_GRID


def fit_predict(X, y, tr, te, seed):
    """Fit every model once on the training rows. Returns the test predictions,
    the SE candidate matrices on test and OOB [S7] (columns = C.se_candidates())."""
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
    se_test = C.se_test_predictions(rf, qrf, Xte)       # (n_te, 1 + len(GRID))
    se_oob = C.se_oob_predictions(rf, qrf, Xtr)          # (n_tr, 1 + len(GRID))
    return preds, se_test, se_oob


def qcol(q):
    """Column of quantile q in the QRF-only part of the SE matrices."""
    return GRID.index(round(q, 2))


def model_preds_for_threshold(preds, se_test, se_oob, y_tr, y_te, line):
    """Model set evaluated at one threshold, including the SE selection rule."""
    out = dict(preds)
    qgrid = se_test[:, 1:]
    for q in FIXED_Q:
        out[f"QRF(q={q:.2f}) fixed"] = qgrid[:, qcol(q)]
    se_label, se_col, _ = C.select_se(y_tr, se_oob, line)
    q_te, _ = C.best_quantile(y_te, qgrid, line)
    out["SE OOB-selected"] = se_test[:, se_col]
    out["QRF test-selected"] = qgrid[:, qcol(q_te)]
    return out, se_label, q_te


def run_primary(X, y, base_line):
    """Seed-42 run: bootstrap CIs, confusion matrices, paired differences."""
    rows, cm_rows, diff_rows, qsel_rows = [], [], [], []
    for proto, split_fn in PROTOCOLS.items():
        tr, te = split_fn(len(y), C.RANDOM_STATE)
        overlap = np.isin(np.unique(te), tr).mean()
        print(f"\n[{proto}] train={len(tr)} test={len(te)} "
              f"unique-test-HH-also-in-train={overlap:.1%}")
        t0 = time.time()
        preds, se_test, se_oob = fit_predict(X, y, tr, te, C.RANDOM_STATE)
        print(f"  fitted in {time.time()-t0:.1f}s")
        y_tr, y_te = y[tr], y[te]
        idx = C.boot_indices(len(te))
        boots = {}   # (threshold_label, model) -> boot dict
        for tlab, tval in THRESHOLDS.items():
            line = resolve_line(tval, base_line, y_tr)
            mp, se_label, q_te = model_preds_for_threshold(preds, se_test, se_oob,
                                                           y_tr, y_te, line)
            qsel_rows.append(dict(protocol=proto, threshold=tlab, line=line,
                                  se_oob_selected=se_label, q_test_selected=q_te))
            for name, yp in mp.items():
                b = C.bootstrap_metrics(y_te, yp, line, idx)
                boots[(tlab, name)] = b
                s = C.summarise(b)
                pt = C.targeting_metrics(y_te, yp, line)
                label = name
                if name == "SE OOB-selected":
                    label += f" ({se_label})"
                if name == "QRF test-selected":
                    label += f" (q={q_te:.2f})"
                r = dict(protocol=proto, threshold=tlab, line=round(line, 4),
                         test_poverty_rate=float((y_te < line).mean()),
                         model=label)
                for m in C.METRICS:
                    r[m], r[f"{m}_lo"], r[f"{m}_hi"] = s[m]
                    r[f"{m}_SE"] = float(np.std(b[m], ddof=1))
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
            preds, se_test, se_oob = fit_predict(X, y, tr, te, seed)
            for tlab, tval in THRESHOLDS.items():
                line = resolve_line(tval, base_line, y[tr])
                mp, se_label, q_te = model_preds_for_threshold(
                    preds, se_test, se_oob, y[tr], y[te], line)
                for name, yp in mp.items():
                    pt = C.targeting_metrics(y[te], yp, line)
                    rows.append(dict(protocol=proto, seed=seed, threshold=tlab, line=line,
                                     model=name, se_choice=se_label, q_test=q_te,
                                     **{m: pt[m] for m in C.METRICS}))
            print(f"  [{proto}] split {s+1}/{N_SPLITS} done", flush=True)
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    X, y, base_line = C.load_bolivia()
    X, y = X.values, y.values
    global FULL_Y
    FULL_Y = y
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
                 .agg(se_choice_mode=("se_choice", lambda s: s.mode().iloc[0]),
                      se_choice_values=("se_choice",
                                        lambda s: {k: int(v) for k, v in s.value_counts().sort_index().items()}),
                      q_test_values=("q_test",
                                     lambda s: {float(k): int(v) for k, v in s.value_counts().sort_index().items()})))
        qfreq.reset_index().to_csv(os.path.join(OUT, "repeated_splits_quantile_choice.csv"),
                                   index=False)
    print(f"\nDone in {time.time()-t0:.0f}s → {OUT}")


if __name__ == "__main__":
    sys.exit(main())
