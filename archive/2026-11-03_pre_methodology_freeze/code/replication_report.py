"""
replication_report.py
─────────────────────
Generates a comprehensive replication verification report for:

  McBride & Nichols (2015)
  "Improved Poverty Targeting Through Machine Learning:
   An Application to the USAID Poverty Assessment Tools"

Verifications:
  1. Dataset / household count
  2. Variable mapping (paper Table 3 → Bolivia EH 2005 SPSS)
  3. Target construction (G_TOTAL_pc, poverty line, poverty rate)
  4. Missing values at each merge step
  5. Bootstrap procedure (N/2 with replacement, 1000 re-draws)
  6. BPAC formula (numerical example, denominator consistency)
  7. IRIS Q(42) quantile regression baseline
  8. Model comparison: DT / RF / QRF / IRIS with 95% CIs

Output: results/Bolivia/replication_report.txt
"""

import os, warnings, sys
from io import StringIO
import numpy as np
import pandas as pd

import common as C

warnings.filterwarnings("ignore")

# ── config: imported from common.py (shared with train_models.py) ─────────────
RESULTS_DIR = os.path.join(C.RESULTS_DIR, "Bolivia")
B_REPS      = C.BOOTSTRAP_REPS
RAND        = C.RANDOM_STATE

os.makedirs(RESULTS_DIR, exist_ok=True)

# ── report buffer ─────────────────────────────────────────────────────────────
_buf = StringIO()

def w(*args, **kw):
    print(*args, **kw, file=_buf)
    print(*args, **kw)          # also print to stdout

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 0 — HEADER
# ══════════════════════════════════════════════════════════════════════════════
w("=" * 72)
w("ADAPTED REPLICATION REPORT")
w("McBride & Nichols (2015): Improved Poverty Targeting Through ML")
w("Adapted replication using a reconstructed poverty threshold and")
w("documented implementation choices. Not an exact replication: the paper's")
w("seed, household subset, threshold and preprocessing are not public.")
w("=" * 72)
w("")
w("Dataset: Bolivia Encuesta de Hogares 2005 (EH 2005)")
w("Source:  https://siip.produccion.gob.bo/repSIIP2/files/encuesta_hogares/EH2005.rar")
w("Files:   BASE_EH_2005_(Pob_y_Viv).sav  +  Bolivia_Equipamiento.sav  +")
w("         Bolivia_Pecuaria.sav")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA (shared across all sections)
# ══════════════════════════════════════════════════════════════════════════════
w("Loading SPSS files ...")
df_main, meta_main, df_eq, df_pec = C.load_raw()
w("Done.")
w("Configuration (common.py — identical in train_models.py):")
for k, v in C.MODEL_CONFIG.items():
    w(f"  {k:<13} {v}")
w(f"  seed={C.RANDOM_STATE}  boot_seed={C.BOOT_SEED}  B={C.BOOTSTRAP_REPS}  "
  f"split=paper N/2 with replacement (np.random.RandomState)")
w(f"  QRF quantile: 5-fold CV on training sample (test set never used)")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — DATASET VERIFICATION
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 1: DATASET VERIFICATION")
w("─" * 72)
n_persons = len(df_main)
n_hh      = df_main['folio'].nunique()
w(f"  Person-level rows:       {n_persons:,}")
w(f"  Unique households (HH):  {n_hh:,}")
w(f"  Paper claims N = 4,086:  {'MATCH ✓' if n_hh == 4086 else 'MISMATCH ✗'}")
w(f"  Equipment rows:          {len(df_eq):,}  ({df_eq['folio'].nunique()} HH × 22 items/HH)")
w(f"  Livestock rows:          {len(df_pec):,}  ({df_pec['folio'].nunique()} HH have livestock records)")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — VARIABLE MAPPING
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 2: VARIABLE MAPPING  (Paper Table 3 → Bolivia EH 2005)")
w("─" * 72)
w(f"  {'Paper variable':<18} {'EH 2005 source':<28} {'Status':<8} Notes")
w(f"  {'-'*17} {'-'*27} {'-'*7} {'-'*28}")

