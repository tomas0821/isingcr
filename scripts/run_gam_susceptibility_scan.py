#!/usr/bin/env python3
"""Susceptibility/specific-heat scan with the GAM field switched on --
characterizing the crossover between a geography-dominated regime and a
GAM-field-dominated regime, rather than just reporting one best-fit T.

Motivation: run_gam_field.py found the GAM field's best classification
accuracy at T=1.008, well below geography-only's T=2.605 (see
00_Master_Notebook.md). That single-point comparison hints at a real
crossover but doesn't characterize it -- this scan does, by computing
susceptibility chi(T) = N*Var(m)/T and specific heat C(T) = Var(E)/(N*T^2)
across the full temperature range with h=GAM fixed, using
isingcr.simulation.observables' existing (already-tested) chi/C
implementations directly on pooled_temperature_scan's raw energy/
magnetization series -- run_gam_field.py never extracted these, only the
per-T classification accuracy.

Same skepticism as every other susceptibility-adjacent analysis in this
project (CLAUDE.md gotcha #7): a real crossover/critical signature is an
INTERIOR bump in chi(T), not a monotonic blow-up toward the low-T scan
edge (which is the known between-chain-metastable-disagreement artifact
that has bitten this project twice already). Reports which case this is,
explicitly, rather than assuming a peak means something.

Same field, budget, and T-grid as run_gam_field.py for direct comparability.
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
from isingcr.simulation.observables import specific_heat, susceptibility, symmetric_alignment_fraction
from run_3d_scan import (
    FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, FULL_T_RANGE,
    MAX_CORES_PER_TASK, MS_PER_SWEEP_DISTRITO,
    VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED, VALIDATE_TEMPERATURES,
)
from run_gam_field import build_graph_and_gam_field

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def run_scan(J, h, empirical, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs):
    N = J.shape[0]
    pooled = pooled_temperature_scan(J, h, temperatures, n_seeds=n_seeds,
                                      n_equil=n_equil, n_sweeps=n_sweeps,
                                      dynamics="glauber", seed=seed, n_jobs=n_jobs)
    chi, C, accuracy = [], [], []
    for i, T in enumerate(temperatures):
        chi.append(susceptibility(pooled[i]["magnetization"], T, N))
        C.append(specific_heat(pooled[i]["energy"], T, N))
        accuracy.append(float(np.mean([symmetric_alignment_fraction(s, empirical)
                                        for s in pooled[i]["final_spins_per_seed"]])))
    return np.array(chi), np.array(C), np.array(accuracy)


def estimate_resources(n_temperatures, n_seeds, n_equil, n_sweeps):
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)
    t_batches = -(-n_temperatures // cores_per_task)
    wall_seconds = n_seeds * t_batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    print("=== Resource estimate (grounded in 2026-08-16 cluster benchmark) ===")
    print(f"  1 field x {n_temperatures} T x {n_seeds} seeds")
    print(f"  Cores per task: {cores_per_task}")
    print(f"  Estimated wall time: {wall_seconds:.1f}s ({wall_seconds / 60:.1f} min)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", choices=["2026", "2022"], default="2026")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--n-temperatures", type=int, default=32)
    args = parser.parse_args()

    if args.estimate and not args.validate:
        estimate_resources(args.n_temperatures, FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    print(f"Building real {args.year} distrito network + GAM field...")
    t0 = time.time()
    J, h_gam, nodes, empirical = build_graph_and_gam_field(args.year)
    N = J.shape[0]
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    if args.validate:
        temperatures = VALIDATE_TEMPERATURES
        n_equil, n_sweeps, n_seeds, seed = VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        print(f"\n--validate mode: {len(temperatures)} T, {n_equil}+{n_sweeps} sweeps, {n_seeds} seed.")
    else:
        temperatures = np.linspace(*FULL_T_RANGE, args.n_temperatures)
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        estimate_resources(args.n_temperatures, n_seeds, n_equil, n_sweeps)

    t_start = time.time()
    chi, C, accuracy = run_scan(J, h_gam, empirical, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs)
    elapsed = time.time() - t_start

    peak_idx = int(np.argmax(chi))
    is_interior = 0 < peak_idx < len(temperatures) - 1
    print(f"\nyear={args.year}: chi peaks at T={temperatures[peak_idx]:.3f} "
          f"(chi={chi[peak_idx]:.2f}), {'INTERIOR -- plausibly real' if is_interior else 'AT SCAN EDGE -- likely the known between-chain-disagreement artifact, not a real crossover'}")
    print(f"Scan took {elapsed:.1f}s")
    for i, T in enumerate(temperatures):
        print(f"  T={T:.3f}  chi={chi[i]:8.2f}  C={C[i]:8.2f}  accuracy={accuracy[i]:.3%}")

    if not args.validate:
        out_path = RESULTS_DIR / f"gam_susceptibility_scan_{args.year}.npz"
        np.savez(out_path, temperatures=temperatures, chi=chi, C=C, accuracy=accuracy, N=N,
                 n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
