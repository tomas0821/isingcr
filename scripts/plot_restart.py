#!/usr/bin/env python3
"""SM figure: alignment of chains started at the consensus configuration and
at the 72-site periphery domain, 100,000 sweeps, both fields at T=1.008 and
T=0.689 (restart_from_consensus_2026.npz)."""
from pathlib import Path
import numpy as np, matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent.parent
z = np.load(ROOT / "data/processed/restart_from_consensus_2026.npz", allow_pickle=True)
cells = [("proxy_hi", "proxy, $T=1.008$"), ("any_hi", "official, $T=1.008$"), ("proxy_lo", "proxy, $T=0.689$"), ("any_lo", "official, $T=0.689$")]
fig, axes = plt.subplots(2, 2, figsize=(9, 5.6), sharex=True, sharey=True)
for ax, (tag, lab) in zip(axes.flat, cells):
    for st, col in (("consensus", "0.6"), ("domain", "tab:red")):
        al = z[f"{tag}_{st}_align"]; x = np.arange(al.shape[1]) * 500
        for k in range(al.shape[0]):
            ax.plot(x, 100 * al[k], color=col, lw=0.7, alpha=0.8, label=f"from {st}" if k == 0 else None)
    ax.set_title(lab, fontsize=9); ax.set_ylim(64, 84)
    ax.legend(fontsize=7, frameon=False, loc="center right")
for ax in axes[1]: ax.set_xlabel("sweep")
for ax in axes[:, 0]: ax.set_ylabel("alignment (%)")
fig.tight_layout(); out = ROOT / "manuscript/figures/restart_series.png"; fig.savefig(out, dpi=200); print("wrote", out)
