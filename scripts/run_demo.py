#!/usr/bin/env python3
"""End-to-end demo on synthetic data: build a graph, scan temperature, plot results.

Runs entirely offline (no real TSE/shapefile data needed) so the pipeline and
the Docker image can be validated before real data is wired in. Swap
`synthetic_electoral_graph(...)` for the real ingestion pipeline
(`isingcr.ingestion`) once TSE result files and a canton/distrito shapefile are
available under data/raw/ -- see README.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.simulation.monte_carlo import temperature_scan
from isingcr.utils.graph_arrays import graph_to_arrays
from isingcr.utils.synthetic import synthetic_electoral_graph
from isingcr.visualization.maps import plot_network_comparison
from isingcr.visualization.plots import plot_alignment_curve, plot_phase_diagram

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)

    print("Building synthetic 84-canton electoral graph...")
    # field_scale > 0 breaks the model's up/down (Z2) symmetry, like a real
    # election does -- without it, "traditional" vs "emerging" is an arbitrary
    # label and low-T runs converge to either sign with 50/50 probability,
    # making alignment-vs-T look randomly bimodal instead of a clean curve.
    G = synthetic_electoral_graph(n_units=84, seed=42, low_T=0.6, n_relax_sweeps=200,
                                   field_scale=1.5)
    arrays = graph_to_arrays(G)
    J, h, nodes, empirical = arrays["J"], arrays["h"], arrays["nodes"], arrays["spin_empirical"]
    print(f"  {J.shape[0]} nodes, {J.nnz // 2} edges")

    temperatures = np.linspace(0.1, 4.0, 20)
    print(f"Running temperature scan over {len(temperatures)} points...")
    results = temperature_scan(J, h, temperatures, n_equil=300, n_sweeps=300,
                                dynamics="glauber", seed=7, n_jobs=1)

    print("Plotting phase diagram...")
    plot_phase_diagram(results, N=J.shape[0], savepath=FIGURES_DIR / "phase_diagram.png")

    print("Plotting alignment-vs-temperature curve...")
    plot_alignment_curve(results, empirical, savepath=FIGURES_DIR / "alignment_curve.png")

    accuracies = [np.mean(r["final_spins"] == empirical) for r in results]
    t_best = temperatures[int(np.argmax(accuracies))]
    print(f"Best empirical alignment at T = {t_best:.3g} ({max(accuracies):.1%} match)")

    best_result = results[int(np.argmax(accuracies))]
    plot_network_comparison(G, best_result["final_spins"], nodes,
                             savepath=FIGURES_DIR / "map_comparison.png")

    print(f"Figures written to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
