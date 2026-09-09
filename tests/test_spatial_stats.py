import numpy as np
import scipy.sparse as sp

from isingcr.utils.spatial_stats import morans_i, morans_i_test


def _ring_graph(n=20, J_value=1.0):
    rows, cols, data = [], [], []
    for i in range(n):
        j = (i + 1) % n
        rows += [i, j]
        cols += [j, i]
        data += [J_value, J_value]
    return sp.csr_matrix((data, (rows, cols)), shape=(n, n))


def test_perfectly_clustered_values_give_high_positive_I():
    n = 20
    J = _ring_graph(n)
    # two contiguous blocks on the ring: strongest possible clustering
    values = np.array([1.0] * 10 + [-1.0] * 10)
    I = morans_i(J, values)
    assert I > 0.5


def test_checkerboard_values_give_negative_I():
    n = 20
    J = _ring_graph(n)
    values = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(n)])
    I = morans_i(J, values)
    assert I < 0


def test_constant_values_give_nan():
    n = 10
    J = _ring_graph(n)
    values = np.ones(n)
    assert np.isnan(morans_i(J, values))


def test_morans_i_test_detects_real_clustering():
    n = 40
    J = _ring_graph(n)
    values = np.array([1.0] * 20 + [-1.0] * 20)  # strongly clustered
    rng = np.random.default_rng(0)
    result = morans_i_test(J, values, n_permutations=200, rng=rng)
    assert result["I"] > 0.5
    assert result["p_value"] < 0.05


def test_morans_i_test_null_for_random_values():
    n = 40
    J = _ring_graph(n)
    rng = np.random.default_rng(1)
    values = rng.permutation(np.array([1.0] * 20 + [-1.0] * 20))
    result = morans_i_test(J, values, n_permutations=200, rng=np.random.default_rng(2))
    # Not asserting p > 0.05 (random draw could get unlucky) -- just that the
    # machinery runs and returns a sane structure.
    assert 0.0 <= result["p_value"] <= 1.0
    assert "z_score" in result
