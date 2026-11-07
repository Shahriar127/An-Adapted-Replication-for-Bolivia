# Validation Design, Quantile Tuning, and Threshold Reconstruction in Machine-Learning Proxy Means Tests: An Adapted Replication for Bolivia

Md. Shahriar Jubair Mahim, Abdullah Al Masud, and A S M Delowar Hossain

*Author note:* Md. Shahriar Jubair Mahim (corresponding author) and Abdullah Al Masud are with the Department of Computer Science and Engineering, Mawlana Bhashani Science and Technology University (MBSTU), Tangail, Bangladesh; the corresponding author's email address is shahriarjubair27@gmail.com. A S M Delowar Hossain is an Associate Professor in the Department of Computer Science and Engineering, MBSTU.

## Abstract

Proxy means tests (PMTs) predict household welfare from easily verified characteristics in order to target transfers. McBride and Nichols (2018) reported that cross-validation and quantile regression forests (QRF) improve the out-of-sample accuracy of the USAID Poverty Assessment Tools. We re-analyse their Bolivia data (Encuesta de Hogares 2005, N = 4,086) under a methodology frozen against the article. We compare the IRIS quantile-regression benchmark, a cross-validated linear quantile regression (CV-QR) and an out-of-bag-selected QRF under overlapping and disjoint validation splits, reconstructed poverty lines and two metric definitions. The CV-QR result replicates (selected quantile 0.37 vs 0.38; BPAC 0.623 vs 0.579). The published QRF result does not (0.653 vs 0.502): an implementation audit rules out software and split variation, and model-free diagnostics show that our welfare variable differs from the authors'. The overlapping split raises QRF accuracy by about 0.035 BPAC and leaves the linear benchmark essentially unchanged. Test-set quantile selection adds 0.022–0.024. The working-paper metric formula shifts the benchmark's BPAC by 0.025–0.064. Reconstructed poverty lines barely change accuracy and do not change method rankings. On single-split evidence, much of the QRF advantage over the fixed-quantile benchmark reflects the choice of quantile; against a tuned linear model the difference is small and unsettled. Evaluation choices move PMT accuracy by amounts comparable to the reported machine-learning gains. Benchmarks should be tuned on the same footing as machine-learning models, validated on disjoint data, and reported with explicit formulas and constructed data.

**JEL classification:** I32, I38, C52, C53

**Key words:** proxy means test, poverty targeting, machine learning, quantile regression forest, replication, out-of-sample validation, Bolivia

---

**PMT background.** Targeting social transfers to the poorest households requires information on welfare that is costly to collect. Proxy means tests address this by predicting household welfare from a small set of observable, verifiable characteristics, such as dwelling materials, assets and household composition, estimated on a nationally representative survey (Grosh and Baker 1995; Coady et al. 2004). PMTs are widely used. Their accuracy is debated, including evidence of substantial targeting errors in African applications (Brown et al. 2018), a review concluding that every targeting mechanism produces inclusion and exclusion errors (Devereux et al. 2017), comparisons with community-based targeting (Alatas et al. 2012), and discussion of the trade-off between targeted and universal transfers (Hanna and Olken 2018).

**ML in targeting.** Machine-learning (ML) methods are increasingly considered for targeting because they prioritise out-of-sample prediction (Varian 2014; Mullainathan and Spiess 2017). Examples include PMT development (McBride and Nichols 2018; Sohnesen and Stender 2017), poverty prediction from satellite imagery and phone metadata (Jean et al. 2016; Blumenstock et al. 2015), phone-based targeting of humanitarian aid and anti-poverty programmes (Aiken et al. 2022, 2023), and the study of accuracy–fairness trade-offs in algorithmic targeting (Noriega-Campero et al. 2020).

**The study we replicate.** McBride and Nichols (2018) re-estimated the USAID Poverty Assessment Tools (PAT) built by the IRIS Center. They reported that two approaches improve out-of-sample targeting accuracy, measured by IRIS's Balanced Poverty Accuracy Criterion (BPAC; IRIS Center 2005):
* selecting the linear quantile-regression quantile by cross-validation;
* using stochastic-ensemble methods (random forests and QRF).

**Why evaluation choices matter.** A targeting tool's reported accuracy is not a property of the algorithm alone. It also depends on:
1. how training and test data are separated;
2. whether tuning choices, here the prediction quantile, are made without the test data;
3. where the poverty line is drawn, which is often reconstructed because the original value is unpublished;
4. how the accuracy metric is defined.

The machine-learning literature documents optimism when models are selected on evaluation data (Varma and Simon 2006; Cawley and Talbot 2010) and when information leaks between training and test data (Kaufman et al. 2012). Kapoor and Narayanan (2023) find leakage in 294 papers across 17 fields, and show in one re-analysis that complex models lose their advantage over logistic regression once the errors are corrected. In a targeted (not systematic) search of Crossref and OpenAlex on 2026-11-04 (search queries in Online Appendix C), we found ML-for-PMT studies (section I) but none that examined validation overlap, test-set tuning, poverty-line reconstruction and metric definitions together for a published ML-for-PMT result, using that study's own data and benchmarks. A systematic review could still find one, so we state this gap as the result of our search, not as a proven absence.

**Research question.**

> *How sensitive are machine-learning poverty-targeting models to reconstructed poverty thresholds and alternative validation procedures?*

It is studied through five sub-questions:
* **RQ1:** How does the validation procedure affect estimated targeting performance?
* **RQ2:** How stable is quantile selection, and how optimistic is test-set selection?
* **RQ3:** How sensitive are the results to reconstructed poverty thresholds?
* **RQ4:** How do metric definitions affect reported conclusions?
* **RQ5:** Are the observed gains attributable to forest flexibility or to quantile tuning?

**Contributions.** We separate the replication findings from our own methodological contributions.

*Replication findings:*
1. A partial replication of the Bolivia results. The linear benchmarks are close to the published values; the published QRF result is not reproduced.
2. A documented audit of the remaining discrepancy (A8), which rules out implementation and split variation and identifies a difference in the welfare variable.

*Methodological contributions:*
1. A sensitivity analysis of validation design, quantile selection, thresholds and metric definitions.
2. Evidence that the comparison between a forest and a quantile-tuned linear model is far closer than the comparison with a fixed-quantile benchmark.
3. Documentation of internal inconsistencies in the published reporting.
4. A reproducibility package with a frozen, page-referenced methodology.

## I. Related Work

**Traditional PMT.**
* PMT weights are typically obtained by regressing household consumption, expenditure or income on candidate proxies (Grosh and Baker 1995). Principal-components asset indices address a different problem, namely measuring wealth rather than targeting (Filmer and Pritchett 2001).
* Applied PMT designs include food-subsidy targeting in Egypt (Ahmed and Bouis 2002). Coady et al. (2004) review targeting methods and their performance across programmes.
* Evidence on PMT accuracy includes a field experiment comparing PMT with community methods (Alatas et al. 2012) and a multi-country assessment of econometric targeting in Africa (Brown et al. 2018).
* For Bolivia, Klasen and Lange (2015) use ROC analysis to show that PMTs identify poor households poorly when transfers are targeted narrowly, that much of the resulting leakage goes to non-poor households close to the poverty line, and that the link between targeting accuracy and poverty impact is weak.
* Devereux et al. (2017) review inclusion and exclusion errors across targeting mechanisms (means tests, PMT, categorical, geographic, community-based and self-selection). They conclude that all mechanisms generate errors and costs and that there is no single best mechanism.
* Hanna and Olken (2018) discuss when targeting errors make universal transfers attractive.

