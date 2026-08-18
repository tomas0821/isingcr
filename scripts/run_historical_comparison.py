#!/usr/bin/env python3
"""Compare the Ising model across three real Costa Rican elections.

Each election is binarized as that year's top-2 finishers (winner vs.
runner-up) -- a well-defined, comparable split every cycle: the 2018 and 2022
runoffs already are winner-vs-runner-up by definition (only 2 candidates), and
2026 was decided outright in round 1 (PUEBLO SOBERANO's margin exceeded the
40%-and-10-point threshold that would have forced a runoff). All three runs
share the same real canton adjacency graph (data/raw/boundaries/), so the only
thing that changes between them is the vote data.

Costa Rica added 3 cantons between 2018 and 2026 (Rio Cuarto, Monteverde,
Puerto Jimenez each split off from an existing canton), and 2018 additionally
used the now-retired name "Valverde Vega" for today's "Sarchi" -- so N_cantons
legitimately differs by year (81 / 82 / 84): build_electoral_graph drops any
adjacency node with no matching results row for that year, rather than
guessing. The Valverde Vega -> Sarchi rename is applied here since it's the
same canton, not a new one.

Each election pools N_SEEDS independent MC replicates per temperature (see
isingcr.simulation.monte_carlo.pooled_temperature_scan) -- a single-seed
version of this comparison originally reported "2022 and 2026 beat their
majority-class baseline, 2018 doesn't"; scripts/run_ablation.py later showed
that same single-seed setup produces alignment gaps and susceptibility peaks
that don't survive proper multi-seed averaging, so that claim needed
re-checking under the same rigor rather than being taken at face value.
"Beats baseline" below means the best-T alignment's 1-sigma band (mean minus
one std across seeds) clears the baseline, not just the point estimate.
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

SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL, CANTON_COL = "adm1_name", "adm2_name"

TSE_JUNTAS = DATA_RAW / "tse_juntas"
ELECTIONS = [
    {
        "label": "2018 (runoff)",
        "zip": TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2018.zip",
        "member": "ronda2/_consolidado_presidenciales.csv",
        "rename": {"ALAJUELA|VALVERDE VEGA": "ALAJUELA|SARCHI"},
    },
    {
        "label": "2022 (runoff)",
        "zip": TSE_JUNTAS / "juntas_TSE_2022_ronda2_provisional_y_definitivo.zip",
        "member": "_consolidado_definitivo.csv",
        "rename": {},
    },
    {
        "label": "2026 (round 1)",
        "zip": TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
        "member": "_consolidado_presidenciales.csv",
        "rename": {},
    },
]

TEMPERATURES = np.linspace(0.05, 3.5, 24)
N_EQUIL, N_SWEEPS, SEED, N_JOBS, N_SEEDS = 500, 500, 7, 8, 8


def _top_two_parties(results, party_cols):
    totals = results[party_cols].sum().sort_values(ascending=False)
    return totals.index[0], totals.index[1], totals


def run_election(election, adjacency):
    results = load_tse_juntas_consolidado(election["zip"], member=election["member"],
                                           level="canton")
    for old, new in election["rename"].items():
        results.loc[results["code"] == old, "code"] = new

    party_cols = [c for c in results.columns
                  if c not in ("code", "name", "provincia_pais", "canton_ciudad")]
    winner, runner_up, totals = _top_two_parties(results, party_cols)
    binarized = binarize_votes(results, [winner], [runner_up])
    baseline = binarized["spin"].value_counts(normalize=True).max()
    majority_label = int(binarized["spin"].value_counts().idxmax())

    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays = graph_to_arrays(G)
    J, h, empirical = arrays["J"], arrays["h"], arrays["spin_empirical"]
    N = J.shape[0]

    pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=N_SEEDS,
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

    best_idx = int(np.argmax(accuracy))
    beats_baseline = (accuracy[best_idx] - accuracy_std[best_idx]) > baseline
    mcnemar = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical,
                                    majority_label)

    return {
        "label": election["label"],
        "winner": winner, "runner_up": runner_up,
        "winner_votes": int(totals[winner]), "runner_up_votes": int(totals[runner_up]),
        "N": N, "baseline": baseline,
        "T_critical_susceptibility": float(TEMPERATURES[np.nanargmax(chi)]),
        "T_critical_specific_heat": float(TEMPERATURES[np.nanargmax(C)]),
        "T_best_alignment": float(TEMPERATURES[best_idx]),
        "best_alignment": float(accuracy[best_idx]),
        "best_alignment_std": float(accuracy_std[best_idx]),
        "beats_baseline": beats_baseline,
        "mcnemar_median_pvalue": mcnemar["median_exact_pvalue"],
        "mcnemar_fraction_significant": mcnemar["fraction_significant_at_0.05"],
        "chi": chi, "C": C, "accuracy": accuracy, "accuracy_std": accuracy_std,
    }


def main():
    FIGURES_DIR.mkdir(exist_ok=True)

    gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c)
                   for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

    print(f"Pooling {N_SEEDS} seeds x {len(TEMPERATURES)} temperatures per election, "
          f"n_jobs={N_JOBS}...")
    results = [run_election(e, adjacency) for e in ELECTIONS]

    print(f"\n{'Election':<16}{'N':>4}{'Baseline':>10}{'BestAlign':>15}{'@T':>7}"
          f"{'>Baseline':>11}{'McNemar p':>11}{f'sig/{N_SEEDS}':>7}")
    for r in results:
        align_str = f"{r['best_alignment']:.1%}+/-{r['best_alignment_std']:.1%}"
        sig_str = f"{int(round(r['mcnemar_fraction_significant'] * N_SEEDS))}/{N_SEEDS}"
        print(f"{r['label']:<16}{r['N']:>4}{r['baseline']:>10.1%}{align_str:>15}"
              f"{r['T_best_alignment']:>7.2f}{str(r['beats_baseline']):>11}"
              f"{r['mcnemar_median_pvalue']:>11.4f}{sig_str:>7}")
    print("(McNemar p = exact paired test vs. the constant majority-class null, "
          f"median across {N_SEEDS} seeds at each election's best-T; "
          f"sig/{N_SEEDS} = seeds significant at p<0.05)")

    print(f"\n{'Election':<16}{'Winner':<28}{'Runner-up':<28}{'T_chi':>8}{'T_C':>8}")
    for r in results:
        print(f"{r['label']:<16}{r['winner']:<28}{r['runner_up']:<28}"
              f"{r['T_critical_susceptibility']:>8.2f}{r['T_critical_specific_heat']:>8.2f}")

    plot_comparison(results)
    print(f"\nFigure written to {FIGURES_DIR / 'historical_comparison.png'}")


def plot_comparison(results):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    colors = ["tab:blue", "tab:orange", "tab:green"]
    for r, color in zip(results, colors):
        axes[0].errorbar(TEMPERATURES, r["accuracy"], yerr=r["accuracy_std"],
                          fmt="o-", color=color, label=r["label"], capsize=2, alpha=0.85)
        axes[0].axhline(r["baseline"], color=color, linestyle=":", linewidth=1, alpha=0.6)
        axes[1].plot(TEMPERATURES, r["chi"], "o-", color=color, label=r["label"])
        axes[2].plot(TEMPERATURES, r["C"], "o-", color=color, label=r["label"])

    axes[0].set_title("Alignment (symmetric) with empirical map\n"
                       "(dotted = majority-class baseline, bars = 1 std across seeds)")
    axes[0].set_xlabel("Temperature T")
    axes[0].set_ylabel("Fraction matching")
    axes[0].legend(fontsize=8)

    axes[1].set_title("Susceptibility")
    axes[1].set_xlabel("Temperature T")
    axes[1].legend(fontsize=8)

    axes[2].set_title("Specific heat")
    axes[2].set_xlabel("Temperature T")
    axes[2].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "historical_comparison.png", dpi=150)


if __name__ == "__main__":
    main()
