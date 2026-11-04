# Results: Bolivia EH 2005, under the frozen methodology

**Methodology:** `METHODOLOGY_REFERENCE.md`, frozen 2026-11-03 against McBride & Nichols (2018), *WBER* 32(3):531–550.
**Metrics:** published Table 2 (p. 534). PA, UC, LE and BPAC all use the denominator **TP+FN**.
**Pre-freeze results:** `archive/2026-11-03_pre_methodology_freeze/`. They used TP+FP for PA and BPAC; **do not cite them.**

**Conventions:**
* Threshold 189.09 Bs unless stated otherwise.
* **Primary** = seed 42, mean of 1000 test-sample bootstrap resamples, with [95% percentile CI] and SE.
* **Repeated** = 30 random splits per protocol, reported as mean (SD) of point estimates.
* **Paper** protocol = the published split: two N/2 draws with replacement (S1).
* **Disjoint** protocol = our untouched 50/50 test set (adaptation).
* **SE** = the stochastic-ensemble model chosen by OOB BPAC on the training sample (S7).

## 0. Impact of the freeze corrections (`results/audit/correction_impact.csv`)

Same split and same bootstrap indices, corrections applied cumulatively. Values are BPAC (PA in brackets).

| Protocol | Model | Pre-freeze | +C1 metrics | +C2 all-leaf QRF | +C3 OOB selection |
|---|---|---|---|---|---|
| paper | IRIS QR(0.42) | 0.611 (0.662) | **0.586** (0.633) | 0.586 | 0.586 |
| paper | QRF(0.40) fixed | 0.665 (0.695) | 0.674 (0.705) | 0.667 (0.712) | 0.667 |
| paper | Selected model | QRF(0.45): 0.627 | QRF(0.40): 0.674 | QRF(0.40): 0.667 | **QRF(0.43): 0.653** |
| disjoint | IRIS QR(0.42) | 0.574 (0.704) | **0.510** (0.624) | 0.510 | 0.510 |
| disjoint | QRF(0.40) fixed | 0.622 (0.652) | 0.625 (0.655) | 0.630 (0.666) | 0.630 |
| disjoint | Selected model | QRF(0.40): 0.622 | QRF(0.40): 0.625 | QRF(0.40): 0.630 | **QRF(0.40): 0.630** |

* **C1 (metric definition) is the correction that matters.** It lowers IRIS BPAC by 0.025 (paper) to 0.064 (disjoint), and changes PA for every model. UC, LE and TA are untouched.
* **C2 (all-leaf QRF)** moves the QRF results by less than 0.01.
* **C3 (OOB selection on a 0.01 grid)** changes the selected quantile from 0.40 to 0.43 on the seed-42 paper split, and leaves the disjoint split unchanged.

## 1. Replication against published Table A1 (paper protocol, seed 42)

| Model | TA | PA | UC | LE | BPAC [95% CI] | Published (Table A1) |
|---|---|---|---|---|---|---|
| IRIS QR(0.42) | 0.840 | 0.633 | 0.367 | 0.324 | 0.586 [0.486, 0.657] | row 2: PA 57.58, BPAC 49.33 [36.73, 60.48] |
| SE, chosen by OOB: QRF(0.43) | 0.861 | 0.688 | 0.312 | 0.289 | 0.653 [0.558, 0.713] | row 9, SE QRF(0.41): PA 55.33, BPAC 50.18 [39.26, 58.57] |
| QRF(0.41) fixed | 0.859 | 0.707 | 0.293 | 0.314 | 0.673 [0.614, 0.722] | (same row 9) |
| RF (conditional mean) | 0.854 | 0.481 | 0.519 | 0.112 | 0.074 [−0.028, 0.172] | — |
| Decision Tree (not in paper) | 0.834 | 0.488 | 0.512 | 0.203 | 0.178 | — |

* **IRIS benchmark:** our BPAC 0.586 lies inside the published 95% CI. Our PA 0.633 is just above its upper bound (0.6265).
* **Open discrepancy (not resolved).** Our QRF does much better than the published SE QRF. Our BPAC is 0.65–0.67, above the published CI upper bound of 0.586.
  * The published paper finds **SE ≈ IRIS** for Bolivia: +0.85 points, not significant (Table 4, p. 542).
  * We find SE − IRIS = **+0.196** (paper protocol) and **+0.162** (disjoint protocol), with SE ahead in 30/30 repeated splits under both protocols.
  * Candidate causes, none tested: R vs Python implementation, `nodesize` vs `min_samples_leaf` (A3), the seed or split, feature coding (D3–D5), and per-row OOB leakage (A4, which affects selection only).
  * This must be stated as a discrepancy, not as a finding.
