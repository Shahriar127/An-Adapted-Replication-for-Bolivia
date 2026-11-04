# Research inventory: what is final, what is supporting, what is superseded

**Created 2026-11-04 (Step 1 of the paper-writing plan).**
This is an **index only**. No file was moved, renamed, edited or deleted, because moving files would break the frozen paths, the SHA-256 snapshots and the run scripts. All paths are relative to `Model_Training/`.

**Status labels**
| Label | Meaning | May be cited in the paper? |
|---|---|---|
| **FINAL** | Current result under the frozen methodology (published 2018 metric definitions) | Yes |
| **FINAL-AUDIT** | Current result from a separate, documented audit (does not change the frozen pipeline) | Yes, labelled as audit/sensitivity |
| **WRITING** | Manuscript and its support files | — |
| **SUMMARY** | Earlier summary document. Superseded by `MANUSCRIPT.md` where they differ | No; cite the underlying result file |
| **SUPERSEDED** | Pre-freeze results (old TP+FP metric) | **No** |
| **UNUSED** | Synthetic-data prototype or empty folders | **No** |
| **RAW / RESTRICTED** | Raw survey data or household-level predictions | Not redistributed |

---

## 1. Manuscript (WRITING) — `final_manuscript/`
| File | Content |
|---|---|
| `MANUSCRIPT.md` | Full draft, §§1–8 (10-part structure, Step 2), Tables 1–3, Figures 1–2 (≈8,250 words after Steps 3–4) |
| `versions/MANUSCRIPT_v1_2026-11-04_before_restructure.md` | Draft before Step 2 (§§1–7) |
| `versions/MANUSCRIPT_v2_2026-11-04_after_step2.md`, `versions/REFERENCES_v1_2026-11-04.md` | Drafts before Steps 3–4 (literature and Discussion) |
| `ABSTRACT.md` | Identical to the manuscript abstract |
| `REFERENCES.md` | 25 verified references (APA 7) |
| `CLAIM_EVIDENCE_TABLE.md` | Each claim → evidence type → source file |
| `REVIEWER_AUDIT.md` | Reviewer-style self-audit |
| `FINAL_CHECKLIST.md` | Open items before submission |
| `RESEARCH_INVENTORY.md` | This file |
| `extract_numbers.py` → `evidence_numbers.csv` | Read-only extraction of 586 values from the result files |
| `check_numbers.py` → `number_check_report.txt` | Checks every decimal number in the manuscript |
| `figures/fig1_quantile_path.png`, `figures/fig2_threshold_scan.png` | Byte-identical copies of the Step 5 plots |

## 2. Final code
**Frozen pipeline (do not modify without change control; see `METHODOLOGY_REFERENCE.md`)**
| File | Role |
|---|---|
| `common.py` | Single source of configuration, data construction, splits, metrics (TP+FN), bootstrap, quantile selection |
| `data_construction_audit.py` | 34 codebook checks of the household data |
| `train_models.py` | Primary DT / RF / QRF run (seed 42, published protocol) |
| `replication_report.py` | Comparison with published Table A1 |
| `sensitivity_analysis.py`, `summarize_sensitivity.py` | Protocols, thresholds, fixed quantiles, 30 repeated splits |
| `config_audit.py`, `correction_impact.py` | Legacy-configuration audit; impact of corrections C1–C3 |
| `tests/test_methodology.py`, `tests/test_audits.py` | 23 unit tests (all pass) |
| `run_all.sh` | Runs the frozen pipeline end to end |

**Audit code (separate outputs)**
| File | Role |
|---|---|
| `a8_qrf_audit.py`, `a8_data_diagnostics.py` | A8 QRF discrepancy audit |
| `cv_qr_baseline.py`, `paired_comparisons.py`, `table_a2_robustness.py` | CV-QR baseline, Table 4 contrasts, Table A2 lines |
| `run_audits.sh` | Runs the scripts above |
| `audit_2026-11-04_repeated_split/scripts/*.py` | CV-QR vs QRF pilot, A9/A10, 24.03% sensitivity |
| `audit_2026-11-04_step5_threshold_scan/scripts/*.py` | Threshold scan 170–210 Bs and plot |
| `audit_2026-11-04_step5_quantile_path/scripts/*.py` | Quantile path q = 0.30–0.50 and plot |

