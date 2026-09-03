#!/usr/bin/env python3
"""Two figures from the saved canton (ablation.npz, N=84, 8 seeds, 24 T) and
distrito (distrito_ablation.npz, N=488, 16 seeds, 32 T) ablation curves:

  figures/resolution_reversal.png   -- the paper's headline visual: alignment
      vs T at canton (left) and distrito (right) resolution on a shared
      y-axis, geography-only vs geography+field. The gap opens from left to
      right.
  figures/response_functions_sm.png -- susceptibility and specific heat for
      both resolutions (Supplementary Material). Both rise monotonically as
      T -> 0, the low-T pooling artifact the main text describes; no interior
      peak.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "data" / "processed"
F = ROOT / "manuscript" / "figures"

canton = np.load(P / "ablation.npz")
distrito = np.load(P / "distrito_ablation.npz")

GRAY, RED = "tab:gray", "tab:red"


def alignment_panel(ax, d, title, show_legend):
    T = d["temperatures"]
    ax.errorbar(T, d["accuracy_a"], yerr=d["accuracy_a_std"], fmt="o-", color=GRAY,
                capsize=2, ms=3.5, lw=1.2, alpha=0.9, label="geography only ($h=0$)")
    ax.errorbar(T, d["accuracy_b"], yerr=d["accuracy_b_std"], fmt="o-", color=RED,
                capsize=2, ms=3.5, lw=1.2, alpha=0.9, label="geography + field ($h=$ margin)")
    ax.axhline(float(d["baseline"]), color="k", ls=":", lw=1, label="majority-class baseline")
    ax.axhline(0.5, color="gray", ls="--", lw=0.8, label="chance (symmetric)")
    gap = d["accuracy_b"].max() - d["accuracy_a"].max()
    ax.set_title(f"{title}   best-fit gain from field: {100*gap:+.1f} pp", fontsize=10)
    ax.set_xlabel("temperature $T$")
    ax.set_ylim(0.45, 0.85)
    ax.grid(alpha=0.25)
    if show_legend:
        ax.legend(fontsize=8, loc="lower right")


fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), sharey=True)
alignment_panel(axes[0], canton, f"canton resolution ($N={int(canton['N'])}$)", True)
alignment_panel(axes[1], distrito, f"distrito resolution ($N={int(distrito['N'])}$)", False)
axes[0].set_ylabel("best-fit alignment with real 2026 map")
fig.tight_layout()
fig.savefig(F / "resolution_reversal.png", dpi=200)
print("wrote", F / "resolution_reversal.png")

fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
for row, (d, name) in enumerate([(canton, "canton ($N=84$)"), (distrito, "distrito ($N=488$)")]):
    T = d["temperatures"]
    for col, (key, lab) in enumerate([("chi", r"susceptibility $\chi$"), ("C", "specific heat $C$")]):
        ax = axes[row, col]
        ax.plot(T, d[f"{key}_a"], "o-", color=GRAY, ms=3, lw=1.1, label="geography only")
        ax.plot(T, d[f"{key}_b"], "o-", color=RED, ms=3, lw=1.1, label="geography + field")
        ax.set_title(f"{lab}, {name}", fontsize=10)
        ax.set_xlabel("temperature $T$")
        ax.grid(alpha=0.25)
        if row == 0 and col == 0:
            ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(F / "response_functions_sm.png", dpi=200)
print("wrote", F / "response_functions_sm.png")
