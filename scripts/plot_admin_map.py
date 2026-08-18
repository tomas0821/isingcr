#!/usr/bin/env python3
"""Costa Rica canton (N=84) vs distrito (N=492) administrative geometry, overlaid."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/home/tomas/mnt/gdrive/Research/Current/IsingCR/src")))

import matplotlib.pyplot as plt
from isingcr.ingestion import load_shapefile

DATA_RAW = Path("/home/tomas/mnt/gdrive/Research/Current/IsingCR/data/raw")
OUT = Path("/home/tomas/mnt/gdrive/Research/Current/IsingCR/manuscript/figures/admin_map.png")

canton = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp", id_col="adm2_name")
distrito = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp", id_col="adm3_name")

# Exclude the remote offshore Isla del Coco (part of Puntarenas canton's
# multipolygon, ~500km from the mainland) when computing the plot extent,
# so the mainland isn't squeezed into a corner of the figure.
exploded = canton.explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03
xlim = (minx - pad_x, maxx + pad_x)
ylim = (miny - pad_y, maxy + pad_y)

fig, ax = plt.subplots(figsize=(7, 7))

distrito.plot(ax=ax, facecolor="#dbe6f2", edgecolor="#888888", linewidth=0.3,
              label=f"distritos (N={len(distrito)})")
canton.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=1.0,
            label=f"cantons (N={len(canton)})")

ax.set_axis_off()
ax.set_aspect("equal")
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)

fig.tight_layout()
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}, canton N={len(canton)}, distrito N={len(distrito)}")
