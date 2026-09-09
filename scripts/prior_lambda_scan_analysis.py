#!/usr/bin/env python3
"""Post-hoc analysis of the political-continuity field's lambda_soc scan
(prior_lambda_scan_2026_lam*.npz): per-lambda energy decomposition, field-
following fraction, and head-to-head paired spatial-block tests (99,999
draws, canton blocks, seed-by-seed) of the political field against the GAM
field at matched points: lambda=6 (sigma-matched) vs GAM lambda=1, and the
political peak vs GAM's lambda*=1.5. Prints a LaTeX-ready table.
"""
import sys, glob
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from isingcr.simulation.observables import spatial_block_permutation_test_paired, alignment_fraction
from run_prior_margin_field import build_graph_and_prior_field
from run_direct_paired_test import canton_blocks
P = ROOT / "data" / "processed"
J, h, nodes, emp, _ = build_graph_and_prior_field()
Jc = J.tocsr()
rows = {}
for f in sorted(glob.glob(str(P / "prior_lambda_scan_2026_lam*.npz"))):
    r = np.load(f, allow_pickle=True)["results"][0]
    lam = r["lambda_soc"]; spins = r["best_final_spins"]
    spins = np.array([s if alignment_fraction(s, emp) >= 0.5 else -s for s in spins])
    EJ = np.mean([0.5 * s @ (Jc @ s) for s in spins]); Eh = np.mean([lam * (h @ s) for s in spins])
    nz = h != 0
    follow = np.mean([np.mean(np.sign(h[nz]) == s[nz]) for s in spins])
    rows[lam] = dict(T=r["best_T"], acc=r["best_accuracy"], std=r["best_accuracy_std"], mc=r["mcnemar_median_p"],
                     EJ=abs(EJ), Eh=abs(Eh), share=abs(Eh) / (abs(EJ) + abs(Eh)), follow=follow, spins=spins)
print("lam & align & T & McNemar & |E_J| & |E_h| & share & follows")
for lam, d in sorted(rows.items()):
    print(f"{lam:g} & {100*d['acc']:.2f}% +/- {100*d['std']:.2f}% & {d['T']:.3f} & {d['mc']:.2g} & {d['EJ']:.0f} & {d['Eh']:.0f} & {d['share']:.3f} & {100*d['follow']:.1f}%")
gam = {}
for i, lam in enumerate([0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 8.0]):
    r = np.load(P / f"gam_lambda_scan_2026_lam{i}.npz", allow_pickle=True)["results"][0]
    gam[lam] = np.array([s if alignment_fraction(s, emp) >= 0.5 else -s for s in r["best_final_spins"]])
blocks = canton_blocks(nodes)
peak = max(rows, key=lambda k: rows[k]["acc"])
for (pl, gl) in [(6.0, 1.0), (peak, 1.5), (peak, 1.0)]:
    if pl not in rows: continue
    ps = np.array([spatial_block_permutation_test_paired(gam[gl][i], rows[pl]["spins"][i], emp, blocks, n_permutations=99_999,
                                                         rng=np.random.default_rng(i))["p_value"] for i in range(16)])
    stat = np.median([np.mean(rows[pl]["spins"][i] == emp) - np.mean(gam[gl][i] == emp) for i in range(16)])
    print(f"political lam={pl:g} vs GAM lam={gl:g}: median alignment diff (pol-GAM)={100*stat:+.2f} pts, median p={np.median(ps):.4f}, sig {int((ps<0.05).sum())}/16, pol better in {int((np.array([np.mean(rows[pl]['spins'][i]==emp)-np.mean(gam[gl][i]==emp) for i in range(16)])>0).sum())}/16 seeds")
