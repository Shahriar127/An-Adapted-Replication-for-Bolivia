"""
Unit tests for the frozen methodology (METHODOLOGY_REFERENCE.md).

Run:  python3 -m unittest discover -s tests -v      (from Model_Training/)

Expected values in the hand-worked examples were computed by hand and are
written out in the comments, not computed by the code under test.
"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common as C  # noqa: E402


class TestMetricFormulas(unittest.TestCase):
    """[M2]-[M6], published Table 2 (p.534)."""

    def test_hand_example_balanced(self):
        # TP=17 FP=7 FN=7 TN=69, so true poor = TP+FN = 24 and N = 100
        # TA = 86/100 = 0.86
        # PA = 17/24 = 0.708333   UC = 7/24 = 0.291667   LE = 7/24 = 0.291667
        # BPAC = 0.708333 - |0.291667 - 0.291667| = 0.708333
        m = C.metrics_from_counts(17, 7, 7, 69)
        self.assertAlmostEqual(m["TA"], 0.86)
        self.assertAlmostEqual(m["PA"], 17 / 24)
        self.assertAlmostEqual(m["UC"], 7 / 24)
        self.assertAlmostEqual(m["LE"], 7 / 24)
        self.assertAlmostEqual(m["BPAC"], 17 / 24)

    def test_hand_example_unbalanced(self):
        # TP=30 FP=20 FN=10 TN=40, true poor = 40, N = 100
        # TA = 70/100 = 0.70
        # PA = 30/40 = 0.75   UC = 10/40 = 0.25   LE = 20/40 = 0.50
        # BPAC = 0.75 - |0.25 - 0.50| = 0.50
        # (The 2015 TP+FP formula would give PA = 30/50 = 0.60 and
        #  BPAC = 0.60 - |10/50 - 20/50| = 0.40; it must NOT be used.)
        m = C.metrics_from_counts(30, 20, 10, 40)
        self.assertAlmostEqual(m["TA"], 0.70)
        self.assertAlmostEqual(m["PA"], 0.75)
        self.assertAlmostEqual(m["UC"], 0.25)
        self.assertAlmostEqual(m["LE"], 0.50)
        self.assertAlmostEqual(m["BPAC"], 0.50)

    def test_leakage_can_exceed_one(self):
        # [M5], fn 6: TP=5 FP=30 FN=5 TN=60, true poor = 10
        # PA = 0.5  UC = 0.5  LE = 30/10 = 3.0  BPAC = 0.5 - |0.5 - 3.0| = -2.0
        m = C.metrics_from_counts(5, 30, 5, 60)
        self.assertAlmostEqual(m["LE"], 3.0)
        self.assertAlmostEqual(m["BPAC"], -2.0)

    def test_pa_plus_uc_is_one(self):
        rng = np.random.RandomState(0)
        for _ in range(200):
            TP, FP, FN, TN = rng.randint(0, 500, 4)
            if TP + FN == 0:
                continue
            m = C.metrics_from_counts(TP, FP, FN, TN)
            self.assertAlmostEqual(m["PA"] + m["UC"], 1.0)
            self.assertAlmostEqual(m["BPAC"], m["PA"] - abs(m["UC"] - m["LE"]))

    def test_no_true_poor(self):
        # [M8] TP+FN = 0: rates are defined as 0
        m = C.metrics_from_counts(0, 5, 0, 95)
        self.assertEqual((m["PA"], m["UC"], m["LE"], m["BPAC"]), (0.0, 0.0, 0.0, 0.0))

    def test_strict_inequality(self):
        # [M7] poor iff value < line; a value exactly at the line is non-poor
        TP, FP, FN, TN = C.confusion([99, 100, 101], [99, 100, 101], 100)
        self.assertEqual((TP, FP, FN, TN), (1, 0, 0, 2))

    def test_confusion_counts(self):
        y_true = np.array([50, 50, 150, 150, 50])
        y_pred = np.array([50, 150, 50, 150, 50])
        # line 100: true poor = {0,1,4}; predicted poor = {0,2,4}
        # TP = {0,4} = 2, FN = {1} = 1, FP = {2} = 1, TN = {3} = 1
        self.assertEqual(C.confusion(y_true, y_pred, 100), (2, 1, 1, 1))


class TestPublishedTableA1Identities(unittest.TestCase):
    """Every point-estimate row of published Table A1 (p.545-546) must satisfy
    PA + UC = 100 and BPAC = PA - |UC - LE|, which holds only with TP+FN
    denominators. Values are copied verbatim from the paper."""

    ROWS = {  # (TA, PA, UC, LE, BPAC)
        "Bolivia row1 QR(0.42) in-sample half": (83.65, 67.18, 32.82, 33.29, 66.71),
        "Bolivia row5 QR(0.42) rep full":       (82.45, 60.69, 39.30, 33.71, 55.10),
        "East Timor row1 Probit in-sample":     (77.14, 75.08, 24.92, 26.20, 73.79),
        "East Timor row5 Probit rep":           (77.16, 71.41, 28.59, 27.63, 70.45),
        "Malawi row1 QR(0.57) in-sample half":  (80.15, 84.12, 15.88, 16.43, 83.57),
        "Malawi row5 QR(0.57) rep full":        (80.82, 84.88, 15.11, 14.39, 84.17),
    }

    def test_identities(self):
        for name, (_, pa, uc, le, bpac) in self.ROWS.items():
            with self.subTest(row=name):
                self.assertAlmostEqual(pa + uc, 100.0, delta=0.02)
                self.assertAlmostEqual(pa - abs(uc - le), bpac, delta=0.02)

    def test_counts_reproduce_bolivia_row5(self):
        # Counts per 10,000 true poor that are consistent with row 5:
        # TP=6069, FN=3930, FP=3371  ->  PA 60.69, UC 39.30, LE 33.71, BPAC 55.10
        m = C.metrics_from_counts(6069, 3371, 3930, 10_000)
        self.assertAlmostEqual(100 * m["PA"], 60.69, delta=0.01)
        self.assertAlmostEqual(100 * m["UC"], 39.30, delta=0.01)
        self.assertAlmostEqual(100 * m["LE"], 33.71, delta=0.01)
        self.assertAlmostEqual(100 * m["BPAC"], 55.10, delta=0.01)


class TestBootstrap(unittest.TestCase):
    def test_vectorised_equals_scalar(self):
        rng = np.random.RandomState(1)
        y = rng.lognormal(5.5, 0.8, 300); yp = y * rng.lognormal(0, 0.4, 300)
        line = float(np.percentile(y, 24.2))
        idx = C.boot_indices(300, B=50, seed=3)
        boot = C.bootstrap_metrics(y, yp, line, idx)
        for b in range(50):
            ref = C.targeting_metrics(y[idx[b]], yp[idx[b]], line)
            for k in C.METRICS:
                self.assertAlmostEqual(boot[k][b], ref[k])

    def test_indices_are_shared_and_reproducible(self):
        # [S5] same seed gives the same resamples for every model
        self.assertTrue(np.array_equal(C.boot_indices(100), C.boot_indices(100)))
        self.assertEqual(C.boot_indices(100).shape, (C.BOOTSTRAP_REPS, 100))

    def test_ci_and_se(self):
        x = np.arange(1001, dtype=float)              # 0..1000
        lo, hi = C.ci(x)
        self.assertAlmostEqual(lo, 25.0); self.assertAlmostEqual(hi, 975.0)
        self.assertAlmostEqual(C.boot_se({"a": np.array([1., 3.])})["a"], np.sqrt(2))


class TestSplits(unittest.TestCase):
    def test_paper_split(self):
        # [S1] two N/2 draws with replacement: sizes N//2, duplicates allowed
        tr, te = C.paper_split_idx(4086, 42)
        self.assertEqual((len(tr), len(te)), (2043, 2043))
        self.assertLess(len(np.unique(tr)), 2043)
        self.assertTrue(np.array_equal(tr, C.paper_split_idx(4086, 42)[0]))

    def test_disjoint_split(self):
        tr, te = C.disjoint_split_idx(4086, 42)
        self.assertEqual(len(np.intersect1d(tr, te)), 0)
        self.assertEqual(len(tr) + len(te), 4086)


class TestModelConfig(unittest.TestCase):
    def test_frozen_settings(self):
        self.assertEqual(C.N_TREES, 500)                                     # [F2]
        self.assertEqual(C.BOOTSTRAP_REPS, 1000)                             # [S4]
        self.assertIsNone(C.MODEL_CONFIG["QRF"]["max_samples_leaf"])        # [F6]
        self.assertEqual(C.MODEL_CONFIG["RandomForest"]["min_samples_leaf"], 5)   # [F5]
        self.assertAlmostEqual(C.IRIS_QUANTILE, 0.42)                        # [S6]
        self.assertEqual(len(C.QRF_QUANTILE_GRID), 99)                       # [S8]
        self.assertEqual(C.QRF_QUANTILE_GRID[40], 0.41)

    def test_mtry_matches_r_default(self):
        # [F3] R: max(floor(21/3), 1) = 7; sklearn max_features=1/3 -> 7
        p = len(C.FEATURE_COLS)
        self.assertEqual(max(int(np.floor(p / 3)), 1), 7)
        self.assertEqual(max(1, int(C.MODEL_CONFIG["QRF"]["max_features"] * p)), 7)


class TestSESelectionUsesTrainingOnly(unittest.TestCase):
    """[S7] OOB selection must not depend on the test sample."""

    def test_selection_ignores_test(self):
        rng = np.random.RandomState(0)
        X = rng.normal(size=(400, 4)); y = np.exp(5 + X[:, 0] + 0.5 * rng.normal(size=400))
        line = float(np.percentile(y, 24.2))
        tr, te = np.arange(200), np.arange(200, 400)
        grid = [0.3, 0.4, 0.5]
        rf = C.make_model("RandomForest").set_params(n_estimators=50).fit(X[tr], y[tr])
        qrf = C.make_model("QRF").set_params(n_estimators=50).fit(X[tr], y[tr])
        oob = C.se_oob_predictions(rf, qrf, X[tr], grid)
        lab1, _, _ = C.select_se(y[tr], oob, line, grid)
        y_scrambled = y.copy(); y_scrambled[te] = rng.permutation(y[te]) * 10
        lab2, _, _ = C.select_se(y_scrambled[tr], oob, line, grid)
        self.assertEqual(lab1, lab2)
        self.assertEqual(oob.shape, (200, 1 + len(grid)))

    def test_tie_break_first_wins(self):
        y = np.array([1., 2., 3., 4.])
        preds = np.column_stack([y, y, y])          # every candidate perfect -> tie
        lab, j, _ = C.select_se(y, preds, 2.5, grid=[0.3, 0.4])
        self.assertEqual((lab, j), ("RF", 0))       # [S10]


if __name__ == "__main__":
    unittest.main()
