# Step 5 sensitivity results: threshold scan and quantile path

**Date:** 2026-11-04. Frozen methodology and data construction; no primary result was changed. Metrics follow the published Table 2 (PA = TP/(TP+FN); every rate uses TP+FN).

**Scope:**
* Single split, seed 42, frozen split functions.
* CIs are 95% test-sample bootstrap intervals (1,000 draws). They do **not** include split-to-split variation.
* No CV-QR re-selection, new models, survey weights or other countries.

**Consistency check:** the scan and the path reproduce the frozen point estimates exactly at the frozen line. On the disjoint split, QRF(0.40) gives BPAC 0.642105, QRF(0.41) 0.642105 and IRIS 0.509474, identical to `results/sensitivity/primary_metrics_bootstrap_ci.csv`.

## A. Continuous threshold scan, 170–210 Bs

**Files:**
* Directory: `audit_2026-11-04_step5_threshold_scan/`
* Scripts: `scripts/threshold_scan.py`, `scripts/plot_threshold_scan.py`
* Outputs: `outputs/threshold_scan_metrics.csv`, `threshold_scan_rankings.csv`, `threshold_scan_family_ranking.csv`, `threshold_scan_ranking_summary.csv`, `bpac_vs_threshold.png`, `RUN_LOG.txt`

**Design:**
* 82 thresholds: 170.0 to 210.0 Bs in steps of 0.5, plus the frozen 189.09.
* Models are fitted once per split; only the line moves.
* The OOB-selected QRF is re-selected at each line on training data. IRIS QR(0.42) and the fixed QRF quantiles are not re-tuned.

**Ranking changes (BPAC point estimates):**

| | Disjoint split | Published (overlapping) split |
|---|---|---|
| Method order: best QRF > IRIS > RF/DT | **all 82 thresholds** | **all 82 thresholds** |
| RF and DT swap places (both weak) | 20 of 82 | 17 of 82 |
| Every QRF variant above IRIS | yes; smallest margin +0.095 | **no**. OOB-selected QRF falls below IRIS at 13 thresholds (170.0–177.5 Bs; worst −0.055). Fixed QRF(0.40) stays above (smallest margin +0.021). |
| OOB-selected QRF − IRIS (point) | +0.116 to +0.203 | −0.055 to +0.116 |
| Paired CI for that difference excludes 0 | 38 of 82 thresholds | 15 of 82 thresholds |
| BPAC range, OOB-selected QRF / IRIS | 0.624–0.698 / 0.475–0.535 | 0.563–0.681 / 0.544–0.623 |
| Quantile chosen by OOB across thresholds | 0.39–0.42 | 0.41–0.45 |

**Plain reading:**
* Moving the line anywhere between 170 and 210 Bs does **not** change which method family ranks first.
* Most "ranking changes" are swaps between QRF variants (0.40, 0.41 and the OOB pick), i.e. settings of the same model, or between the two weak conditional-mean models.
* Under the published overlapping split, the OOB-selected QRF is unstable at low thresholds, where it chooses q = 0.41–0.42 and drops below IRIS. Under the disjoint split this does not happen. This matches the known issue that OOB selection is optimistic when the training sample contains duplicated households (METHODOLOGY_REFERENCE A4). That link is plausible but not tested here.
* **Caveat:** IRIS here uses its *fixed* published quantile (0.42), not a tuned one. CV-QR could not be re-selected per threshold without about 40 minutes of CV per line. So these rankings do **not** compare QRF with a tuned linear model.

## B. Quantile path, q = 0.30–0.50, disjoint split

**Files:**
* Directory: `audit_2026-11-04_step5_quantile_path/`
* Scripts: `scripts/quantile_path.py`, `scripts/plot_quantile_path.py`
* Outputs: `outputs/quantile_path_metrics.csv`, `quantile_path_bpac_by_family.csv`, `quantile_path_selection_summary.csv`, `quantile_path.png`, `RUN_LOG.txt`

**Design:**
* QRF uses one frozen fit, predicted at each q.
* Linear QR uses the frozen IRIS design, refitted at each q.
* The training-only selection curves are the QRF's OOB BPAC and the stored linear-QR CV BPAC (500 × 3; read-only).

| | QRF | Linear QR |
|---|---|---|
| q chosen on training data | 0.40 → test BPAC **0.642** | 0.34 → test BPAC **0.629** |
| Best q on test, in hindsight (not a valid selection) | 0.40–0.41 → 0.642 | 0.36 → **0.663** |
| BPAC at q = 0.42 (IRIS's fixed quantile) | 0.587 | 0.509 |
| q where UC ≈ LE | 0.41 | 0.36 |

**What it shows:**
* **Each method peaks at a different quantile.** Compared at the same fixed q, either family can look clearly better:
  * at q = 0.36, linear QR leads by 0.110;
  * at q = 0.42, QRF leads by 0.078.
* **Each at its own training-selected quantile,** the two are close: QRF 0.642 vs linear QR 0.629, a difference of +0.013. The test-bootstrap CIs overlap heavily.
* Most of the apparent "QRF beats IRIS" gap therefore comes from **which quantile each model is given**, not from the forest itself (one split; see limitations).

**Mathematical notes** (published definitions; verified numerically to 2e-16):
1. **PA and UC are redundant.** PA = TP/(TP+FN) and UC = FN/(TP+FN), so PA + UC = 1 identically. The two middle panels of the figure carry the same information; the script asserts this for every row.
2. **BPAC is piecewise:**
   * BPAC = 1 − LE when LE ≥ UC (the model over-predicts poverty, FP ≥ FN);
   * BPAC = 2·PA + LE − 1 when UC > LE.

   BPAC therefore peaks near UC = LE, i.e. where the number predicted poor equals the number truly poor. Both curves peak exactly there.

## Limitations (both analyses)
* **One split (seed 42) per analysis.** No split-to-split variability is included. The 3-split pilot (`audit_2026-11-04_repeated_split/REPEATED_SPLIT_RESULTS.md`) showed differences between QRF and CV-QR of 0.04–0.07 under the published protocol, larger than in this single disjoint split.
* **Neighbouring thresholds share almost all households.** The counts of "CI excludes 0" across 82 thresholds are descriptive and are **not** independent tests.
* **IRIS is held at its fixed quantile in the threshold scan.** A tuned linear benchmark was not re-selected per threshold.
* **The welfare variable differs from the authors' (A8).** All levels are specific to our construction of the data.
* **No claim is made that QRF outperforms linear quantile regression or the published method.**
