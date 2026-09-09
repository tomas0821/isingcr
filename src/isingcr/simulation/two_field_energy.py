"""Two-field extension of the Hamiltonian for the political/social-development scan.

E(s) = -sum_<ij> J_ij s_i s_j - sum_i (lambda_pol h_i^pol + lambda_soc h_i^soc) s_i

Deliberately kept separate from `IsingModel`, whose H = -sum J s s - sum h s
and O(degree) `flip()` stay exactly as they were -- every existing 1D scan
script constructs `IsingModel(J, h, ...)` with a single field array, and nothing
here changes that signature or behavior. Once lambda_pol/lambda_soc are fixed
for one scan point, the two weighted fields collapse into a single effective
field (`combine_fields`), which is physically identical to a one-field system
-- so the existing, already-tested Monte Carlo engine (`temperature_scan`,
`pooled_temperature_scan`) needs no changes either; a 3D scan is just a loop
over `combine_fields(...)` results feeding the unmodified engine.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def combine_fields(h_pol: np.ndarray, h_soc: np.ndarray,
                    lambda_pol: float, lambda_soc: float) -> np.ndarray:
    """h_eff = lambda_pol * h_pol + lambda_soc * h_soc.

    The single effective field `IsingModel`/`temperature_scan` already know
    how to consume -- this is the only integration point the 3D scan needs.
    """
    h_pol = np.asarray(h_pol, dtype=np.float64)
    h_soc = np.asarray(h_soc, dtype=np.float64)
    if h_pol.shape != h_soc.shape:
        raise ValueError(f"h_pol shape {h_pol.shape} != h_soc shape {h_soc.shape}")
    return lambda_pol * h_pol + lambda_soc * h_soc


def two_field_energy(J: sp.spmatrix, spins: np.ndarray, h_pol: np.ndarray, h_soc: np.ndarray,
                      lambda_pol: float, lambda_soc: float) -> float:
    """Direct (non-incremental) evaluation of E(s) with two independently
    weighted fields, for verification/logging rather than the MC inner loop.

    Matches `IsingModel.energy()`'s coupling_term/field_term split exactly
    when `combine_fields(h_pol, h_soc, lambda_pol, lambda_soc)` is passed to
    `IsingModel` instead -- see `tests/test_two_field_energy.py`.
    """
    s = np.asarray(spins, dtype=np.float64)
    coupling_term = -0.5 * s @ J.dot(s)
    h_eff = combine_fields(h_pol, h_soc, lambda_pol, lambda_soc)
    field_term = -h_eff @ s
    return float(coupling_term + field_term)
