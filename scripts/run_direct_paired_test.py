#!/usr/bin/env python3
"""Direct paired test: does adding h (geography+margin, arm B) actually
predict the real map significantly better than geography alone (arm A),
compared HEAD-TO-HEAD -- not each arm separately against the trivial
majority-class baseline, which is all every other significance test in this
paper does (referee-flagged gap, both rounds: round-1 finding #4, round-2
Abstract/Section-4.2 finding).

Uses `spatial_block_permutation_test_paired` (isingcr.simulation.observables),
already implemented but never invoked anywhere in this project until now:
it randomizes at the block level which of the two arms' predictions is
credited with matching the empirical map on each discordant unit, so it
inherits the same spatial-autocorrelation-robustness as this paper's other
spatial-block test rather than assuming independent per-unit outcomes.

Runs each arm only at its already-identified best-fit temperature (no full
grid rescan needed) via `temperature_scan` directly, at the same seed
counts/sweep budgets used for the headline canton and distrito ablations.
For each of the paired seeds (seed i of arm A vs. seed i of arm B), computes
one paired test; reports the median p-value and the fraction of seed-pairs
individually significant, matching this paper's existing per-seed summary
convention.
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
from isingcr.simulation.monte_carlo import temperature_scan
from isingcr.simulation.observables import (
    alignment_fraction,
    spatial_block_permutation_test_paired,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]
N_PERMUTATIONS = 999


def province_blocks(nodes):
    return np.array([n.split("|")[0] for n in nodes])


def canton_blocks(nodes):
    return np.array(["|".join(n.split("|")[:2]) for n in nodes])


def best_t_final_spins_aligned(J, h, T, empirical, n_equil, n_sweeps, n_seeds, n_jobs, seed):
    results = temperature_scan(J, h, [T] * n_seeds, n_equil=n_equil, n_sweeps=n_sweeps,
                                dynamics="glauber", seed=seed, n_jobs=n_jobs)
    raw = [r["final_spins"] for r in results]
    return [s if alignment_fraction(s, empirical) >= 0.5 else -s for s in raw]


def paired_test(label, spins_a_list, spins_b_list, empirical, blocks, n_seeds):
    ps = [spatial_block_permutation_test_paired(sa, sb, empirical, blocks,
                                                 n_permutations=N_PERMUTATIONS,
                                                 rng=np.random.default_rng(i))["p_value"]
          for i, (sa, sb) in enumerate(zip(spins_a_list, spins_b_list))]
    median_p = float(np.median(ps))
    frac_sig = float(np.mean(np.array(ps) < 0.05))
    print(f"{label}: n_blocks={len(np.unique(blocks))}  per-seed p-values={[f'{p:.3f}' for p in ps]}")
    print(f"  median p={median_p:.4f}  significant in {int(round(frac_sig*n_seeds))}/{n_seeds} seed-pairs")
    return {"ps": np.array(ps), "median_p": median_p, "frac_sig": frac_sig}


def canton_direct_test():
    print("=== Canton-level: direct paired test, arm A (h=0, T=2.60) vs. "
          "arm B (h=margin, T=1.55) ===")
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp", id_col="adm2_name")
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf["adm1_name"], gdf["adm2_name"])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

    G_a = build_electoral_graph(adjacency, binarized, code_col="code", h_col=None)
    arrays_a = graph_to_arrays(G_a)
    G_b = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays_b = graph_to_arrays(G_b)
    empirical = arrays_b["spin_empirical"]
    nodes = arrays_b["nodes"]

    N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 500, 500, 8, 8, 7
    spins_a = best_t_final_spins_aligned(arrays_a["J"], arrays_a["h"], 2.60, empirical,
                                          N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    spins_b = best_t_final_spins_aligned(arrays_b["J"], arrays_b["h"], 1.55, empirical,
                                          N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    blocks = province_blocks(nodes)
    return paired_test("canton (province blocks)", spins_a, spins_b, empirical, blocks, N_SEEDS)


def distrito_direct_test():
    print("\n=== Distrito-level: direct paired test, arm A (h=0, T=2.83) vs. "
          "arm B (h=margin, T=0.61) ===")
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp", id_col="adm3_name")
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf["adm1_name"], gdf["adm2_name"], gdf["adm3_name"])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    adjacency.remove_nodes_from(list(nx.isolates(adjacency)))

    G_a = build_electoral_graph(adjacency, binarized, code_col="code", h_col=None)
    arrays_a = graph_to_arrays(G_a)
    G_b = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays_b = graph_to_arrays(G_b)
    empirical = arrays_b["spin_empirical"]
    nodes = arrays_b["nodes"]

    N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 32, 7
    spins_a = best_t_final_spins_aligned(arrays_a["J"], arrays_a["h"], 2.83, empirical,
                                          N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    spins_b = best_t_final_spins_aligned(arrays_b["J"], arrays_b["h"], 0.61, empirical,
                                          N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    blocks = canton_blocks(nodes)
    return paired_test("distrito (canton blocks)", spins_a, spins_b, empirical, blocks, N_SEEDS)


def main():
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    canton = canton_direct_test()
    distrito = distrito_direct_test()
    np.savez(RESULTS_DIR / "direct_paired_test.npz",
             canton_ps=canton["ps"], canton_median_p=canton["median_p"], canton_frac_sig=canton["frac_sig"],
             distrito_ps=distrito["ps"], distrito_median_p=distrito["median_p"],
             distrito_frac_sig=distrito["frac_sig"])
    print(f"\nRaw results written to {RESULTS_DIR / 'direct_paired_test.npz'}")


if __name__ == "__main__":
    main()
