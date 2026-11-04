"""
common.py — single source of truth for the Bolivia EH 2005 replication.

Every methodological decision here is documented, with page references, in
METHODOLOGY_REFERENCE.md (frozen against McBride & Nichols 2018, WBER
32(3):531-550). Tags like [M3], [S7] and [F6] point to rows in that file.

Every script (train_models.py, replication_report.py, sensitivity_analysis.py)
imports data loading, model configuration, splitting, metrics and bootstrap
from here, so the report table and the model outputs are produced by the
same code path and the same configuration.
"""

import hashlib
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data", "bolivia")
RESULTS_DIR = os.path.join(HERE, "results")

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION (canonical — do not redefine in other scripts)
# ══════════════════════════════════════════════════════════════════════════════
RANDOM_STATE = 42          # model seed AND split seed (legacy np.random.RandomState)
BOOT_SEED = 42             # same bootstrap indices for every model (paired comparison)
BOOTSTRAP_REPS = 1000      # [S4] p.539
N_TREES = 500              # [F2] p.539, fn 10
POVERTY_RATE = 0.242       # [D8] p.538 text "24.2 percent" (Table 3 says 24.03: ambiguity A2)
QRF_QUANTILE_GRID = [round(float(q), 2) for q in np.arange(0.01, 1.00, 0.01)]   # [S8] 0.01 grid
QRF_QUANTILES_FOR_INTERVALS = (0.10, 0.90)
IRIS_QUANTILE = 0.42       # [S6] Table A1 row 2: IRIS QR(0.42) for Bolivia

MODEL_CONFIG = {
    # Paper does not report tree hyper-parameters; these are fixed a-priori
    # and shared by every script.
    "DecisionTree": dict(max_depth=10, min_samples_leaf=20),
    # [F3][F4][F5] R randomForest regression defaults: ntree=500, mtry=floor(p/3), nodesize=5
    "RandomForest": dict(n_estimators=N_TREES, max_features=1 / 3,
                         min_samples_leaf=5, oob_score=True),
    # [F6] Meinshausen QRF keeps ALL leaf observations -> max_samples_leaf=None
    "QRF": dict(n_estimators=N_TREES, max_features=1 / 3, min_samples_leaf=5,
                max_samples_leaf=None),
    "IRIS_QR": dict(quantile=IRIS_QUANTILE, alpha=0.0, solver="highs",
                    fit_intercept=True),   # + 8 region dummies (drop_first)
}

FEATURE_COLS = [
    "hhsize", "hhsize2", "age_head", "age_head2",
    "regions", "rural", "sublease",
    "brick_wall", "wood_wall", "dirt_floor", "cement_floor",
    "fridge", "radio", "tv", "dvd", "fan", "car",
    "num_beds", "num_kitchens", "num_computers", "sheep",
]

RAW_FILES = [
    "BASE_EH_2005_(Pob_y_Viv).sav",
    "Bolivia_Equipamiento.sav",
    "Bolivia_Pecuaria.sav",
]
RAW_ARCHIVE = "EH2005.rar"
DATA_SOURCE_URL = ("https://siip.produccion.gob.bo/repSIIP2/files/"
                   "encuesta_hogares/EH2005.rar")


def config_dict():
    """Configuration snapshot written next to every result set."""
    return dict(
        RANDOM_STATE=RANDOM_STATE, BOOT_SEED=BOOT_SEED,
        BOOTSTRAP_REPS=BOOTSTRAP_REPS, N_TREES=N_TREES,
        POVERTY_RATE=POVERTY_RATE, QRF_QUANTILE_GRID=QRF_QUANTILE_GRID,
        IRIS_QUANTILE=IRIS_QUANTILE,
        metric_denominator="TP+FN for PA, UC, LE, BPAC [M3-M6]",
        se_selection="best OOB BPAC on training sample over RF + QRF(grid) [S7][S8]",
        MODEL_CONFIG=MODEL_CONFIG, FEATURE_COLS=FEATURE_COLS,
        split="paper: two independent N/2 draws with replacement "
              "(np.random.RandomState(RANDOM_STATE); train drawn first)",
    )


def save_config(path):
    with open(path, "w") as f:
        json.dump(config_dict(), f, indent=2)


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


