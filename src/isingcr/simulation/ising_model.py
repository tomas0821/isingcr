"""Core Ising Hamiltonian on an arbitrary weighted graph.

This module has no knowledge of elections, geography, or pandas/networkx/geopandas.
It operates purely on a sparse coupling matrix J and field vector h, so the same
engine works for any graph topology and can be swapped onto an HPC backend without
touching the data-ingestion layer.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


class IsingModel:
    """Ising system H = -sum_<ij> J_ij s_i s_j - sum_i h_i s_i on a sparse graph.

    Parameters
    ----------
    J : scipy.sparse matrix, shape (N, N)
        Symmetric coupling matrix (edge weights). Diagonal is ignored/assumed zero.
    h : np.ndarray, shape (N,)
        External field per site.
    spins : np.ndarray, shape (N,), optional
        Initial spin configuration (+1/-1 int8). Random if omitted.
    rng : np.random.Generator, optional
    """

    __slots__ = ("N", "J", "h", "spins", "rng", "_local_field")

    def __init__(self, J: sp.spmatrix, h: np.ndarray, spins: np.ndarray | None = None,
                 rng: np.random.Generator | None = None):
        J = J.tocsr()
        N = J.shape[0]
        if J.shape != (N, N):
            raise ValueError(f"J must be square, got {J.shape}")
        h = np.asarray(h, dtype=np.float64)
        if h.shape != (N,):
            raise ValueError(f"h must have shape ({N},), got {h.shape}")

        self.N = N
        self.J = J
        self.h = h
        self.rng = rng if rng is not None else np.random.default_rng()

        if spins is None:
            spins = self.rng.choice(np.array([-1, 1], dtype=np.int8), size=N)
        else:
            spins = np.asarray(spins, dtype=np.int8)
            if spins.shape != (N,):
                raise ValueError(f"spins must have shape ({N},), got {spins.shape}")
        self.spins = spins

        # Local field h_i + sum_j J_ij s_j, maintained incrementally under flips.
        self._local_field = self.J.dot(self.spins.astype(np.float64)) + self.h

    def local_field(self, i: int) -> float:
        return float(self._local_field[i])

    def delta_energy(self, i: int) -> float:
        """Energy cost of flipping spin i: E(flipped) - E(current)."""
        return 2.0 * self.spins[i] * self._local_field[i]

    def flip(self, i: int) -> None:
        """Flip spin i and incrementally update neighbors' local fields (O(degree))."""
        delta_s = -2.0 * self.spins[i]
        self.spins[i] = -self.spins[i]
        start, end = self.J.indptr[i], self.J.indptr[i + 1]
        nbrs = self.J.indices[start:end]
        weights = self.J.data[start:end]
        self._local_field[nbrs] += weights * delta_s

    def energy(self) -> float:
        s = self.spins.astype(np.float64)
        coupling_term = -0.5 * s @ self.J.dot(s)
        field_term = -self.h @ s
        return float(coupling_term + field_term)

    def magnetization(self) -> float:
        """Mean spin per site, in [-1, 1]."""
        return float(np.mean(self.spins))

    def reset_spins(self, spins: np.ndarray | None = None) -> None:
        if spins is None:
            spins = self.rng.choice(np.array([-1, 1], dtype=np.int8), size=self.N)
        self.spins = np.asarray(spins, dtype=np.int8)
        self._local_field = self.J.dot(self.spins.astype(np.float64)) + self.h
