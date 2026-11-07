# Final code and results review (2026-11-06)

Pre-submission review of every script, result file and manuscript number in this package.

## 1. Verification performed

| Check | Result |
|---|---|
| Raw-data checksums (`sha256sum -c SHA256SUMS`) | 4/4 OK |
| Unit tests (`python3 -m unittest discover -s tests`) | 23/23 pass |
| **Full re-run of the frozen pipeline** (`run_all.sh`, clean copy, raw data → results) | All 19 aggregate result files (CSV/TXT/JSON/MD) reproduce **byte-for-byte**: `results/audit/`, `results/Bolivia/`, `results/sensitivity/`. The only difference is ~1e-13 floating-point noise in the household-level `predictions.csv`, which is not distributed and does not change any metric. Run time: 7 min 18 s on 12 cores. |
| **Re-run of the shorter audits** (A8 forest audit and data diagnostics, Table A2, paired contrasts, threshold scan, quantile path) | See §4 |
| CV-QR baseline (`cv_qr_baseline.py`) | **Not re-run** (published protocol: 2,235 s; the stored log's 41,353 s total is inflated by the disjoint stage, probably a suspended machine). Indirect checks pass: the pilot reproduced its seed-42 stage 1 exactly (`audit_2026-11-04_repeated_split/outputs/repro_check_seed42_stage1.json`), and Table A2 and the paired contrasts, which read its output, reproduce. |
| Published reference values typed into the code (Table A1 rows 2–11, Table A2 Bolivia, Table 4 Bolivia) | All checked against the article PDF: **match** |
| Independent recomputation of the manuscript's key claims from the CSVs | Tables 1–2; quantile-selection ranges and modes; optimism (+0.024 / +0.022; 22 and 21 of 30); QRF(0.40) − QRF(0.45); SE − IRIS 30/30; threshold effects; scan counts (13 lines; 38/82 and 15/82); A8 deltas: **all match**, except one error (§2, item 1) |
| `final_manuscript/check_numbers.py` | 484 decimal numbers; 16 unmatched, all explained (configured thresholds, section numbers, software versions, one published bound rounded) |
| Standalone abstract vs manuscript abstract | Identical |

## 2. Problems found and fixed

| # | Where | Problem | Fix | Effect on results |
|---|---|---|---|---|
| 1 | `MANUSCRIPT.md` §5.7 and the §6.4 table; `CLAIM_EVIDENCE_TABLE.md` R9 | "3.0–9.6 split SDs". `a8_summary.csv` gives a minimum of 3.03 and a maximum of 9.98 (E9, QRF(0.40)). The automatic checker missed it because 9.6 matches another value in the evidence file. | Changed to **3.0–10.0**, as in `A8_AUDIT.md` ("3–10") | Text only |
| 2 | `train_models.py` docstring and printed "Methodology notes" (known issue K2) | Stated PA and BPAC with the old TP+FP formula, cited the 2015 working paper, page "p. 13", and said "DOWNLOADED AUTOMATICALLY". The code itself always used `common.targeting_metrics` (TP+FN). | Rewritten to the published TP+FN definitions, 2018 citation and p. 539 | None. Output files regenerated; numbers byte-identical. |
| 3 | `replication_report.py` header and printed text | Cited the 2015 working paper. Listed the A8 causes as "hypotheses, not tested", although the A8 audit later tested them. | Cites 2018; the note now points to the A8 audit outcome | None (text in `replication_report.txt`) |
| 4 | `README.md` title (K4) | "McBride & Nichols (2015)" | → 2018 | — |
| 5 | `MANUSCRIPT.md` §3.1 | "(Table 3)" was ambiguous with the manuscript's own Table 3 | → "(published Table 3, p. 538)" | — |
| 6 | `MANUSCRIPT.md` front matter | Internal draft material: "Draft for supervisor review", the traceability note and the title options | Removed. Title options moved to `final_manuscript/SUBMISSION_CHECKLIST.md`. | — |
| 7 | `results/Bolivia/train_models_log.txt` (K1) | Stale pre-freeze log printing TP+FP | Not included in the package; the current log is `results/run_all_log.txt` | — |
| 8 | `README.md`, `MANUSCRIPT.md` §4.6 | Pipeline run time "15–25 min" | Measured 7 min 18 s → "about 7 min" / "under 10 minutes" | — |
| 9 | `audit_2026-11-04_step5_threshold_scan/outputs/threshold_scan_family_ranking.csv` | **No script produced this file**, although the §5.4 family-ranking claims and `extract_numbers.py` rely on it (made ad hoc on 2026-11-04) | Added `scripts/family_ranking.py`. It regenerates the stored file **byte-for-byte**. | None |
| 10 | Figures | PNG only, 200 dpi, with an embedded title and footer | The plot scripts also write journal versions (`final_manuscript/figures/Figure*.pdf/png`: vector + 300 dpi, no title; that text is in the captions). The audit PNGs are unchanged (same SHA-256). | None |

**Added:**
* `describe_dataset.py` → `results/dataset/`: aggregate descriptive statistics for the dataset description.
* `final_manuscript/tables/make_tables.py` → every manuscript table as CSV plus `TABLES.md`, generated from the result files.

The previous manuscript is kept in the working repository as `final_manuscript/versions/MANUSCRIPT_v3_2026-11-04_before_final_review.md`.

## 3. Code review findings (no correctness bugs found)

**Correct, as documented:**
* **Metrics** (`common.metrics_from_counts`, `bootstrap_metrics`): follow published Table 2 (TP+FN). The vectorised and scalar versions agree (unit test). Division by zero is handled (BPAC = 0 when there are no true poor).
* **No test-set leakage in model selection:** the SE choice uses OOB predictions on the training sample (`select_se`); CV-QR folds are inside the training sample (`cv_qr_baseline.fold_job`); a unit test checks that selection ignores the test set. Test-set selection exists only to measure optimism and is labelled so.
* **Paired comparisons:** one bootstrap index matrix (seed 42) is shared by every model and threshold.
* **Determinism:** every model receives an explicit seed; the full re-run is byte-identical.
* **Data construction:** 34 codebook assertions pass.

**Known, disclosed limitations (not bugs; all stated in the manuscript):**
* The 189.09 Bs line is computed on the full sample, so test households help define it. A training-only line is reported as a sensitivity.
* Under the published protocol the training sample contains duplicate households, so OOB and CV folds can contain copies of the same household (A4; as in R). The A8 audit shows the effect is −0.003 BPAC.
* `min_samples_leaf = 5` is not R's `nodesize` rule (A10). The R rule raises BPAC by about 0.04.

**Weaknesses of the tooling (not results):**
* `check_numbers.py` accepts a number if it matches *any* value in `evidence_numbers.csv` at the printed precision. It finds unsupported numbers but cannot tell that a number is attached to the wrong claim (see fix 1). The claim-level mapping is in `CLAIM_EVIDENCE_TABLE.md`.
* `train_models.py` still contains placeholder loaders for East Timor and Malawi that raise `NotImplementedError`. They are harmless, out of scope and documented.

## 4. Audit re-run results

Re-run in a clean copy on 2026-11-06 (17 min), then compared with the stored files:

| Audit | Files compared | Result |
|---|---|---|
| A8 forest audit, 20 splits (`a8_qrf_audit.py`) | `a8_raw.csv`, `a8_summary.csv`, `a8_primary_seed42.csv`, `a8_configs.txt`, `a8_log.txt` | **Byte-identical** |
| A8 data diagnostics (`a8_data_diagnostics.py`) | 3 CSVs | **Byte-identical** |
| Table A2 (`table_a2_robustness.py`) | 3 CSVs | **Byte-identical** |
| Paired contrasts (`paired_comparisons.py`) | `paired_comparisons.csv` | **Byte-identical** |
| Threshold scan + new `family_ranking.py` + plot | 4 CSVs, `bpac_vs_threshold.png` (data of Figure 1) | **Byte-identical** |
| Quantile path + plot | 3 CSVs, `quantile_path.png` (data of Figure 2) | **Byte-identical** |
| CV-QR baseline; 3-split pilot | — | Not re-run (about 40 min per protocol; about 26 min per pilot split). Verified indirectly (see §1). |

**Package self-test:** a copy of this package with the raw data placed in `data/bolivia/` passes the checksums and the 23 tests, and regenerates `data_construction_audit.txt`, `correction_impact.csv` and `descriptive_statistics.csv` identically. `make_tables.py`, `extract_numbers.py` and `check_numbers.py` run inside the package and give identical outputs.

## 5. Submission edits (2026-11-06, second pass)

| Change | Verification |
|---|---|
| Cited the 2015 working paper (McBride & Nichols, 2015) at §3.4, §5.5 and §6.6 | Metadata verified via the IHSN citation catalogue (entry 60412) |
| Added Klasen & Lange (2015), CRC-PEG DP 164 (Bolivia PMT accuracy), to §2 | Metadata via RePEc IDEAS; described from its abstract only |
| Added the EH 2005 data citation (INE, 2005) | — |
| Inline APA reference list (47 entries) | Script check: every citation has an entry and every entry is cited |
| Abstract shortened 387 → 237 words; "most" → "much of" | Numbers unchanged; `check_numbers.py` passes (16 explained unmatched) |
| Internal file names → Online Appendix A–C; title page, keywords, JEL codes, declarations placeholders; institutional-setting limitation | — |
| `build_docs.py` builds `submission/Manuscript` and `Online_Appendix` (DOCX + PDF) | Rendered pages inspected |
| `LICENSE` (MIT; excludes data and GPL R excerpts) | — |
| `check_numbers.py` now ignores the reference list (DOIs look like decimal numbers) | — |

## 6. Journal formatting (2026-11-07)

The manuscript and the Online Appendix are typeset to match the reference article (McBride and Nichols 2018, *WBER*). The specification was measured from its PDF with PyMuPDF; `build_docs.py` documents it in its header.

| Element | Reference article (measured) | Ours |
|---|---|---|
| Page / text block | 504 × 720 pt; 424.8 pt wide; margins 39.9 / 39.3 pt | identical |
| Body | Sabon 9.46 pt, leading 12.45 pt, justified, indent 12 pt | Garamond 9.5 pt, leading 12.45 pt (measured in our PDF), justified, indent 12 pt |
| Title / authors | Sabon Bold 17.93 / Univers Bold 11.96 | Garamond Bold 18 / Arial Bold 12 |
| Abstract | heading Univers Bold 9.96; text Sabon 8.97, leading 11.95; JEL line bold label | identical sizes |
| Sections | Univers Bold 9.96, Roman numerals; introduction unnumbered | identical (subsections, absent from the article, in italic) |
| Author note | first-page footnote, Sabon 7.97 | first-page footnote, 8 pt |
| Running heads | Univers Condensed 7.97, rule below; even: page / authors; odd: title / page | identical layout, Arial Narrow 8 |
| Tables | caption above (Univers Bold + regular 7.47); body 7.47; header bold 6.97; horizontal rules only; notes 5.98 | identical sizes; column widths fitted to content; numeric columns right-aligned |
| Figures | caption above (Univers 6.97); full text width; notes 5.98 below | identical; figures redrawn at print width (labels 7–8 pt) |
| References | Sabon 8.47, leading 11.45, hanging indent 9.9 pt; Chicago author-date | identical; all 47 entries rewritten in this style (one-to-one check against the APA list) |
| Citations | (Author and Author 2004; Author et al. 2010), "table 1", "figure 1" in text | converted (51 parenthetical citations) |

Sabon and Univers are commercial fonts. The DOCX names Garamond, Arial and Arial Narrow, which are standard in Microsoft Office. The PDF built here uses the metric-equivalent free fonts EB Garamond and Liberation Sans (Narrow). Font sizes are on Word's half-point grid; the article's sizes are these nominal sizes × 0.996.

Content changes that the format required:
* Figures were renumbered to order of first citation (the threshold scan is now Figure 1).
* Sections were renumbered after the unnumbered introduction (Related Work = I … Conclusion = VII); every cross-reference was updated.
* The structured abstract became one paragraph.
* Table captions were split into a Title Case title above the table and notes below it.

After these changes: `check_numbers.py` reports 433 numbers with 10 explained unmatched (the drop comes from section numbers that are no longer decimals); 23/23 tests pass.