VMAP = [
    ("hhsize",        "miembros",               "DIRECT",   "Members in household"),
    ("hhsize2",       "miembros^2",              "DERIVED", "Polynomial term"),
    ("age_head",      "s1_03 where s1_05=1",     "DIRECT",   "Jefe/jefa age"),
    ("age_head2",     "age_head^2",              "DERIVED", "Polynomial term"),
    ("regions",       "depto  (codes 1–9)",      "APPROX",  "Ordinal; OLS needs dummies"),
    ("rural",         "urb_rur == 2",            "DIRECT",   "2=rural, 1=urban"),
    ("sublease",      "s7_02 == 1  (alquilada)", "APPROX",  "'Rented' used; no 'sublease' code"),
    ("brick_wall",    "s7_05 == 1",              "DIRECT",   "Ladrillo/bloque de cemento"),
    ("wood_wall",     "s7_05 == 5",              "DIRECT",   "Madera"),
    ("dirt_floor",    "s7_08 == 1",              "DIRECT",   "Tierra"),
    ("cement_floor",  "s7_08 == 5",              "DIRECT",   "Cemento"),
    ("fridge",        "Equip s6_16cod=7",        "DIRECT",   "Refrigerador/Freezer"),
    ("radio",         "Equip s6_16cod=10",       "DIRECT",   "Radiograbador"),
    ("tv",            "Equip s6_16cod=12",       "DIRECT",   "Televisor"),
    ("dvd",           "Equip s6_16cod=13",       "DIRECT",   "Reproductor VHS/DVD"),
    ("fan",           "Equip s6_16cod=18",       "DIRECT",   "Ventilador"),
    ("car",           "Equip s6_16cod=22",       "DIRECT",   "Automóvil"),
    ("num_beds",      "Equip s6_16cod=1, count", "DIRECT",   "Count catre/cama (s6_17)"),
    ("num_kitchens",  "s7_19 == 1  (binary)",    "APPROX",  "Paper says count; EH has binary"),
    ("num_computers", "Equip s6_16cod=9, count", "DIRECT",   "Count computadora (s6_17)"),
    ("sheep",         "Pecuaria codb='B', sum",  "DIRECT",   "Ovinos stock (s8_10)"),
]
n_exact   = sum(1 for *_,s,_ in VMAP if s=="DIRECT")
n_approx  = sum(1 for *_,s,_ in VMAP if s=="APPROX")
n_derived = sum(1 for *_,s,_ in VMAP if s=="DERIVED")
for pv, src, status, note in VMAP:
    sym = "✓" if status=="DIRECT" else ("~" if status=="APPROX" else "Δ")
    w(f"  {pv:<18} {src:<28} {sym+' '+status:<8} {note}")
w("")
w("  DIRECT = survey variable matches the paper's variable name/meaning per the")
w("  EH 2005 codebook (checked by data_construction_audit.py). It does NOT prove")
w("  the paper's authors built the variable the same way.")
w(f"  Summary: {n_exact} direct (codebook-verified) | {n_derived} derived | {n_approx} approximations")
w(f"  Approximations flagged:")
for pv, src, status, note in VMAP:
    if status == "APPROX":
        w(f"    '{pv}': {note}")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — TARGET CONSTRUCTION
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 3: TARGET VARIABLE CONSTRUCTION")
w("─" * 72)
vl = meta_main.column_names_to_labels
w(f"  Variable: G_TOTAL_pc")
w(f"  Full label: {str(vl.get('G_TOTAL_pc',''))}")
w(f"  Components:")
for comp in ['G_ALIM_DENTRO_pc','G_ALIM_FUERA_pc','G_NO_ALIMENTARIO_pc','G_VIVIENDA_pc']:
    if comp in df_main.columns:
        w(f"    {comp:<30} — {str(vl.get(comp,''))[:50]}")
w("")

