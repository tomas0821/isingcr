#!/usr/bin/env python3
"""Counterfactual temperature-sensitivity sweep: fix the real 2026 network
and the real GAM field, then ask how much the equilibrium map would have
looked different if collective conformity pressure (T) had been higher or
lower than what best matches reality (T=1.008) -- a question a fitted
regression coefficient cannot answer, since there's no "turn up the noise
and re-solve" operation on a regression. Prompted directly by the fair
challenge that most of this session's covariate work could be argued nearly
as well from raw vote margins; this is the second of the genuinely
model-native follow-ups (after the multistability check above).

Reuses build_graph_and_gam_field/pooled_temperature_scan exactly as
run_gam_field.py/run_gam_susceptibility_scan.py do, but captures per-node
majority-vote maps at each T (the earlier scans discarded spins, keeping
only aggregate accuracy) so divergence between temperatures can be measured
directly, not just each T's accuracy against the empirical map.

A curated 13-point T subset, not the full 32-point grid (cost-saving: this
question doesn't need every point, just enough resolution to see the shape
of the sensitivity curve around the best-fit T=1.008).
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
from isingcr.simulation.observables import symmetric_alignment_fraction
from run_3d_scan import FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, MAX_CORES_PER_TASK, MS_PER_SWEEP_DISTRITO
from run_gam_field import build_graph_and_gam_field

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
SWEEP_TEMPERATURES = np.array([0.05, 0.369, 0.689, 0.848, 1.008, 1.327, 1.647,
                                1.966, 2.285, 2.605, 2.924, 3.563, 5.0])
REFERENCE_T = 1.008  # GAM field's own best-T (run_gam_field.py)


def majority_map(spins_per_seed):
    stacked = np.array(spins_per_seed)  # (n_seeds, N)
    return np.sign(stacked.sum(axis=0)).astype(np.int8)  # ties -> 0, rare with 16 seeds


def estimate_resources(n_temperatures, n_seeds, n_equil, n_sweeps):
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)
    t_batches = -(-n_temperatures // cores_per_task)
    wall_seconds = n_seeds * t_batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    print(f"=== Resource estimate: {n_temperatures} T x {n_seeds} seeds, "
          f"{cores_per_task} cores, ~{wall_seconds / 60:.1f} min ===")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    args = parser.parse_args()

    if args.estimate and not args.validate:
        estimate_resources(len(SWEEP_TEMPERATURES), FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    print("Building real 2026 distrito network + GAM field...")
    t0 = time.time()
    J, h_gam, nodes, empirical = build_graph_and_gam_field("2026")
    N = J.shape[0]
    print(f"  N={N} distritos, built in {time.time() - t0:.1f}s")

    if args.validate:
        temperatures = np.array([0.5, 2.0])
        n_equil, n_sweeps, n_seeds, seed = 50, 50, 1, 7
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        print(f"\n--validate mode: {len(temperatures)} T, {n_equil}+{n_sweeps} sweeps, {n_seeds} seed.")
    else:
        temperatures = SWEEP_TEMPERATURES
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        estimate_resources(len(temperatures), n_seeds, n_equil, n_sweeps)

    t_start = time.time()
    pooled = pooled_temperature_scan(J, h_gam, temperatures, n_seeds=n_seeds,
                                      n_equil=n_equil, n_sweeps=n_sweeps,
                                      dynamics="glauber", seed=seed, n_jobs=n_jobs)
    elapsed = time.time() - t_start
    print(f"Scan took {elapsed:.1f}s")

    maps = [majority_map(p["final_spins_per_seed"]) for p in pooled]
    accuracy = [float(np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
                for p in pooled]

    ref_idx = int(np.argmin(np.abs(temperatures - REFERENCE_T)))
    ref_map = maps[ref_idx]
    print(f"\nReference T={temperatures[ref_idx]:.3f} (closest to best-fit {REFERENCE_T})")
    print(f"{'T':>8}{'accuracy':>12}{'frac_flipped_vs_ref':>22}")
    frac_flipped = []
    for i, T in enumerate(temperatures):
        # symmetric_alignment_fraction handles the Z2 sign ambiguity between independent maps
        flipped = 1.0 - symmetric_alignment_fraction(maps[i], ref_map)
        frac_flipped.append(flipped)
        print(f"{T:>8.3f}{accuracy[i]:>12.3%}{flipped:>22.3%}")

    if not args.validate:
        out = RESULTS_DIR / "gam_counterfactual_sweep_2026.npz"
        np.savez(out, temperatures=temperatures, accuracy=np.array(accuracy),
                 frac_flipped_vs_ref=np.array(frac_flipped), reference_T=temperatures[ref_idx],
                 maps=np.array(maps), nodes=nodes)
        print(f"\nRaw results written to {out}")


if __name__ == "__main__":
    main()
