#!/usr/bin/env python3
"""Sensitivity check: does the distrito-level spatial-block permutation
test's p=0.064 (arm B, geography+margin) depend on the specific blocking
granularity chosen (84 canton-blocks)? Reruns at the same best-fit
temperatures with an INDEPENDENT seed set (SEED=13, distinct from
run_spatial_robustness_check.py's SEED=7) and computes the spatial-block
test at three granularities: coarser (7 province-blocks), as-reported (84
canton-blocks), and finer (~168 half-canton blocks)."""

from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.ingestion import (
    binarize_votes, build_adjacency_graph, build_electoral_graph, load_shapefile,
    load_tse_juntas_consolidado, normalize_canton_code, normalize_distrito_code,
)
from isingcr.simulation.monte_carlo import pooled_temperature_scan, temperature_scan
from isingcr.simulation.observables import (
    alignment_fraction, mcnemar_test, spatial_block_permutation_test,
    symmetric_alignment_fraction,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
CANTON_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"
TSE_JUNTAS = DATA_RAW / "tse_juntas"

N_PERMUTATIONS = 999
SEED = 13  # independent of run_spatial_robustness_check.py's SEED=7


def province_blocks(nodes):
    return np.array([n.split("|")[0] for n in nodes])


def canton_blocks(nodes):
    return np.array(["|".join(n.split("|")[:2]) for n in nodes])


def fine_canton_blocks(nodes):
    """~2 sub-blocks per canton: alternate distrito index within each canton."""
    cb = canton_blocks(nodes)
    counters = {}
    out = []
    for c in cb:
        i = counters.get(c, 0)
        out.append(f"{c}__{i % 2}")
        counters[c] = i + 1
    return np.array(out)


def best_t_final_spins(J, h, T, n_equil, n_sweeps, n_seeds, n_jobs, seed):
    results = temperature_scan(J, h, [T] * n_seeds, n_equil=n_equil, n_sweeps=n_sweeps,
                                dynamics="glauber", seed=seed, n_jobs=n_jobs)
    return [r["final_spins"] for r in results]


def sweep_blockings(label, empirical, majority_label, final_spins_per_seed, blockings):
    aligned = [s if alignment_fraction(s, empirical) >= 0.5 else -s for s in final_spins_per_seed]
    mc_p = float(np.median([mcnemar_test(s, np.full_like(empirical, majority_label), empirical)["exact_pvalue"]
                             for s in aligned]))
    print(f"\n{label}  (McNemar median p={mc_p:.4f}, independent SEED={SEED})")
    results = {"mcnemar_median_p": mc_p, "blocks": {}}
    for bname, blocks in blockings.items():
        n_blocks = len(np.unique(blocks))
        ps = [spatial_block_permutation_test(s, empirical, majority_label, blocks,
                                              n_permutations=N_PERMUTATIONS,
                                              rng=np.random.default_rng(0))["p_value"]
              for s in aligned]
        p_med = float(np.median(ps))
        print(f"  {bname:28s} n_blocks={n_blocks:4d}  spatial-block median p={p_med:.4f}")
        results["blocks"][bname] = {"n_blocks": n_blocks, "median_p": p_med}
    return results


def distrito_sensitivity():
    LEADING_PARTY = ["PUEBLO SOBERANO"]
    COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]
    results = load_tse_juntas_consolidado(TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
                                           member="_consolidado_presidenciales.csv", level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    adjacency.remove_nodes_from(list(nx.isolates(adjacency)))

    print("=== Distrito-level: spatial-block granularity sensitivity ===")
    out = {}
    for label, h_col, T in [("A: geography only", None, 2.83), ("B: geography+margin", "margin", 0.61)]:
        G = build_electoral_graph(adjacency, binarized, code_col="code", h_col=h_col)
        arrays = graph_to_arrays(G)
        J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
        maj = 1 if np.mean(empirical == 1) > 0.5 else -1
        nodes = arrays["nodes"]
        blockings = {
            "coarser: province (7)": province_blocks(nodes),
            "as-reported: canton (84)": canton_blocks(nodes),
            "finer: half-canton (~168)": fine_canton_blocks(nodes),
        }
        final_spins = best_t_final_spins(J, h, T, n_equil=20000, n_sweeps=20000,
                                          n_seeds=16, n_jobs=12, seed=SEED)
        out[label] = sweep_blockings(f"Distrito {label} (T={T})", empirical, maj, final_spins, blockings)
    return out


def canton_sensitivity():
    LEADING_PARTY = ["PUEBLO SOBERANO"]
    COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]
    results = load_tse_juntas_consolidado(TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
                                           member="_consolidado_presidenciales.csv", level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(CANTON_SHAPEFILE, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    TEMPERATURES = np.linspace(0.05, 3.5, 24)

    print("\n=== Canton-level: spatial-block granularity sensitivity ===")
    out = {}
    for label, h_col in [("A: geography only", None), ("B: geography+margin", "margin")]:
        G = build_electoral_graph(adjacency, binarized, code_col="code", h_col=h_col)
        arrays = graph_to_arrays(G)
        J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
        maj = 1 if np.mean(empirical == 1) > 0.5 else -1
        nodes = arrays["nodes"]

        pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=8, n_equil=500, n_sweeps=500,
                                          dynamics="glauber", seed=SEED, n_jobs=8)
        per_t_accuracy = [np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]])
                           for p in pooled]
        best_idx = int(np.argmax(per_t_accuracy))
        T = TEMPERATURES[best_idx]

        blockings = {
            "coarser: province (7)": province_blocks(nodes),
            "as-reported: single-canton (84)": np.array(nodes),  # every unit its own block
        }
        out[label] = sweep_blockings(f"Canton {label} (T={T:.2f})", empirical, maj,
                                      pooled[best_idx]["final_spins_per_seed"], blockings)
    return out


if __name__ == "__main__":
    distrito_sensitivity()
    canton_sensitivity()
