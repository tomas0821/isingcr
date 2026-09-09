#!/usr/bin/env python3
"""3D parameter scan for the 2022 runoff: lambda_pol x lambda_soc x T,
distrito-level (N=483 -- 5 fewer than 2026's N=488, all explainable by
cantons/distritos created after 2022, e.g. Monteverde/Puerto Jimenez; see
run_historical_comparison.py's docstring for the canton-level version of the
same pattern).

Same model, same MC engine, same MIDEPLAN IDS 2023 social-development field
as run_3d_scan.py -- see that script's docstring for the physics and the
--validate/--estimate modes, unchanged here. The only real differences:

- Election data: the 2022 runoff (`juntas_TSE_2022_ronda2_provisional_y_
  definitivo.zip`, `_consolidado_definitivo.csv`), not 2026.
- Binarization: winner-vs-runner-up, computed dynamically from whichever two
  parties actually appear in the file, matching run_historical_comparison.py
  and run_distrito_ablation_wvru.py's convention -- the 2022 runoff already
  is a 2-candidate contest by construction (PROGRESO SOCIAL DEMOCRATICO vs.
  LIBERACION NACIONAL), unlike 2026's multi-party first round, which needed
  the coalition-split construction instead.
- MIDEPLAN's IDS is still the 2023 snapshot (no earlier version exists) --
  applying it to a 2022 outcome means the social-development field
  postdates the election by about a year, a bigger temporal gap than for
  2026 (where the index roughly coincides with the election). Development
  indices are slow-moving relative to a single election cycle, but this is
  a real caveat worth stating explicitly, not silently assuming away.
- Default --output-prefix is "scan_3d_2022", not "scan_3d" -- a different
  election's grid is not comparable point-for-point with 2026's even at
  the same (i, j) index, so it must never share a filename prefix with it.
"""

from __future__ import annotations

import argparse
import sys
import time
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
from isingcr.ingestion.mideplan_ids import ids_zscore_by_code, load_mideplan_ids
from isingcr.simulation.monte_carlo import pooled_temperature_scan
from isingcr.simulation.observables import mcnemar_seed_summary, symmetric_alignment_fraction
from isingcr.simulation.two_field_energy import combine_fields
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "juntas_TSE_2022_ronda2_provisional_y_definitivo.zip"
TSE_MEMBER = "_consolidado_definitivo.csv"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
MIDEPLAN_IDS_CSV = DATA_RAW / "mideplan_ids_2023.csv"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

# Full-grid (cluster) budget -- matches run_3d_scan.py exactly.
FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED = 20000, 20000, 16, 7
FULL_T_RANGE = (0.05, 5.0)

# Local smoke-test budget -- deliberately tiny, see run_3d_scan.py's --validate.
VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED = 50, 50, 1, 7
VALIDATE_TEMPERATURES = np.array([0.5, 2.0])
VALIDATE_LAMBDA_COMBOS = [(1.0, 0.0), (0.5, 0.5)]

# Measured 2026-08-16, UCR HPC cluster -- see run_3d_scan.py / run_finite_size_scaling_heavy.py.
MS_PER_SWEEP_DISTRITO = 2.03
MAX_CORES_PER_TASK = 32


