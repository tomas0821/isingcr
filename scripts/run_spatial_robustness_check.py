#!/usr/bin/env python3
"""Two follow-up robustness checks flagged as open limitations by the
2026-08-17 referee panel (see ../referee_report_2026-08-17.md, Limitations
subsection of the manuscript):

1. **Spatial-block permutation test** (`spatial_block_permutation_test`):
   McNemar's exact test assumes independent paired outcomes, which spatial
   adjacency violates. This reruns the significance check for every
   headline result using a block-permutation test that only randomizes at
   the level of each unit's parent administrative area (province for
   cantons, canton for distritos) -- respecting, rather than ignoring,
   local spatial structure.
2. **Bonferroni correction for the T-grid search**: every headline p-value
   is reported at whichever temperature, out of a scanned grid, maximizes
   alignment -- a best-of-grid selection that inflates significance if left
   uncorrected. This multiplies each raw p-value by the grid size actually
   scanned (24 for the canton ablation/historical comparison, 32 for the
   distrito ablation) as a simple, conservative correction.

Reruns each headline result at its already-known best-fit temperature only
(not a full grid rescan) to get fresh per-seed final spin configurations,
since the original scripts didn't persist raw spins to disk. Canton-level
reruns use the full 24-point grid anyway (cheap, seconds); the distrito
rerun targets only the two known best-T values (T=2.83 for h=0, T=0.61 for
h=margin) with seeds parallelized across the T-list -- exploits the same
`temperature_scan` machinery by passing the same T n_seeds times, which
gives n_seeds independent parallel replicates at that one T -- to stay fast
on a 12-core local machine without needing the cluster again.
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
from isingcr.simulation.monte_carlo import pooled_temperature_scan, temperature_scan
from isingcr.simulation.observables import (
    alignment_fraction,
    mcnemar_test,
    spatial_block_permutation_test,
    symmetric_alignment_fraction,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
CANTON_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"
TSE_JUNTAS = DATA_RAW / "tse_juntas"

N_PERMUTATIONS = 999
SEED = 7


def province_blocks(nodes):
    """Canton-level node code "PROVINCE|CANTON" -> province block."""
    return np.array([n.split("|")[0] for n in nodes])


def canton_blocks(nodes):
    """Distrito-level node code "PROVINCE|CANTON|DISTRITO" -> parent-canton block."""
    return np.array(["|".join(n.split("|")[:2]) for n in nodes])


def best_t_final_spins(J, h, T, n_equil, n_sweeps, n_seeds, n_jobs, seed):
    """n_seeds independent replicates at a single T, parallelized across seeds
    (not the usual across-temperatures axis) by passing T repeated n_seeds
    times -- each repeat gets its own seed offset from `temperature_scan`."""
    results = temperature_scan(J, h, [T] * n_seeds, n_equil=n_equil, n_sweeps=n_sweeps,
                                dynamics="glauber", seed=seed, n_jobs=n_jobs)
    return [r["final_spins"] for r in results]


def report(label, empirical, majority_label, final_spins_per_seed, blocks, grid_size):
    per_seed_mc, per_seed_block = [], []
    for s in final_spins_per_seed:
        s_aligned = s if alignment_fraction(s, empirical) >= 0.5 else -s
        null = np.full_like(empirical, majority_label)
        per_seed_mc.append(mcnemar_test(s_aligned, null, empirical)["exact_pvalue"])
        per_seed_block.append(spatial_block_permutation_test(
            s_aligned, empirical, majority_label, blocks,
            n_permutations=N_PERMUTATIONS, rng=np.random.default_rng(0))["p_value"])

    mc_median = float(np.median(per_seed_mc))
    block_median = float(np.median(per_seed_block))
    print(f"{label:40s} McNemar median p={mc_median:.4f} (Bonferroni x{grid_size}: "
          f"{min(1.0, mc_median * grid_size):.4f})  |  "
          f"spatial-block median p={block_median:.4f} (Bonferroni x{grid_size}: "
          f"{min(1.0, block_median * grid_size):.4f})  n_blocks={spatial_block_permutation_test(final_spins_per_seed[0], empirical, majority_label, blocks, n_permutations=1)['n_blocks']}")
    return {"label": label, "mcnemar_median_p": mc_median, "block_median_p": block_median,
            "mcnemar_bonferroni_p": min(1.0, mc_median * grid_size),
            "block_bonferroni_p": min(1.0, block_median * grid_size)}


def canton_ablation_check():
    print("\n=== Canton ablation (2026 coalition split) ===")
    LEADING_PARTY = ["PUEBLO SOBERANO"]
    COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]
    results = load_tse_juntas_consolidado(TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
                                           member="_consolidado_presidenciales.csv", level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(CANTON_SHAPEFILE, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

    TEMPERATURES = np.linspace(0.05, 3.5, 24)
    out = []
    for label, h_col, majority_label in [("A: geography only", None, None), ("B: geography+margin", "margin", None)]:
        G = build_electoral_graph(adjacency, binarized, code_col="code", h_col=h_col)
        arrays = graph_to_arrays(G)
        J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
        maj = 1 if np.mean(empirical == 1) > 0.5 else -1
        blocks = province_blocks(arrays["nodes"])

        pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=8, n_equil=500, n_sweeps=500,
                                          dynamics="glauber", seed=SEED, n_jobs=8)
        # matches run_ablation.py: symmetric_alignment_fraction unconditionally,
        # even for h=margin, for consistency with the original best-T selection.
        per_t_accuracy = [np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]) for p in pooled]
        best_idx = int(np.argmax(per_t_accuracy))
        out.append(report(f"Canton {label} (T={TEMPERATURES[best_idx]:.2f})", empirical, maj,
                           pooled[best_idx]["final_spins_per_seed"], blocks, grid_size=24))
    return out


def historical_comparison_check():
    print("\n=== Historical comparison (winner vs. runner-up) ===")
    ELECTIONS = [
        {"label": "2018 (runoff)", "zip": TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2018.zip",
         "member": "ronda2/_consolidado_presidenciales.csv",
         "rename": {"ALAJUELA|VALVERDE VEGA": "ALAJUELA|SARCHI"}},
        {"label": "2022 (runoff)", "zip": TSE_JUNTAS / "juntas_TSE_2022_ronda2_provisional_y_definitivo.zip",
         "member": "_consolidado_definitivo.csv", "rename": {}},
        {"label": "2026 (round 1)", "zip": TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
         "member": "_consolidado_presidenciales.csv", "rename": {}},
    ]
    gdf = load_shapefile(CANTON_SHAPEFILE, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    TEMPERATURES = np.linspace(0.05, 3.5, 24)

    out = []
    for election in ELECTIONS:
        results = load_tse_juntas_consolidado(election["zip"], member=election["member"], level="canton")
        for old, new in election["rename"].items():
            results.loc[results["code"] == old, "code"] = new
        party_cols = [c for c in results.columns if c not in ("code", "name", "provincia_pais", "canton_ciudad")]
        totals = results[party_cols].sum().sort_values(ascending=False)
        winner, runner_up = totals.index[0], totals.index[1]
        binarized = binarize_votes(results, [winner], [runner_up])

        G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
        arrays = graph_to_arrays(G)
        J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
        maj = int(np.sign(np.mean(empirical)))
        blocks = province_blocks(arrays["nodes"])

        pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=8, n_equil=500, n_sweeps=500,
                                          dynamics="glauber", seed=SEED, n_jobs=8)
        per_t_accuracy = [np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]) for p in pooled]
        best_idx = int(np.argmax(per_t_accuracy))
        out.append(report(f"{election['label']} (T={TEMPERATURES[best_idx]:.2f})", empirical, maj,
                           pooled[best_idx]["final_spins_per_seed"], blocks, grid_size=24))
    return out


def distrito_ablation_check():
    print("\n=== Distrito ablation (2026 coalition split, targeted best-T reruns) ===")
    LEADING_PARTY = ["PUEBLO SOBERANO"]
    COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]
    results = load_tse_juntas_consolidado(TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
                                           member="_consolidado_presidenciales.csv", level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    isolates = list(nx.isolates(adjacency))
    adjacency.remove_nodes_from(isolates)

    out = []
    for label, h_col, T in [("A: geography only", None, 2.83), ("B: geography+margin", "margin", 0.61)]:
        G = build_electoral_graph(adjacency, binarized, code_col="code", h_col=h_col)
        arrays = graph_to_arrays(G)
        J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
        maj = 1 if np.mean(empirical == 1) > 0.5 else -1
        blocks = canton_blocks(arrays["nodes"])

        final_spins = best_t_final_spins(J, h, T, n_equil=20000, n_sweeps=20000,
                                          n_seeds=16, n_jobs=12, seed=SEED)
        if h_col is None:
            final_spins = [s if alignment_fraction(s, empirical) >= 0.5 else -s for s in final_spins]
        out.append(report(f"Distrito {label} (T={T})", empirical, maj, final_spins, blocks, grid_size=32))
    return out


def main():
    canton_ablation_check()
    historical_comparison_check()
    distrito_ablation_check()


if __name__ == "__main__":
    main()
