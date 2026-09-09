import networkx as nx
import pandas as pd
import pytest

from isingcr.ingestion.graph_builder import build_electoral_graph


def test_build_electoral_graph_attaches_spin_and_field():
    adjacency = nx.Graph()
    adjacency.add_edge("001", "002")
    adjacency.add_edge("002", "003")

    results = pd.DataFrame({
        "code": ["001", "002", "003"],
        "spin": [1, -1, 1],
        "h_raw": [0.3, -0.1, 0.0],
    })

    G = build_electoral_graph(adjacency, results, h_col="h_raw")
    assert G.nodes["001"]["spin_empirical"] == 1
    assert G.nodes["002"]["h"] == pytest.approx(-0.1)


def test_build_electoral_graph_drops_unmatched_by_default():
    adjacency = nx.Graph()
    adjacency.add_edge("001", "999")  # "999" has no results row

    results = pd.DataFrame({"code": ["001"], "spin": [1]})
    with pytest.warns(UserWarning):
        G = build_electoral_graph(adjacency, results)
    assert set(G.nodes) == {"001"}


def test_build_electoral_graph_raises_when_drop_disabled():
    adjacency = nx.Graph()
    adjacency.add_edge("001", "999")
    results = pd.DataFrame({"code": ["001"], "spin": [1]})
    with pytest.raises(ValueError):
        build_electoral_graph(adjacency, results, drop_unmatched=False)
