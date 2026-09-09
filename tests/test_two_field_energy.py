import numpy as np
import pytest
import scipy.sparse as sp

from isingcr.simulation.ising_model import IsingModel
from isingcr.simulation.two_field_energy import combine_fields, two_field_energy


def _triangle_J():
    # 3-node ring (triangle), uniform ferromagnetic coupling J=1 -- same
    # fixture as tests/test_ising_model.py's _triangle_model, so the
    # all-aligned energy (-3.0) check below is directly comparable.
    rows = [0, 1, 1, 2, 2, 0]
    cols = [1, 0, 2, 1, 0, 2]
    data = [1.0] * 6
    return sp.csr_matrix((data, (rows, cols)), shape=(3, 3))


def test_combine_fields_is_weighted_sum():
    h_pol = np.array([1.0, -1.0, 0.5])
    h_soc = np.array([0.2, 0.2, -0.4])
    combined = combine_fields(h_pol, h_soc, lambda_pol=2.0, lambda_soc=0.5)
    assert np.allclose(combined, 2.0 * h_pol + 0.5 * h_soc)


def test_combine_fields_rejects_mismatched_shapes():
    with pytest.raises(ValueError):
        combine_fields(np.zeros(3), np.zeros(4), lambda_pol=1.0, lambda_soc=1.0)


def test_two_field_energy_matches_manual_hamiltonian():
    J = _triangle_J()
    spins = np.array([1, -1, 1], dtype=np.int8)
    h_pol = np.array([1.0, 0.0, -1.0])
    h_soc = np.array([0.0, 1.0, 1.0])
    lambda_pol, lambda_soc = 1.5, 0.5

    s = spins.astype(np.float64)
    expected_coupling = -0.5 * s @ J.dot(s)
    expected_field = -(lambda_pol * h_pol + lambda_soc * h_soc) @ s
    expected = expected_coupling + expected_field

    got = two_field_energy(J, spins, h_pol, h_soc, lambda_pol, lambda_soc)
    assert got == pytest.approx(expected)


def test_two_field_energy_all_aligned_no_field_is_minus_three():
    # Same reference point as test_ising_model.py::test_energy_all_aligned_is_minimal.
    J = _triangle_J()
    spins = np.array([1, 1, 1], dtype=np.int8)
    e = two_field_energy(J, spins, np.zeros(3), np.zeros(3), lambda_pol=1.0, lambda_soc=1.0)
    assert e == pytest.approx(-3.0)


def test_two_field_energy_reduces_to_single_field_when_lambda_soc_zero():
    # Physically, lambda_soc=0 must be indistinguishable from IsingModel's
    # existing single-field Hamiltonian with h = lambda_pol * h_pol.
    J = _triangle_J()
    spins = np.array([1, 1, -1], dtype=np.int8)
    h_pol = np.array([0.3, -0.2, 0.7])
    h_soc = np.array([5.0, -5.0, 5.0])  # must have zero effect when lambda_soc=0
    lambda_pol = 2.0

    two_field = two_field_energy(J, spins, h_pol, h_soc, lambda_pol, lambda_soc=0.0)
    single = IsingModel(J, lambda_pol * h_pol, spins=spins.copy()).energy()
    assert two_field == pytest.approx(single)


def test_two_field_energy_symmetric_under_swapping_pol_and_soc():
    J = _triangle_J()
    spins = np.array([-1, 1, 1], dtype=np.int8)
    hA = np.array([0.4, -0.6, 0.1])
    hB = np.array([-0.3, 0.2, 0.5])
    e1 = two_field_energy(J, spins, hA, hB, lambda_pol=1.2, lambda_soc=0.8)
    e2 = two_field_energy(J, spins, hB, hA, lambda_pol=0.8, lambda_soc=1.2)
    assert e1 == pytest.approx(e2)
