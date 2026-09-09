#!/usr/bin/env python3
"""lambda_soc scan for the political-continuity field (2022 runoff PPSD
margin joined onto the 2026 N=488 distrito network), mirroring
run_gam_lambda_scan.py point for point.

Why: the manuscript ranks GAM above this field at unit weight only. The
political field has sigma=0.167 against +/-1 for GAM, so lambda_soc=1
injects roughly one sixth of GAM's nominal field strength, and its
sign-agreement ceiling on the coalition split (80.6%) is essentially GAM's
(80.9%). A lambda scan is the direct test of whether the gap closes once
the field is weight-matched (lambda~6 equalizes the standard deviation).

Grid: [0.5, 1, 2, 3, 4, 6, 8, 12, 16] (first submission) extended by
[24, 32, 48, 64] (second submission, array indices 9-12) because the curve
was still rising at 16; lambda=1 reproduces
run_prior_margin_field.py's headline run under the identical seed set.
Same budget as every other headline number (16 seeds, 20000+20000 sweeps,
32 T in [0.05, 5.0]). One lambda point per SLURM array task.
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
from run_prior_margin_field import build_graph_and_prior_field

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

LAMBDA_GRID = [0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0, 32.0, 48.0, 64.0]


def scan_point(J, h_gam, lam, empirical, majority_label, temperatures,
               n_equil, n_sweeps, n_seeds, seed, n_jobs):
    h_eff = lam * h_gam
    pooled = pooled_temperature_scan(J, h_eff, temperatures, n_seeds=n_seeds,
                                      n_equil=n_equil, n_sweeps=n_sweeps,
                                      dynamics="glauber", seed=seed, n_jobs=n_jobs)
    per_t_accuracy = [
        float(np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
        for p in pooled
    ]
    per_t_std = [
        float(np.std([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
        for p in pooled
    ]
    best_idx = int(np.argmax(per_t_accuracy))
    mc = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical, majority_label)
    return {
        "lambda_soc": lam,
        "best_T": float(temperatures[best_idx]),
        "best_accuracy": per_t_accuracy[best_idx],
        "best_accuracy_std": per_t_std[best_idx],
        "accuracy_by_T": per_t_accuracy,
        "mcnemar_median_p": mc["median_exact_pvalue"],
        "mcnemar_fraction_significant": mc["fraction_significant_at_0.05"],
        "best_final_spins": np.array(pooled[best_idx]["final_spins_per_seed"]),
    }


def estimate_resources(n_temperatures, n_seeds, n_equil, n_sweeps):
    cores = min(MAX_CORES_PER_TASK, n_temperatures)
    batches = -(-n_temperatures // cores)
    wall = n_seeds * batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    print("=== Resource estimate (grounded in 2026-08-16 cluster benchmark) ===")
    print(f"  {len(LAMBDA_GRID)} lambda points x {n_temperatures} T x {n_seeds} seeds")
    print(f"  Cores per task: {cores}; est. wall per lambda point: {wall:.0f}s ({wall/60:.1f} min)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--n-temperatures", type=int, default=32)
    parser.add_argument("--lambda-index", type=int, default=None,
                        help="Run only LAMBDA_GRID[index] (SLURM array mode).")
    args = parser.parse_args()

    if args.estimate and not args.validate:
        estimate_resources(args.n_temperatures, FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print("Building real 2026 distrito network + political-continuity (2022 runoff) field...")
    t0 = time.time()
    J, h_gam, nodes, empirical, _n_missing = build_graph_and_prior_field()
    N = J.shape[0]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    if args.validate:
        temperatures = VALIDATE_TEMPERATURES
        lambdas = [0.5, 2.0]
        n_equil, n_sweeps, n_seeds, seed = VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED
        print(f"\n--validate mode: {len(lambdas)} lambda x {len(temperatures)} T, "
              f"{n_equil}+{n_sweeps} sweeps, {n_seeds} seed -- smoke test only.")
    else:
        temperatures = np.linspace(*FULL_T_RANGE, args.n_temperatures)
        lambdas = [LAMBDA_GRID[args.lambda_index]] if args.lambda_index is not None else LAMBDA_GRID
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
        estimate_resources(args.n_temperatures, n_seeds, n_equil, n_sweeps)
    n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))

    results = []
    t_start = time.time()
    for lam in lambdas:
        r = scan_point(J, h_gam, lam, empirical, majority_label, temperatures,
                       n_equil, n_sweeps, n_seeds, seed, n_jobs)
        results.append(r)
        print(f"  lambda_soc={lam:.2f} -> best T={r['best_T']:.3f}, "
              f"best accuracy={r['best_accuracy']:.3%} +/- {r['best_accuracy_std']:.3%}, "
              f"McNemar median p={r['mcnemar_median_p']:.4g}")
    print(f"\n{len(lambdas)} lambda point(s) scanned in {time.time() - t_start:.1f}s.")

    if not args.validate:
        suffix = f"_lam{args.lambda_index}" if args.lambda_index is not None else ""
        out_path = RESULTS_DIR / f"prior_lambda_scan_2026{suffix}.npz"
        np.savez(out_path, results=np.array(results, dtype=object),
                 lambda_grid=np.array(LAMBDA_GRID), temperatures=temperatures,
                 nodes=np.array(nodes), empirical=empirical, N=N,
                 n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
