#!/usr/bin/env python3
"""Heavier re-run of run_finite_size_scaling.py, sized for the UCR HPC cluster.

The local run (500 equil + 500 measurement sweeps, 8 seeds, 24 temperatures)
left the distrito (N~488) curve undersampled: several U4 values came out
negative, outside the physically valid [0, 2/3] equilibrium range, which
`00_Master_Notebook.md` flagged as "inconclusive, not a confirmed no-transition"
pending a heavier run. This script is that heavier run.

Sized from a cluster throughput benchmark (bench_distrito.py, 2026-08-16):
~2.03 ms/sweep at distrito scale (N=488) on one core of the `shared`
partition. n_equil=n_sweeps=20000 (40x the local run) is projected at ~81s
per (seed, temperature) -- with n_jobs=32 parallelizing across all 32
temperatures at once (32 is the p-serial QoS's MaxTRESPerJob cpu cap), that's
~81s/seed x 16 seeds ~= 22 min for the distrito curve, plus a few minutes for
the much cheaper canton (N=84) curve.

Everything else (Binder cumulant, h=0, crossing detection) is unchanged from
run_finite_size_scaling.py -- see that script's docstring for the physics
rationale. Output is deliberately kept in separate result/figure files
(*_heavy suffix) so the original "inconclusive" run stays on record rather
than being silently overwritten.
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
from isingcr.simulation.monte_carlo import pooled_temperature_scan
from isingcr.simulation.observables import binder_cumulant
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
CANTON_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]

TEMPERATURES = np.linspace(0.05, 3.5, 32)
N_EQUIL, N_SWEEPS, SEED, N_JOBS, N_SEEDS = 20000, 20000, 7, 32, 16


def build_canton_graph_and_votes():
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(CANTON_SHAPEFILE, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    return adjacency, binarized


def build_distrito_graph_and_votes():
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
    gdf = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    isolates = list(nx.isolates(adjacency))
    if isolates:
        print(f"  Dropping {len(isolates)} isolated distrito(s) (no adjacency neighbors, "
              f"pure noise at h=0): {isolates}")
        adjacency.remove_nodes_from(isolates)
    return adjacency, binarized


def run_binder_scan(adjacency, binarized, label):
    print(f"Running {label}: {N_SEEDS} seeds x {len(TEMPERATURES)} temperatures, "
          f"n_equil={N_EQUIL}, n_sweeps={N_SWEEPS}, n_jobs={N_JOBS}...", flush=True)
    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col=None)  # h=0
    arrays = graph_to_arrays(G)
    J, h = arrays["J"], arrays["h"]
    N = J.shape[0]

    pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=N_SEEDS,
                                      n_equil=N_EQUIL, n_sweeps=N_SWEEPS,
                                      dynamics="glauber", seed=SEED, n_jobs=N_JOBS)
    U4 = np.array([binder_cumulant(p["magnetization"]) for p in pooled])
    return {"label": label, "N": N, "U4": U4}


def find_crossings(temperatures, u4_a, u4_b):
    """Linearly interpolate every T where (u4_a - u4_b) changes sign."""
    diff = u4_a - u4_b
    crossings = []
    for i in range(len(temperatures) - 1):
        if np.isnan(diff[i]) or np.isnan(diff[i + 1]):
            continue
        if diff[i] == 0:
            crossings.append(float(temperatures[i]))
        elif diff[i] * diff[i + 1] < 0:
            t0, t1, d0, d1 = temperatures[i], temperatures[i + 1], diff[i], diff[i + 1]
            crossings.append(float(t0 + (0 - d0) * (t1 - t0) / (d1 - d0)))
    return crossings


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)

    canton_adj, canton_votes = build_canton_graph_and_votes()
    distrito_adj, distrito_votes = build_distrito_graph_and_votes()

    canton = run_binder_scan(canton_adj, canton_votes, "canton (N=84)")
    distrito = run_binder_scan(distrito_adj, distrito_votes, "distrito (N~490)")

    crossings = find_crossings(TEMPERATURES, canton["U4"], distrito["U4"])

    print(f"\n{'T':>6}{'U4 canton (N=' + str(canton['N']) + ')':>22}"
          f"{'U4 distrito (N=' + str(distrito['N']) + ')':>24}")
    for T, ua, ub in zip(TEMPERATURES, canton["U4"], distrito["U4"]):
        print(f"{T:>6.3f}{ua:>22.4f}{ub:>24.4f}")

    if crossings:
        print(f"\nCurves cross at T = {[round(c, 3) for c in crossings]}")
        if len(crossings) > 1:
            print("Multiple crossings -- almost certainly noise (two smooth physical "
                  "curves from a real transition cross once in this range), not a "
                  "confirmed critical point.")
    else:
        print("\nNo crossing found in the scanned range.")

    negative_u4_a = int(np.sum(canton["U4"] < 0))
    negative_u4_b = int(np.sum(distrito["U4"] < 0))
    print(f"\nUndersampling check: {negative_u4_a} (canton) / {negative_u4_b} (distrito) "
          f"negative U4 values (should be 0 at true equilibrium for a symmetric system; "
          f"the local run at n_equil=n_sweeps=500 had several). "
          f"{'Still undersampled -- treat as inconclusive.' if (negative_u4_a or negative_u4_b) else 'None found -- this run equilibrated cleanly.'}")

    np.savez(RESULTS_DIR / "finite_size_scaling_heavy.npz",
              temperatures=TEMPERATURES,
              U4_canton=canton["U4"], N_canton=canton["N"],
              U4_distrito=distrito["U4"], N_distrito=distrito["N"],
              crossings=np.array(crossings),
              n_equil=N_EQUIL, n_sweeps=N_SWEEPS, n_seeds=N_SEEDS)
    print(f"Raw results written to {RESULTS_DIR / 'finite_size_scaling_heavy.npz'}")

    plot(canton, distrito, crossings)
    print(f"Figure written to {FIGURES_DIR / 'finite_size_scaling_heavy.png'}")


def plot(canton, distrito, crossings):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(TEMPERATURES, canton["U4"], "o-", color="tab:blue", markersize=3,
             label=f"canton (N={canton['N']})")
    ax.plot(TEMPERATURES, distrito["U4"], "o-", color="tab:orange", markersize=3,
             label=f"distrito (N={distrito['N']})")
    for c in crossings:
        ax.axvline(c, color="gray", linestyle="--", linewidth=1)
    ax.axhspan(0, 2 / 3, color="green", alpha=0.05, label="physically valid U4 range")
    ax.set_xlabel("Temperature T")
    ax.set_ylabel("Binder cumulant U4")
    ax.set_title(f"Finite-size scaling (heavy: n_equil=n_sweeps={N_EQUIL}, "
                 f"{N_SEEDS} seeds, h=0, 2026 coalition split)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "finite_size_scaling_heavy.png", dpi=150)


if __name__ == "__main__":
    main()
