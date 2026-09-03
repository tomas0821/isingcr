#!/usr/bin/env python3
"""Leave-one-province-out spatial cross-validation for the 2026 GAM headline
result (run_gam_field.py: best T=1.008, best accuracy=81.07%, N=488).

Motivation: every accuracy number in this paper so far is in-sample -- the
same real map is used both to select the best temperature and to report the
accuracy at that temperature. This does not test whether the fitted model
generalizes to geography it was not scored against. A genuine held-out test
answers a different, stronger question a reviewer could otherwise raise:
"how do we know this isn't just overfitting the temperature grid to this one
map?"

Design (the cheap variant, not a full per-fold T-reselection -- see
00_Master_Notebook.md for the cost tradeoff): fix T at the already-selected
headline value (no re-scanning the 32-point grid per fold -- h_i is given
directly from the GAM list, so T is the only thing "fit" to data at all).
Run 16 independent seeds at that T (same budget as every other headline
number: n_equil=n_sweeps=20000), saving each seed's final spin configuration.
Split the N=488 distritos into the SAME 7 province-blocks already used by
run_spatial_block_sensitivity.py's granularity check. For each held-out
province: resolve the model's Z2 sign ambiguity using ONLY the training
(non-held-out) nodes' accuracy (to avoid leaking the held-out labels into
that decision), then score accuracy on the held-out province's nodes with
that fixed sign. Report per-province test accuracy against that province's
own majority-class baseline, plus a McNemar test.

This is a real, if partial, generalization test: it does not re-derive T
from only training data (that would need a per-fold 32-point grid rerun --
a natural but far more expensive follow-up, see the script's own est.
resource note below), so it can't rule out that the single global T value
was implicitly tuned on the full map. It CAN answer whether the fitted
equilibrium's accuracy holds up uniformly across held-out geography or is
being carried by just one or two provinces.
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
from run_gam_field import build_graph_and_gam_field
from run_spatial_block_sensitivity import best_t_final_spins, province_blocks

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

# From data/processed/gam_field_2026.npz's saved result -- the headline best_T,
# reused here rather than re-selecting per fold (see docstring).
BEST_T_2026 = 1.0080645161290325
N_JOBS = 12  # matches run_spatial_block_sensitivity.py's local budget


def held_out_fold(final_spins_per_seed, empirical, blocks, held_block):
    """Score one province held out: resolve the Z2 sign using ONLY the
    training (non-held-out) nodes, then score the held-out nodes with that
    fixed sign -- no information from the held-out province enters the sign
    decision."""
    train_mask = blocks != held_block
    test_mask = blocks == held_block
    per_seed = []
    for s in final_spins_per_seed:
        train_match = alignment_fraction(s[train_mask], empirical[train_mask])
        s_aligned = s if train_match >= 0.5 else -s
        train_acc = max(train_match, 1.0 - train_match)
        test_acc = alignment_fraction(s_aligned[test_mask], empirical[test_mask])
        per_seed.append({"train_acc": train_acc, "test_acc": test_acc, "spins_aligned": s_aligned})
    return per_seed


def main():
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print("Building real 2026 distrito network + GAM field...")
    t0 = time.time()
    J, h_gam, nodes, empirical = build_graph_and_gam_field("2026")
    N = J.shape[0]
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    blocks = province_blocks(nodes)
    provinces = sorted(np.unique(blocks))
    print(f"  {len(provinces)} province-blocks: "
          + ", ".join(f"{p} (n={int((blocks == p).sum())})" for p in provinces))

    print(f"\nRunning {FULL_N_SEEDS} seeds at fixed T={BEST_T_2026:.4f} "
          f"(n_equil={FULL_N_EQUIL}, n_sweeps={FULL_N_SWEEPS})...")
    t_start = time.time()
    final_spins = best_t_final_spins(J, h_gam, BEST_T_2026, n_equil=FULL_N_EQUIL,
                                      n_sweeps=FULL_N_SWEEPS, n_seeds=FULL_N_SEEDS,
                                      n_jobs=N_JOBS, seed=FULL_SEED)
    elapsed = time.time() - t_start
    print(f"  done in {elapsed:.1f}s ({elapsed / 60:.1f} min)")

    # In-sample sanity check: symmetric alignment over the full map should
    # reproduce the headline 81.07% (same T, same seed budget).
    full_match = [alignment_fraction(s, empirical) for s in final_spins]
    full_sym = [max(m, 1 - m) for m in full_match]
    print(f"\nIn-sample sanity check (full N=488, symmetric alignment): "
          f"median={np.median(full_sym):.4%} (headline was 81.07%)")

    print("\n=== Leave-one-province-out spatial cross-validation ===")
    rows = []
    for prov in provinces:
        test_mask = blocks == prov
        n_test = int(test_mask.sum())
        maj_label = 1 if np.mean(empirical[test_mask] == 1) > 0.5 else -1
        baseline = float(np.mean(empirical[test_mask] == maj_label))

        per_seed = held_out_fold(final_spins, empirical, blocks, prov)
        test_accs = [r["test_acc"] for r in per_seed]
        train_accs = [r["train_acc"] for r in per_seed]
        median_test = float(np.median(test_accs))

        null_spins = np.full(n_test, maj_label)
        mc_ps = [mcnemar_test(r["spins_aligned"][test_mask], null_spins,
                               empirical[test_mask])["exact_pvalue"] for r in per_seed]
        median_p = float(np.median(mc_ps))

        print(f"  {prov:12s} n={n_test:4d}  train_acc(median)={np.median(train_accs):.4%}  "
              f"HELD-OUT test_acc(median)={median_test:.4%}  baseline={baseline:.4%}  "
              f"McNemar median p={median_p:.4f}")
        rows.append({
            "province": prov, "n_test": n_test, "baseline": baseline,
            "median_train_acc": float(np.median(train_accs)),
            "median_test_acc": median_test, "mcnemar_median_p": median_p,
            "test_accs": test_accs, "mcnemar_ps": mc_ps,
        })

    pooled_test = np.concatenate([r["test_accs"] for r in rows])
    weighted_mean = sum(r["median_test_acc"] * r["n_test"] for r in rows) / N
    print(f"\nPooled held-out accuracy across all 7 folds: "
          f"mean of per-seed values={pooled_test.mean():.4%}, "
          f"size-weighted mean of per-province medians={weighted_mean:.4%} "
          f"(vs. in-sample headline 81.07%)")

    out_path = RESULTS_DIR / "gam_spatial_cv_2026.npz"
    np.savez(out_path, rows=np.array(rows, dtype=object), best_T=BEST_T_2026,
             n_equil=FULL_N_EQUIL, n_sweeps=FULL_N_SWEEPS, n_seeds=FULL_N_SEEDS,
             full_map_symmetric_alignment_median=float(np.median(full_sym)),
             weighted_mean_test_acc=weighted_mean)
    print(f"\nRaw results written to {out_path}")


if __name__ == "__main__":
    main()
