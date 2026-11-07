"""
family_ranking.py — method-family ordering at every scanned threshold (manuscript §5.4).

Reads outputs/threshold_scan_metrics.csv (from threshold_scan.py); no model is fitted.
Writes outputs/threshold_scan_family_ranking.csv with, per protocol and threshold:
  family_order          BPAC order of the four families, "QRF" = best of the three QRF variants
                        (SE OOB-selected, QRF(0.40) fixed, QRF(0.41) fixed)
  worst_QRF_minus_IRIS  min over the three QRF variants of BPAC(QRF) - BPAC(IRIS)
  SE_minus_IRIS         BPAC(SE OOB-selected) - BPAC(IRIS QR(0.42))
  IRIS_minus_RF, RF_minus_DT

Added 2026-11-06: the stored CSV of 2026-11-04 had been produced ad hoc. This script
reproduces it (checked with pandas, see CODE_REVIEW.md).
"""
import os

import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
QRF = ["SE OOB-selected", "QRF(q=0.40) fixed", "QRF(q=0.41) fixed"]


def main():
    m = pd.read_csv(os.path.join(OUT, "threshold_scan_metrics.csv"))
    m = m[~m.model.str.startswith("paired")]
    p = m.pivot_table(index=["protocol", "threshold"], columns="model", values="BPAC", sort=False)
    rows = []
    for (proto, th), r in p.iterrows():
        fam = {"QRF": r[QRF].max(), "IRIS": r["IRIS_Q42"], "RF": r["RandomForest"], "DT": r["DecisionTree"]}
        order = " > ".join(sorted(fam, key=lambda k: -fam[k]))
        rows.append(dict(protocol=proto, threshold=th, family_order=order,
                         worst_QRF_minus_IRIS=(r[QRF] - r["IRIS_Q42"]).min(),
                         SE_minus_IRIS=r["SE OOB-selected"] - r["IRIS_Q42"],
                         IRIS_minus_RF=r["IRIS_Q42"] - r["RandomForest"],
                         RF_minus_DT=r["RandomForest"] - r["DecisionTree"]))
    df = pd.DataFrame(rows).sort_values(["protocol", "threshold"], kind="stable")
    df.to_csv(os.path.join(OUT, "threshold_scan_family_ranking.csv"), index=False)
    print(df.groupby("protocol").family_order.value_counts().to_string())


if __name__ == "__main__":
    main()
