# Phases 2–3: published CV baseline and Table A2 robustness

These are separate audit outputs. They are not part of the frozen primary pipeline; the frozen methodology and its results are unchanged.

**Scripts** (all run by `run_audits.sh`):
* `cv_qr_baseline.py`
* `table_a2_robustness.py`
* `paired_comparisons.py`

**Setup:** Bolivia EH 2005, seed 42, frozen 189.09 Bs line, 1,000 test-sample bootstrap draws (frozen `BOOT_SEED`). Metrics follow published Table 2 (TP+FN denominators).

## Phase 2: cross-validated linear quantile regression (published "CV" approach, p. 539)

**Procedure:**
* Linear quantile regression on the 21 IRIS variables.
* 500 iterations of 3-fold CV **inside the training sample**, grid 0.01–0.99, selecting by mean held-out BPAC.
* Refit on the full training sample at the chosen quantile, then evaluate on the test sample. The test sample is never used before the quantile is fixed.

**Compute shortcut (ADAPTED):**
* Stage 1 ran 50 iterations over the full grid.
* Stage 2 ran the remaining 450 only for quantiles within ±0.10 of each line's stage-1 best.
* Every excluded quantile trailed the stage-1 leader by **≥ 6.7 SE** (`cv_pruning_check.csv`), so the pruning cannot have changed the choice.
* The chosen quantile is stable from 50 iterations onward (`cv_choice_stability.csv`).

| | TA | PA | UC | LE | BPAC [95% CI] |
|---|---|---|---|---|---|
| **Published CV QR(0.38)** (Table A1 rows 6–8) | 81.76 | 63.37 | 36.63 | 41.61 | 57.94 [50.61, 63.44] |
| Ours, paper protocol: **CV QR(0.37)** | 83.71 | 66.52 | 33.48 | 36.86 | 62.27 [55.70, 67.32] |
| Ours, disjoint protocol: CV QR(0.34) | 83.93 | 67.84 | 32.16 | 37.04 | 62.62 [56.22, 67.72] |

**Confirmed:** our CV baseline replicates the published one.
* The selected quantile is 0.37 against the published 0.38.
* PA, UC, LE and BPAC all fall inside the published 95% CIs. TA is 0.39 points above the published upper bound.

## Published Table 4 contrasts, using paired bootstrap

`paired_comparisons.py` computes these contrasts at the base line. Each cell is the difference in BPAC or PA, with its 95% paired CI.

| Contrast | Published (Table 4) | Ours, paper protocol | Ours, disjoint protocol |
|---|---|---|---|
| CV − IRIS, BPAC | +8.61* | +0.037 [−0.056, +0.126] | +0.116 [−0.026, +0.226] |
| SE − IRIS, BPAC | +0.85 (n.s.) | **+0.067 [+0.002, +0.137]** | +0.120 [−0.011, +0.222] |
| CV − SE, BPAC | **+7.76*** | −0.030 [−0.109, +0.065] | **−0.004 [−0.053, +0.056]** |
| CV − IRIS, PA | +5.79* | +0.032 [+0.017, +0.048] | +0.055 [+0.035, +0.076] |
| CV − SE, PA | +8.04* | −0.023 [−0.058, +0.009] | +0.013 [−0.024, +0.047] |

**Confirmed for our data (single split):** the CV linear model and the stochastic-ensemble QRF are **statistically indistinguishable** (disjoint split: BPAC difference −0.004). In the published paper, CV beats SE by 7.76 points.

So the large "QRF beats IRIS" margins in `RESULTS.md` (+0.16 to +0.20) mostly reflect that the frozen IRIS benchmark uses a fixed, untuned quantile (0.42). Once the linear model's quantile is tuned on training data, the forest's advantage is no longer distinguishable from zero.

**Not tested:** the CV−SE contrast over repeated splits. The CV costs about 40 minutes per split.

### Why paired bootstrap instead of Tukey-Kramer

1. **Same households.** All models are scored on the same test households and the same 1,000 resamples. The CI of the per-resample difference d_b = M_A(b) − M_B(b) therefore accounts for the positive correlation between two models' errors. Comparing two separate CIs ignores that correlation and is too conservative.
2. **Replicates are not observations.** Table 4's Tukey-Kramer statistics (for example TK = 37.55) treat the 1,000 bootstrap replicates as independent data. Because B is chosen by the analyst, the test statistic grows roughly with √B while the actual uncertainty stays fixed. The resulting p-values do not measure sampling uncertainty.
3. **No distributional assumption.** BPAC contains an absolute value and is not smooth. The percentile CI of d_b does not assume normality.
4. **Scope.** The CI covers *test-sample* uncertainty for one fitted model per method. It does **not** cover training-sample or split variation; that is measured separately by the repeated-split runs in `results/sensitivity/` and `results/a8_audit/`.

## Phase 3: Table A2, halved and doubled poverty lines (p. 539, p. 547)

**Lines:** half and twice the frozen line, 94.55 Bs and 378.18 Bs.

**Rows, following the published definitions:**
* **IRIS:** the quantile with the best **in-sample** (training) BPAC at the new line.
* **CV and SE:** rerun at the new line.
* The frozen IRIS QR(0.42), not re-tuned, is shown for reference.

**Paper protocol, BPAC** (published values in brackets):

| Line | Rate: ours (published) | IRIS, in-sample best | CV | SE |
|---|---|---|---|---|
| Half | 6.09% (4.92%) | QR(0.51): 0.334 [QR(0.22): 30.07] | QR(0.51): 0.334 [QR(0.24): 29.65] | QRF(0.27): 0.492 [QRF(0.26): 26.94] |
| Double | 57.10% (62.26%) | QR(0.45): 0.811 [QR(0.54): 81.10] | QR(0.44): 0.809 [QR(0.52): 81.92] | QRF(0.53): 0.837 [QRF(0.54): 80.62] |

**Disjoint protocol, BPAC:**
* Half: IRIS 0.393, CV 0.361, SE 0.379.
* Double: IRIS 0.820, CV 0.820, SE 0.830.

**Findings:**
* **Double line:** BPAC levels match the published ones (0.81–0.84 vs 80.6–81.9). The ranking is flat, with all methods within about 0.03, as in the paper ("perform about the same", p. 543).
* **Half line:**
  * BPAC is very uncertain; CIs span about 0.3. Only about 6% of households are poor, and LE has a small denominator.
  * Our linear models choose QR(0.51), while the paper chose 0.22–0.24. Our SE choice of QRF(0.27) matches the paper's 0.26.
  * The paired-split SE value of 0.49 is not robust: the disjoint split gives 0.38, and the CIs overlap.
* **Not directly comparable:** the poverty rates at the new lines differ from the published ones (6.09% vs 4.92%; 57.10% vs 62.26%). This is the same welfare-distribution difference found in the A8 audit, so Table A2 can only be compared approximately.
