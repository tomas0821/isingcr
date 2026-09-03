#!/usr/bin/env python3
"""Re-plot figures/finite_size_scaling_heavy.png from the saved
finite_size_scaling_heavy.npz (no re-run of the cluster scan). Same content
as run_finite_size_scaling_heavy.plot() minus the in-figure title, which
duplicated the caption and was clipped at the figure edge.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
d = np.load(ROOT / "data" / "processed" / "finite_size_scaling_heavy.npz")
T = d["temperatures"]

fig, ax = plt.subplots(figsize=(7, 4.6))
ax.axhspan(0, 2 / 3, color="green", alpha=0.06, label="physically valid $U_4$ range $[0, 2/3]$")
ax.plot(T, d["U4_canton"], "o-", color="tab:blue", ms=3.5, lw=1.2,
        label=f"canton ($N={int(d['N_canton'])}$)")
ax.plot(T, d["U4_distrito"], "o-", color="tab:orange", ms=3.5, lw=1.2,
        label=f"distrito ($N={int(d['N_distrito'])}$)")
for i, c in enumerate(d["crossings"]):
    ax.axvline(c, color="gray", ls="--", lw=0.9, label="crossings (5)" if i == 0 else None)
ax.set_xlabel("temperature $T$")
ax.set_ylabel("Binder cumulant $U_4$")
ax.set_ylim(-0.02, 0.72)
ax.grid(alpha=0.25)
ax.legend(fontsize=8, loc="lower center")
fig.tight_layout()
out = ROOT / "manuscript" / "figures" / "finite_size_scaling_heavy.png"
fig.savefig(out, dpi=200)
print("wrote", out)