**Environment:** `requirements.txt`, `ENVIRONMENT.txt` (Python 3.14.8, scikit-learn 1.8.0, quantile-forest 1.4.2, numpy 2.3.5, pandas 3.0.1).

## 3. Dataset description
| Item | Value | Source |
|---|---|---|
| Survey | Bolivia Encuesta de Hogares 2005 (EH 2005), INE Bolivia | `DATA_MANIFEST.json` |
| Download | `EH2005.rar` from siip.produccion.gob.bo, 2026-11-03 | `DATA_MANIFEST.json`, `README.md` §3 |
| Files used | `BASE_EH_2005_(Pob_y_Viv).sav`, `Bolivia_Equipamiento.sav`, `Bolivia_Pecuaria.sav` (SHA-256 in `SHA256SUMS`) | `data/bolivia/` (**RAW / RESTRICTED**) |
| Not used | `Bolivia_Agricola.sav`, `Bolivia_Subproductos.sav` | — |
| Unit / N | Household; N = 4,086 (matches published Table 3) | `results/audit/data_construction_audit.txt` |
| Target | `G_TOTAL_pc`, monthly per-capita household expenditure (Bs) | `common.py` |
| Features | 21 IRIS variables (published Table 3); 3 approximations (sublease, kitchens, region coding) | `MANUSCRIPT.md` §3.1 |
| Poverty line | P24.2 of full sample = 189.09 Bs (data-derived; reconstructed) | `METHODOLOGY_REFERENCE.md` |
| Missing data | 0 rows dropped, 0 values imputed | `README.md` §2 |
| Known difference | Welfare distribution differs from the authors' (fingerprint 6.07 / 57.00 vs 4.92 / 62.26) | `results/a8_audit/a8_data_diagnostics_fingerprint.csv` |

## 4. Final results → where they appear in the manuscript
| Manuscript item | Result file(s) | Status |
|---|---|---|
| Table 1 (§4.1), replication vs Table A1 | `results/sensitivity/primary_metrics_bootstrap_ci.csv`, `results/cv_qr/cv_qr_results.csv` | FINAL / FINAL-AUDIT |
| Primary model run (seed 42) | `results/Bolivia/model_comparison.csv`, `confusion_matrices.csv`, `replication_report.txt`, `config.json` | FINAL |
| Table 2 (§4.2), protocols over 30 splits | `results/sensitivity/repeated_splits_raw.csv`, `repeated_splits_summary.csv` | FINAL |
| §4.2 legacy configuration (0.784 vs 0.586) | `results/audit/config_audit.csv` | FINAL |
| §4.3 quantile selection | `results/sensitivity/repeated_splits_raw.csv`, `repeated_splits_quantile_choice.csv`, `primary_quantile_selection.csv` | FINAL |
| §4.4 reconstructed thresholds | `results/sensitivity/repeated_splits_raw.csv` | FINAL |
| §4.4 threshold scan, Figure 2 | `audit_2026-11-04_step5_threshold_scan/outputs/` | FINAL-AUDIT (seed 42) |
| §4.4 Table A2 halved/doubled lines | `results/table_a2/table_a2_results.csv` | FINAL-AUDIT |
| §4.5 metric definition | `results/audit/correction_impact.csv` | FINAL |
| §4.6 CV-QR vs SE | `results/cv_qr/paired_comparisons.csv`, `cv_pruning_check.csv` | FINAL-AUDIT (single split) |
| §4.6 pilot (n = 3) | `audit_2026-11-04_repeated_split/outputs/pilot_per_split_results.csv` | FINAL-AUDIT (descriptive) |
| §4.6 quantile path, Figure 1 | `audit_2026-11-04_step5_quantile_path/outputs/` | FINAL-AUDIT (single split) |
| §4.7 and Table 3, A8 | `results/a8_audit/a8_summary.csv`, `a8_data_diagnostics_*.csv` | FINAL-AUDIT |

