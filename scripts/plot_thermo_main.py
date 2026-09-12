#!/usr/bin/env python3
"""Main-text figure: the conventional statistical-mechanics diagnostics in one
row. (a) susceptibility chi(T) and (b) specific heat C(T) for the geography-
plus-margin arm at both resolutions (ablation.npz, distrito_ablation.npz; the
h=0 arm's chi is uninformative below ordering, see main text Sec. 3.3), and
(c) the Binder cumulant U4(T) of the canton and distrito networks at h=0
(finite_size_scaling_heavy.npz). None shows an interior peak or a single
crossing."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "data" / "processed"
c = np.load(P / "ablation.npz", allow_pickle=True); d = np.load(P / "distrito_ablation.npz", allow_pickle=True)
f = np.load(P / "finite_size_scaling_heavy.npz", allow_pickle=True)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
ax = axes[0]
ax.plot(c["temperatures"], c["chi_b"], "o-", ms=3, color="tab:blue", label="canton, $N=84$")
ax.plot(d["temperatures"], d["chi_b"], "s-", ms=3, color="tab:orange", label="distrito, $N=488$")
ax.set_yscale("log"); ax.set_xlabel("$T$"); ax.set_ylabel(r"$\chi$"); ax.set_title("(a) susceptibility, geography + margin", fontsize=9)
ax.legend(fontsize=8, frameon=False)
ax = axes[1]
ax.plot(c["temperatures"], c["C_b"], "o-", ms=3, color="tab:blue")
ax.plot(d["temperatures"], d["C_b"], "s-", ms=3, color="tab:orange")
ax.set_yscale("log"); ax.set_xlabel("$T$"); ax.set_ylabel("$C$"); ax.set_title("(b) specific heat, geography + margin", fontsize=9)
ax = axes[2]
T = f["temperatures"]
ax.plot(T, f["U4_canton"], "o-", ms=3, color="tab:blue", label="canton")
ax.plot(T, f["U4_distrito"], "s-", ms=3, color="tab:orange", label="distrito")
for x in f["crossings"]:
    ax.axvline(float(x), color="0.7", lw=0.7, ls=":")
ax.axhline(2 / 3, color="0.5", lw=0.6, ls="--"); ax.set_ylim(0, 0.72)
ax.set_xlabel("$T$"); ax.set_ylabel("$U_4$"); ax.set_title("(c) Binder cumulant, $h=0$", fontsize=9)
ax.legend(fontsize=8, frameon=False, loc="lower left")
fig.tight_layout()
out = ROOT / "manuscript" / "figures" / "thermo_main.png"; fig.savefig(out, dpi=200); print("wrote", out, "crossings:", np.round(f["crossings"], 2).tolist())
