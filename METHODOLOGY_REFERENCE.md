# Methodology reference (frozen 2026-11-03)

**Reference:** McBride, L. and Nichols, A. (2018). "Retooling Poverty Targeting Using Out-of-Sample Validation and Machine Learning." *World Bank Economic Review* 32(3): 531–550. doi:10.1093/wber/lhw056.

* **Copy used:** the publisher's typeset version of record, hosted by the World Bank Open Knowledge Repository (bitstream `fc38c300-c05d-537f-852e-d37610020264`). It is stored locally as `reference/McBride_Nichols_2018_WBER.pdf`, SHA-256 `087f3c64…b824d`. This is copyrighted, so it must not be redistributed.
* **Page references** are journal pages; PDF page *n* is journal page 530 + *n*.
* **The 2015 working paper** (`improvedtargeting_12jan2015.pdf`, SHA-256 `28446c7e…8832`) is **superseded**. It is cited below only where it explains an earlier decision.

## Change control

These rules apply to every future change to this methodology:

1. A decision in this file changes only with **concrete evidence**. That means a quoted page, table, equation or footnote from the reference, or a reproducible numerical check.
2. Every proposed correction must state:
   * the evidence;
   * why the current decision is wrong;
   * its measured impact on existing results.
3. "Another reading also seems plausible" is **not** a reason to change anything. Such cases are recorded under *Unresolved ambiguities* (Section 5).
4. Before any change, archive the results under `archive/<date>_<reason>/` with a SHA-256 manifest.

Status labels used below:

| Label | Meaning |
|---|---|
| **SPECIFIED** | The paper states it explicitly. We follow it. |
| **RECONSTRUCTED** | The paper is silent. We chose a value and record the choice. |
| **ADAPTED** | We deliberately depart from, or add to, the paper. The reason is given. |
| **NOT IMPLEMENTED** | The paper specifies it, but our pipeline does not do it yet. |

---

## 1. Metrics

| # | Decision | Status | Evidence |
|---|---|---|---|
| M1 | Confusion matrix: P = true very poor, P̂ = predicted very poor | SPECIFIED | Table 1, p. 534 |
| M2 | **TA = (TP+TN)/(TP+TN+FP+FN)** | SPECIFIED | Table 2 and text, p. 534 |
| M3 | **PA = TP/(TP+FN)** | SPECIFIED | Table 2 and text, p. 534: "the correctly predicted very poor as a percentage of the total true very poor" |
| M4 | **UC = FN/(TP+FN)** | SPECIFIED | Table 2, p. 534 |
| M5 | **LE = FP/(TP+FN)**, which can exceed 1 | SPECIFIED | Table 2, p. 534; footnote 6, p. 535 |
| M6 | **BPAC = TP/(TP+FN) − \|FN/(TP+FN) − FP/(TP+FN)\|** = PA − \|UC − LE\| | SPECIFIED | Table 2 and text, p. 534 |
| M7 | Very poor if expenditure **< line** (strict); predicted very poor if prediction **< line** | RECONSTRUCTED | The paper does not state the tie rule. With continuous expenditure the measured effect is 0 (no household sits exactly on 189.0915). |
| M8 | If TP+FN = 0, PA, UC, LE and BPAC are set to 0 | RECONSTRUCTED | Not specified. This never happens at our thresholds. |

**Numerical evidence for M3–M6.** Every point-estimate row of Table A1 (p. 545–546, rows 1 and 5 for each country) satisfies both PA + UC = 100 and BPAC = PA − |UC − LE|, to rounding. This is checked in `tests/test_metrics.py`. Both identities hold only when all denominators are TP+FN.

**Correction C1.** The pre-freeze code used TP+FP as the denominator for PA and BPAC, copied from the 2015 working paper's Table 2. That formula contradicts:
* the 2015 paper's own text and its own Table A1 numbers;
* the published Table 2.

Measured impact (seed 42, `results/audit/correction_impact.csv`): TA, UC and LE are unchanged.

| Protocol | IRIS BPAC | IRIS PA | QRF(0.40) BPAC |
|---|---|---|---|
| Paper | 0.611 → 0.586 | 0.662 → 0.633 | 0.665 → 0.674 |
| Disjoint | 0.574 → 0.510 | 0.704 → 0.624 | — |

The old values are archived in `archive/2026-11-03_pre_methodology_freeze/`.

**Inconsistency inside the reference.** Page 534 also says "poverty accuracy (also known as precision…)". That conflicts with the formula, because TP/(TP+FN) is recall, not precision. We follow the formula, because the tables are numerically consistent only with the formula (Section 5, A1).

