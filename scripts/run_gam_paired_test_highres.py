#!/usr/bin/env python3
"""Re-run the 2026 GAM-vs-geography-only paired spatial-block permutation
test with 99,999 sign-flip draws instead of 999, because at 999 draws eight
of the 16 seed pairs recorded zero exceedances (p reported as 0.000) and the
median p=0.0005 was the midpoint of 0.000 and 0.001, i.e. below the test's
resolution. Same arms, temperatures, budget, seeds and canton blocks as the
original run (geography-only at its best T=2.605, GAM at T=1.008). Reports
both the raw exceedance fraction and the (b+1)/(m+1) convention.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.observables import spatial_block_permutation_test_paired
from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks
from run_gam_field import build_graph_and_gam_field

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 12, 7
T_GEO, T_GAM = 2.605, 1.0080645161290325
N_PERM = 99_999


def main():
    J, h_gam, nodes, empirical = build_graph_and_gam_field("2026")
    N = len(nodes)
    spins_a = best_t_final_spins_aligned(J, np.zeros(N), T_GEO, empirical, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    spins_b = best_t_final_spins_aligned(J, h_gam, T_GAM, empirical, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    blocks = canton_blocks(nodes)
    ps_raw, ps_plus1 = [], []
    for i, (sa, sb) in enumerate(zip(spins_a, spins_b)):
        r = spatial_block_permutation_test_paired(sa, sb, empirical, blocks, n_permutations=N_PERM,
                                                  rng=np.random.default_rng(i))
        b = r["p_value"] * N_PERM
        ps_raw.append(r["p_value"]); ps_plus1.append((b + 1) / (N_PERM + 1))
    ps_raw, ps_plus1 = np.array(ps_raw), np.array(ps_plus1)
    print("per-seed raw p:", np.array2string(ps_raw, precision=6))
    print("per-seed (b+1)/(m+1) p:", np.array2string(ps_plus1, precision=6))
    for name, ps in [("raw", ps_raw), ("plus1", ps_plus1)]:
        med = float(np.median(ps))
        print(f"{name}: median p={med:.6f}  sig(<0.05) {int((ps<0.05).sum())}/{N_SEEDS}  "
              f"x32 Bonferroni={min(1,32*med):.4f}  x32x3={min(1,96*med):.4f}  x32x8={min(1,256*med):.4f}")
    out = Path(__file__).resolve().parent.parent / "data" / "processed" / "gam_paired_test_highres_2026.npz"
    np.savez(out, ps_raw=ps_raw, ps_plus1=ps_plus1, n_permutations=N_PERM)
    print("written", out)


if __name__ == "__main__":
    main()
