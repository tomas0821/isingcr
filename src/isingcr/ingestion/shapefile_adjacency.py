"""Extract a spatial adjacency graph from a Costa Rican canton/distrito shapefile.

Costa Rica's official cadastral CRS is CRTM05 (EPSG:5367); geometry predicates
(touches, shared-border length) are computed in a projected CRS so lengths are
in meters, not degrees.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import networkx as nx

CRTM05 = "EPSG:5367"


def load_shapefile(path: str | Path, id_col: str, target_crs: str = CRTM05) -> gpd.GeoDataFrame:
    """Load a shapefile/GeoJSON and reproject to a metric CRS."""
    gdf = gpd.read_file(path)
    if id_col not in gdf.columns:
        raise ValueError(f"id_col={id_col!r} not found. Available columns: {list(gdf.columns)}")
    if gdf.crs is None:
        raise ValueError(f"{path} has no CRS defined; cannot safely reproject.")
    return gdf.to_crs(target_crs)


def build_adjacency_graph(gdf: gpd.GeoDataFrame, id_col: str,
                           weight_by: str = "uniform") -> nx.Graph:
    """Connect polygons that share a border into a networkx Graph.

    Parameters
    ----------
    gdf : GeoDataFrame in a projected (metric) CRS, one row per geographic unit.
    id_col : column used as node identifier.
    weight_by : "uniform" (all edges weight 1.0) or "border_length" (edge weight
        proportional to the shared-border length, normalized so the mean weight
        is 1.0 -- a first cut at the "weight by similarity" extension the spec
        calls for; swap in demographic/economic similarity the same way.

    Returns
    -------
    networkx.Graph with edge attribute "weight" and "border_length_m".
    """
    if weight_by not in ("uniform", "border_length"):
        raise ValueError(f"weight_by must be 'uniform' or 'border_length', got {weight_by!r}")

    gdf = gdf.reset_index(drop=True)
    G = nx.Graph()
    for _, row in gdf.iterrows():
        G.add_node(row[id_col])

    sindex = gdf.sindex
    lengths = []
    edges = []
    for i, geom_i in enumerate(gdf.geometry):
        for j in sindex.query(geom_i, predicate="intersects"):
            if j <= i:
                continue
            geom_j = gdf.geometry.iloc[j]
            if not (geom_i.touches(geom_j) or geom_i.overlaps(geom_j)):
                continue
            shared = geom_i.intersection(geom_j)
            length = getattr(shared, "length", 0.0)
            if length <= 0:
                continue
            edges.append((gdf[id_col].iloc[i], gdf[id_col].iloc[j], length))
            lengths.append(length)

    mean_length = sum(lengths) / len(lengths) if lengths else 1.0
    for u, v, length in edges:
        weight = 1.0 if weight_by == "uniform" else length / mean_length
        G.add_edge(u, v, weight=weight, border_length_m=length)

    isolated = list(nx.isolates(G))
    if isolated:
        import warnings
        warnings.warn(
            f"{len(isolated)} node(s) have no detected neighbors (possible islands "
            f"or geometry gaps): {isolated[:10]}{'...' if len(isolated) > 10 else ''}"
        )
    return G
