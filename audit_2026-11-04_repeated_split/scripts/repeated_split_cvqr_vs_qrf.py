"""
Phase 1 — repeated-split comparison of CV-QR (published cross-validation
approach) and QRF (frozen stochastic-ensemble OOB rule) on IDENTICAL train/test
households. See ../PROTOCOL.md (pre-declared).

Read-only with respect to the frozen pipeline: imports common.py, writes only to
audit_2026-11-04_repeated_split/outputs/.

Usage (from Model_Training/):
  python3 audit_2026-11-04_repeated_split/scripts/repeated_split_cvqr_vs_qrf.py --repro-check
  python3 audit_2026-11-04_repeated_split/scripts/repeated_split_cvqr_vs_qrf.py --seeds 1000 1001 1002
Each finished split is checkpointed to outputs/per_split/split_<seed>.json and
skipped on re-run (resumable).
"""
import argparse
import hashlib
import json
import os
import sys
import time
import warnings

import numpy as np
from joblib import Parallel, delayed
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import QuantileRegressor
from sklearn.model_selection import KFold

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
ROOT = os.path.dirname(AUDIT)
sys.path.insert(0, ROOT)
import common as C  # noqa: E402

OUT = os.path.join(AUDIT, "outputs")
PER_SPLIT = os.path.join(OUT, "per_split")
os.makedirs(PER_SPLIT, exist_ok=True)

GRID = C.QRF_QUANTILE_GRID
N_ITER, STAGE1, WINDOW, K = 500, 50, 0.10, 3          # as cv_qr_baseline.py
METRICS = ("TA", "PA", "UC", "LE", "BPAC")


def fold_job(Xtr, ytr, a, b, lines, cols):
    """Same computation as cv_qr_baseline.fold_job, plus convergence accounting."""
    out = np.full((len(lines), len(GRID)), np.nan)
    n_warn = n_fail = 0
    for j in cols:
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always", ConvergenceWarning)
                m = QuantileRegressor(quantile=GRID[j], alpha=0.0, solver="highs").fit(Xtr[a], ytr[a])
            n_warn += sum(issubclass(x.category, ConvergenceWarning) for x in w)
        except Exception:                                    # noqa: BLE001
            n_fail += 1
            continue
        p = m.predict(Xtr[b])
        for i, l in enumerate(lines):
            out[i, j] = C.targeting_metrics(ytr[b], p, l)["BPAC"]
    return out, n_warn, n_fail


def run_iters(Xtr, ytr, lines, seed, iters, cols):
    jobs = [(a, b) for it in iters
            for a, b in KFold(K, shuffle=True, random_state=seed * 100_000 + it).split(Xtr)]
    res = Parallel(n_jobs=-1, batch_size=2)(delayed(fold_job)(Xtr, ytr, a, b, lines, cols)
                                            for a, b in jobs)
    return np.stack([r[0] for r in res]), sum(r[1] for r in res), sum(r[2] for r in res)


def cv_select(Xtr, ytr, lines, seed):
    S1, w1, f1 = run_iters(Xtr, ytr, lines, seed, range(STAGE1), list(range(len(GRID))))
    m1 = np.nanmean(S1, 0)
    keep = set()
    for i in range(len(lines)):
        qb = GRID[int(np.nanargmax(m1[i]))]
        keep |= {j for j, q in enumerate(GRID) if abs(q - qb) <= WINDOW + 1e-9}
    keep = sorted(keep)
    S2, w2, f2 = run_iters(Xtr, ytr, lines, seed, range(STAGE1, N_ITER), keep)
    S = np.concatenate([S1, S2])
    se1 = np.nanstd(S1, 0, ddof=1) / np.sqrt(S1.shape[0])
    excl = [j for j in range(len(GRID)) if j not in keep]
    info = dict(stage2_grid=[GRID[keep[0]], GRID[keep[-1]], len(keep)],
                convergence_warnings=int(w1 + w2), fit_failures=int(f1 + f2), lines={})
    for i in range(len(lines)):
        mean = np.nanmean(S[:, i, :], 0)
        jb1 = int(np.nanargmax(m1[i]))
        je = max(excl, key=lambda j: m1[i, j]) if excl else None
        info["lines"][i] = dict(
            q=GRID[int(np.nanargmax(mean))],
            cv_bpac=float(np.nanmax(mean)),
            stability={r: GRID[int(np.nanargmax(np.nanmean(S[:r * K, i, :], 0)))]
                       for r in (10, 50, 100, 250, 500)},
            pruning_gap_in_SE=(float((m1[i, jb1] - m1[i, je]) / np.hypot(se1[i, jb1], se1[i, je]))
                               if je is not None else None))
    return S, info


