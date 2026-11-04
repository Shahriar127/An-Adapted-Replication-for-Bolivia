#!/usr/bin/env bash
# Reproduce every result in results/ from the raw Bolivia EH 2005 files.
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS                       # 1. verify raw data
python3 data_construction_audit.py            # 2a. codebook checks of household construction
python3 config_audit.py                       # 2b. Step 1: legacy-config audit
python3 train_models.py                       # 3. model outputs  (results/Bolivia/)
python3 replication_report.py                 # 4. report         (results/Bolivia/replication_report.txt)
N_SPLITS=30 python3 sensitivity_analysis.py   # 5. Steps 2–3      (results/sensitivity/)
python3 summarize_sensitivity.py              # 6. Markdown summary
