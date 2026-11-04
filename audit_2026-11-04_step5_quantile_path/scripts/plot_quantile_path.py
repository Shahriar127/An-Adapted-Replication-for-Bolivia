"""Small multiples: BPAC, PA, UC, LE against q for QRF and linear QR
(reads outputs/quantile_path_metrics.csv). One y-axis per panel; slots 1-2 of the
reference categorical palette; direct labels and CSV table as contrast relief."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
df = pd.read_csv(os.path.join(OUT, "quantile_path_metrics.csv"))
sel = pd.read_csv(os.path.join(OUT, "quantile_path_selection_summary.csv")).set_index("family")
FAM = [("QRF", "#2a78d6", "-", "o"), ("linear QR", "#eb6834", "--", "s")]
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
PANELS = [("BPAC", "BPAC  (higher is better)"), ("PA", "Poverty accuracy PA  (higher is better)"),
          ("UC", "Undercoverage UC = 1 − PA  (lower is better)"), ("LE", "Leakage LE  (lower is better)")]

fig, axes = plt.subplots(2, 2, figsize=(11, 7.4), sharex=True, facecolor=SURF)
for ax, (m, title) in zip(axes.ravel(), PANELS):
    ax.set_facecolor(SURF)
    ends, notes = [], []
    for fam, col, ls, mk in FAM:
        s = df[df.family == fam].sort_values("q")
        ax.plot(s.q, s[m], color=col, lw=2, ls=ls, marker=mk, ms=4, label=fam, zorder=3)
        if m == "BPAC":
            ax.fill_between(s.q, s[f"{m}_lo"], s[f"{m}_hi"], color=col, alpha=0.10, lw=0, zorder=2)
            qs = sel.loc[fam, "q_selected_on_training"]
            v = s.set_index("q").loc[qs, m]
            ax.plot([qs], [v], marker=mk, ms=9, mfc=SURF, mec=col, mew=2, zorder=4)
            notes.append(f"{fam}: q={qs:.2f} selected on training data (open marker), test BPAC {v:.3f}")
        ends.append([s[m].iloc[-1], fam, s.q.iloc[-1]])
    lo_, hi_ = ax.get_ylim(); gap = 0.06 * (hi_ - lo_)
    ends.sort(key=lambda e: e[0]); placed = []
    for yv, lab, xv in ends:
        yl = yv if not placed else max(yv, placed[-1] + gap)
        placed.append(yl)
        ax.annotate(lab, (xv, yv), xytext=(xv + 0.006, yl), textcoords="data", fontsize=7.5, color=INK,
                    va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))
    if m == "BPAC":
        ax.text(0.99, 0.03, "\n".join(notes), transform=ax.transAxes, ha="right", va="bottom",
                fontsize=7, color=MUTED)
    ax.set_title(title, fontsize=9.5, color=INK, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.set_xlim(0.295, 0.535)
for ax in axes[1]:
    ax.set_xlabel("Quantile q", fontsize=9, color=MUTED)
axes[0, 0].legend(loc="upper left", fontsize=7.5, frameon=False)
fig.suptitle("Quantile path on the disjoint split (seed 42, line 189.09 Bs), Bolivia EH 2005",
             fontsize=11, color=INK, x=0.01, ha="left")
fig.text(0.01, 0.005, "PA and UC are redundant: under the published definitions PA = TP/(TP+FN) and UC = FN/(TP+FN), "
         "so PA + UC = 1. Bands: 95% bootstrap CI (test sample). Data: quantile_path_metrics.csv",
         fontsize=7, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(os.path.join(OUT, "quantile_path.png"), dpi=200, facecolor=SURF)
print("saved", os.path.join(OUT, "quantile_path.png"))
