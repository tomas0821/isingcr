import numpy as np
import pytest
import scipy.sparse as sp

from isingcr.simulation.ising_model import IsingModel


def _triangle_model(spins=None):
    # 3-node ring (triangle), uniform ferromagnetic coupling J=1, no field.
    rows = [0, 1, 1, 2, 2, 0]
    cols = [1, 0, 2, 1, 0, 2]
    data = [1.0] * 6
    J = sp.csr_matrix((data, (rows, cols)), shape=(3, 3))
    h = np.zeros(3)
    rng = np.random.default_rng(0)
    return IsingModel(J, h, spins=spins, rng=rng)


def test_energy_all_aligned_is_minimal():
    model = _triangle_model(spins=np.array([1, 1, 1], dtype=np.int8))
    # 3 edges, each contributes -1*1*1 = -1 -> E = -3
    assert model.energy() == pytest.approx(-3.0)


def test_delta_energy_matches_brute_force_difference():
    rng = np.random.default_rng(1)
    model = _triangle_model(spins=np.array([1, -1, 1], dtype=np.int8))
    for i in range(3):
        e_before = model.energy()
        predicted_dE = model.delta_energy(i)
        # brute force: flip, measure, flip back
        model.spins[i] *= -1
        model._local_field = model.J.dot(model.spins.astype(np.float64)) + model.h
        e_after = model.energy()
        model.spins[i] *= -1
        model._local_field = model.J.dot(model.spins.astype(np.float64)) + model.h
        assert predicted_dE == pytest.approx(e_after - e_before)


def test_flip_updates_local_field_incrementally():
    model = _triangle_model(spins=np.array([1, 1, -1], dtype=np.int8))
    model.flip(0)
    expected_field = model.J.dot(model.spins.astype(np.float64)) + model.h
    assert np.allclose(model._local_field, expected_field)


def test_magnetization_bounds():
    model = _triangle_model(spins=np.array([1, 1, 1], dtype=np.int8))
    assert model.magnetization() == pytest.approx(1.0)
    model = _triangle_model(spins=np.array([1, -1, 1], dtype=np.int8))
    assert model.magnetization() == pytest.approx(1.0 / 3.0)


def test_field_only_system():
    # No coupling; field alone determines the ground state.
    J = sp.csr_matrix((3, 3))
    h = np.array([1.0, -1.0, 0.5])
    model = IsingModel(J, h, spins=np.array([-1, 1, -1], dtype=np.int8))
    # site 0: spin -1 but h>0 (field wants +1) -> flipping is favorable (dE<0)
    assert model.delta_energy(0) < 0
    # site 1: spin +1 but h<0 (field wants -1) -> flipping is favorable (dE<0)
    assert model.delta_energy(1) < 0
    # site 2: spin -1 and h>0 (field wants +1) -> flipping is favorable (dE<0)
    assert model.delta_energy(2) < 0
