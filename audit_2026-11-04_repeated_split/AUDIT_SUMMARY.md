# Audit summary: repeated-split CV-QR vs QRF (stopped after pilot)

* **Protocol:** `PROTOCOL.md`, pre-declared 2026-11-04 09:27.
* **Run:** a 3-split pilot (seeds 1000–1002, published split) plus a reproducibility check. **Passed:**
  * the stored seed-42 CV stage was reproduced exactly;
  * 0 convergence warnings and 0 failed fits;
  * about 26 minutes per split.
* **Result:** QRF scored higher than CV-QR on BPAC in all 3 splits (Δ = −0.039, −0.068, −0.038; each test-bootstrap CI reaches or crosses 0). This is confounded with the overlap inflation of about +0.035 for QRF. **Not conclusive.** Details: `REPEATED_SPLIT_RESULTS.md`, `outputs/pilot_per_split_results.csv`.
* **Not run, by your decision of 2026-11-04:**
  * the remaining 7 splits;
  * Phase 2, A9/A10 (`scripts/a9_a10_sensitivity.py`, written but not executed);
  * Phase 3, poverty rate (`scripts/poverty_rate_sensitivity.py`, written but not executed).

  `A9_A10_SENSITIVITY.md` and `POVERTY_RATE_SENSITIVITY.md` were therefore not produced. Earlier A8-audit results on A9/A10 (`results/a8_audit/`) and the frozen 24.03% sensitivity (`RESULTS.md` §4) still stand.
* **Evidence:** byte-level R sources with SHA-256 (randomForest 4.6-12; quantregForest 1.3-5) in `evidence/r_source/`.
* **Preservation:** pre-audit checksums are in `logs/PRE_AUDIT_CHECKSUMS.sha256` and are verified at the end of the step.
