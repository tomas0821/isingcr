#!/usr/bin/env python3
"""Figure: best-fit alignment vs. field weight lambda for the GAM field
(run_gam_lambda_scan.py, 2026) and the circular own-margin field
(run_3d_scan.py --lambda_pol extension, scan_3d_polext_pol{0..8}_soc0.npz,
2026), on the same axes, with each field's structural ceiling as a dashed
line. This is the paper's "genuine field vs. label leak" argument in one
picture: GAM peaks at finite lambda* ~ 1.5 and sits on its 80.9% ceiling;
the own-margin field climbs monotonically toward its 99.8% ceiling.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from run_gam_field import build_graph_and_gam_field  # noqa: E402

P = ROOT / "data" / "processed"
OUT = ROOT / "manuscript" / "figures" / "gam_lambda_scan.png"

# GAM scan
gam = []
for i in range(9):
    r = np.load(P / f"gam_lambda_scan_2026_lam{i}.npz", allow_pickle=True)["results"][0]
    gam.append((r["lambda_soc"], r["best_accuracy"], r["best_accuracy_std"]))
gam.sort()
# lambda=0 point = geography-only baseline (same run family as the own-margin extension)
base = np.load(P / "scan_3d_polext_pol0_soc0.npz", allow_pickle=True)["results"][0]
gam.insert(0, (0.0, base["best_accuracy"], 0.0))

# own-margin extension
own = []
for i in range(9):
    r = np.load(P / f"scan_3d_polext_pol{i}_soc0.npz", allow_pickle=True)["results"][0]
    own.append((r["lambda_pol"], r["best_accuracy"], 0.0))
own.sort()

# ceilings
J, h_gam, nodes, emp = build_graph_and_gam_field("2026")
gam_ceiling = max(np.mean(np.sign(h_gam) == emp), np.mean(np.sign(h_gam) == -emp))
own_ceiling = 0.998  # sign(h_own) == label on 487/488 nodes by construction (main text)

gl, ga, gs = np.array(gam).T
ol, oa, _ = np.array(own).T
print("GAM ceiling:", gam_ceiling, "lambda*:", gl[np.argmax(ga)], "peak:", ga.max())

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.errorbar(gl, 100 * ga, yerr=100 * gs, fmt="o-", color="tab:red", capsize=3,
            label="GAM (capital region, $h_i=\\pm1$)")
ax.plot(ol, 100 * oa, "s--", color="tab:gray", label="own vote margin (circular)")
ax.axhline(100 * gam_ceiling, color="tab:red", ls=":", lw=1)
ax.text(8.1, 100 * gam_ceiling + 0.4, f"GAM ceiling {100*gam_ceiling:.1f}%", color="tab:red",
        fontsize=8, ha="right", va="bottom")
ax.axhline(100 * own_ceiling, color="tab:gray", ls=":", lw=1)
ax.text(8.1, 100 * own_ceiling - 0.5, "own-margin ceiling 99.8%", color="tab:gray",
        fontsize=8, ha="right", va="top")
ax.axhline(100 * base["best_accuracy"], color="k", ls="-.", lw=0.8)
ax.text(0.05, 100 * base["best_accuracy"] - 0.5, "geography only", fontsize=8, va="top")
ax.axvline(gl[np.argmax(ga)], color="tab:red", lw=0.6, alpha=0.4)
ax.text(gl[np.argmax(ga)] + 0.1, 70, r"$\lambda^{*}$", color="tab:red", fontsize=10)
ax.set_xlabel(r"field weight $\lambda$ (units of mean $J_{ij}$)")
ax.set_ylabel("best-fit alignment with real 2026 map (%)")
ax.set_xlim(-0.2, 8.3)
ax.set_ylim(64, 101)
ax.legend(loc="lower right", fontsize=9)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT, dpi=200)
print("wrote", OUT)
