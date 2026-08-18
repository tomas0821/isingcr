import geopandas as gpd
from shapely.geometry import box

from isingcr.ingestion.shapefile_adjacency import build_adjacency_graph


def _grid_gdf():
    # 2x2 grid of unit squares: A|B on top row, C|D on bottom row, all touching.
    geoms = {
        "A": box(0, 1, 1, 2),
        "B": box(1, 1, 2, 2),
        "C": box(0, 0, 1, 1),
        "D": box(1, 0, 2, 1),
    }
    gdf = gpd.GeoDataFrame(
        {"id": list(geoms.keys()), "geometry": list(geoms.values())},
        crs="EPSG:5367",
    )
    return gdf


def test_grid_adjacency_topology():
    gdf = _grid_gdf()
    G = build_adjacency_graph(gdf, id_col="id", weight_by="uniform")

    assert set(G.nodes) == {"A", "B", "C", "D"}
    expected_edges = {frozenset(e) for e in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]}
    actual_edges = {frozenset(e) for e in G.edges}
    assert actual_edges == expected_edges
    # A and D only share a corner point, not an edge -> no border, not connected.
    assert not G.has_edge("A", "D")


def test_border_length_weighting():
    gdf = _grid_gdf()
    G = build_adjacency_graph(gdf, id_col="id", weight_by="border_length")
    for _, _, d in G.edges(data=True):
        assert d["border_length_m"] == 1.0  # unit squares -> unit shared edges
        assert d["weight"] == 1.0  # all borders equal -> normalized weight is uniform
