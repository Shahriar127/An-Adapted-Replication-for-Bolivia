# Validation Design, Quantile Tuning, and Threshold Reconstruction in Machine-Learning Proxy Means Tests: An Adapted Replication for Bolivia

## Abstract

Proxy means tests (PMTs) predict household welfare from easily verified characteristics in order to target transfers. McBride and Nichols (2018) reported that cross-validation and quantile regression forests (QRF) improve the out-of-sample accuracy of the USAID Poverty Assessment Tools. We re-analyse their Bolivia data (Encuesta de Hogares 2005, N = 4,086) under a methodology frozen against the article. We compare the IRIS quantile-regression benchmark, a cross-validated linear quantile regression (CV-QR) and an out-of-bag-selected QRF under overlapping and disjoint validation splits, reconstructed poverty lines and two metric definitions. The CV-QR result replicates (selected quantile 0.37 vs 0.38; BPAC 0.623 vs 0.579). The published QRF result does not (0.653 vs 0.502): an implementation audit rules out software and split variation, and model-free diagnostics show that our welfare variable differs from the authors'. The overlapping split raises QRF accuracy by about 0.035 BPAC and leaves the linear benchmark essentially unchanged. Test-set quantile selection adds 0.022–0.024. The working-paper metric formula shifts the benchmark's BPAC by 0.025–0.064. Reconstructed poverty lines barely change accuracy and do not change method rankings. On single-split evidence, much of the QRF advantage over the fixed-quantile benchmark reflects the choice of quantile; against a tuned linear model the difference is small and unsettled. Evaluation choices move PMT accuracy by amounts comparable to the reported machine-learning gains. Benchmarks should be tuned on the same footing as machine-learning models, validated on disjoint data, and reported with explicit formulas and constructed data.

**JEL classification:** I32, I38, C52, C53

**Key words:** proxy means test, poverty targeting, machine learning, quantile regression forest, replication, out-of-sample validation, Bolivia

*Identical to the abstract in `MANUSCRIPT.md`.*
