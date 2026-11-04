"""
Phase 3 — poverty-rate sensitivity: frozen 24.2% (primary, unchanged) vs 24.03%.

The published article is internally inconsistent: text p.538 says "24.2 percent
in Bolivia", Table 3 p.538 says 24.03%, and Table A1 row 5 implies 24.038%
through TA = 1 - p(UC + LE).

Runs the frozen primary model set (sensitivity_analysis.fit_predict /
model_preds_for_threshold, unchanged) at both lines for seed 42 (bootstrap) and
30 repeated splits (seeds 1000-1029), for both protocols. The 24.2% numbers must
reproduce the stored results/sensitivity output exactly (reproducibility check).
CV-QR at 24.03% comes from the Phase 1 per-split files.

Writes only to audit_2026-11-04_repeated_split/outputs/poverty_rate/.
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
import sensitivity_analysis as SA  # noqa: E402  (functions only; its main() is not called)

OUT = os.path.join(AUDIT, "outputs", "poverty_rate")
os.makedirs(OUT, exist_ok=True)


def main():
    t0 = time.time()
    X, y, base = C.load_bolivia(verbose=False)
    X, y = X.values, y.values
    lines = {"P24.2 (frozen)": base, "P24.03": float(np.percentile(y, 24.03))}
    pd.DataFrame([dict(label=k, line_bs=v, rate_full_sample=float((y < v).mean())) for k, v in lines.items()]
                 ).to_csv(os.path.join(OUT, "lines.csv"), index=False)
    rows = []
    for proto, split in SA.PROTOCOLS.items():
        for seed in [C.RANDOM_STATE] + list(range(1000, 1030)):
            tr, te = split(len(y), seed)
            preds, se_test, se_oob = SA.fit_predict(X, y, tr, te, seed)
            idx = C.boot_indices(len(te)) if seed == C.RANDOM_STATE else None
            for lab, l in lines.items():
                mp, se_label, q_te = SA.model_preds_for_threshold(preds, se_test, se_oob, y[tr], y[te], l)
                for name, p in mp.items():
                    pt = C.targeting_metrics(y[te], p, l)
                    r = dict(protocol=proto, seed=seed, line=lab, line_bs=l, model=name,
                             se_selected=se_label, test_selected_q=q_te,
                             test_rate=float((y[te] < l).mean()), **{m: pt[m] for m in C.METRICS})
                    if idx is not None:
                        b = C.bootstrap_metrics(y[te], p, l, idx)
                        r.update({f"{m}_boot_mean": float(b[m].mean()) for m in C.METRICS})
                    rows.append(r)
            print(f"[{proto}] seed {seed} done ({time.time()-t0:.0f}s)", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "poverty_rate_per_split.csv"), index=False)

    # reproducibility check against the stored frozen sensitivity run (seeds 1000-1029)
    stored = pd.read_csv(os.path.join(ROOT, "results", "sensitivity", "repeated_splits_raw.csv"))
    smap = {"189.09 (full-sample P24.2)": "P24.2 (frozen)", "188.77 (full-sample P24.03, published Table 3)": "P24.03"}
    stored = stored[stored.threshold.isin(smap)].assign(line=lambda d: d.threshold.map(smap))
    mine = df[df.seed != C.RANDOM_STATE]
    mrg = mine.merge(stored, on=["protocol", "seed", "line", "model"], suffixes=("", "_stored"))
    diffs = {m: float((mrg[m] - mrg[f"{m}_stored"]).abs().max()) for m in C.METRICS}
    check = dict(rows_compared=len(mrg), expected=len(mine), max_abs_diff=diffs,
                 se_choice_identical=bool((mrg.se_selected == mrg.se_choice).all()))
    pd.Series(check).to_json(os.path.join(OUT, "repro_check_vs_results_sensitivity.json"), indent=2)
    print("repro check:", check)

    rep = df[df.seed != C.RANDOM_STATE]
    w = rep.pivot_table(index=["protocol", "model", "seed"], columns="line", values=list(C.METRICS))
    summ = []
    for (proto, model), g in w.groupby(level=[0, 1]):
        for m in C.METRICS:
            d = g[(m, "P24.03")] - g[(m, "P24.2 (frozen)")]
            summ.append(dict(protocol=proto, model=model, metric=m,
                             mean_P24_2=g[(m, "P24.2 (frozen)")].mean(), mean_P24_03=g[(m, "P24.03")].mean(),
                             diff_mean=d.mean(), diff_sd=d.std(ddof=1), diff_max_abs=d.abs().max()))
    pd.DataFrame(summ).to_csv(os.path.join(OUT, "poverty_rate_summary.csv"), index=False)
    sel = (rep[rep.model == "SE OOB-selected"].drop_duplicates(["protocol", "seed", "line"])
           .pivot_table(index=["protocol", "seed"], columns="line", values="se_selected", aggfunc="first"))
    sel["same_choice"] = sel["P24.03"] == sel["P24.2 (frozen)"]
    sel.to_csv(os.path.join(OUT, "se_selection_by_line.csv"))
    print(sel.groupby(level=0).same_choice.agg(["sum", "count"]))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
