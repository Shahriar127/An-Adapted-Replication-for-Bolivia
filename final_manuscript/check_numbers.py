"""
Numerical consistency check: every decimal number in MANUSCRIPT.md must match
(to its printed precision) a value in evidence_numbers.csv, a value from the
published article (PUBLISHED below, as printed in the PDF), or an explicitly
documented derived value (DERIVED below). Unmatched numbers are listed for
manual review. Read-only; writes number_check_report.txt.
Usage (from Model_Training/): python3 final_manuscript/check_numbers.py
"""
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ev = pd.read_csv(os.path.join(HERE, "evidence_numbers.csv"))
vals = set()
for v in ev.value.astype(str):
    for tok in re.findall(r"[-+]?\d+\.\d+", v):
        x = float(tok)
        for nd in (1, 2, 3, 4):
            vals.add(round(x, nd)); vals.add(round(-x, nd)); vals.add(round(x * 100, nd)); vals.add(round(x / 100, nd))
# Published values as printed (percent) in McBride & Nichols (2018) Tables A1, A2, 3, 4
PUBLISHED = [81.88, 57.58, 42.42, 34.3, 49.33, 79.78, 83.68, 52.51, 62.65, 37.35, 47.49, 27.6, 41.66, 36.73, 60.48,
             81.76, 63.37, 36.63, 41.61, 57.94, 80.10, 83.32, 58.84, 67.88, 32.12, 41.15, 35.15, 48.24, 50.61, 63.44,
             80.17, 55.33, 44.67, 40.44, 50.18, 78.25, 82.03, 50.51, 60.12, 39.88, 49.49, 33.59, 48.11, 39.26, 58.57,
             82.45, 60.69, 39.30, 33.71, 55.10, 24.03, 24.2, 4.92, 62.26, 81.10, 81.92, 80.62, 30.07, 29.65, 26.94,
             5.79, 2.25, 8.04, 8.61, 0.85, 7.76, 64.78]
for p in PUBLISHED:
    for nd in (1, 2, 3):
        vals.add(round(p, nd)); vals.add(round(p / 100, nd)); vals.add(round(-p / 100, nd))
# Documented derived values (computed in the text from evidence values)
DERIVED = {0.034: "gap widening paper (0.088-0.054)", 0.067: "gap widening disjoint (0.115-0.048)",
           0.035: "overlap effect (rounded, Table 2)", 0.036: "SE overlap diff 0.679-0.644", 0.045: "QRF45 overlap diff",
           0.066: "RF overlap diff", 0.002: "IRIS overlap diff", 0.013: "0.642-0.629", 0.110: "0.663-0.554",
           0.078: "0.587-0.509", 0.025: "IRIS C1 shift paper", 0.064: "IRIS C1 shift disjoint",
           2.2: "2.2e-16 residual", 1.6: "1.6e-12 emulation match", 0.3: "0.3 Bs shift", 0.5: "scan step 0.5 Bs",
           0.1: "+-0.10 window", 6.65: "pruning gap", 0.12: "-", 0.02: "approx optimism",
           0.39: "1-exp(-1/2)=0.393, overlap probability (algebra, Disc 6.1)", 0.32: "189.0915-188.7743=0.317 Bs",
           0.17: "24.20%-24.03% = 0.17 pp of sample", 174.5: "scan threshold (configured grid value)"}
for k in DERIVED:
    vals.add(round(k, 3))
txt = open(os.path.join(HERE, "MANUSCRIPT.md")).read()
nums = re.findall(r"(?<![\w.])[−+-]?\d+\.\d+", txt)
unmatched = []
for n in nums:
    x = float(n.replace("−", "-"))
    nd = len(n.split(".")[1])
    if round(x, nd) not in vals and round(abs(x), nd) not in vals:
        unmatched.append(n)
rep = [f"decimal numbers in manuscript: {len(nums)}",
       f"unmatched (need manual review): {len(set(unmatched))}", *sorted(set(unmatched))]
open(os.path.join(HERE, "number_check_report.txt"), "w").write("\n".join(rep) + "\n")
print("\n".join(rep))
