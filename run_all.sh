#!/usr/bin/env bash
# Reproduce every result of the frozen pipeline from the raw Bolivia EH 2005 files.
# Usage: ./run_all.sh 2>&1 | tee results/run_all_log.txt   (~8 min on 12 cores)
# The audits are run separately by run_audits.sh (CV-QR step: about 40 min per protocol).
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS                       # 1. verify raw data
python3 -m unittest discover -s tests          # 1b. methodology unit tests (must pass)
python3 data_construction_audit.py            # 2a. codebook checks of household construction
python3 config_audit.py                       # 2b. Step 1: legacy-config audit
python3 correction_impact.py                  # 2c. impact of each freeze correction (C1-C3)
python3 train_models.py                       # 3. model outputs  (results/Bolivia/)
python3 replication_report.py                 # 4. report         (results/Bolivia/replication_report.txt)
N_SPLITS=30 python3 sensitivity_analysis.py   # 5. Steps 2–3      (results/sensitivity/)
python3 summarize_sensitivity.py              # 6. Markdown summary
python3 describe_dataset.py                   # 7. aggregate descriptive statistics (results/dataset/)
