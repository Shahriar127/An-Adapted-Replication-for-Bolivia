"""
Step 5b — quantile path q = 0.30 … 0.50 (step 0.01) on the existing DISJOINT
split (frozen disjoint_split_idx, seed 42), frozen line 189.09 Bs.

Two model families from the frozen methodology, no new models:
  * QRF: one frozen QRF fit (C.make_model("QRF")), predicted at each q
  * linear QR: the frozen IRIS design and solver (C.make_model("IRIS_QR")),
    refitted at each q (the IRIS / CV-QR family)
Test metrics (TA, PA, UC, LE, BPAC) are point estimates plus 95% bootstrap CIs
(1,000 draws, frozen BOOT_SEED). Training-only selection curves are recorded too:
  * QRF: OOB BPAC on the training sample (frozen SE rule)
  * linear QR: mean CV BPAC from the stored 500 x 3-fold run
    (results/cv_qr/cv_scores.csv, disjoint, base line; read-only)

NOTE: under the published metric definition PA = TP/(TP+FN) and
UC = FN/(TP+FN), so PA + UC = 1 identically. The script asserts this.

Usage (from Model_Training/):
  python3 audit_2026-11-04_step5_quantile_path/scripts/quantile_path.py
Writes only to audit_2026-11-04_step5_quantile_path/outputs/.
"""
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
ROOT = os.path.dirname(AUDIT)
sys.path.insert(0, ROOT)
import common as C  # noqa: E402

OUT = os.path.join(AUDIT, "outputs")
os.makedirs(OUT, exist_ok=True)
QS = [round(0.30 + 0.01 * i, 2) for i in range(21)]


def main():
    t0 = time.time()
    X, y, line = C.load_bolivia(verbose=False)
    Xv, Xd, y = X.values, C.iris_design(X.values), y.values
    tr, te = C.disjoint_split_idx(len(y), C.RANDOM_STATE)
    idx = C.boot_indices(len(te))
    qrf = C.make_model("QRF", C.RANDOM_STATE).fit(Xv[tr], y[tr])
    qrf_te = qrf.predict(Xv[te], quantiles=QS)
    qrf_oob = qrf.predict(Xv[tr], quantiles=QS, oob_score=True)
    cv = pd.read_csv(os.path.join(ROOT, "results", "cv_qr", "cv_scores.csv"))
    cv = cv[(cv.protocol == "disjoint") & (cv.line == "base")].set_index("q").cv_bpac
    rows = []
    for j, q in enumerate(QS):
        lin = C.make_model("IRIS_QR").set_params(quantile=q).fit(Xd[tr], y[tr])
        for fam, p, sel in (("QRF", qrf_te[:, j], C.targeting_metrics(y[tr], qrf_oob[:, j], line)["BPAC"]),
                            ("linear QR", lin.predict(Xd[te]), float(cv.loc[q]))):
            pt = C.targeting_metrics(y[te], p, line)
            assert abs(pt["PA"] + pt["UC"] - 1) < 1e-12, "PA + UC must equal 1"
            b = C.bootstrap_metrics(y[te], p, line, idx)
            r = dict(family=fam, q=q, training_selection_bpac=sel,
                     selection_criterion="OOB BPAC (training)" if fam == "QRF" else "mean CV BPAC (training, 500x3)",
                     **{m: pt[m] for m in C.METRICS})
            for m in C.METRICS:
                r[f"{m}_lo"], r[f"{m}_hi"] = C.ci(b[m])
            rows.append(r)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "quantile_path_metrics.csv"), index=False)
    best = (df.loc[df.groupby("family").training_selection_bpac.idxmax(), ["family", "q", "BPAC"]]
            .rename(columns={"q": "q_selected_on_training", "BPAC": "test_BPAC_at_selected_q"}))
    test_best = (df.loc[df.groupby("family").BPAC.idxmax(), ["family", "q", "BPAC"]]
                 .rename(columns={"q": "q_best_on_test_hindsight", "BPAC": "test_BPAC_max"}))
    summ = best.merge(test_best, on="family")
    summ.to_csv(os.path.join(OUT, "quantile_path_selection_summary.csv"), index=False)
    wide = df.pivot(index="q", columns="family", values="BPAC")
    wide["QRF_minus_linearQR"] = wide["QRF"] - wide["linear QR"]
    wide.to_csv(os.path.join(OUT, "quantile_path_bpac_by_family.csv"))
    pd.set_option("display.width", 200)
    print(summ.to_string(index=False)); print(wide.round(4).to_string())
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
