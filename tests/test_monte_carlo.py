import numpy as np
import scipy.sparse as sp

from isingcr.simulation.monte_carlo import pooled_temperature_scan, temperature_scan


def _ring_graph(n=10, J_value=1.0):
    rows, cols, data = [], [], []
    for i in range(n):
        j = (i + 1) % n
        rows += [i, j]
        cols += [j, i]
        data += [J_value, J_value]
    return sp.csr_matrix((data, (rows, cols)), shape=(n, n))


def test_temperature_scan_returns_one_result_per_temperature():
    J = _ring_graph(10)
    h = np.zeros(10)
    temps = [0.5, 1.0, 1.5]
    results = temperature_scan(J, h, temps, n_equil=10, n_sweeps=10, seed=0)
    assert [r["T"] for r in results] == temps
    for r in results:
        assert r["energy"].shape == (10,)
        assert r["final_spins"].shape == (10,)


def test_temperature_scan_parallel_matches_serial_shape():
    J = _ring_graph(10)
    h = np.zeros(10)
    temps = [0.5, 1.0]
    serial = temperature_scan(J, h, temps, n_equil=5, n_sweeps=5, seed=0, n_jobs=1)
    parallel = temperature_scan(J, h, temps, n_equil=5, n_sweeps=5, seed=0, n_jobs=2)
    assert len(serial) == len(parallel) == 2


def test_pooled_temperature_scan_pools_across_seeds():
    n, n_seeds = 10, 4
    J = _ring_graph(n)
    h = np.zeros(n)
    temps = [0.5, 1.0]
    pooled = pooled_temperature_scan(J, h, temps, n_seeds=n_seeds,
                                      n_equil=5, n_sweeps=5, seed=0)
    assert len(pooled) == len(temps)
    for p, T in zip(pooled, temps):
        assert p["T"] == T
        assert p["energy"].shape == (n_seeds * 5,)
        assert p["magnetization"].shape == (n_seeds * 5,)
        assert len(p["final_spins_per_seed"]) == n_seeds
        for spins in p["final_spins_per_seed"]:
            assert spins.shape == (n,)


def test_pooled_temperature_scan_seeds_are_actually_independent():
    # Different seed streams -> not all replicates identical (statistically near-certain
    # for a 10-node ring at T=1.0 with independent random inits).
    n = 10
    J = _ring_graph(n)
    h = np.zeros(n)
    pooled = pooled_temperature_scan(J, h, [1.0], n_seeds=5, n_equil=20, n_sweeps=5, seed=0)
    final_spins = pooled[0]["final_spins_per_seed"]
    assert not all(np.array_equal(final_spins[0], s) for s in final_spins[1:])
