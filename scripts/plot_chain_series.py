#!/usr/bin/env python3
"""SM figure: alignment of the running configuration with the 2026 map, every
100 measurement sweeps, for the 16 chains of the canton-proxy run at T=1.008
(seeds 7-22). Shows the two atypical starts: one frozen in a periphery domain
(seed 20) and one decaying out of it during the measurement window (seed 10).
Reads gam_timeavg_grid_2026.npz (run_gam_timeavg_grid.py)."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent.parent
z = np.load(ROOT / "data/processed/gam_timeavg_grid_2026.npz", allow_pickle=True)
ser = z["proxy_hi_align_series"]; seed0 = int(z["proxy_hi_seed0"]); n = ser.shape[1]
x = np.arange(n) * 100
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for k in range(ser.shape[0]):
    if k in (3, 13):
        continue
    ax.plot(x, 100 * ser[k], color="0.75", lw=0.8, label="14 stationary chains" if k == 0 else None)
ax.plot(x, 100 * ser[13], color="tab:red", lw=1.4, label=f"seed {seed0+13}: periphery domain, frozen")
ax.plot(x, 100 * ser[3], color="tab:blue", lw=1.4, label=f"seed {seed0+3}: periphery domain, decaying")
ax.set_xlabel("measurement sweep"); ax.set_ylabel("alignment with 2026 map (%)")
ax.set_title("Canton-proxy GAM field, $T=1.008$, 16 chains after 20,000 equilibration sweeps", fontsize=10)
ax.legend(fontsize=8, loc="lower right", frameon=False)
ax.set_ylim(60, 86)
fig.tight_layout()
out = ROOT / "manuscript/figures/chain_series.png"; fig.savefig(out, dpi=200); print("wrote", out)
