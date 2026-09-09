#!/usr/bin/env python3
"""Map the canton-level coupling network J_ij (border-length-weighted).

Illustrates two real features of the coupling data described in
Section 2.2 (Geographic adjacency network) but not otherwise visualized:
the highest-degree hub (Heredia Central, 13 neighbors) and lowest-degree
pendant (Puerto Jimenez, 1 neighbor), plus a cluster of near-zero-weight
edges in the dense GAM core where canton boundaries meet at a vanishingly
short shared segment (a near-tripoint) rather than a genuine border.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D

from isingcr.ingestion import build_adjacency_graph, load_shapefile, normalize_canton_code

DATA_RAW = ROOT / "data" / "raw"
OUT = ROOT / "manuscript" / "figures" / "coupling_weights.png"

SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL, CANTON_COL = "adm1_name", "adm2_name"

HUB = "HEREDIA|CENTRAL"
PENDANT = "PUNTARENAS|PUERTO JIMENEZ"

gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
G = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

gdf = gdf.set_index("code")
centroids = {code: (geom.centroid.x, geom.centroid.y) for code, geom in gdf.geometry.items()}

edges = [(u, v, d["weight"]) for u, v, d in G.edges(data=True)]
weights = np.array([w for _, _, w in edges])
print(f"{len(edges)} edges, weight range [{weights.min():.4f}, {weights.max():.2f}], "
      f"mean {weights.mean():.3f} (normalized to 1.0 by construction)")

degrees = dict(G.degree())
print(f"Hub {HUB}: degree {degrees.get(HUB)}")
print(f"Pendant {PENDANT}: degree {degrees.get(PENDANT)}")

five_weakest = sorted(edges, key=lambda e: e[2])[:5]
print("5 weakest edges (near-tripoints):")
for u, v, w in five_weakest:
    print(f"  {u} -- {v}: J={w:.4f}")

# Exclude offshore Isla del Coco (Puntarenas multipolygon, ~500km from mainland)
# from the plotted extent, matching plot_admin_map.py's convention.
exploded = gdf.reset_index().explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03

norm = LogNorm(vmin=weights.min(), vmax=weights.max())
cmap = plt.get_cmap("plasma")

fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(ax=ax, facecolor="#eeeeee", edgecolor="#999999", linewidth=0.4)

for u, v, w in edges:
    x1, y1 = centroids[u]
    x2, y2 = centroids[v]
    ax.plot([x1, x2], [y1, y2], color=cmap(norm(w)), linewidth=0.6 + 2.5 * norm(w),
             alpha=0.85, zorder=2, solid_capstyle="round")

hx, hy = centroids[HUB]
ax.scatter([hx], [hy], s=140, facecolor="none", edgecolor="tab:red", linewidth=2.0,
           zorder=5, label=f"Heredia Central (degree {degrees[HUB]}, highest)")
px, py = centroids[PENDANT]
ax.scatter([px], [py], s=140, marker="D", facecolor="none", edgecolor="tab:blue",
           linewidth=2.0, zorder=5, label=f"Puerto Jiménez (degree {degrees[PENDANT]}, lowest)")

ax.set_axis_off()
ax.set_aspect("equal")
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)
ax.legend(loc="lower left", fontsize=9, frameon=True)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label(r"Coupling weight $J_{ij}$ (log scale, mean $=1.0$)")

# GAM-core inset: same edges, zoomed to the bounding box of the 5 weakest edges'
# endpoints, where the near-tripoint low-weight edges are otherwise invisible
# at national scale.
gam_nodes = {n for e in five_weakest for n in e[:2]}
gxs = [centroids[n][0] for n in gam_nodes]
gys = [centroids[n][1] for n in gam_nodes]
gminx, gmaxx = min(gxs), max(gxs)
gminy, gmaxy = min(gys), max(gys)
gpad_x, gpad_y = (gmaxx - gminx) * 0.35, (gmaxy - gminy) * 0.35

axins = fig.add_axes([0.60, 0.62, 0.34, 0.34])
gdf.plot(ax=axins, facecolor="#eeeeee", edgecolor="#999999", linewidth=0.5)
for u, v, w in edges:
    x1, y1 = centroids[u]
    x2, y2 = centroids[v]
    axins.plot([x1, x2], [y1, y2], color=cmap(norm(w)), linewidth=0.8 + 3.0 * norm(w),
               alpha=0.9, zorder=2, solid_capstyle="round")
for u, v, w in five_weakest:
    x1, y1 = centroids[u]
    x2, y2 = centroids[v]
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
    axins.annotate(f"{w:.3f}", (xm, ym), fontsize=6.5, color="black",
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
inset_xlim = (gminx - gpad_x, gmaxx + gpad_x)
inset_ylim = (gminy - gpad_y, gmaxy + gpad_y)
axins.set_xlim(*inset_xlim)
axins.set_ylim(*inset_ylim)
axins.set_xticks([])
axins.set_yticks([])
for spine in axins.spines.values():
    spine.set_visible(True)
    spine.set_edgecolor("black")
    spine.set_linewidth(1.2)
axins.set_title("GAM core: near-tripoint edges\n(shared-border length in meters/mean)",
                 fontsize=8)

# Rectangle on the main map marking the zoomed region, connected to the inset.
from matplotlib.patches import Rectangle
rect = Rectangle((inset_xlim[0], inset_ylim[0]),
                  inset_xlim[1] - inset_xlim[0], inset_ylim[1] - inset_ylim[0],
                  fill=False, edgecolor="black", linewidth=1.2, zorder=6)
ax.add_patch(rect)
for (mx, my) in [(inset_xlim[1], inset_ylim[1]), (inset_xlim[1], inset_ylim[0])]:
    fig_coords_main = ax.transData.transform((mx, my))
    ax.annotate("", xy=(0.60, 0.62 + (0.34 if my == inset_ylim[1] else 0)),
                xycoords="figure fraction", xytext=(mx, my), textcoords="data",
                arrowprops=dict(arrowstyle="-", color="black", linewidth=0.6, alpha=0.6))

fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}")
