"""Single-spin update rules (Metropolis and Glauber) for IsingModel."""

from __future__ import annotations

import numpy as np

from .ising_model import IsingModel


def metropolis_step(model: IsingModel, i: int, T: float, rng: np.random.Generator) -> bool:
    """Metropolis acceptance: flip if dE <= 0, else with probability exp(-dE/T).

    T <= 0 is treated as the zero-temperature limit: flip only if it lowers energy.
    Returns True if the spin was flipped.
    """
    dE = model.delta_energy(i)
    if T <= 0:
        accept = dE < 0
    else:
        accept = dE <= 0 or rng.random() < np.exp(-dE / T)
    if accept:
        model.flip(i)
    return accept


def glauber_step(model: IsingModel, i: int, T: float, rng: np.random.Generator) -> bool:
    """Glauber (heat-bath) dynamics: flip with probability 1 / (1 + exp(dE/T)).

    T <= 0 is treated as the zero-temperature limit: flip only if it lowers energy
    (ties broken by not flipping).
    Returns True if the spin was flipped.
    """
    dE = model.delta_energy(i)
    if T <= 0:
        accept = dE < 0
    else:
        # Numerically stable sigmoid: naive exp(dE/T) overflows float64 for a
        # strongly unfavorable flip (large dE) at low T -- harmless mathematically
        # (1/(1+inf) -> 0, the correct answer) but noisy (RuntimeWarning) and worth
        # avoiding since this project's finite-size scans push T down to 0.05.
        x = dE / T
        p_flip = np.exp(-x) / (1.0 + np.exp(-x)) if x >= 0 else 1.0 / (1.0 + np.exp(x))
        accept = rng.random() < p_flip
    if accept:
        model.flip(i)
    return accept


DYNAMICS = {"metropolis": metropolis_step, "glauber": glauber_step}
