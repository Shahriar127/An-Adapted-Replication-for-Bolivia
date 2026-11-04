# Claim–evidence table

**Paths** are relative to `Model_Training/`. **Values** are reproduced read-only in `final_manuscript/evidence_numbers.csv` by `final_manuscript/extract_numbers.py`. The **Key** column gives the row key in that CSV (prefix match).

**Evidence types:**
* **C:** confirmed; the result is directly computed.
* **D:** descriptive; dispersion or counts only, no inferential claim.
* **H:** hypothesis; plausible but not tested.
* **P:** from the published article, with page cited.

## Replication findings

| ID | Claim (manuscript §) | Type | Evidence | Source file(s) / key |
|---|---|---|---|---|
| R1 | N = 4,086 households, matching the published Table 3 (§3.1) | C + P | 34 codebook checks pass; published Table 3, p. 538 | `results/audit/data_construction_audit.txt` (`codebook_*`); reference PDF |
| R2 | Published metrics use TP+FN denominators; PA + UC = 1 (§3.4) | C + P | Table 2, p. 534; unit tests on published Table A1 rows; max \|PA+UC−1\| = 0 | `tests/test_methodology.py`; `qpath\|max_abs_PA_plus_UC_minus_1` |
| R3 | BPAC = 1 − LE when LE ≥ UC, else 2PA + LE − 1 (§3.4) | C | max residual 2.2e-16 | `qpath\|max_abs_BPAC_piecewise_residual` |
| R4 | The article is internally inconsistent on the poverty rate: text 24.2%, Table 3 24.03%, row 5 implies 24.038% (§3.2) | C + P | implied rate 24.038 | `results/a8_audit/a8_data_diagnostics_implied_rate.csv` |
| R5 | CV-QR replicates: q = 0.37 vs 0.38; PA, UC, LE and BPAC inside the published CIs; TA just above (§5.1) | C | 0.837 / 0.665 / 0.335 / 0.369 / 0.623 [0.557, 0.673] | `results/cv_qr/cv_qr_results.csv` (`cvqr\|paper\|base\|*`) |
| R6 | IRIS: BPAC and LE inside the published CIs; TA, PA and UC just outside (§5.1) | C | 0.840 / 0.633 / 0.367 / 0.324 / 0.586 [0.486, 0.657] | `results/sensitivity/primary_metrics_bootstrap_ci.csv` (`primary\|paper\|IRIS_Q42\|*`) |
| R7 | SE QRF does not replicate; all metrics outside the published CIs, in the higher-accuracy direction (§5.1) | C | QRF(0.43) BPAC 0.653 [0.558, 0.713] vs published 0.502 [0.393, 0.586] | `primary\|paper\|SE OOB-selected (QRF(0.43))\|*` |
| R8 | Implementation is not the cause of A8; R emulation and the node rule raise BPAC (§5.7) | C | ΔBPAC (SE) vs B0: +0.004, −0.004, +0.038, +0.040, −0.003, +0.002, −0.002, −0.002 | `results/a8_audit/a8_summary.csv` (`a8\|*\|SE\|dBPAC_vs_B0`) |
| R9 | Split variation is not the cause; published value 3.0–9.6 split-SDs below ours (§5.7) | C | `gap_in_SDs` across configurations | `a8\|*\|gap_in_SDs` |
| R10 | The welfare distribution differs: 6.07 / 57.00 vs 4.92 / 62.26; none of 9 aggregates matches (§5.7) | C + P | fingerprint rows | `results/a8_audit/a8_data_diagnostics_fingerprint.csv` (`fingerprint\|*`); Table A2 p. 547 |
| R11 | In-sample linear refit differs in LE and TA; best of 21 variants LE 26.99 (§5.7) | C + P | ours TA 84.65, PA 61.10, UC 38.90, LE 24.95; published row 5 | `results/a8_audit/a8_data_diagnostics_row5.csv` (`row5_*`) |
| R12 | The data difference causes A8 | **H** | not testable without the authors' data | — |
| R13 | Doubled-line BPACs close to published; halved line approximate (§5.4) | C + P | 0.811 / 0.809 / 0.837 vs 0.811 / 0.819 / 0.806; halved CV 0.334 [0.143, 0.461] | `results/table_a2/table_a2_results.csv` (`a2\|paper\|*`) |

## Methodological findings