**ML-based poverty prediction and targeting.**
* McBride and Nichols (2018) apply cross-validation, random forests (Breiman 2001) and QRF (Meinshausen 2006) to the PAT data for Bolivia, East Timor and Malawi. Schreiner (2006) is cited by them as an early out-of-sample validation of poverty scorecards.
* Sohnesen and Stender (2017) compare out-of-sample poverty predictions in six countries and find random forests often more accurate than the usual stepwise and Lasso imputation models, but no method predicts poverty consistently well over time.
* Recent ML-based PMTs include a field-tested model for water-subsidy targeting in Ghana, compared with a wealth index, a poverty scorecard, community-based targeting and a government programme (Poulin et al. 2022), and PMT models for Indonesia that add area-level features and data augmentation (Wobcke and Mariyah 2023).
* Non-survey data have also been used: satellite imagery (Jean et al. 2016), mobile-phone metadata (Blumenstock et al. 2015), and phone data for targeting humanitarian and anti-poverty transfers (Aiken et al. 2022, 2023). Noriega-Campero et al. (2020) study the accuracy and fairness of algorithmic targeting.
* *How this study differs:* these studies propose or compare predictive models. We take one published comparison as given and ask how much its conclusions depend on evaluation choices.

**Quantile regression and QRF.**
* Linear quantile regression estimates conditional quantiles (Koenker and Bassett 1978; Koenker 2005). A quantile below the median shifts predictions downwards and thereby trades undercoverage for leakage.
* Random forests can be viewed as adaptive nearest-neighbour weighting (Lin and Jeon 2006). QRF uses this weighting to estimate the full conditional distribution (Meinshausen 2006).
* Software implementations differ in how they compute sample quantiles (Hyndman and Fan 1996). This matters for our implementation audit (section IV.7).

**Validation, model selection and leakage.**
* Selecting hyper-parameters on the data used to report performance biases the estimate upwards (Varma and Simon 2006; Cawley and Talbot 2010). Arlot and Celisse (2010) survey cross-validation for model selection.
* Overlap between training and evaluation data is a form of leakage (Kaufman et al. 2012). Kapoor and Narayanan (2023) document leakage across many fields and propose a taxonomy of its types.
* Out-of-bag estimates are a convenient tuning criterion for forests, but their accuracy has been questioned: in binary classification they can overestimate the error, depending on the forest's parameters (Janitza and Hornung 2018). This is relevant because the published stochastic ensemble selects its quantile by OOB BPAC.
* Hand (2006) argues that simple classifiers often perform almost as well as sophisticated ones, and that the difference may be swamped by uncertainties that standard comparisons ignore. Our RQ5 asks this question for PMT.
* Variance estimates from repeated resampled splits are biased downwards because the splits share observations. Nadeau and Bengio (2003) propose a corrected variance. Percentile bootstrap intervals (Efron and Tibshirani 1993) quantify test-sample uncertainty, but not training-sample or split variation.

**Replication and transparency.** We follow Clemens (2017) in distinguishing replication types. Our study is a *reproduction/robustness* exercise using the same survey under documented adaptations, not a re-run of the authors' code. Christensen and Miguel (2018) review evidence on limited replicability in economics and the role of open data and materials.

**Poverty-line sensitivity.**
* In poverty *measurement*, the choice of line is recognised as a judgement, and dominance conditions are used to check whether poverty comparisons hold over a range of lines (Atkinson 1987). Ravallion and Bidani (1994) find an Indonesian poverty profile highly sensitive to some measurement choices and robust to others.
* Our threshold scan applies the same idea, checking a conclusion over a band of lines, to *targeting-model rankings*. In our search we found no study that examines poverty-line reconstruction in ML-PMT evaluation, so we make no literature claim beyond this analogy.

## II. Data and Methodology

This section describes the data, the models and the accuracy metrics. How the models are trained, validated and compared is described in section III. The full methodology, with page references to the published article and each decision tagged SPECIFIED, RECONSTRUCTED, ADAPTED or NOT IMPLEMENTED, is given in Online Appendix A.

### II.1 Data
* **Survey:** Bolivia Encuesta de Hogares 2005 (Instituto Nacional de Estadística 2005), as used in the published study.
* **Sample:** after household-level aggregation, N = 4,086 households, matching the published sample size (McBride and Nichols 2018, table 3, p. 538).
* **Features:** the 21 IRIS-selected variables (published table 3, p. 538): household size and its square; age of head and its square; region; rural; sublease; brick and wood walls; dirt and cement floors; fridge; radio; television; DVD; fan; car; number of beds; number of kitchens; number of computers; sheep.
* **Variable mapping:** checked against the survey codebook (34 automated checks, all passed). Three variables are approximations:
  * `sublease` is coded as rented tenure;
  * `number of kitchens` is binary in EH 2005;
  * `region` is ordinal for trees and eight dummies for linear models.

### II.2 Welfare variable and poverty classification
* **Welfare variable:** monthly per-capita household expenditure (`G_TOTAL_pc`). The article does not name its aggregate, beyond restricting itself to surveys with publicly available aggregates (pp. 537–538).
* **Classification:** a household is "very poor" if its welfare is below the line; it is predicted very poor if its prediction is below the line.
* **Primary line:** the 24.2th percentile of `G_TOTAL_pc`, 189.09 Bs per person per month, following the article's text ("24.2 percent", p. 538). The line is derived from the data and uses the full sample.
* **Internal inconsistency in the article:**
  * table 3 (p. 538) reports 24.03%.
  * Published table A1 row 5 implies a rate of 24.038% through the identity TA = 1 − p(UC + LE).
  * We keep the frozen 24.2% and report P24.03 (188.77 Bs) as a sensitivity analysis.

### II.3 Models

| Model | Specification |
|---|---|
| **IRIS benchmark** | Linear quantile regression at the published quantile 0.42. Intercept and 8 region dummies; HiGHS solver; no penalty. |
| **CV-QR** | The published cross-validation approach (p. 539): 500 iterations of 3-fold CV inside the training sample, selecting the quantile (grid 0.01–0.99) with the highest mean held-out BPAC, then refitting on the full training sample. A documented two-stage evaluation reduces computation (section III.4). |
| **Stochastic ensemble ("SE")** | Random forest and QRF (500 trees, 7 of 21 features per split, minimum leaf size 5, all leaf observations retained), via scikit-learn (Pedregosa et al. 2011) and quantile-forest (Johnson 2024). The preferred model is the candidate (RF, or QRF at q = 0.01–0.99) with the highest **out-of-bag** BPAC on the training sample (p. 539). In every analysis reported here a QRF was selected, never the RF. |
| **Reference models** | A conditional-mean random forest, and a decision tree (an adaptation; not in the paper). |

### II.4 Metrics (published definitions)

Rates are reported as proportions (0–1); published percentages are converted, and "published" refers to McBride and Nichols (2018) unless stated otherwise. The metrics follow published table 2 (p. 534), with TP, FP, FN and TN from the very-poor confusion matrix:

| Metric | Formula |
|---|---|
| TA | (TP+TN)/N |
| PA | TP/(TP+FN) |
| UC | FN/(TP+FN) |
| LE | FP/(TP+FN) |
| BPAC | TP/(TP+FN) − \|FN/(TP+FN) − FP/(TP+FN)\| = PA − \|UC − LE\| |