## 2. Data and target

| # | Decision | Status | Evidence |
|---|---|---|---|
| D1 | Bolivia 2005 Encuesta de Hogares, **N = 4,086 households** | SPECIFIED | Table 3, p. 538. Our build gives 4,086. |
| D2 | 21 IRIS-selected variables (hhsize, hhsize², age head, age head², regions, rural, sublease, brick wall, wood wall, dirt floor, cement floor, fridge, radio, tv, dvd, fan, car, number beds, number kitchens, number computers, sheep) | SPECIFIED (names only) | Table 3, p. 538 |
| D3 | Each variable's survey source and coding (codebook-verified) | RECONSTRUCTED | The paper gives names only. Checked by `data_construction_audit.py`. |
| D4 | `sublease` = rented tenure (`s7_02 == 1`); `num_kitchens` = binary dedicated-kitchen indicator | RECONSTRUCTED | EH 2005 has no sublease code and no kitchen count. |
| D5 | `regions`: ordinal department code (1–9) for tree models; 8 dummies plus intercept for linear quantile regression | RECONSTRUCTED | Encoding not stated. 9 vs 8 dummies gives identical predictions (`RESULTS.md`). |
| D6 | Target = `G_TOTAL_pc`, the publicly available expenditure aggregate | SPECIFIED in principle | p. 537–538: authors restricted themselves to data with "publicly available" income/expenditure aggregates. The exact variable is not named. |
| D7 | "Very poor" = poorest half of those below the national poverty line, or below $1/day | SPECIFIED (concept) | p. 533 |
| D8 | **Line = 24.2th percentile of `G_TOTAL_pc`** in the full sample = 189.0915 Bs | RECONSTRUCTED | The paper gives no line in Bs. The text on p. 538 says "24.2 percent in Bolivia", but Table 3 (p. 538) says **24.03**. See Section 5, A2. |
| D9 | Survey weights are not used | RECONSTRUCTED | The paper never mentions weights. |

## 3. Split, bootstrap and model selection

| # | Decision | Status | Evidence |
|---|---|---|---|
| S1 | Training and testing samples are **two independent draws of size N/2, with replacement** | SPECIFIED | p. 539: "randomly draw, with replacement, two samples of size N/2" |
| S2 | A **single** split (no iteration over splits) | SPECIFIED | p. 539: "Over this split of the data"; one set of results per method in Table A1 |
| S3 | Seed 42 with `np.random.RandomState`, training sample drawn first | RECONSTRUCTED | The seed is not published. |
| S4 | Test evaluation on **1,000 bootstrap resamples** of the testing sample. Report the mean, the SE (SD of the replicates), and the 95% percentile CI (2.5th, 97.5th). | SPECIFIED | p. 539; Table A1 notes a and b, and its Std. err. rows |
| S5 | The same resample indices for every model (`BOOT_SEED = 42`) | RECONSTRUCTED | Not specified. This makes model comparisons paired. |
| S6 | **IRIS benchmark:** quantile regression at τ = 0.42 trained on the training sample, tested as in S4 | SPECIFIED | p. 539: "training their preferred model in the training data"; Table A1 row 2 |
| S7 | **Stochastic ensemble (SE) selection:** RF and QRF fit on the training sample; the preferred model is the one with the **best BPAC on out-of-bag (OOB) predictions** | SPECIFIED | p. 539: "We select our preferred model as that with the lowest BPAC error in the OOB sample" |
| S8 | SE candidates are RF (conditional mean) and QRF at quantiles **0.01, 0.02, …, 0.99** | RECONSTRUCTED | The grid is not stated. Reported choices such as QRF(0.41), (0.47), (0.57), (0.26) and (0.54) imply a resolution of 0.01. |
| S9 | OOB is computed per **row**: duplicated households in the with-replacement training sample are treated as separate rows | RECONSTRUCTED (follows R `randomForest`) | R computes OOB per row. This leaks between copies of the same household; see Section 5, A4. |
| S10 | Ties in OOB BPAC: the first candidate wins (RF before QRF, lower quantile before higher) | RECONSTRUCTED | Not specified. |
| S11 | **Cross-validation (CV) approach:** linear quantile regression with τ chosen by 500 iterations of 3-fold CV on BPAC in the training sample, giving CV Q(0.38) for Bolivia | **NOT IMPLEMENTED** | p. 539; Table A1 rows 6–8. This is the paper's best-performing method, and it is pending your decision (Section 6). |
| S12 | Model comparison by **Tukey-Kramer tests** on bootstrap means | **NOT IMPLEMENTED** | p. 539; Table 4, p. 542. We report paired bootstrap CIs for differences instead (ADAPTED: bootstrap replicates are not independent observations, so test statistics computed on them are not meaningful). |
| S13 | Robustness at **halved and doubled** poverty lines | **NOT IMPLEMENTED** | p. 539; Table A2, p. 547. We report the 189.05, 194.10 and training-sample thresholds instead (ADAPTED). |

