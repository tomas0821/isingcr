import networkx as nx
import numpy as np

from isingcr.utils.graph_arrays import graph_to_arrays


def test_graph_to_arrays_shapes_and_symmetry():
    G = nx.Graph()
    G.add_node("A", h=0.5, spin_empirical=1)
    G.add_node("B", h=-0.2, spin_empirical=-1)
    G.add_node("C", h=0.0, spin_empirical=1)
    G.add_edge("A", "B", weight=2.0)
    G.add_edge("B", "C", weight=1.0)

    out = graph_to_arrays(G)
    J, h, nodes, empirical = out["J"], out["h"], out["nodes"], out["spin_empirical"]

    assert J.shape == (3, 3)
    assert np.allclose(J.toarray(), J.toarray().T)  # symmetric
    assert h.shape == (3,)
    assert list(nodes) == ["A", "B", "C"]
    assert np.array_equal(empirical, np.array([1, -1, 1], dtype=np.int8))

    i, j = nodes.index("A"), nodes.index("B")
    assert J[i, j] == 2.0


def test_graph_to_arrays_defaults_missing_attrs():
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0, 1)  # no weight attr -> defaults to 1.0

    out = graph_to_arrays(G)
    assert out["h"].tolist() == [0.0, 0.0]
    assert out["spin_empirical"].tolist() == [0, 0]
    assert out["J"][0, 1] == 1.0
