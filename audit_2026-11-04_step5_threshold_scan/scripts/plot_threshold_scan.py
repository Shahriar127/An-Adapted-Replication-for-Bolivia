"""Plot BPAC vs poverty threshold (reads outputs/threshold_scan_metrics.csv).
Palette: reference categorical slots 1-4 (validated light mode; the contrast WARN
is relieved by direct labels, distinct line styles and the CSV table view)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
df = pd.read_csv(os.path.join(OUT, "threshold_scan_metrics.csv"))
SERIES = [  # (model key, label, color slot, linestyle)
    ("SE OOB-selected", "QRF (OOB-selected q)", "#2a78d6", "-"),
    ("QRF(q=0.40) fixed", "QRF q=0.40 fixed", "#eb6834", "--"),
    ("IRIS_Q42", "IRIS QR q=0.42 fixed", "#1baf7a", "-."),
    ("RandomForest", "RF (conditional mean)", "#eda100", ":"),
]
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
REF = [(188.77, "P24.03"), (189.09, "frozen P24.2"), (194.10, "194.10")]

fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True, facecolor=SURF)
for ax, proto, title in zip(axes, ["paper", "disjoint"],
                            ["Published protocol (overlapping N/2 draws)", "Disjoint 50/50 split"]):
    ax.set_facecolor(SURF)
    sub = df[df.protocol == proto]
    ends = []
    for x, lab in REF:
        ax.axvline(x, color=MUTED, lw=0.8, ls=(0, (2, 3)), zorder=1)
    ax.text(189.09, 1.0, "  189.09 (frozen)", transform=ax.get_xaxis_transform(), fontsize=7.5,
            color=MUTED, va="top", ha="left")
    for key, lab, col, ls in SERIES:
        s = sub[sub.model == key].sort_values("threshold")
        ax.plot(s.threshold, s.BPAC, color=col, lw=2, ls=ls, label=lab, zorder=3)
        if key in ("SE OOB-selected", "IRIS_Q42"):
            ax.fill_between(s.threshold, s.BPAC_lo, s.BPAC_hi, color=col, alpha=0.10, lw=0, zorder=2)
        ends.append([s.BPAC.iloc[-1], lab, s.threshold.iloc[-1]])
    # direct labels with a minimum vertical gap (label dodge), connected by a hairline
    ends.sort(key=lambda e: e[0])
    placed = []
    for yv, lab, xv in ends:
        yl = yv if not placed else max(yv, placed[-1] + 0.035)
        placed.append(yl)
        ax.annotate(lab, (xv, yv), xytext=(xv + 0.8, yl), textcoords="data", fontsize=7.5, color=INK,
                    va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.set_xlabel("Poverty threshold (Bs per person per month)", fontsize=9, color=MUTED)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.set_xlim(170, 220)
axes[0].set_ylabel("BPAC (test sample, point estimate)", fontsize=9, color=MUTED)
axes[0].legend(loc="lower left", fontsize=7.5, frameon=False)
fig.suptitle("Targeting accuracy (BPAC) across poverty thresholds, Bolivia EH 2005, seed 42",
             fontsize=11, color=INK, x=0.01, ha="left")
fig.text(0.01, 0.005, "Bands: 95% bootstrap CI (test-sample uncertainty, 1,000 draws) for the OOB-selected QRF and IRIS. "
         "Dotted verticals: 188.77, 189.09 (frozen), 194.10 Bs. Data: threshold_scan_metrics.csv",
         fontsize=7, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(os.path.join(OUT, "bpac_vs_threshold.png"), dpi=200, facecolor=SURF)
fig.savefig(os.path.join(OUT, "bpac_vs_threshold.pdf"), facecolor=SURF)   # vector copy for journal submission
print("saved", os.path.join(OUT, "bpac_vs_threshold.png"))

# Journal versions of this figure: final_manuscript/figures/make_journal_figures.py
