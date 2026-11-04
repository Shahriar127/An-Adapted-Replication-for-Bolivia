# Adapted replication of McBride & Nichols (2015), Bolivia EH 2005, plus a robustness extension

*Adapted replication using a reconstructed poverty threshold and documented implementation choices. This is not an exact replication: the paper's seed, IRIS training subset, poverty line in Bs and preprocessing are not public.*

This is an adapted replication of *"Improved Poverty Targeting Through Machine Learning: An Application to the USAID Poverty Assessment Tools"* (McBride & Nichols, 2015). It covers Bolivia only, and adds checks on the poverty threshold, the validation procedure and the QRF quantile.

## 1. Quick start

```bash
pip install -r requirements.txt          # exact versions used; see ENVIRONMENT.txt
# put the raw data in data/bolivia/ (see Section 3)
./run_all.sh                             # verifies checksums, then runs everything (~15–25 min on 12 cores)
```

Run the scripts one at a time:

| Script | Purpose | Output |
|---|---|---|
| `common.py` | The only place that defines the configuration, data construction, splits, metrics, bootstrap and quantile selection. Every other script imports it. | — |
| `data_construction_audit.py` | Checks the household-level construction against the EH 2005 codebook (SPSS value labels), with assertions | `results/audit/data_construction_audit.txt` |
| `config_audit.py` | Step 1. Re-runs the two old, inconsistent configurations so you can see how far each one moves the results. | `results/audit/` |
| `train_models.py` | Main model run: DT, RF and QRF with plots and predictions | `results/Bolivia/` |
| `replication_report.py` | Text report checking the replication against paper Table A1 | `results/Bolivia/replication_report.txt` |
| `sensitivity_analysis.py` | Steps 2–3: QRF(40) vs QRF(45), the three thresholds, two validation protocols and repeated splits | `results/sensitivity/` |
| `summarize_sensitivity.py` | Turns the sensitivity CSVs into Markdown | `results/sensitivity/SUMMARY.md` |
| `legacy/` | Both scripts as they were before the consistency fix. Kept for reference only. | — |

`synthetic_poverty_dataset.csv`, `generate_synthetic_poverty_dataset.py` and the PNG/CSV files at the top level of `results/` come from an earlier synthetic-data prototype. **No result in this package uses them.**

## 2. Fixed configuration

Everything below is set in `common.py`. Each result folder also gets a copy in `config.json`.

| Item | Value |
|---|---|
| Random seed (models and split) | `42`, using `np.random.RandomState` |
| Bootstrap seed | `42`. Every model and threshold uses the same 1000 resample indices, so all comparisons are paired. |
| Bootstrap re-draws | 1000 of the test sample, percentile 95% CI |
| Split, paper protocol | Two independent draws of N/2 = 2043, with replacement. About 40% of unique test households also appear in training. |
| Split, disjoint protocol | Random 50/50 partition, so the test set is never touched |
| Decision Tree | `max_depth=10, min_samples_leaf=20` |
| Random Forest | `n_estimators=500, max_features=1/3, min_samples_leaf=5` (R `randomForest` regression defaults) |
| QRF | `n_estimators=500, max_features=1/3, min_samples_leaf=5` (`quantile-forest`) |
| QRF quantile | Chosen by 5-fold CV BPAC **on the training sample only**, using household-grouped folds. Fixed q = 0.40 and 0.45 are also reported. |
| IRIS baseline | Linear quantile regression at τ = 0.42, `alpha=0`, HiGHS solver, with intercept and 8 region dummies (reference region: Chuquisaca). The earlier version used 9 dummies plus an intercept, which is rank-deficient; its predictions were identical, but its coefficients were not identified. |
| Features | The 21 variables from paper Table 3 (mapping in `replication_report.txt`, Section 2) |
| Target | `G_TOTAL_pc`, monthly per-capita household expenditure in Bs |
| Poverty line | 24.2th percentile of `G_TOTAL_pc` in the **full sample** = **189.0915 Bs**. This is **data-derived**: the test households help define it. The sensitivity analysis also uses 189.05 Bs, 194.10 Bs, and a **train-only** P24.2 computed separately for each split. |
| Missing data | Drop rows with a missing target or head age (0 rows dropped), then median-impute (no values needed imputing) |

## 3. Data

* **Survey:** Encuesta de Hogares 2005 (EH 2005), Instituto Nacional de Estadística (INE), Bolivia. N = 4,086 households, which matches the paper.
* **Source:** <https://siip.produccion.gob.bo/repSIIP2/files/encuesta_hogares/EH2005.rar> (downloaded 2026-11-03)
* **Files used:** `BASE_EH_2005_(Pob_y_Viv).sav`, `Bolivia_Equipamiento.sav`, `Bolivia_Pecuaria.sav`
* **Checksums:** `SHA256SUMS` (check with `sha256sum -c SHA256SUMS`); sizes are in `DATA_MANIFEST.json`
* **Version:** INE does not publish a version number for this release, so the SHA-256 hashes are the version identifier. If a later download has different hashes, the results may differ.

> **Raw data are not redistributed.** The microdata belong to INE Bolivia, and we found no explicit open licence that allows redistribution. They also contain household-level records. Download them yourself from the source above and check the hashes. The distributed tarball contains only code and aggregate results. `results/Bolivia/predictions.csv` holds household-level expenditure, so it is excluded from the tarball; `train_models.py` regenerates it locally.

## 4. Outputs

| File | Contents |
|---|---|
| `results/Bolivia/model_comparison.csv` | DT, RF and QRF: RMSE, MAE, R², and PA/UC/LE/BPAC with bootstrap 95% CIs |
| `results/Bolivia/confusion_matrices.csv` | TP/FP/FN/TN on the full test sample |
| `results/Bolivia/report_model_comparison.csv`, `report_confusion_matrices.csv` | The same split and models, plus IRIS Q(42) and fixed QRF(40) |
| `results/sensitivity/primary_metrics_bootstrap_ci.csv` | Every model × threshold × protocol, mean with 95% CI and point estimate |
| `results/sensitivity/primary_confusion_matrices.csv` | Confusion matrices for every model × threshold × protocol |
| `results/sensitivity/primary_paired_differences.csv` | Paired bootstrap CIs for QRF(40) − QRF(45) and for each threshold change |
| `results/sensitivity/repeated_splits_*.csv` | Point metrics over 30 random splits per protocol, plus the quantile chosen in each |
| `results/audit/config_audit.csv` | The old configurations re-run under both protocols |

## 5. Results

See `RESULTS.md`.

## 6. Known limitations

* Variable approximations: `regions` is ordinal for the tree models; `sublease` is coded as rented tenure; `num_kitchens` is binary.
* The original IRIS training subset, poverty line and seed are not public, so this is an *adapted* replication.
* Our implementation uses Python (`scikit-learn` / `quantile-forest`); the original used R `randomForest` / `quantregForest`.
* Only Bolivia is covered. East Timor and Malawi need World Bank registration.
* `G_TOTAL_pc` is 0 for one household.
* **Threshold:** every threshold used here is computed on this EH 2005 sample. We did not have an externally published "very poor" line in Bs.
* **Overlapping paper split:** about 40% of unique test households are also in training, which makes flexible models look better than they are. Results are also reported on a disjoint (untouched) test set.
* **Household construction:** checked against the codebook. Every household variable has one value per household, assets have one row per household and item, and `codb == "B"` is Ovinos (sheep). See `results/audit/data_construction_audit.txt`.
