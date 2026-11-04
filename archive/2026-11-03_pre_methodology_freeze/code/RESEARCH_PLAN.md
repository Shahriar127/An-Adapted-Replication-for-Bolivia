# Step 5: From adapted replication to research contribution

## Research question

> **How sensitive are machine-learning poverty-targeting models to reconstructed poverty thresholds and alternative validation procedures?**

### Sub-questions, with the evidence so far (Bolivia EH 2005; see `RESULTS.md`)

| # | Sub-question | Current answer |
|---|---|---|
| RQ1 | **Validation procedure:** How much does the paper's overlapping N/2 bootstrap split inflate performance compared with an untouched test set? | It depends on model flexibility. QRF(40) gains +0.03 BPAC from the overlap; a QRF with `min_samples_leaf=1` gains +0.20. |
| RQ2 | **Quantile selection:** Is the targeting quantile stable, and how optimistic is choosing it on the test set? | Stable: CV picks q = 0.40 in 30 of 30 splits. Test-set selection is optimistic by less than 0.01 BPAC. Fixing the quantile at 0.40 vs 0.45 moves BPAC by about 0.10 and trades UC against LE. |
| RQ3 | **Threshold reconstruction:** Do plausible reconstructions of an unpublished threshold change the conclusions? | 189.05 vs 189.09 Bs: no. 194.10 Bs: QRF does not shift, while RF/DT shift by 0.05–0.08 BPAC; rankings are unchanged. The threshold's sampling SD (≈ 5 Bs) is as large as the reconstruction gap. |
| RQ4 | **Metric dependence:** Do PA and BPAC rank models the same way? | No. PA favours RF and QRF(45); BPAC favours QRF(40). |

### Contribution
1. **Methodological:** a reproducible protocol for checking how ML poverty-targeting results depend on threshold, split and quantile. It uses paired bootstrap, repeated splits, train-only selection and train-only thresholds.
2. **Empirical:** BPAC differences reported in the literature can be smaller than the variation caused by the validation protocol itself. Model rankings stay fixed, but metric levels do not.
3. **Practical:** guidance for PAT-style tools. Pick the quantile by CV, report results on a disjoint test set, and report a threshold band rather than a single point.

## Next steps
Following the original plan, **no XGBoost, SHAP or new models** until these steps are done:
1. **Threshold band:** scan the threshold continuously over ±10% of 189 Bs (about 170–210 Bs) and plot BPAC against it for each model.
2. **Quantile path:** plot BPAC, PA, UC and LE against q (0.30–0.50) on the disjoint split.
3. **External threshold:** if an official INE/UDAPE extreme-poverty line for 2005 can be sourced with a citation, add it as a truly external threshold.
4. **Second country:** test whether the findings generalise to Timor-Leste or Malawi (requires World Bank microdata registration).
5. **Feature construction ablation:** to explain the IRIS PA gap, swap `regions` between ordinal and dummies, and swap the binary and count variants.
6. **Survey weights:** EH 2005 has expansion factors (`factor`) that the paper ignores. Test weighted vs unweighted metrics.
