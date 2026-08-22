#!/usr/bin/env python3
"""Domain-wall analysis for the GAM field result (run_gam_field.py): which
specific distritos does geography+GAM get wrong, and are those errors
concentrated at the boundary between GAM and periphery -- the interface
between the model's two "domains" -- rather than scattered randomly?

This is the kind of question only a spatially-coupled model can naturally
frame: a distrito adjacent to at least one distrito of the OPPOSITE GAM
status is caught between two competing pulls (agree with your GAM-status
field vs. agree with a differently-labeled neighbor via J), while an
"interior" distrito (all neighbors share its own GAM status) has no such
tension. If the model's physics is doing real work, boundary distritos
should show a measurably higher error rate than interior ones.

Reuses the exact spin configurations each year's GAM paired significance
test already established are the right ones to look at (that year's GAM
field's own best-T, 16 seeds, geography+GAM) -- recomputed here since
run_gam_field.py's saved .npz only has aggregate accuracy, not per-node
spins (same limitation as every other single-point scan in this project).

--year selects 2026 (original run) or 2022 (the natural follow-up: does the
same poor-core-votes-like-periphery pattern hold where the overall GAM
signal was much weaker, or is it 2026-specific like everything else in
this covariate search?).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_direct_paired_test import best_t_final_spins_aligned
from run_gam_field import build_graph_and_gam_field

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 12, 7
GAM_BEST_T = {"2026": 1.008, "2022": 1.008}  # both years' gam_field_<year>.npz best_T
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", choices=["2026", "2022"], default="2026")
    args = parser.parse_args()
    year = args.year
    best_t = GAM_BEST_T[year]

    J, h_gam, nodes, empirical = build_graph_and_gam_field(year)
    N = len(nodes)
    is_gam = h_gam > 0

    print(f"Running {N_SEEDS} seeds at {year}'s GAM field best-T={best_t}...")
    spins = best_t_final_spins_aligned(J, h_gam, best_t, empirical,
                                        N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED)
    spins = np.array(spins)  # (n_seeds, N)
    error_rate = (spins != empirical[None, :]).mean(axis=0)  # per-node, fraction of seeds wrong

    # Boundary flag: any J-neighbor with a different GAM status.
    J_csr = J.tocsr()
    is_boundary = np.zeros(N, dtype=bool)
    for i in range(N):
        neighbors = J_csr.indices[J_csr.indptr[i]:J_csr.indptr[i + 1]]
        if len(neighbors) and np.any(is_gam[neighbors] != is_gam[i]):
            is_boundary[i] = True

    df = pd.DataFrame({
        "node": nodes, "is_gam": is_gam, "is_boundary": is_boundary, "error_rate": error_rate,
    })

    print(f"\n=== Boundary vs. interior error rate ===")
    for boundary_val, label in [(True, "boundary (has an opposite-status neighbor)"),
                                 (False, "interior (all neighbors same status)")]:
        sub = df[df["is_boundary"] == boundary_val]
        print(f"  {label}: n={len(sub)}, mean error rate={sub['error_rate'].mean():.3f}, "
              f"median={sub['error_rate'].median():.3f}")

    print(f"\n=== Four-way breakdown (GAM status x boundary status) ===")
    for gam_val in [True, False]:
        for boundary_val in [True, False]:
            sub = df[(df["is_gam"] == gam_val) & (df["is_boundary"] == boundary_val)]
            if len(sub):
                print(f"  GAM={gam_val}, boundary={boundary_val}: n={len(sub)}, "
                      f"mean error rate={sub['error_rate'].mean():.3f}")

    print(f"\n=== Top 20 highest-error distritos ===")
    top = df.sort_values("error_rate", ascending=False).head(20)
    for _, row in top.iterrows():
        print(f"  {row['node']:45s} gam={row['is_gam']!s:5s} boundary={row['is_boundary']!s:5s} "
              f"error_rate={row['error_rate']:.3f}")

    out = RESULTS_DIR / f"gam_domain_wall_analysis_{year}.npz"
    np.savez(out, nodes=nodes, is_gam=is_gam, is_boundary=is_boundary, error_rate=error_rate)
    df.to_csv(RESULTS_DIR / f"gam_domain_wall_analysis_{year}.csv", index=False)
    print(f"\nRaw results written to {out} and .csv")


if __name__ == "__main__":
    main()
