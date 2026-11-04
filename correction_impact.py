"""
correction_impact.py — measured impact of each methodology-freeze correction
(METHODOLOGY_REFERENCE.md, C1–C3), applied cumulatively on the SAME split and
the SAME bootstrap indices (seed 42, threshold 189.09 Bs):

  step 0  pre-freeze pipeline: TP+FP metrics, QRF max_samples_leaf=1,
          quantile by 5-fold grouped CV on a 0.05 grid
  step 1  + C1  published metric definitions (TP+FN)
  step 2  + C2  QRF keeps all leaf observations (max_samples_leaf=None)
  step 3  + C3  SE selection by OOB BPAC over RF + QRF(0.01..0.99)

Output → results/audit/correction_impact.csv
"""
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

import common as C

OUT = os.path.join(C.RESULTS_DIR, "audit")
os.makedirs(OUT, exist_ok=True)
OLD_GRID = [round(float(q), 2) for q in np.arange(0.05, 0.96, 0.05)]


def old_metrics(TP, FP, FN, TN):
    """Pre-freeze (2015 Table 2 typo) definitions, used only here for comparison."""
    d, t = TP + FP, TP + FN
    with np.errstate(divide="ignore", invalid="ignore"):
        return dict(TA=(TP + TN) / (TP + FP + FN + TN),
                    PA=np.where(d > 0, TP / d, 0.0), UC=np.where(t > 0, FN / t, 0.0),
                    LE=np.where(t > 0, FP / t, 0.0),
                    BPAC=np.where(d > 0, TP / d - np.abs(FN / d - FP / d), 0.0))


def boot(y, p, line, idx, old):
    if not old:
        return C.bootstrap_metrics(y, p, line, idx)
    a = (y < line)[idx]; q = (p < line)[idx]
    return old_metrics(*(x.sum(1).astype(float) for x in (a & q, ~a & q, a & ~q, ~a & ~q)))


def point_bpac(y, p, line, old):
    TP, FP, FN, TN = C.confusion(y, p, line)
    if old:
        d = TP + FP
        return TP / d - abs(FN / d - FP / d) if d else 0.0
    return C.metrics_from_counts(TP, FP, FN, TN)["BPAC"]


def old_cv_quantile(X, y, groups, line, msl, old):
    """Pre-freeze selection: 5-fold grouped CV on the training sample, 0.05 grid."""
    oof = np.zeros((len(y), len(OLD_GRID)))
    for k, (a, b) in enumerate(GroupKFold(5).split(X, y, groups)):
        m = C.make_model("QRF", seed=C.RANDOM_STATE + k).set_params(max_samples_leaf=msl)
        oof[b] = m.fit(X[a], y[a]).predict(X[b], quantiles=OLD_GRID)
    sc = [point_bpac(y, oof[:, j], line, old) for j in range(len(OLD_GRID))]
    return OLD_GRID[int(np.argmax(sc))]


def main():
    X, y, line = C.load_bolivia(verbose=False)
    X, y = X.values, y.values
    Xd = C.iris_design(X)
    rows = []
    for proto, fn in (("paper", C.paper_split_idx), ("disjoint", C.disjoint_split_idx)):
        tr, te = fn(len(y), C.RANDOM_STATE)
        idx = C.boot_indices(len(te))
        iris = C.make_model("IRIS_QR").fit(Xd[tr], y[tr]).predict(Xd[te])
        rf = C.make_model("RandomForest").fit(X[tr], y[tr])
        fits = {}
        for msl in (1, None):
            fits[msl] = C.make_model("QRF").set_params(max_samples_leaf=msl).fit(X[tr], y[tr])
        steps = [("0 pre-freeze", True, 1, "cv"), ("1 +C1 metrics", False, 1, "cv"),
                 ("2 +C2 all-leaf QRF", False, None, "cv"), ("3 +C3 OOB selection", False, None, "oob")]
        for step, old, msl, sel in steps:
            qrf = fits[msl]
            if sel == "cv":
                q = old_cv_quantile(X[tr], y[tr], tr, line, msl, old)
                sel_label, sel_pred = f"QRF({q:.2f})", qrf.predict(X[te], quantiles=q)
            else:
                lab, col, _ = C.select_se(y[tr], C.se_oob_predictions(rf, qrf, X[tr]), line)
                sel_label, sel_pred = lab, C.se_test_predictions(rf, qrf, X[te])[:, col]
            for name, p in (("IRIS QR(0.42)", iris),
                            ("QRF(0.40) fixed", qrf.predict(X[te], quantiles=0.40)),
                            ("QRF(0.41) fixed", qrf.predict(X[te], quantiles=0.41)),
                            (f"selected: {sel_label}", sel_pred)):
                b = boot(y[te], p, line, idx, old)
                rows.append(dict(protocol=proto, step=step, model=name,
                                 **{m: round(float(np.mean(b[m])), 4) for m in C.METRICS}))
            print(proto, step, sel_label, flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "correction_impact.csv"), index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