**Two consequences of the published definitions** (verified numerically to 2·10⁻¹⁶):
1. PA + UC = 1, so PA and UC carry identical information.
2. BPAC is piecewise:
   * **BPAC = 1 − LE** when LE ≥ UC (FP ≥ FN);
   * **BPAC = 2·PA + LE − 1** when UC > LE.

   BPAC therefore peaks near FP = FN.

**The earlier formula.** The 2015 working-paper version (McBride and Nichols 2015) printed TP+FP denominators for PA and BPAC. The published table 2 and every point-estimate row of published table A1 are consistent only with TP+FN. The page also calls PA "precision" while defining recall (p. 534).

### II.5 Adaptations and differences from the published study

| | |
|---|---|
| **Adapted** | Python instead of R; the disjoint protocol; repeated splits; paired bootstrap instead of Tukey-Kramer; two-stage CV computation; the decision-tree reference model. |
| **Reconstructed** | Seed; quantile grid; poverty-line value; variable codings; IRIS dummy design; tie-breaking. |
| **Known divergences** | The welfare aggregate (section IV.7); QRF leaf storage (the paper's text vs its cited software, A9); R's node-size rule vs our minimum leaf size (A10). |

## III. Experimental Setup

This section describes how the models in section II are trained, validated and compared, and which experiment answers which research question.

### III.1 Validation procedures

| Procedure | Description |
|---|---|
| **Published (overlapping) protocol** | Training and test samples are two independent draws of size N/2 *with replacement* (p. 539). About 40% of unique test households also appear in training. |
| **Disjoint protocol (adaptation)** | A random 50/50 partition, so the test set is untouched. |
| **Seeds** | The published seed is unknown. Primary results use seed 42. Repeated-split analyses use 30 splits per protocol (seeds 1000–1029). |
| **Training-only selection** | All quantile and model choices use training data only. A test-set-selected quantile is reported *only* to measure optimism. |

### III.2 Fixed configuration and model selection

All settings are fixed a priori in one configuration module shared by every script. The article does not report tree hyper-parameters, so these are reconstructed choices (R `randomForest` regression defaults for the forests).

| Item | Setting |
|---|---|
| Decision tree (reference) | maximum depth 10, minimum leaf size 20 |
| Random forest | 500 trees, 1/3 of features per split, minimum leaf size 5 |
| QRF | 500 trees, 1/3 of features per split, minimum leaf size 5, all leaf observations retained |
| IRIS benchmark | linear QR at q = 0.42, no penalty, HiGHS solver, intercept + 8 region dummies |
| Quantile grid | 0.01–0.99 in steps of 0.01 (forest OOB selection and CV-QR) |
| SE selection | highest out-of-bag BPAC on the training sample over RF and QRF(0.01–0.99) |
| Fixed comparison quantiles | QRF(0.40), QRF(0.41), QRF(0.45) |
| Bootstrap | 1,000 resamples of the test sample, seed 42, identical indices for every model |
| Poverty line (primary) | P24.2 of the full sample, 189.09 Bs (section II.2) |

### III.3 Uncertainty quantification
* **Test-sample uncertainty:** 1,000 bootstrap resamples of the test sample, with the mean and 95% percentile intervals (Efron and Tibshirani 1993). The same resample indices are used for every model, so model contrasts are *paired*.
* **Paired bootstrap instead of Tukey-Kramer.** The published Tukey-Kramer tests (table 4) treat bootstrap replicates as independent observations. Their test statistics then grow with the number of replicates, which the analyst chooses. We therefore report paired bootstrap intervals and no significance tests.
* **What the intervals do not cover:** training-sample or split variation. That is described separately by repeated splits. Because splits overlap, across-split dispersion is descriptive only (Nadeau and Bengio 2003).

### III.4 CV-QR computation

* **Published procedure:** 500 iterations of 3-fold cross-validation inside the training sample over the quantile grid 0.01–0.99; the quantile with the highest mean held-out BPAC is refitted on the full training sample (p. 539).
* **Two-stage evaluation (adaptation):** Stage 1 runs 50 iterations over the full grid. Stage 2 runs the remaining 450 iterations (500 in total) for quantiles within ±0.10 of each line's stage-1 best. Every excluded quantile trailed the stage-1 leader by at least 6.65 standard errors.
* **Check:** across the 10/50/100/250/500-iteration checkpoints the seed-42 choice varied only between 0.36 and 0.37 (section IV.3).

### III.5 Experimental design by research question

| Question | Experiment | Protocol(s) | Splits | Results |
|---|---|---|---|---|
| Replication | Comparison with published table A1 (IRIS, CV-QR, SE) | published | seed 42 | section IV.1 |
| RQ1 | SE, fixed QRF(0.40) and QRF(0.45), IRIS, RF under both protocols; legacy configuration | both | 30 (seeds 1000–1029) | section IV.2 |
| RQ2 | OOB-selected vs test-selected quantile; QRF(0.40) vs QRF(0.45); stability of selected q | both | 30 | section IV.3 |
| RQ3 | Reconstructed lines 188.77, 189.05, 194.10 Bs and a training-sample P24.2 | both | 30 | section IV.4 |
| RQ3 | Continuous scan 170–210 Bs in steps of 0.5 Bs (81 lines plus the frozen line, 82 in total) | both | seed 42 | section IV.4, figure 1 |
| RQ3 | Published halved and doubled lines (table A2 analogue) | published | seed 42 | section IV.4 |
| RQ4 | Published vs 2015 metric formula; corrections applied one at a time | both | seed 42 | section IV.5 |
| RQ5 | Paired CV-QR vs SE vs IRIS contrasts | both | seed 42 | section IV.6 |
| RQ5 | CV-QR vs QRF pilot | published | 3 (seeds 1000–1002) | section IV.6 |
| RQ5 | Quantile path q = 0.30–0.50 (step 0.01) for QRF and linear QR | disjoint | seed 42 | section IV.6, figure 2 |
| A8 | One-factor implementation audit and R emulation | published | seed 42 + 20 (seeds 1000–1019) | section IV.7 |
| A8 | Data-construction diagnostics (distribution fingerprint, in-sample refit) | none (full sample) | — | section IV.7 |

### III.6 Software, computation and reproducibility controls

* **Software:** Python 3.14.8 with NumPy 2.3.5, pandas 3.0.1, SciPy 1.17.1, scikit-learn 1.8.0 (Pedregosa et al. 2011) and quantile-forest 1.4.2 (Johnson 2024). The original study used R; R behaviour relevant to A8 was emulated from verified source code, not executed (section IV.7).
* **Hardware:** one Linux workstation with 12 CPU cores. The frozen pipeline runs in under 10 minutes; the CV-QR step takes about 40 minutes per protocol.
* **Controls:**
  * a frozen methodology document with change control, and superseded results archived with SHA-256 checksums;
  * 23 unit tests, including the identities in the published table A1 rows;
  * training-only selection enforced by a unit test;
  * checksums of the raw survey files;
  * an automated check of every number in this manuscript against the result files.

## IV. Results

### IV.1 Replication against the published results (published protocol, seed 42)

**Table 1.** Replication against the Published Results (Published Protocol, Seed 42)

| Model | TA | PA | UC | LE | BPAC [95% CI] | Published counterpart |
|---|---|---|---|---|---|---|
| IRIS QR(0.42) | 0.840 | 0.633 | 0.367 | 0.324 | 0.586 [0.486, 0.657] | QR(0.42): TA 0.819, PA 0.576, UC 0.424, LE 0.343, BPAC 0.493 [0.367, 0.605] |
| CV-QR, selected q = 0.37 | 0.837 | 0.665 | 0.335 | 0.369 | 0.623 [0.557, 0.673] | CV QR(0.38): 0.818, 0.634, 0.366, 0.416, 0.579 [0.506, 0.634] |
| SE, selected QRF(0.43) | 0.861 | 0.688 | 0.312 | 0.289 | 0.653 [0.558, 0.713] | SE QRF(0.41): 0.802, 0.553, 0.447, 0.404, 0.502 [0.393, 0.586] |
| RF (conditional mean) | 0.854 | 0.481 | 0.519 | 0.112 | 0.074 [−0.028, 0.172] | — |
| Decision tree (reference) | 0.834 | 0.488 | 0.512 | 0.203 | 0.178 [0.078, 0.276] | — |

*Notes:* Test-sample bootstrap means [95% CI] over 1,000 resamples. Published values are from table A1 of McBride and Nichols (2018, 545–546), converted to proportions.

Comparing our point estimates with the published 95% intervals:

* **CV-QR:** the selected quantile (0.37 vs 0.38), PA, UC, LE and BPAC lie inside the published intervals. TA (0.837) is just above the published upper bound (0.833).
* **IRIS:** BPAC and LE lie inside the published intervals. TA, PA and UC lie just outside: TA 0.840 vs 0.837; PA 0.633 vs 0.627; UC 0.367 vs 0.374.
  * Published row 2 is IRIS's own reported result, computed on IRIS's training subset and split. So this comparison is less direct than the CV-QR one.
* **SE QRF:** all five metrics lie outside the published intervals, all in the direction of higher accuracy for our QRF. This is discrepancy A8 (section IV.7).
* **Selected forest quantile:** 0.43 on this split. Across 30 splits the selection ranged from 0.36 to 0.43, which includes the published 0.41.

### IV.2 RQ1: Validation protocol

**Table 2.** BPAC by Validation Protocol over 30 Random Splits

| Model | Published (overlapping) | Disjoint | Difference |
|---|---|---|---|
| SE (OOB-selected QRF) | 0.679 (0.030) | 0.644 (0.029) | −0.036 |
| QRF(0.40) fixed | 0.673 (0.040) | 0.638 (0.035) | −0.035 |
| QRF(0.45) fixed | 0.534 (0.072) | 0.489 (0.060) | −0.045 |
| IRIS QR(0.42) | 0.483 (0.052) | 0.481 (0.054) | −0.002 |
| RF (conditional mean) | 0.014 (0.075) | −0.052 (0.053) | −0.066 |

*Notes:* Mean (SD) of BPAC point estimates on the test sample, 30 splits per protocol (seeds 1000–1029). Difference = disjoint − published.

**Finding.** Moving from overlapping to disjoint validation lowers the forest models' BPAC by 0.035–0.066 and leaves the linear benchmark practically unchanged.

**A more extreme case: the legacy configuration.** A pre-freeze configuration combined unrestricted trees with `min_samples_leaf = 1` and a different random-number stream. Under the published metric definitions it scored:
* fixed QRF(0.40): BPAC 0.784 on the overlapping split vs 0.586 on a disjoint split;
* decision tree: 0.749 vs 0.457.

The splits differ between those two runs, so the gap is indicative rather than a controlled estimate.

### IV.3 RQ2: Quantile selection

* **Stability (30 splits).** The training-only OOB rule selected:
  * published protocol: q between 0.36 and 0.43 (modes 0.39 and 0.40, 8 splits each);
  * disjoint protocol: q between 0.37 and 0.42 (mode 0.40, 12 splits).

  CV-QR selected 0.37 (published protocol) and 0.34 (disjoint) on seed 42. In the three pilot splits it selected 0.33, 0.34 and 0.34. Across the 10/50/100/250/500-iteration checkpoints the seed-42 choice varied only between 0.36 and 0.37.
* **Optimism of test-set selection.** Choosing the QRF quantile with hindsight on the test sample raises mean BPAC over the training-only choice:
  * published protocol: +0.024 (higher in 22 of 30 splits);
  * disjoint protocol: +0.022 (21 of 30).
* **Sensitivity to a fixed quantile.** QRF(0.40) − QRF(0.45):
  * BPAC: +0.139 (published) and +0.148 (disjoint), positive in 29 of 30 splits under both;
  * PA: +0.057 / +0.060;
  * LE: +0.068 / +0.074.

  A five-point change in the quantile moves BPAC by more than the published difference between the QRF and IRIS.

### IV.4 RQ3: Poverty-threshold sensitivity

**Reconstructed lines (30 splits).** Mean change in BPAC relative to 189.09 Bs:

| Line | Effect |
|---|---|
| 188.77 Bs (P24.03) | ≤ 0.010 in absolute value, all models |
| 189.05 Bs | ≤ 0.001 |
| 194.10 Bs | SE +0.007 / +0.008; IRIS +0.020 / +0.021; RF +0.040 / +0.041 |
| Training-sample P24.2 (ranging 179.4–201.0 Bs) | ≤ 0.012, all models except RF on the disjoint split (+0.022) |

Single-split changes can be larger. For example, the largest absolute change at 188.77 Bs across all models and splits was 0.080. This reflects the non-smooth BPAC.

**Continuous scan, 170–210 Bs** (seed 42; 82 lines; figure 1):
* The ordering of method families, with the best QRF above IRIS and IRIS above RF and DT, is the same at all 82 lines under both protocols.
* The only family-level changes are swaps between the two weak conditional-mean models (RF and DT) at 20 lines (disjoint) and 17 lines (published).
* On the disjoint split, every QRF variant exceeds IRIS at every line; the smallest margin is +0.095.
* On the published split, the OOB-selected QRF falls *below* IRIS at 13 lines between 170.0 and 177.5 Bs (worst −0.055), while fixed QRF(0.40) stays above it (smallest margin +0.021).
* The paired interval for the OOB-selected QRF minus IRIS excludes zero at 38 of 82 lines (disjoint) and 15 of 82 (published). Neighbouring lines share almost all households, so these counts are descriptive, not independent tests.

**Published halved and doubled lines (table A2 analogue, seed 42, published protocol):**
* **Doubled line (378.18 Bs):** our BPACs are 0.811, 0.809 and 0.837 (in-sample-tuned IRIS, CV-QR, SE), against the published 0.811, 0.819 and 0.806.
* **Halved line (94.55 Bs):**
  * Intervals are wide; for example CV-QR gives 0.334 [0.143, 0.461].
  * Our linear models select q = 0.51, whereas the published ones select 0.22–0.24.
* **Rates differ:** at the halved and doubled lines they are 6.09% and 57.10% in our data, against 4.92% and 62.26% published. These comparisons are therefore approximate.


<!-- FIGURE 1 -->
### IV.5 RQ4: Metric definition

Applying the published definitions in place of the 2015 working-paper formula (McBride and Nichols 2015), on the same split and bootstrap draws:

| Model | Published split | Disjoint split |
|---|---|---|
| IRIS BPAC | 0.611 → 0.586 | 0.574 → 0.510 |
| IRIS PA | 0.662 → 0.633 | 0.704 → 0.624 |
| QRF(0.40) BPAC | 0.665 → 0.674 | 0.622 → 0.625 |

* The correction therefore widens the QRF–IRIS gap by 0.034–0.067 BPAC.
* It also reverses an earlier qualitative conclusion: under TP+FP, PA favoured QRF(0.45) over QRF(0.40); under the published definition QRF(0.40) has the higher PA.

### IV.6 RQ5: Forest flexibility or quantile tuning?

**Paired comparison on identical test households (seed 42).** BPAC differences [95% paired test-bootstrap CI]:

| Contrast | Published protocol | Disjoint protocol | Published table 4 (Bolivia) |
|---|---|---|---|
| CV-QR − IRIS | +0.037 [−0.056, +0.126] | +0.116 [−0.026, +0.226] | +0.086 |
| SE − IRIS | +0.067 [+0.002, +0.137] | +0.120 [−0.011, +0.222] | +0.009 (not significant in the paper) |
| CV-QR − SE | −0.030 [−0.109, +0.065] | −0.004 [−0.053, +0.056] | +0.078 |

**Repeated splits against the fixed benchmark.** SE − IRIS was positive in 30 of 30 splits under both protocols, with mean +0.196 (published) and +0.162 (disjoint).

**Three-split pilot of CV-QR vs QRF** (published protocol, seeds 1000–1002, same households, training-only selection):

| Seed | CV-QR | QRF | Δ (CV-QR − QRF) [95% test-bootstrap CI] |
|---|---|---|---|
| 1000 | 0.625 | 0.664 | −0.039 [−0.077, 0.000] |
| 1001 | 0.626 | 0.694 | −0.068 [−0.110, +0.004] |
| 1002 | 0.659 | 0.697 | −0.038 [−0.084, +0.025] |

* QRF scored higher in all three splits, but each interval reaches or crosses zero.
* The pilot had no convergence warnings and no failed fits, and it reproduced the seed-42 CV stage exactly.
* The planned 10-split comparison was not run.

**Quantile path (disjoint split, seed 42; figure 2).** Test BPAC as a function of q for the QRF and the linear QR:
* **Best in hindsight:** linear QR peaks at q = 0.36 (0.663); QRF at q = 0.40–0.41 (0.642).
* **At a common fixed q:** at q = 0.42, IRIS's quantile, QRF leads by 0.078 (0.587 vs 0.509). At q = 0.36 linear QR leads by 0.110 (0.663 vs 0.554).
* **At each method's training-selected quantile:** QRF at 0.40 gives 0.642, and linear QR at 0.34 gives 0.629, a difference of +0.013.

**Finding.** Much of the large QRF advantage over the IRIS benchmark is an advantage over a *fixed* quantile. Against a quantile-tuned linear model, the difference is:
* small on one disjoint split;
* not distinguishable from zero on seed 42 under either protocol;
* in favour of QRF in a three-split pilot under the overlapping protocol, which is known to inflate forests (section IV.2).

The evidence does not settle whether the forest adds accuracy beyond quantile tuning.


<!-- FIGURE 2 -->
### IV.7 The replication discrepancy A8

Our SE QRF exceeds the published SE QRF: 20-split mean BPAC 0.685 in the A8 runs, about 7.2 split standard deviations above the published 0.502. We audited the implementation one factor at a time on the published protocol (seed 42 plus 20 splits), against the frozen baseline B0.

**R emulation.** We built a Python emulation of R `quantregForest` 1.3-5 (Meinshausen 2016) and `randomForest` 4.6-12 (Liaw and Wiener 2002) from their byte-verified source:
* one randomly drawn response per leaf from all training rows;
* a type-7 quantile across trees (Hyndman and Fan 1996);
* R's out-of-bag (OOB) procedure.

The emulation's in-bag reconstruction matches the library's OOB predictions to 1.6·10⁻¹².

**Table 3.** Implementation Audit of the QRF Discrepancy (A8)

| Factor changed | Δ BPAC |
|---|---|
| One value per leaf (`quantile-forest`) | +0.004 |
| Exact `quantregForest` 1.3-5 leaf/quantile/OOB procedure | −0.004 |
| R node-size rule (`min_samples_split = 6`, leaves may be smaller than 5) | **+0.038** |
| Full R emulation (procedure + node rule) | **+0.040** |
| OOB with duplicated households merged | −0.003 |
| Region one-hot | +0.002 |
| Log target | −0.002 |
| P24.03 line | −0.002 |

*Notes:* Change in mean SE BPAC relative to the frozen baseline B0, published protocol, 20 splits (seeds 1000–1019).

* Every configuration leaves our QRF between 3.0 and 10.0 split standard deviations above the published value.
* Emulating R's node-size rule *raises* our BPAC, widening the gap.

**Data-construction diagnostics.** Two deterministic checks, involving no random split:
1. **Distribution fingerprint.** At half and double the line, the poverty rates are 4.92% and 62.26% published (table A2), against 6.07% and 57.00% for our welfare variable (P24.03 base). None of the nine aggregates available in the survey file matches. The closest is food expenditure per capita, at 5.82% and 62.90%.
2. **In-sample refit of published row 5** (QR(0.42) on the full sample):
   * PA and UC agree closely: ours 0.611 / 0.389 vs published 0.607 / 0.393.
   * LE and TA do not: LE 0.250 vs 0.337, TA 0.847 vs 0.825.
   * None of 21 pre-specified variants in target, threshold and design closes the gap; the best reaches LE 0.270.

**Status:**
* **Confirmed:** the welfare-variable distribution and the in-sample linear behaviour differ from the authors'.
* **Ruled out:** implementation differences and split variation.
* **Not established:** that this data difference *causes* the forest discrepancy. Our linear models land near the published intervals despite the same difference.

**A8 remains unresolved.**

## V. Discussion

Each subsection below answers one question: what we observed, why it plausibly happens, and how firm the explanation is. **Evidence status** uses the labels of the claim–evidence table in Online Appendix B: *confirmed* (directly computed), *consistent with* (the data fit the explanation, but it was not tested separately) and *hypothesis* (not tested).

### V.1 Why does overlapping validation raise forest performance? (RQ1)

**What we observed.** Moving from the overlapping to the disjoint protocol lowers mean BPAC over 30 splits by 0.035–0.066 for every forest model. The linear IRIS benchmark changes by only 0.002 (table 2).

**Why the overlap exists.** The published protocol draws training and test samples of N/2 independently and with replacement. A given household is absent from one draw of N/2 with probability (1 − 1/N)^(N/2) ≈ e^(−1/2), so it is in the training draw with probability about 1 − e^(−1/2) ≈ 39%. This is an algebraic consequence of the protocol and matches the observed share of about 40% of unique test households.

**Why it helps forests and not the linear model.**
* A forest with small terminal nodes (5 observations here) predicts a training household from a handful of neighbours that include the household itself. When the same household reappears in the test sample, its prediction is close to its own recorded welfare, and it is likely to be classified correctly.
* A 29-parameter linear quantile regression cannot fit individual households this closely, so a household's presence in training barely changes its own prediction.
* Two observations fit this explanation:
  * the conditional-mean RF, the most flexible fit to individual welfare values, gains most (0.066);
  * the legacy configuration with `min_samples_leaf = 1`, where each leaf can isolate a single household, shows the largest gap (0.784 vs 0.586; different splits, so indicative only).
* This is the train–test leakage described by Kaufman et al. (2012). Kapoor and Narayanan (2023) report that correcting leakage can remove the apparent advantage of complex models over simple ones; our result is a milder case of the same pattern.

**Evidence status.** The size of the protocol effect is *confirmed*. The memorisation mechanism is *consistent with* the evidence but remains a *hypothesis* (claim M16). We did not compare accuracy separately for test households that do and do not also appear in training.

### V.2 Why does selecting the quantile on test data give optimistic results? (RQ2)

**What we observed.** Choosing the QRF quantile with hindsight on the test sample raises mean BPAC by 0.024 (published protocol) and 0.022 (disjoint) over the training-only OOB rule.

**Why.**
* The test-selected quantile is, by construction, the best of 99 candidates *on the very sample used to score it*. Its score is the maximum of 99 noisy estimates, and the maximum of noisy estimates is biased upwards even when the candidates are equally good. This is the selection bias described by Varma and Simon (2006) and Cawley and Talbot (2010).
* The data show this structure exactly. Test-set selection was never worse than the OOB rule in any split. It was better in 22 of 30 splits (published) and 21 of 30 (disjoint), and identical in the remaining 8 and 9 splits, where both rules picked the same quantile.
* The bias matters more than its size suggests because BPAC is steep in the quantile. Under the published definitions, BPAC peaks where false positives and false negatives balance (FP ≈ FN, section II.4), so the quantile works like a calibration parameter. Two examples:
  * moving from QRF(0.45) to QRF(0.40) changes BPAC by about 0.14 (section IV.3);
  * at the 170 Bs line on the published split, QRF(0.40) scores 0.620 and QRF(0.41) 0.581, so a 0.01 change in the quantile moves BPAC by 0.039.

**Evidence status.** The optimism is *confirmed*, and its direction follows from the construction of the test-selected score. Why the curve is steep follows from the BPAC algebra (*confirmed*); how steep it is depends on the data and the split.

### V.3 Why does the model ranking stay the same when the poverty threshold changes? (RQ3)

**What we observed.** Across 82 lines from 170 to 210 Bs (poverty rates 20.3%–28.4% of the full sample), the family ordering QRF > IRIS > conditional-mean models never changes on either protocol. Mean BPAC over 30 splits moves by at most 0.010 at 188.77 Bs and 0.001 at 189.05 Bs (section IV.4).

**Why.**
* *The gaps between families are larger than the movement caused by the line.* The conditional-mean models score far below the quantile models at every line (for example RF 0.074 vs IRIS 0.586 at the primary line). A mean regression shrinks predictions towards the centre of the welfare distribution, so few households are predicted to be below a line near the 24th percentile. The RF accordingly has UC 0.519 against LE 0.112 (table 1), and moving the line by a few bolivianos cannot remove an imbalance of that size.
* *Quantile models can be recalibrated to the line.* The OOB rule re-selects the QRF quantile at each line (between 0.41 and 0.45 on the published split), which keeps FP and FN roughly balanced as the line moves. The IRIS quantile is fixed at 0.42 and cannot adapt in this way.
* *Nearby lines classify almost the same households.* The reconstructed lines 188.77 and 189.05 Bs lie within 0.32 Bs of 189.09 Bs. Because the lines are sample percentiles, moving from P24.2 to P24.03 reclassifies 0.17% of the sample, about 7 of 4,086 households. This is why the mean effects are so small.

**The exception, and what it shows.** On the published split the OOB-selected QRF falls below IRIS at 13 lines between 170.0 and 177.5 Bs. At those lines the OOB rule chose q = 0.41–0.42; at 56 of the other 69 lines it chose 0.43–0.45. Fixed QRF(0.40) stays above IRIS at every line, while fixed QRF(0.41) falls below it at 6 lines. At 174.5 Bs the scores are QRF(0.40) 0.675, QRF(0.41) 0.633, IRIS 0.622 and the OOB-selected QRF(0.42) 0.568. The reversal therefore comes from the quantile chosen at those lines, not from a failure of the forest. This is the steep quantile sensitivity of section V.2 again.

**Evidence status.** The ranking stability is *confirmed* on one split (seed 42) for the scan, and over 30 splits for the reconstructed lines. The explanations are *consistent with* the reported metrics; the claim that the gaps between families exceed the effect of the line is a direct comparison of reported numbers. The poverty-measurement literature checks conclusions over a range of lines in the same spirit (Atkinson 1987; Ravallion and Bidani 1994), which supports reporting a band of lines rather than a single reconstructed value.

### V.4 Why could the published QRF result not be reproduced? (A8)

**What we observed.** Our QRF reaches BPAC 0.653 on seed 42 and a mean of 0.685 over the 20 A8 splits, against the published 0.502. The linear models land close to their published values.

**Candidate explanations and their status:**

| Candidate explanation | Test | Status |
|---|---|---|
| Different quantile | Fixing our QRF at the published q = 0.41 gives 0.673 [0.614, 0.722] on seed 42 and 0.658 on average over 30 splits; the published value is 0.502 [0.393, 0.586] | **Ruled out:** the gap remains |
| Random split / seed | The published value lies 3.0–10.0 split standard deviations below ours in every configuration | **Ruled out** |
| Python vs R implementation | Emulation of R `quantregForest` and `randomForest` (leaf sampling, type-7 quantile, OOB procedure, node-size rule) | **Ruled out:** emulating R *raises* BPAC by up to 0.040 |
| Duplicated households in OOB selection | OOB with duplicates merged: −0.003 | **Ruled out** as a main cause |
| Feature coding, log target, P24.03 line | changes of ±0.002 | **Ruled out** as a main cause |
| Different welfare variable | Distribution fingerprint (6.07% / 57.00% vs 4.92% / 62.26% at half and double the line); in-sample linear refit differs in LE (0.250 vs 0.337) | **Difference confirmed; causal link not established** |
| Unknown data cleaning, IRIS training subset or code details | Not testable without the authors' data or code | **Open** |

**Why the welfare variable is the leading candidate but not a confirmed cause.**
* It is the only factor shown to differ between our data and the authors'. None of the nine aggregates in the survey file reproduces the published distribution.
* It does not explain why our *linear* models match the published values while the forest does not. We have no evidence on why a different welfare variable would affect the forest more than the linear models, and we do not speculate on a mechanism.
* The difference is therefore a *necessary caveat* on every level comparison with the published forest, and the most promising lead for resolving A8 with the authors' data. It is not an explanation of the gap.

**What this means for interpretation.**
* We cannot say whether our forest is better or worse than the published one.
* The within-data comparisons (sections IV.2–IV.6) do not depend on resolving A8, because all models there use the same households and the same welfare variable.

### V.5 Forest flexibility or quantile tuning? (RQ5)

* The IRIS benchmark uses a quantile chosen in-sample on IRIS's data (0.42). On our data it sits to the right of the linear model's optimum (about 0.34–0.37), so the QRF with a tuned quantile is compared against a mis-calibrated linear model.
* When the linear quantile is also tuned (CV-QR), the gap narrows: the seed-42 contrasts include zero, and at the training-selected quantiles the difference is 0.013 on the disjoint split.
* The published paper itself reports that CV-QR outperforms the stochastic ensemble for Bolivia (table 4). That fits the view that quantile tuning, rather than forest flexibility, drives much of the gain. Hand (2006) makes the same general point: simple methods often perform almost as well as sophisticated ones once other sources of uncertainty are considered.
* Our three-split pilot leans the other way under the overlapping protocol, which section V.1 shows favours forests. **The question is open.**

### V.6 Metric definitions (RQ4)

* Under the published definitions, PA and UC are redundant (PA + UC = 1), and BPAC reduces to 1 − LE whenever a model over-predicts poverty. Leakage therefore drives the ranking for the quantiles typically selected.
* A typographical error in a widely circulated working-paper version (McBride and Nichols 2015) changes PA and BPAC enough to alter qualitative conclusions: under the TP+FP version, PA favoured QRF(0.45) over QRF(0.40), and the published definition reverses this (section IV.5).
* Replications should verify formulas against reported numbers, as we did with the identity PA + UC = 1.

### V.7 Comparison with the published study and the literature

* *Agreement with the published study:*
  * our CV-QR result;
  * our doubled-line results;
  * the published finding that the forest does not outperform CV-QR in Bolivia, which our seed-42 contrasts do not contradict.
* *Disagreement:* the *level* of the QRF result. Our forest performs about as well as CV-QR; the published one performs about as well as the fixed IRIS benchmark.
* *Relation to the wider literature:*
  * Sohnesen and Stender (2017) find random forests often, but not consistently, more accurate than standard poverty-imputation models. Our results add that the size of such gains depends on how validation and tuning are done.
  * Reviews of targeting stress that all mechanisms make errors (Devereux et al. 2017; Brown et al. 2018). Our results show that how those errors are *measured* is itself uncertain.

### V.8 Implications for PMT practice

These are qualified by the single-country scope:
1. Benchmarks should be tuned on the same footing as ML models.
2. Validation should use disjoint households.
3. Tuning should use training data only.
4. Accuracy formulas should be stated and checked against reported numbers.
5. Results should be reported over a band of poverty lines when the line is reconstructed.
6. Constructed data should be released, because welfare-aggregate differences can dominate algorithm differences.

## VI. Limitations

| Limitation | Effect on interpretation |
|---|---|
| **Institutional setting of the metric** | The PAT and its "very poor" line and BPAC criterion stem from a US legislative mandate for USAID microenterprise funds (McBride and Nichols 2018, 533). Conclusions about BPAC need not carry over to programmes with other objectives or accuracy measures. |
| **One country, one survey (EH 2005, collected two decades ago)** | Findings are Bolivia-specific and need not hold for other surveys, poverty rates (the published Malawi rate is far higher) or current data. |
| **Welfare variable differs from the authors' (A8)** | The authors' aggregate is unidentified. All levels describe our construction; direct level comparisons with the published QRF are not valid. |
| **A8 unresolved** | We cannot claim our QRF is better or worse than the published one, and we do not. |
| **Single split for CV-QR vs QRF, plus a three-split pilot** | Test-sample intervals ignore split variation. The pilot is too small for inference and is confounded with overlap inflation. The forest-vs-tuning question (RQ5) is open. |
| **Halved-line comparison is approximate** | Different poverty rates (6.09% vs 4.92%) and very wide intervals. Only qualitative statements are justified. |
| **QRF implementation ambiguities (A9, A10)** | The paper's text and its cited software disagree on leaf storage (effect ≤ 0.007 BPAC). Our minimum-leaf rule is not R's node-size rule (R's rule raises our BPAC by about 0.04). Neither explains A8, but absolute QRF levels depend on these choices. |
| **Python rather than R; no native R run** | R behaviour was emulated from verified source, not executed. |
| **Unknown seed and IRIS training subset** | Exact replication of published point values is not possible. |
| **No survey weights (following the paper); data-derived thresholds** | Results describe the sample, not the population. No external official "very poor" line was available to validate the reconstructed thresholds. |
| **Descriptive multiple comparisons** | Counts across thresholds and splits are not independent tests, and no multiplicity correction is applied. |

## VII. Conclusion

**What we found.** We re-examined a published machine-learning approach to proxy means testing for Bolivia under a frozen, transparent methodology.
* The cross-validated linear quantile regression replicates closely.
* The quantile regression forest does not. Our forest is more accurate than the published one, for reasons that implementation and split variation do not explain. The welfare variable demonstrably differs, so the discrepancy remains unresolved.

**Strongest defensible findings**, all specific to our construction of the Bolivia data:
1. Overlapping train–test validation inflates forest accuracy (about +0.035 BPAC) but not that of the linear benchmark.
2. Test-set quantile selection adds about 0.02 BPAC of optimism.
3. Reconstructed poverty lines between 170 and 210 Bs do not change the ranking of method families.
4. Correcting the metric formula changes benchmark BPAC by 0.025–0.064 and can reverse qualitative conclusions.
5. Much of the forest's advantage over the published benchmark is a quantile-calibration effect. Whether the forest adds accuracy beyond a tuned linear model remains open.

**Methodological contribution.**
* A replication protocol with page-referenced decisions, change control and archived superseded results.
* Algebraic results for the published accuracy metrics: PA = 1 − UC, and BPAC = 1 − LE under over-prediction.
* Documented inconsistencies in the published reporting.

**Practical implications.** Evaluate PMT tools against tuned benchmarks on disjoint data with training-only selection, and report formulas and constructed data.

**Future research:**
1. Obtain the authors' constructed data or code to resolve A8.
2. Repeat the CV-QR vs QRF comparison over enough splits, under both protocols, to settle RQ5.
3. Extend the analysis to a second country, for example Malawi, to test generality.

We do not claim that the forest outperforms the published method or linear quantile regression.

---

**Data and code availability.**
* A replication package accompanies this article **[repository URL / DOI to be inserted]**. It contains all code, the frozen methodology, unit tests, aggregate results, the tables and figures, and SHA-256 checksums of the raw survey files. `run_all.sh` reproduces the frozen pipeline; `run_audits.sh` and the `audit_*` directories reproduce the audits.
* The raw survey files are not redistributed, because we found no open licence permitting redistribution. They can be downloaded from INE Bolivia; the source, file checksums and variable construction are documented in the package. Superseded pre-freeze results are kept in the project's version history.

**Figures:**
* **Figure 1.** BPAC (test-sample point estimate) against the poverty threshold, 170–210 Bs, under the published (overlapping) and disjoint protocols (Bolivia EH 2005, seed 42). Series: OOB-selected QRF, QRF(0.40), IRIS QR(0.42) and RF. Bands: 95% bootstrap intervals (1,000 test-sample draws) for the OOB-selected QRF and IRIS. Dotted vertical lines mark 188.77, 189.09 (primary) and 194.10 Bs.
* **Figure 2.** Quantile path on the disjoint split (Bolivia EH 2005, seed 42, line 189.09 Bs). BPAC, PA, UC and LE against the quantile q, for QRF and linear QR, with 95% test-bootstrap bands for BPAC. Open markers show the quantiles selected on training data. Under the published definitions PA + UC = 1, so the PA and UC panels carry the same information.

**Declarations.**
* *Funding:* [to be completed by the authors].
* *Competing interests:* The authors declare no competing interests. [Confirm.]
* *Acknowledgements:* [to be completed by the authors].

## References

Ahmed, A. U., and H. E. Bouis. 2002. “Weighing What’s Practical: Proxy Means Tests for Targeting Food Subsidies in Egypt.” *Food Policy* 27 (5–6): 519–540.

Aiken, E., S. Bellue, D. Karlan, C. Udry, and J. E. Blumenstock. 2022. “Machine Learning and Phone Data Can Improve Targeting of Humanitarian Aid.” *Nature* 603 (7903): 864–870.

Aiken, E. L., G. Bedoya, J. E. Blumenstock, and A. Coville. 2023. “Program Targeting with Machine Learning and Mobile Phone Data: Evidence from an Anti-Poverty Intervention in Afghanistan.” *Journal of Development Economics* 161: 103016.

Alatas, V., A. Banerjee, R. Hanna, B. A. Olken, and J. Tobias. 2012. “Targeting the Poor: Evidence from a Field Experiment in Indonesia.” *American Economic Review* 102 (4): 1206–1240.

Arlot, S., and A. Celisse. 2010. “A Survey of Cross-Validation Procedures for Model Selection.” *Statistics Surveys* 4: 40–79.

Atkinson, A. B. 1987. “On the Measurement of Poverty.” *Econometrica* 55 (4): 749–764.

Blumenstock, J., G. Cadamuro, and R. On. 2015. “Predicting Poverty and Wealth from Mobile Phone Metadata.” *Science* 350 (6264): 1073–1076.

Breiman, L. 2001. “Random Forests.” *Machine Learning* 45 (1): 5–32.

Brown, C., M. Ravallion, and D. van de Walle. 2018. “A Poor Means Test? Econometric Targeting in Africa.” *Journal of Development Economics* 134: 109–124.

Cawley, G. C., and N. L. C. Talbot. 2010. “On Over-Fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation.” *Journal of Machine Learning Research* 11: 2079–2107.

Christensen, G., and E. Miguel. 2018. “Transparency, Reproducibility, and the Credibility of Economics Research.” *Journal of Economic Literature* 56 (3): 920–980.

Clemens, M. A. 2017. “The Meaning of Failed Replications: A Review and Proposal.” *Journal of Economic Surveys* 31 (1): 326–342.

Coady, D., M. Grosh, and J. Hoddinott. 2004. *Targeting of Transfers in Developing Countries: Review of Lessons and Experience*. Washington, DC: The World Bank.

Devereux, S., E. Masset, R. Sabates-Wheeler, M. Samson, A.-M. Rivas, and D. te Lintelo. 2017. “The Targeting Effectiveness of Social Transfers.” *Journal of Development Effectiveness* 9 (2): 162–211.

Efron, B., and R. J. Tibshirani. 1993. *An Introduction to the Bootstrap*. Boston, MA: Springer US.

Filmer, D., and L. H. Pritchett. 2001. “Estimating Wealth Effects without Expenditure Data—or Tears: An Application to Educational Enrollments in States of India.” *Demography* 38 (1): 115–132.

Grosh, M. E., and J. L. Baker. 1995. “Proxy Means Tests for Targeting Social Programs: Simulations and Speculation.” LSMS Working Paper No. 118. The World Bank, Washington, DC.

Hand, D. J. 2006. “Classifier Technology and the Illusion of Progress.” *Statistical Science* 21 (1): 1–14.

Hanna, R., and B. A. Olken. 2018. “Universal Basic Incomes versus Targeted Transfers: Anti-Poverty Programs in Developing Countries.” *Journal of Economic Perspectives* 32 (4): 201–226.

Hyndman, R. J., and Y. Fan. 1996. “Sample Quantiles in Statistical Packages.” *The American Statistician* 50 (4): 361–365.

Instituto Nacional de Estadística. 2005. *Encuesta de Hogares 2005 (EH 2005)*. Data set. La Paz: INE Bolivia. Accessed November 3, 2026. https://siip.produccion.gob.bo/repSIIP2/files/encuesta_hogares/EH2005.rar.

IRIS Center. 2005. “Note on Assessment and Improvement of Tool Accuracy. Poverty Assessment Tools.” USAID.

Janitza, S., and R. Hornung. 2018. “On the Overestimation of Random Forest’s Out-of-Bag Error.” *PLOS ONE* 13 (8): e0201904.

Jean, N., M. Burke, M. Xie, W. M. Davis, D. B. Lobell, and S. Ermon. 2016. “Combining Satellite Imagery and Machine Learning to Predict Poverty.” *Science* 353 (6301): 790–794.

Johnson, R. A. 2024. “quantile-forest: A Python Package for Quantile Regression Forests.” *Journal of Open Source Software* 9 (93): 5976.

Kapoor, S., and A. Narayanan. 2023. “Leakage and the Reproducibility Crisis in Machine-Learning-Based Science.” *Patterns* 4 (9): 100804.

Kaufman, S., S. Rosset, C. Perlich, and O. Stitelman. 2012. “Leakage in Data Mining: Formulation, Detection, and Avoidance.” *ACM Transactions on Knowledge Discovery from Data* 6 (4): 1–21.

Klasen, S., and S. Lange. 2015. “Accuracy and Poverty Impacts of Proxy Means-Tested Transfers: An Empirical Assessment for Bolivia.” Courant Research Centre: Poverty, Equity and Growth Discussion Paper No. 164. University of Göttingen. http://www2.vwl.wiso.uni-goettingen.de/courant-papers/CRC-PEG_DP_164.pdf.

Koenker, R. 2005. *Quantile Regression*. Cambridge: Cambridge University Press.

Koenker, R., and G. Bassett. 1978. “Regression Quantiles.” *Econometrica* 46 (1): 33–50.

Liaw, A., and M. Wiener. 2002. “Classification and Regression by randomForest.” *R News* 2 (3): 18–22.

Lin, Y., and Y. Jeon. 2006. “Random Forests and Adaptive Nearest Neighbors.” *Journal of the American Statistical Association* 101 (474): 578–590.

McBride, L., and A. Nichols. 2015. “Improved Poverty Targeting through Machine Learning: An Application to the USAID Poverty Assessment Tools.” Working Paper. http://www.econthatmatters.com/wp-content/uploads/2015/01/improvedtargeting_21jan2015.pdf.

——. 2018. “Retooling Poverty Targeting Using Out-of-Sample Validation and Machine Learning.” *The World Bank Economic Review* 32 (3): 531–550.

Meinshausen, N. 2006. “Quantile Regression Forests.” *Journal of Machine Learning Research* 7: 983–999.

——. 2016. *quantregForest: Quantile Regression Forests*. R package version 1.3-5. Available at http://CRAN.R-project.org/package=quantregForest.

Mullainathan, S., and J. Spiess. 2017. “Machine Learning: An Applied Econometric Approach.” *Journal of Economic Perspectives* 31 (2): 87–106.

Nadeau, C., and Y. Bengio. 2003. “Inference for the Generalization Error.” *Machine Learning* 52 (3): 239–281.

Noriega-Campero, A., B. Garcia-Bulle, L. F. Cantu, M. A. Bakker, L. Tejerina, and A. Pentland. 2020. “Algorithmic Targeting of Social Policies: Fairness, Accuracy, and Distributed Governance.” In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*, 241–251. New York: ACM.

Pedregosa, F., G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and É. Duchesnay. 2011. “Scikit-learn: Machine Learning in Python.” *Journal of Machine Learning Research* 12: 2825–2830.

Poulin, C., J. Trimmer, J. Press-Williams, B. Yachori, R. Khush, R. Peletz, and C. Delaire. 2022. “Performance of a Novel Machine Learning-Based Proxy Means Test in Comparison to Other Methods for Targeting Pro-Poor Water Subsidies in Ghana.” *Development Engineering* 7: 100098.

Ravallion, M., and B. Bidani. 1994. “How Robust Is a Poverty Profile?” *The World Bank Economic Review* 8 (1): 75–102.

Schreiner, M. 2006. “A Simple Poverty Scorecard for Bangladesh, Report to Grameen Foundation USA.” Working Paper. Saint Louis, MO: Microfinance Risk Management, L.L.C.

Sohnesen, T. P., and N. Stender. 2017. “Is Random Forest a Superior Methodology for Predicting Poverty? An Empirical Assessment.” *Poverty & Public Policy* 9 (1): 118–133.

Varian, H. R. 2014. “Big Data: New Tricks for Econometrics.” *Journal of Economic Perspectives* 28 (2): 3–28.

Varma, S., and R. Simon. 2006. “Bias in Error Estimation When Using Cross-Validation for Model Selection.” *BMC Bioinformatics* 7: 91.

Wobcke, W., and S. Mariyah. 2023. “Machine Learning and Data Augmentation in the Proxy Means Test for Poverty Targeting.” *Statistical Journal of the IAOS* 39 (4): 961–977.
