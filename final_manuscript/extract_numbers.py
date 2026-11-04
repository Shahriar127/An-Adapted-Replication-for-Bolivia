"""
Read-only extraction of every number cited in MANUSCRIPT.md from existing
result files. No model is fitted; nothing outside final_manuscript/ is written.

Output: final_manuscript/evidence_numbers.csv  (key, value, source, selector)
Usage (from Model_Training/): python3 final_manuscript/extract_numbers.py
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(ROOT, *p)  # noqa: E731
rows = []


def put(key, value, source, selector=""):
    rows.append(dict(key=key, value=value, source=source, selector=selector))


# ── data / threshold ─────────────────────────────────────────────────────────
cfg = json.load(open(R("results", "sensitivity", "config.json")))
put("poverty_rate_frozen", cfg["POVERTY_RATE"], "results/sensitivity/config.json", "POVERTY_RATE")
pq = pd.read_csv(R("results", "sensitivity", "primary_quantile_selection.csv"))
put("line_P24.2", pq[pq.threshold.str.startswith("189.09")].line.iloc[0],
    "results/sensitivity/primary_quantile_selection.csv", "threshold 189.09")
put("line_P24.03", pq[pq.threshold.str.startswith("188.77")].line.iloc[0],
    "results/sensitivity/primary_quantile_selection.csv", "threshold 188.77")
ir = pd.read_csv(R("results", "a8_audit", "a8_data_diagnostics_implied_rate.csv"))
put("implied_rate_row5", ir.implied_rate.iloc[0], "results/a8_audit/a8_data_diagnostics_implied_rate.csv")

# ── main comparison (seed 42, bootstrap means & CIs) ────────────────────────
pm = pd.read_csv(R("results", "sensitivity", "primary_metrics_bootstrap_ci.csv"))
pm = pm[pm.threshold.str.startswith("189.09")]
for _, r in pm.iterrows():
    for m in ("TA", "PA", "UC", "LE", "BPAC"):
        put(f"primary|{r.protocol}|{r.model}|{m}", r[m], "results/sensitivity/primary_metrics_bootstrap_ci.csv",
            "threshold 189.09; bootstrap mean")
    put(f"primary|{r.protocol}|{r.model}|BPAC_CI", f"[{r.BPAC_lo:.3f}, {r.BPAC_hi:.3f}]",
        "results/sensitivity/primary_metrics_bootstrap_ci.csv", "threshold 189.09")
    put(f"primary|{r.protocol}|{r.model}|BPAC_point", r.BPAC_point,
        "results/sensitivity/primary_metrics_bootstrap_ci.csv", "point estimate")

# ── CV-QR (seed 42) ──────────────────────────────────────────────────────────
cv = pd.read_csv(R("results", "cv_qr", "cv_qr_results.csv"))
for _, r in cv.iterrows():
    for m in ("TA", "PA", "UC", "LE", "BPAC"):
        put(f"cvqr|{r.protocol}|{r.line}|{m}", r[m], "results/cv_qr/cv_qr_results.csv", r.model)
    put(f"cvqr|{r.protocol}|{r.line}|q", r.q, "results/cv_qr/cv_qr_results.csv", r.model)
    put(f"cvqr|{r.protocol}|{r.line}|BPAC_CI", f"[{r.BPAC_lo:.3f}, {r.BPAC_hi:.3f}]", "results/cv_qr/cv_qr_results.csv")
    put(f"cvqr|{r.protocol}|{r.line}|TA_CI", f"[{r.TA_lo:.4f}, {r.TA_hi:.4f}]", "results/cv_qr/cv_qr_results.csv")
pr = pd.read_csv(R("results", "cv_qr", "cv_pruning_check.csv"))
put("cv_pruning_min_gap_SE", pr.gap_in_SE.min(), "results/cv_qr/cv_pruning_check.csv")
pc = pd.read_csv(R("results", "cv_qr", "paired_comparisons.csv"))
for _, r in pc.iterrows():
    put(f"paired|{r.protocol}|{r.contrast}|{r.metric}", f"{r['diff']:+.3f} [{r.lo:+.3f}, {r.hi:+.3f}]",
        "results/cv_qr/paired_comparisons.csv")

# ── repeated splits (30 per protocol) ────────────────────────────────────────
raw = pd.read_csv(R("results", "sensitivity", "repeated_splits_raw.csv"))
base = raw[raw.threshold.str.startswith("189.09")]
w = base.pivot_table(index=["protocol", "seed"], columns="model", values=["PA", "UC", "LE", "BPAC"])
for proto in ("paper", "disjoint"):
    s = w.loc[proto]
    put(f"rep|{proto}|n_splits", len(s), "results/sensitivity/repeated_splits_raw.csv")
    for mdl in ("SE OOB-selected", "QRF(q=0.40) fixed", "QRF(q=0.45) fixed", "IRIS_Q42", "RandomForest",
                "QRF test-selected"):
        put(f"rep|{proto}|{mdl}|BPAC_mean", s[("BPAC", mdl)].mean(), "results/sensitivity/repeated_splits_raw.csv")
        put(f"rep|{proto}|{mdl}|BPAC_sd", s[("BPAC", mdl)].std(ddof=1), "results/sensitivity/repeated_splits_raw.csv")
    for a, b in (("SE OOB-selected", "IRIS_Q42"), ("QRF(q=0.40) fixed", "QRF(q=0.45) fixed"),
                 ("QRF test-selected", "SE OOB-selected")):
        d = s[("BPAC", a)] - s[("BPAC", b)]
        put(f"rep|{proto}|{a} - {b}|dBPAC_mean", d.mean(), "results/sensitivity/repeated_splits_raw.csv")
        put(f"rep|{proto}|{a} - {b}|n_positive", int((d > 0).sum()), "results/sensitivity/repeated_splits_raw.csv")
    for m in ("PA", "LE"):
        d = s[(m, "QRF(q=0.40) fixed")] - s[(m, "QRF(q=0.45) fixed")]
        put(f"rep|{proto}|QRF40-QRF45|d{m}_mean", d.mean(), "results/sensitivity/repeated_splits_raw.csv")
ch = pd.read_csv(R("results", "sensitivity", "repeated_splits_quantile_choice.csv"))
for _, r in ch[ch.threshold.str.startswith("189.09")].iterrows():
    put(f"rep|{r.protocol}|SE_choices", r.se_choice_values, "results/sensitivity/repeated_splits_quantile_choice.csv")
# threshold effects (mean change vs 189.09 over 30 splits)
t = raw.pivot_table(index=["protocol", "seed", "model"], columns="threshold", values="BPAC")
t.columns = [c.split(" ")[0] for c in t.columns]
for c in ("188.77", "189.05", "194.10", "train-sample"):
    d = (t[c] - t["189.09"]).groupby(level=[0, 2])
    for (proto, mdl), v in d:
        put(f"thr|{proto}|{mdl}|{c}|mean", v.mean(), "results/sensitivity/repeated_splits_raw.csv")
    put(f"thr|all|{c}|max_abs", float((t[c] - t["189.09"]).abs().max()), "results/sensitivity/repeated_splits_raw.csv")
trl = raw[raw.threshold == "train-sample P24.2"].line
put("train_line_min", trl.min(), "results/sensitivity/repeated_splits_raw.csv")
put("train_line_max", trl.max(), "results/sensitivity/repeated_splits_raw.csv")

# ── metric-definition & legacy-config audits ────────────────────────────────
ci = pd.read_csv(R("results", "audit", "correction_impact.csv"))
for _, r in ci.iterrows():
    put(f"corr|{r.protocol}|{r.step}|{r.model}|BPAC", r.BPAC, "results/audit/correction_impact.csv")
    put(f"corr|{r.protocol}|{r.step}|{r.model}|PA", r.PA, "results/audit/correction_impact.csv")
ca = pd.read_csv(R("results", "audit", "config_audit.csv"))
for _, r in ca.iterrows():
    put(f"legacy|{r.config}|{r.protocol}|{r.model}|BPAC", r.BPAC, "results/audit/config_audit.csv")

# ── A8 audit ─────────────────────────────────────────────────────────────────
a8 = pd.read_csv(R("results", "a8_audit", "a8_summary.csv"))
for _, r in a8.iterrows():
    put(f"a8|{r.config}|{r.model}|BPAC_mean", r.BPAC_mean, "results/a8_audit/a8_summary.csv")
    put(f"a8|{r.config}|{r.model}|dBPAC_vs_B0", r.dBPAC_vs_B0, "results/a8_audit/a8_summary.csv")
    put(f"a8|{r.config}|{r.model}|gap_in_SDs", r.gap_in_SDs, "results/a8_audit/a8_summary.csv")
fp = pd.read_csv(R("results", "a8_audit", "a8_data_diagnostics_fingerprint.csv"))
for _, r in fp[fp.base_percentile == 24.03].iterrows():
    put(f"fingerprint|{r['aggregate']}", f"{r.half_rate:.2f} / {r.double_rate:.2f}",
        "results/a8_audit/a8_data_diagnostics_fingerprint.csv", "base P24.03")
r5 = pd.read_csv(R("results", "a8_audit", "a8_data_diagnostics_row5.csv"))
fz = r5[(r5.target == "G_TOTAL_pc") & (r5.threshold == "P24.03") & (r5.design == "8 dummies (frozen)") & (r5["transform"] == "level")].iloc[0]
put("row5_ours_frozen", f"TA {fz.TA} PA {fz.PA} UC {fz.UC} LE {fz.LE} BPAC {fz.BPAC}", "results/a8_audit/a8_data_diagnostics_row5.csv")
bst = r5.sort_values("L1_distance_to_row5").iloc[0]
put("row5_best_variant", f"{bst.target}/{bst.threshold}/{bst.design}/{bst["transform"]}: TA {bst.TA} PA {bst.PA} UC {bst.UC} LE {bst.LE} BPAC {bst.BPAC}",
    "results/a8_audit/a8_data_diagnostics_row5.csv")
put("row5_n_variants", len(r5), "results/a8_audit/a8_data_diagnostics_row5.csv")

# ── Table A2 ─────────────────────────────────────────────────────────────────
a2 = pd.read_csv(R("results", "table_a2", "table_a2_results.csv"))
for _, r in a2.iterrows():
    put(f"a2|{r.protocol}|{r.line}|{r.model}|BPAC", f"{r.BPAC:.3f} [{r.BPAC_lo:.3f}, {r.BPAC_hi:.3f}]", "results/table_a2/table_a2_results.csv")
    put(f"a2|{r.protocol}|{r.line}|rate_full", r.poverty_rate_full, "results/table_a2/table_a2_results.csv")

# ── Step 5 ───────────────────────────────────────────────────────────────────
S5T = "audit_2026-11-04_step5_threshold_scan/outputs/"
fr = pd.read_csv(R(S5T, "threshold_scan_family_ranking.csv"))
for proto, g in fr.groupby("protocol"):
    put(f"scan|{proto}|n_thresholds", len(g), S5T + "threshold_scan_family_ranking.csv")
    put(f"scan|{proto}|n_QRF_family_first", int(g.family_order.str.startswith("QRF > IRIS").sum()), S5T + "threshold_scan_family_ranking.csv")
    put(f"scan|{proto}|n_SE_below_IRIS", int((g.SE_minus_IRIS < 0).sum()), S5T + "threshold_scan_family_ranking.csv")
    put(f"scan|{proto}|SE_minus_IRIS_range", f"{g.SE_minus_IRIS.min():+.3f} to {g.SE_minus_IRIS.max():+.3f}", S5T + "threshold_scan_family_ranking.csv")
    put(f"scan|{proto}|worst_QRF_minus_IRIS_min", g.worst_QRF_minus_IRIS.min(), S5T + "threshold_scan_family_ranking.csv")
    put(f"scan|{proto}|n_RF_DT_order_RF_first", int(g.family_order.str.endswith("RF > DT").sum()), S5T + "threshold_scan_family_ranking.csv")
sm = pd.read_csv(R(S5T, "threshold_scan_metrics.csv"))
pp = sm[sm.model == "paired: SE - IRIS_Q42"]
for proto, g in pp.groupby("protocol"):
    put(f"scan|{proto}|n_paired_CI_excl0", int((g.BPAC_lo > 0).sum()), S5T + "threshold_scan_metrics.csv")
q40 = sm[sm.model == "QRF(q=0.40) fixed"].set_index(["protocol", "threshold"]).BPAC
iris = sm[sm.model == "IRIS_Q42"].set_index(["protocol", "threshold"]).BPAC
put("scan|paper|QRF040_minus_IRIS_min", float((q40 - iris).loc["paper"].min()), S5T + "threshold_scan_metrics.csv")
S5Q = "audit_2026-11-04_step5_quantile_path/outputs/"
qp = pd.read_csv(R(S5Q, "quantile_path_metrics.csv"))
for fam, g in qp.groupby("family"):
    g = g.set_index("q")
    for q in (0.34, 0.36, 0.40, 0.41, 0.42):
        put(f"qpath|{fam}|q{q:.2f}|BPAC", g.loc[q, "BPAC"], S5Q + "quantile_path_metrics.csv")
ss = pd.read_csv(R(S5Q, "quantile_path_selection_summary.csv"))
for _, r in ss.iterrows():
    put(f"qpath|{r.family}|selected_q", r.q_selected_on_training, S5Q + "quantile_path_selection_summary.csv")
    put(f"qpath|{r.family}|test_BPAC_at_selected", r.test_BPAC_at_selected_q, S5Q + "quantile_path_selection_summary.csv")
    put(f"qpath|{r.family}|hindsight_q", r.q_best_on_test_hindsight, S5Q + "quantile_path_selection_summary.csv")
    put(f"qpath|{r.family}|hindsight_BPAC", r.test_BPAC_max, S5Q + "quantile_path_selection_summary.csv")
put("qpath|max_abs_PA_plus_UC_minus_1", float((qp.PA + qp.UC - 1).abs().max()), S5Q + "quantile_path_metrics.csv")
pz = np.where(qp.LE >= qp.UC, 1 - qp.LE, 2 * qp.PA + qp.LE - 1)
put("qpath|max_abs_BPAC_piecewise_residual", float(np.abs(qp.BPAC - pz).max()), S5Q + "quantile_path_metrics.csv")

# ── pilot ────────────────────────────────────────────────────────────────────
PL = "audit_2026-11-04_repeated_split/outputs/pilot_per_split_results.csv"
pl = pd.read_csv(R(PL)); pl = pl[pl.line == "P24.2_frozen"]
for _, r in pl.iterrows():
    put(f"pilot|{r.seed}", f"CV-QR q={r.cvqr_q:.2f} BPAC {r.BPAC_cvqr:.3f}; QRF {r.qrf_selected} BPAC {r.BPAC_qrf:.3f}; "
        f"d={r.dBPAC_cvqr_minus_qrf:+.3f} [{r.dBPAC_boot_lo:+.3f}, {r.dBPAC_boot_hi:+.3f}]", PL)
put("pilot|convergence_warnings_total", int(pl.convergence_warnings.sum()), PL)
put("pilot|fit_failures_total", int(pl.fit_failures.sum()), PL)
rc = json.load(open(R("audit_2026-11-04_repeated_split", "outputs", "repro_check_seed42_stage1.json")))
put("pilot|repro_check_identical", rc["identical"], "audit_2026-11-04_repeated_split/outputs/repro_check_seed42_stage1.json")

# ── codebook audit ───────────────────────────────────────────────────────────
txt = open(R("results", "audit", "data_construction_audit.txt")).read()
put("codebook_all_checks_passed", "ALL CHECKS PASSED" in txt, "results/audit/data_construction_audit.txt")
put("codebook_n_checks_ok", txt.count("[OK ]"), "results/audit/data_construction_audit.txt")


# ── Step 4 discussion additions (read-only, 2026-11-04) ──────────────────────
RS = "results/sensitivity/repeated_splits_raw.csv"
rr = pd.read_csv(R(RS)); bb = rr[rr.threshold.str.startswith("189.09")]
pv = bb.pivot_table(index=["protocol", "seed"], columns="model", values="BPAC")
dd = pv["QRF test-selected"] - pv["SE OOB-selected"]
for proto in ("paper", "disjoint"):
    g = dd.loc[proto]
    put(f"disc|{proto}|testsel_minus_SE_n_pos", int((g > 1e-12).sum()), RS, "189.09; BPAC point")
    put(f"disc|{proto}|testsel_minus_SE_n_tie", int((g.abs() <= 1e-12).sum()), RS, "ties = both rules chose the same q")
    put(f"disc|{proto}|testsel_minus_SE_n_neg", int((g < -1e-12).sum()), RS)
    put(f"disc|{proto}|QRF041_BPAC_mean", float(pv.loc[proto, "QRF(q=0.41) fixed"].mean()), RS, "30-split mean")
sc = pd.read_csv(R(S5T + "threshold_scan_metrics.csv"))
rate = sc.groupby("threshold").rate_full.first()
put("disc|scan|rate_full_170", float(rate.loc[170.0]), S5T + "threshold_scan_metrics.csv")
put("disc|scan|rate_full_210", float(rate.loc[210.0]), S5T + "threshold_scan_metrics.csv")
pp = sc[sc.protocol == "paper"].pivot_table(index="threshold", columns="model", values="BPAC")
for th in (170.0, 174.5):
    for mname in ("SE OOB-selected", "QRF(q=0.40) fixed", "QRF(q=0.41) fixed", "IRIS_Q42"):
        put(f"disc|scan|paper|{th}|{mname}", float(pp.loc[th, mname]), S5T + "threshold_scan_metrics.csv", "BPAC point")
ssel = sc[(sc.protocol == "paper") & (sc.model == "SE OOB-selected")].set_index("threshold").se_selected
neg = (pp["SE OOB-selected"] - pp["IRIS_Q42"]) < 0
put("disc|scan|paper|SE_choice_where_below_IRIS", ", ".join(sorted(set(ssel[neg]))), S5T + "threshold_scan_metrics.csv")
put("disc|scan|paper|SE_choice_counts_elsewhere", str(ssel[~neg].value_counts().to_dict()), S5T + "threshold_scan_metrics.csv")
put("disc|scan|paper|QRF041_minus_IRIS_n_neg", int(((pp["QRF(q=0.41) fixed"] - pp["IRIS_Q42"]) < 0).sum()), S5T + "threshold_scan_metrics.csv")

out = pd.DataFrame(rows)
out.to_csv(os.path.join(ROOT, "final_manuscript", "evidence_numbers.csv"), index=False)
print(f"{len(out)} values extracted")
