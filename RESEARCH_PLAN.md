# Step 5: From adapted replication to research contribution

## Research question

> **How sensitive are machine-learning poverty-targeting models to reconstructed poverty thresholds and alternative validation procedures?**

### Sub-questions, with the evidence so far

Bolivia EH 2005, under the frozen methodology; see `RESULTS.md`. Numbers were updated on 2026-11-03 after the freeze.

| # | Sub-question | Current answer |
|---|---|---|
| RQ1 | **Validation procedure:** How much does the published overlapping N/2 split inflate performance compared with an untouched test set? | It depends on model flexibility. SE gains +0.035 BPAC from the overlap and IRIS gains about 0. The old `min_samples_leaf=1` QRF gained about +0.20. |
| RQ2 | **Quantile selection:** Is the targeting quantile stable, and how optimistic is choosing it on the test set? | Moderately stable: OOB selection picks q = 0.36–0.43 (mode 0.39–0.40; published 0.41). Test-set selection is optimistic by +0.022 to +0.024 BPAC. QRF(0.40) vs QRF(0.45) differs by about 0.14–0.15 BPAC. |
| RQ3 | **Threshold reconstruction:** Do plausible reconstructions of an unpublished threshold change the conclusions? | 188.77 Bs (P24.03), 189.05 Bs and 189.09 Bs: no (mean change ≤ 0.010). 194.10 Bs: SE/QRF +0.01, IRIS +0.02, RF +0.04. Rankings are unchanged. |
| RQ4 | **Metric dependence:** Does the metric definition change the conclusions? | Yes. The 2015 typo (TP+FP) moves IRIS BPAC by 0.025–0.064, and with it the size of the QRF − IRIS gap. Under the published definition, PA = 1 − UC, so PA and UC carry the same information. |
| RQ5 | **Is the ML gain a forest effect or a quantile-tuning effect?** (new, from Phase 2) | On our data, mostly **quantile tuning**. The published CV linear QR replicates (QR(0.37) vs 0.38). It is indistinguishable from the SE QRF (disjoint BPAC −0.004 [−0.053, +0.056]). Single split only. |
| (open) | **Replication gap A8** | Narrowed, not resolved; see "Confirmed findings" below. |

### Contribution
1. **Methodological:** a reproducible protocol for checking how ML poverty-targeting results depend on threshold, split and quantile. It uses paired bootstrap, repeated splits, train-only selection and train-only thresholds.
2. **Empirical:** BPAC differences reported in the literature can be smaller than the variation caused by the validation protocol itself. Model rankings stay fixed, but metric levels do not.
3. **Practical:** guidance for PAT-style tools. Pick the quantile on training data only (OOB or CV), report results on a disjoint test set, and report a threshold band rather than a single point.

## Confirmed findings and remaining uncertainties (A8 audit and Phases 2–3, 2026-11-04)

Details: `results/a8_audit/A8_AUDIT.md` and `results/cv_qr/PHASE2_3_RESULTS.md`. The frozen methodology and its results are unchanged.

**Confirmed (direct evidence):**
1. **Implementation is not the cause of A8.**
   * One factor at a time (20 splits each), none of these moves our SE QRF by more than 0.013 BPAC: one value per leaf, the exact R `quantregForest` 1.3-5 procedure and OOB, OOB de-duplication, one-hot regions, a log target, and P24.03.
   * R's exact node-size rule *raises* BPAC by about +0.04, widening the gap.
2. **Split variation is not the cause.** The published SE value lies 3–10 split-SDs below ours under every configuration.
3. **The authors' welfare variable differs from ours.**
   * This is model-free evidence: at half and double the line they report 4.92% and 62.26%; `G_TOTAL_pc` gives 6.07% and 57.00%.
   * None of the 9 aggregates available in EH 2005 matches.
