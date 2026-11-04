"""
paired_comparisons.py — the published Table 4 contrasts (CV vs IRIS, SE vs IRIS,
CV vs SE) at the base poverty line, estimated with PAIRED bootstrap confidence
intervals instead of Tukey-Kramer tests (Tukey-Kramer is out of scope).

Why paired bootstrap:
  * All models are evaluated on the SAME test households. The 1,000 bootstrap
    resamples (frozen BOOT_SEED) are shared, so for each resample b the
    difference d_b = metric_A(b) - metric_B(b) is computed on identical
    households. The 2.5th/97.5th percentiles of d_b give a CI for the
    difference that accounts for the positive correlation between the two
    models' errors. Unpaired comparisons ignore that correlation and are
    conservative.
  * Tukey-Kramer as used in the paper (Table 4) treats the 1,000 bootstrap
    replicates as independent observations. Their number is chosen by the
    analyst, so test statistics such as t = 37.55 grow with B and do not
    measure sampling uncertainty.
  * Limitation: the CI covers test-sample uncertainty for ONE fitted model per
    method. It does not cover training-sample or split variation. That is
    covered separately by the repeated-split analysis in results/sensitivity/.

Requires results/cv_qr/cv_scores.csv. Output → results/cv_qr/paired_comparisons.csv
"""
import os

import numpy as np
import pandas as pd

import common as C

OUT = os.path.join(C.RESULTS_DIR, "cv_qr")
PUBLISHED_T4 = {  # Bolivia, Table 4 p.542 (percentage points; * = significant at 1%)
    ("CV - IRIS", "PA"): "5.79*", ("SE - IRIS", "PA"): "-2.25*", ("CV - SE", "PA"): "8.04*",
    ("CV - IRIS", "BPAC"): "8.61*", ("SE - IRIS", "BPAC"): "0.85", ("CV - SE", "BPAC"): "7.76*",
}


def main():
    cv = pd.read_csv(os.path.join(OUT, "cv_scores.csv"))
    X, y, line = C.load_bolivia(verbose=False)
    Xv, Xd, y = X.values, C.iris_design(X.values), y.values
    rows = []
    for proto, split in (("paper", C.paper_split_idx), ("disjoint", C.disjoint_split_idx)):
        tr, te = split(len(y), C.RANDOM_STATE)
        idx = C.boot_indices(len(te))
        sub = cv[(cv.protocol == proto) & (cv.line == "base")].sort_values("q")
        q_cv = float(sub.q.iloc[int(np.argmax(sub.cv_bpac.values))])
        preds = {
            "IRIS": C.make_model("IRIS_QR").fit(Xd[tr], y[tr]).predict(Xd[te]),
            "CV": C.make_model("IRIS_QR").set_params(quantile=q_cv).fit(Xd[tr], y[tr]).predict(Xd[te]),
        }
        rf = C.make_model("RandomForest").fit(Xv[tr], y[tr])
        qrf = C.make_model("QRF").fit(Xv[tr], y[tr])
        lab, col, _ = C.select_se(y[tr], C.se_oob_predictions(rf, qrf, Xv[tr]), line)
        preds["SE"] = C.se_test_predictions(rf, qrf, Xv[te])[:, col]
        boots = {k: C.bootstrap_metrics(y[te], p, line, idx) for k, p in preds.items()}
        for a, b in (("CV", "IRIS"), ("SE", "IRIS"), ("CV", "SE")):
            for m in C.METRICS:
                d = boots[a][m] - boots[b][m]
                lo, hi = C.ci(d)
                rows.append(dict(protocol=proto, contrast=f"{a} - {b}", metric=m,
                                 models=f"CV QR({q_cv:.2f}) / SE {lab} / IRIS QR(0.42)",
                                 diff=float(d.mean()), lo=lo, hi=hi,
                                 ci_excludes_0=bool(lo > 0 or hi < 0),
                                 share_resamples_positive=float((d > 0).mean()),
                                 published_table4=PUBLISHED_T4.get((f"{a} - {b}", m), "")))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "paired_comparisons.csv"), index=False)
    pd.set_option("display.width", 220)
    print(df[df.metric.isin(["PA", "BPAC"])].drop(columns="models").round(4).to_string(index=False))


if __name__ == "__main__":
    main()
