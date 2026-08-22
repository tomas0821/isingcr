#!/usr/bin/env python3
"""How much of the real map's energetic favorability is geography vs. predisposition?

The canton and distrito ablations (run_ablation.py, run_distrito_ablation.py)
answer the geography-vs-predisposition question via a classification-accuracy
proxy: does adding h improve best-fit alignment with the real map? That's a
paired-classification-accuracy comparison, not a physical observable of the
Hamiltonian itself.

This script asks the same question a different way, with no MC scan needed:
under this paper's own Hamiltonian H = -sum J_ij s_i s_j - sum h_i s_i,
decompose the *real, empirical* map's total energy into its coupling term
(-0.5 s^T J s, "geography") and field term (-h^T s, "predisposition") at
each resolution, for the same 2026 coalition-split binarization used
throughout. This is a direct, deterministic property of the true
configuration under the fitted Hamiltonian -- not a fitted or simulated
quantity -- so it needs no seeds, no temperature scan, and no equilibration.

If predisposition's growing role at finer resolution (the ablation's
headline finding) is a real physical effect and not just an artifact of how
classification accuracy is scored, the field term's share of the total
binding energy should also grow at distrito resolution relative to canton
resolution. This gives R4 a genuinely physical quantity (an energy-term
decomposition) to sit alongside the accuracy-based ablation result.
"""

from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.ingestion import (
    binarize_votes,
    build_adjacency_graph,
    build_electoral_graph,
    load_shapefile,
    load_tse_juntas_consolidado,
    normalize_canton_code,
    normalize_distrito_code,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"

LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]


def energy_terms(J, h, spins):
    """Same two terms IsingModel.energy() sums, reported separately."""
    s = spins.astype(np.float64)
    coupling_term = -0.5 * s @ J.dot(s)
    field_term = -h @ s
    return float(coupling_term), float(field_term)


def canton_arrays():
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp", id_col="adm2_name")
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf["adm1_name"], gdf["adm2_name"])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    return graph_to_arrays(G)


def distrito_arrays():
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp", id_col="adm3_name")
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf["adm1_name"], gdf["adm2_name"], gdf["adm3_name"])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    isolates = list(nx.isolates(adjacency))
    if isolates:
        adjacency.remove_nodes_from(isolates)
    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    return graph_to_arrays(G)


def report(label, arrays, normalize=False):
    J, h, spins = arrays["J"], arrays["h"], arrays["spin_empirical"]
    N = J.shape[0]
    mean_degree = float(np.asarray(J.sum(axis=1)).ravel().mean())
    J_used = J / mean_degree if normalize else J
    coupling_term, field_term = energy_terms(J_used, h, spins)
    total = coupling_term + field_term
    field_share = field_term / (abs(coupling_term) + abs(field_term))
    tag = " (J row-mean-degree-normalized)" if normalize else ""
    print(f"{label:10}{tag:32} N={N:4d}  mean_degree={mean_degree:6.3f}  "
          f"coupling={coupling_term:10.3f}  field={field_term:10.3f}  "
          f"total={total:10.3f}  coupling/N={coupling_term/N:7.4f}  field/N={field_term/N:7.4f}  "
          f"field share of |terms|={field_share:.1%}")
    return {"N": N, "mean_degree": mean_degree, "coupling_term": coupling_term,
            "field_term": field_term, "total": total, "field_share": field_share}


def main():
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print("Energy decomposition of the TRUE 2026 map under this paper's Hamiltonian "
          "(coalition split, h=margin) -- deterministic, no MC, no seeds.\n")
    canton_a, distrito_a = canton_arrays(), distrito_arrays()

    print("-- raw J (unnormalized) --")
    canton = report("canton", canton_a)
    distrito = report("distrito", distrito_a)
    print(f"Field share of total binding energy: canton {canton['field_share']:.1%} "
          f"-> distrito {distrito['field_share']:.1%} "
          f"({distrito['field_share'] - canton['field_share']:+.1%} points)")

    print("\n-- J normalized by each graph's own mean weighted degree, to control for "
          "coupling budget mechanically scaling with resolution --")
    canton_n = report("canton", canton_a, normalize=True)
    distrito_n = report("distrito", distrito_a, normalize=True)
    print(f"Field share of total binding energy: canton {canton_n['field_share']:.1%} "
          f"-> distrito {distrito_n['field_share']:.1%} "
          f"({distrito_n['field_share'] - canton_n['field_share']:+.1%} points)")

    np.savez(RESULTS_DIR / "energy_decomposition.npz",
             canton_N=canton["N"], canton_coupling=canton["coupling_term"],
             canton_field=canton["field_term"], canton_field_share=canton["field_share"],
             canton_mean_degree=canton["mean_degree"],
             distrito_N=distrito["N"], distrito_coupling=distrito["coupling_term"],
             distrito_field=distrito["field_term"], distrito_field_share=distrito["field_share"],
             distrito_mean_degree=distrito["mean_degree"],
             canton_field_share_normalized=canton_n["field_share"],
             distrito_field_share_normalized=distrito_n["field_share"])
    print(f"\nRaw results written to {RESULTS_DIR / 'energy_decomposition.npz'}")


if __name__ == "__main__":
    main()
