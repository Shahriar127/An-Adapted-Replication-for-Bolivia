# Pre-declared protocol: repeated-split CV-QR vs QRF audit

**Written:** 2026-11-04 09:27 (+06), **before** any Phase 1 result was computed. Any deviation is reported in `REPEATED_SPLIT_RESULTS.md` under "Deviations".

**Preservation:**
* The frozen methodology (`common.py`, `METHODOLOGY_REFERENCE.md`), existing results, the archive and the reproducibility package are read-only.
* A SHA-256 snapshot of 121 files was taken before starting: `logs/PRE_AUDIT_CHECKSUMS.sha256`. It is re-verified at the end.
* All new files are written under `audit_2026-11-04_repeated_split/`.

## Phase 1: repeated-split CV-QR vs QRF

| Item | Pre-declared choice |
|---|---|
| Split protocol | Published S1, unchanged: `common.paper_split_idx` (two independent N/2 draws with replacement) |
| Splits | Seeds **1000–1009**, the same seeds as the existing repeated-split analyses. **Pilot = seeds 1000, 1001, 1002.** If the pilot passes and no code changes, the pilot splits count as the first 3 of the 10. |
| Same households | For each seed, CV-QR and QRF use the identical training index set and the identical test index set. |
| CV-QR | As in `cv_qr_baseline.py`: linear QR on the frozen IRIS design (8 region dummies plus intercept, HiGHS, `alpha=0`); 500 iterations × 3-fold row-level CV inside the training sample; grid 0.01–0.99; score = mean held-out BPAC; first maximum wins. Two-stage evaluation: 50 iterations on the full grid, then 450 iterations within ±0.10 of each scored line's stage-1 best. Fold seeds are `split_seed × 100000 + iteration`. Refit on the full training sample at the chosen q. |
| QRF | The frozen stochastic-ensemble rule: RF plus QRF(0.01–0.99) (frozen `MODEL_CONFIG`), with the model chosen by OOB BPAC on the training sample. Model seed = split seed, as in the existing repeated-split runs. The selected label is recorded; it may be RF. |
| Lines scored | Primary: frozen 189.09 Bs (full-sample P24.2). Phase 3 also scores P24.03 = 188.77 Bs, with **no extra fits** (each fold's predictions are scored at both lines). The stage-2 window is the union over both lines. |
| Test data | Used only after both selections are fixed. Nothing is tuned on test data. |
| Primary outcome | Split-level **ΔBPAC = BPAC(CV-QR) − BPAC(QRF)** on the full test sample (point estimate). |
| Secondary outcomes | ΔTA, ΔPA, ΔUC and ΔLE, defined the same way |
| **Tie tolerance** | **\|Δ\| ≤ 0.010** (1 percentage point) counts as a tie. Otherwise Δ > 0 is a CV-QR win and Δ < 0 a QRF win. For UC and LE lower is better, so the win direction is reversed for those. |
| Within-split uncertainty | Paired bootstrap, 1,000 resamples of the test sample (frozen `BOOT_SEED`), giving a 95% percentile CI for Δ. This is **test-sample** uncertainty only. |
| Across-split summary | For the 10 split-level Δ values: mean, SD, minimum and maximum, and the 2.5th–97.5th empirical percentiles. A 95% CI for the mean is given two ways: (a) naive t-interval, mean ± t₀.₉₇₅,₉ · SD/√10; (b) the Nadeau–Bengio corrected variance (1/J + n_test/n_train) · SD², because splits share households and are not independent. With n_test = n_train this correction is very conservative; (a) and (b) are reported as bounds. |
| Bootstrap ≠ splits | Bootstrap resamples are never counted as splits. Only the 10 split-level point estimates enter the across-split statistics. |
| Convergence | Every HiGHS fit is checked: any `ConvergenceWarning` or failed fit is counted per split and reported. |
| Reproducibility check | Stage 1 of the existing seed-42 run is recomputed for the base line and must equal the stored `results/cv_qr/cv_fold_bpac_paper.npy` (line 0, first 150 folds) exactly. |
| Pilot pass criteria | (1) no crash and no unhandled fit failure; (2) the reproducibility check is exact; (3) per-split outputs are complete and valid (selected q inside the grid, metrics in range, PA + UC = 1); (4) the measured runtime is reported, with a projection for 10 splits. |
| Compute limit | If 10 splits are infeasible, stop after the pilot, report it, and propose a reduced design explicitly. The number of splits is never silently reduced. |

## Phase 2: A9/A10 sensitivity

This is separate from Phase 1. Seeds **42 and 1000–1019** (the A8 audit seeds). One factor at a time from the frozen baseline B0, and both selection outputs are recorded: the SE (OOB-selected) model and fixed QRF(0.41). Configurations:
* **A9-text:** frozen, all leaf observations; this is B0.
* **A9-software:** the exact `quantregForest` 1.3-5 emulation (one value per leaf from all n rows, type-7 quantile, R OOB).
* **A9-qf1:** `quantile-forest` with `max_samples_leaf=1`.
* **A10-R:** `min_samples_split=6, min_samples_leaf=1` for both RF and QRF.
* **A9+A10:** the software emulation combined with the R node rule.

## Phase 3: poverty-rate sensitivity

The frozen 24.2% stays primary. 24.03% is a separate run:
* The frozen primary models (DT, RF, IRIS QR(0.42), QRF fixed at 0.40/0.41/0.45, SE OOB), both protocols, with seed-42 bootstrap and 30 repeated splits (seeds 1000–1029).
* CV-QR at 24.03% for the 10 Phase 1 splits.
