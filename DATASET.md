# Dataset description

**Status: FINAL.** Generated statistics: `results/dataset/` (by `describe_dataset.py`) and `results/audit/data_construction_audit.txt` (by `data_construction_audit.py`). Paper-ready table: `final_manuscript/tables/tableS6_descriptive_statistics.csv`.

## 1. Source

| Item | Value |
|---|---|
| Survey | Encuesta de Hogares 2005 (EH 2005), Instituto Nacional de Estadística (INE), Bolivia |
| Used in | McBride & Nichols (2018), Bolivia results (Table 3, p. 538) |
| Download | <https://siip.produccion.gob.bo/repSIIP2/files/encuesta_hogares/EH2005.rar> (accessed 2026-11-03) |
| Version | INE publishes no version number. The SHA-256 hashes below identify the exact files used. |
| Licence | No explicit open licence found. **The raw microdata are not redistributed in this package.** |

**Files used** (the archive also contains `Bolivia_Agricola.sav` and `Bolivia_Subproductos.sav`, which are not used):

| File | Content | Bytes | SHA-256 |
|---|---|---|---|
| `EH2005.rar` | Original archive | 10,329,896 | `ae7691d4…349d9d` |
| `BASE_EH_2005_(Pob_y_Viv).sav` | Persons and dwellings; includes the expenditure aggregate | 15,938,762 | `b329b433…208068` |
| `Bolivia_Equipamiento.sav` | Durable goods, one row per household × item | 4,674,411 | `5894d872…74d949a` |
| `Bolivia_Pecuaria.sav` | Livestock | 738,407 | `ff097b3a…30beca9aa` |

Full hashes: `SHA256SUMS` (check with `sha256sum -c SHA256SUMS`). Sizes: `DATA_MANIFEST.json`.

**To reproduce:** download and extract the archive, then place the four files in `data/bolivia/` (see `data/bolivia/README.md`).

## 2. Unit of analysis and sample

* **Unit:** household (`folio`). Person-level and item-level records are aggregated to one row per household (`common.build_household_frame`).
* **N = 4,086 households.** This matches the published sample size.
* **Missing data:** rows with a missing target or a missing head age are dropped, then any remaining feature is median-imputed. In practice, **0 rows were dropped and 0 values imputed.**
* **Survey weights:** not used, following the published study. Results describe the sample, not the population.
* One household has `G_TOTAL_pc` = 0. It is kept.

## 3. Target and poverty classification

| Item | Value |
|---|---|
| Welfare variable | `G_TOTAL_pc`: "gasto corriente total del hogar per cápita" (Bs/month). The article does not name its aggregate. |
| Distribution | mean 457.1 Bs; P10 121.0, median 329.4, P90 918.0 Bs |
| Primary poverty line | **189.09 Bs** = 24.2th percentile of the full sample ("24.2 percent", p. 538). Data-derived and **reconstructed**; no official "very poor" line in Bs was available. |
| Poverty rate at the line | 24.20% (full sample) |
| Sensitivity lines | 188.77 Bs (P24.03, published Table 3); 189.05 and 194.10 Bs (IRIS method reconstructions); a training-sample P24.2 per split (179.4–201.0 Bs); a 170–210 Bs scan; halved and doubled lines (94.55 and 378.18 Bs) |
| Rates at half / double the line | 6.09% / 57.10% (published: 4.92% / 62.26%). The welfare distribution differs from the authors'; see `RESULTS.md` §7. |

## 4. Features (the 21 IRIS variables of published Table 3)

| Feature | Survey source | Construction | Mean |
|---|---|---|---|
| `hhsize`, `hhsize2` | `miembros` | Household size and its square | 4.13 |
| `age_head`, `age_head2` | `s1_03` where `s1_05 == 1` | Age of the head (exactly one per household) and its square | 45.5 |
| `regions` | `depto` | Department 1–9. Ordinal for tree models; 8 dummies (reference: Chuquisaca) for linear models | — |
| `rural` | `urb_rur == 2` | Rural area | 0.429 |
| `sublease` ‡ | `s7_02 == 1` ("alquilada") | Rented dwelling. EH 2005 has no separate sublease category. | 0.141 |
| `brick_wall`, `wood_wall` | `s7_05 == 1`, `== 5` | Wall material | 0.379, 0.059 |
| `dirt_floor`, `cement_floor` | `s7_08 == 1`, `== 5` | Floor material | 0.315, 0.374 |
| `fridge`, `radio`, `tv`, `dvd`, `fan`, `car` | `s6_16 == 1` for items 7, 10, 12, 13, 18, 22 | Owns item | 0.293, 0.551, 0.596, 0.218, 0.097, 0.062 |
| `num_beds`, `num_computers` | `s6_17` for items 1, 9 | Count if owned, else 0 | 2.75, 0.10 |
| `num_kitchens` ‡ | `s7_19 == 1` | Separate kitchen room (binary). EH 2005 has no count. | 0.761 |
| `sheep` | `s8_10` where `codb == "B"` (Ovinos) | Sheep held last month; 0 if not in the livestock module | 4.77 |

‡ Approximation. The full statistics (SD, quartiles, min, max) are in `results/dataset/descriptive_statistics.csv`.

**Codebook verification:** 34 automated checks against the SPSS value labels, all passed (`results/audit/data_construction_audit.txt`). They cover one value per household, exactly one head, one row per household × item, label meanings and the sheep code.

## 5. Splits used for evaluation

| Protocol | Construction | Seeds |
|---|---|---|
| Published (overlapping) | Train and test = two independent draws of N/2 = 2,043 *with replacement* (p. 539); ~40% of unique test households also in training | 42 (primary); 1000–1029 (repeated) |
| Disjoint (adaptation) | Random 50/50 partition | same |

## 6. What is distributed

| Distributed | Not distributed |
|---|---|
| Code; aggregate results; descriptive statistics; figures; checksums | Raw survey files (`data/bolivia/*`); household-level predictions (`results/Bolivia/predictions.csv`); household-level plots (`actual_vs_predicted.png`, `qrf_intervals.png`). These are regenerated locally by `train_models.py`. |
