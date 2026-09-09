"""Combine spatial adjacency + electoral results into one annotated networkx graph.

This is the seam between data ingestion (pandas/geopandas/networkx) and the
simulation engine (scipy sparse arrays): see `isingcr.utils.graph_arrays.graph_to_arrays`
for the conversion step, kept in its own module so simulation code never imports
networkx/pandas/geopandas directly.
"""

from __future__ import annotations

import warnings

import networkx as nx
import pandas as pd


def build_electoral_graph(adjacency_graph: nx.Graph, results_df: pd.DataFrame,
                           code_col: str = "code", spin_col: str = "spin",
                           h_col: str | None = None, default_h: float = 0.0,
                           drop_unmatched: bool = True) -> nx.Graph:
    """Attach empirical spin/field data to each node of a spatial adjacency graph.

    Parameters
    ----------
    adjacency_graph : output of `build_adjacency_graph`, nodes keyed by geographic code.
    results_df : must contain `code_col` and `spin_col` (see `binarize_votes`).
    h_col : optional column in results_df to use as the external field h_i
        (e.g. a rescaled incumbency/margin score). Falls back to `default_h`.
    drop_unmatched : drop graph nodes with no matching row in results_df (True)
        or raise (False).

    Returns
    -------
    A copy of `adjacency_graph` with node attributes "spin_empirical" and "h".
    """
    lookup = results_df.set_index(code_col)
    G = adjacency_graph.copy()

    unmatched = [n for n in G.nodes if n not in lookup.index]
    if unmatched:
        msg = f"{len(unmatched)} adjacency node(s) have no matching results row: {unmatched[:10]}"
        if drop_unmatched:
            warnings.warn(msg + " -- dropping them.")
            G.remove_nodes_from(unmatched)
        else:
            raise ValueError(msg)

    for node in G.nodes:
        row = lookup.loc[node]
        G.nodes[node]["spin_empirical"] = int(row[spin_col])
        G.nodes[node]["h"] = float(row[h_col]) if h_col else default_h

    return G
