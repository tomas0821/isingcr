"""Side-by-side maps of empirical vs. simulated equilibrium spin states.

Two entry points:
  - plot_comparison_map: choropleth over real polygons (requires geopandas + a
    GeoDataFrame, as produced by isingcr.ingestion.shapefile_adjacency).
  - plot_network_comparison: node-color scatter over a networkx graph with a
    "pos" attribute (works for the synthetic demo graph, no shapefile needed).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


def plot_comparison_map(gdf, id_col: str, simulated_spins: dict,
                         empirical_col: str = "spin_empirical",
                         savepath: str | Path | None = None):
    """gdf: GeoDataFrame with columns [id_col, empirical_col]. simulated_spins: {id: spin}."""
    import matplotlib.pyplot as plt

    gdf = gdf.copy()
    gdf["simulated"] = gdf[id_col].map(simulated_spins)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    gdf.plot(column=empirical_col, cmap="RdBu", ax=axes[0], edgecolor="black",
              linewidth=0.2, legend=False)
    axes[0].set_title("Empirical (TSE)")
    axes[0].axis("off")

    gdf.plot(column="simulated", cmap="RdBu", ax=axes[1], edgecolor="black",
              linewidth=0.2, legend=False)
    axes[1].set_title("Simulated equilibrium")
    axes[1].axis("off")

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=150)
    return fig


def plot_network_comparison(G, simulated_spins: np.ndarray, node_order: list,
                             empirical_attr: str = "spin_empirical",
                             savepath: str | Path | None = None):
    """G: networkx graph with node attr "pos" and `empirical_attr`.
    simulated_spins/node_order: aligned arrays as returned by graph_to_arrays + run_mc.
    """
    import matplotlib.pyplot as plt
    import networkx as nx

    pos = nx.get_node_attributes(G, "pos")
    empirical = [G.nodes[n][empirical_attr] for n in node_order]
    sim_by_node = dict(zip(node_order, simulated_spins))
    simulated = [sim_by_node[n] for n in node_order]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for ax, values, title in ((axes[0], empirical, "Empirical (TSE)"),
                               (axes[1], simulated, "Simulated equilibrium")):
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3, width=0.5)
        nx.draw_networkx_nodes(G, pos, nodelist=node_order, node_color=values,
                                cmap="RdBu", vmin=-1, vmax=1, node_size=80, ax=ax)
        ax.set_title(title)
        ax.axis("off")

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=150)
    return fig