def repro_check():
    """Stage 1 of the stored seed-42 paper-protocol run must be reproduced exactly."""
    t0 = time.time()
    X, y, base = C.load_bolivia(verbose=False)
    Xd, y = C.iris_design(X.values), y.values
    tr, _ = C.paper_split_idx(len(y), C.RANDOM_STATE)
    S1, w, f = run_iters(Xd[tr], y[tr], [base], C.RANDOM_STATE, range(STAGE1), list(range(len(GRID))))
    stored = np.load(os.path.join(ROOT, "results", "cv_qr", "cv_fold_bpac_paper.npy"))[:STAGE1 * K, 0, :]
    res = dict(identical=bool(np.array_equal(S1[:, 0, :], stored)),
               max_abs_diff=float(np.nanmax(np.abs(S1[:, 0, :] - stored))),
               shape=list(S1[:, 0, :].shape), convergence_warnings=int(w), fit_failures=int(f),
               runtime_s=round(time.time() - t0, 1))
    with open(os.path.join(OUT, "repro_check_seed42_stage1.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print("repro check:", res, flush=True)


def evaluate(y_te, pred_a, pred_b, line, idx):
    pa, pb = C.targeting_metrics(y_te, pred_a, line), C.targeting_metrics(y_te, pred_b, line)
    ba, bb = C.bootstrap_metrics(y_te, pred_a, line, idx), C.bootstrap_metrics(y_te, pred_b, line, idx)
    out = {}
    for m in METRICS:
        d = ba[m] - bb[m]
        lo, hi = C.ci(d)
        out[m] = dict(cvqr=pa[m], qrf=pb[m], diff=pa[m] - pb[m], boot_lo=lo, boot_hi=hi,
                      boot_mean=float(d.mean()))
    out["confusion"] = dict(cvqr=[pa[k] for k in ("TP", "FP", "FN", "TN")],
                            qrf=[pb[k] for k in ("TP", "FP", "FN", "TN")])
    return out


def run_split(seed):
    path = os.path.join(PER_SPLIT, f"split_{seed}.json")
    if os.path.exists(path):
        print(f"seed {seed}: already done, skipping", flush=True)
        return
    t0 = time.time()
    X, y, base = C.load_bolivia(verbose=False)
    Xv, Xd, y = X.values, C.iris_design(X.values), y.values
    lines = {"P24.2_frozen": base, "P24.03": float(np.percentile(y, 24.03))}
    tr, te = C.paper_split_idx(len(y), seed)
    rec = dict(seed=seed, protocol="paper (published S1)", n_train=len(tr), n_test=len(te),
               n_unique_train=int(len(np.unique(tr))),
               share_unique_test_in_train=float(np.isin(np.unique(te), tr).mean()),
               lines=lines, train_idx_sha256=hashlib.sha256(tr.tobytes()).hexdigest()[:16])
    # CV-QR: selection on training only
    t1 = time.time()
    S, info = cv_select(Xd[tr], y[tr], list(lines.values()), seed)
    np.savez_compressed(os.path.join(PER_SPLIT, f"cv_fold_bpac_{seed}.npz"), S=S)
    rec["cv_runtime_s"] = round(time.time() - t1, 1)
    rec["cv_info"] = info
    # QRF (frozen SE rule): selection on training only
    t2 = time.time()
    rf = C.make_model("RandomForest", seed).fit(Xv[tr], y[tr])
    qrf = C.make_model("QRF", seed).fit(Xv[tr], y[tr])
    oob = C.se_oob_predictions(rf, qrf, Xv[tr])
    se_test = C.se_test_predictions(rf, qrf, Xv[te])
    rec["qrf_runtime_s"] = round(time.time() - t2, 1)
    idx = C.boot_indices(len(te))
    rec["results"] = {}
    for i, (lab, l) in enumerate(lines.items()):
        q_cv = info["lines"][i]["q"]
        cvqr = C.make_model("IRIS_QR").set_params(quantile=q_cv).fit(Xd[tr], y[tr]).predict(Xd[te])
        se_label, col, _ = C.select_se(y[tr], oob, l)
        rec["results"][lab] = dict(cvqr_q=q_cv, qrf_selected=se_label,
                                   **evaluate(y[te], cvqr, se_test[:, col], l, idx))
    rec["total_runtime_s"] = round(time.time() - t0, 1)
    with open(path, "w") as fh:
        json.dump(rec, fh, indent=2, default=float)
    r = rec["results"]["P24.2_frozen"]
    print(f"seed {seed}: CV-QR q={r['cvqr_q']:.2f} BPAC={r['BPAC']['cvqr']:.4f} | "
          f"QRF {r['qrf_selected']} BPAC={r['BPAC']['qrf']:.4f} | dBPAC={r['BPAC']['diff']:+.4f} | "
          f"warn={info['convergence_warnings']} fail={info['fit_failures']} | {rec['total_runtime_s']}s",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[])
    ap.add_argument("--repro-check", action="store_true")
    a = ap.parse_args()
    if a.repro_check:
        repro_check()
    for s in a.seeds:
        run_split(s)


if __name__ == "__main__":
    main()
