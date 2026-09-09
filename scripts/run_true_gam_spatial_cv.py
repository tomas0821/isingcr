#!/usr/bin/env python3
"""Leave-one-province-out check for the true-boundary GAM field (same
protocol as run_gam_spatial_cv.py: fixed T, 16 seeds, global sign resolved on
the training provinces only)."""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.observables import alignment_fraction, mcnemar_test
from run_3d_scan import FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
from run_gam_spatial_cv import N_JOBS, held_out_fold
from run_spatial_block_sensitivity import best_t_final_spins, province_blocks
from run_gam_true_field import build_true_field
P = Path(__file__).resolve().parent.parent / "data" / "processed"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--variant", default="majority"); ap.add_argument("--lam", type=float, default=1.0); ap.add_argument("--t", type=float, required=True); a = ap.parse_args()
    J, h, nodes, empirical, _ = build_true_field(a.variant, verbose=False)
    blocks = province_blocks(nodes); provinces = sorted(np.unique(blocks))
    t0 = time.time()
    spins = best_t_final_spins(J, a.lam * h, a.t, n_equil=FULL_N_EQUIL, n_sweeps=FULL_N_SWEEPS, n_seeds=FULL_N_SEEDS, n_jobs=N_JOBS, seed=FULL_SEED)
    full = np.median([max(m, 1 - m) for m in (alignment_fraction(s, empirical) for s in spins)])
    print(f"variant={a.variant} lam={a.lam} T={a.t}: in-sample full-map alignment (median) {full:.4%} ({time.time()-t0:.0f}s)")
    rows = {}
    for prov in provinces:
        tm = blocks == prov; maj = 1 if np.mean(empirical[tm] == 1) > 0.5 else -1
        base = float(np.mean(empirical[tm] == maj)); per = held_out_fold(spins, empirical, blocks, prov)
        acc = float(np.median([r["test_acc"] for r in per]))
        p = float(np.median([mcnemar_test(r["spins_aligned"][tm], np.full(tm.sum(), maj), empirical[tm])["exact_pvalue"] for r in per]))
        rows[prov] = (base, acc, p); print(f"  {prov:11s} n={int(tm.sum()):3d} baseline={base:.1%} held-out={acc:.1%} gap={100*(acc-base):+.1f} McNemar p={p:.4f}")
    np.savez(P / f"true_gam_spatial_cv_{a.variant}_2026.npz", rows=np.array([rows], dtype=object), full=full, lam=a.lam, T=a.t)


if __name__ == "__main__":
    main()
