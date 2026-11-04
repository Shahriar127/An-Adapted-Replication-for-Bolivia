# A8 audit: why does our QRF outperform the published SE QRF?

**Scope:** Phase 1 of the A8 investigation. The frozen methodology (`common.py`, `METHODOLOGY_REFERENCE.md`) and every existing result were left unchanged. All outputs are in `results/a8_audit/`.

**Scripts:**
* `a8_qrf_audit.py`: controlled forest experiments, one factor at a time.
* `a8_data_diagnostics.py`: deterministic checks of the data construction.

**Published target** (Table A1 row 9, p. 545), SE QRF(0.41), bootstrap means: TA 80.17, PA 55.33, UC 44.67, LE 40.44, **BPAC 50.18** [39.26, 58.57].

**Our frozen result** (paper protocol): seed 42, SE QRF(0.43), BPAC 0.653. Over 20 further splits: SE BPAC 0.685 (SD 0.025), which is **7.2 split-SDs above** the published value.

## 1. Inventory of differences between the published procedure and ours

| # | Component | Published / R | Ours (frozen) | How checked | Result |
|---|---|---|---|---|---|
| I1 | Software | R `randomForest` 4.x and `quantregForest` 1.3-5 | Python `scikit-learn` 1.8.0 and `quantile-forest` 1.4.2 | E1–E4: emulation of R 1.3-5 from its verbatim source | Not a cause (see I2–I5) |
| I2 | Leaf contents | **One** response per leaf per tree, drawn at random from **all n** training rows (`quantregForest.R` 1.3-5) | All in-bag observations, weighted (`max_samples_leaf=None`) | E1 (one in-bag value per leaf), E3 (exact R procedure) | ΔBPAC −0.004 to +0.004 (SE). **Not a cause.** |
| I3 | Quantile computation | `quantile()` type 7 over the ntree per-tree values, unweighted | Weighted quantile over leaf observations, linear interpolation | E3 | Included in E3: ΔBPAC −0.004. **Not a cause.** |
| I4 | Tree size rule | `nodesize=5`: a child with ≤ 5 rows becomes terminal, and children can be smaller than 5 (`regTree.c`) | `min_samples_leaf=5` (every leaf ≥ 5) | E2: `min_samples_split=6, min_samples_leaf=1`, exactly R's rule | ΔBPAC **+0.038** (SE), +0.044 to +0.059 (fixed q). This **widens** the gap. |
| I5 | Out-of-bag (OOB) prediction | Trees where the row is OOB; the stored leaf value can be the row's own y (leak); `minoob` subsample | Weighted OOB over in-bag leaf observations | E3 (R OOB), E5 (duplicates merged) | ΔBPAC −0.004 / −0.003. **Not a cause.** |
| I6 | mtry, ntree, bootstrap size | 7, 500, n with replacement | 7, 500, n with replacement | Checked against the source | Identical |
| I7 | Quantile selection | "Lowest BPAC error in the OOB sample" | Highest OOB BPAC on a 0.01 grid | Same rule. SE choices across splits: 0.36–0.43; published 0.41 | Not a cause. Fixed QRF(0.41) shows the same gap (4.0 SDs). |
| I8 | Encoding of `regions` | Unknown; an R factor would allow categorical splits | Ordinal 1–9 | E6: 9 binary columns | ΔBPAC +0.002 (SE). **Not a cause.** |
| I9 | Target transform | Unknown | Level | E7: log(1+y) | ΔBPAC −0.002. **Not a cause** for the forest. |
| I10 | Poverty rate | **24.03%**. Table 3, plus the rate implied by row 5 via TA = 1 − p(UC+LE): **24.038%** | 24.2% (frozen) | E8: P24.03 | ΔBPAC −0.002. Not a cause. The published rate is **confirmed numerically**; see §3. |
| I11 | Split seed | Unpublished; single split | Seed 42 plus 20 extra seeds | Distribution of splits | The published value is 3–10 SDs below ours under every configuration. **Not explained by split variation.** |
| I12 | **Welfare aggregate (target)** | "Publicly available" income/expenditure aggregate; variable not named | `G_TOTAL_pc` | Model-free distribution fingerprint and deterministic in-sample refit (§2) | **Confirmed to differ.** No available aggregate matches. |
| I13 | Feature construction | Names only (Table 3) | Codebook mapping (D3–D5) | Row-5 refit under encoding variants | **Confirmed residual difference**; the cause is not identified. |
| I14 | Train/test duplicates in evaluation | Same protocol | Same protocol | — | Identical |

