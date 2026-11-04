"""
config_audit.py — Step 1: consistency audit between the OLD train_models.py and
the OLD replication_report.py configurations (before both were switched to
common.py).

Re-runs both legacy configurations on the same data and quantifies how much
each difference (hyper-parameters, split RNG, bootstrap seed, protocol)
moves the headline numbers.

Legacy model settings are reproduced on purpose (including quantile-forest's
default max_samples_leaf=1 and the 0.05 grid). Metrics are computed with the
FROZEN published definitions (TP+FN denominators), so PA and BPAC differ from
the archived pre-freeze audit; TA, UC and LE are identical.

Output → results/audit/config_audit.csv and config_audit.txt
"""

import os
import numpy as np
import pandas as pd

import common as C

OUT = os.path.join(C.RESULTS_DIR, "audit")
os.makedirs(OUT, exist_ok=True)

LEGACY_GRID = [round(float(q), 2) for q in np.arange(0.05, 0.96, 0.05)]   # pre-freeze grid

LEGACY = {
    # what each script actually used before the fix
    "train_models.py (old)": dict(
        dt=dict(max_depth=10, min_samples_leaf=20), leaf=5,
        split_rng="RandomState", boot_seeds=dict(DT=42, RF=42, QRF=42)),
    "replication_report.py (old)": dict(
        dt=dict(), leaf=1,
        split_rng="default_rng", boot_seeds=dict(DT=52, RF=62, QRF=72)),
}


def split(n, rng_kind, seed, protocol):
    if protocol == "disjoint":
        return C.disjoint_split_idx(n, seed)
    if rng_kind == "RandomState":
        return C.paper_split_idx(n, seed)
    rng = np.random.default_rng(seed)
    return rng.choice(n, n // 2, replace=True), rng.choice(n, n // 2, replace=True)


def boot_idx(n, rng_kind, seed):
    if rng_kind == "RandomState":
        return np.random.RandomState(seed).randint(0, n, size=(C.BOOTSTRAP_REPS, n))
    rng = np.random.default_rng(seed)
    return np.stack([rng.choice(n, n, replace=True) for _ in range(C.BOOTSTRAP_REPS)])


def main():
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from quantile_forest import RandomForestQuantileRegressor

    X, y, line = C.load_bolivia(verbose=False)
    X, y = X.values, y.values
    rows = []
    for cfg_name, cfg in LEGACY.items():
        for protocol in ("paper", "disjoint"):
            tr, te = split(len(y), cfg["split_rng"], C.RANDOM_STATE, protocol)
            Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]
            dt = DecisionTreeRegressor(random_state=42, **cfg["dt"]).fit(Xtr, ytr)
            rf = RandomForestRegressor(n_estimators=500, max_features=1/3,
                                       min_samples_leaf=cfg["leaf"], n_jobs=-1,
                                       random_state=42).fit(Xtr, ytr)
            qrf = RandomForestQuantileRegressor(n_estimators=500, max_features=1/3,
                                                min_samples_leaf=cfg["leaf"],
                                                n_jobs=-1, random_state=42).fit(Xtr, ytr)
            q_best, _ = C.select_quantile_on_test(qrf, Xte, yte, line, grid=LEGACY_GRID)
            preds = {"DT": dt.predict(Xte), "RF": rf.predict(Xte),
                     f"QRF(test-sel q={q_best:.2f})": qrf.predict(Xte, quantiles=q_best),
                     "QRF(q=0.40)": qrf.predict(Xte, quantiles=0.40),
                     "QRF(q=0.45)": qrf.predict(Xte, quantiles=0.45)}
            for name, yp in preds.items():
                key = name.split("(")[0]
                bseed = cfg["boot_seeds"].get(key, 42)
                b = C.summarise(C.bootstrap_metrics(
                    yte, yp, line, boot_idx(len(yte), cfg["split_rng"], bseed)))
                rows.append(dict(config=cfg_name, protocol=protocol, model=name,
                                 **{m: round(b[m][0], 4) for m in ("PA", "UC", "LE", "BPAC")},
                                 BPAC_lo=round(b["BPAC"][1], 4),
                                 BPAC_hi=round(b["BPAC"][2], 4)))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "config_audit.csv"), index=False)
    txt = df.to_string(index=False)
    with open(os.path.join(OUT, "config_audit.txt"), "w") as f:
        f.write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
