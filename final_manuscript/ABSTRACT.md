# Validation Design, Quantile Tuning, and Threshold Reconstruction in Machine-Learning Proxy Means Tests: An Adapted Replication for Bolivia

## Abstract

**Background.** Proxy means tests (PMTs) predict household welfare from easily verified characteristics in order to target transfers. McBride and Nichols (2018) report that cross-validation and quantile regression forests (QRF) can improve the out-of-sample accuracy of the USAID Poverty Assessment Tools.

**Research problem.** Reported gains depend on evaluation choices that published studies specify only partly: the accuracy formula, the train–test protocol, how the targeting quantile is selected, and the poverty line. We ask how sensitive machine-learning targeting results are to reconstructed poverty thresholds and alternative validation procedures.

**Data and methods.**
* We re-analyse the Bolivia Encuesta de Hogares 2005 (N = 4,086 households) using a methodology frozen against the published article.
* The models are the IRIS quantile-regression benchmark, a cross-validated linear quantile regression (CV-QR), and a stochastic-ensemble QRF selected on out-of-bag accuracy.
* Results are compared under the published overlapping bootstrap split and under a disjoint split, with training-only model selection, several reconstructed poverty lines, and the published and earlier metric definitions.

**Results.**
* **What replicates:** the published CV-QR result (selected quantile 0.37 vs 0.38 published; BPAC 0.623 vs 0.579).
* **What does not:** the published QRF result. Our QRF scores higher (BPAC 0.653 vs 0.502). An implementation audit, including an emulation of the original R procedure, rules out software differences and split variation. Model-free diagnostics show that our welfare variable differs from the authors'.
* **Validation design:** the overlapping split raises QRF accuracy by about 0.035 BPAC and leaves the linear benchmark essentially unchanged.
* **Quantile selection:** choosing the quantile on test data adds about 0.022–0.024 BPAC.
* **Thresholds:** reconstructed poverty lines barely change mean accuracy over 30 splits, and in a single-split scan from 170 to 210 Bs they do not change the ranking of method families.
* **Metric definition:** using the 2015 working-paper formula shifts the benchmark's BPAC by 0.025–0.064.
* **Forest vs tuning:** on single-split evidence, most of the QRF advantage over the fixed-quantile benchmark reflects the choice of quantile. Against a quantile-tuned linear model the difference is small and unsettled; a three-split pilot leans towards the forest under the overlapping protocol.

**Contribution.** A transparent, reproducible adapted replication, plus evidence that the evaluation choices themselves move results by amounts comparable to the reported machine-learning gains.

**Limitations.**
* One country and survey.
* An unidentified difference in the welfare aggregate (unresolved discrepancy A8).
* The QRF-versus-CV-QR comparison rests on one split per protocol plus a three-split pilot.

*Identical to the abstract in `MANUSCRIPT.md`. Every number is traceable via `CLAIM_EVIDENCE_TABLE.md`.*