| ID | Claim (manuscript §) | Type | Evidence | Source file(s) / key |
|---|---|---|---|---|
| M1 | Overlapping validation inflates forests by about 0.035–0.066 BPAC; IRIS −0.002 (§5.2) | C (D for SDs) | 30-split means, Table 2 | `results/sensitivity/repeated_splits_raw.csv` (`rep\|*\|BPAC_mean`) |
| M2 | Legacy configuration: 0.784 (overlapping) vs 0.586 (disjoint) (§5.2) | C, indicative (different splits) | config audit under published metrics | `results/audit/config_audit.csv` (`legacy\|replication_report.py (old)\|*`) |
| M3 | OOB-selected q ranges 0.36–0.43 (published) and 0.37–0.42 (disjoint) (§5.3) | D | choice counts | `results/sensitivity/repeated_splits_quantile_choice.csv` (`rep\|*\|SE_choices`) |
| M4 | Test-set selection optimism +0.024 (22/30) and +0.022 (21/30) (§5.3) | C | paired across splits | `rep\|*\|QRF test-selected - SE OOB-selected\|*` |
| M5 | QRF(0.40) − QRF(0.45): BPAC +0.139 / +0.148 (29/30 each) (§5.3) | C | paired across splits | `rep\|*\|QRF(q=0.40) fixed - QRF(q=0.45) fixed\|*` |
| M6 | Reconstructed lines: mean \|Δ\| ≤ 0.010 (188.77), ≤ 0.001 (189.05); 194.10 up to +0.041 (RF) (§5.4) | C | 30-split means | `thr\|*\|mean` |
| M7 | Family ranking unchanged across 82 lines, 170–210 Bs, both protocols (§5.4) | C (seed 42) | 82 of 82 | `audit_2026-11-04_step5_threshold_scan/outputs/threshold_scan_family_ranking.csv` (`scan\|*`) |
| M8 | Published protocol: OOB-QRF below IRIS at 13 lines (170–177.5 Bs); QRF(0.40) never below (§5.4) | C (seed 42) | min −0.055; QRF(0.40) min +0.021 | `scan\|paper\|*` |
| M9 | The 2015 formula shifts IRIS BPAC by 0.025–0.064; the QRF–IRIS gap widens by 0.034–0.067 (§5.5) | C | correction impact | `results/audit/correction_impact.csv` (`corr\|*`) |
| M10 | Under TP+FP, PA favoured QRF(0.45) over QRF(0.40); reversed under published definitions (§5.5) | C | step 0: QRF(0.45) PA 0.731 vs QRF(0.40) 0.695; published: QRF(0.40) PA 0.712 vs QRF(0.45) 0.667 | `corr\|paper\|0 pre-freeze\|*\|PA`; `primary\|paper\|QRF(q=0.4*)\|PA` |
| M11 | Seed-42 CV-QR − SE contrasts include zero (§5.6) | C (single split) | −0.030 [−0.109, +0.065]; −0.004 [−0.053, +0.056] | `results/cv_qr/paired_comparisons.csv` (`paired\|*\|CV - SE\|BPAC`) |
| M12 | Pilot: QRF higher in 3/3, each CI reaching or crossing 0 (§5.6) | D (n = 3) | −0.039, −0.068, −0.038 | `audit_2026-11-04_repeated_split/outputs/pilot_per_split_results.csv` (`pilot\|*`) |
| M13 | Quantile path: each method peaks at a different q; at the training-selected q the difference is +0.013 (§5.6) | C (single split) | QRF 0.642 at 0.40; linear 0.629 at 0.34; at 0.42: 0.587 vs 0.509 | `audit_2026-11-04_step5_quantile_path/outputs/quantile_path_*.csv` (`qpath\|*`) |
| M14 | Most of the QRF advantage over IRIS is a quantile-calibration effect (§5.6, §6) | C on our data (single split), **with RQ5 open** | M11, M13, SE − IRIS +0.162 / +0.196 | as above |
| M15 | The forest adds accuracy beyond quantile tuning | **Not established** | M11 vs M12 conflict | — |
| M16 | The overlap mechanism is memorisation of duplicated households (§6.1) | **H** | consistent with M1, not directly observed | — |
| M17 | Under the published protocol, P(a household is in the training draw) ≈ 1 − e^(−1/2) ≈ 39% (§6.1) | C (algebra) | (1 − 1/N)^(N/2) = 0.6065 for N = 4,086; matches the observed ≈ 40% | `README.md` §2; derivation in text |
| M18 | Test-set selection is never worse than OOB selection; better in 22/30 and 21/30 splits, tied in 8/30 and 9/30 when both chose the same q (§6.2) | C | counts per protocol | `disc\|*\|testsel_minus_SE_n_*` |
| M19 | At 170 Bs (published split, seed 42) QRF(0.40) 0.620 vs QRF(0.41) 0.581 (§6.2) | C (single split) | scan BPAC points | `disc\|scan\|paper\|170.0\|*` |
| M20 | Scan lines 170–210 Bs correspond to full-sample poverty rates of 20.3%–28.4% (§6.3) | C | rate at 170 and 210 Bs | `disc\|scan\|rate_full_*` |
| M21 | Where the OOB-selected QRF falls below IRIS, the OOB rule chose q = 0.41–0.42; elsewhere 0.43–0.45 at 56 of 69 lines; fixed QRF(0.41) is below IRIS at 6 lines; QRF(0.40) never (§6.3) | C (single split) | scan selections | `disc\|scan\|paper\|SE_choice_*`, `disc\|scan\|paper\|QRF041_minus_IRIS_n_neg`, `disc\|scan\|paper\|174.5\|*` |
| M22 | The reversal at 170–177.5 Bs is caused by the selected quantile, not by the forest (§6.3) | C on this split (fixed-quantile comparison), not generalised | M21 | as M21 |
| R14 | Quantile choice does not explain A8: QRF fixed at the published q = 0.41 gives 0.673 [0.614, 0.722] (seed 42) and 0.658 (30-split mean) vs published 0.502 [0.393, 0.586] (§6.4) | C | primary and repeated-split values | `primary\|paper\|QRF(q=0.41) fixed\|*`; `disc\|paper\|QRF041_BPAC_mean` |

## Published values used for comparison
All are taken from McBride & Nichols (2018) via `reference/McBride_Nichols_2018_WBER.pdf`:
* Table A1, pp. 545–546: rows 2, 4, 5, 6, 8, 9 and 11 for Bolivia;
* Table 4, p. 542: Bolivia contrasts;
* Table A2, p. 547: Bolivia halved and doubled lines;
* Table 3, p. 538: N and poverty rate;
* Table 2, p. 534: formulas.
