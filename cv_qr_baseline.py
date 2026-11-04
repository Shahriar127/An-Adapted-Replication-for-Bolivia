"""
cv_qr_baseline.py — Phase 2: the published cross-validation (CV) baseline.

Published procedure (McBride & Nichols 2018, p.539; Table A1 rows 6-8):
  "we perform k-fold cross-validation in the training sample and select as our
   preferred model the one that produces the best BPAC in cross-validation ...
   we produce 500 iterations of three-fold cross-validation"
  Bolivia result: CV QR(0.38): TA 81.76 PA 63.37 UC 36.63 LE 41.61 BPAC 57.94.

Implementation:
  SPECIFIED      linear quantile regression (the IRIS model family, same 21
                 variables), 500 iterations x 3-fold CV inside the TRAINING
                 sample, selection by BPAC; final model refit on the whole
                 training sample at the chosen quantile; 1,000 bootstrap test draws.
  RECONSTRUCTED  quantile grid 0.01..0.99 (the published choices are integers);
                 fold assignment by row (the paper's training sample is a
                 with-replacement draw, so a household's copies may straddle
                 folds, as in R); score = mean BPAC over the 1,500 held-out folds;
                 ties -> lowest quantile; solver HiGHS, alpha=0, intercept,
                 8 region dummies (frozen IRIS design).
  ADAPTED (compute) two-stage evaluation, which gives the same argmax unless a
                 pruned quantile could overtake the leader: stage 1 = 50
                 iterations over the full grid; stage 2 = the remaining 450
                 iterations (500 in total) only for quantiles within +/-0.10 of any
                 line's stage-1 best. Excluded quantiles keep their stage-1 mean.
                 The stage-1 margin of the best excluded quantile, in SE units, is
                 written to cv_pruning_check.csv.
  The test sample is never touched before the quantile is fixed.

Outputs → results/cv_qr/ (CV scores are stored for the base, halved and
doubled lines so Phase 3 can reuse them without re-running the CV).
"""
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.linear_model import QuantileRegressor
from sklearn.model_selection import KFold

import common as C

warnings.filterwarnings("ignore")
OUT = os.path.join(C.RESULTS_DIR, "cv_qr")
os.makedirs(OUT, exist_ok=True)
N_ITER = int(os.environ.get("CV_ITER", 500))
STAGE1 = min(50, N_ITER)
WINDOW = 0.10
K = 3
GRID = C.QRF_QUANTILE_GRID
PROTOCOLS = {"paper": C.paper_split_idx, "disjoint": C.disjoint_split_idx}


def line_set(base):
    """Base (frozen) line plus the Table A2 halved and doubled lines (p.539)."""
    return {"base": base, "half": base / 2, "double": base * 2}


def fold_job(Xtr, ytr, a, b, lines, cols):
    """Fit QR at the grid quantiles in `cols` on rows a; BPAC on held-out rows b per line."""
    out = np.full((len(lines), len(GRID)), np.nan)
    for j in cols:
        q = GRID[j]
        m = QuantileRegressor(quantile=q, alpha=0.0, solver="highs").fit(Xtr[a], ytr[a])
        p = m.predict(Xtr[b])
        for i, l in enumerate(lines):
            out[i, j] = C.targeting_metrics(ytr[b], p, l)["BPAC"]
    return out


def run_iters(Xtr, ytr, lines, seed, iters, cols):
    jobs = [(a, b) for it in iters
            for a, b in KFold(K, shuffle=True, random_state=seed * 100_000 + it).split(Xtr)]
    res = Parallel(n_jobs=-1, batch_size=2)(
        delayed(fold_job)(Xtr, ytr, a, b, lines, cols) for a, b in jobs)
    return np.stack(res)                      # (len(iters)*K, n_lines, n_grid)


