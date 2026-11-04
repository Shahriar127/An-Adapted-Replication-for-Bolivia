"""
a8_data_diagnostics.py — Phase 1 (A8): model-free and deterministic checks of
whether our data construction matches the authors'. These checks involve no
random split.

1. Poverty rate implied by published Table A1 row 5 (in-sample, full sample):
   TA = 1 - p*(UC + LE)  =>  p = (1 - TA) / (UC + LE)
2. Published row 5 refit: QR(0.42) fitted and evaluated in-sample on the full
   sample, for the frozen target and a pre-specified set of target, threshold
   and design variants.
3. Distribution fingerprint: poverty rates at half and double the line
   (published Table A2, Bolivia: 4.92% and 62.26%) for the welfare aggregates
   available in the EH 2005 file.

Writes results/a8_audit/a8_data_diagnostics_*.csv. Changes nothing else.
"""
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import QuantileRegressor

import common as C

OUT = os.path.join(C.RESULTS_DIR, "a8_audit")
os.makedirs(OUT, exist_ok=True)
ROW5 = dict(TA=82.45, PA=60.69, UC=39.30, LE=33.71, BPAC=55.10)


def main():
    # 1. implied poverty rate
    p = (1 - ROW5["TA"] / 100) / ((ROW5["UC"] + ROW5["LE"]) / 100)
    pd.DataFrame([dict(source="Table A1 row 5 (Bolivia, in-sample full)", implied_rate=round(100 * p, 3),
                       text_p538=24.2, table3_p538=24.03)]).to_csv(
        os.path.join(OUT, "a8_data_diagnostics_implied_rate.csv"), index=False)
    print(f"implied poverty rate from row 5: {100*p:.3f}%")

    # 2. row-5 refits
    dm, _, de, dp = C.load_raw()
    hh = C.clean(C.build_household_frame(dm, de, dp))
    extra = dm.groupby("folio")[["y_percapB", "z"]].first().reset_index()
    hh = hh.merge(extra, on="folio", how="left")
    Xv = hh[C.FEATURE_COLS].values.astype(float)
    ri = C.FEATURE_COLS.index("regions")
    designs = {"8 dummies (frozen)": C.iris_design(Xv), "ordinal regions": Xv,
               "no regions": np.delete(Xv, ri, axis=1)}
    rows = []
    for tname in ("G_TOTAL_pc", "y_percapB"):
        y = hh[tname].astype(float).values
        for thr in ("P24.03", "P24.2", "median-of-poor(z)"):
            line = (np.percentile(y, 24.03) if thr == "P24.03" else np.percentile(y, 24.2)
                    if thr == "P24.2" else np.median(y[y < hh.z.values]))
            for dname, D in designs.items():
                for tr_name, fwd, inv in (("level", lambda v: v, lambda v: v),
                                          ("log(1+y)", np.log1p, np.expm1)):
                    if tname == "y_percapB" and (dname != "8 dummies (frozen)" or tr_name != "level"):
                        continue
                    m = QuantileRegressor(quantile=0.42, alpha=0, solver="highs").fit(D, fwd(y))
                    mm = C.targeting_metrics(y, inv(m.predict(D)), line)
                    r = dict(target=tname, threshold=thr, design=dname, transform=tr_name,
                             rate=round(100 * float((y < line).mean()), 2),
                             **{k: round(100 * mm[k], 2) for k in ROW5})
                    r["L1_distance_to_row5"] = round(sum(abs(r[k] - ROW5[k]) for k in ROW5), 2)
                    rows.append(r)
    df = pd.DataFrame(rows).sort_values("L1_distance_to_row5")
    df.to_csv(os.path.join(OUT, "a8_data_diagnostics_row5.csv"), index=False)
    print(df.head(8).to_string(index=False)); print("published row 5:", ROW5)

    # 3. distribution fingerprint
    h = dm.groupby("folio").first(); n = h.miembros
    cands = {"G_TOTAL_pc (frozen)": h.G_TOTAL_pc, "G_TOTAL household": h.G_TOTAL,
             "G_TOTAL_pc - G_VIVIENDA_pc": h.G_TOTAL_pc - h.G_VIVIENDA_pc,
             "G_TOTAL_pc - G_EDUCACION_pc": h.G_TOTAL_pc - h.G_EDUCACION_pc,
             "G_ALIMENTOS_pc": h.G_ALIMENTOS_pc,
             "G_ALIM_DENTRO_pc + G_NO_ALIMENTARIO_pc": h.G_ALIM_DENTRO_pc + h.G_NO_ALIMENTARIO_pc,
             "G_TOTAL / sqrt(hhsize)": h.G_TOTAL / np.sqrt(n),
             "G_TOTAL / hhsize^0.75": h.G_TOTAL / n ** 0.75, "y_percapB (income)": h.y_percapB}
    fp = []
    for k, v in cands.items():
        v = v.astype(float).values
        for base in (24.03, 24.2):
            l = np.percentile(v, base)
            half, dbl = 100 * (v < l / 2).mean(), 100 * (v < 2 * l).mean()
            fp.append(dict(aggregate=k, base_percentile=base, half_rate=round(half, 2),
                           double_rate=round(dbl, 2),
                           L1_distance=round(abs(half - 4.92) + abs(dbl - 62.26), 2)))
    fp = pd.DataFrame(fp).sort_values("L1_distance")
    fp.to_csv(os.path.join(OUT, "a8_data_diagnostics_fingerprint.csv"), index=False)
    print(fp.head(6).to_string(index=False)); print("published Table A2: half 4.92  double 62.26")


if __name__ == "__main__":
    main()