def build_distrito_graph_and_fields():
    """Real N=483 2022-runoff distrito adjacency (J) + real h^pol (2022
    winner-vs-runner-up margin) + h^soc (MIDEPLAN IDS z-score, real if
    data/raw/mideplan_ids_2023.csv exists, else a loudly-flagged seeded
    synthetic placeholder -- see run_3d_scan.py)."""
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
    party_cols = [c for c in results.columns
                  if c not in ("code", "name", "provincia_pais", "canton_ciudad", "distrito")]
    totals = results[party_cols].sum().sort_values(ascending=False)
    winner, runner_up = totals.index[0], totals.index[1]
    print(f"  2022 runoff winner vs. runner-up (by national vote count): {winner} vs. {runner_up}")
    binarized = binarize_votes(results, [winner], [runner_up])

    gdf = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
    gdf["code"] = [normalize_distrito_code(p, c, d)
                   for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")
    isolates = list(nx.isolates(adjacency))
    if isolates:
        print(f"  Dropping {len(isolates)} isolated distrito(s): {isolates}")
        adjacency.remove_nodes_from(isolates)

    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays = graph_to_arrays(G)
    J, h_pol, nodes, empirical = arrays["J"], arrays["h"], arrays["nodes"], arrays["spin_empirical"]

    if MIDEPLAN_IDS_CSV.exists():
        ids_df = load_mideplan_ids(MIDEPLAN_IDS_CSV)
        h_soc, n_missing = ids_zscore_by_code(ids_df, nodes)
        print(f"  MIDEPLAN IDS 2023 loaded from {MIDEPLAN_IDS_CSV.name}: "
              f"{n_missing}/{len(nodes)} distritos missing an IDS score (h_soc=0 for those). "
              f"NOTE: this index postdates the 2022 election by about a year.")
    else:
        print(f"  *** {MIDEPLAN_IDS_CSV.name} not found under data/raw/ -- using a SEEDED "
              f"SYNTHETIC h^soc placeholder (mean 0, std 1) so this script still runs "
              f"end to end. Not a research result; swap in the real MIDEPLAN file. ***")
        rng = np.random.default_rng(20230101)
        h_soc = rng.normal(loc=0.0, scale=1.0, size=len(nodes))

    return J, h_pol, h_soc, nodes, empirical


def scan_point(J, h_pol, h_soc, empirical, majority_label, lambda_pol, lambda_soc,
                temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs):
    h_eff = combine_fields(h_pol, h_soc, lambda_pol, lambda_soc)
    pooled = pooled_temperature_scan(J, h_eff, temperatures, n_seeds=n_seeds,
                                      n_equil=n_equil, n_sweeps=n_sweeps,
                                      dynamics="glauber", seed=seed, n_jobs=n_jobs)
    per_t_accuracy = [
        float(np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
        for p in pooled
    ]
    best_idx = int(np.argmax(per_t_accuracy))
    mc = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical, majority_label)
    return {
        "lambda_pol": lambda_pol, "lambda_soc": lambda_soc,
        "best_T": float(temperatures[best_idx]), "best_accuracy": per_t_accuracy[best_idx],
        "accuracy_by_T": per_t_accuracy, "mcnemar_median_p": mc["median_exact_pvalue"],
    }


def estimate_resources(n_lambda_pol, n_lambda_soc, n_temperatures, n_seeds, n_equil, n_sweeps):
    n_tasks = n_lambda_pol * n_lambda_soc
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)
    t_batches = -(-n_temperatures // cores_per_task)
    wall_seconds_per_task = n_seeds * t_batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    total_core_seconds = n_tasks * cores_per_task * wall_seconds_per_task

    print("=== Resource estimate (grounded in 2026-08-16 cluster benchmark) ===")
    print(f"  Grid: {n_lambda_pol} lambda_pol x {n_lambda_soc} lambda_soc x {n_temperatures} T "
          f"x {n_seeds} seeds")
    print(f"  SLURM array tasks (one per lambda_pol/lambda_soc pair): {n_tasks}")
    print(f"  Cores per task (parallelizes over T, capped at p-serial QoS's "
          f"{MAX_CORES_PER_TASK}): {cores_per_task}")
    print(f"  Estimated wall time per task: {wall_seconds_per_task:.1f}s "
          f"({wall_seconds_per_task / 60:.1f} min)")
    print(f"  Estimated total core-hours (all tasks, sequential array): "
          f"{total_core_seconds / 3600:.2f}")
    return {"n_tasks": n_tasks, "cores_per_task": cores_per_task,
            "wall_seconds_per_task": wall_seconds_per_task,
            "total_core_seconds": total_core_seconds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--n-lambda-pol", type=int, default=5)
    parser.add_argument("--n-lambda-soc", type=int, default=5)
    parser.add_argument("--n-temperatures", type=int, default=32)
    parser.add_argument("--lambda-max", type=float, default=2.0)
    parser.add_argument("--output-prefix", type=str, default="scan_3d_2022")
    parser.add_argument("--lambda-pol-index", type=int, default=None)
    parser.add_argument("--lambda-soc-index", type=int, default=None)
    args = parser.parse_args()

    have_pol_idx, have_soc_idx = args.lambda_pol_index is not None, args.lambda_soc_index is not None
    if have_pol_idx != have_soc_idx:
        parser.error("--lambda-pol-index and --lambda-soc-index must be given together")

    if args.estimate and not args.validate:
        estimate_resources(args.n_lambda_pol, args.n_lambda_soc, args.n_temperatures,
                            FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print("Building real 2022-runoff distrito adjacency network + h^pol + h^soc...")
    t0 = time.time()
    J, h_pol, h_soc, nodes, empirical = build_distrito_graph_and_fields()
    N = J.shape[0]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    if args.validate:
        temperatures = VALIDATE_TEMPERATURES
        lambda_combos = VALIDATE_LAMBDA_COMBOS
        n_equil, n_sweeps, n_seeds, seed = (VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS,
                                             VALIDATE_N_SEEDS, VALIDATE_SEED)
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        print(f"\n--validate mode: {len(lambda_combos)} lambda combos x {len(temperatures)} T, "
              f"{n_equil}+{n_sweeps} sweeps, {n_seeds} seed -- smoke test only.")
    else:
        temperatures = np.linspace(*FULL_T_RANGE, args.n_temperatures)
        lambda_values_pol = np.linspace(0.0, args.lambda_max, args.n_lambda_pol)
        lambda_values_soc = np.linspace(0.0, args.lambda_max, args.n_lambda_soc)

        if have_pol_idx:
            lambda_combos = [(lambda_values_pol[args.lambda_pol_index],
                               lambda_values_soc[args.lambda_soc_index])]
            print(f"Single grid point selected: pol-index={args.lambda_pol_index}, "
                  f"soc-index={args.lambda_soc_index} (SLURM array task mode)")
        else:
            lambda_combos = [(lp, ls) for lp in lambda_values_pol for ls in lambda_values_soc]

        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        estimate_resources(args.n_lambda_pol, args.n_lambda_soc, args.n_temperatures,
                            n_seeds, n_equil, n_sweeps)

    results = []
    t_start = time.time()
    for lambda_pol, lambda_soc in lambda_combos:
        r = scan_point(J, h_pol, h_soc, empirical, majority_label, lambda_pol, lambda_soc,
                        temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs)
        results.append(r)
        print(f"  lambda_pol={lambda_pol:.3f} lambda_soc={lambda_soc:.3f} -> "
              f"best T={r['best_T']:.3f}, best accuracy={r['best_accuracy']:.3%}, "
              f"McNemar median p={r['mcnemar_median_p']:.4f}")

    elapsed = time.time() - t_start
    print(f"\n{len(lambda_combos)} lambda combo(s) x {len(temperatures)} T scanned in "
          f"{elapsed:.1f}s.")

    if not args.validate:
        if args.lambda_pol_index is not None:
            out_path = RESULTS_DIR / f"{args.output_prefix}_pol{args.lambda_pol_index}_soc{args.lambda_soc_index}.npz"
        else:
            out_path = RESULTS_DIR / f"{args.output_prefix}.npz"
        np.savez(out_path, results=np.array(results, dtype=object),
                 temperatures=temperatures, N=N,
                 n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
