#!/usr/bin/env python3
"""Direct paired spatial-block test between the two readings of the official
GAM boundary (inclusive any-overlap vs. area-majority), from the spins saved by
run_true_gam_paired_test.py (same 16 seeds, each reading at its own best T).
Round-8 referee item: the inclusive-vs-strict comparison in Section 4.5 had
only been made indirectly, through each reading's head-to-head with the proxy.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.observables import spatial_block_permutation_test_paired
from run_direct_paired_test import canton_blocks
from run_gam_true_field import build_true_field

P = Path(__file__).resolve().parent.parent / "data" / "processed"
N_PERM = 99_999


def main():
    a = np.load(P / "true_gam_paired_test_any_lam1_2026.npz", allow_pickle=True)
    m = np.load(P / "true_gam_paired_test_majority_lam1_2026.npz", allow_pickle=True)
    assert np.array_equal(a["spins_proxy"], m["spins_proxy"]), "seed sets differ"
    _, _, nodes, emp, _ = build_true_field("any", verbose=False)
    blocks = canton_blocks(nodes)
    sa, sm = a["spins_true"], m["spins_true"]
    d = np.array([np.mean(sa[i] == emp) - np.mean(sm[i] == emp) for i in range(len(sa))])
    ps = np.array([spatial_block_permutation_test_paired(sm[i], sa[i], emp, blocks, n_permutations=N_PERM,
                                                          rng=np.random.default_rng(i))["p_value"] for i in range(len(sa))])
    print(f"inclusive - majority per seed (pts): {np.round(100*d,2).tolist()}")
    print(f"inclusive ahead in {(d>0).sum()}/{len(d)} seeds; median {100*np.median(d):+.2f} pts; mean {100*d.mean():+.2f}")
    print(f"paired spatial-block p: median {np.median(ps):.4f}, significant {(ps<0.05).sum()}/{len(ps)}; x32 = {32*np.median(ps):.3f}")
    print(f"T_any={float(a['T']):.3f} T_majority={float(m['T']):.3f}")
    np.savez(P / "official_readings_head_to_head_2026.npz", diff=d, ps=ps, T_any=a["T"], T_majority=m["T"])


if __name__ == "__main__":
    main()