# ══════════════════════════════════════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════════════════════════════════════
ASSET_MAP = {
    1: ("num_beds", "count"),
    7: ("fridge", "binary"),
    9: ("num_computers", "count"),
    10: ("radio", "binary"),
    12: ("tv", "binary"),
    13: ("dvd", "binary"),
    18: ("fan", "binary"),
    22: ("car", "binary"),
}


def build_household_frame(df_main, df_eq, df_pec):
    """Person/asset/livestock files → one row per household (all features + target)."""
    hh_cols = ["folio", "miembros", "G_TOTAL_pc", "urb_rur", "depto",
               "s7_02", "s7_05", "s7_08", "s7_19"]
    hh = df_main[hh_cols].groupby("folio").first().reset_index()

    head = (df_main.loc[df_main["s1_05"] == 1.0, ["folio", "s1_03"]]
            .groupby("folio").first()
            .rename(columns={"s1_03": "age_head"}).reset_index())
    hh = hh.merge(head, on="folio", how="left")

    for code, (col, kind) in ASSET_MAP.items():
        sub = (df_eq[df_eq["s6_16cod"] == float(code)][["folio", "s6_16", "s6_17"]]
               .groupby("folio").first().reset_index())
        if kind == "binary":
            sub[col] = (sub["s6_16"] == 1.0).astype(int)
        else:
            sub[col] = np.where(sub["s6_16"] == 1.0, sub["s6_17"].fillna(0), 0)
        hh = hh.merge(sub[["folio", col]], on="folio", how="left")
        hh[col] = hh[col].fillna(0)

    sheep = (df_pec[df_pec["codb"] == "B"].groupby("folio")["s8_10"]
             .sum().rename("sheep").reset_index())
    hh = hh.merge(sheep, on="folio", how="left")
    hh["sheep"] = hh["sheep"].fillna(0)

    hh["hhsize"] = hh["miembros"]
    hh["hhsize2"] = hh["miembros"] ** 2
    hh["age_head2"] = hh["age_head"] ** 2
    hh["rural"] = (hh["urb_rur"] == 2.0).astype(int)
    hh["sublease"] = (hh["s7_02"] == 1.0).astype(int)
    hh["brick_wall"] = (hh["s7_05"] == 1.0).astype(int)
    hh["wood_wall"] = (hh["s7_05"] == 5.0).astype(int)
    hh["dirt_floor"] = (hh["s7_08"] == 1.0).astype(int)
    hh["cement_floor"] = (hh["s7_08"] == 5.0).astype(int)
    hh["num_kitchens"] = (hh["s7_19"] == 1.0).astype(int)
    hh["regions"] = hh["depto"]
    return hh


def load_raw():
    import pyreadstat
    df_main, meta = pyreadstat.read_sav(os.path.join(DATA_DIR, RAW_FILES[0]))
    df_eq, _ = pyreadstat.read_sav(os.path.join(DATA_DIR, RAW_FILES[1]))
    df_pec, _ = pyreadstat.read_sav(os.path.join(DATA_DIR, RAW_FILES[2]))
    return df_main, meta, df_eq, df_pec


def clean(hh):
    """Single missing-data rule for all scripts: drop rows with missing target or
    head age, then median-impute any remaining feature NaN."""
    out = hh.dropna(subset=["G_TOTAL_pc", "age_head"]).reset_index(drop=True)
    out[FEATURE_COLS] = out[FEATURE_COLS].fillna(
        out[FEATURE_COLS].median(numeric_only=True))
    return out


def load_bolivia(verbose=True):
    """Returns X (DataFrame), y (Series), poverty_line (float)."""
    df_main, _, df_eq, df_pec = load_raw()
    hh = clean(build_household_frame(df_main, df_eq, df_pec))
    X = hh[FEATURE_COLS].copy()
    y = hh["G_TOTAL_pc"].astype(float).copy()
    line = reconstructed_poverty_line(y)
    if verbose:
        print(f"    N = {len(X)} households | features = {len(FEATURE_COLS)}")
        print(f"    Poverty line: {line:.4f} Bs -> {(y < line).mean():.2%} poor")
    return X, y, line