## 2. Data-construction evidence (deterministic, no split)

**(a) Distribution fingerprint.** Poverty rates at half and double the line depend only on the welfare variable:

| | At line/2 | At 2 × line |
|---|---|---|
| Published (Table A2) | **4.92%** | **62.26%** |
| `G_TOTAL_pc` (ours) | 6.07% | 57.00% |
| Best available aggregate (`G_ALIMENTOS_pc`) | 5.82% | 62.90% |
| Income `y_percapB` | 14.37% | 42.02% |

Our welfare variable has more mass far below the line and less mass between the line and twice the line. **The authors' welfare variable is not `G_TOTAL_pc`, and none of the 9 aggregates in the file reproduces it.**

**(b) In-sample refit of published row 5:** QR(0.42) on the full sample, in-sample, so no randomness is involved.

| | TA | PA | UC | LE | BPAC |
|---|---|---|---|---|---|
| Published row 5 | 82.45 | 60.69 | 39.30 | 33.71 | 55.10 |
| Ours, frozen design, P24.03 | 84.65 | 61.10 | 38.90 | **24.95** | 47.15 |
| Best of 21 pre-specified variants | 84.14 | 61.00 | 39.00 | 26.99 | 48.98 |

* PA and UC agree to within 0.5 points.
* Leakage does not: their linear model flags about 2 percentage points more of the population as poor, at the same true-positive rate.
* Their model has lower total accuracy (82.45 vs 84.65) on the same 21 variable names.

## 3. Confirmed vs hypothesised

**Confirmed (direct evidence):**
1. The forest implementation (I1–I9) does **not** explain A8. Emulating R `quantregForest` 1.3-5 exactly, together with R's node-size rule (E4), raises our QRF to BPAC 0.725–0.741, moving it further from the published 0.502.
2. Split and seed variation does **not** explain A8: the gap is 3–10 split-SDs under every configuration.
3. The authors' welfare distribution **differs** from ours (§2a).
4. Their feature/target construction gives a **less accurate linear model** on the same variable names (§2b).
5. The published poverty rate used in the computations is 24.03%, not 24.2% (I10). The effect on our results is ≤ 0.002 BPAC.

**Hypothesis (not testable with the data we have):**
* The published QRF performs worse **because** of the different welfare aggregate and feature construction (I12, I13), not because of the method.
  * For: the same construction difference makes their *linear* model weaker in-sample (§2b).
  * Against: it would have to hurt the forest much more than the linear model, since our IRIS benchmark lands inside the published CI.
  * Testing it needs the authors' constructed data set or code.

**Not established:** that our QRF is better than the published one. The two results come from **different welfare variables** and cannot be compared directly. Only within-dataset comparisons on our construction are valid.

## 4. New ambiguity for the methodology reference (no change to the frozen pipeline)

* **A9:** the paper's appendix (p. 544) describes Meinshausen's QRF, "retain the value of all observation". The cited software, `quantregForest` 1.3-5, stores **one** randomly sampled response per leaf.
  * The frozen pipeline follows the text (C2).
  * Measured difference between the two: ≤ 0.007 BPAC (E1, E3).
* **A2 update:** row 5 numerically implies a poverty rate of 24.038%, which supports Table 3's 24.03%.
  * Changing the frozen 24.2% would change results by ≤ 0.002 BPAC (E8; also the sensitivity run).
  * Under the change-control rules this is evidence for a correction, and **the decision is yours**.

## 5. Reframing after Phase 2 (`results/cv_qr/PHASE2_3_RESULTS.md`)

On our data, the published **CV linear quantile regression** replicates well: CV QR(0.37) against the published QR(0.38), with every metric except TA inside the published CIs.

On the same test households, our SE QRF is **not distinguishable** from our CV baseline:
* Disjoint split: BPAC −0.004 [−0.053, +0.056].
* Paper split: −0.030 [−0.109, +0.065].

So A8 narrows to one question: **why does the published SE QRF fall 7.76 BPAC points below the published CV baseline**, when on our construction the two are equal?

* **Implementation:** ruled out, see §1.
* **Remaining hypothesis:** the welfare aggregate and feature construction (I12, I13) hurt the forest more than the linear model in the authors' data. This is untested.

Until that is resolved, the defensible statement is:

> "On our construction of the Bolivia data, the QRF performs on par with the cross-validated linear quantile regression. Both clearly beat a fixed-quantile linear model on PA, and only in some protocols on BPAC."

Not:

> "QRF outperforms the published results."
