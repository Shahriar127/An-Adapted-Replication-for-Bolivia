"""
make_journal_figures.py — Figures 1–2 of the manuscript, drawn at journal print size.

Reads the same result files as the audit plots (no model is fitted):
  Figure 1  audit_2026-11-04_step5_threshold_scan/outputs/threshold_scan_metrics.csv
  Figure 2  audit_2026-11-04_step5_quantile_path/outputs/quantile_path_metrics.csv (+ selection summary)

Layout follows the reference article (World Bank Economic Review): full text-block
width (424.8 pt = 5.9 in), no embedded title (the caption is set above the figure in
the manuscript), sans-serif labels at 7–8 pt, legend instead of in-plot labels.
Writes Figure1_threshold_scan.(pdf|png) and Figure2_quantile_path.(pdf|png), PNG at 600 dpi.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
W = 5.9                                     # inches = 424.8 pt text block
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
})
INK, GRID = "#231f20", "#d9d9d9"
COL = {"SE": "#2a78d6", "Q40": "#eb6834", "IRIS": "#1baf7a", "RF": "#eda100", "LIN": "#eb6834"}


def save(fig, stem):
    for ext, kw in ((".pdf", {}), (".png", {"dpi": 600})):
        fig.savefig(os.path.join(HERE, stem + ext), facecolor="white", bbox_inches="tight", pad_inches=0.02, **kw)
    plt.close(fig)
    print("saved", stem)


def figure1():
    df = pd.read_csv(os.path.join(ROOT, "audit_2026-11-04_step5_threshold_scan", "outputs", "threshold_scan_metrics.csv"))
    series = [("SE OOB-selected", "QRF, OOB-selected q", COL["SE"], "-"),
              ("QRF(q=0.40) fixed", "QRF, q = 0.40 fixed", COL["Q40"], "--"),
              ("IRIS_Q42", "IRIS QR, q = 0.42 fixed", COL["IRIS"], "-."),
              ("RandomForest", "RF (conditional mean)", COL["RF"], ":")]
    fig, axes = plt.subplots(1, 2, figsize=(W, 2.55), sharey=True)
    for ax, proto, title in zip(axes, ("paper", "disjoint"), ("A. Published protocol (overlapping draws)", "B. Disjoint 50/50 split")):
        sub = df[df.protocol == proto]
        for x in (188.77, 189.09, 194.10):
            ax.axvline(x, color="#7f7f7f", lw=0.5, ls=(0, (1.5, 2)), zorder=1)
        for key, lab, col, ls in series:
            s = sub[sub.model == key].sort_values("threshold")
            ax.plot(s.threshold, s.BPAC, color=col, lw=1.1, ls=ls, label=lab, zorder=3)
            if key in ("SE OOB-selected", "IRIS_Q42"):
                ax.fill_between(s.threshold, s.BPAC_lo, s.BPAC_hi, color=col, alpha=0.12, lw=0, zorder=2)
        ax.set_title(title, loc="left", color=INK)
        ax.set_xlabel("Poverty line (Bs per person per month)")
        ax.set_xlim(170, 210)
        ax.grid(axis="y", color=GRID, lw=0.4)
    axes[0].set_ylabel("BPAC (test sample)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.02), handlelength=2.6)
    fig.tight_layout(rect=(0, 0.08, 1, 1), w_pad=1.0)
    save(fig, "Figure1_threshold_scan")


def figure2():
    out = os.path.join(ROOT, "audit_2026-11-04_step5_quantile_path", "outputs")
    df = pd.read_csv(os.path.join(out, "quantile_path_metrics.csv"))
    sel = pd.read_csv(os.path.join(out, "quantile_path_selection_summary.csv")).set_index("family")
    fam = [("QRF", "QRF", COL["SE"], "-", "o"), ("linear QR", "Linear QR", COL["LIN"], "--", "s")]
    panels = [("BPAC", "A. BPAC (higher is better)"), ("PA", "B. Poverty accuracy, PA (higher is better)"),
              ("UC", "C. Undercoverage, UC = 1 − PA (lower is better)"), ("LE", "D. Leakage, LE (lower is better)")]
    fig, axes = plt.subplots(2, 2, figsize=(W, 4.1), sharex=True)
    for ax, (m, title) in zip(axes.ravel(), panels):
        for key, lab, col, ls, mk in fam:
            s = df[df.family == key].sort_values("q")
            ax.plot(s.q, s[m], color=col, lw=1.0, ls=ls, marker=mk, ms=2.2, label=lab, zorder=3)
            if m == "BPAC":
                ax.fill_between(s.q, s[f"{m}_lo"], s[f"{m}_hi"], color=col, alpha=0.12, lw=0, zorder=2)
                qs = sel.loc[key, "q_selected_on_training"]
                ax.plot([qs], [s.set_index("q").loc[qs, m]], marker=mk, ms=5.5, mfc="white", mec=col, mew=1.1,
                        zorder=4, ls="none")
        ax.set_title(title, loc="left", color=INK)
        ax.grid(axis="y", color=GRID, lw=0.4)
        ax.set_xlim(0.295, 0.505)
    for ax in axes[1]:
        ax.set_xlabel("Quantile q")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.05, 1, 1), h_pad=0.8, w_pad=1.0)
    save(fig, "Figure2_quantile_path")


if __name__ == "__main__":
    figure1()
    figure2()
