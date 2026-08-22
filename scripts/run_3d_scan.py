#!/usr/bin/env python3
"""3D parameter scan: lambda_pol x lambda_soc x T, distrito-level (N=488).

Combines two independent external fields -- h^pol (real 2026 vote margin,
same field every other distrito script uses) and h^soc (MIDEPLAN Indice de
Desarrollo Social 2023, z-scored) -- under
    E(s) = -sum_<ij> J_ij s_i s_j - sum_i (lambda_pol h_i^pol + lambda_soc h_i^soc) s_i
via `isingcr.simulation.two_field_energy.combine_fields`, then hands the
resulting effective field to the existing, unmodified
`isingcr.simulation.monte_carlo.pooled_temperature_scan` -- the MC engine and
the real J_ij adjacency network are untouched by this script; only the field
construction is new. See two_field_energy.py's docstring for why that's
physically exact, not an approximation.

Two run modes:
  --validate   2 temperatures x 2 (lambda_pol, lambda_soc) combinations,
               n_equil=50/n_sweeps=50 (100 MC sweeps total), 1 seed -- a
               smoke test proving the pipeline runs end to end, meant to
               finish in well under a minute locally. Not a research result.
  (default)    the full grid defined by --n-lambda-pol/--n-lambda-soc/
               --n-temperatures, at the distrito-scale budget
               (n_equil=n_sweeps=20000, 16 seeds -- matching
               run_distrito_ablation.py) -- meant for the cluster, not a
               laptop; see --estimate.

  --estimate   print the task count / core / wall-time estimate for the
               *current* grid settings and exit, without running anything.
               Reuses the measured ~2.03 ms/sweep-at-distrito-scale
               throughput benchmark from run_finite_size_scaling_heavy.py's
               2026-08-16 UCR HPC cluster run (`shared` partition, node
               cn002, 32 cores = the p-serial QoS's MaxTRESPerJob cap) so
               the estimate is grounded in a real measurement on this
               project's actual cluster, not a guess.

MIDEPLAN's real IDS 2023 CSV is not present under data/raw/ as of writing
(see mideplan_ids.py's docstring) -- if data/raw/mideplan_ids_2023.csv is
missing, this script falls back to a small seeded synthetic h^soc so the
pipeline is still runnable end to end, loudly logging that it did so. This
mirrors run_demo.py's existing synthetic-data-for-validation convention;
swap in the real file (no code changes needed) once available.
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

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
MIDEPLAN_IDS_CSV = DATA_RAW / "mideplan_ids_2023.csv"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]

# Full-grid (cluster) budget -- matches run_distrito_ablation.py exactly.
FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED = 20000, 20000, 16, 7
FULL_T_RANGE = (0.05, 5.0)  # wider than the 1D ablations' [0.05, 3.5] per this scan's spec

# Local smoke-test budget -- deliberately tiny, see --validate above.
VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED = 50, 50, 1, 7
VALIDATE_TEMPERATURES = np.array([0.5, 2.0])
VALIDATE_LAMBDA_COMBOS = [(1.0, 0.0), (0.5, 0.5)]  # 2 lambda "ratios"

# Measured 2026-08-16, UCR HPC cluster, `shared` partition, node cn002, one
# core, distrito scale (N=488) -- see run_finite_size_scaling_heavy.py.
MS_PER_SWEEP_DISTRITO = 2.03
MAX_CORES_PER_TASK = 32  # p-serial QoS's MaxTRESPerJob cap on this cluster


def build_distrito_graph_and_fields():
    """Real N=488 distrito adjacency (J) + real h^pol (2026 vote margin) +
    h^soc (MIDEPLAN IDS z-score, real if data/raw/mideplan_ids_2023.csv
    exists, else a loudly-flagged seeded synthetic placeholder)."""
    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)

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
              f"{n_missing}/{len(nodes)} distritos missing an IDS score (h_soc=0 for those).")
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
    """Task count / cores-per-task / wall-time estimate for the SLURM array
    template, grounded in the ~2.03 ms/sweep distrito-scale benchmark."""
    n_tasks = n_lambda_pol * n_lambda_soc  # one SLURM array task per (lambda_pol, lambda_soc)
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)  # pooled_temperature_scan parallelizes over T
    t_batches = -(-n_temperatures // cores_per_task)  # ceil: batches if n_temperatures > cores_per_task
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
    if n_tasks > 1 and wall_seconds_per_task > 600:
        print(f"  -> Suggest submitting as a SLURM job array (--array=0-{n_tasks - 1}) on the "
              f"`shared` partition / p-serial QoS, {cores_per_task} cores per task.")
    else:
        print("  -> Small enough for a single job / interactive session; no array needed.")
    return {"n_tasks": n_tasks, "cores_per_task": cores_per_task,
            "wall_seconds_per_task": wall_seconds_per_task,
            "total_core_seconds": total_core_seconds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true",
                         help="Tiny local smoke test: 2 T x 2 lambda combos, 100 sweeps, 1 seed.")
    parser.add_argument("--estimate", action="store_true",
                         help="Print the resource estimate for the current grid and exit.")
    parser.add_argument("--n-lambda-pol", type=int, default=5)
    parser.add_argument("--n-lambda-soc", type=int, default=5)
    parser.add_argument("--n-temperatures", type=int, default=32)
    parser.add_argument("--lambda-max", type=float, default=2.0)
    parser.add_argument("--output-prefix", type=str, default="scan_3d",
                         help="Prefix for output .npz filenames (scan_3d_pol<i>_soc<j>.npz). "
                              "Change this for any follow-up scan with a different grid "
                              "(different --lambda-max/--n-lambda-pol/--n-lambda-soc) than a "
                              "prior run -- grid indices are NOT physically comparable across "
                              "different linspace ranges, so reusing the default prefix would "
                              "silently overwrite an earlier real result with a different point "
                              "that happens to share the same (i, j) index.")
    parser.add_argument("--lambda-pol-index", type=int, default=None,
                         help="Restrict to a single lambda_pol grid point (0-indexed). "
                              "For SLURM array tasks: one task = one (pol-index, soc-index) "
                              "pair, letting each array task run just its own grid point "
                              "instead of the whole grid in one process.")
    parser.add_argument("--lambda-soc-index", type=int, default=None,
                         help="Restrict to a single lambda_soc grid point (0-indexed); see "
                              "--lambda-pol-index.")
    args = parser.parse_args()

    have_pol_idx, have_soc_idx = args.lambda_pol_index is not None, args.lambda_soc_index is not None
    if have_pol_idx != have_soc_idx:
        parser.error("--lambda-pol-index and --lambda-soc-index must be given together")

    if args.estimate and not args.validate:
        estimate_resources(args.n_lambda_pol, args.n_lambda_soc, args.n_temperatures,
                            FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print("Building real N=488 distrito adjacency network + h^pol + h^soc...")
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
