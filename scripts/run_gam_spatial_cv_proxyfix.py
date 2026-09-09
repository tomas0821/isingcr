#!/usr/bin/env python3
"""Does the leave-one-province-out failure in Alajuela come from the
canton-level GAM proxy? Re-run run_gam_spatial_cv.py's exact procedure
(fixed T=1.008, 16 seeds, sign resolved on the training folds only) with
the GAM field modified so that the cantons the main text flags as most
likely over-included by the canton-level proxy are set to periphery (-1):

  variant A: Alajuela Central only (14 distritos; 93% in-sample error)
  variant B: all four flagged cantons (Mora, Alajuela Central, Aserri,
             Paraiso; 34 distritos)

Reports per-province held-out accuracy and the in-sample full-map
alignment for each variant next to the unmodified baseline, so the
question "is Alajuela's failure a labeling artifact?" gets a direct answer.
Cost: 3 x ~3.5 min locally.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.observables import alignment_fraction, mcnemar_test
from run_3d_scan import FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
from run_gam_field import build_graph_and_gam_field, canton_of
from run_gam_spatial_cv import BEST_T_2026, N_JOBS, held_out_fold
from run_spatial_block_sensitivity import best_t_final_spins, province_blocks

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
VARIANTS = {
    "baseline (canton proxy as published)": [],
    "A: Alajuela Central -> periphery": ["ALAJUELA|CENTRAL"],
    "B: all four flagged cantons -> periphery": ["ALAJUELA|CENTRAL", "SAN JOSE|MORA",
                                                 "SAN JOSE|ASERRI", "CARTAGO|PARAISO"],
}


def main():
    J, h_gam0, nodes, empirical = build_graph_and_gam_field("2026")
    blocks = province_blocks(nodes)
    provinces = sorted(np.unique(blocks))
    cantons = np.array([canton_of(n) for n in nodes])
    out = {}
    for label, flip in VARIANTS.items():
        h = h_gam0.copy()
        mask = np.isin(cantons, flip)
        h[mask] = -1.0
        print(f"\n=== {label}: {int(mask.sum())} distritos flipped, GAM count {int((h > 0).sum())} ===")
        t0 = time.time()
        spins = best_t_final_spins(J, h, BEST_T_2026, n_equil=FULL_N_EQUIL, n_sweeps=FULL_N_SWEEPS,
                                   n_seeds=FULL_N_SEEDS, n_jobs=N_JOBS, seed=FULL_SEED)
        full = np.median([max(m, 1 - m) for m in (alignment_fraction(s, empirical) for s in spins)])
        print(f"  in-sample full-map alignment (median): {full:.4%}   ({time.time()-t0:.0f}s)")
        rows = {}
        for prov in provinces:
            tm = blocks == prov
            maj = 1 if np.mean(empirical[tm] == 1) > 0.5 else -1
            base = float(np.mean(empirical[tm] == maj))
            per = held_out_fold(spins, empirical, blocks, prov)
            acc = float(np.median([r["test_acc"] for r in per]))
            p = float(np.median([mcnemar_test(r["spins_aligned"][tm], np.full(tm.sum(), maj),
                                              empirical[tm])["exact_pvalue"] for r in per]))
            rows[prov] = (base, acc, p)
            print(f"  {prov:11s} baseline={base:.1%}  held-out={acc:.1%}  gap={100*(acc-base):+.1f}  McNemar p={p:.4f}")
        out[label] = {"full_map": full, "rows": rows, "n_flipped": int(mask.sum())}
    np.savez(RESULTS_DIR / "gam_spatial_cv_proxyfix_2026.npz", results=np.array([out], dtype=object))
    print(f"\nwritten {RESULTS_DIR / 'gam_spatial_cv_proxyfix_2026.npz'}")


if __name__ == "__main__":
    main()
