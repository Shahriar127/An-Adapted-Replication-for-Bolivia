# Final research assessment: Bolivia PMT replication

**Date:** 2026-11-04.

**Reference:** McBride, L. & Nichols, A. (2018), "Retooling Poverty Targeting Using Out-of-Sample Validation and Machine Learning", *World Bank Economic Review* 32(3): 531–550 (doi:10.1093/wber/lhw056).

**Scope of evidence.** Only outputs computed with the **published metric definitions** are used here (Table 2, p. 534: PA = TP/(TP+FN); every rate uses the TP+FN denominator). The pre-freeze archive (`archive/2026-11-03_pre_methodology_freeze/`) used TP+FP for PA and BPAC and is **not used**.

**Sources:**
* `RESULTS.md` (frozen primary)
* `METHODOLOGY_REFERENCE.md`
* `results/a8_audit/A8_AUDIT.md`  
* `results/cv_qr/PHASE2_3_RESULTS.md`
* `results/table_a2/`
* `audit_2026-11-04_repeated_split/` (pilot only)

**Supersession note.** `RESULTS.md` §1 (frozen, not edited) lists the A8 causes as "none tested". They were tested afterwards; see §4 below and `results/a8_audit/A8_AUDIT.md`.

---

## 1. What this study investigates

It is an **adapted replication** of the Bolivia results in McBride & Nichols (2018). It uses the same public survey (EH 2005, N = 4,086) and a methodology frozen against the article, with every decision page-referenced and tagged SPECIFIED, RECONSTRUCTED, ADAPTED or NOT IMPLEMENTED.

**Research question:**

> Do the published Bolivia results replicate, and how sensitive are the reported ML targeting gains to metric definition, benchmark tuning, validation design and poverty-line reconstruction?

## 2. What has been replicated

| Element | Our result | Published | Status |
|---|---|---|---|
| Sample | N = 4,086 households | 4,086 (Table 3) | **Exact** |
| IRIS QR(0.42) benchmark, test bootstrap | BPAC 0.586 [0.486, 0.657], PA 0.633 | BPAC 49.33 [36.73, 60.48], PA 57.58 (row 2) | BPAC inside the published CI. PA just above its upper bound (62.65). *Row 2 is IRIS's own reported result on IRIS's subset and split, not the authors' rerun.* |
| CV linear QR (500 × 3-fold, training only) | **q = 0.37**; PA 0.665, UC 0.335, LE 0.369, BPAC 0.623 [0.557, 0.673] | **q = 0.38**; PA 63.37, UC 36.63, LE 41.61, BPAC 57.94 [50.61, 63.44] | PA, UC, LE and BPAC inside the published CIs; TA 0.39 points above |
| Doubled poverty line (Table A2) | BPAC 0.809–0.837 (paper protocol) | 80.62–81.92 | Levels agree; all methods perform about the same, as published |
| Poverty rate used in computations | Row 5 implies **24.038%** | Table 3: 24.03% | Consistent |

## 3. Where we differ, with confirmed reasons

| Difference | Confirmed reason | Evidence |
|---|---|---|
| **Stochastic-ensemble (SE) QRF:** ours BPAC 0.653 (QRF(0.43)), published 50.18 [39.26, 58.57] | **Not identified (A8).** Ruled out: implementation, split variation, poverty rate. | §4 |
| Welfare-variable distribution | **Confirmed to differ.** Rates at half and double the line: ours 6.07% / 57.00%; published 4.92% / 62.26%. These are model-free. None of the 9 aggregates available in the file matches. | `results/a8_audit/a8_data_diagnostics_fingerprint.csv` |
| In-sample linear refit (row 5) | **Confirmed residual construction difference.** PA and UC match (61.10 vs 60.69), but LE is 24.95 vs 33.71 and TA 84.65 vs 82.45. 21 pre-specified variants do not close it. | `results/a8_audit/a8_data_diagnostics_row5.csv` |
| Halved poverty line | Linear QR chooses q = 0.51 against the published 0.22–0.24. BPAC levels are similar (0.33 vs 0.30), but the CIs span about 0.3. Rates differ (6.09% vs 4.92%). | `results/table_a2/` |
| Earlier "QRF(45), BPAC 0.797" | **Confirmed artefact:** inconsistent configuration (`min_samples_leaf=1`) plus the overlapping split | `results/audit/config_audit.csv` |
| Earlier PA/BPAC values | **Confirmed:** the TP+FP formula, a typo in the 2015 working paper | Correction C1 |

