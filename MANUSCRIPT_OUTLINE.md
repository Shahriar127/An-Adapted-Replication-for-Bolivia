# Manuscript outline: Bolivia PMT replication

**Status:** outline only. Every number below comes from the corrected (published-metric) outputs listed in `FINAL_RESEARCH_ASSESSMENT.md`.
* **[verify]** marks a claim or citation that must be checked before submission.
* **[decide]** marks an open choice.
* Nothing here asserts statistical significance beyond what the cited outputs report.

## Title options
1. *Retooling, revisited: an adapted replication of machine-learning proxy means testing for Bolivia*
2. *How robust are machine-learning gains in poverty targeting? A replication of McBride and Nichols (2018) with Bolivian household data*
3. *Metric definitions, benchmark tuning and validation design in ML poverty targeting: evidence from a Bolivian replication*

Recommendation: title 2, which is descriptive and signals a replication.

## Abstract structure (150–200 words)
1. **Context:** proxy means tests (PMTs); McBride & Nichols (2018) report out-of-sample gains from cross-validation and quantile regression forests.
2. **What we do:** an adapted replication on the Bolivia EH 2005 data, against a frozen, page-referenced methodology, plus robustness checks on metric definition, validation design, quantile selection and poverty-line reconstruction.
3. **Replicated:**
   * sample size (N = 4,086);
   * the IRIS QR(0.42) benchmark, inside the published CI;
   * the cross-validated linear QR, which selects q = 0.37 against the published 0.38, with PA/UC/LE/BPAC inside the published CIs;
   * results at the doubled poverty line.
4. **Not replicated:** the published QRF result. Ours is higher, and the cause is not identified. Implementation differences are ruled out. The welfare-variable distribution demonstrably differs.
5. **Robustness findings:**
   * the metric definition and the tuning of the benchmark's quantile shift headline gains by amounts comparable to the reported gains;
   * overlapping train/test draws flatter flexible models;
   * small poverty-line reconstructions do not matter.
6. **Implication:** report metric formulas exactly, tune benchmarks on the same footing as ML models, and release constructed data.

## 1. Introduction and research gap
* PMTs and their use in targeting (Coady, Grosh & Hoddinott 2004; Grosh & Baker 1995).
* The USAID Poverty Assessment Tools (PAT) and IRIS's BPAC criterion (IRIS Center 2005).
* The case for ML in PMT (McBride & Nichols 2018).
* **Gap:**
  * ML-for-targeting results are rarely replicated independently [verify: search for existing replications];
  * reported gains depend on choices that papers specify only partly (metric formulas, benchmark tuning, validation design, poverty-line construction).
* **Research question:** do the published Bolivia results replicate, and how sensitive are the ML gains to these choices?
* **Contributions** (state modestly):
  1. a transparent adapted replication with a frozen, page-referenced methodology;
  2. documented inconsistencies within the published article;
  3. evidence that most of the ML gain over the *fixed-quantile* IRIS benchmark comes from quantile choice, on our construction of the data (the QRF vs CV-QR comparison remains unsettled);
  4. a reproducibility package.

## 2. Related work
* **PMT design and evaluation:** Coady et al. 2004; Grosh & Baker 1995; Schreiner 2006 (out-of-sample validation of scorecards).
* **Asset indices vs targeting tools:** Filmer & Pritchett 2001.
* **ML in economics:** Varian 2014; Hastie, Tibshirani & Friedman 2009.
* **Forests and quantiles:** Breiman 2001 (random forests); Meinshausen 2006 (QRF); Lin & Jeon 2006; Koenker 2005 (quantile regression).
* **Critiques of PMT accuracy:** Brown, Ravallion & van de Walle (2018), *J. Dev. Econ.* [verify citation details].
* **Inference with resampled splits:** Nadeau & Bengio (2003), *Machine Learning* [verify].
* **Replication in economics:** [verify: cite a methodological reference on replication; none verified yet].

## 3. Data and methodology
* **Data:**
  * Bolivia Encuesta de Hogares 2005 (INE), source URL and SHA-256 checksums;
  * N = 4,086 households;
  * the 21 IRIS variables, with the mapping verified against the codebook (`data_construction_audit.py`).
