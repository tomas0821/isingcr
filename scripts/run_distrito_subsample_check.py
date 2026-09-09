#!/usr/bin/env python3
"""MAUP/power check for the canton-vs-distrito ablation "reversal" (Section
4.6 of the manuscript, referee-flagged as an unresolved confound): is the
distrito-level result's larger, more significant effect a genuine
resolution effect, or partly just an artifact of distrito level having
N=488 (much more statistical power) and a different baseline than canton
level's N=84?

Runs the same geography-only vs. geography+margin ablation used throughout
this project, but on N_SUBSAMPLES independent random size-84 subsamples of
the 488 distritos (matching canton-level N exactly) -- same statistical
power as the canton-level check, same fine-grained distrito-level political
heterogeneity. If the effect size/significance at distrito-subsample scale
looks like the real canton result (small, not significant), the canton vs.
full-distrito contrast is largely an N/power artifact. If it still looks
like the full-distrito result (large, significant), resolution itself is
doing the work, not sample size.

Sized to match run_ablation.py's canton-level budget (24-point grid,
500+500 sweeps, 8 seeds) since we're deliberately matching canton-level
statistical power, not distrito-level's heavier budget.
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
    normalize_distrito_code,
)
from isingcr.simulation.monte_carlo import pooled_temperature_scan
from isingcr.simulation.observables import (
    mcnemar_seed_summary,
    symmetric_alignment_fraction,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"
TSE_JUNTAS = DATA_RAW / "tse_juntas"

LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]

TEMPERATURES = np.linspace(0.05, 3.5, 24)
N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS = 500, 500, 8, 24
N_SUBSAMPLES = 10
SUBSAMPLE_N = 84  # match canton-level N exactly


def build_full_distrito_graph_and_votes():
    results = load_tse_juntas_consolidado(TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
                                           member="_consolidado_presidenciales.csv", level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    adjacency.remove_nodes_from(list(nx.isolates(adjacency)))
    return adjacency, binarized


def run_arm(subgraph, binarized, h_col, seed):
    G = build_electoral_graph(subgraph, binarized, code_col="code", h_col=h_col, drop_unmatched=True)
    arrays = graph_to_arrays(G)
    J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
    N = J.shape[0]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    baseline = float(np.mean(empirical == majority_label))

    pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=N_SEEDS,
                                      n_equil=N_EQUIL, n_sweeps=N_SWEEPS,
                                      dynamics="glauber", seed=seed, n_jobs=N_JOBS)
    per_t_accuracy = [np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]])
                       for p in pooled]
    best_idx = int(np.argmax(per_t_accuracy))
    accuracy = per_t_accuracy[best_idx]
    mc = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical, majority_label)
    return {"N": N, "baseline": baseline, "T_best": float(TEMPERATURES[best_idx]),
            "accuracy": accuracy, "mcnemar_median_p": mc["median_exact_pvalue"],
            "frac_sig": mc["fraction_significant_at_0.05"]}


def main():
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    adjacency, binarized = build_full_distrito_graph_and_votes()
    all_nodes = list(adjacency.nodes)
    print(f"Full distrito graph: N={len(all_nodes)}")

    results = []
    for k in range(N_SUBSAMPLES):
        rng = np.random.default_rng(1000 + k)
        sample_nodes = rng.choice(all_nodes, size=SUBSAMPLE_N, replace=False)
        subgraph = adjacency.subgraph(sample_nodes).copy()
        n_edges = subgraph.number_of_edges()
        print(f"\n--- Subsample {k+1}/{N_SUBSAMPLES}: N={subgraph.number_of_nodes()}, "
              f"edges={n_edges} ---", flush=True)

        arm_a = run_arm(subgraph, binarized, h_col=None, seed=7 + k * 100)
        arm_b = run_arm(subgraph, binarized, h_col="margin", seed=7 + k * 100)
        gap = arm_b["accuracy"] - arm_a["accuracy"]
        print(f"  A (geography only):   {arm_a['accuracy']:.1%} vs baseline {arm_a['baseline']:.1%}, "
              f"McNemar p={arm_a['mcnemar_median_p']:.4f}, {arm_a['frac_sig']*N_SEEDS:.0f}/{N_SEEDS} sig")
        print(f"  B (geography+margin): {arm_b['accuracy']:.1%} vs baseline {arm_b['baseline']:.1%}, "
              f"McNemar p={arm_b['mcnemar_median_p']:.4f}, {arm_b['frac_sig']*N_SEEDS:.0f}/{N_SEEDS} sig")
        print(f"  gap = {gap:+.1%}")
        results.append({"k": k, "n_edges": n_edges, "arm_a": arm_a, "arm_b": arm_b, "gap": gap})

    gaps = np.array([r["gap"] for r in results])
    b_pvals = np.array([r["arm_b"]["mcnemar_median_p"] for r in results])
    n_b_sig = int(np.sum(b_pvals < 0.05))
    print(f"\n=== Summary across {N_SUBSAMPLES} size-84 distrito subsamples ===")
    print(f"gap: mean={gaps.mean():+.1%}, std={gaps.std():.1%}, min={gaps.min():+.1%}, max={gaps.max():+.1%}")
    print(f"arm B McNemar significant (p<0.05) in {n_b_sig}/{N_SUBSAMPLES} subsamples")
    print("Compare to: canton-level (N=84, real cantons) gap = +1.2pp, not significant;"
          " full distrito (N=488) gap = +8.7pp, McNemar-significant but not spatial-block-significant.")

    np.savez(RESULTS_DIR / "distrito_subsample_check.npz",
              gaps=gaps, b_pvals=b_pvals,
              results=np.array(results, dtype=object))
    print(f"\nRaw results written to {RESULTS_DIR / 'distrito_subsample_check.npz'}")


if __name__ == "__main__":
    main()