## 4. What remains unresolved: A8

**Confirmed:** the gap is not caused by any of these.
* **Forest implementation.** An exact emulation of R `quantregForest` 1.3-5 and `randomForest` 4.6-12 behaviour was validated against sklearn's OOB predictions to 1.6e-12, and the source files are byte-checked with SHA-256 in `audit_2026-11-04_repeated_split/evidence/r_source/`.
  * Over 20 splits, no single implementation factor moves the SE BPAC by more than 0.013.
  * R's node-size rule *raises* it by about 0.04, widening the gap.
* **Split variation:** the published value lies 3–10 split-SDs below ours.
* **Poverty rate:** ≤ 0.002 BPAC.

**Plausible hypothesis (untested):** the authors' welfare aggregate and feature construction (both confirmed to differ) hurt the forest more than the linear model.
* For: on our construction SE ≈ CV-QR, whereas in the paper CV-QR beats SE by 7.76 points (Table 4).
* Against, or unexplained: our IRIS and CV-QR land inside the published CIs despite the same construction difference.
* Testing it needs the authors' constructed data or code.

## 5. Why the evidence does not show that QRF outperforms the published method

1. **Different data.** Our QRF and the published QRF were trained on welfare variables with demonstrably different distributions, so their scores are not on a common footing.
2. **On our data, QRF vs CV-QR is not settled, and the gap is small relative to protocol effects.** Paired bootstrap on identical test households, one split each:
   * disjoint split: BPAC difference −0.004 [−0.053, +0.056];
   * paper split: −0.030 [−0.109, +0.065].

   The 3-split pilot under the published protocol leans towards QRF (−0.038 to −0.068), but it is confounded with overlap inflation of about +0.035 (§7). The large margins over IRIS (+0.16 to +0.20 across 30 splits) are against a **fixed, untuned** benchmark quantile. The quantile path (`STEP5_SENSITIVITY_RESULTS.md`) shows that each method peaks at a different q, and at their training-selected q they differ by only +0.013.
3. **Repeated-split evidence is thin.** Only a 3-split pilot exists (§7); the planned 10-split comparison was not run.
4. **Statistical scope.** Paired bootstrap CIs capture test-sample uncertainty for one fitted model, not split-to-split variation. We report no Tukey-Kramer-style significance.

## 6. Is a second country necessary?

**As a replication and robustness study: no, not essential.**

The Bolivia study can stand as a *single-country adapted replication* provided:
* it is framed as one;
* it reports the partial replication (IRIS, CV-QR and doubled line replicate; SE does not);
* it presents the robustness findings as Bolivia-specific.

**For any general claim** (about ML vs linear PMT, or about how fragile reported gains are), **yes**: one survey cannot support generalisation.

What each country would add:
* **East Timor (TLSS 2001, N = 1,800; published benchmark is a probit).**
  * Tests whether the SE ≈ CV-QR pattern holds for a different benchmark family and a small sample.
  * The published SE − IRIS gap there is small (Table 4: BPAC +1.29).
* **Malawi (IHS2 2004/05, N = 11,280).**
  * A large sample and a high poverty rate, so less noise.
  * Note that the article is inconsistent here too: Table 3 2018 gives 64.78%, against 90.4% in the 2015 draft **[verify which rate the tables use]**.
  * The most informative test of whether the A8 pattern is Bolivia-specific.

**Extra work, per country:**
* World Bank microdata registration and a data-access agreement;
* mapping about 21 variables against the codebook;
* identifying the welfare aggregate, which runs into the same A8 risk;
* adding loaders and audits;
* CV-QR at about 40 minutes per split.

Realistically this is several days of careful work per country, plus write-up.

**Recommendation:** finish and write the Bolivia study now as a replication and robustness paper. Treat a second country (Malawi first) as a separate, optional extension, and decide on it after the draft exists.

## 7. Repeated-split pilot (seeds 1000–1002, published protocol)

*Pilot only, n = 3. This is not the planned 10-split study, which was stopped by your decision of 2026-11-04.*

Same households for both methods; training-only selection; published overlapping split. Full record: `audit_2026-11-04_repeated_split/REPEATED_SPLIT_RESULTS.md` and `outputs/pilot_per_split_results.csv`.

