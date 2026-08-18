import numpy as np

from isingcr.utils.graph_arrays import graph_to_arrays
from isingcr.utils.synthetic import synthetic_electoral_graph


def test_synthetic_graph_shape_and_attrs():
    G = synthetic_electoral_graph(n_units=30, seed=1, n_relax_sweeps=20)
    assert G.number_of_nodes() == 30
    assert G.number_of_edges() > 0
    for n, d in G.nodes(data=True):
        assert d["spin_empirical"] in (-1, 1)
        assert "pos" in d
        assert "code" in d


def test_synthetic_graph_reproducible_with_seed():
    G1 = synthetic_electoral_graph(n_units=20, seed=5, n_relax_sweeps=10)
    G2 = synthetic_electoral_graph(n_units=20, seed=5, n_relax_sweeps=10)
    spins1 = [G1.nodes[n]["spin_empirical"] for n in sorted(G1.nodes)]
    spins2 = [G2.nodes[n]["spin_empirical"] for n in sorted(G2.nodes)]
    assert spins1 == spins2


def test_synthetic_graph_feeds_graph_to_arrays():
    G = synthetic_electoral_graph(n_units=25, seed=2, n_relax_sweeps=10)
    out = graph_to_arrays(G)
    assert out["J"].shape == (25, 25)
    assert np.allclose(out["J"].toarray(), out["J"].toarray().T)