4. **The authors' feature or target construction gives a weaker linear model in-sample.** In the deterministic refit of row 5, PA and UC match, LE is 24.95 vs 33.71, and TA is 84.65 vs 82.45.
5. **The published poverty rate used in the computations is 24.03%** (implied by row 5: 24.038%). The effect on our results is ≤ 0.002 BPAC. The frozen 24.2% is unchanged, pending your decision.
6. **The published CV baseline replicates** on our data: CV QR(0.37), with PA, UC, LE and BPAC inside the published CIs.
7. **On our data, SE QRF ≈ CV linear QR.** The large QRF − IRIS margins in `RESULTS.md` are against a *fixed*, untuned IRIS quantile (0.42).
8. **Table A2, doubled line:** BPAC levels match the published ones (0.81–0.84) and all methods perform about the same, as the paper reports.

**Remaining uncertainties:**
* **A8 core (untested hypothesis):** the authors' welfare aggregate and feature construction may hurt the forest more than the linear model. That would explain why their SE trails their CV by 7.76 BPAC while ours ties. Testing it needs the authors' data or code.
* **CV vs SE across repeated splits:** not run, because CV takes about 40 minutes per split. The equivalence rests on one split per protocol.
* **Table A2, halved line:**
  * About 6% of households are poor, and the CIs span about 0.3 BPAC.
  * Our linear models choose QR(0.51), while the paper chose 0.22–0.24. This is not explained.
  * The rates differ from the published ones (6.09% vs 4.92%), so comparisons are approximate.
* **A9 and A10 (methodology reference):** the paper text and its software disagree on QRF leaf storage, and our `min_samples_leaf=5` is not R's exact node rule. Both are recorded, the frozen pipeline is unchanged, and the decision is yours.

**What can be claimed now:**

> "On our construction of the Bolivia EH 2005 data, tuning the quantile on training data (by cross-validation or out-of-bag) drives the gains in targeting accuracy. The QRF and a cross-validated linear quantile regression are statistically indistinguishable."

**What cannot be claimed:** that our QRF outperforms the published QRF, or that QRF beats linear models.

## Next steps
Following the original plan, **no XGBoost, SHAP or new models** until these steps are done:
1. **Threshold band:** scan the threshold continuously over ±10% of 189 Bs (about 170–210 Bs) and plot BPAC against it for each model.
2. **Quantile path:** plot BPAC, PA, UC and LE against q (0.30–0.50) on the disjoint split.
3. **External threshold:** if an official INE/UDAPE extreme-poverty line for 2005 can be sourced with a citation, add it as a truly external threshold.
4. **Second country:** test whether the findings generalise to Timor-Leste or Malawi (requires World Bank microdata registration).
5. **A8 resolution:** request the constructed data set or code from the authors. Without it, the welfare-aggregate hypothesis cannot be tested. The ablations already run (regions encoding, log target, R emulation) did not close the gap.
6. **Survey weights:** EH 2005 has expansion factors (`factor`) that the paper ignores. Test weighted vs unweighted metrics.
7. **CV vs SE robustness:** repeat the CV baseline over about 10 repeated splits, at about 40 minutes each, to test whether SE ≈ CV holds beyond a single split.


---

## Final status update (2026-11-04)

This section was added at the end; the content above is preserved unchanged.

**Experiment expansion has stopped.** No second country, no new models, no further repeated CV splits, and no weighted analyses until you approve them.

**Final documents:**
* `FINAL_RESEARCH_ASSESSMENT.md`: confirmed findings, hypotheses, limitations, and the second-country recommendation;
* `MANUSCRIPT_OUTLINE.md`;
* `STEP5_SENSITIVITY_RESULTS.md`.

**Step 5 (threshold scan and quantile path) is done:**
* The method ranking (QRF > fixed IRIS > RF/DT) is unchanged across 170–210 Bs.
* Under the published overlapping split, the OOB-selected QRF falls below IRIS at 13 low thresholds.
* Each method peaks at a different quantile. At their training-selected quantiles, QRF and linear QR differ by only +0.013 BPAC on the disjoint split.
* PA = 1 − UC (redundant).

**The 3-split pilot leans towards QRF over CV-QR under the overlapping protocol, but it is not conclusive.** QRF vs CV-QR remains open, and A8 remains unresolved.

**Next practical step:** write the manuscript draft from `MANUSCRIPT_OUTLINE.md`, and request the authors' constructed data or code for A8.
