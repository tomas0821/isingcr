#!/usr/bin/env python3
"""Paired spatial-block test (99,999 draws, canton blocks) of the residualized
GAM field at a chosen lambda/T against geography-only (T=2.605), plus a
head-to-head test against the raw GAM field at lambda=1 (saved spins)."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.observables import spatial_block_permutation_test_paired, alignment_fraction
from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks
from run_gam_residual_field import build_residual_field
N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED, T_GEO, N_PERM = 20000, 20000, 16, 12, 7, 2.605, 99_999
P = Path(__file__).resolve().parent.parent / "data" / "processed"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--lam", type=float, required=True); ap.add_argument("--t", type=float, required=True); a = ap.parse_args()
    J, h, nodes, emp, _ = build_residual_field(verbose=False)
    N = len(nodes); blocks = canton_blocks(nodes)
    sa = best_t_final_spins_aligned(J, np.zeros(N), T_GEO, emp, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    sb = best_t_final_spins_aligned(J, a.lam * h, a.t, emp, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    ps = np.array([spatial_block_permutation_test_paired(x, y, emp, blocks, n_permutations=N_PERM, rng=np.random.default_rng(i))["p_value"] for i, (x, y) in enumerate(zip(sa, sb))])
    print(f"resid lam={a.lam} T={a.t}: median align geo={np.median([np.mean(s==emp) for s in sa]):.4%} resid={np.median([np.mean(s==emp) for s in sb]):.4%}")
    print("per-seed p:", np.array2string(ps, precision=5)); med = float(np.median(ps))
    print(f"median p={med:.5f} sig {int((ps<0.05).sum())}/{N_SEEDS} x32={min(1,32*med):.4f} x32x8={min(1,256*med):.4f}")
    gam = np.load(P / "gam_lambda_scan_2026_lam3.npz", allow_pickle=True)["results"][0]["best_final_spins"]
    gam = [s if alignment_fraction(s, emp) >= 0.5 else -s for s in gam]
    ph = np.array([spatial_block_permutation_test_paired(sb[i], gam[i], emp, blocks, n_permutations=N_PERM, rng=np.random.default_rng(i))["p_value"] for i in range(N_SEEDS)])
    d = [np.mean(sb[i]==emp) - np.mean(gam[i]==emp) for i in range(N_SEEDS)]
    print(f"resid vs raw GAM(lam=1): median diff {100*np.median(d):+.2f} pts, GAM ahead in {int((np.array(d)<0).sum())}/16 seeds, median p={np.median(ph):.4f}, sig {int((ph<0.05).sum())}/16")
    np.savez(P / f"resid_paired_test_lam{a.lam:g}_2026.npz", ps=ps, ps_vs_gam=ph, lam=a.lam, T=a.t)

if __name__ == "__main__":
    main()
