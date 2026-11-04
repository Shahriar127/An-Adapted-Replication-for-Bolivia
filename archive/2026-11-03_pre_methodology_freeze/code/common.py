"""
common.py — single source of truth for the Bolivia EH 2005 replication.

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
BOOTSTRAP_REPS = 1000      # paper p.13
N_TREES = 500              # paper footnote 10
POVERTY_RATE = 0.242       # paper: Bolivia "very poor" rate
QRF_QUANTILE_GRID = [round(q, 2) for q in np.arange(0.05, 0.96, 0.05)]
QRF_QUANTILES_FOR_INTERVALS = (0.10, 0.90)
IRIS_QUANTILE = 0.42       # paper Table 4: IRIS Q(42) for Bolivia
CV_FOLDS = 5               # inner CV (training data only) for honest quantile selection

MODEL_CONFIG = {
    # Paper does not report tree hyper-parameters; these are fixed a-priori
    # and shared by every script.
    "DecisionTree": dict(max_depth=10, min_samples_leaf=20),
    # R randomForest regression defaults: ntree=500, mtry=p/3, nodesize=5
    "RandomForest": dict(n_estimators=N_TREES, max_features=1 / 3,
                         min_samples_leaf=5),
    "QRF": dict(n_estimators=N_TREES, max_features=1 / 3, min_samples_leaf=5),
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
        IRIS_QUANTILE=IRIS_QUANTILE, CV_FOLDS=CV_FOLDS,
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
    """Paper p.13: two INDEPENDENT N/2 draws with replacement.
    NB: train and test overlap (~39% of test rows also appear in train)."""
    rng = np.random.RandomState(seed)
    tr = rng.choice(n, size=n // 2, replace=True)
    te = rng.choice(n, size=n // 2, replace=True)
    return tr, te


def disjoint_split_idx(n, seed=RANDOM_STATE):
    """Untouched-test protocol: random 50/50 partition, no shared households."""
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
    N = TP + FP + FN + TN
    d = TP + FP
    t = TP + FN
    return dict(
        TP=TP, FP=FP, FN=FN, TN=TN,
        TA=(TP + TN) / N if N else 0.0,
        PA=TP / d if d else 0.0,
        UC=FN / t if t else 0.0,
        LE=FP / t if t else 0.0,
        BPAC=(TP / d - abs(FN / d - FP / d)) if d else 0.0,
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
    d = TP + FP
    t = TP + FN
    with np.errstate(divide="ignore", invalid="ignore"):
        out = dict(
            TA=(TP + TN) / N,
            PA=np.where(d > 0, TP / d, 0.0),
            UC=np.where(t > 0, FN / t, 0.0),
            LE=np.where(t > 0, FP / t, 0.0),
            BPAC=np.where(d > 0, TP / d - np.abs(FN / d - FP / d), 0.0),
        )
    return out


def ci(arr, alpha=0.05):
    return (float(np.percentile(arr, 100 * alpha / 2)),
            float(np.percentile(arr, 100 * (1 - alpha / 2))))


def summarise(boot):
    """dict metric -> (mean, lo, hi)."""
    return {k: (float(np.mean(v)), *ci(v)) for k, v in boot.items()}


# ══════════════════════════════════════════════════════════════════════════════
#  QRF QUANTILE SELECTION
# ══════════════════════════════════════════════════════════════════════════════
def qrf_oof_predictions(X_tr, y_tr, groups=None, seed=RANDOM_STATE,
                        folds=CV_FOLDS, grid=QRF_QUANTILE_GRID):
    """Out-of-fold QRF predictions on the TRAINING sample at every grid quantile.

    groups: household ids of the training rows. With the paper's
    with-replacement split the training sample contains duplicates; grouping
    keeps every copy of a household in the same fold."""
    from sklearn.model_selection import GroupKFold
    X_tr = np.asarray(X_tr); y_tr = np.asarray(y_tr)
    if groups is None:
        groups = np.arange(len(y_tr))
    oof = np.zeros((len(y_tr), len(grid)))
    for k, (a, b) in enumerate(GroupKFold(n_splits=folds).split(X_tr, y_tr, groups)):
        m = make_model("QRF", seed=seed + k)
        m.fit(X_tr[a], y_tr[a])
        oof[b] = m.predict(X_tr[b], quantiles=list(grid))
    return oof


def best_quantile(y, preds, line, grid=QRF_QUANTILE_GRID):
    """Grid quantile with highest BPAC; preds has one column per grid quantile."""
    scores = {q: targeting_metrics(y, preds[:, j], line)["BPAC"]
              for j, q in enumerate(grid)}
    return max(scores, key=scores.get), scores


def select_quantile_cv(X_tr, y_tr, line, groups=None, seed=RANDOM_STATE):
    """Honest selection: CV on training data only; test set never seen."""
    return best_quantile(y_tr, qrf_oof_predictions(X_tr, y_tr, groups, seed), line)


def select_quantile_on_test(qrf, X_te, y_te, line, grid=QRF_QUANTILE_GRID):
    """Paper-style (optimistic) selection: best BPAC on the test sample itself."""
    return best_quantile(y_te, qrf.predict(np.asarray(X_te), quantiles=list(grid)),
                         line, grid)
