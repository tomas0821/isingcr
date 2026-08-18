#!/usr/bin/env python3
"""Finite-size scaling: is there a real critical point, at two different N?

Every pooled temperature scan run so far in this project (run_ablation.py,
run_historical_comparison.py) found the same thing: susceptibility/specific
heat monotonically blow up toward T->0 with no interior bump, the signature of
a low-T pooling artifact (see pooled_temperature_scan's docstring), not a real
critical point. This script asks the question those scans can't: using the
canonical way statistical mechanics locates a genuine critical point
independent of system size -- the Binder cumulant crossing.

U4(T) = 1 - <m^4>/(3<m^2>^2) run at two different system sizes N should cross
at a single T that both curves agree on, if a real phase transition exists;
if there's no real transition (or the two N's are both far from any
thermodynamic-limit behavior), the curves either don't cross or cross
somewhere that drifts with more seeds/sweeps.

Real canton-level (N=84) and distrito-level (N=492) geometry and 2026 TSE data
give exactly the two system sizes needed, on the same country, same election,
same real adjacency structure -- nothing else in this project has both ready
to compare. **h=0 for both**, deliberately: the Binder cumulant crossing
technique's standard textbook interpretation assumes a symmetric order
parameter (m -> -m symmetry), which only literally holds at h=0 -- see
README "A physics note". h=0 also means U4 doesn't care about sign at all
(m^2, m^4 are sign-invariant), so there's no symmetric_alignment_fraction-style
sign bookkeeping needed here.

Costa Rica's distrito layer has 2 island distritos with no adjacency neighbors
(Isla del Coco, Chira -- see shapefile_adjacency's isolate warning). At h=0 a
fully isolated node has zero local field at every T, so it's a pure 50/50 coin
flip regardless of temperature -- physically uninformative noise for a
coupling-driven diagnostic like this one. They're dropped before the scan.
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

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
CANTON_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]

TEMPERATURES = np.linspace(0.05, 3.5, 24)
N_EQUIL, N_SWEEPS, SEED, N_JOBS, N_SEEDS = 500, 500, 7, 8, 8


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
          f"n_jobs={N_JOBS}...")
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

    canton_adj, canton_votes = build_canton_graph_and_votes()
    distrito_adj, distrito_votes = build_distrito_graph_and_votes()

    canton = run_binder_scan(canton_adj, canton_votes, "canton (N=84)")
    distrito = run_binder_scan(distrito_adj, distrito_votes, "distrito (N~490)")

    crossings = find_crossings(TEMPERATURES, canton["U4"], distrito["U4"])

    print(f"\n{'T':>6}{'U4 canton (N=' + str(canton['N']) + ')':>22}"
          f"{'U4 distrito (N=' + str(distrito['N']) + ')':>24}")
    for T, ua, ub in zip(TEMPERATURES, canton["U4"], distrito["U4"]):
        print(f"{T:>6.2f}{ua:>22.4f}{ub:>24.4f}")

    if crossings:
        print(f"\nCurves cross at T = {[round(c, 3) for c in crossings]}")
        if len(crossings) > 1:
            print("Multiple crossings -- almost certainly noise (two smooth physical "
                  "curves from a real transition cross once in this range), not a "
                  "confirmed critical point. Would need more seeds/sweeps to tell.")
    else:
        print("\nNo crossing found in the scanned range.")

    negative_u4_a = int(np.sum(canton["U4"] < 0))
    negative_u4_b = int(np.sum(distrito["U4"] < 0))
    if negative_u4_a or negative_u4_b:
        print(f"\nCaveat this result is inconclusive, not a confident 'no transition': "
              f"U4 has {negative_u4_a} (canton) / {negative_u4_b} (distrito) negative "
              f"values, which shouldn't happen at true equilibrium for a symmetric "
              f"system (U4 in [0, 2/3]). That's a sign of undersampling, not physics --"
              f" likely N={distrito['N']} needs more n_equil/n_sweeps than N={canton['N']}"
              f" does to equilibrate properly at this seed count, a standard finite-size"
              f" scaling issue (larger systems generally need longer runs). The 'no "
              f"shared crossing' read above should be treated as unconfirmed pending a "
              f"heavier run, not as evidence against a real critical point.")

    plot(canton, distrito, crossings)
    print(f"\nFigure written to {FIGURES_DIR / 'finite_size_scaling.png'}")


def plot(canton, distrito, crossings):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(TEMPERATURES, canton["U4"], "o-", color="tab:blue",
             label=f"canton (N={canton['N']})")
    ax.plot(TEMPERATURES, distrito["U4"], "o-", color="tab:orange",
             label=f"distrito (N={distrito['N']})")
    for c in crossings:
        ax.axvline(c, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Temperature T")
    ax.set_ylabel("Binder cumulant U4")
    ax.set_title("Finite-size scaling: Binder cumulant crossing (h=0, 2026 coalition split)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "finite_size_scaling.png", dpi=150)


if __name__ == "__main__":
    main()
