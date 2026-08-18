#!/usr/bin/env python3
"""Why does the model fail to beat baseline for 2018 but not 2022/2026?

run_historical_comparison.py established the fact (2018: 76.4%+/-0.4% vs. a
76.5% baseline, McNemar 0/8 seeds significant -- a confident null; 2022/2026
show a positive point estimate). This script investigates *why*, with cheap,
deterministic diagnostics that don't need any MC temperature scan.

Two questions, in order:

1. Does 2018 lack real geographic structure to exploit? Answer: no --
   Moran's I (isingcr.utils.spatial_stats) shows 2018 is the *most* spatially
   autocorrelated of the three elections, not the least (checked on both the
   binarized spin and the continuous margin). Ruled out.

2. Is the true 2018 map even a favorable state under this model's own
   physics? Answer: this is where the real story is. Every election's
   trivial "everyone votes for the winner" configuration has lower energy
   than the true map (unsurprising -- it's the null the model is being
   compared against), but *how much* lower, per canton, differs sharply:
   the true 2018 map costs ~1.13 energy units/canton relative to the trivial
   state, vs. ~0.77 (2022) and ~0.59 (2026). A random-start MC search is
   least likely to ever find its way near the true minority pattern when
   that pattern is this energetically disfavored relative to the trivial
   global optimum -- which is exactly what run_historical_comparison.py
   observed. This cleanly separates 2018 from 2022/2026 as a category
   (which is the question asked), even though it doesn't perfectly rank
   2022 vs. 2026 against each other (a secondary, lower-priority question).
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
from isingcr.simulation.ising_model import IsingModel
from isingcr.simulation.monte_carlo import run_sweep
from isingcr.utils.graph_arrays import graph_to_arrays
from isingcr.utils.spatial_stats import morans_i_test

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

N_PERMUTATIONS = 999
SEED = 42
T0_RELAXATION_SWEEPS = 100
N_RELAX_SEEDS = 8


def _top_two_parties(results, party_cols):
    totals = results[party_cols].sum().sort_values(ascending=False)
    return totals.index[0], totals.index[1]


def analyze_election(election, adjacency, rng):
    results = load_tse_juntas_consolidado(election["zip"], member=election["member"],
                                           level="canton")
    for old, new in election["rename"].items():
        results.loc[results["code"] == old, "code"] = new

    party_cols = [c for c in results.columns
                  if c not in ("code", "name", "provincia_pais", "canton_ciudad")]
    winner, runner_up = _top_two_parties(results, party_cols)
    binarized = binarize_votes(results, [winner], [runner_up])

    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays = graph_to_arrays(G)
    J, h, spin = arrays["J"], arrays["h"], arrays["spin_empirical"]
    N = J.shape[0]
    majority_label = 1 if np.mean(spin == 1) > 0.5 else -1
    n_minority = int(np.sum(spin != majority_label))

    # Question 1: is 2018 short on real geographic structure?
    spin_moran = morans_i_test(J, spin.astype(float), n_permutations=N_PERMUTATIONS, rng=rng)
    margin_moran = morans_i_test(J, h, n_permutations=N_PERMUTATIONS, rng=rng)

    # Question 2: how favorable is the true map under the model's own energetics?
    model_truth = IsingModel(J, h, spins=spin.copy())
    E_truth = model_truth.energy()
    model_allmaj = IsingModel(J, h, spins=np.full(N, majority_label, dtype=np.int8))
    E_allmaj = model_allmaj.energy()
    E_gap_per_N = (E_truth - E_allmaj) / N

    # T=0 relaxation starting AT the truth: how much of it is even locally stable?
    # Pooled across N_RELAX_SEEDS seeds (not a single run) -- T=0 Glauber is not fully
    # deterministic (ties at delta-E=0 still flip with probability 1/2), and this
    # project's own rule is never to trust a single-seed MC result (see gotcha #7).
    stable_fractions = []
    for seed in range(N_RELAX_SEEDS):
        relax_rng = np.random.default_rng(seed)
        model_relax = IsingModel(J, h, spins=spin.copy(), rng=relax_rng)
        for _ in range(T0_RELAXATION_SWEEPS):
            run_sweep(model_relax, T=0.0, dynamics="glauber", rng=relax_rng)
        stable_fractions.append(float(np.mean(model_relax.spins == spin)))
    stable_fractions = np.array(stable_fractions)

    return {
        "label": election["label"], "winner": winner, "runner_up": runner_up,
        "N": N, "n_minority": n_minority,
        "spin_moran_I": spin_moran["I"], "spin_moran_p": spin_moran["p_value"],
        "margin_moran_I": margin_moran["I"], "margin_moran_p": margin_moran["p_value"],
        "E_gap_per_N": E_gap_per_N,
        "fraction_locally_stable": float(stable_fractions.mean()),
        "fraction_locally_stable_std": float(stable_fractions.std()),
    }


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)

    gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c)
                   for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

    results = [analyze_election(e, adjacency, rng) for e in ELECTIONS]

    print(f"\n{'Election':<16}{'N':>4}{'n_min':>7}{'MoranI(spin)':>14}{'p':>8}"
          f"{'MoranI(margin)':>16}{'p':>8}{'E_gap/N':>10}{'%locally-stable (8 seeds)':>27}")
    for r in results:
        stable_str = f"{r['fraction_locally_stable']:.1%}+/-{r['fraction_locally_stable_std']:.1%}"
        print(f"{r['label']:<16}{r['N']:>4}{r['n_minority']:>7}"
              f"{r['spin_moran_I']:>14.3f}{r['spin_moran_p']:>8.3f}"
              f"{r['margin_moran_I']:>16.3f}{r['margin_moran_p']:>8.3f}"
              f"{r['E_gap_per_N']:>10.3f}{stable_str:>27}")

    print("\nMoran's I: is the empirical map spatially clustered at all? (all three are, "
          "p<0.01 -- 2018 is the MOST clustered of the three, so lack of geographic "
          "structure is ruled out as the explanation.)")
    print("E_gap/N: how much energy (per canton, under this model's own Hamiltonian) "
          "the true map costs relative to the trivial 'everyone votes for the winner' "
          "state. Higher = the true minority pattern is more energetically disfavored, "
          "so a random-start MC search is less likely to ever find it. 2018's value is "
          "~50% higher than 2022's and ~90% higher than 2026's -- this is the")
    print("mechanistic explanation for the historical-comparison result: it isn't that "
          "2018 lacks geography, it's that 2018's true opposition map is a much more "
          "energetically 'expensive' pattern for this Hamiltonian to prefer over the "
          "trivial alternative, so the MC scan's random restarts rarely land near it.")

    plot(results)
    print(f"\nFigure written to {FIGURES_DIR / '2018_anomaly.png'}")


def plot(results):
    import matplotlib.pyplot as plt

    labels = [r["label"] for r in results]
    e_gap = [r["E_gap_per_N"] for r in results]
    moran = [r["spin_moran_I"] for r in results]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(labels, e_gap, color=["tab:red", "tab:blue", "tab:blue"])
    axes[0].set_ylabel("Energy gap per canton\n(truth vs. trivial majority state)")
    axes[0].set_title("Higher = true map is more energetically disfavored")

    axes[1].bar(labels, moran, color=["tab:blue", "tab:blue", "tab:blue"])
    axes[1].set_ylabel("Moran's I (empirical spin)")
    axes[1].set_title("All three are spatially clustered (p<0.01) --\n2018 is not short on geographic structure")

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "2018_anomaly.png", dpi=150)


if __name__ == "__main__":
    main()
