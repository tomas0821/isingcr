#!/usr/bin/env python3
"""Consolidate the 25 per-grid-point scan_3d_pol<i>_soc<j>.npz files (from
scripts/run_3d_scan.py's cluster run, 2026-08-20, real MIDEPLAN IDS 2023 +
real 2026 vote margins, N=488 distrito network) into one summary table and
report the headline pattern: does adding the social-development field
(lambda_soc) improve on political-margin-alone (lambda_pol only), and if so,
by how much and how robustly.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
N_LAMBDA = 5
LAMBDA_MAX = 2.0
LAMBDA_VALUES = np.linspace(0.0, LAMBDA_MAX, N_LAMBDA)


def load_grid(prefix="scan_3d"):
    grid = {}
    for i in range(N_LAMBDA):
        for j in range(N_LAMBDA):
            path = RESULTS_DIR / f"{prefix}_pol{i}_soc{j}.npz"
            d = np.load(path, allow_pickle=True)
            r = d["results"][0]
            grid[(i, j)] = r
    return grid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", type=str, default="scan_3d")
    args = parser.parse_args()
    grid = load_grid(args.prefix)

    print(f"=== [{args.prefix}] Best-fit accuracy grid (rows=lambda_pol, cols=lambda_soc) ===")
    header = "lam_pol\\soc " + "".join(f"{v:>9.2f}" for v in LAMBDA_VALUES)
    print(header)
    for i in range(N_LAMBDA):
        row = f"{LAMBDA_VALUES[i]:>11.2f} "
        for j in range(N_LAMBDA):
            row += f"{grid[(i, j)]['best_accuracy']:>9.2%}"
        print(row)

    print("\n=== McNemar median p grid (rows=lambda_pol, cols=lambda_soc) ===")
    print(header)
    for i in range(N_LAMBDA):
        row = f"{LAMBDA_VALUES[i]:>11.2f} "
        for j in range(N_LAMBDA):
            row += f"{grid[(i, j)]['mcnemar_median_p']:>9.4f}"
        print(row)

    print("\n=== Best-fit T grid (rows=lambda_pol, cols=lambda_soc) ===")
    print(header)
    for i in range(N_LAMBDA):
        row = f"{LAMBDA_VALUES[i]:>11.2f} "
        for j in range(N_LAMBDA):
            row += f"{grid[(i, j)]['best_T']:>9.3f}"
        print(row)

    # Headline comparisons
    pure_pol = grid[(N_LAMBDA - 1, 0)]      # lambda_pol=2.0, lambda_soc=0.0
    pure_soc = grid[(0, N_LAMBDA - 1)]       # lambda_pol=0.0, lambda_soc=2.0
    geography_only = grid[(0, 0)]            # lambda_pol=0.0, lambda_soc=0.0
    best_overall = max(grid.values(), key=lambda r: r["best_accuracy"])

    print("\n=== Headline comparisons ===")
    print(f"Geography only (lambda_pol=0, lambda_soc=0): {geography_only['best_accuracy']:.2%} "
          f"(p={geography_only['mcnemar_median_p']:.4f})")
    print(f"Pure political (lambda_pol={pure_pol['lambda_pol']:.1f}, lambda_soc=0): "
          f"{pure_pol['best_accuracy']:.2%} (p={pure_pol['mcnemar_median_p']:.4f})")
    print(f"Pure social-dev (lambda_pol=0, lambda_soc={pure_soc['lambda_soc']:.1f}): "
          f"{pure_soc['best_accuracy']:.2%} (p={pure_soc['mcnemar_median_p']:.4f})")
    print(f"Best combination overall: lambda_pol={best_overall['lambda_pol']:.2f}, "
          f"lambda_soc={best_overall['lambda_soc']:.2f} -> {best_overall['best_accuracy']:.2%} "
          f"(p={best_overall['mcnemar_median_p']:.4f})")

    # Does adding social-dev on top of the best political weight help?
    best_pol_idx = max(range(N_LAMBDA), key=lambda i: grid[(i, 0)]["best_accuracy"])
    print(f"\nBest lambda_pol alone (lambda_soc=0): lambda_pol={LAMBDA_VALUES[best_pol_idx]:.2f} "
          f"-> {grid[(best_pol_idx, 0)]['best_accuracy']:.2%}")
    row_best = max(range(N_LAMBDA), key=lambda j: grid[(best_pol_idx, j)]["best_accuracy"])
    print(f"Adding social-dev on top (same lambda_pol row): best lambda_soc="
          f"{LAMBDA_VALUES[row_best]:.2f} -> {grid[(best_pol_idx, row_best)]['best_accuracy']:.2%} "
          f"({grid[(best_pol_idx, row_best)]['best_accuracy'] - grid[(best_pol_idx, 0)]['best_accuracy']:+.2%})")


if __name__ == "__main__":
    main()
