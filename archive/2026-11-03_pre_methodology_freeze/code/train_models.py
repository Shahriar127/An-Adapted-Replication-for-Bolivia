"""
Replication of McBride & Nichols (2015)
"Improved Poverty Targeting Through Machine Learning:
 An Application to the USAID Poverty Assessment Tools"

WHAT THIS SCRIPT DOES
─────────────────────
Adapted replication of the paper's methodology (reconstructed poverty threshold,
documented implementation choices) using the same survey datasets:
  • Bolivia   — 2005 Encuesta de Hogares (EH2005) — DOWNLOADED AUTOMATICALLY
  • East Timor — 2001 Living Standards Survey (TLSS) — manual download required
  • Malawi    — 2004-2005 Second Integrated Household Survey (IHS2) — manual download

SPLIT STRATEGY (paper p. 13)
  Draw WITH REPLACEMENT two bootstrap samples of size N/2 from each country's data.
  One is the training sample; the other is the test sample.
  Evaluate on 1000 bootstrapped re-draws of the test sample.

MODELS  (paper p. 7–10)
  1. Regression Tree (Decision Tree Regressor)
  2. Random Forest  — 500 trees, 1/3 features per split
  3. Quantile Regression Forest — 500 trees; quantile selected by BPAC

METRICS  (paper Table 2 formulas)
  PA   = TP / (TP+FP)                 denominator = predicted poor
  UC   = FN / (TP+FN)                 denominator = true poor
  LE   = FP / (TP+FN)                 IRIS unconventional; can exceed 1
  BPAC = TP/(TP+FP) − |FN/(TP+FP) − FP/(TP+FP)|   all terms share TP+FP
"""

import os, warnings, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import common as C

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION — imported from common.py (shared with replication_report.py)
# ══════════════════════════════════════════════════════════════════════════════
N_TREES          = C.N_TREES
BOOTSTRAP_REPS   = C.BOOTSTRAP_REPS
RANDOM_STATE     = C.RANDOM_STATE
RESULTS_DIR      = C.RESULTS_DIR
QRF_QUANTILES    = C.QRF_QUANTILE_GRID

