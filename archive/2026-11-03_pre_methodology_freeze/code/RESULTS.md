# Results: consistency audit, QRF(40) vs QRF(45), threshold sensitivity

Data: Bolivia EH 2005, N = 4,086. Configuration: `common.py` / `config.json`. Unless stated otherwise, the threshold is 189.09 Bs.
"Repeated splits" means 30 random splits per protocol, and figures are mean (SD) of the point estimates. "Primary" means seed 42, with a 95% bootstrap CI from 1000 resamples.
**Paper** protocol: overlapping N/2 bootstrap split. **Disjoint** protocol: untouched 50/50 test set.

## Step 1: Consistency audit

Before the fix, the two scripts did **not** share a configuration:

| Item | old `train_models.py` | old `replication_report.py` |
|---|---|---|
| Decision Tree | `max_depth=10, min_samples_leaf=20` | unrestricted (sklearn defaults) |
| RF / QRF `min_samples_leaf` | 5 | 1 (default) |
| Split RNG | `np.random.RandomState(42)` | `np.random.default_rng(42)`, so a **different split** |
| Bootstrap seed | 42 for every model | 52/62/72 (one per model, so comparisons were unpaired) |
| QRF quantile | best BPAC **on the test set** | best BPAC **on the test set** |
| Missing-data rule | drop missing target | drop missing target **or** head age (0 rows on this data) |
| Section 11 figures | — | hard-coded, not computed |

`config_audit.py` re-runs both old configurations and reproduces both old outputs exactly. That pins down where the earlier "QRF(45), BPAC 0.797" came from:

| Old report config, QRF(45) | PA | BPAC [95% CI] |
|---|---|---|
| paper split (overlapping) | 0.832 | 0.797 [0.755, 0.833] |
| same config, disjoint split | 0.658 | 0.594 [0.520, 0.651] |

With `min_samples_leaf=1`, the forest memorises training households, and about 40% of the unique test households are also in training. That overlap inflated BPAC by about 0.20. **The 0.797 figure is an artefact of the protocol and should not be reported.**

**After the fix:** all scripts import `common.py`. `train_models.py` and `replication_report.py` now give identical DT/RF/QRF numbers, and the quantile is chosen by CV on the training sample only.

### Checks on household construction (`data_construction_audit.py`)
All checks pass against the EH 2005 codebook (SPSS value labels):

* Household variables have exactly one value per household, and each household has exactly one head.
* Durable goods have exactly one row per (household, item), so `.first()` drops nothing. All 22 items are present for every household, and the item codes match their labels.
* `codb == "B"` is *Ovinos* (sheep), with one record per household. `s8_10` is present exactly when `s8_05 == 1`.

**Conclusion:** the construction follows the survey's coding. Whether it matches the variables *the paper's authors* built cannot be checked. Three approximations remain: `num_kitchens` is binary, `sublease` is coded as rented, and `regions` is ordinal for the tree models.

### IRIS dummy redundancy
With 9 region dummies plus an intercept, the design has rank 29 of 30. Switching to `drop_first` (reference region: Chuquisaca) or dropping the intercept gives **identical predictions** (maximum absolute difference 0.0) and identical PA/UC/LE/BPAC. Targeting results are therefore unaffected; only the coefficients were not identified. `common.iris_design` now uses 8 dummies plus an intercept.

## Step 2: QRF(40) vs QRF(45), controlled comparison

Both models come from the same fitted forest, use the same split, and are evaluated on the same bootstrap indices. Neither quantile was chosen by looking at the test set.

| Protocol | Model | PA | UC | LE | BPAC |
|---|---|---|---|---|---|
| paper, primary | QRF(40) | 0.695 | 0.295 | 0.310 | 0.665 [0.583, 0.719] |
| paper, primary | QRF(45) | 0.731 | 0.337 | 0.244 | 0.627 [0.554, 0.691] |
| disjoint, primary | QRF(40) | 0.652 | 0.345 | 0.350 | 0.622 [0.547, 0.671] |
| disjoint, primary | QRF(45) | 0.677 | 0.404 | 0.285 | 0.540 [0.458, 0.616] |
| disjoint, 30 splits | QRF(40) | 0.674 (.018) | 0.334 (.022) | 0.323 (.029) | 0.641 (.031) |
| disjoint, 30 splits | QRF(45) | 0.705 (.019) | 0.396 (.023) | 0.253 (.026) | 0.535 (.047) |

