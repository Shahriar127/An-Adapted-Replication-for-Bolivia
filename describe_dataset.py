"""
describe_dataset.py — descriptive statistics of the analysis sample (Bolivia EH 2005).

Read-only with respect to the frozen pipeline: it uses common.load_bolivia() (the
same data construction as every result) and writes AGGREGATE statistics only.
No household-level record is written, so the outputs may be redistributed.

Outputs → results/dataset/
  descriptive_statistics.csv   one row per feature + target: mean, SD, min, P25, median, P75, max, share non-zero
  sample_summary.csv           N, poverty line, poverty rates, welfare quantiles, urban/rural split
"""
import os

import numpy as np
import pandas as pd

import common as C

OUT = os.path.join(C.RESULTS_DIR, "dataset")
os.makedirs(OUT, exist_ok=True)

LABELS = {
    "hhsize": "Household size (members)",
    "hhsize2": "Household size squared",
    "age_head": "Age of household head (years)",
    "age_head2": "Age of head squared",
    "regions": "Department (1-9; ordinal code)",
    "rural": "Rural area (0/1)",
    "sublease": "Rented dwelling, proxy for 'sublease' (0/1)",
    "brick_wall": "Brick/cement-block walls (0/1)",
    "wood_wall": "Wood walls (0/1)",
    "dirt_floor": "Dirt floor (0/1)",
    "cement_floor": "Cement floor (0/1)",
    "fridge": "Owns refrigerator/freezer (0/1)",
    "radio": "Owns radio/recorder (0/1)",
    "tv": "Owns television (0/1)",
    "dvd": "Owns video/DVD player (0/1)",
    "fan": "Owns fan (0/1)",
    "car": "Owns car (0/1)",
    "num_beds": "Number of beds",
    "num_kitchens": "Separate kitchen room (0/1; proxy for 'number of kitchens')",
    "num_computers": "Number of computers",
    "sheep": "Number of sheep",
    "G_TOTAL_pc": "TARGET: monthly per-capita household expenditure (Bs)",
}


def main():
    X, y, line = C.load_bolivia(verbose=False)
    df = X.copy()
    df["G_TOTAL_pc"] = y.values
    rows = []
    for col in list(C.FEATURE_COLS) + ["G_TOTAL_pc"]:
        v = df[col].astype(float)
        rows.append(dict(variable=col, description=LABELS[col], mean=v.mean(), sd=v.std(ddof=1),
                         min=v.min(), p25=v.quantile(0.25), median=v.median(),
                         p75=v.quantile(0.75), max=v.max(), share_nonzero=(v != 0).mean(),
                         n_missing=int(v.isna().sum())))
    pd.DataFrame(rows).round(4).to_csv(os.path.join(OUT, "descriptive_statistics.csv"), index=False)

    yv = y.values.astype(float)
    p2403 = float(np.percentile(yv, 24.03))
    summ = [
        ("N households", len(yv)),
        ("N features", len(C.FEATURE_COLS)),
        ("poverty line P24.2 (Bs/person/month, frozen)", line),
        ("poverty rate at P24.2", float((yv < line).mean())),
        ("poverty line P24.03 (Bs, sensitivity)", p2403),
        ("rate at half the P24.2 line", float((yv < line / 2).mean())),
        ("rate at double the P24.2 line", float((yv < line * 2).mean())),
        ("households with G_TOTAL_pc == 0", int((yv == 0).sum())),
        ("share rural", float(df["rural"].mean())),
        ("welfare P10 (Bs)", float(np.percentile(yv, 10))),
        ("welfare P50 (Bs)", float(np.percentile(yv, 50))),
        ("welfare P90 (Bs)", float(np.percentile(yv, 90))),
        ("welfare mean (Bs)", float(yv.mean())),
    ]
    pd.DataFrame(summ, columns=["item", "value"]).to_csv(os.path.join(OUT, "sample_summary.csv"), index=False)
    print(pd.DataFrame(summ, columns=["item", "value"]).to_string(index=False))
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
