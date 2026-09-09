#!/usr/bin/env python3
"""Single-node perturbation / cascade analysis: for a curated set of
candidate distritos, flip that ONE node's GAM field and re-equilibrate the
whole real network, then count how many OTHER distritos' equilibrium spin
changes as a consequence. Answers two related questions from the same runs:
does a local political shift cascade through the real geographic network or
stay contained (a literal domino-effect test only a coupled dynamical
system can run), and which specific places are the most "electorally
load-bearing" in the network (a leverage/centrality measure with no
regression analog).

10 candidates chosen to span every category surfaced by the multistability
check, the counterfactual sweep, and the domain-wall analysis (all above):
genuinely multistable "fault line" nodes (uncertain even at fixed T),
seed-locked-but-temperature-fragile nodes (a distinct kind of fragility),
a locked-but-consistently-WRONG node (Pavas, highest-population GAM
distrito), and locked-correct high-population "core" controls on both the
GAM and periphery sides.

Reuses the T=1.008 reference majority map already computed by
run_gam_counterfactual_sweep.py as the unperturbed baseline (same field, T,
budget, seed) rather than re-running it.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.monte_carlo import temperature_scan
from run_3d_scan import FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
from run_gam_field import build_graph_and_gam_field

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
BEST_T = 1.008
N_JOBS = 12  # local run

CANDIDATES = {
    "SAN JOSE|MORA|TABARCIA": "multistable fault line (top overall, cross-year consistent)",
    "SAN JOSE|ASERRI|MONTERREY": "multistable fault line (cross-year consistent)",
    "SAN JOSE|ACOSTA|PALMICHAL": "multistable fault line (exact 8-8 split in 2022)",
    "CARTAGO|PARAISO|OROSI": "multistable fault line + boundary + temperature-fragile",
    "SAN JOSE|MORA|PIEDRAS NEGRAS": "seed-locked but temperature-fragile (distinct fragility type)",
    "SAN JOSE|CENTRAL|PAVAS": "locked but consistently WRONG (highest-pop GAM distrito)",
    "SAN JOSE|CENTRAL|HATILLO": "locked but temperature-fragile, high-pop GAM",
    "HEREDIA|CENTRAL|SAN FRANCISCO": "locked+correct, high-pop GAM control",
    "GUANACASTE|LIBERIA|LIBERIA": "locked+correct, high-pop periphery control",
    "SAN JOSE|PEREZ ZELEDON|SAN ISIDRO DE EL GENERAL": "locked+correct, high-pop periphery control",
}


def main():
    print("Building real 2026 distrito network + GAM field...")
    J, h_gam, nodes, empirical = build_graph_and_gam_field("2026")
    nodes = np.asarray(nodes)
    N = len(nodes)
    node_idx = {n: i for i, n in enumerate(nodes)}

    ref = np.load(RESULTS_DIR / "gam_counterfactual_sweep_2026.npz")
    ref_T_idx = int(np.argmin(np.abs(ref["temperatures"] - BEST_T)))
    baseline_map = ref["maps"][ref_T_idx]
    assert list(ref["nodes"]) == list(nodes), "node ordering mismatch vs counterfactual sweep"

    results = []
    for target, category in CANDIDATES.items():
        if target not in node_idx:
            print(f"  [skip] {target}: not found in node set")
            continue
        idx = node_idx[target]
        h_perturbed = h_gam.copy()
        h_perturbed[idx] *= -1
        print(f"\n=== Perturbing {target} ({category}) ===")
        t0 = time.time()
        # temperature_scan with [T]*n_seeds parallelizes all 16 (T, seed) runs across
        # n_jobs workers via ProcessPoolExecutor -- pooled_temperature_scan's own
        # seed-loop is NOT itself parallelized (only the T-list inside each replicate
        # is), so with a single-T list it silently runs seeds sequentially on 1 core.
        # Same pattern as run_direct_paired_test.py's best_t_final_spins_aligned.
        scan_results = temperature_scan(J, h_perturbed, [BEST_T] * FULL_N_SEEDS,
                                         n_equil=FULL_N_EQUIL, n_sweeps=FULL_N_SWEEPS,
                                         dynamics="glauber", seed=FULL_SEED, n_jobs=N_JOBS)
        perturbed_spins = np.array([r["final_spins"] for r in scan_results])
        perturbed_map = np.sign(perturbed_spins.sum(axis=0)).astype(np.int8)
        # align global sign (Z2) to baseline before counting flips at OTHER nodes
        agree = np.mean(perturbed_map == baseline_map)
        if agree < 0.5:
            perturbed_map = -perturbed_map
        diff = (perturbed_map != baseline_map)
        diff[idx] = False  # exclude the perturbed node itself -- its own flip is trivial/expected
        cascade_size = int(diff.sum())
        elapsed = time.time() - t0
        print(f"  cascade size (other nodes flipped): {cascade_size}/{N-1} ({elapsed:.1f}s)")
        if cascade_size:
            print(f"  flipped: {list(nodes[diff])[:10]}{' ...' if cascade_size > 10 else ''}")
        results.append({"target": target, "category": category, "cascade_size": cascade_size})

    print(f"\n{'='*70}\nSummary, ranked by cascade size\n{'='*70}")
    for r in sorted(results, key=lambda x: -x["cascade_size"]):
        print(f"  {r['cascade_size']:>4} other nodes flipped -- {r['target']:45s} ({r['category']})")

    out = RESULTS_DIR / "gam_cascade_analysis_2026.npz"
    np.savez(out, targets=[r["target"] for r in results],
             cascade_sizes=[r["cascade_size"] for r in results])
    print(f"\nRaw results written to {out}")


if __name__ == "__main__":
    main()
