#!/usr/bin/env python3
"""Direct paired test: does adding the MIDEPLAN social-development field
(h_soc, at lambda_pol=0) actually predict the real distrito map significantly
better than pure geography (h=0), compared HEAD-TO-HEAD -- not each arm
separately against the trivial majority-class baseline (same rationale as
run_direct_paired_test.py; reuses its spatial_block_permutation_test_paired
machinery). Answers: is the 2026 grid's lambda_pol=0 row peak (67.64% at
soc=0 -> 74.42% at soc=1.5, +6.78pp) statistically distinguishable from the
2022 row's much smaller peak (62.46% -> 63.59%, +1.13pp)?

Runs each arm only at its already-identified best-fit T from the 5x5 grid
(scripts/run_3d_scan.py / run_3d_scan_2022.py), no rescan needed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.two_field_energy import combine_fields
from isingcr.simulation.observables import spatial_block_permutation_test_paired
from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks, paired_test

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 12, 7


def run_year(label, build_fn, t_a, lambda_soc_b, t_b):
    print(f"\n=== {label}: h=0 (T={t_a}) vs. h=lambda_soc*h_soc, lambda_soc={lambda_soc_b} (T={t_b}) ===")
    J, h_pol, h_soc, nodes, empirical = build_fn()
    h_a = combine_fields(h_pol, h_soc, 0.0, 0.0)
    h_b = combine_fields(h_pol, h_soc, 0.0, lambda_soc_b)
    spins_a = best_t_final_spins_aligned(J, h_a, t_a, empirical, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    spins_b = best_t_final_spins_aligned(J, h_b, t_b, empirical, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    blocks = canton_blocks(nodes)
    return paired_test(label, spins_a, spins_b, empirical, blocks, N_SEEDS)


def main():
    from run_3d_scan import build_distrito_graph_and_fields as build_2026
    from run_3d_scan_2022 import build_distrito_graph_and_fields as build_2022

    r2026 = run_year("2026 (lambda_soc=1.5 row peak)", build_2026, 2.605, 1.5, 1.647)
    r2022 = run_year("2022 (lambda_soc=0.5 row peak)", build_2022, 3.563, 0.5, 2.924)

    out = Path(__file__).resolve().parent.parent / "data" / "processed" / "soc_paired_test.npz"
    np.savez(out,
             p2026_ps=r2026["ps"], p2026_median_p=r2026["median_p"], p2026_frac_sig=r2026["frac_sig"],
             p2022_ps=r2022["ps"], p2022_median_p=r2022["median_p"], p2022_frac_sig=r2022["frac_sig"])
    print(f"\nRaw results written to {out}")


if __name__ == "__main__":
    main()