hh_exp     = df_main.groupby('folio')['G_TOTAL_pc'].first().dropna()
pline      = C.reconstructed_poverty_line(hh_exp.values)
prate      = float((hh_exp < pline).mean())
w(f"  Poverty line construction:")
w(f"    Method: 24.2th percentile of G_TOTAL_pc across all {n_hh} HH")
w(f"    Value:  {pline:.4f} Bs/month per capita")
w(f"    Resulting poverty rate: {prate:.4f} ({prate*100:.2f}%)")
w(f"    Paper's 24.2% rate is reproduced BY CONSTRUCTION (threshold chosen to hit it).")
w(f"    LIMITATION: the threshold is DATA-DERIVED from the FULL sample, so test")
w(f"    households help define it. Train-derived P24.2 for the seed-42 paper split")
w(f"    = {C.reconstructed_poverty_line(df_main.groupby('folio')['G_TOTAL_pc'].first().dropna().values[C.paper_split_idx(n_hh)[0]]):.2f} Bs;"
  f" its effect is reported in results/sensitivity/.")
w(f"  Distribution of G_TOTAL_pc:")
w(f"    Mean: {hh_exp.mean():.2f}  Median: {hh_exp.median():.2f}  Min: {hh_exp.min():.2f}  Max: {hh_exp.max():.2f}")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — MISSING VALUES / MERGE AUDIT
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 4: MISSING VALUE AUDIT — MERGE PIPELINE")
w("─" * 72)

hh = C.build_household_frame(df_main, df_eq, df_pec)
FEAT = C.FEATURE_COLS
w(f"  Step 1–3 — collapse to HH, merge head age, equipment, livestock: {len(hh):,} HH")
w(f"    Missing G_TOTAL_pc:  {hh['G_TOTAL_pc'].isna().sum()}")
w(f"    Missing age_head:    {hh['age_head'].isna().sum()}")
w(f"    Feature NaN (any):   {hh[FEAT].isna().any(axis=1).sum()}")
w(f"    HH with sheep>0:     {(hh['sheep']>0).sum():,}")
w(f"    HH with G_TOTAL_pc == 0: {(hh['G_TOTAL_pc']==0).sum()}")

hh_clean = C.clean(hh)
w(f"  Step 4 — drop missing G_TOTAL_pc or age_head: {len(hh_clean):,} HH")
w(f"    Dropped: {len(hh) - len(hh_clean)}")
w(f"  FINAL analysis N = {len(hh_clean):,}  (matches paper N=4,086: "
  f"{'YES ✓' if len(hh_clean)==4086 else 'NO ✗'})")
w("")

X_full  = hh_clean[FEAT].values
y_full  = hh_clean['G_TOTAL_pc'].values.astype(float)
poverty_line = pline
N       = len(y_full)
N2      = N // 2

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — BOOTSTRAP PROCEDURE
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 5: BOOTSTRAP PROCEDURE VERIFICATION")
w("─" * 72)
w(f"  Total households N = {N}")
w(f"  Bootstrap sample size = N/2 = {N2}")
w(f"  Resampling: WITH replacement (paper p.13)")
w(f"  Test evaluations B = {B_REPS} bootstrap re-draws")
w("")
w(f"  Theoretical expected unique fraction (k=N/2 draws from N with replacement):")
w(f"    E[unique/k] = 2*(1 - e^(-0.5)) = {2*(1-np.exp(-0.5)):.4f}  (≈78.69%)")
w("")