def reconstructed_poverty_line(y):
    """24.2th percentile of per-capita expenditure (numpy 'linear' method).

    NB: this is DATA-DERIVED. When y is the full sample, the test households
    help define the threshold, so the test set is not fully untouched. Pass
    y[train] to get a train-derived threshold (see sensitivity_analysis.py)."""
    return float(np.percentile(np.asarray(y, dtype=float), POVERTY_RATE * 100))


# ══════════════════════════════════════════════════════════════════════════════
#  SPLITS
# ══════════════════════════════════════════════════════════════════════════════
def paper_split_idx(n, seed=RANDOM_STATE):
    """[S1] p.539: two INDEPENDENT N/2 draws with replacement. [S3] seed reconstructed.
    NB: train and test overlap (~40% of unique test households also appear in train)."""
    rng = np.random.RandomState(seed)
    tr = rng.choice(n, size=n // 2, replace=True)
    te = rng.choice(n, size=n // 2, replace=True)
    return tr, te


def disjoint_split_idx(n, seed=RANDOM_STATE):
    """ADAPTED (section 7): untouched-test protocol, random 50/50 partition, no shared households."""
    rng = np.random.RandomState(seed)
    perm = rng.permutation(n)
    return perm[: n // 2], perm[n // 2:]


# ══════════════════════════════════════════════════════════════════════════════
#  MODELS
# ══════════════════════════════════════════════════════════════════════════════
def make_model(name, seed=RANDOM_STATE):
    if name == "DecisionTree":
        from sklearn.tree import DecisionTreeRegressor
        return DecisionTreeRegressor(random_state=seed, **MODEL_CONFIG[name])
    if name == "RandomForest":
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(random_state=seed, n_jobs=-1,
                                     **MODEL_CONFIG[name])
    if name == "QRF":
        from quantile_forest import RandomForestQuantileRegressor
        return RandomForestQuantileRegressor(random_state=seed, n_jobs=-1,
                                             **MODEL_CONFIG[name])
    if name == "IRIS_QR":
        from sklearn.linear_model import QuantileRegressor
        return QuantileRegressor(**MODEL_CONFIG[name])
    raise ValueError(name)


def iris_design(X):
    """IRIS linear model design: regions as 8 dummies, Chuquisaca (depto=1)
    is the reference category (the model has an intercept). Keeping all 9
    dummies plus an intercept is rank-deficient (rank 29 of 30); we checked
    that it gives identical predictions, but its coefficients are not identified."""
    df = pd.DataFrame(X, columns=FEATURE_COLS)
    reg = df.pop("regions").astype(int)
    for r in range(2, 10):
        df[f"region_{r}"] = (reg == r).astype(float)
    return df.astype(float).values


# ══════════════════════════════════════════════════════════════════════════════
#  METRICS (paper Table 2)
# ══════════════════════════════════════════════════════════════════════════════
def confusion(y_true, y_pred, line):
    a = np.asarray(y_true) < line
    p = np.asarray(y_pred) < line
    TP = int(np.sum(a & p)); FP = int(np.sum(~a & p))
    FN = int(np.sum(a & ~p)); TN = int(np.sum(~a & ~p))
    return TP, FP, FN, TN


def metrics_from_counts(TP, FP, FN, TN):
    """Published Table 2 (p.534) [M2-M6]. Every rate except TA has the
    denominator TP+FN (the true very poor). BPAC = PA - |UC - LE|."""
    N = TP + FP + FN + TN
    t = TP + FN
    PA = TP / t if t else 0.0
    UC = FN / t if t else 0.0
    LE = FP / t if t else 0.0
    return dict(
        TP=TP, FP=FP, FN=FN, TN=TN,
        TA=(TP + TN) / N if N else 0.0,
        PA=PA, UC=UC, LE=LE,
        BPAC=(PA - abs(UC - LE)) if t else 0.0,    # [M8] t == 0 -> 0
    )


def targeting_metrics(y_true, y_pred, line):
    return metrics_from_counts(*confusion(y_true, y_pred, line))


METRICS = ("TA", "PA", "UC", "LE", "BPAC")


def boot_indices(n, B=BOOTSTRAP_REPS, seed=BOOT_SEED):
    """Same index matrix for every model/threshold → paired comparisons."""
    return np.random.RandomState(seed).randint(0, n, size=(B, n))


def bootstrap_metrics(y_true, y_pred, line, idx):
    """Vectorised bootstrap of Table-2 metrics. idx: (B, n) index matrix.
    Returns dict metric -> (B,) array."""
    a = (np.asarray(y_true) < line)[idx]
    p = (np.asarray(y_pred) < line)[idx]
    TP = (a & p).sum(1).astype(float); FP = (~a & p).sum(1).astype(float)
    FN = (a & ~p).sum(1).astype(float); TN = (~a & ~p).sum(1).astype(float)
    N = TP + FP + FN + TN
    t = TP + FN
    with np.errstate(divide="ignore", invalid="ignore"):
        PA = np.where(t > 0, TP / t, 0.0)
        UC = np.where(t > 0, FN / t, 0.0)
        LE = np.where(t > 0, FP / t, 0.0)
        out = dict(TA=(TP + TN) / N, PA=PA, UC=UC, LE=LE,
                   BPAC=np.where(t > 0, PA - np.abs(UC - LE), 0.0))
    return out


def ci(arr, alpha=0.05):
    return (float(np.percentile(arr, 100 * alpha / 2)),
            float(np.percentile(arr, 100 * (1 - alpha / 2))))


def summarise(boot):
    """dict metric -> (mean, lo, hi). [S4]"""
    return {k: (float(np.mean(v)), *ci(v)) for k, v in boot.items()}


def boot_se(boot):
    """dict metric -> bootstrap standard error (SD of replicates). [S4]"""
    return {k: float(np.std(v, ddof=1)) for k, v in boot.items()}


# ══════════════════════════════════════════════════════════════════════════════
#  STOCHASTIC-ENSEMBLE MODEL SELECTION  [S7][S8][S9][S10]
# ══════════════════════════════════════════════════════════════════════════════
def se_candidates(grid=QRF_QUANTILE_GRID):
    """Candidate labels, in tie-break order [S10]: RF first, then QRF by quantile."""
    return ["RF"] + [f"QRF({q:.2f})" for q in grid]


def se_oob_predictions(rf, qrf, X_tr, grid=QRF_QUANTILE_GRID):
    """Out-of-bag predictions on the TRAINING sample for every SE candidate.
    rf must be fitted with oob_score=True. OOB is per row [S9], as in R.
    Returns an (n_train, 1 + len(grid)) matrix whose columns follow se_candidates()."""
    oob_q = qrf.predict(np.asarray(X_tr), quantiles=list(grid), oob_score=True)
    return np.column_stack([rf.oob_prediction_, oob_q])


def select_se(y_tr, oob_preds, line, grid=QRF_QUANTILE_GRID):
    """[S7] Preferred SE model = highest OOB BPAC (= lowest BPAC error).
    Returns (label, column index, {label: BPAC})."""
    labels = se_candidates(grid)
    scores = {lab: targeting_metrics(y_tr, oob_preds[:, j], line)["BPAC"]
              for j, lab in enumerate(labels)}
    best = max(labels, key=lambda lab: scores[lab])    # first maximum wins [S10]
    return best, labels.index(best), scores


def se_test_predictions(rf, qrf, X_te, grid=QRF_QUANTILE_GRID):
    """Test predictions for every SE candidate, columns as se_candidates()."""
    X_te = np.asarray(X_te)
    return np.column_stack([rf.predict(X_te), qrf.predict(X_te, quantiles=list(grid))])


def best_quantile(y, preds, line, grid=QRF_QUANTILE_GRID):
    """Grid quantile with highest BPAC; preds has one column per grid quantile.
    The first maximum wins."""
    scores = {q: targeting_metrics(y, preds[:, j], line)["BPAC"]
              for j, q in enumerate(grid)}
    best = max(grid, key=lambda q: scores[q])
    return best, scores


def select_quantile_on_test(qrf, X_te, y_te, line, grid=QRF_QUANTILE_GRID):
    """OPTIMISTIC selection on the test sample itself (2015-draft practice).
    Used only to measure selection optimism, never as a primary result."""
    return best_quantile(y_te, qrf.predict(np.asarray(X_te), quantiles=list(grid)),
                         line, grid)
