"""
Step 5a — continuous poverty-threshold sensitivity scan, 170–210 Bs.

Frozen methodology and data construction, unchanged: models come from
sensitivity_analysis.fit_predict (DT, RF, IRIS QR(0.42), RF+QRF candidates)
fitted once per split. Only the classification line changes. The SE model is
re-selected at each line by OOB BPAC on the training sample (frozen rule [S7]);
IRIS QR(0.42) and the fixed QRF quantiles are not re-tuned.

Splits: seed 42, published protocol (paper) and disjoint protocol (frozen
split functions). 1,000 test bootstrap draws (frozen BOOT_SEED) per threshold.
CV-QR is NOT included: its quantile choice needs a 40-min CV per line.

Pre-declared ranking rule: at each threshold, rank the models by point BPAC on
the full test sample. A "ranking change" is any ordering different from the
ordering at the frozen line (189.09 Bs). A change is "material" only if the two
models whose order flips differ by more than 0.010 BPAC (the tolerance used in
earlier audits).

Usage (from Model_Training/):
  python3 audit_2026-11-04_step5_threshold_scan/scripts/threshold_scan.py
Writes only to audit_2026-11-04_step5_threshold_scan/outputs/.
"""
import itertools
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
import sensitivity_analysis as SA  # noqa: E402  (functions only)

OUT = os.path.join(AUDIT, "outputs")
os.makedirs(OUT, exist_ok=True)
THRESHOLDS = [round(float(t), 1) for t in np.arange(170.0, 210.01, 0.5)]
MODELS = ["SE OOB-selected", "QRF(q=0.40) fixed", "QRF(q=0.41) fixed", "IRIS_Q42", "RandomForest", "DecisionTree"]
TOL = 0.010


def main():
    t0 = time.time()
    X, y, base = C.load_bolivia(verbose=False)
    X, y = X.values, y.values
    lines = sorted(set(THRESHOLDS) | {round(base, 4)})
    rows = []
    for proto, split in SA.PROTOCOLS.items():
        tr, te = split(len(y), C.RANDOM_STATE)
        preds, se_test, se_oob = SA.fit_predict(X, y, tr, te, C.RANDOM_STATE)
        idx = C.boot_indices(len(te))
        for l in lines:
            mp, se_label, _ = SA.model_preds_for_threshold(preds, se_test, se_oob, y[tr], y[te], l)
            boots = {}
            for name in MODELS:
                p = mp[name]
                pt = C.targeting_metrics(y[te], p, l)
                b = C.bootstrap_metrics(y[te], p, l, idx); boots[name] = b
                lo, hi = C.ci(b["BPAC"])
                rows.append(dict(protocol=proto, threshold=l, is_frozen_line=abs(l - base) < 1e-3,
                                 rate_full=float((y < l).mean()), rate_test=float((y[te] < l).mean()),
                                 model=name, se_selected=se_label if name == "SE OOB-selected" else "",
                                 **{m: pt[m] for m in C.METRICS},
                                 BPAC_boot_mean=float(b["BPAC"].mean()), BPAC_lo=lo, BPAC_hi=hi))
            d = boots["SE OOB-selected"]["BPAC"] - boots["IRIS_Q42"]["BPAC"]
            rows.append(dict(protocol=proto, threshold=l, is_frozen_line=abs(l - base) < 1e-3,
                             model="paired: SE - IRIS_Q42", BPAC=float(np.mean(d)),
                             BPAC_lo=C.ci(d)[0], BPAC_hi=C.ci(d)[1]))
        print(f"[{proto}] done ({time.time()-t0:.0f}s)", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "threshold_scan_metrics.csv"), index=False)

    # rankings
    rk = []
    for proto in SA.PROTOCOLS:
        sub = df[(df.protocol == proto) & df.model.isin(MODELS)]
        ref_l = sub[sub.is_frozen_line].threshold.iloc[0]
        ref = sub[sub.threshold == ref_l].sort_values("BPAC", ascending=False).model.tolist()
        for l, g in sub.groupby("threshold"):
            g = g.set_index("model")
            order = g.sort_values("BPAC", ascending=False).index.tolist()
            flips = [(a, b) for a, b in itertools.combinations(ref, 2) if order.index(a) > order.index(b)]
            material = [(a, b) for a, b in flips if abs(g.loc[a, "BPAC"] - g.loc[b, "BPAC"]) > TOL]
            rk.append(dict(protocol=proto, threshold=l, ranking=" > ".join(order),
                           changed_vs_frozen=bool(flips), material_change=bool(material),
                           material_flips="; ".join(f"{a} vs {b}" for a, b in material),
                           top_model=order[0], se_selected=g.loc["SE OOB-selected", "se_selected"]))
    rk = pd.DataFrame(rk)
    rk.to_csv(os.path.join(OUT, "threshold_scan_rankings.csv"), index=False)
    summary = (rk.groupby("protocol").agg(n_thresholds=("threshold", "size"),
                                          n_any_change=("changed_vs_frozen", "sum"),
                                          n_material_change=("material_change", "sum"),
                                          top_models=("top_model", lambda s: dict(s.value_counts())),
                                          se_choices=("se_selected", lambda s: dict(s.value_counts().sort_index()))))
    summary.to_csv(os.path.join(OUT, "threshold_scan_ranking_summary.csv"))
    pd.set_option("display.width", 250)
    print(summary.to_string())
    print(rk[rk.material_change][["protocol", "threshold", "material_flips"]].to_string(index=False))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
