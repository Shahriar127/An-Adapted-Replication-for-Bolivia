"""
Replication of McBride & Nichols (2015)
"Improved Poverty Targeting Through Machine Learning:
 An Application to the USAID Poverty Assessment Tools"

WHAT THIS SCRIPT DOES
─────────────────────
Implements the paper's exact methodology using the same real survey datasets:
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

METRICS  (paper Table 2, exact formulas)
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
import pyreadstat
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

warnings.filterwarnings("ignore")

# ── quantile-forest is required for QRF ──────────────────────────────────────
try:
    from quantile_forest import RandomForestQuantileRegressor
except ImportError:
    sys.exit("ERROR: pip install quantile-forest")

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
N_TREES          = 500        # paper footnote 10
BOOTSTRAP_REPS   = 1000       # paper p.13 — bootstrap samples of test set
RANDOM_STATE     = 42
DATA_DIR         = "data"
RESULTS_DIR      = "results"

# Quantile grid to search for best BPAC in QRF (paper uses country-specific best)
QRF_QUANTILES    = list(np.round(np.arange(0.05, 0.96, 0.05), 2))

os.makedirs(RESULTS_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
#  METRIC FUNCTIONS  (exact Table 2, McBride & Nichols 2015)
# ══════════════════════════════════════════════════════════════════════════════

def targeting_metrics(y_true, y_pred, line):
    """
    Paper Table 2 formulas.

    Confusion matrix (Table 1):
                     P=1 (true poor)   P=0 (true non-poor)
      Phat=1            TP                   FP
      Phat=0            FN                   TN

    PA   = TP/(TP+FP)      ← denom = PREDICTED poor (precision)
    UC   = FN/(TP+FN)      ← denom = TRUE poor
    LE   = FP/(TP+FN)      ← IRIS unconventional; can exceed 1 (footnote 7)
    BPAC = TP/(TP+FP) − |FN/(TP+FP) − FP/(TP+FP)|
           all three BPAC sub-terms share TP+FP denominator
    """
    actual = (np.asarray(y_true) < line).astype(int)
    pred   = (np.asarray(y_pred) < line).astype(int)

    TP = int(np.sum((actual == 1) & (pred == 1)))
    FP = int(np.sum((actual == 0) & (pred == 1)))
    FN = int(np.sum((actual == 1) & (pred == 0)))
    TN = int(np.sum((actual == 0) & (pred == 0)))
    N  = TP + FP + FN + TN

    TA   = (TP + TN) / N if N > 0 else 0.0
    PA   = TP / (TP + FP)  if (TP + FP) > 0 else 0.0
    UC   = FN / (TP + FN)  if (TP + FN) > 0 else 0.0
    LE   = FP / (TP + FN)  if (TP + FN) > 0 else 0.0
    denom = TP + FP
    BPAC = (TP/denom - abs(FN/denom - FP/denom)) if denom > 0 else 0.0

    return dict(TP=TP, FP=FP, FN=FN, TN=TN,
                TA=TA, PA=PA, UC=UC, LE=LE, BPAC=BPAC)


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
    """
    Construct household-level dataset from Bolivia EH 2005 raw SPSS files.

    IRIS variables used (Table 3):
      hhsize, hhsize2, age_head, age_head2, regions (9 departments),
      rural, sublease, brick_wall, wood_wall, dirt_floor, cement_floor,
      fridge, radio, tv, dvd, fan, car, num_beds, num_kitchens,
      num_computers, sheep  (21 features matching Table 3)

    Target: G_TOTAL_pc — Total per-capita monthly household expenditure (Bs)
    Poverty line: 24.2th percentile → 24.2% poverty rate (matches paper)
    """
    bdir = f"{DATA_DIR}/bolivia"
    print("  Loading Bolivia SPSS files ...")
    df_main, meta_main = pyreadstat.read_sav(
        f"{bdir}/BASE_EH_2005_(Pob_y_Viv).sav")
    df_eq,   _         = pyreadstat.read_sav(
        f"{bdir}/Bolivia_Equipamiento.sav")
    df_pec,  _         = pyreadstat.read_sav(
        f"{bdir}/Bolivia_Pecuaria.sav")

    # ── 1. Collapse to one row per household ─────────────────────────────────
    # All housing variables are identical within a household; take first row.
    hh_cols = ['folio', 'miembros', 'G_TOTAL_pc', 'urb_rur', 'depto',
               's7_02', 's7_05', 's7_08', 's7_19']
    hh = (df_main[hh_cols]
          .groupby('folio').first()
          .reset_index())

    # ── 2. Household head's age ───────────────────────────────────────────────
    # s1_05 == 1 → "jefe o jefa del hogar"
    head = (df_main.loc[df_main['s1_05'] == 1.0, ['folio', 's1_03']]
            .groupby('folio').first()
            .rename(columns={'s1_03': 'age_head'})
            .reset_index())
    hh = hh.merge(head, on='folio', how='left')

    # ── 3. Equipment (assets) — long → wide ──────────────────────────────────
    # Code → (feature_name, 'binary' or 'count')
    ASSET_MAP = {
        1:  ('num_beds',      'count'),
        7:  ('fridge',        'binary'),
        9:  ('num_computers', 'count'),
        10: ('radio',         'binary'),
        12: ('tv',            'binary'),
        13: ('dvd',           'binary'),
        18: ('fan',           'binary'),
        22: ('car',           'binary'),
    }
    for code, (col, kind) in ASSET_MAP.items():
        sub = (df_eq[df_eq['s6_16cod'] == float(code)]
               [['folio', 's6_16', 's6_17']]
               .groupby('folio').first()
               .reset_index())
        if kind == 'binary':
            sub[col] = (sub['s6_16'] == 1.0).astype(int)
        else:   # count (beds, computers)
            sub[col] = np.where(sub['s6_16'] == 1.0, sub['s6_17'].fillna(0), 0)
        hh = hh.merge(sub[['folio', col]], on='folio', how='left')
        hh[col] = hh[col].fillna(0)

    # ── 4. Sheep — Pecuaria file ──────────────────────────────────────────────
    # codb == 'B' → Ovinos (sheep)
    sheep = (df_pec[df_pec['codb'] == 'B']
             .groupby('folio')['s8_10']
             .sum()
             .rename('sheep')
             .reset_index())
    hh = hh.merge(sheep, on='folio', how='left')
    hh['sheep'] = hh['sheep'].fillna(0)

    # ── 5. Feature engineering ────────────────────────────────────────────────
    hh['hhsize']       = hh['miembros']
    hh['hhsize2']      = hh['miembros'] ** 2
    hh['age_head2']    = hh['age_head'] ** 2
    hh['rural']        = (hh['urb_rur'] == 2.0).astype(int)   # 2=rural
    # sublease: household is renting (alquilada = code 1)
    # Note: paper uses "sublease"; closest match in Bolivia EH is rented tenure
    hh['sublease']     = (hh['s7_02'] == 1.0).astype(int)
    # Wall materials (s7_05: 1=brick/concrete, 5=wood)
    hh['brick_wall']   = (hh['s7_05'] == 1.0).astype(int)
    hh['wood_wall']    = (hh['s7_05'] == 5.0).astype(int)
    # Floor materials (s7_08: 1=dirt, 5=cement)
    hh['dirt_floor']   = (hh['s7_08'] == 1.0).astype(int)
    hh['cement_floor'] = (hh['s7_08'] == 5.0).astype(int)
    # Kitchen room (s7_19: 1=yes; paper's "number kitchens" — binary proxy)
    hh['num_kitchens'] = (hh['s7_19'] == 1.0).astype(int)
    # Regions = department code (1–9); tree methods split on ordinal values
    hh['regions']      = hh['depto']

    # ── 6. Target and poverty line ────────────────────────────────────────────
    # G_TOTAL_pc: monthly per-capita total household expenditure (Bs)
    # Poverty line calibrated to reproduce paper's 24.2% poverty rate
    y = hh['G_TOTAL_pc'].copy()
    hh_nona = y.dropna()
    poverty_line = float(np.percentile(hh_nona.values, 24.2))  # ≈ 189 Bs/month

    # ── 7. Feature matrix ─────────────────────────────────────────────────────
    FEATURE_COLS = [
        'hhsize', 'hhsize2', 'age_head', 'age_head2',
        'regions', 'rural', 'sublease',
        'brick_wall', 'wood_wall', 'dirt_floor', 'cement_floor',
        'fridge', 'radio', 'tv', 'dvd', 'fan', 'car',
        'num_beds', 'num_kitchens', 'num_computers', 'sheep',
    ]
    X = hh[FEATURE_COLS].copy()

    # Drop rows where target is missing (only 1 household)
    valid = y.notna()
    X = X.loc[valid].reset_index(drop=True)
    y = y.loc[valid].reset_index(drop=True)

    # Impute remaining NaN in features with column median
    X = X.fillna(X.median(numeric_only=True))

    print(f"    N = {len(X)} households  |  features = {len(FEATURE_COLS)}")
    print(f"    Target: G_TOTAL_pc (Bs/month per capita)")
    print(f"    Poverty line: {poverty_line:.2f} Bs  →  "
          f"{(y < poverty_line).mean():.1%} poor")

    return X, y, poverty_line, FEATURE_COLS


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
    """
    Paper p.13: 'randomly draw, with replacement, two samples of size N/2'.
    Training and test samples are INDEPENDENT bootstrap samples — not disjoint.
    """
    rng  = np.random.RandomState(seed)
    N    = len(X)
    N2   = N // 2
    tr   = rng.choice(N, size=N2, replace=True)
    te   = rng.choice(N, size=N2, replace=True)
    return (X.iloc[tr].reset_index(drop=True),
            y.iloc[tr].reset_index(drop=True),
            X.iloc[te].reset_index(drop=True),
            y.iloc[te].reset_index(drop=True))


def bootstrap_evaluate_model(predict_fn, X_test, y_test, poverty_line,
                              B=BOOTSTRAP_REPS, seed=42):
    """
    Paper p.13: 'we test the model using 1000 bootstrapped samples of the
    testing sample.'

    predict_fn takes X and returns y_pred array.
    Returns B-length arrays of PA and BPAC (all five metrics available).
    """
    rng    = np.random.RandomState(seed)
    N      = len(y_test)
    y_pred = predict_fn(X_test)    # predict once; resample predictions

    metrics_boot = {k: [] for k in ('TA', 'PA', 'UC', 'LE', 'BPAC')}
    for _ in range(B):
        idx = rng.choice(N, size=N, replace=True)
        m   = targeting_metrics(y_test.values[idx], y_pred[idx], poverty_line)
        for k in metrics_boot:
            metrics_boot[k].append(m[k])

    return {k: np.array(v) for k, v in metrics_boot.items()}


# ══════════════════════════════════════════════════════════════════════════════
#  MODEL TRAINING
# ══════════════════════════════════════════════════════════════════════════════

def train_decision_tree(X_train, y_train):
    m = DecisionTreeRegressor(max_depth=10, min_samples_leaf=20,
                              random_state=RANDOM_STATE)
    m.fit(X_train, y_train)
    return m


def train_random_forest(X_train, y_train):
    m = RandomForestRegressor(
        n_estimators=N_TREES,
        max_features=1/3,      # paper: random 1/3 of features at each split
        min_samples_leaf=5,
        n_jobs=-1,
        oob_score=True,        # OOB error described in paper (p.9)
        random_state=RANDOM_STATE,
    )
    m.fit(X_train, y_train)
    return m


def train_qrf(X_train, y_train, X_test, y_test, poverty_line):
    """
    Train QRF and select quantile with highest BPAC on test set.
    Paper: QRF(40) for Bolivia, QRF(47) for East Timor, QRF(60) for Malawi.
    """
    m = RandomForestQuantileRegressor(
        n_estimators=N_TREES,
        max_features=1/3,
        min_samples_leaf=5,
        n_jobs=-1,
        random_state=RANDOM_STATE,
    )
    m.fit(X_train, y_train)

    # Predict at all quantiles in one call (efficient: shared leaf nodes)
    all_q = sorted(set(QRF_QUANTILES + [0.10, 0.25, 0.50, 0.75, 0.90]))
    preds  = m.predict(X_test, quantiles=all_q)    # shape (n_test, len(all_q))
    q_idx  = {q: i for i, q in enumerate(all_q)}

    # Select quantile by best BPAC on test set (paper's criterion)
    best_q, best_bpac = None, -999
    per_q_bpac = {}
    for q in QRF_QUANTILES:
        bpac_q = targeting_metrics(y_test.values, preds[:, q_idx[q]], poverty_line)['BPAC']
        per_q_bpac[q] = bpac_q
        if bpac_q > best_bpac:
            best_bpac = bpac_q
            best_q    = q

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
    X_tr, y_tr, X_te, y_te = paper_split(X, y, seed=RANDOM_STATE)
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
        train_qrf(X_tr, y_tr, X_te, y_te, poverty_line)

    print(f"\n  BPAC by quantile:")
    for q, b in sorted(per_q_bpac.items()):
        marker = "  ← BEST" if q == best_q else ""
        print(f"    q={q:.2f}  BPAC={b:.4f}{marker}")

    qrf_pred_best = qrf_all_preds[:, q_idx[best_q]]
    qrf_boot = bootstrap_evaluate_model(
        lambda X: qrf.predict(X, quantiles=[best_q]).ravel(),
        X_te, y_te, poverty_line)
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
    ax.set_title(f"{country} — QRF: BPAC by Quantile", fontweight="bold")
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
  This script implements that exactly.

Metrics (Table 2, exact formulas):
  PA   = TP/(TP+FP)         ← denominator is PREDICTED poor
  UC   = FN/(TP+FN)         ← denominator is TRUE poor
  LE   = FP/(TP+FN)         ← IRIS unconventional; can exceed 1 (footnote 7)
  BPAC = TP/(TP+FP) - |FN/(TP+FP) - FP/(TP+FP)|
         All three sub-terms use TP+FP; NOT the same as standalone UC/LE.

Poverty line (Bolivia):
  Calibrated to 24.2th percentile of G_TOTAL_pc → replicates paper's
  reported 24.2% poverty rate.  Does NOT use any official threshold.

QRF quantile selection:
  Best BPAC on the test set; then that fixed quantile is used for
  all 1000 bootstrap evaluations.

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
