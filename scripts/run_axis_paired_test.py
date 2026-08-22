#!/usr/bin/env python3
"""Direct paired test: for each MIDEPLAN IDS axis (run_mideplan_axis_screen.py),
does it predict the real distrito map significantly better than pure geography
(h=0), head-to-head -- not against the trivial majority-class baseline. Same
rationale and machinery as run_soc_paired_test.py (which did this for the
composite IDS score); this generalizes it to the five sub-dimensions.

Reuses the geography-only arm (h=0) at each year's already-known best-T
(T=2.605 for 2026, T=3.563 for 2022 -- from the lambda_pol=0/lambda_soc=0
grid point, scan_3d_pol0_soc0.npz / scan_3d_2022_pol0_soc0.npz) computed
ONCE and shared across all 5 axis comparisons, rather than recomputed per
axis.

Requires scripts/run_mideplan_axis_screen.py's cluster output
(data/processed/mideplan_axis_<year>_<axis>.npz) to already exist for every
axis/year being tested -- reads each axis's best_T from there rather than
hardcoding it.

Multiple-comparison note: testing 5 axes is 5 hypothesis tests per year.
Report applies Bonferroni (alpha=0.05/5=0.01 per axis) alongside the raw
per-axis p-value -- do not call a single axis "significant" off the raw 0.05
threshold alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.two_field_energy import combine_fields
from isingcr.ingestion.mideplan_ids import ids_zscore_by_code, load_mideplan_ids_axes
from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks, paired_test
from run_mideplan_axis_screen import AXES, BUILDERS, MIDEPLAN_IDS_CSV

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 12, 7
GEOGRAPHY_ONLY_BEST_T = {"2026": 2.605, "2022": 3.563}  # from the lambda_pol=0/lambda_soc=0 grid point
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
BONFERRONI_ALPHA = 0.05 / len(AXES)


def run_year(year):
    print(f"\n{'=' * 70}\nYear {year}\n{'=' * 70}")
    build_fn = BUILDERS[year]
    J, h_pol, _composite_h_soc, nodes, empirical = build_fn()
    blocks = canton_blocks(nodes)

    t_a = GEOGRAPHY_ONLY_BEST_T[year]
    h_zero = np.zeros_like(h_pol)
    print(f"Arm A (geography only, h=0, T={t_a}) -- computed once, reused across all axes")
    spins_a = best_t_final_spins_aligned(J, h_zero, t_a, empirical, N_EQUIL, N_SWEEPS,
                                          N_SEEDS, N_JOBS, SEED)

    axes_df = load_mideplan_ids_axes(MIDEPLAN_IDS_CSV)
    results = {}
    for axis in AXES:
        npz_path = RESULTS_DIR / f"mideplan_axis_{year}_{axis}.npz"
        if not npz_path.exists():
            print(f"  [skip] {axis}: {npz_path.name} not found -- run "
                  f"run_mideplan_axis_screen.py --year {year} --axis-index "
                  f"{AXES.index(axis)} first (or the cluster array job).")
            continue
        d = np.load(npz_path, allow_pickle=True)
        r = d["result"].item()
        t_b = r["best_T"]
        lambda_axis = float(d["lambda_axis"])

        h_axis, _ = ids_zscore_by_code(axes_df, nodes, ids_col=f"{axis}_raw")
        h_b = combine_fields(h_pol, h_axis, 0.0, lambda_axis)
        spins_b = best_t_final_spins_aligned(J, h_b, t_b, empirical, N_EQUIL, N_SWEEPS,
                                              N_SEEDS, N_JOBS, SEED)

        label = f"{year}/{axis} (h=0 T={t_a} vs. h={axis} T={t_b:.3f})"
        result = paired_test(label, spins_a, spins_b, empirical, blocks, N_SEEDS)
        sig_bonf = result["median_p"] < BONFERRONI_ALPHA
        print(f"  Bonferroni (alpha={BONFERRONI_ALPHA:.3f}): "
              f"{'SIGNIFICANT' if sig_bonf else 'not significant'} on median p")
        results[axis] = {**result, "grid_best_accuracy": r["best_accuracy"], "sig_bonferroni": sig_bonf}
    return results


def main():
    all_results = {year: run_year(year) for year in ["2026", "2022"]}

    print(f"\n{'=' * 70}\nSummary (Bonferroni alpha={BONFERRONI_ALPHA:.3f} per axis)\n{'=' * 70}")
    for year, results in all_results.items():
        print(f"\n{year}:")
        for axis, r in results.items():
            flag = "***" if r["sig_bonferroni"] else ("*" if r["median_p"] < 0.05 else "")
            print(f"  {axis:12s} grid_acc={r['grid_best_accuracy']:.2%}  "
                  f"median_p={r['median_p']:.4f}  sig_pairs={int(round(r['frac_sig'] * N_SEEDS))}/{N_SEEDS}  {flag}")

    out = RESULTS_DIR / "axis_paired_test.npz"
    np.savez(out, **{
        f"{year}_{axis}_ps": r["ps"] for year, results in all_results.items() for axis, r in results.items()
    })
    print(f"\nRaw results written to {out}")


if __name__ == "__main__":
    main()
