#!/usr/bin/env python3
"""Non-circular political field: geography + the 2022 runoff margin (PPSD
vs. PLN) as the predisposition field for predicting the REAL 2026 outcome,
in place of run_3d_scan.py's own-election h^pol.

Motivation: 2026's leading party (Pueblo Soberano) is the direct electoral
successor of 2022's winner (Progreso Social Democratico, PPSD) -- same
Chaves-aligned movement, different registered vehicle (confirmed via press
coverage, not just a naming coincidence). Every h^pol used elsewhere in this
project so far is built from the SAME election's own vote margin it's used
to predict, which is why the lambda_pol-extension scan in run_3d_scan.py
turned out circular (sign(h^pol) matches the label on 487/488 nodes by
construction). This field has no such problem: it's built entirely from
2022 votes and evaluated against 2026 votes.

A free correlation check (no MC) done before this script existed found the
2022 ROUND 1 PPSD share barely correlates with 2026 (r=0.147) -- round 1 was
a fragmented 25-candidate race that dilutes PPSD's real coalition -- but the
2022 RUNOFF margin (round 2, PPSD vs. PLN, already computed as h^pol by
run_3d_scan_2022.py) correlates strongly: r=0.704 with 2026's own margin,
r=0.565 with the 2026 outcome itself -- comparable in magnitude to
MIDEPLAN's composite IDS (r=-0.555) but non-circular. This script uses that
runoff margin, joined onto 2026's N=488 distrito node set (482/488 matched,
same 6 missing nodes as every other 2022-vs-2026 join in this project --
canton/distrito creation between cycles; missing nodes get h=0, not
dropped). No z-scoring needed -- margin = (votes_a-votes_b)/total is already
centered by construction (binarize.py), same as every other margin field
here.

Single field, no lambda weighting or combine_fields -- matches
run_distrito_ablation.py's Run B methodology exactly (geography + h,
h used as-is), just with a non-circular h this time. That keeps this
directly comparable to the existing distrito ablation's geography-only
baseline (66.2%) and this session's own geography-only point (67.64% @
T=2.605, from run_3d_scan.py's grid) rather than inventing a new baseline.

Modes match run_3d_scan.py: --validate (tiny smoke test), --estimate
(resource estimate, no run), default (full budget: n_equil=n_sweeps=20000,
16 seeds, 32 T in linspace(0.05, 5.0) -- identical to one grid point in the
original 3D scan).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.monte_carlo import pooled_temperature_scan
from isingcr.simulation.observables import mcnemar_seed_summary, symmetric_alignment_fraction
from run_3d_scan import (
    FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, FULL_T_RANGE,
    MAX_CORES_PER_TASK, MS_PER_SWEEP_DISTRITO,
    VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED, VALIDATE_TEMPERATURES,
)
from run_3d_scan import build_distrito_graph_and_fields as build_2026
from run_3d_scan_2022 import build_distrito_graph_and_fields as build_2022

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def build_graph_and_prior_field():
    J, _h_pol_own, _h_soc, nodes, empirical = build_2026()
    N = len(nodes)
    _J22, h_pol_2022_runoff, _h_soc_22, nodes22, _empirical22 = build_2022()

    lookup = dict(zip(nodes22, h_pol_2022_runoff))
    prior_margin = np.array([lookup.get(c, 0.0) for c in nodes])
    n_missing = sum(1 for c in nodes if c not in lookup)
    print(f"  2022 runoff (PPSD vs. PLN) margin joined onto 2026's N={N} distritos: "
          f"{n_missing}/{N} missing (h=0 for those, not dropped).")
    return J, prior_margin, nodes, empirical, n_missing


def scan(J, h, empirical, majority_label, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs):
    pooled = pooled_temperature_scan(J, h, temperatures, n_seeds=n_seeds,
                                      n_equil=n_equil, n_sweeps=n_sweeps,
                                      dynamics="glauber", seed=seed, n_jobs=n_jobs)
    per_t_accuracy = [
        float(np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
        for p in pooled
    ]
    best_idx = int(np.argmax(per_t_accuracy))
    mc = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical, majority_label)
    return {
        "best_T": float(temperatures[best_idx]), "best_accuracy": per_t_accuracy[best_idx],
        "accuracy_by_T": per_t_accuracy, "mcnemar_median_p": mc["median_exact_pvalue"],
    }


def estimate_resources(n_temperatures, n_seeds, n_equil, n_sweeps):
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)
    t_batches = -(-n_temperatures // cores_per_task)
    wall_seconds = n_seeds * t_batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    print("=== Resource estimate (grounded in 2026-08-16 cluster benchmark) ===")
    print(f"  1 field x {n_temperatures} T x {n_seeds} seeds")
    print(f"  Cores per task: {cores_per_task}")
    print(f"  Estimated wall time: {wall_seconds:.1f}s ({wall_seconds / 60:.1f} min)")
    return {"cores_per_task": cores_per_task, "wall_seconds": wall_seconds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--n-temperatures", type=int, default=32)
    args = parser.parse_args()

    if args.estimate and not args.validate:
        estimate_resources(args.n_temperatures, FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print("Building real N=488 2026 distrito network + non-circular 2022-runoff prior field...")
    t0 = time.time()
    J, h, nodes, empirical, n_missing = build_graph_and_prior_field()
    N = J.shape[0]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    if args.validate:
        n_equil, n_sweeps, n_seeds, seed = VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED
        temperatures = VALIDATE_TEMPERATURES
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        print(f"\n--validate mode: {len(temperatures)} T, {n_equil}+{n_sweeps} sweeps, {n_seeds} seed.")
    else:
        temperatures = np.linspace(*FULL_T_RANGE, args.n_temperatures)
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        estimate_resources(args.n_temperatures, n_seeds, n_equil, n_sweeps)

    t_start = time.time()
    r = scan(J, h, empirical, majority_label, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs)
    elapsed = time.time() - t_start
    print(f"\nprior_margin_field -> best T={r['best_T']:.3f}, best accuracy={r['best_accuracy']:.3%}, "
          f"McNemar median p={r['mcnemar_median_p']:.4f} ({elapsed:.1f}s)")

    if not args.validate:
        out_path = RESULTS_DIR / "prior_margin_field_2026.npz"
        np.savez(out_path, result=r, temperatures=temperatures, N=N, n_missing=n_missing,
                 n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
