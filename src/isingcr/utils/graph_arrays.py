"""The one place networkx graphs get converted into the plain arrays the
simulation engine consumes. Keeping this conversion in `utils` (not in
`simulation`) is what lets `isingcr.simulation` stay free of ingestion
dependencies (networkx/pandas/geopandas) -- see the module docstring in
`isingcr.ingestion.graph_builder`.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import scipy.sparse as sp


def graph_to_arrays(G: nx.Graph, weight_attr: str = "weight", h_attr: str = "h",
                     spin_attr: str = "spin_empirical", default_h: float = 0.0) -> dict:
    """Convert an annotated networkx graph into (J, h, node order, empirical spins).

    Returns
    -------
    dict with:
      "J": scipy.sparse.csr_matrix (N, N), symmetric coupling matrix
      "h": np.ndarray (N,), external field
      "nodes": list, node labels in the order used by J/h/spin_empirical
      "spin_empirical": np.ndarray (N,) int8, ground-truth spins (0 if absent)
    """
    nodes = list(G.nodes)
    index = {n: i for i, n in enumerate(nodes)}
    N = len(nodes)

    rows, cols, data = [], [], []
    for u, v, d in G.edges(data=True):
        w = float(d.get(weight_attr, 1.0))
        i, j = index[u], index[v]
        rows += [i, j]
        cols += [j, i]
        data += [w, w]
    J = sp.csr_matrix((data, (rows, cols)), shape=(N, N)) if data else sp.csr_matrix((N, N))

    h = np.array([float(G.nodes[n].get(h_attr, default_h)) for n in nodes])
    spin_empirical = np.array(
        [int(G.nodes[n].get(spin_attr, 0)) for n in nodes], dtype=np.int8
    )

    return {"J": J, "h": h, "nodes": nodes, "spin_empirical": spin_empirical}