**Result reports (readable summaries of the files above):** `RESULTS.md` (frozen), `results/sensitivity/SUMMARY.md`, `results/cv_qr/PHASE2_3_RESULTS.md`, `results/a8_audit/A8_AUDIT.md`, `audit_2026-11-04_repeated_split/REPEATED_SPLIT_RESULTS.md`, `STEP5_SENSITIVITY_RESULTS.md`.

## 5. Figures
| Figure | Status |
|---|---|
| `final_manuscript/figures/fig1_quantile_path.png`, `fig2_threshold_scan.png` | FINAL (used in the manuscript) |
| `results/Bolivia/*.png` (7 plots) | FINAL pipeline diagnostics, not used in the manuscript |
| `results/*.png` (top level, 7 plots) | **UNUSED** (synthetic prototype, 2026-11-03 11:33) |

## 6. Summary and planning documents (SUMMARY)
| File | Note |
|---|---|
| `RESEARCH_PLAN.md` | Project history and status |
| `FINAL_RESEARCH_ASSESSMENT.md` | Evidence consolidation; **see known issue K3** |
| `MANUSCRIPT_OUTLINE.md` | Superseded by `MANUSCRIPT.md`; **see K3** |
| `METHODOLOGY_REFERENCE.md` | Frozen methodology (authoritative, not a summary) |
| `README.md` | Reproduction instructions; **see K4** |

## 7. Superseded and unused (do not cite)
| Path | Why |
|---|---|
| `archive/2026-11-03_pre_methodology_freeze/` | Pre-freeze code and results, TP+FP metric. Integrity: `MANIFEST.sha256` |
| `legacy/train_models.py`, `legacy/replication_report.py` | Scripts before the consistency fix |
| `results/model_comparison.csv`, `all_predictions.csv`, `confusion_matrices.csv`, `results/*.png` | Synthetic prototype |
| `synthetic_poverty_dataset.csv`, `generate_synthetic_poverty_dataset.py` | Synthetic prototype |
| `results/East Timor/`, `results/Malawi/` | Empty folders; out of scope |
| `results/Bolivia/train_models_log.txt` | **Stale: see K1** |

## 8. Known issues found during this inventory (not fixed; frozen files)
| ID | Issue | Effect on results | Proposed handling |
|---|---|---|---|
| **K1** | `results/Bolivia/train_models_log.txt` (dated 2026-11-03 19:11) predates the freeze (21:00) and is byte-identical to the archived copy. It prints TP+FP formulas. | None. The current run output is `results/run_all_log.txt`; `model_comparison.csv` (21:03) matches the manuscript (QRF(0.43) BPAC 0.653). | Treat as SUPERSEDED. Do not cite. |
| **K2** | The **docstring (lines 25–28) and printed "Methodology notes" (lines 543–547) of frozen `train_models.py`** still state PA and BPAC with TP+FP. The same text therefore appears in `results/run_all_log.txt` (lines 246–250). | **None on numbers.** The script computes metrics with `common.targeting_metrics` (TP+FN), which the unit tests verify. The text is a stale comment. | Correcting comment text is a code change under change control. **Your decision:** fix with a logged, comment-only change (no rerun needed), or leave it and disclose. A reviewer reading the code would notice it. |
| **K3** | `FINAL_RESEARCH_ASSESSMENT.md` line 132 says IRIS replicates within the published CIs "except PA". Correct: TA, PA and UC fall just outside; only LE and BPAC are inside. `MANUSCRIPT_OUTLINE.md` line 20 says "inside the published CI" without naming the metric. | None. `MANUSCRIPT.md` §4.1 is correct. | `MANUSCRIPT.md` supersedes both documents. |
| **K4** | `README.md` title cites "McBride & Nichols (2015)"; the body correctly uses the 2018 article. | None. | Correct the title when the README is next revised (README is in the reproducibility package). |
| **K5** | `RESULTS.md` §1 says the A8 causes are "none tested" and line 111 mentions the old "0.797". Both are already documented as superseded in `FINAL_RESEARCH_ASSESSMENT.md`. | None. | No action. |

## 9. Redistribution
* **Not redistributable:** `data/bolivia/*` (INE licence to be confirmed); `results/Bolivia/predictions.csv` and any household-level predictions.
* **Redistributable:** code, aggregate result CSVs, reports, figures, checksums.