## 4. Model specifications

| # | Decision | Status | Evidence |
|---|---|---|---|
| F1 | RF: R `randomForest` | SPECIFIED | p. 539 (Liaw and Wiener 2002) |
| F2 | 500 trees | SPECIFIED | p. 539; footnote 10 |
| F3 | Features tried at each split = one third of 21 = **7**. sklearn `max_features=1/3` also gives 7. | SPECIFIED as "typically"; matches the R default | p. 536; `randomForest` 4.7-1.2 regression default `mtry = max(floor(p/3), 1)` |
| F4 | Bootstrap rows with replacement, sample size = n | RECONSTRUCTED (R default) | `randomForest`: `replace = TRUE`, `sampsize = nrow(x)`. sklearn defaults are the same. |
| F5 | Minimum terminal node size 5, as sklearn `min_samples_leaf=5` | RECONSTRUCTED (R default) | `randomForest` regression default `nodesize = 5`. R's `nodesize` is not exactly the same as sklearn's `min_samples_leaf`; see Section 5, A3. |
| F6 | QRF follows Meinshausen and **keeps all training observations in each leaf** | SPECIFIED | Appendix, QRF algorithm step 1, p. 544: "retain the value of all observation in a given region, not just their average" |
| F7 | QRF via R `quantregForest` 1.3-5, which passes `ntree`, `mtry` and `nodesize` through to `randomForest` | SPECIFIED (package) | p. 539; references (Meinshausen 2016). The 1.4-0 manual: "Other arguments passed to randomForest such as nodesize or mtry". Version 1.3-5 itself was not checked. |
| F8 | Python `scikit-learn` 1.8.0 and `quantile-forest` 1.4.2 instead of R | ADAPTED | R is not used here. Implementation differences are an acknowledged limitation. |
| F9 | Linear quantile regression: HiGHS solver, no penalty (`alpha = 0`), with intercept | RECONSTRUCTED | IRIS software is not specified. |
| F10 | Decision Tree (`max_depth=10`, `min_samples_leaf=20`) | ADAPTED (not in the paper) | Kept as a reference learner. It is not part of the replication. |

