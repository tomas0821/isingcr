#!/usr/bin/env python3
"""Paired spatial-block tests (10^6 sign-flip draws, canton blocks) for the
true-boundary GAM field at a given variant/lambda/T: (i) against geography-only
(T=2.605), (ii) head to head against the canton-proxy GAM field at unit weight
(T=1.008), all re-simulated with the standard budget and the same seeds."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.observables import spatial_block_permutation_test_paired
from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks
from run_gam_true_field import build_true_field
from run_gam_field import GAM_CANTONS, canton_of
N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED, T_GEO, T_PROXY, N_PERM = 20000, 20000, 16, 12, 7, 2.605, 1.0080645161290325, 999_999
P = Path(__file__).resolve().parent.parent / "data" / "processed"


def summarize(ps, label):
    b = np.round(ps * N_PERM); p1 = (b + 1) / (N_PERM + 1)
    print(f"{label}: median p={np.median(ps):.2e} (plain) {np.median(p1):.2e} ((b+1)/(m+1)); zeros={int((ps==0).sum())}; sig {int((ps<0.05).sum())}/{len(ps)}; x32={32*np.median(ps):.2e}; x32x8={256*np.median(ps):.2e}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--variant", default="majority"); ap.add_argument("--lam", type=float, default=1.0); ap.add_argument("--t", type=float, required=True); a = ap.parse_args()
    J, h, nodes, emp, frac = build_true_field(a.variant, verbose=False)
    N = len(nodes); blocks = canton_blocks(nodes)
    hp = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
    sa = best_t_final_spins_aligned(J, np.zeros(N), T_GEO, emp, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    sb = best_t_final_spins_aligned(J, a.lam * h, a.t, emp, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    sp = best_t_final_spins_aligned(J, hp, T_PROXY, emp, N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    al = lambda S: np.median([np.mean(s == emp) for s in S])
    print(f"variant={a.variant} lam={a.lam} T={a.t}: median alignment geo={al(sa):.4%} true={al(sb):.4%} proxy={al(sp):.4%}")
    ps = np.array([spatial_block_permutation_test_paired(sa[i], sb[i], emp, blocks, n_permutations=N_PERM, rng=np.random.default_rng(i))["p_value"] for i in range(N_SEEDS)])
    summarize(ps, "true vs geography-only")
    ph = np.array([spatial_block_permutation_test_paired(sp[i], sb[i], emp, blocks, n_permutations=N_PERM, rng=np.random.default_rng(i))["p_value"] for i in range(N_SEEDS)])
    d = np.array([np.mean(sb[i] == emp) - np.mean(sp[i] == emp) for i in range(N_SEEDS)])
    print(f"true vs proxy: median diff {100*np.median(d):+.2f} pts, true ahead in {int((d>0).sum())}/16 seeds, median p={np.median(ph):.4f}, sig {int((ph<0.05).sum())}/16")
    np.savez(P / f"true_gam_paired_test_{a.variant}_lam{a.lam:g}_2026.npz", ps=ps, ps_vs_proxy=ph, diff_vs_proxy=d, lam=a.lam, T=a.t, variant=a.variant,
             spins_geo=np.array(sa), spins_true=np.array(sb), spins_proxy=np.array(sp))
    print("written")


if __name__ == "__main__":
    main()
