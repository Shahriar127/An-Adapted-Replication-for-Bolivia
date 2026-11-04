"""
data_construction_audit.py — checks the household-level dataset construction
in common.build_household_frame against the survey's own SPSS codebook
(value labels embedded in the .sav files). Fails loudly if an assumption breaks.

Output → results/audit/data_construction_audit.txt
"""
import os
import pyreadstat
import common as C

OUT = os.path.join(C.RESULTS_DIR, "audit")
os.makedirs(OUT, exist_ok=True)
lines = []


def log(s=""):
    print(s); lines.append(s)


def check(cond, msg):
    log(f"  [{'OK ' if cond else 'FAIL'}] {msg}")
    assert cond, msg


dm, mm = pyreadstat.read_sav(os.path.join(C.DATA_DIR, C.RAW_FILES[0]))
de, me = pyreadstat.read_sav(os.path.join(C.DATA_DIR, C.RAW_FILES[1]))
dp, mp = pyreadstat.read_sav(os.path.join(C.DATA_DIR, C.RAW_FILES[2]))
L = lambda m, v: m.variable_value_labels.get(v, {})

log("1. Household-level variables (person file) — is groupby('folio').first() exact?")
for v in ["miembros", "G_TOTAL_pc", "urb_rur", "depto", "s7_02", "s7_05", "s7_08", "s7_19"]:
    n = int((dm.groupby("folio")[v].nunique(dropna=False) > 1).sum())
    check(n == 0, f"{v:<11} constant within every household ({mm.column_names_to_labels.get(v)})")
check((dm.groupby("folio").size() == dm.groupby("folio").miembros.first()).all(),
      "miembros equals number of person rows per household")
check(L(mm, "s1_05").get(1.0) == "jefe o jefa del hogar", "s1_05==1 is 'jefe o jefa del hogar'")
check((dm[dm.s1_05 == 1].groupby("folio").size() == 1).all()
      and dm[dm.s1_05 == 1].folio.nunique() == dm.folio.nunique(),
      "exactly one head per household")

log("\n2. Value labels used for binary features")
for v, code, want in [("urb_rur", 2.0, "rural"), ("s7_02", 1.0, "alquilada"),
                      ("s7_05", 1.0, "ladrillo/bloques de cemento/hormigón"),
                      ("s7_05", 5.0, "madera"), ("s7_08", 1.0, "tierra"),
                      ("s7_08", 5.0, "cemento"), ("s7_19", 1.0, "si")]:
    check(L(mm, v).get(code) == want, f"{v}=={code:g} -> '{want}'")

log("\n3. Durable goods (Equipamiento) — one record per (household, item)?")
check((de.groupby(["folio", "s6_16cod"]).size() == 1).all(),
      "exactly one row per (folio, s6_16cod) → .first() loses nothing")
check(de.groupby("folio").size().eq(22).all(), "all 22 items recorded for every household")
check(L(me, "s6_16") == {1.0: "Si", 2.0: "No"}, "s6_16: 1=Si (owns), 2=No")
expect = {1: "Catre o cama", 7: "Refrigerador o Freezer", 9: "Computadora",
          10: "Radiograbador", 12: "Televisor", 13: "Reproductor de video, VHS, DVD, etc",
          18: "Ventilador", 22: "Automovil (para uso del hogar"}
for code, want in expect.items():
    check(L(me, "s6_16cod").get(float(code)) == want, f"s6_16cod=={code} -> '{want}'")
for code in (1, 9):
    s = de[(de.s6_16cod == code) & (de.s6_16 == 1)]
    check(s.s6_17.notna().all() and (s.s6_17 >= 1).all(),
          f"item {code}: count s6_17 present and >=1 whenever owned")
n_fridge_nan = int(de[(de.s6_16cod == 7) & (de.s6_16 == 1)].s6_17.isna().sum())
log(f"  [info] fridge owned but count missing: {n_fridge_nan} (irrelevant: fridge is binary)")

log("\n4. Livestock (Pecuaria) — sheep")
check(L(mp, "codb").get("B") == "Ovinos", "codb=='B' -> 'Ovinos' (sheep)")
b = dp[dp.codb == "B"]
check(b.folio.is_unique, "one sheep record per household (sum == value)")
check(((b.s8_05 == 1) == (b.s8_10.notna())).all(),
      "s8_10 (stock last month) present iff s8_05==1 (raised sheep)")
dups = dp[dp.duplicated(["folio", "codb"], keep=False)]
log(f"  [info] duplicate (folio,codb) rows: {len(dups)} — categories {sorted(dups.codb.unique())} (not used)")
log(f"  [info] households in livestock module: {dp.folio.nunique()} of {dm.folio.nunique()}; "
    f"others get sheep=0")
log(f"  [info] sheep stock = s8_10 'CUANTOS ANIMALES TENIA HASTA EL MES ANTERIOR'")

log("\n5. Known approximations (not errors, but not verifiable against the paper)")
log("  - num_kitchens: s7_19 is binary (dedicated kitchen yes/no); paper says 'number'")
log("  - sublease: s7_02==1 'alquilada' (rented); no sublease category exists")
log("  - regions: depto 1–9 (ordinal for trees, dummies for IRIS)")
log(f"  - G_TOTAL_pc == 0 for {int((dm.groupby('folio').G_TOTAL_pc.first() == 0).sum())} household(s)")
log("\nALL CHECKS PASSED")
open(os.path.join(OUT, "data_construction_audit.txt"), "w").write("\n".join(lines) + "\n")