Paired difference QRF(40) − QRF(45), disjoint protocol, 30 splits:

| Metric | Mean difference | Splits where QRF(40) is higher |
|---|---|---|
| PA | −0.031 | 0 / 30 |
| UC | −0.062 | 0 / 30 |
| LE | +0.070 | 30 / 30 |
| BPAC | +0.105 | 29 / 30 |

On a single split, the bootstrap CI for the BPAC difference includes 0 (seed 42, disjoint: +0.082 [−0.052, +0.153]). Across splits the sign is very consistent.

**Quantile chosen by CV on the training data:** q = 0.40 in 30 of 30 repeated splits under both protocols. The one exception is seed 42 with the paper split, where CV picks 0.45; that is the split `train_models.py` and `replication_report.py` report, so their tables show QRF(CV q = 45) next to the fixed QRF(40). Test-set selection also picks 0.40 in 27–28 of 30. With a consistent configuration and honest selection, **we recover the paper's QRF(40). Our earlier QRF(45) came from the inconsistent report configuration.**

Choosing the quantile on the test set adds only +0.005 (paper) and +0.007 (disjoint) BPAC over CV selection. The optimism is small here because the choice is stable; the overlapping split is a much larger source of optimism.

Trade-off: QRF(40) flags more households, so it has lower UC but higher LE. BPAC favours that trade, while PA favours QRF(45). Which quantile is "better" therefore depends on the metric.

## Step 3: Poverty-threshold sensitivity

The thresholds compared are 189.09 Bs (full-sample P24.2), 189.05 Bs, 194.10 Bs, and P24.2 computed from the **training sample only**. Models are fit once; only the classification line changes.

Change in BPAC relative to 189.09 Bs, disjoint protocol, mean (SD) over 30 splits:

| Model | 189.05 | 194.10 |
|---|---|---|
| QRF(40) | ≈0 | +0.005 (0.019) |
| QRF(45) | ≈0 | +0.023 (0.017) |
| IRIS Q(42) | ≈0 | +0.018 (0.012) |
| Random Forest | ≈0 | +0.079 (0.037) |
| Decision Tree | ≈0 | +0.053 (0.108) |

* **189.05 vs 189.09 Bs is negligible.** Across every model, split and protocol, the largest absolute change in BPAC is 0.014. In the primary run, every paired CI includes 0.
* **194.10 Bs is not uniformly negligible.** For QRF(40) the shift is within noise (+0.005). The conditional-mean models, RF and DT, shift by +0.05 to +0.08 BPAC, and in the primary disjoint run the RF change is significant: +0.071 [+0.010, +0.137]. For QRF(40) on the disjoint split, PA (+0.025) and LE (−0.030) also change significantly. Model *rankings* do not change.
* **Train-derived threshold:** P24.2 of the training sample varies from 179 to 201 Bs across splits (SD ≈ 5 Bs). The threshold's own sampling variation is therefore as large as the 189 → 194 Bs gap. Using it instead of the full-sample threshold changes QRF(40)'s mean BPAC by less than 0.005.

## Other findings

* **Overlap optimism:** moving from the paper protocol to the disjoint one lowers QRF(40) BPAC from 0.675 to 0.641 (30-split means). RF PA drops from 0.829 to 0.794. In the primary run, DT and RF BPAC fall below 0.
* **The QRF advantage comes from the quantile shift:** RF (conditional mean) has UC ≈ 0.58 and BPAC ≈ −0.1 on the disjoint split. QRF at q = 0.40 beats IRIS Q(42) on BPAC by +0.09 (29 of 30 splits).
* **Comparison with paper Table A1:** on the disjoint split, our QRF(40) has PA 0.674 and BPAC 0.641; the paper reports 0.621 and 0.582 [0.47, 0.63]. For IRIS Q(42), we get PA 0.702 and BPAC 0.551; the paper reports 0.576 and 0.493. The largest gap is IRIS PA, about +0.13. Neither the threshold nor the overlap explains it, so it most likely comes from feature construction or the paper's unpublished training subset. That remains a hypothesis.
