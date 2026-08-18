import warnings

import numpy as np
import scipy.sparse as sp

from isingcr.simulation.dynamics import glauber_step
from isingcr.simulation.ising_model import IsingModel
from isingcr.simulation.monte_carlo import run_mc


def _ring_graph(n=20, J_value=1.0):
    rows, cols, data = [], [], []
    for i in range(n):
        j = (i + 1) % n
        rows += [i, j]
        cols += [j, i]
        data += [J_value, J_value]
    return sp.csr_matrix((data, (rows, cols)), shape=(n, n))


def test_low_temperature_converges_to_ferromagnetic_order():
    n = 30
    J = _ring_graph(n, J_value=1.0)
    h = np.zeros(n)
    rng = np.random.default_rng(0)
    model = IsingModel(J, h, rng=rng)
    result = run_mc(model, T=0.05, n_equil=200, n_sweeps=50, dynamics="glauber", rng=rng)
    assert abs(result["magnetization"][-1]) > 0.9


def test_high_temperature_is_disordered():
    n = 60
    J = _ring_graph(n, J_value=1.0)
    h = np.zeros(n)
    rng = np.random.default_rng(1)
    model = IsingModel(J, h, rng=rng)
    result = run_mc(model, T=50.0, n_equil=100, n_sweeps=200, dynamics="glauber", rng=rng)
    assert abs(np.mean(result["magnetization"])) < 0.3


def test_metropolis_and_glauber_both_reach_ground_state_with_field():
    n = 10
    J = sp.csr_matrix((n, n))  # no coupling
    h = np.full(n, 2.0)  # strong uniform field favors all-up
    for dynamics in ("metropolis", "glauber"):
        rng = np.random.default_rng(3)
        model = IsingModel(J, h, spins=-np.ones(n, dtype=np.int8), rng=rng)
        run_mc(model, T=0.1, n_equil=50, n_sweeps=1, dynamics=dynamics, rng=rng)
        assert np.all(model.spins == 1)


def test_glauber_step_no_overflow_warning_at_low_T_large_dE():
    # A large, strongly unfavorable dE at very low T used to overflow exp(dE/T)
    # in the naive sigmoid -- mathematically harmless (p_flip -> 0) but noisy.
    n = 6
    rows = list(range(n - 1))
    cols = list(range(1, n))
    data = [100.0] * (n - 1)  # strong coupling -> large |dE|
    J = sp.csr_matrix((data + data, (rows + cols, cols + rows)), shape=(n, n))
    h = np.zeros(n)
    rng = np.random.default_rng(0)
    model = IsingModel(J, h, spins=np.ones(n, dtype=np.int8), rng=rng)  # all-aligned: flipping is very unfavorable

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        flipped = glauber_step(model, 0, T=0.01, rng=rng)
    assert not flipped  # p_flip ~ 0, should essentially never accept


def test_glauber_step_no_overflow_warning_at_low_T_favorable_flip():
    n = 6
    rows = list(range(n - 1))
    cols = list(range(1, n))
    data = [100.0] * (n - 1)
    J = sp.csr_matrix((data + data, (rows + cols, cols + rows)), shape=(n, n))
    h = np.zeros(n)
    rng = np.random.default_rng(0)
    # site 0 misaligned with its aligned neighbors -> flipping it is very favorable
    spins = np.ones(n, dtype=np.int8)
    spins[0] = -1
    model = IsingModel(J, h, spins=spins, rng=rng)

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        flipped = glauber_step(model, 0, T=0.01, rng=rng)
    assert flipped  # p_flip ~ 1, should essentially always accept
