#!/usr/bin/env python3
"""Screen MIDEPLAN IDS 2023's five sub-dimensions individually, instead of
the composite score used by run_3d_scan.py / run_3d_scan_2022.py.

The composite IDS is itself a blend of SALUD (health), PARTICIPA
(participation), SEGURIDAD (security), EDUCACION (education), and ECONOMICO
(economic) -- see scripts/parse_mideplan_ids.py. A direct paired test found
the composite's effect real-but-borderline for 2026 (median p=0.058, 8/16
seed-pairs significant) and a clean null for 2022 (median p=0.405, 0/16
significant); this script checks whether that borderline 2026 signal is
diffuse across all five axes or concentrated in one or two.

Reuses `build_distrito_graph_and_fields()` from run_3d_scan.py (2026) /
run_3d_scan_2022.py (2022) for J, h_pol, nodes, empirical -- their returned
composite h_soc is discarded here in favor of one axis at a time, via the
new `load_mideplan_ids_axes` loader (isingcr.ingestion.mideplan_ids).

lambda_pol is fixed at 0.0 (isolates the social-axis contribution cleanly,
same reasoning as the composite's own direct-paired-test script) and
lambda_axis is fixed at 1.5 -- the composite's own peak point in the 2026
lambda_pol=0 row, so every axis is directly comparable to the composite
result at the same weight. Same MC budget/T-range as run_3d_scan.py's
FULL_* constants: one axis-index task here costs the same as one point in
the original 25-point grid.

Modes:
  --check-correlations   Free, no MC: pairwise correlation among the 5 raw
                          axes + composite, and each axis's correlation with
                          h_pol and the empirical outcome. Prints and exits.
  --validate              Tiny local smoke test (matches run_3d_scan.py's).
  --estimate              Print the resource estimate and exit.
  (default)                Full-budget single-T-scan for one axis/year.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.ingestion.mideplan_ids import ids_zscore_by_code, load_mideplan_ids, load_mideplan_ids_axes
from isingcr.simulation.observables import symmetric_alignment_fraction
from isingcr.simulation.two_field_energy import combine_fields
from run_3d_scan import (
    FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, FULL_T_RANGE,
    MAX_CORES_PER_TASK, MS_PER_SWEEP_DISTRITO,
    VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED,
    VALIDATE_TEMPERATURES,
    scan_point,
)
from run_3d_scan import build_distrito_graph_and_fields as build_2026
from run_3d_scan_2022 import build_distrito_graph_and_fields as build_2022

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
MIDEPLAN_IDS_CSV = DATA_RAW / "mideplan_ids_2023.csv"

AXES = ["salud", "participa", "seguridad", "educacion", "economico"]
LAMBDA_POL = 0.0
LAMBDA_AXIS = 1.5  # matches the composite's own peak in the 2026 lambda_pol=0 row

BUILDERS = {"2026": build_2026, "2022": build_2022}


def check_correlations(nodes, h_pol, empirical):
    ids_df = load_mideplan_ids(MIDEPLAN_IDS_CSV)
    axes_df = load_mideplan_ids_axes(MIDEPLAN_IDS_CSV)
    lookup = axes_df.set_index("code")
    ids_lookup = dict(zip(ids_df["code"], ids_df["ids_raw"]))

    cols = {"ids": [ids_lookup.get(c, np.nan) for c in nodes]}
    for axis in AXES:
        col = f"{axis}_raw"
        per_node = lookup[col].to_dict() if col in lookup.columns else {}
        cols[axis] = [per_node.get(c, np.nan) for c in nodes]
    cols["h_pol"] = h_pol
    cols["empirical"] = empirical.astype(float)

    df = pd.DataFrame(cols, index=nodes).dropna()
    print(f"n distritos with complete data: {len(df)}/{len(nodes)}\n")
    print("=== Pairwise correlation (composite + 5 axes + h_pol + empirical) ===")
    print(df.corr().round(3).to_string())


def estimate_resources_single_axis(n_temperatures, n_seeds, n_equil, n_sweeps):
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)
    t_batches = -(-n_temperatures // cores_per_task)
    wall_seconds = n_seeds * t_batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    print("=== Resource estimate (grounded in 2026-08-16 cluster benchmark) ===")
    print(f"  1 axis x {n_temperatures} T x {n_seeds} seeds")
    print(f"  Cores per task: {cores_per_task}")
    print(f"  Estimated wall time per task: {wall_seconds:.1f}s ({wall_seconds / 60:.1f} min)")
    print(f"  Full screen (5 axes x 2 years = 10 tasks): "
          f"{10 * wall_seconds / 60:.1f} min total wall (run as a SLURM array, not sequentially)")
    return {"cores_per_task": cores_per_task, "wall_seconds_per_task": wall_seconds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", choices=["2026", "2022"], default="2026")
    parser.add_argument("--axis-index", type=int, default=None,
                         help=f"0-{len(AXES) - 1}, indexing into {AXES}. Required unless "
                              "--check-correlations/--validate/--estimate.")
    parser.add_argument("--check-correlations", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--n-temperatures", type=int, default=32)
    args = parser.parse_args()

    if not (args.check_correlations or args.validate or args.estimate) and args.axis_index is None:
        parser.error("--axis-index is required outside --check-correlations/--validate/--estimate")
    if args.axis_index is not None and not (0 <= args.axis_index < len(AXES)):
        parser.error(f"--axis-index must be in [0, {len(AXES) - 1}]")

    if args.estimate and not args.validate and not args.check_correlations:
        estimate_resources_single_axis(args.n_temperatures, FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    build_fn = BUILDERS[args.year]
    print(f"Building real distrito adjacency network + h^pol ({args.year}) + h^soc axes...")
    t0 = time.time()
    J, h_pol, _composite_h_soc, nodes, empirical = build_fn()
    N = J.shape[0]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    if args.check_correlations:
        check_correlations(nodes, h_pol, empirical)
        return

    axes_df = load_mideplan_ids_axes(MIDEPLAN_IDS_CSV)

    if args.validate:
        axis_index = args.axis_index if args.axis_index is not None else 0
        axis = AXES[axis_index]
        h_axis, n_missing = ids_zscore_by_code(axes_df, nodes, ids_col=f"{axis}_raw")
        print(f"\n--validate mode: axis={axis}, {n_missing}/{N} distritos missing this axis "
              f"(h_soc=0 for those).")
        r = scan_point(J, h_pol, h_axis, empirical, majority_label, LAMBDA_POL, LAMBDA_AXIS,
                        VALIDATE_TEMPERATURES, VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS,
                        VALIDATE_N_SEEDS, VALIDATE_SEED, min(MAX_CORES_PER_TASK, len(VALIDATE_TEMPERATURES)))
        print(f"  axis={axis} -> best T={r['best_T']:.3f}, best accuracy={r['best_accuracy']:.3%}, "
              f"McNemar median p={r['mcnemar_median_p']:.4f}")
        return

    axis = AXES[args.axis_index]
    h_axis, n_missing = ids_zscore_by_code(axes_df, nodes, ids_col=f"{axis}_raw")
    print(f"  axis={axis}: {n_missing}/{N} distritos missing this axis (h_soc=0 for those).")

    temperatures = np.linspace(*FULL_T_RANGE, args.n_temperatures)
    n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
    estimate_resources_single_axis(args.n_temperatures, FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)

    t_start = time.time()
    r = scan_point(J, h_pol, h_axis, empirical, majority_label, LAMBDA_POL, LAMBDA_AXIS,
                    temperatures, FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, n_jobs)
    elapsed = time.time() - t_start
    print(f"\naxis={axis} year={args.year} -> best T={r['best_T']:.3f}, "
          f"best accuracy={r['best_accuracy']:.3%}, McNemar median p={r['mcnemar_median_p']:.4f} "
          f"({elapsed:.1f}s)")

    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    out_path = RESULTS_DIR / f"mideplan_axis_{args.year}_{axis}.npz"
    np.savez(out_path, result=r, temperatures=temperatures, N=N,
             n_equil=FULL_N_EQUIL, n_sweeps=FULL_N_SWEEPS, n_seeds=FULL_N_SEEDS,
             axis=axis, year=args.year, lambda_pol=LAMBDA_POL, lambda_axis=LAMBDA_AXIS)
    print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
