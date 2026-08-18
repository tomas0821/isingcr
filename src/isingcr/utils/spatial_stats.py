"""Plain spatial-autocorrelation diagnostics on the real adjacency graph.

Deliberately independent of the MC engine: Moran's I answers "is the real,
empirical data actually spatially clustered on this graph" directly from the
data, in milliseconds -- the natural first check before asking whether an
Ising fit *should* be expected to find geographic structure in a given
election. See CLAUDE.md's discussion of Ising-model vs. plain spatial
statistics: this is the "regular data analysis" side of that comparison,
used here as a diagnostic for the model rather than a replacement for it.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def morans_i(J: sp.spmatrix, values: np.ndarray) -> float:
    """Moran's I spatial autocorrelation of `values` over the graph in `J`.

    I = (n/W) * (dev^T J dev) / (dev^T dev), dev = values - mean(values),
    W = sum of all edge weights. Positive I = neighbors tend to share similar
    values (spatial clustering); near 0 = no spatial structure; negative =
    neighbors tend to differ (checkerboard-like).
    """
    J = J.tocsr()
    n = J.shape[0]
    W = float(J.sum())
    dev = np.asarray(values, dtype=np.float64) - np.mean(values)
    denom = float(dev @ dev)
    if W == 0 or denom == 0:
        return float("nan")
    numerator = float(dev @ J.dot(dev))
    return (n / W) * (numerator / denom)


def morans_i_test(J: sp.spmatrix, values: np.ndarray, n_permutations: int = 999,
                   rng: np.random.Generator | None = None) -> dict:
    """Moran's I plus a permutation test: shuffle `values` across nodes (J fixed)
    `n_permutations` times and see how extreme the real I is against that null.

    Returns {"I", "expected_I" (the -1/(n-1) null-randomization expectation),
    "p_value" (two-sided, fraction of permutations at least as extreme),
    "z_score" (against the permutation null's own mean/std)}.
    """
    rng = rng if rng is not None else np.random.default_rng()
    n = J.shape[0]
    observed = morans_i(J, values)

    permuted = np.empty(n_permutations)
    values = np.asarray(values, dtype=np.float64)
    for k in range(n_permutations):
        permuted[k] = morans_i(J, rng.permutation(values))

    p_value = float(np.mean(np.abs(permuted) >= abs(observed)))
    z_score = float((observed - permuted.mean()) / permuted.std()) if permuted.std() > 0 else float("nan")
    return {
        "I": observed,
        "expected_I": -1.0 / (n - 1),
        "p_value": p_value,
        "z_score": z_score,
    }
