#!/usr/bin/env python3
"""Cross-binarization validation of the distrito-level ablation (referee-
flagged gap: run_distrito_ablation.py's headline +8.7pp result uses the
2026 coalition split; run_historical_comparison.py's winner-vs-runner-up
(wvru) binarization is never tested at distrito level, so it's unknown
whether the reversal is specific to the coalition-split construction.

Same geography-only vs. geography+margin ablation, same heavy Monte Carlo
budget as run_distrito_ablation.py (16 pooled seeds, 20,000+20,000 sweeps,
32 temperatures), same distrito adjacency network -- only the binarization
changes: 2026's top two vote-getters head to head (Pueblo Soberano vs.
Liberacion Nacional, by vote count), matching run_historical_comparison.py's
2026 row exactly, one administrative level down.
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
    specific_heat,
    susceptibility,
    symmetric_alignment_fraction,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

TEMPERATURES = np.linspace(0.05, 3.5, 32)
N_EQUIL, N_SWEEPS, SEED, N_JOBS, N_SEEDS = 20000, 20000, 7, 32, 16


def build_graph_and_votes():
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
    party_cols = [c for c in results.columns
                  if c not in ("code", "name", "provincia_pais", "canton_ciudad", "distrito")]
    totals = results[party_cols].sum().sort_values(ascending=False)
    winner, runner_up = totals.index[0], totals.index[1]
    print(f"Winner vs. runner-up (by national vote count): {winner} vs. {runner_up}")
    binarized = binarize_votes(results, [winner], [runner_up])

    gdf = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    isolates = list(nx.isolates(adjacency))
    if isolates:
        print(f"  Dropping {len(isolates)} isolated distrito(s): {isolates}")
        adjacency.remove_nodes_from(isolates)
    return adjacency, binarized, winner, runner_up


def run_scan(adjacency, binarized, h_col, n_seeds=N_SEEDS):
    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col=h_col)
    arrays = graph_to_arrays(G)
    J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
    N = J.shape[0]

    pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=n_seeds,
                                      n_equil=N_EQUIL, n_sweeps=N_SWEEPS,
                                      dynamics="glauber", seed=SEED, n_jobs=N_JOBS)

    chi = np.array([susceptibility(p["magnetization"], p["T"], N) for p in pooled])
    C = np.array([specific_heat(p["energy"], p["T"], N) for p in pooled])
    per_seed_accuracy = [
        [symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]
        for p in pooled
    ]
    accuracy = np.array([np.mean(a) for a in per_seed_accuracy])
    accuracy_std = np.array([np.std(a) for a in per_seed_accuracy])
    final_spins_per_seed_by_T = [p["final_spins_per_seed"] for p in pooled]
    return {"N": N, "chi": chi, "C": C, "accuracy": accuracy, "accuracy_std": accuracy_std,
            "empirical": empirical, "final_spins_per_seed_by_T": final_spins_per_seed_by_T}


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    adjacency, binarized, winner, runner_up = build_graph_and_votes()
    baseline = binarized["spin"].value_counts(normalize=True).max()
    majority_label = int(binarized["spin"].value_counts().idxmax())

    print(f"Running Run A (geography only, h=0), {N_SEEDS} seeds x {len(TEMPERATURES)} "
          f"temperatures, n_equil={N_EQUIL}, n_sweeps={N_SWEEPS}, n_jobs={N_JOBS}...",
          flush=True)
    run_a = run_scan(adjacency, binarized, h_col=None)
    print(f"Running Run B (geography + predisposition, h=margin), {N_SEEDS} seeds...",
          flush=True)
    run_b = run_scan(adjacency, binarized, h_col="margin")

    print(f"\n{'':20}{'N':>4}{'Baseline':>10}{'BestAlign':>13}{'@T':>7}"
          f"{'PeakChi':>9}{'@T':>7}{'McNemar p':>11}{'sig/16':>8}")
    for label, r in (("A: geography only", run_a), ("B: geography+h", run_b)):
        best_idx = int(np.argmax(r["accuracy"]))
        peak_idx = int(np.nanargmax(r["chi"]))
        best_str = f"{r['accuracy'][best_idx]:.1%}+/-{r['accuracy_std'][best_idx]:.1%}"
        mc = mcnemar_seed_summary(r["final_spins_per_seed_by_T"][best_idx],
                                   r["empirical"], majority_label)
        sig_str = f"{int(round(mc['fraction_significant_at_0.05'] * N_SEEDS))}/{N_SEEDS}"
        print(f"{label:20}{r['N']:>4}{baseline:>10.1%}{best_str:>13}"
              f"{TEMPERATURES[best_idx]:>7.2f}{r['chi'][peak_idx]:>9.2f}"
              f"{TEMPERATURES[peak_idx]:>7.2f}{mc['median_exact_pvalue']:>11.4f}{sig_str:>8}")

    gap = run_b["accuracy"].max() - run_a["accuracy"].max()
    print(f"\nMarginal contribution of predisposition (h) over pure geography, at "
          f"distrito granularity, winner-vs-runner-up binarization ({winner} vs. "
          f"{runner_up}): {gap:+.1%}")
    print("Compare to coalition-split distrito result (run_distrito_ablation.py): +8.7pp.")

    np.savez(RESULTS_DIR / "distrito_ablation_wvru.npz",
              temperatures=TEMPERATURES,
              accuracy_a=run_a["accuracy"], accuracy_a_std=run_a["accuracy_std"],
              accuracy_b=run_b["accuracy"], accuracy_b_std=run_b["accuracy_std"],
              baseline=baseline, N=run_a["N"], winner=winner, runner_up=runner_up,
              n_equil=N_EQUIL, n_sweeps=N_SWEEPS, n_seeds=N_SEEDS)
    print(f"Raw results written to {RESULTS_DIR / 'distrito_ablation_wvru.npz'}")


if __name__ == "__main__":
    main()
