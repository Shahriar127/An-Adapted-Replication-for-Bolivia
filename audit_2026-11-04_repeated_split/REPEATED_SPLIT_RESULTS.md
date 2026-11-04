# Repeated-split CV-QR vs QRF: PILOT ONLY (n = 3)

**Status.** The pre-declared protocol (`PROTOCOL.md`) planned a 3-split pilot followed by 10 splits.
* The pilot ran and passed every pass criterion.
* The remaining 7 splits were **not run**, by your decision of 2026-11-04 to stop expensive repeated-split runs.
* **This file therefore reports a 3-split pilot, not the planned 10-split study.** No across-split inference is drawn.

**Run record:**
* **Command:** `python3 audit_2026-11-04_repeated_split/scripts/repeated_split_cvqr_vs_qrf.py --repro-check --seeds 1000 1001 1002`, run inside `systemd-inhibit --what=sleep:idle`.
* **Time:** started 2026-11-04 09:28:06 (+06), ended 10:53:54. Exit code 0. Log: `logs/pilot.log`, `logs/COMMANDS.log`.
* **Protocol:** published S1 split (`common.paper_split_idx`). The frozen 189.09 Bs line is primary; P24.03 (188.77 Bs) is also scored.
* **CV-QR:** 500 × 3-fold CV on training only, two-stage, grid 0.01–0.99.
* **QRF:** frozen OOB-BPAC rule over RF and QRF(0.01–0.99). Model seed = split seed.
* **Same households:** CV-QR and QRF used identical train/test households in every split.

## Pilot pass criteria

| Criterion | Result |
|---|---|
| Reproducibility: stage 1 of the stored seed-42 run recomputed | **Identical.** 150 × 99 fold BPACs, max \|diff\| = 0.0 (`outputs/repro_check_seed42_stage1.json`) |
| Convergence | **0** `ConvergenceWarning`s and **0** failed fits, across all fits in 3 splits plus the check |
| Output validity | Selected q inside the grid; PA + UC = 1 exactly; pruning margin 20–23 SE (so the pruned quantiles could not win); CV choice stable from 50 iterations onward |
| Runtime | 1,512 s, 1,569 s and 1,545 s per split (about 26 min); repro check 520 s. Projection for 10 splits ≈ 4.3 h. |

## Per-split results (frozen line 189.09 Bs)

Machine-readable: `outputs/pilot_per_split_results.csv`, with both lines and all metrics. Δ = CV-QR − QRF on the full test sample. The CI is a paired bootstrap over test-sample resamples (1,000 draws), so it reflects test-sample uncertainty only.

| Seed | CV-QR q | QRF chosen | BPAC CV-QR | BPAC QRF | ΔBPAC [95% test-bootstrap CI] | ΔPA | ΔLE | Outcome (tol. 0.010) |
|---|---|---|---|---|---|---|---|---|
| 1000 | 0.33 | QRF(0.41) | 0.625 | 0.664 | −0.039 [−0.077, 0.000] | −0.033 | +0.039 | QRF higher |
| 1001 | 0.34 | QRF(0.40) | 0.626 | 0.694 | −0.068 [−0.110, +0.004] | −0.035 | +0.068 | QRF higher |
| 1002 | 0.34 | QRF(0.39) | 0.659 | 0.697 | −0.038 [−0.084, +0.025] | −0.030 | +0.038 | QRF higher |

**Across the 3 splits (descriptive only):**
* ΔBPAC mean −0.048, SD 0.017, range −0.068 to −0.038.
* Wins: CV-QR 0, QRF 3, ties 0.
* With n = 3, no across-split interval is reported. The pre-declared t and Nadeau–Bengio intervals need the 10-split run.

**At P24.03 (188.77 Bs):** ΔBPAC −0.045, −0.054 and −0.032. The selected CV-QR q is unchanged except for seed 1001 (0.34 → 0.35). The QRF choices are unchanged.

## Interpretation (cautious)

1. **The pilot leans the other way from the earlier single-split result.** That result, on seed 42 with the paper protocol, gave ΔBPAC −0.030 [−0.109, +0.065]. Here all three pilot splits favour QRF by 0.038–0.068. Every per-split test-bootstrap CI reaches or crosses zero.
2. **This is the published, overlapping protocol.** About 40% of unique test households also appear in training. The earlier frozen analysis (`RESULTS.md` §5) found that this overlap adds about +0.035 BPAC to the QRF and about 0 to linear QR. That bias is of the **same size** as the pilot differences, so the pilot cannot separate a genuine QRF advantage from overlap inflation. The disjoint protocol was not part of this pilot.
3. **A metric property explains why ΔBPAC = −ΔLE in every row.** Under the published definitions (PA = 1 − UC), BPAC = 1 − LE whenever LE ≥ UC, i.e. FP ≥ FN. Both models over-predict poverty here, so the BPAC difference is entirely a leakage difference.
4. **Conclusion:** the pilot does **not** establish that QRF is better than CV-QR, and it does not confirm equivalence either. The earlier "SE ≈ CV-QR" statement rests on one split per protocol, and this pilot weakens it for the published protocol. Answering the question needs the planned 10 splits, ideally under both protocols. That was not run.

## Deviations from the protocol
* 7 of the 10 planned splits were not run (your decision). Nothing else deviated.
* Phase 2 (`scripts/a9_a10_sensitivity.py`) and Phase 3 (`scripts/poverty_rate_sensitivity.py`) were **written but not run**, after the same decision. Their deliverables (`A9_A10_SENSITIVITY.md`, `POVERTY_RATE_SENSITIVITY.md`) were therefore not produced. The 24.03% figures above come only from the pilot's joint scoring.
