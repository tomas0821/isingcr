#!/usr/bin/env python3
"""lambda_soc scan for the GAM field, 2026, distrito level (N=488).

Closes a gap the manuscript's Supplementary Material states explicitly:
GAM was only ever run unweighted (lambda_soc=1, run_gam_field.py), never
lambda-scanned the way MIDEPLAN's peak was (run_3d_scan.py). This scan
answers two questions the paper could not:

1. What is GAM's optimal field weight lambda* -- i.e., with h_GAM = +/-1
   and mean J_ij = 1 by construction, the effective field-to-coupling ratio
   at which capital-region membership best reproduces the real map. That is
   a physics-native statement ("the capital/periphery divide is worth X
   units of neighbor contagion") no regression coefficient provides.
2. Does GAM PEAK at finite lambda and then decline, or climb monotonically
   toward its own sign-agreement ceiling the way the circular own-margin
   field did (67.64% -> 92.70% over lambda_pol in [0,8], best-T collapsing
   to 0.37 -- Section "A second predisposition field")? A finite peak is the
   signature of a genuine predisposition field interacting with the
   coupling term; monotonic saturation is the signature of a field that
   simply overwhelms it. GAM's sign-agreement ceiling with the 2026 outcome
   is far below 100% (31.7% of GAM distritos vs 88.7% of periphery on the
   leading side), so the two behaviors are distinguishable here.

Grid: explicit lambda_soc points [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 8].
lambda=0 is the geography-only baseline (67.64%, already on disk from
run_3d_scan.py); lambda=1 duplicates run_gam_field.py's headline run under
the identical seed set as an internal consistency check. Same MC budget as
every other headline number (16 seeds, 20000+20000 sweeps, 32 T in
[0.05, 5.0]). One lambda point per SLURM array task (--lambda-index).

Also saves each lambda point's best-T final spin configurations (all 16
seeds) so the fitted equilibrium's energy can be decomposed into coupling
vs. field contributions post hoc without re-running MC.
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
from run_gam_field import build_graph_and_gam_field

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

LAMBDA_GRID = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 8.0]


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
    print("Building real 2026 distrito network + GAM field...")
    t0 = time.time()
    J, h_gam, nodes, empirical = build_graph_and_gam_field("2026")
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
        out_path = RESULTS_DIR / f"gam_lambda_scan_2026{suffix}.npz"
        np.savez(out_path, results=np.array(results, dtype=object),
                 lambda_grid=np.array(LAMBDA_GRID), temperatures=temperatures,
                 nodes=np.array(nodes), empirical=empirical, N=N,
                 n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
