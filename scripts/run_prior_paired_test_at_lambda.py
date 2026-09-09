#!/usr/bin/env python3
"""Paired spatial-block permutation test of the political-continuity field
at a chosen weight lambda_soc (and its best-of-grid T from
run_prior_lambda_scan.py) against geography-only (T=2.605), on the 2026
N=488 distrito network. Same arms/budget/seeds/blocks convention as
run_gam_paired_test_highres.py (16 seeds, 20000+20000 sweeps, canton
blocks, 99,999 sign-flip draws). Usage:
    python scripts/run_prior_paired_test_at_lambda.py --lam 6 --t 1.2
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.observables import spatial_block_permutation_test_paired
from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks
from run_prior_margin_field import build_graph_and_prior_field

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 12, 7
T_GEO = 2.605


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--lam", type=float, required=True); ap.add_argument("--t", type=float, required=True); ap.add_argument("--n-perm", type=int, default=99_999)
    a = ap.parse_args(); N_PERM = a.n_perm
    J, h, nodes, empirical, _ = build_graph_and_prior_field()
    N = len(nodes)
    spins_a = best_t_final_spins_aligned(J, np.zeros(N), T_GEO, empirical, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    spins_b = best_t_final_spins_aligned(J, a.lam * h, a.t, empirical, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    blocks = canton_blocks(nodes)
    ps = np.array([spatial_block_permutation_test_paired(sa, sb, empirical, blocks, n_permutations=N_PERM,
                                                         rng=np.random.default_rng(i))["p_value"]
                   for i, (sa, sb) in enumerate(zip(spins_a, spins_b))])
    acc_a = np.median([np.mean(s == empirical) for s in spins_a]); acc_b = np.median([np.mean(s == empirical) for s in spins_b])
    print(f"lambda={a.lam} T={a.t}: median alignment geo={acc_a:.4%} field={acc_b:.4%}")
    print("per-seed p:", np.array2string(ps, precision=5))
    med = float(np.median(ps))
    b = np.round(ps * N_PERM); p1 = (b + 1) / (N_PERM + 1); med1 = float(np.median(p1))
    print(f"median p={med:.2e} (plain) {med1:.2e} ((b+1)/(m+1))  zeros={int((ps==0).sum())}  sig(<0.05) {int((ps<0.05).sum())}/{N_SEEDS}  x32={32*med:.2e}/{32*med1:.2e} x32x8={256*med:.2e}/{256*med1:.2e} x32x8x13={3328*med:.4f}/{3328*med1:.4f}")
    out = Path(__file__).resolve().parent.parent / "data" / "processed" / (f"prior_paired_test_lam{a.lam:g}_2026.npz" if N_PERM == 99_999 else f"prior_paired_test_lam{a.lam:g}_2026_perm{N_PERM}.npz")
    np.savez(out, ps=ps, lam=a.lam, T=a.t, n_permutations=N_PERM, align_geo=acc_a, align_field=acc_b, spins_geo=np.array(spins_a), spins_field=np.array(spins_b))
    print("written", out)


if __name__ == "__main__":
    main()