u_fracs = [np.unique(C.paper_split_idx(N, s)[0]).size / N2 for s in range(20)]
obs_mean = np.mean(u_fracs)
expected = 2*(1 - np.exp(-0.5))
w(f"  Observed mean unique fraction (20 draws): {obs_mean:.4f}")
w(f"  Expected:                                 {expected:.4f}")
w(f"  Bootstrap N/2 verified: {'YES ✓' if abs(obs_mean-expected) < 0.03 else 'NO ✗'}")
_tr, _te = C.paper_split_idx(N, RAND)
w(f"  NOTE: train and test are independent draws, so they overlap:")
w(f"    {np.isin(np.unique(_te), _tr).mean():.1%} of unique test households also appear in training")
w(f"    (see results/sensitivity/ for an untouched-test-set protocol)")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — BPAC FORMULA
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 6: BPAC FORMULA VERIFICATION")
w("─" * 72)
w("""  Paper Table 2 formulas:
    TA   = (TP+TN) / N
    PA   = TP / (TP+FP)                  denominator = PREDICTED poor
    UC   = FN / (TP+FN)                  denominator = TRUE poor
    LE   = FP / (TP+FN)                  unconventional; can exceed 1 (footnote 7)
    BPAC = TP/(TP+FP) − |FN/(TP+FP) − FP/(TP+FP)|
           ALL three BPAC sub-terms share denominator (TP+FP)
           This differs from UC (TP+FN) and LE (TP+FN) denominators.

  Numerical examples:""")

targeting_metrics = C.targeting_metrics

for label, TP,FP,FN,TN in [("Realistic (QRF-like)",17,7,7,69),
                             ("Perfect",             24,0,0,76),
                             ("Random",               6,18,18,58)]:
    Nn=TP+FP+FN+TN; d=TP+FP
    TA=(TP+TN)/Nn; PA=TP/d if d>0 else 0
    UC=FN/(TP+FN) if (TP+FN)>0 else 0; LE=FP/(TP+FN) if (TP+FN)>0 else 0
    BPAC=TP/d-abs(FN/d-FP/d) if d>0 else 0
    w(f"  {label}:  TP={TP} FP={FP} FN={FN} TN={TN}")
    w(f"    TA={TA:.4f}  PA={PA:.4f}  UC={UC:.4f}  LE={LE:.4f}  BPAC={BPAC:.4f}")
    w(f"    BPAC = {TP}/{d} − |{FN}/{d} − {FP}/{d}| = {TP/d:.4f} − {abs(FN/d-FP/d):.4f} = {BPAC:.4f}")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# HELPER: draw paper split + bootstrap evaluation
# ══════════════════════════════════════════════════════════════════════════════
TR_IDX, TE_IDX = C.paper_split_idx(N, RAND)     # one split for ALL models
BOOT_IDX = C.boot_indices(len(TE_IDX))          # same resamples for ALL models

def evaluate(y_pred):
    return C.bootstrap_metrics(y_full[TE_IDX], np.asarray(y_pred), poverty_line, BOOT_IDX)

ci = C.ci

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — IRIS Q(42) BASELINE
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 7: IRIS Q(42) BASELINE — Quantile Regression at 42nd Percentile")
w("─" * 72)
w("""  IRIS method = USAID's quantile regression benchmark (paper Table 4).
  Bolivia: IRIS Q(42) — fit at quantile=0.42, same 21 variables.
  'regions' encoded as 9 dummy variables for the linear model.
  Evaluated with {B} bootstrap re-draws of the test set.
""".format(B=B_REPS))

X_iris_vals = C.iris_design(X_full)
w(f"  Feature count: {X_iris_vals.shape[1]} (20 non-region + 8 region dummies; reference")
w(f"  region = Chuquisaca, + intercept). The previous 9-dummies+intercept design was")
w(f"  rank-deficient (29/30); it gave identical predictions, so earlier IRIS targeting")
w(f"  metrics are unaffected, but coefficients are only identified in the new design.")
w(f"  Fitting IRIS Q(42) ...")
iris_model = C.make_model("IRIS_QR").fit(X_iris_vals[TR_IDX], y_full[TR_IDX])
yp_iris_te = iris_model.predict(X_iris_vals[TE_IDX])
m_iris_pt  = targeting_metrics(y_full[TE_IDX], yp_iris_te, poverty_line)
w(f"  Point-estimate (no bootstrap): PA={m_iris_pt['PA']:.4f}  "
  f"UC={m_iris_pt['UC']:.4f}  LE={m_iris_pt['LE']:.4f}  BPAC={m_iris_pt['BPAC']:.4f}")
