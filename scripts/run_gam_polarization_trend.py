#!/usr/bin/env python3
"""Track the GAM (Gran Area Metropolitana) field's effective strength across
all three available elections (2018, 2022, 2026) -- using the model as an
instrument to ask whether Costa Rica's capital-vs-periphery political divide
is getting sharper or weaker over time, not just fitting one election.

Canton-level (not distrito), reusing run_historical_comparison.py's exact
election-loading machinery (same adjacency graph, same winner-vs-runner-up
binarization, same canton-scale MC budget that script already validated as
sufficient -- N~84 nodes converges fast, no need for distrito-scale
20000/20000 sweeps here). A bonus of canton level specifically: GAM's
31-canton list applies EXACTLY here, no partial-inclusion imprecision like
the distrito-level proxy used elsewhere in this project (run_gam_field.py's
docstring) -- every one of the 31 cantons genuinely is in GAM, full stop.

For each election: (1) the raw GAM-vs-periphery vote-share gap (no MC, the
plain magnitude of the divide), (2) geography-only vs. geography+GAM MC
accuracy, and (3) the direct paired significance test between them
(spatial_block_permutation_test_paired, PROVINCE-blocked -- matches
run_direct_paired_test.py's canton-level convention exactly, since canton-
level blocks would be degenerate at this granularity).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.ingestion import (
    binarize_votes,
    build_adjacency_graph,
    build_electoral_graph,
    load_shapefile,
    load_tse_juntas_consolidado,
    normalize_canton_code,
)
from isingcr.simulation.monte_carlo import pooled_temperature_scan
from isingcr.simulation.observables import mcnemar_seed_summary, symmetric_alignment_fraction
from isingcr.utils.graph_arrays import graph_to_arrays
from run_direct_paired_test import best_t_final_spins_aligned, paired_test, province_blocks
from run_gam_field import GAM_CANTONS

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL, CANTON_COL = "adm1_name", "adm2_name"

ELECTIONS = [
    {"label": "2018 (runoff)", "zip": DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2018.zip",
     "member": "ronda2/_consolidado_presidenciales.csv",
     "rename": {"ALAJUELA|VALVERDE VEGA": "ALAJUELA|SARCHI"}},
    {"label": "2022 (runoff)", "zip": DATA_RAW / "tse_juntas" / "juntas_TSE_2022_ronda2_provisional_y_definitivo.zip",
     "member": "_consolidado_definitivo.csv", "rename": {}},
    {"label": "2026 (round 1)", "zip": DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip",
     "member": "_consolidado_presidenciales.csv", "rename": {}},
]

TEMPERATURES = np.linspace(0.05, 3.5, 24)
N_EQUIL, N_SWEEPS, SEED, N_JOBS, N_SEEDS = 500, 500, 7, 8, 8
N_PERMUTATIONS = 999


def _top_two_parties(results, party_cols):
    totals = results[party_cols].sum().sort_values(ascending=False)
    return totals.index[0], totals.index[1], totals


def canton_of(node_code: str) -> str:
    return node_code.split("|")[0] + "|" + node_code.split("|")[1]


def load_election(election, adjacency):
    results = load_tse_juntas_consolidado(election["zip"], member=election["member"], level="canton")
    for old, new in election["rename"].items():
        results.loc[results["code"] == old, "code"] = new
    party_cols = [c for c in results.columns
                  if c not in ("code", "name", "provincia_pais", "canton_ciudad")]
    winner, runner_up, _ = _top_two_parties(results, party_cols)
    binarized = binarize_votes(results, [winner], [runner_up])

    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays = graph_to_arrays(G)
    J, nodes, empirical = arrays["J"], arrays["nodes"], arrays["spin_empirical"]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    return J, nodes, empirical, majority_label, winner, runner_up


def scan(J, h, empirical, majority_label, n_jobs):
    pooled = pooled_temperature_scan(J, h, TEMPERATURES, n_seeds=N_SEEDS,
                                      n_equil=N_EQUIL, n_sweeps=N_SWEEPS,
                                      dynamics="glauber", seed=SEED, n_jobs=n_jobs)
    accuracy = [float(np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
                for p in pooled]
    best_idx = int(np.argmax(accuracy))
    mc = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical, majority_label)
    return {"best_T": float(TEMPERATURES[best_idx]), "best_accuracy": accuracy[best_idx],
            "mcnemar_median_p": mc["median_exact_pvalue"]}


def main():
    gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

    results = {}
    for election in ELECTIONS:
        label = election["label"]
        print(f"\n=== {label} ===")
        J, nodes, empirical, majority_label, winner, runner_up = load_election(election, adjacency)
        N = J.shape[0]
        is_gam = np.array([canton_of(n) in GAM_CANTONS for n in nodes])
        h_gam = np.where(is_gam, 1.0, -1.0)

        gam_share = (empirical[is_gam] == 1).mean()
        periph_share = (empirical[~is_gam] == 1).mean()
        gap = abs(gam_share - periph_share) * 100
        print(f"  {winner} vs. {runner_up}, N={N}, GAM cantons={is_gam.sum()}/{N}")
        print(f"  Raw gap: leading-side share in GAM={gam_share:.1%}, in periphery={periph_share:.1%}, "
              f"gap={gap:.1f}pp")

        n_jobs = min(N_JOBS, len(TEMPERATURES))
        r_geo = scan(J, np.zeros(N), empirical, majority_label, n_jobs)
        r_gam = scan(J, h_gam, empirical, majority_label, n_jobs)
        print(f"  Geography-only: {r_geo['best_accuracy']:.2%} @ T={r_geo['best_T']:.3f} "
              f"(p={r_geo['mcnemar_median_p']:.4f})")
        print(f"  Geography+GAM:  {r_gam['best_accuracy']:.2%} @ T={r_gam['best_T']:.3f} "
              f"(p={r_gam['mcnemar_median_p']:.4f})")

        blocks = province_blocks(nodes)
        spins_a = best_t_final_spins_aligned(J, np.zeros(N), r_geo["best_T"], empirical,
                                              N_EQUIL, N_SWEEPS, N_SEEDS, n_jobs, SEED)
        spins_b = best_t_final_spins_aligned(J, h_gam, r_gam["best_T"], empirical,
                                              N_EQUIL, N_SWEEPS, N_SEEDS, n_jobs, SEED)
        paired = paired_test(f"{label}: geography-only vs. GAM", spins_a, spins_b, empirical,
                              blocks, N_SEEDS)

        results[label] = {"gap_pp": gap, "geo": r_geo, "gam": r_gam, "paired": paired}

    print(f"\n{'=' * 70}\nSummary: GAM polarization trend, 2018 -> 2022 -> 2026\n{'=' * 70}")
    print(f"{'Election':<16}{'Gap(pp)':>9}{'GeoOnly':>10}{'Geo+GAM':>10}{'Gain':>8}"
          f"{'PairedP':>10}{'sig/8':>7}")
    for label, r in results.items():
        gain = r["gam"]["best_accuracy"] - r["geo"]["best_accuracy"]
        sig = int(round(r["paired"]["frac_sig"] * N_SEEDS))
        print(f"{label:<16}{r['gap_pp']:>9.1f}{r['geo']['best_accuracy']:>10.2%}"
              f"{r['gam']['best_accuracy']:>10.2%}{gain:>+8.2%}{r['paired']['median_p']:>10.4f}"
              f"{sig:>6}/8")

    out = RESULTS_DIR / "gam_polarization_trend.npz"
    np.savez(out, **{f"{label}_gap_pp": r["gap_pp"] for label, r in results.items()},
             **{f"{label}_geo_acc": r["geo"]["best_accuracy"] for label, r in results.items()},
             **{f"{label}_gam_acc": r["gam"]["best_accuracy"] for label, r in results.items()},
             **{f"{label}_paired_p": r["paired"]["median_p"] for label, r in results.items()})
    print(f"\nRaw results written to {out}")


if __name__ == "__main__":
    main()