**Correction C2.** `quantile-forest` defaults to `max_samples_leaf=1`, which stores one sampled value per leaf. That is not the published algorithm (F6). The pipeline now sets `max_samples_leaf=None`, which stores all values. Evidence: p. 544, plus the `quantile-forest` source, which states "Maximum number of samples to store per tree leaf", default 1. Predictions differ (for example, the second test household's 41st-percentile prediction is 278.4 under the old setting and 270.3 under the new one). Measured impact on QRF(0.40) BPAC (seed 42): paper split 0.674 → 0.667; disjoint split 0.625 → 0.630.

**Correction C3.** Before the freeze, we chose the quantile by 5-fold grouped CV on a 0.05 grid. That choice was made while only the 2015 draft was available, and the 2015 draft selected on the test set. The published paper specifies OOB BPAC (S7) and implies a 0.01 grid (S8), so the pipeline now uses that rule. Both the old and new rules use only training data. Measured impact (seed 42): the selected model changes from QRF(0.40) to QRF(0.43) on the paper split (BPAC 0.667 → 0.653), and stays at QRF(0.40) on the disjoint split.

## 5. Unresolved ambiguities

These are recorded and left unchanged.

| ID | Ambiguity | Current choice | Evidence each way | Measured impact |
|---|---|---|---|---|
| A1 | p. 534 calls PA "precision", but the formula is recall | Formula (recall) | The formula and every row of Table A1 are consistent only with recall. | — |
| A2 | Bolivia poverty rate: "24.2 percent" (text, p. 538) vs **24.03%** (Table 3, p. 538) | 24.2% → 189.0915 Bs | The 2018 text and the 2015 Table 3 give 24.2. The IRIS Bolivia accuracy submission (IRIS 2009) was not consulted. The 2018 Table 3 gives 24.03. P24.03 = 188.7743 Bs. | 189.05 Bs, which is 0.04 Bs from P24.2, already showed a negligible effect. P24.03 is 0.32 Bs away. Measured over 30 splits: mean change in BPAC is at most 0.010 for every model; the largest change in a single split is 0.080. |
| A3 | R `nodesize = 5` (nodes smaller than this are not split) vs sklearn `min_samples_leaf = 5` (every leaf must have at least 5) | `min_samples_leaf=5` | Neither is an exact equivalent in sklearn. | Not measured. Would need an R run. |
| A4 | OOB with a training sample drawn with replacement: a household's duplicate can be in-bag while its copy is OOB | Per-row OOB, as R does | This is what the paper's software would do. It is optimistic. | The disjoint protocol (ADAPTED) has no duplicates and serves as the check. |
| A5 | "Lowest BPAC error" (p. 539): read as highest BPAC | Highest BPAC | Same ranking either way, since error = 1 − BPAC. | None |
| A6 | Which RF/QRF candidates and quantile grid were searched | RF plus QRF on a 0.01 grid (S8) | Not stated. | — |
| A8 | **Our QRF outperforms the published SE QRF.** Seed 42, paper split: QRF(0.41) BPAC 0.673 and SE QRF(0.43) 0.653, vs published 50.18 [39.26, 58.57]. The published paper finds SE ≈ IRIS (+0.85, not significant); we find SE − IRIS ≈ +0.16 to +0.20. | Not resolved; reported as a discrepancy | Candidates (untested): R vs Python, A3, feature coding (D3–D5), seed or split. Our IRIS replication lies inside the published CI, so the gap is specific to the forest. | — |
| A9 | Paper appendix (p. 544): Meinshausen QRF "retain the value of all observation". Cited software `quantregForest` 1.3-5 (verbatim source): **one** randomly sampled response per leaf per tree, from all n training rows, with an unweighted type-7 quantile over the trees. | Text (C2: `max_samples_leaf=None`) | The text says one thing, the software another. | ≤ 0.007 BPAC (`results/a8_audit/`, E1/E3) |
| A10 | R `nodesize=5` makes children with ≤ 5 rows terminal, and children may be smaller than 5 (`regTree.c`). sklearn equivalent: `min_samples_split=6, min_samples_leaf=1`. Frozen: `min_samples_leaf=5` (F5). | Frozen F5 | Source code shows F5 is **not** the exact R rule. | +0.038 BPAC (SE) when R's rule is used (E2). The gap to the published value **widens**. Not changed; you decide. |
| A7 | IRIS used a random half of the Bolivia data for its in-sample PAT (p. 538) | We use the full sample for the replication row | Stated by the authors themselves. | It explains part of the row-1 vs row-5 gap. |

**Evidence added 2026-11-03 (A8 audit, `results/a8_audit/A8_AUDIT.md`):**

* **A2:** published Table A1 row 5 implies, through TA = 1 − p(UC + LE), a poverty rate of **24.038%**. This supports Table 3's 24.03%.
* **A8:** the forest implementation is ruled out as the cause. The authors' welfare distribution is confirmed to differ from `G_TOTAL_pc`:
  * At half and double the line they report 4.92% and 62.26%; ours gives 6.07% and 57.00%.
  * The cause is not identified.

No frozen decision was changed.

## 6. Decisions pending (yours)

The paper specifies these, and they are not implemented. Under the freeze, they will not be added without your approval.

1. **S11: the CV quantile regression approach.** *Now implemented as a separate audit output (`cv_qr_baseline.py`, `results/cv_qr/`). It is not part of the frozen primary pipeline.* This is the paper's main result for Bolivia: CV Q(0.38), BPAC 57.94. It is a selection procedure for the existing IRIS model family, not a new learner.
2. **S12: Tukey-Kramer tests.** Paired bootstrap CIs are currently used instead.
3. **S13: halved and doubled poverty lines.** *Now implemented as a separate audit output (`table_a2_robustness.py`, `results/table_a2/`).* Originally: the paper's robustness analysis in Table A2.

## 7. Deliberate adaptations kept

These are the robustness extension, not the replication:

* **Disjoint 50/50 split,** an untouched test set (no shared households). It addresses A4 and S1-type overlap.
* **30 repeated splits** per protocol.
* **Thresholds 189.05 Bs, 194.10 Bs, the training-sample P24.2, and P24.03.**
* **Fixed-quantile comparisons:** QRF(0.40) (2015 draft), QRF(0.41) (published SE choice), QRF(0.45) (earlier result).
* **Test-set-selected quantile,** reported only to measure optimism. It is never the primary result.