**Pilot checks passed:**
* the seed-42 CV stage was reproduced exactly;
* 0 convergence warnings and 0 failed fits;
* about 26 minutes per split.

| Seed | CV-QR | QRF (OOB) | ΔBPAC CV-QR − QRF [95% test-bootstrap CI] |
|---|---|---|---|
| 1000 | q 0.33: 0.625 | q 0.41: 0.664 | −0.039 [−0.077, 0.000] |
| 1001 | q 0.34: 0.626 | q 0.40: 0.694 | −0.068 [−0.110, +0.004] |
| 1002 | q 0.34: 0.659 | q 0.39: 0.697 | −0.038 [−0.084, +0.025] |

* QRF scored higher in all 3 pilot splits. Every per-split CI reaches or crosses zero.
* The overlapping split is known to flatter the QRF by about +0.035 BPAC (`RESULTS.md` §5), which is the same size as these differences.
* **Conclusion:** the pilot neither establishes a QRF advantage nor confirms equivalence. The earlier "SE ≈ CV-QR" statement is **single-split evidence only**.

## 8. Summary by evidence type

**Confirmed findings**
1. N and the variable construction follow the EH 2005 codebook. All codebook checks pass.
2. Published metrics: PA = TP/(TP+FN) and BPAC = PA − |UC − LE|. Every point-estimate row of Table A1 obeys these identities, and the unit tests check this.
3. The IRIS benchmark and the CV-QR baseline replicate within the published CIs, except TA for CV-QR and PA for IRIS, which are just above.
4. The SE QRF does not replicate. Implementation, split variation and poverty rate are ruled out as causes.
5. The welfare distribution differs from the authors' (model-free evidence).
6. On our data, SE QRF and CV-QR are indistinguishable on one split per protocol. A 3-split pilot under the overlapping protocol leans towards QRF, so equivalence is **not confirmed**. Most of the QRF advantage over the fixed-quantile IRIS benchmark is a quantile-choice effect (quantile path).
7. **Methodological sensitivity on our data:**
   * the metric definition moves IRIS BPAC by 0.025–0.064;
   * overlapping train/test draws add about +0.035 BPAC to SE and about 0 to IRIS;
   * test-set quantile selection adds +0.022 to +0.024;
   * the poverty-line reconstructions 188.77, 189.05 and 194.10 Bs change mean SE BPAC by ≤ 0.010, and model rankings do not change.
8. **The published article is internally inconsistent** in three places:
   * the Bolivia poverty rate: 24.2% in the text vs 24.03% in Table 3 (row 5 implies 24.04%);
   * "precision" wording for a recall formula;
   * the appendix QRF description vs the cited software's behaviour (A9).

**Plausible hypotheses**
* A8 is caused by the welfare aggregate and feature construction.
* The authors' welfare variable is a different expenditure aggregate. Food expenditure per capita is the closest fingerprint, but it does not match.

**Limitations**
* One country and one survey.
* The authors' welfare aggregate is unidentified.
* No native R run; R behaviour was emulated from verified source.
* The published seed and IRIS's training subset are unknown.
* Survey weights not used, following the paper.
* CV-QR vs SE rests on 1 split per protocol plus a 3-split pilot.
* The halved-line results are very noisy.
* Python vs R implementations.

**Future work (short list)**
1. Request the constructed data or code from the authors. This is the only direct route to resolving A8.
2. Optional: one more country (Malawi).

## 9. What the work can legitimately contribute

* A **transparent, reproducible adapted replication** of a widely used ML-for-PMT result. It includes:
  * a frozen, page-referenced methodology;
  * an archive of superseded results;
  * checksums;
  * unit tests.
* **Documented reporting problems:**
  * the metric-formula typo in the 2015 working paper;
  * internal inconsistencies in the 2018 article.

  These matter to anyone reusing BPAC.
* **Evidence that headline ML gains are sensitive to evaluation choices.** In this Bolivia replication:
  * benchmark tuning, the metric definition and validation overlap each shift BPAC by amounts comparable to the published gains;
  * the forest's advantage over IRIS shrinks to a small, unsettled difference against a cross-validated linear benchmark.
* A **partial-replication result with diagnostics:** the linear methods replicate, the forest does not, and the discrepancy is localised to data construction rather than the algorithm.

This is a replication and robustness contribution. It does **not** show that QRF is better or worse than the published method, and no claim about journal tier or acceptance is made.
