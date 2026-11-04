"""Render results/sensitivity/*.csv into results/sensitivity/SUMMARY.md."""
import os
import pandas as pd
import common as C

D = os.path.join(C.RESULTS_DIR, "sensitivity")
P = pd.read_csv(os.path.join(D, "primary_metrics_bootstrap_ci.csv"))
DF = pd.read_csv(os.path.join(D, "primary_paired_differences.csv"))
QS = pd.read_csv(os.path.join(D, "primary_quantile_selection.csv"))
out = ["# Sensitivity analysis — Bolivia EH 2005", "",
       "Mean of 1000 bootstrap re-draws of the test sample, 95% percentile CI in brackets.",
       "Seed 42. `paper` = overlapping N/2 bootstrap split; `disjoint` = untouched 50/50 test set.", ""]


def cell(r, m):
    return f"{r[m]:.3f} [{r[m+'_lo']:.3f}, {r[m+'_hi']:.3f}]"


for proto in ("paper", "disjoint"):
    out += [f"## Protocol: {proto}", ""]
    for th in P.threshold.unique():
        sub = P[(P.protocol == proto) & (P.threshold == th)]
        out += [f"### Threshold {th} — test poverty rate {sub.test_poverty_rate.iloc[0]:.2%}", "",
                "| Model | PA | UC | LE | BPAC |", "|---|---|---|---|---|"]
        out += [f"| {r.model} | " + " | ".join(cell(r, m) for m in ("PA", "UC", "LE", "BPAC")) + " |"
                for _, r in sub.iterrows()]
        out.append("")

out += ["## Step 2 — paired difference QRF(40) − QRF(45)", "",
        "| Protocol | Threshold | Metric | Diff | 95% CI | CI excludes 0 |", "|---|---|---|---|---|---|"]
for _, r in DF[DF.comparison == "QRF(40) - QRF(45)"].iterrows():
    if r.metric in ("PA", "UC", "LE", "BPAC"):
        out.append(f"| {r.protocol} | {r.threshold} | {r.metric} | {r['diff']:+.4f} | "
                   f"[{r.lo:+.4f}, {r.hi:+.4f}] | {'yes' if r.excludes_zero else 'no'} |")

out += ["", "## Step 3 — paired difference vs 189.09 Bs (same model, same test resamples)", "",
        "| Protocol | Model | Change | Metric | Diff | 95% CI | CI excludes 0 |",
        "|---|---|---|---|---|---|---|"]
th = DF[DF.comparison != "QRF(40) - QRF(45)"]
for _, r in th[th.metric.isin(["PA", "UC", "LE", "BPAC"])].iterrows():
    out.append(f"| {r.protocol} | {r.comparison.replace(': threshold','')} | "
               f"{r.threshold.split(' (')[0]} − 189.09 | {r.metric} | {r['diff']:+.4f} | "
               f"[{r.lo:+.4f}, {r.hi:+.4f}] | {'yes' if r.excludes_zero else 'no'} |")

out += ["", "## Quantile selected (seed 42)", "", QS.to_markdown(index=False), ""]

rs = os.path.join(D, "repeated_splits_summary.csv")
if os.path.exists(rs):
    R = pd.read_csv(rs)
    n = pd.read_csv(os.path.join(D, "repeated_splits_raw.csv")).seed.nunique()
    out += [f"## Repeated splits — mean (SD) of point metrics over {n} random splits per protocol", "",
            "| Protocol | Threshold | Model | PA | UC | LE | BPAC |", "|---|---|---|---|---|---|---|"]
    for _, r in R.iterrows():
        out.append(f"| {r.protocol} | {r.threshold.split(' (')[0]} | {r.model} | " +
                   " | ".join(f"{r[m+'_mean']:.3f} ({r[m+'_std']:.3f})"
                              for m in ("PA", "UC", "LE", "BPAC")) + " |")
    Q = pd.read_csv(os.path.join(D, "repeated_splits_quantile_choice.csv"))
    out += ["", "### Quantile chosen across splits (value: count)", "", Q.to_markdown(index=False)]

open(os.path.join(D, "SUMMARY.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
