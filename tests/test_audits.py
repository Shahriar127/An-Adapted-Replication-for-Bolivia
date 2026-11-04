"""Tests for the A8 / Phase 2-3 audit code (not part of the frozen pipeline)."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from a8_qrf_audit import RQuantregForest, FROZEN_NODE  # noqa: E402
import cv_qr_baseline as CV  # noqa: E402


class TestRQuantregForestEmulation(unittest.TestCase):
    """Behaviour of R quantregForest 1.3-5 (verbatim source): one stored response
    per leaf, drawn from all training rows in the leaf; type-7 quantile over trees."""

    @classmethod
    def setUpClass(cls):
        rng = np.random.RandomState(0)
        cls.X = rng.normal(size=(300, 3)); cls.y = np.exp(4 + cls.X[:, 0] + 0.3 * rng.normal(size=300))
        cls.m = RQuantregForest(FROZEN_NODE, 1)
        cls.m.rf.set_params(n_estimators=30)
        cls.m.fit(cls.X, cls.y)

    def test_one_value_per_leaf_from_training_responses(self):
        for b in range(5):
            leaves = np.unique(self.m.train_leaves[:, b])
            vals = self.m.values[b][leaves]
            self.assertTrue(np.all(np.isfinite(vals)))
            for leaf, v in zip(leaves, vals):          # value belongs to a row in that leaf
                rows = np.where(self.m.train_leaves[:, b] == leaf)[0]
                self.assertIn(v, set(self.y[rows]))

    def test_prediction_is_type7_quantile_over_trees(self):
        x = self.X[:3]
        leaves = self.m.rf.apply(x.astype(np.float32))
        vals = np.column_stack([self.m.values[b][leaves[:, b]] for b in range(leaves.shape[1])])
        expect = np.quantile(vals, 0.41, axis=1, method="linear")
        np.testing.assert_allclose(self.m.predict(x, [0.41])[:, 0], expect)

    def test_oob_excludes_inbag_trees(self):
        self.assertEqual(self.m.inbag.shape, (300, 30))
        self.assertTrue((self.m.inbag.sum(0) == 300).all())   # n draws per tree


class TestCVFoldJob(unittest.TestCase):
    def test_fold_job_uses_only_given_rows(self):
        rng = np.random.RandomState(0)
        X = rng.normal(size=(150, 3)); y = np.exp(4 + X[:, 0])
        a, b = np.arange(80), np.arange(80, 120)          # rows 120..149 belong to neither
        out1 = CV.fold_job(X, y, a, b, [50.0], [37])
        X2, y2 = X.copy(), y.copy()
        X2[120:] = rng.normal(size=(30, 3)) * 100; y2[120:] = 1e6   # perturb unused rows
        out2 = CV.fold_job(X2, y2, a, b, [50.0], [37])
        np.testing.assert_allclose(out1[:, 37], out2[:, 37])
        self.assertTrue(np.isnan(out1[0, 0]))    # quantiles outside `cols` are not evaluated

    def test_first_best_tie_break(self):
        s = np.zeros(len(CV.GRID)); s[[10, 20]] = 1.0
        self.assertEqual(CV.first_best(s), CV.GRID[10])


if __name__ == "__main__":
    unittest.main()
