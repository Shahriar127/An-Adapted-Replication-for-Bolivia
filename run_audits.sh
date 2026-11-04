#!/usr/bin/env bash
# A8 audit + Phase 2-3 (published CV baseline, Table A2). Separate from the
# frozen pipeline (run_all.sh); writes only to results/a8_audit, results/cv_qr,
# results/table_a2. The CV step takes about 40 min per protocol on 12 cores.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m unittest discover -s tests
python3 a8_data_diagnostics.py                 # deterministic data-construction checks
A8_SPLITS=20 python3 a8_qrf_audit.py           # one-factor forest experiments (~13 min)
CV_ITER=500 python3 cv_qr_baseline.py          # published CV QR baseline (500 x 3-fold)
python3 table_a2_robustness.py                 # halved / doubled lines (needs cv_qr)
python3 paired_comparisons.py                  # Table 4 contrasts, paired bootstrap