* **Target:** `G_TOTAL_pc`, monthly per-capita household expenditure. **Limitation:** the authors' aggregate is not named, and the distribution fingerprint shows that it differs (§5).
* **Poverty line:** 24.2th percentile = 189.09 Bs (frozen). The article is internally inconsistent here (text 24.2%; Table 3 24.03%; Table A1 row 5 implies 24.04%). Sensitivity shown.
* **Metrics:** published Table 2 (p. 534). PA = TP/(TP+FN); UC, LE and BPAC all use the TP+FN denominator. Note the 2015 working-paper typo and the "precision" wording on p. 534.
* **Models:**
  * IRIS QR(0.42);
  * CV-QR (500 × 3-fold CV inside the training sample);
  * stochastic ensemble (RF and QRF, 500 trees, mtry = 7, OOB-BPAC selection over a 0.01 grid);
  * the decision tree, reported only as a reference.
* **Frozen methodology:** `METHODOLOGY_REFERENCE.md` (SPECIFIED, RECONSTRUCTED, ADAPTED and NOT IMPLEMENTED tags, with page references). Put a condensed version in the appendix.

## 4. Experimental setup
* **Published protocol:** two N/2 draws with replacement, then 1,000 bootstrap resamples of the test sample. Seed 42 (the published seed is unknown).
* **Adaptations:**
  * a disjoint 50/50 split;
  * 30 repeated splits;
  * paired bootstrap CIs instead of Tukey-Kramer tests (rationale: `results/cv_qr/PHASE2_3_RESULTS.md`).
* **Robustness dimensions:**
  * metric definition (C1);
  * benchmark tuning (fixed vs CV quantile);
  * validation overlap;
  * quantile-selection optimism;
  * poverty-line reconstructions (188.77, 189.05, 194.10 Bs, training-sample line);
  * halved and doubled lines (Table A2).
* **Software:** Python 3.14, scikit-learn 1.8.0, quantile-forest 1.4.2. R emulation for the implementation audit.

## 5. Results and discussion

Suggested order, with the table each section draws on:

| Section | Content | Source |
|---|---|---|
| 5.1 | Replication against Table A1: IRIS, CV-QR, SE | `RESULTS.md` §1; `results/cv_qr/PHASE2_3_RESULTS.md` |
| 5.2 | The unreplicated SE result (A8): implementation ruled out; data construction differs | `results/a8_audit/A8_AUDIT.md` |
| 5.3 | Within-data comparison: SE vs CV-QR vs IRIS (paired bootstrap; 3-split pilot; quantile path in `STEP5_SENSITIVITY_RESULTS.md`) | `results/cv_qr/paired_comparisons.csv`; `audit_2026-11-04_repeated_split/` (n = 3 pilot) |
| 5.4 | How much do methodological choices move the headline? Metric definition; benchmark tuning; overlap; selection optimism | `RESULTS.md` §0, §3, §5 |
| 5.5 | Poverty-line sensitivity, including Table A2 and the 170–210 Bs scan | `RESULTS.md` §4; `results/table_a2/`; `STEP5_SENSITIVITY_RESULTS.md` |
| 5.6 | Inconsistencies in the published article | `METHODOLOGY_REFERENCE.md` §5 (A1, A2, A9) |

**Discussion points:**
* ML gains for targeting should be judged against a benchmark tuned on the same footing.
* Reporting standards: exact formulas, constructed data, seeds and splits.

## 6. Limitations
* One country.
* The welfare aggregate differs from the authors' (unidentified).
* No R run; R behaviour was emulated from source code.
* The CV-QR vs SE comparison rests on 1 split per protocol plus a 3-split pilot.
* Unpublished seed, and IRIS's training subset is unknown.
* Survey weights not used, following the paper.
* The halved-line results are very noisy.

## 7. Conclusion
* Partial replication: the linear benchmarks replicate; the forest result does not, and the most likely source is data construction.
* On our data, the forest's advantage over a cross-validated linear quantile regression is small and unsettled: one split per protocol shows no clear difference, a 3-split pilot leans towards QRF under the overlapping protocol, and this is confounded with overlap inflation. Each method peaks at a different quantile (quantile path).
* Recommendations for PMT evaluation practice.
* **[decide]** Whether to include a second country before submission (see `FINAL_RESEARCH_ASSESSMENT.md` §6).

## Appendices (planned)
* **A.** Methodology reference, condensed.
* **B.** Data construction and codebook audit.
* **C.** Implementation audit: R `quantregForest` / `randomForest` emulation, with source checksums.
* **D.** Full robustness tables.
* **E.** Reproducibility instructions.

## Venue
Target a journal or section that publishes replications and robustness studies **[verify scope and requirements before choosing; no venue has been confirmed]**. No claim about acceptance or ranking is made.