os.makedirs(RESULTS_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
#  METRIC FUNCTIONS  (Table 2, McBride & Nichols 2015)
# ══════════════════════════════════════════════════════════════════════════════

targeting_metrics = C.targeting_metrics   # paper Table 2 (see common.py)


def bootstrap_ci(samples, alpha=0.05):
    lo = np.percentile(samples, 100 * alpha / 2)
    hi = np.percentile(samples, 100 * (1 - alpha / 2))
    return lo, hi


def regression_metrics(y_true, y_pred):
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae  = float(mean_absolute_error(y_true, y_pred))
    r2   = float(r2_score(y_true, y_pred))
    return dict(RMSE=rmse, MAE=mae, R2=r2)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA PREPARATION
# ══════════════════════════════════════════════════════════════════════════════

def load_bolivia():
    """Bolivia EH 2005 — see common.build_household_frame for the variable
    mapping. Poverty line = 24.2th percentile of G_TOTAL_pc (≈189.09 Bs)."""
    print("  Loading Bolivia SPSS files ...")
    X, y, poverty_line = C.load_bolivia()
    return X, y, poverty_line, list(C.FEATURE_COLS)


def load_timor_leste():
    """
    Load East Timor TLSS 2001.
    Download from: https://microdata.worldbank.org/index.php/catalog/75
    (free registration required)

    Expected files in data/timor_leste/:
      Place the downloaded .dta or .sav files here.
      Reference ID: TLS_2001_TLSS_v01_M
      N = 1,800 households, poverty rate = 44.7%

    IRIS variables (Table 3):
      hhsize, hhsize2, age_head, age_head2, regions, rattantin_wall, leaf_roof,
      tile_roof, num_rooms, private_water, shared_water, bowl_toilet,
      electricity_light, private_light, fan, adults_who_read, farmland,
      num_axes, num_baskets, num_chickens

    Once files are present, implement analogously to load_bolivia().
    """
    raise NotImplementedError(
        "\n  East Timor TLSS 2001 data not found.\n"
        "  Download steps:\n"
        "    1. Register (free) at https://microdata.worldbank.org\n"
        "    2. Search catalog ID: TLS_2001_TLSS_v01_M\n"
        "    3. Request access → download files\n"
        "    4. Place .dta/.sav files in data/timor_leste/\n"
        "    5. Implement load_timor_leste() following load_bolivia() pattern"
    )


def load_malawi():
    """
    Load Malawi IHS2 2004-2005.
    Download from: https://microdata.worldbank.org/index.php/catalog/2307
    (free registration + Data Access Agreement required)

    Expected files in data/malawi/:
      Reference ID: MWI_2004_IHS-II_v01_M
      N = 11,280 households, poverty rate = 90.4%

    IRIS variables (Table 3):
      hhsize, hhsize2, age_head, age_head2, regions, rural, never_married,
      share_adults_no_education, share_adults_who_read, num_rooms, cement_floor,
      electricity, flush_toilet, soap, bed, bike, music_player, coffee_table,
      iron, garden, goats

    Once files are present, implement analogously to load_bolivia().
    """
    raise NotImplementedError(
        "\n  Malawi IHS2 2004-2005 data not found.\n"
        "  Download steps:\n"
        "    1. Register (free) at https://microdata.worldbank.org\n"
        "    2. Search: 'MWI_2004_IHS-II_v01_M'\n"
        "    3. Complete Data Access Agreement → download files\n"
        "    4. Place files in data/malawi/\n"
        "    5. Implement load_malawi() following load_bolivia() pattern"
    )


DATA_LOADERS = {
    "Bolivia":    load_bolivia,
    "East Timor": load_timor_leste,
    "Malawi":     load_malawi,
}


# ══════════════════════════════════════════════════════════════════════════════
#  PAPER'S SPLIT STRATEGY
# ══════════════════════════════════════════════════════════════════════════════

def paper_split(X, y, seed):
    """Paper p.13: two INDEPENDENT N/2 draws with replacement (overlapping)."""
    tr, te = C.paper_split_idx(len(X), seed)
    return (X.iloc[tr].reset_index(drop=True), y.iloc[tr].reset_index(drop=True),
            X.iloc[te].reset_index(drop=True), y.iloc[te].reset_index(drop=True),
            tr)


def bootstrap_evaluate_model(predict_fn, X_test, y_test, poverty_line):
    """1000 bootstrap re-draws of the test sample; identical indices for every
    model (C.BOOT_SEED) so model comparisons are paired."""
    y_pred = np.asarray(predict_fn(X_test))
    idx = C.boot_indices(len(y_test))
    return C.bootstrap_metrics(y_test.values, y_pred, poverty_line, idx)


# ══════════════════════════════════════════════════════════════════════════════
#  MODEL TRAINING
# ══════════════════════════════════════════════════════════════════════════════

def train_decision_tree(X_train, y_train):
    return C.make_model("DecisionTree").fit(X_train, y_train)


def train_random_forest(X_train, y_train):
    m = C.make_model("RandomForest")
    m.set_params(oob_score=True)          # OOB error described in paper (p.9)
    return m.fit(X_train, y_train)


def train_qrf(X_train, y_train, X_test, poverty_line, groups):
    """Train QRF; select the quantile by 5-fold CV BPAC on the TRAINING sample
    only (honest — the test set is never used for selection).
    Paper: QRF(40) for Bolivia, QRF(47) East Timor, QRF(60) Malawi."""
    m = C.make_model("QRF").fit(X_train, y_train)
    best_q, per_q_bpac = C.select_quantile_cv(X_train.values, y_train.values,
                                              poverty_line, groups=groups)
    all_q = sorted(set(QRF_QUANTILES + [0.10, 0.25, 0.50, 0.75, 0.90]))
    preds = m.predict(X_test, quantiles=all_q)
    q_idx = {q: i for i, q in enumerate(all_q)}
    return m, best_q, per_q_bpac, preds, all_q, q_idx


# ══════════════════════════════════════════════════════════════════════════════
#  PRINT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def print_boot_results(name, boot_metrics, reg_m=None):
    """Print bootstrap mean ± 95% CI for each metric."""
    print(f"\n{'─'*60}")
    print(f"  {name}")
    print(f"{'─'*60}")
    if reg_m:
        print(f"  Regression (point estimate on test set):")
        print(f"    RMSE={reg_m['RMSE']:.2f}  MAE={reg_m['MAE']:.2f}  R²={reg_m['R2']:.4f}")
    print(f"  Targeting metrics  (mean ± 95% CI over {BOOTSTRAP_REPS} bootstrap samples):")
    for k in ('TA', 'PA', 'UC', 'LE', 'BPAC'):
        samples = boot_metrics[k]
        lo, hi  = bootstrap_ci(samples)
        symbol  = "↑" if k in ('TA', 'PA', 'BPAC') else "↓"
        print(f"    {k:<5s}  {np.mean(samples):.4f}  [{lo:.4f}, {hi:.4f}]  {symbol}")


# ══════════════════════════════════════════════════════════════════════════════
#  PER-COUNTRY PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def run_country(country, load_fn):
    print(f"\n{'═'*60}")
    print(f"  COUNTRY: {country.upper()}")
    print(f"{'═'*60}")

    os.makedirs(f"{RESULTS_DIR}/{country}", exist_ok=True)

    # ── Load data ─────────────────────────────────────────────────────────────
    X, y, poverty_line, feature_cols = load_fn()
    N = len(X)
    print(f"\n  Full dataset: N={N}  |  poverty_line={poverty_line:.2f}  |  "
          f"poverty_rate={( y < poverty_line).mean():.1%}")

    # ── Paper's split ─────────────────────────────────────────────────────────
    X_tr, y_tr, X_te, y_te, tr_ids = paper_split(X, y, seed=RANDOM_STATE)
    C.save_config(f"{RESULTS_DIR}/{country}/config.json")
    print(f"  Train={len(X_tr)}  Test={len(X_te)}  "
          f"(N/2 bootstrap samples with replacement, seed={RANDOM_STATE})")

    results = {}   # store bootstrap metrics + predictions for each model

    # ── Decision Tree ─────────────────────────────────────────────────────────
    print(f"\n  [1/3] Decision Tree ...")
    dt = train_decision_tree(X_tr, y_tr)
    dt_pred_te = dt.predict(X_te)
    dt_boot = bootstrap_evaluate_model(
        lambda X: dt.predict(X), X_te, y_te, poverty_line)
    dt_reg  = regression_metrics(y_te, dt_pred_te)
    print_boot_results("Decision Tree", dt_boot, dt_reg)
    results["Decision Tree"] = dict(boot=dt_boot, reg=dt_reg, pred=dt_pred_te)

    # ── Random Forest ─────────────────────────────────────────────────────────
    print(f"\n  [2/3] Random Forest  ({N_TREES} trees) ...")
    rf = train_random_forest(X_tr, y_tr)
    rf_pred_te = rf.predict(X_te)
    rf_boot = bootstrap_evaluate_model(
        lambda X: rf.predict(X), X_te, y_te, poverty_line)
    rf_reg  = regression_metrics(y_te, rf_pred_te)
    print_boot_results("Random Forest", rf_boot, rf_reg)
    print(f"    OOB R² = {rf.oob_score_:.4f}")
    results["Random Forest"] = dict(boot=rf_boot, reg=rf_reg, pred=rf_pred_te)

    # Feature importance
    fi = pd.Series(rf.feature_importances_,
                   index=feature_cols).sort_values(ascending=False)
    print(f"\n  Feature importances (RF):")
    for feat, imp in fi.items():
        bar = "█" * int(imp * 50)
        print(f"    {feat:<22s}  {imp:.4f}  {bar}")

    # ── QRF ───────────────────────────────────────────────────────────────────
    print(f"\n  [3/3] QRF  ({N_TREES} trees) — quantile search ...")
    qrf, best_q, per_q_bpac, qrf_all_preds, all_q, q_idx = \
        train_qrf(X_tr, y_tr, X_te, poverty_line, tr_ids)

    print(f"\n  BPAC by quantile (5-fold CV on training sample):")
    for q, b in sorted(per_q_bpac.items()):
        marker = "  ← BEST" if q == best_q else ""
        print(f"    q={q:.2f}  BPAC={b:.4f}{marker}")

    qrf_pred_best = qrf_all_preds[:, q_idx[best_q]]
    qrf_boot = bootstrap_evaluate_model(
        lambda X: qrf_pred_best, X_te, y_te, poverty_line)
    qrf_reg  = regression_metrics(y_te, qrf_pred_best)
    print_boot_results(f"QRF (q={best_q:.2f})", qrf_boot, qrf_reg)

    # Prediction intervals (10th–90th)
    p10 = qrf_all_preds[:, q_idx[0.10]]
    p90 = qrf_all_preds[:, q_idx[0.90]]
    coverage  = float(np.mean((y_te.values >= p10) & (y_te.values <= p90)))
    avg_width = float(np.mean(p90 - p10))
    print(f"\n    10–90% interval: coverage={coverage:.1%}  avg_width={avg_width:.1f}")
    results["QRF"] = dict(boot=qrf_boot, reg=qrf_reg, pred=qrf_pred_best,
                          best_q=best_q, p10=p10, p90=p90,
                          coverage=coverage, avg_width=avg_width)

    # ── Comparison table ──────────────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print(f"  COMPARISON TABLE — {country}")
    print(f"{'═'*60}")
    rows = []
    for name, res in results.items():
        label = name if "QRF" not in name else f"QRF (q={res['best_q']:.2f})"
        r = {
            "Model": label,
            "RMSE":  round(res["reg"]["RMSE"], 2),
            "MAE":   round(res["reg"]["MAE"],  2),
            "R²":    round(res["reg"]["R2"],    4),
        }
        for m in ("PA", "UC", "LE", "BPAC"):
            samples = res["boot"][m]
            lo, hi  = bootstrap_ci(samples)
            r[m]              = round(np.mean(samples), 4)
            r[f"{m}_CI_lo"]   = round(lo, 4)
            r[f"{m}_CI_hi"]   = round(hi, 4)
        rows.append(r)

    comp_df = pd.DataFrame(rows)
    display_cols = ["Model", "RMSE", "MAE", "R²", "PA", "UC", "LE", "BPAC"]
    print(comp_df[display_cols].to_string(index=False))
    comp_df.to_csv(f"{RESULTS_DIR}/{country}/model_comparison.csv", index=False)

    # Save all predictions
    pd.DataFrame({
        "y_true":       y_te.values,
        "actual_poor":  (y_te.values < poverty_line).astype(int),
        "dt_pred":      results["Decision Tree"]["pred"],
        "rf_pred":      results["Random Forest"]["pred"],
        "qrf_pred":     results["QRF"]["pred"],
        "qrf_p10":      results["QRF"]["p10"],
        "qrf_p90":      results["QRF"]["p90"],
    }).to_csv(f"{RESULTS_DIR}/{country}/predictions.csv", index=False)

    # Confusion matrices on the full test sample (point estimate)
    cm = []
    for name, res in results.items():
        label = name if name != "QRF" else f"QRF (q={res['best_q']:.2f})"
        m = targeting_metrics(y_te.values, res["pred"], poverty_line)
        cm.append({"Model": label, **{k: m[k] for k in ("TP", "FP", "FN", "TN")}})
    pd.DataFrame(cm).to_csv(f"{RESULTS_DIR}/{country}/confusion_matrices.csv",
                            index=False)

    # ── Visualisations ────────────────────────────────────────────────────────
    _make_plots(country, results, y_te, poverty_line, fi, per_q_bpac, best_q,
                coverage, avg_width)

    print(f"\n  Saved results → {RESULTS_DIR}/{country}/")
    return comp_df


def _make_plots(country, results, y_te, poverty_line, fi,
                per_q_bpac, best_q, coverage, avg_width):
    """Generate and save all plots for one country."""
    plt.rcParams.update({"figure.dpi": 120, "font.size": 9})
    COLORS = {"Decision Tree": "#e07b54",
              "Random Forest": "#4e8fa2",
              "QRF":           "#6dab6d"}

    # ── 1. Bootstrap distribution of PA and BPAC ──────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(f"{country} — Bootstrap Distributions (B={BOOTSTRAP_REPS})\n"
                 "Vertical dashed = mean; error bars = 95% CI",
                 fontweight="bold")
    for ax, metric in zip(axes, ["PA", "BPAC"]):
        direction = "↑ higher = better"
        ax.set_title(f"{metric}  ({direction})")
        for i, (name, res) in enumerate(results.items()):
            color  = COLORS.get(name.split(" (")[0].replace("QRF","QRF"), "#888")
            label  = name if "QRF" not in name else f"QRF (q={res['best_q']:.2f})"
            s = res["boot"][metric]
            ax.hist(s, bins=40, alpha=0.5, color=list(COLORS.values())[i],
                    label=label, density=True)
            ax.axvline(s.mean(), color=list(COLORS.values())[i],
                       linestyle="--", lw=1.5)
        ax.set_xlabel(metric)
        ax.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{country}/bootstrap_distributions.png",
                bbox_inches="tight")
    plt.close()

    # ── 2. Mean metric comparison with CIs ────────────────────────────────────
    metric_specs = [("PA",   True,  "Poverty Accuracy\n↑ better"),
                    ("UC",   False, "Undercoverage\n↓ better"),
                    ("LE",   False, "Leakage (IRIS)\n↓ better"),
                    ("BPAC", True,  "BPAC\n↑ better")]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    fig.suptitle(f"{country} — Targeting Metrics  (mean ± 95% CI,  B={BOOTSTRAP_REPS})",
                 fontweight="bold")
    for ax, (m, _, label) in zip(axes, metric_specs):
        ax.set_title(label, fontsize=8)
        for i, (name, res) in enumerate(results.items()):
            samples = res["boot"][m]
            mean    = samples.mean()
            lo, hi  = bootstrap_ci(samples)
            color   = list(COLORS.values())[i]
            ax.bar(i, mean, color=color, alpha=0.8)
            ax.errorbar(i, mean, yerr=[[mean - lo], [hi - mean]],
                        fmt="none", color="black", capsize=4, lw=1.5)
            ax.text(i, hi + 0.005, f"{mean:.3f}", ha="center",
                    fontsize=7, va="bottom")
        short_labels = [n.split(" (")[0] for n in results.keys()]
        ax.set_xticks(range(len(short_labels)))
        ax.set_xticklabels(short_labels, fontsize=7, rotation=10)
        ax.set_ylim(0, 1.1)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{country}/targeting_metrics.png", bbox_inches="tight")
    plt.close()

    # ── 3. Feature importance ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    fi_s = fi.sort_values()
    colors = ["#4e8fa2" if v >= fi_s.median() else "#a8cdd9"
              for v in fi_s.values]
    fi_s.plot(kind="barh", ax=ax, color=colors)
    ax.set_title(f"{country} — Random Forest Feature Importance", fontweight="bold")
    ax.set_xlabel("Mean Decrease in Impurity")
    for i, v in enumerate(fi_s.values):
        ax.text(v + 0.001, i, f"{v:.3f}", va="center", fontsize=7)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{country}/feature_importance.png", bbox_inches="tight")
    plt.close()

    # ── 4. QRF BPAC by quantile ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 4))
    qs   = sorted(per_q_bpac.keys())
    bpacs = [per_q_bpac[q] for q in qs]
    ax.plot([int(q * 100) for q in qs], bpacs,
            marker="o", ms=4, color="#6dab6d", lw=1.5)
    ax.axvline(int(best_q * 100), color="red", lw=1.5, ls="--",
               label=f"Best q={int(best_q*100)} (BPAC={per_q_bpac[best_q]:.3f})")
    ax.set_xlabel("Quantile (%)")
    ax.set_ylabel("BPAC")
    ax.set_title(f"{country} — QRF: CV BPAC by Quantile (training data)", fontweight="bold")
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{country}/qrf_bpac_by_quantile.png",
                bbox_inches="tight")
    plt.close()

    # ── 5. QRF prediction intervals ───────────────────────────────────────────
    qrf_res = results["QRF"]
    fig, ax = plt.subplots(figsize=(11, 5))
    sort_idx = np.argsort(y_te.values)
    x_axis   = np.arange(len(sort_idx))
    ax.fill_between(x_axis, qrf_res["p10"][sort_idx], qrf_res["p90"][sort_idx],
                    alpha=0.3, color="#6dab6d", label="10–90% interval")
    ax.plot(x_axis, qrf_res["pred"][sort_idx],
            color="#2d6e2d", lw=1.2, label=f"QRF (q={qrf_res['best_q']:.2f})")
    ax.scatter(x_axis, y_te.values[sort_idx], s=6, color="black",
               alpha=0.3, label="Actual")
    ax.axhline(poverty_line, color="red", lw=1.2, ls="--",
               label=f"Poverty line = {poverty_line:.0f}")
    ax.set_xlabel("Households (sorted by actual)")
    ax.set_ylabel("Per-capita expenditure")
    ax.set_title(f"{country} — QRF Intervals  "
                 f"(coverage={coverage:.1%}, avg width={avg_width:.0f})",
                 fontweight="bold")
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{country}/qrf_intervals.png", bbox_inches="tight")
    plt.close()

    # ── 6. Actual vs predicted ────────────────────────────────────────────────
    model_preds = {
        "Decision Tree": results["Decision Tree"]["pred"],
        "Random Forest": results["Random Forest"]["pred"],
        f"QRF q={qrf_res['best_q']:.2f}": results["QRF"]["pred"],
    }
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"{country} — Actual vs Predicted", fontweight="bold")
    for ax, (nm, pred), color in zip(axes, model_preds.items(),
                                     COLORS.values()):
        r2 = r2_score(y_te, pred)
        lims = [min(y_te.min(), pred.min())-10,
                max(y_te.max(), pred.max())+10]
        ax.scatter(y_te, pred, alpha=0.25, s=10, color=color)
        ax.plot(lims, lims, "k--", lw=1)
        ax.axvline(poverty_line, color="red", lw=0.8, ls=":")
        ax.axhline(poverty_line, color="red", lw=0.8, ls=":")
        ax.set_xlim(lims); ax.set_ylim(lims)
        ax.set_title(f"{nm}\nR²={r2:.3f}")
        ax.set_xlabel("Actual"); ax.set_ylabel("Predicted")
    plt.tight_layout()
    plt.savefig(f"{RESULTS_DIR}/{country}/actual_vs_predicted.png",
                bbox_inches="tight")
    plt.close()

    print(f"  Plots saved: {RESULTS_DIR}/{country}/")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    all_results = {}

    for country, loader in DATA_LOADERS.items():
        try:
            comp_df = run_country(country, loader)
            all_results[country] = comp_df
        except NotImplementedError as e:
            print(f"\n{'─'*60}")
            print(f"  SKIPPING {country}:{e}")
            print(f"{'─'*60}")
        except FileNotFoundError as e:
            print(f"\n  SKIPPING {country} — data files not found: {e}")

    # ── Cross-country BPAC summary (if multiple countries available) ──────────
    if len(all_results) > 1:
        print(f"\n{'═'*60}")
        print("  CROSS-COUNTRY BPAC SUMMARY")
        print(f"{'═'*60}")
        for cty, df in all_results.items():
            row = df[["Model", "BPAC"]].to_string(index=False)
            print(f"  {cty}:")
            for line in row.split("\n"):
                print(f"    {line}")

    print(f"\n{'═'*60}")
    print("  METHODOLOGY NOTES")
    print(f"{'═'*60}")
    print(f"""
Split strategy:
  Paper:  Two independent bootstrap samples of size N/2 (WITH replacement).
          Test set evaluated on B={BOOTSTRAP_REPS} bootstrapped re-draws.
  This script follows that procedure. NB: train and test overlap (~40%
  of unique test households also appear in training).

Metrics (Table 2 formulas):
  PA   = TP/(TP+FP)         ← denominator is PREDICTED poor
  UC   = FN/(TP+FN)         ← denominator is TRUE poor
  LE   = FP/(TP+FN)         ← IRIS unconventional; can exceed 1 (footnote 7)
  BPAC = TP/(TP+FP) - |FN/(TP+FP) - FP/(TP+FP)|
         All three sub-terms use TP+FP; NOT the same as standalone UC/LE.

Poverty line (Bolivia):
  Calibrated to 24.2th percentile of G_TOTAL_pc (full sample, data-derived)
  → matches the paper's
  reported 24.2% poverty rate.  Does NOT use any official threshold.

QRF quantile selection:
  Best pooled out-of-fold BPAC from 5-fold CV on the TRAINING sample
  (households grouped so duplicates never straddle folds). The test
  set is never used for selection. See sensitivity_analysis.py for
  fixed QRF(40) vs QRF(45) and test-selected comparisons.

Configuration:
  All hyper-parameters, seeds and the split come from common.py and
  are written to results/<country>/config.json.

"num_kitchens" approximation:
  Paper lists "number kitchens" for Bolivia.  Bolivia EH 2005 only
  has a binary indicator (s7_19: dedicated kitchen room YES/NO).
  We use this binary as a proxy; a continuous count is not available.

"sublease" mapping:
  Paper's variable corresponds to rented tenure (s7_02==1, "alquilada").
  Bolivia EH 2005 does not distinguish renting from sub-leasing.

East Timor / Malawi:
  Datasets require free World Bank registration + download.
  Implement load_timor_leste() and load_malawi() once files are in place.
""")

    print(f"✓  Done.  Results in: {os.path.abspath(RESULTS_DIR)}")