iris_bs = evaluate(yp_iris_te)
w(f"  IRIS Q(42) results (mean ± 95% CI, B={B_REPS}):")
for metric in ['TA','PA','UC','LE','BPAC']:
    lo, hi = ci(iris_bs[metric])
    w(f"    {metric:<6} = {iris_bs[metric].mean():.4f}  [{lo:.4f}, {hi:.4f}]")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — DT / RF / QRF MODELS
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 8: MODEL TRAINING AND EVALUATION")
w("─" * 72)

Xtr, ytr = X_full[TR_IDX], y_full[TR_IDX]
Xte, yte = X_full[TE_IDX], y_full[TE_IDX]
results, preds_te = {}, {}

w("  Training Decision Tree ...")
preds_te['DT'] = C.make_model("DecisionTree").fit(Xtr, ytr).predict(Xte)
w(f"  Training Random Forest ({C.N_TREES} trees) ...")
preds_te['RF'] = C.make_model("RandomForest").fit(Xtr, ytr).predict(Xte)
w(f"  Training QRF ({C.N_TREES} trees) ...")
qrf = C.make_model("QRF").fit(Xtr, ytr)
best_q, cv_scores = C.select_quantile_cv(Xtr, ytr, poverty_line, groups=TR_IDX)
w(f"  QRF quantile chosen by 5-fold CV on training sample: q={best_q:.2f} "
  f"(CV BPAC={cv_scores[best_q]:.4f})")
w(f"  Paper reports QRF(40) for Bolivia — "
  f"{'MATCH ✓' if abs(best_q-0.40)<1e-9 else f'OUR CV choice q={best_q:.2f}'}")
preds_te['QRF'] = qrf.predict(Xte, quantiles=best_q)
preds_te['QRF40'] = qrf.predict(Xte, quantiles=0.40)
for k, p in preds_te.items():
    results[k] = evaluate(p)
results['IRIS'] = iris_bs
preds_te['IRIS'] = yp_iris_te
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — COMPARISON TABLE
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 9: MODEL COMPARISON (mean ± 95% CI from 1000 bootstrap re-draws)")
w("─" * 72)
w(f"  {'Model':<12} {'TA':>22} {'PA':>22} {'UC':>22} {'LE':>22} {'BPAC':>22}")
w(f"  {'-'*11} {'-'*22} {'-'*22} {'-'*22} {'-'*22} {'-'*22}")

MODEL_LABELS = {
    'IRIS':  'IRIS Q(42)',
    'DT':    'DTree',
    'RF':    'RF(500)',
    'QRF40': 'QRF(40) fix',
    'QRF':   f'QRF(CV q={round(best_q*100)})',
}
table_rows = []
for key in MODEL_LABELS:
    bs  = results[key]
    row = MODEL_LABELS[key]
    cells = []
    for m in ['TA','PA','UC','LE','BPAC']:
        mn = bs[m].mean()
        lo,hi = ci(bs[m])
        cells.append(f"{mn:.3f} [{lo:.3f},{hi:.3f}]")
        table_rows.append(dict(model=row, metric=m, mean=mn, lo=lo, hi=hi))
    w(f"  {row:<12} {cells[0]:>22} {cells[1]:>22} {cells[2]:>22} {cells[3]:>22} {cells[4]:>22}")

pd.DataFrame(table_rows).to_csv(f"{RESULTS_DIR}/report_model_comparison.csv", index=False)
w("")
w("  Confusion matrices (full test sample, point estimate):")
w(f"  {'Model':<14} {'TP':>5} {'FP':>5} {'FN':>5} {'TN':>5}")
cm_rows = []
for key, label in MODEL_LABELS.items():
    m = targeting_metrics(yte, preds_te[key], poverty_line)
    cm_rows.append(dict(model=label, TP=m['TP'], FP=m['FP'], FN=m['FN'], TN=m['TN']))
    w(f"  {label:<14} {m['TP']:>5} {m['FP']:>5} {m['FN']:>5} {m['TN']:>5}")
