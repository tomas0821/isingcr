#!/usr/bin/env python3
"""Ablation: how much of the real map does geography alone explain?

Runs the same real canton graph and the same 2026 binarization
(PUEBLO SOBERANO vs. the LIBERACION NACIONAL / COALICION AGENDA CIUDADANA /
FRENTE AMPLIO coalition, see run_real_pipeline.py) twice:

  Run A "geography only": h_i = 0 everywhere. Only the coupling network (real
      canton adjacency) can produce any structure -- a canton's simulated
      spin is decided purely by conformity pressure from its neighbors, with
      no innate lean of its own. Scored with symmetric_alignment_fraction
      since h=0 makes the model's up/down labeling arbitrary (see its
      docstring) -- a raw score would be meaningless.
  Run B "geography + predisposition": h_i = real vote margin, i.e. the
      run_real_pipeline.py default.

Comparing best-achieved alignment isolates how much of the real map's spatial
clustering comes from "neighbors pull on each other" alone vs. how much needs
each canton's own political lean on top of that. Comparing susceptibility
curve shape between the two (same N=84 in both, so finite-size smearing is
identical) is a fair look at which ingredient drives whatever critical-like
behavior exists -- see README "A physics note" and the discussion of this
ablation for the reasoning.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.ingestion import (
    binarize_votes,
    build_adjacency_graph,
    build_electoral_graph,
    load_shapefile,
    load_tse_juntas_consolidado,
    normalize_canton_code,
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

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL, CANTON_COL = "adm1_name", "adm2_name"

LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]

TEMPERATURES = np.linspace(0.05, 3.5, 24)
N_EQUIL, N_SWEEPS, SEED, N_JOBS = 500, 500, 7, 8
N_SEEDS = 8  # independent replicates per temperature, pooled -- see pooled_temperature_scan


def build_graph_and_votes():
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)

    gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c)
                   for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    return adjacency, binarized


def run_scan(adjacency, binarized, h_col, n_seeds=N_SEEDS):
    """Run n_seeds pooled replicates per temperature -- see pooled_temperature_scan
    for why pooling matters and the low-T divergence caveat it can expose."""
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
    adjacency, binarized = build_graph_and_votes()
    baseline = binarized["spin"].value_counts(normalize=True).max()
    majority_label = int(binarized["spin"].value_counts().idxmax())

    print(f"Running Run A (geography only, h=0), {N_SEEDS} seeds x {len(TEMPERATURES)} "
          f"temperatures, n_jobs={N_JOBS}...")
    run_a = run_scan(adjacency, binarized, h_col=None)
    print(f"Running Run B (geography + predisposition, h=margin), {N_SEEDS} seeds...")
    run_b = run_scan(adjacency, binarized, h_col="margin")

    print(f"\n{'':20}{'N':>4}{'Baseline':>10}{'BestAlign':>13}{'@T':>7}"
          f"{'PeakChi':>9}{'@T':>7}{'McNemar p':>11}{'sig/8':>7}")
    for label, r in (("A: geography only", run_a), ("B: geography+h", run_b)):
        best_idx = int(np.argmax(r["accuracy"]))
        peak_idx = int(np.nanargmax(r["chi"]))
        best_str = f"{r['accuracy'][best_idx]:.1%}+/-{r['accuracy_std'][best_idx]:.1%}"
        mc = mcnemar_seed_summary(r["final_spins_per_seed_by_T"][best_idx],
                                   r["empirical"], majority_label)
        sig_str = f"{int(round(mc['fraction_significant_at_0.05'] * N_SEEDS))}/{N_SEEDS}"
        print(f"{label:20}{r['N']:>4}{baseline:>10.1%}{best_str:>13}"
              f"{TEMPERATURES[best_idx]:>7.2f}{r['chi'][peak_idx]:>9.2f}"
              f"{TEMPERATURES[peak_idx]:>7.2f}{mc['median_exact_pvalue']:>11.4f}{sig_str:>7}")

    print("(McNemar p = exact paired test, model's best-T config vs. the constant "
          "majority-class null, median across seeds; sig/8 = seeds significant at "
          "p<0.05 -- see mcnemar_test's docstring)")

    gap = run_b["accuracy"].max() - run_a["accuracy"].max()
    print(f"\nMarginal contribution of predisposition (h) over pure geography: "
          f"{gap:+.1%}")

    plot(run_a, run_b, baseline)
    print(f"\nFigure written to {FIGURES_DIR / 'ablation.png'}")


def plot(run_a, run_b, baseline):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    for label, r, color in (("A: geography only (h=0)", run_a, "tab:gray"),
                             ("B: geography + predisposition (h=margin)", run_b, "tab:red")):
        axes[0].errorbar(TEMPERATURES, r["accuracy"], yerr=r["accuracy_std"],
                          fmt="o-", color=color, label=label, capsize=2, alpha=0.85)
        axes[1].plot(TEMPERATURES, r["chi"], "o-", color=color, label=label)
        axes[2].plot(TEMPERATURES, r["C"], "o-", color=color, label=label)
    axes[0].axhline(baseline, color="black", linestyle=":", linewidth=1,
                     label="majority-class baseline")
    axes[0].axhline(0.5, color="gray", linestyle="--", linewidth=1, label="chance (symmetric)")

    axes[0].set_title("Alignment (symmetric)")
    axes[0].set_xlabel("Temperature T")
    axes[0].legend(fontsize=7)
    axes[1].set_title("Susceptibility")
    axes[1].set_xlabel("Temperature T")
    axes[1].legend(fontsize=7)
    axes[2].set_title("Specific heat")
    axes[2].set_xlabel("Temperature T")
    axes[2].legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "ablation.png", dpi=150)


if __name__ == "__main__":
    main()