* **Selected quantile:** across 30 paper-protocol splits, the SE rule chooses QRF(0.36)–QRF(0.43), most often 0.39 and 0.40. The published 0.41 lies within this range. RF was never selected.

## 2. QRF(0.40) vs QRF(0.45): controlled comparison (Step 2)

Same fitted forest, same split, same bootstrap indices. Neither quantile was chosen by looking at the test set.

| Protocol | Model | PA | UC | LE | BPAC |
|---|---|---|---|---|---|
| disjoint, primary | QRF(0.40) | 0.666 | 0.334 | 0.359 | 0.630 [0.571, 0.677] |
| disjoint, primary | QRF(0.45) | 0.611 | 0.389 | 0.283 | 0.505 [0.403, 0.604] |
| disjoint, 30 splits | QRF(0.40) | 0.674 (.024) | 0.326 | 0.333 | 0.638 (.035) |
| disjoint, 30 splits | QRF(0.45) | 0.615 (.021) | 0.385 | 0.260 | 0.489 (.060) |

Paired differences QRF(0.40) − QRF(0.45) over 30 disjoint splits:
* BPAC **+0.148**, positive in 29 of 30 splits.
* PA **+0.060** (30 of 30) and UC **−0.060**, because PA = 1 − UC under the published definition.
* LE **+0.074**.

The paper protocol gives the same pattern: BPAC +0.139, 29 of 30.

> **Change from the pre-freeze conclusion.** Earlier we wrote that "PA favours QRF(45)". That came from the TP+FP definition. Under the published definition, PA = 1 − UC, so QRF(0.40) is better on PA, UC and BPAC, and worse only on LE.

## 3. Quantile-selection optimism

* **Test-set selection vs OOB selection (SE):** BPAC +0.024 (paper) and +0.022 (disjoint). The test-selected quantile wins in about 70% of splits. With the finer 0.01 grid the optimism is larger than the pre-freeze figure of 0.005–0.007.
* **SE rule vs fixed QRF(0.40):** 0.679 vs 0.673 (paper) and 0.644 vs 0.638 (disjoint), about +0.006.

## 4. Threshold sensitivity (Step 3)

Change in BPAC relative to 189.09 Bs, mean (SD) over 30 splits:

| Model | 188.77 (P24.03) | 189.05 | 194.10 | Training-sample P24.2 |
|---|---|---|---|---|
| **Disjoint protocol** | | | | |
| SE (OOB) | −0.003 (.005) | +0.001 (.004) | +0.008 (.017) | −0.001 (.022) |
| QRF(0.40) | −0.003 (.005) | +0.001 (.002) | +0.010 (.017) | +0.006 (.021) |
| IRIS QR(0.42) | +0.004 (.004) | +0.001 (.002) | +0.021 (.015) | +0.011 (.017) |
| RF | −0.000 (.004) | −0.000 (.002) | **+0.040** (.016) | +0.022 (.040) |
| **Paper protocol** | | | | |
| SE (OOB) | −0.002 (.012) | +0.001 (.005) | +0.007 (.018) | −0.002 (.030) |
| IRIS QR(0.42) | +0.005 (.006) | +0.001 (.003) | +0.020 (.020) | +0.006 (.020) |
| RF | +0.000 (.006) | +0.001 (.002) | **+0.041** (.020) | +0.003 (.051) |

* **188.77 Bs** (the published Table 3 rate of 24.03%, ambiguity A2) and **189.05 Bs** have negligible effects on average: |mean| ≤ 0.010.
  * In individual splits the largest changes are 0.080 and 0.021 BPAC. These occur where few households sit near the line, and BPAC is not smooth.
* **194.10 Bs:**
  * SE and QRF(0.40) change by only +0.006 to +0.010.
  * IRIS changes by about +0.02, and RF by about +0.04.
  * Model rankings do not change.
* **Training-sample threshold:** it varies from about 179 to 201 Bs across splits. Its mean effect on SE/QRF BPAC is ≤ 0.006.

## 5. Validation protocol (overlap)

Moving from the paper protocol to the disjoint protocol (30-split means):
* SE BPAC: 0.679 → 0.644 (−0.035)
* QRF(0.40): 0.673 → 0.638
* IRIS: 0.483 → 0.481, practically unchanged

The overlapping split mainly flatters the flexible models.

## 6. Unchanged from before the freeze
* Household construction checked against the codebook: `results/audit/data_construction_audit.txt`.
* IRIS dummy coding (9 vs 8 dummies) gives identical predictions.
* `config_audit.py` still shows that the old "QRF(45), BPAC 0.797" was an artefact of `min_samples_leaf=1` plus the overlapping split. It now reports values under the frozen metrics.