pd.DataFrame(cm_rows).to_csv(f"{RESULTS_DIR}/report_confusion_matrices.csv", index=False)
C.save_config(f"{RESULTS_DIR}/config.json")
w("")
w("  Paper Table A1 — Bolivia 2005 EH (values as reported in the paper):")
w("  " + "─" * 68)
w("  Source                      TA        PA        UC        LE       BPAC")
w("  " + "─" * 68)
w("  IRIS Q(42) in-sample½      83.65     67.18     32.82     33.29    66.71")
w("  IRIS Q(42) bootstrap mean  81.88     57.58     42.42     34.30    49.33")
w("  IRIS Q(42) 95% CI       [79.78,  [52.51,  [37.35,  [27.60,  [36.73,")
w("                            83.68]   62.65]   47.49]   41.66]   60.48]")
w("  Authors Q(42) full-sample  82.45     60.69     39.30     33.71    55.10")
w("  Authors QRF(40) boot mean  81.44     62.14     37.86     40.11    58.17")
w("  Authors QRF(40) 95% CI  [79.67,  [57.59,  [22.41,  [33.10,  [47.15,")
w("                            83.28]   66.59]   42.41]   47.57]   63.45]")
w("  " + "─" * 68)
w("")
w("  Note: ^ = bootstrapped 1000×, with replacement (mean reported)")
w("        + = 95% CI, lower = 2.5th pct, upper = 97.5th pct")
w("        All Table A1 values are in percentage (×100).")
w("")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — POVERTY-LINE RECONSTRUCTION AND COMPARABILITY
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 10: POVERTY-LINE RECONSTRUCTION AND COMPARABILITY")
w("─" * 72)
w("""
  The original Bolivian poverty-line value in Bolivianos is not reported in
  the paper. The paper states that the USAID-defined "very poor" rate in
  Bolivia was 24.2%. The IRIS 2005 document describes the "very poor"
  threshold as the median consumption expenditure of households classified
  as poor under the official poverty line.

  Applying this methodology approximately to Bolivia EH 2005 suggests a
  threshold around 189–194 Bolivianos, depending on the official poverty-line
  value used:
    Official line ~320 Bs → median of poor ≈ 189.05 Bs → 24.18% very poor
    Official line ~328 Bs → median of poor ≈ 194.10 Bs → 24.91% very poor

  Our reconstructed threshold of 189.09 Bolivianos, defined as the 24.2th
  percentile of G_TOTAL_pc, is therefore numerically consistent with one
  plausible application of the IRIS methodology. However, the original Bolivia
  PAT threshold and expenditure aggregate remain unverified.

  Denominator consistency check (BPAC formula):
    IRIS 2005 uses "PIE" = (FN−FP)/(TP+FP); BPAC = PA − |PIE|.
    This is algebraically identical to the paper's Table 2 formula:
      BPAC = TP/(TP+FP) − |FN/(TP+FP) − FP/(TP+FP)|
    Our implementation uses this formula. ✓

  We consequently treat 189.09 Bolivianos as a reconstructed approximation,
  not as the confirmed original IRIS threshold.
""")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 11 — ADAPTED REPLICATION STATEMENT
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 11: ADAPTED REPLICATION AND RESULTS")
w("─" * 72)
w("""
  Our implementation reproduces the broad methodological framework but does
  not establish an exact replication of the original Bolivia PAT. The paper
  reports that IRIS used a randomly selected subset of the Bolivian data and
  acknowledges that its own replication estimates did not perform as well as
  IRIS. The original subset, random seed, and exact expenditure aggregate
  are not available in the information currently verified.

""")
def _m(key, metric): return 100 * results[key][metric].mean()
w(f"  Gap analysis vs Table A1 (paper values: IRIS PA 57.58, BPAC 49.33; QRF(40) PA 62.14, BPAC 58.17):")
w(f"    PA:   our IRIS Q(42)  = {_m('IRIS','PA'):.2f}%  vs 57.58%  ({_m('IRIS','PA')-57.58:+.1f})")
w(f"    BPAC: our IRIS Q(42)  = {_m('IRIS','BPAC'):.2f}%  vs 49.33%  ({_m('IRIS','BPAC')-49.33:+.1f})")
w(f"    PA:   our QRF(40) fix = {_m('QRF40','PA'):.2f}%  vs 62.14%  ({_m('QRF40','PA')-62.14:+.1f})")
w(f"    BPAC: our QRF(40) fix = {_m('QRF40','BPAC'):.2f}%  vs 58.17%  ({_m('QRF40','BPAC')-58.17:+.1f})")
w(f"    BPAC: our QRF(CV q={round(best_q*100)}) = {_m('QRF','BPAC'):.2f}%")
w("""
  Whether poverty-line differences (189.05–194.10 Bs) matter is tested
  empirically in sensitivity_analysis.py (results/sensitivity/).
  Likely causes:
    1. Unknown random seed — paper's split may produce a harder test set.
    2. IRIS trained on a private randomly selected subset (not full 4,086 HH).
    3. R randomForest vs Python quantile-forest implementation differences.
    4. 3 variable approximations (regions ordinal, sublease, num_kitchens).

  These explanations remain hypotheses and require further investigation.

  REPLICATION LABEL:
  "Adapted replication of McBride & Nichols (2015), Bolivia EH 2005.
   Poverty line reconstructed as the 24.2th percentile of G_TOTAL_pc
   (≈189.09 Bs/month per capita), per the stated poverty rate of 24.2%.
   The exact IRIS-defined threshold was not publicly available; the IRIS
   'median of officially-poor' methodology (IRIS 2005) would yield ≈189–194 Bs
   depending on the official poverty line applied. Results are not directly
   comparable to Table A1 due to: unknown random seed, IRIS private training
   subset, and R vs Python QRF implementation differences."
""")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 12 — KNOWN APPROXIMATIONS AND LIMITATIONS
# ══════════════════════════════════════════════════════════════════════════════
w("─" * 72)
w("SECTION 12: KNOWN APPROXIMATIONS AND LIMITATIONS")
w("─" * 72)
w("""  1. 'regions' encoded as ordinal integer (depto 1–9) for tree models.
     Paper may use 8 regional dummies for IRIS OLS but trees handle ordinal.
     IRIS model here uses 8 dummies + intercept (reference: Chuquisaca).

  2. 'sublease' coded as s7_02==1 (alquilada = rented tenure).
     Bolivia EH 2005 does not distinguish sublease from plain rental.

  3. 'num_kitchens' coded as binary (s7_19==1 = has dedicated kitchen).
     Paper lists it as count; survey variable is binary in EH 2005.

  4. Bootstrap seed not published; our 1000-rep CIs differ from paper's.

  8. Poverty threshold (189.09 Bs) is the 24.2th percentile of the FULL
     sample — data-derived, and the test sample contributes to it. The
     alternatives 189.05 / 194.10 Bs are likewise computed on this sample.
     No externally published 'very poor' line in Bs was available to us.

  7. Paper split draws train and test independently WITH replacement, so
     ~40% of unique test households also appear in training. Flexible
     models (deep trees, small leaves) are optimistic under this protocol.
     results/sensitivity/ reports an untouched (disjoint) test-set protocol.

  5. East Timor and Malawi results not reproduced (data requires World Bank
     registration — see load_timor_leste() / load_malawi() in train_models.py).

  6. IRIS built Bolivia PAT on a randomly selected subset of 4,086 HH.
     Exact subset unknown; we use all 4,086 HH as the authors also did.
""")

# ══════════════════════════════════════════════════════════════════════════════
# SAVE REPORT
# ══════════════════════════════════════════════════════════════════════════════
report_txt = _buf.getvalue()
out_path   = f"{RESULTS_DIR}/replication_report.txt"
with open(out_path, 'w') as f:
    f.write(report_txt)

print(f"\n{'='*72}")
print(f"Report saved → {out_path}")
print(f"{'='*72}")
