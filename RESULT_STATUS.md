# Result status: what is FINAL and what is OLD

**Rule:** everything **in the current tree of this repository** is final and may be cited. Everything listed under "Old / superseded" was removed from the tree on 2026-11-07. It remains in the git history (commit `8af6117`, `git show 8af6117:<path>`) and must **not** be cited.

| Label | Meaning | Cite? |
|---|---|---|
| **FINAL** | Frozen pipeline under the published metric definitions (`run_all.sh`) | Yes |
| **FINAL-AUDIT** | Separate documented audit that does not change the frozen pipeline (`run_audits.sh`, `audit_*` folders) | Yes, labelled as audit or sensitivity |
| **PAPER** | Manuscript, tables, figures and their tooling | — |
| **OLD** | Superseded result or summary | **No** |
| **NOT RUN** | Code prepared but never executed; no results exist | **No** |
| **RESTRICTED** | Raw or household-level data | Not redistributed |

## 1. In this repository (all FINAL)

| Path | Label | Produced by | Used in manuscript |
|---|---|---|---|
| `RESULTS.md` | FINAL | consolidated 2026-11-06 | all of section IV |
| `DATASET.md`, `results/dataset/` | FINAL | `describe_dataset.py` | section II.1, Table S6 |
| `results/audit/data_construction_audit.txt` | FINAL | `data_construction_audit.py` | section II.1 |
| `results/audit/config_audit.*` | FINAL | `config_audit.py` | section IV.2 (legacy configuration) |
| `results/audit/correction_impact.csv` | FINAL | `correction_impact.py` | section IV.5, Table S2 |
| `results/Bolivia/` | FINAL (primary run; diagnostic plots not in the paper) | `train_models.py`, `replication_report.py` | section IV.1 |
| `results/sensitivity/` | FINAL | `sensitivity_analysis.py`, `summarize_sensitivity.py` | Tables 1–2, sections IV.2–IV.4, Table S1 |
| `results/run_all_log.txt` | FINAL (console log of the 2026-11-06 run) | `run_all.sh` | — |
| `results/a8_audit/` | FINAL-AUDIT | `a8_qrf_audit.py`, `a8_data_diagnostics.py` | section IV.7, Table 3 |
| `results/cv_qr/` | FINAL-AUDIT (single split per protocol) | `cv_qr_baseline.py`, `paired_comparisons.py` | Table 1 (CV-QR), section IV.6, Table S3 |
| `results/table_a2/` | FINAL-AUDIT (seed 42) | `table_a2_robustness.py` | section IV.4, Table S5 |
| `audit_2026-11-04_step5_threshold_scan/` | FINAL-AUDIT (seed 42) | its `scripts/` | section IV.4, Figure 1 |
| `audit_2026-11-04_step5_quantile_path/` | FINAL-AUDIT (seed 42, disjoint) | its `scripts/` | section IV.6, Figure 2 |
| `audit_2026-11-04_repeated_split/` | FINAL-AUDIT (**pilot, n = 3**, descriptive) | `scripts/repeated_split_cvqr_vs_qrf.py` | section IV.6, Table S4 |
| `STEP5_SENSITIVITY_RESULTS.md`, `results/*/*.md` | FINAL-AUDIT reports (readable summaries of the CSVs) | hand-written 2026-11-04 | — |
| `final_manuscript/` | PAPER | — | — |
| `final_manuscript/tables/` | PAPER (generated) | `make_tables.py` | Tables 1–3, S1–S6 |
| `final_manuscript/figures/` | PAPER | journal versions redrawn at print width from the Step 5 result CSVs by `make_journal_figures.py` (Figure 1 = threshold scan, Figure 2 = quantile path); PDF + 600-dpi PNG | Figures 1–2 |
| `final_manuscript/submission/` (not tracked; built locally) | **PAPER — final product** | `build_docs.py` from `MANUSCRIPT.md` and the appendix sources | the submission itself |

**Known caveats on FINAL files:**
* `results/sensitivity/SUMMARY.md` and the audit reports were written on 2026-11-04. Their numbers are final, but where wording differs from `RESULTS.md` or the manuscript, `RESULTS.md` wins.
* `results/Bolivia/replication_report.txt` was regenerated on 2026-11-06. Its numbers are unchanged; only the citation and the A8 note were updated.

## 2. Old / superseded (removed from the tree; in git history at commit `8af6117`; do not cite)

| Item (path at commit `8af6117`) | Why it is old |
|---|---|
| `archive/2026-11-03_pre_methodology_freeze/` (code and results) | Pre-freeze. PA and BPAC used the TP+FP typo from the 2015 working paper. Includes the "QRF(45) BPAC 0.797" artefact. |
| `legacy/train_models.py`, `legacy/replication_report.py` | Scripts before the configuration-consistency fix |
| `RESULTS.md` (frozen, 2026-11-03) | Superseded by this package's `RESULTS.md`. Its §1 says the A8 causes were "none tested" (they were tested later). |
| `FINAL_RESEARCH_ASSESSMENT.md`, `RESEARCH_PLAN.md`, `MANUSCRIPT_OUTLINE.md` | Planning and summary documents from 2026-11-04. Some wording is outdated (e.g. "IRIS replicates within the CI", "SE ≈ CV-QR"). |
| `final_manuscript/RESEARCH_INVENTORY.md`, `FINAL_CHECKLIST.md` | Replaced by this file and by `final_manuscript/SUBMISSION_CHECKLIST.md` |
| `final_manuscript/versions/` | Earlier manuscript drafts (v1, v2) |
| `results/Bolivia/train_models_log.txt` (2026-11-03 19:11) | Pre-freeze console log; prints TP+FP formulas. Replaced by `results/run_all_log.txt`. |
| Synthetic-data prototype (`synthetic_poverty_dataset.csv`, etc.; never in git) | No reported result uses them. |
| `reproducibility_package_2026-11-03.tar.gz` (never in git) | Pre-freeze package (2026-11-03). Replaced by this repository. |

## 3. Not run (no results exist; not cited)

| Script (`audit_2026-11-04_repeated_split/scripts/`, at commit `8af6117`) | Status |
|---|---|
| `a9_a10_sensitivity.py` | Written, never executed (stopped by author decision, 2026-11-04). A9/A10 effects are covered by the A8 audit instead. |
| `poverty_rate_sensitivity.py` | Written, never executed. The 24.03% sensitivity is covered by `results/sensitivity/`. |
| 10-split CV-QR vs QRF study (`repeated_split_cvqr_vs_qrf.py` with 10 seeds) | Only the 3-split pilot was run. |

## 4. Restricted (never distributed)

`data/bolivia/*` (INE microdata); `results/Bolivia/predictions.csv`, `actual_vs_predicted.png`, `qrf_intervals.png` (household-level); `reference/McBride_Nichols_2018_WBER.pdf` (copyrighted).