def cv_scores(Xtr, ytr, lines, seed):
    """Two-stage CV. Returns fold-level BPAC (NaN where not evaluated) and a pruning check."""
    S1 = run_iters(Xtr, ytr, lines, seed, range(STAGE1), list(range(len(GRID))))
    m1 = S1.mean(0)                                            # (n_lines, n_grid)
    keep = set()
    for i in range(len(lines)):
        qb = GRID[int(np.argmax(m1[i]))]
        keep |= {j for j, q in enumerate(GRID) if abs(q - qb) <= WINDOW + 1e-9}
    keep = sorted(keep)
    S2 = run_iters(Xtr, ytr, lines, seed, range(STAGE1, N_ITER), keep) if N_ITER > STAGE1 else None
    S = S1 if S2 is None else np.concatenate([S1, S2])
    checks = []
    se1 = S1.std(0, ddof=1) / np.sqrt(S1.shape[0])
    excl = [j for j in range(len(GRID)) if j not in keep]
    for i in range(len(lines)):
        jb = int(np.argmax(m1[i]))
        if excl:
            je = max(excl, key=lambda j: m1[i, j])
            gap = m1[i, jb] - m1[i, je]
            checks.append(dict(line_index=i, stage1_best_q=GRID[jb], best_excluded_q=GRID[je],
                               stage1_gap=gap, gap_in_SE=gap / np.hypot(se1[i, jb], se1[i, je])))
    return S, keep, checks


def first_best(scores):
    return GRID[int(np.argmax(scores))]       # argmax returns the first maximum


def main():
    t0 = time.time()
    X, y, base = C.load_bolivia(verbose=False)
    Xd, y = C.iris_design(X.values), y.values
    lines = line_set(base)
    score_rows, stab_rows, res_rows, cm_rows, prune_rows = [], [], [], [], []
    for proto, split in PROTOCOLS.items():
        tr, te = split(len(y), C.RANDOM_STATE)
        S, keep, checks = cv_scores(Xd[tr], y[tr], list(lines.values()), C.RANDOM_STATE)
        for c in checks:
            c.update(protocol=proto, line=list(lines)[c["line_index"]],
                     stage2_grid=f"{GRID[keep[0]]:.2f}-{GRID[keep[-1]]:.2f} ({len(keep)} q)")
            prune_rows.append(c)
        np.save(os.path.join(OUT, f"cv_fold_bpac_{proto}.npy"), S)
        idx = C.boot_indices(len(te))
        for i, (lab, l) in enumerate(lines.items()):
            mean_scores = np.nanmean(S[:, i, :], axis=0)
            for j, q in enumerate(GRID):
                score_rows.append(dict(protocol=proto, line=lab, line_value=l, q=q,
                                       cv_bpac=mean_scores[j]))
            for r in (10, 50, 100, 250, 500):
                if r <= N_ITER:
                    stab_rows.append(dict(protocol=proto, line=lab, iterations=r,
                                          chosen_q=first_best(np.nanmean(S[:r * K, i, :], axis=0))))
            q_star = first_best(mean_scores)
            m = C.make_model("IRIS_QR").set_params(quantile=q_star).fit(Xd[tr], y[tr])
            pred = m.predict(Xd[te])
            b = C.bootstrap_metrics(y[te], pred, l, idx)
            se, s = C.boot_se(b), C.summarise(b)
            res_rows.append(dict(protocol=proto, line=lab, line_value=l, model=f"CV QR({q_star:.2f})",
                                 q=q_star, **{m_: s[m_][0] for m_ in C.METRICS},
                                 **{f"{m_}_SE": se[m_] for m_ in C.METRICS},
                                 **{f"{m_}_lo": s[m_][1] for m_ in C.METRICS},
                                 **{f"{m_}_hi": s[m_][2] for m_ in C.METRICS}))
            pt = C.targeting_metrics(y[te], pred, l)
            cm_rows.append(dict(protocol=proto, line=lab, model=f"CV QR({q_star:.2f})",
                                **{k: pt[k] for k in ("TP", "FP", "FN", "TN")}))
        print(f"[{proto}] CV done in {time.time()-t0:.0f}s", flush=True)
    pd.DataFrame(score_rows).to_csv(os.path.join(OUT, "cv_scores.csv"), index=False)
    pd.DataFrame(stab_rows).to_csv(os.path.join(OUT, "cv_choice_stability.csv"), index=False)
    pd.DataFrame(prune_rows).to_csv(os.path.join(OUT, "cv_pruning_check.csv"), index=False)
    print(pd.DataFrame(prune_rows).to_string(index=False))
    pd.DataFrame(res_rows).to_csv(os.path.join(OUT, "cv_qr_results.csv"), index=False)
    pd.DataFrame(cm_rows).to_csv(os.path.join(OUT, "cv_qr_confusion.csv"), index=False)
    print(pd.DataFrame(stab_rows).to_string(index=False))
    print(pd.DataFrame(res_rows)[["protocol", "line", "model", "TA", "PA", "UC", "LE", "BPAC",
                                  "BPAC_lo", "BPAC_hi"]].round(4).to_string(index=False))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    sys.exit(main())
