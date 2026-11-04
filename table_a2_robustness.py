"""
table_a2_robustness.py — Phase 3: published Table A2 robustness analysis
(halved and doubled poverty lines), McBride & Nichols (2018), p.539 and Table A2 p.547.

Published definitions (p.539):
  * "two new poverty lines: one that is half the original poverty line and a
     second that is twice the original poverty line"
  * IRIS row: "the best possible results IRIS could have gotten using their
     methods and preferred tools by adapting those tools to obtain the greatest
     BPAC under the new poverty lines ... selection of the quantile that offers
     the best in-sample BPAC under the new poverty lines in Bolivia"
  * CV and SE rows: the paper's CV and stochastic-ensemble procedures, re-run
     under the new line.

Implementation:
  original line   = frozen 189.09 Bs (P24.2)  -> half 94.55, double 378.18
  IRIS (adapted)  = linear QR on the training sample; quantile 0.01..0.99 with
                    the best IN-SAMPLE (training) BPAC at the new line
                    [RECONSTRUCTED: "in-sample" read as the training sample]
  CV QR           = from cv_qr_baseline.py (500 x 3-fold CV, scores stored per line)
  SE              = frozen OOB-BPAC rule over RF + QRF(0.01..0.99) at the new line
  also reported   = frozen IRIS QR(0.42) unchanged (not re-tuned), as a reference
Evaluation: 1,000 bootstrap draws of the test sample (frozen), seed 42,
paper and disjoint protocols. Requires results/cv_qr/cv_scores.csv.

Outputs → results/table_a2/
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.linear_model import QuantileRegressor

import common as C

warnings.filterwarnings("ignore")
OUT = os.path.join(C.RESULTS_DIR, "table_a2")
os.makedirs(OUT, exist_ok=True)
GRID = C.QRF_QUANTILE_GRID
CV_SCORES = os.path.join(C.RESULTS_DIR, "cv_qr", "cv_scores.csv")
PROTOCOLS = {"paper": C.paper_split_idx, "disjoint": C.disjoint_split_idx}
PUBLISHED = pd.DataFrame([
    # Table A2, Bolivia (p.547): estimation, line, TA, PA, UC, LE, BPAC, poverty rate
    ("IRIS QR(0.22)", "half", 94.55, 41.65, 58.35, 65.89, 30.07, 4.92),
    ("CV QR(0.24)", "half", 94.53, 41.20, 58.80, 66.31, 29.65, 4.92),
    ("SE QRF(0.26)", "half", 94.39, 43.65, 56.35, 71.03, 26.94, 4.92),
    ("IRIS QR(0.54)", "double", 78.90, 82.64, 17.36, 16.65, 81.10, 62.26),
    ("CV QR(0.52)", "double", 79.01, 83.60, 16.40, 17.45, 81.92, 62.26),
    ("SE QRF(0.54)", "double", 77.89, 83.66, 16.34, 19.32, 80.62, 62.26),
], columns=["model", "line", "TA", "PA", "UC", "LE", "BPAC", "poverty_rate"])


def qr_fit_predict(Xtr, ytr, Xte, q):
    m = QuantileRegressor(quantile=q, alpha=0.0, solver="highs").fit(Xtr, ytr)
    return m.predict(Xtr), m.predict(Xte)


def main():
    if not os.path.exists(CV_SCORES):
        sys.exit("run cv_qr_baseline.py first")
    cv = pd.read_csv(CV_SCORES)
    X, y, base = C.load_bolivia(verbose=False)
    Xv, Xd, y = X.values, C.iris_design(X.values), y.values
    lines = {"base": base, "half": base / 2, "double": base * 2}
    rows, cms = [], []
    for proto, split in PROTOCOLS.items():
        tr, te = split(len(y), C.RANDOM_STATE)
        idx = C.boot_indices(len(te))
        # linear QR at every grid quantile, fitted once on the training sample
        fits = Parallel(n_jobs=-1)(delayed(qr_fit_predict)(Xd[tr], y[tr], Xd[te], q) for q in GRID)
        qr_in = np.column_stack([f[0] for f in fits]); qr_te = np.column_stack([f[1] for f in fits])
        # frozen SE candidates
        rf = C.make_model("RandomForest").fit(Xv[tr], y[tr])
        qrf = C.make_model("QRF").fit(Xv[tr], y[tr])
        se_oob, se_te = C.se_oob_predictions(rf, qrf, Xv[tr]), C.se_test_predictions(rf, qrf, Xv[te])
        for lab, l in lines.items():
            q_iris, _ = C.best_quantile(y[tr], qr_in, l)                       # in-sample best
            sub = cv[(cv.protocol == proto) & (cv.line == lab)].sort_values("q")
            q_cv = float(sub.q.iloc[int(np.argmax(sub.cv_bpac.values))])
            se_label, se_col, _ = C.select_se(y[tr], se_oob, l)
            models = {f"IRIS QR({q_iris:.2f}) in-sample best": qr_te[:, GRID.index(q_iris)],
                      f"CV QR({q_cv:.2f})": qr_te[:, GRID.index(round(q_cv, 2))],
                      f"SE {se_label}": se_te[:, se_col],
                      "IRIS QR(0.42) not re-tuned": qr_te[:, GRID.index(0.42)]}
            for name, p in models.items():
                b = C.bootstrap_metrics(y[te], p, l, idx)
                s, se = C.summarise(b), C.boot_se(b)
                rows.append(dict(protocol=proto, line=lab, line_value=round(l, 2),
                                 poverty_rate_full=float((y < l).mean()),
                                 poverty_rate_test=float((y[te] < l).mean()), model=name,
                                 **{m: s[m][0] for m in C.METRICS},
                                 **{f"{m}_SE": se[m] for m in C.METRICS},
                                 **{f"{m}_lo": s[m][1] for m in C.METRICS},
                                 **{f"{m}_hi": s[m][2] for m in C.METRICS}))
                pt = C.targeting_metrics(y[te], p, l)
                cms.append(dict(protocol=proto, line=lab, model=name,
                                **{k: pt[k] for k in ("TP", "FP", "FN", "TN")}))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "table_a2_results.csv"), index=False)
    pd.DataFrame(cms).to_csv(os.path.join(OUT, "table_a2_confusion.csv"), index=False)
    PUBLISHED.to_csv(os.path.join(OUT, "table_a2_published_bolivia.csv"), index=False)
    pd.set_option("display.width", 250)
    print(df[["protocol", "line", "line_value", "poverty_rate_full", "model", "TA", "PA", "UC",
              "LE", "BPAC", "BPAC_lo", "BPAC_hi"]].round(4).to_string(index=False))
    print("\nPublished (Table A2, Bolivia):\n" + PUBLISHED.to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
