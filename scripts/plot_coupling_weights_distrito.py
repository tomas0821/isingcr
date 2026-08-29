#!/usr/bin/env python3
"""Map the distrito-level coupling network J_ij (border-length-weighted).

Companion to plot_coupling_weights.py (canton level). Highlights the same
kind of structure one administrative level down (N=492, 1350 edges) --
the highest-degree nodes, the near-tripoint weak-coupling cluster -- plus
the headline cross-scale finding: Puerto Jimenez, the canton-level
network's most isolated node (degree 1), has exactly one distrito, whose
edge to Bahia Drake is one of the STRONGEST couplings in the entire
distrito network (J=8.19, vs. a network mean of 1.0) -- a concrete,
visible instance of the paper's own central scale-dependence theme.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

from isingcr.ingestion import build_adjacency_graph, load_shapefile, normalize_distrito_code

DATA_RAW = ROOT / "data" / "raw"
OUT = ROOT / "manuscript" / "figures" / "coupling_weights_distrito.png"

SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

HUBS = ["ALAJUELA|SARCHI|TORO AMARILLO", "HEREDIA|CENTRAL|VARABLANCA"]
PJ = "PUNTARENAS|PUERTO JIMENEZ|PUERTO JIMENEZ"
DRAKE = "PUNTARENAS|OSA|BAHIA DRAKE"

gdf = load_shapefile(SHAPEFILE_PATH, id_col=DISTRITO_COL)
gdf["code"] = [normalize_distrito_code(p, c, d)
               for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]
G = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

gdf = gdf.set_index("code")
centroids = {code: (geom.centroid.x, geom.centroid.y) for code, geom in gdf.geometry.items()}

edges = [(u, v, d["weight"]) for u, v, d in G.edges(data=True)]
weights = np.array([w for _, _, w in edges])
print(f"{len(edges)} edges, weight range [{weights.min():.5f}, {weights.max():.2f}], "
      f"mean {weights.mean():.3f}")

degrees = dict(G.degree())
for h in HUBS:
    print(f"Hub {h}: degree {degrees.get(h)}")
print(f"Puerto Jimenez: degree {degrees.get(PJ)}")
pj_edges = [(u, v, w) for u, v, w in edges if PJ in (u, v)]
print("Puerto Jimenez's edges:", pj_edges)

five_weakest = sorted(edges, key=lambda e: e[2])[:5]
print("5 weakest edges (near-tripoints):")
for u, v, w in five_weakest:
    print(f"  {u} -- {v}: J={w:.5f}")

exploded = gdf.reset_index().explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03

norm = LogNorm(vmin=weights.min(), vmax=weights.max())
cmap = plt.get_cmap("plasma")

fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(ax=ax, facecolor="#eeeeee", edgecolor="#bbbbbb", linewidth=0.15)

# Draw the bulk network thin/faint (1350 edges -- a full-strength rendering
# like the canton figure would be an unreadable hairball at this density);
# the point here is the specific highlighted structure, not every edge.
for u, v, w in edges:
    x1, y1 = centroids[u]
    x2, y2 = centroids[v]
    ax.plot([x1, x2], [y1, y2], color=cmap(norm(w)), linewidth=0.25, alpha=0.35, zorder=2)

# Highlight the Puerto Jimenez / Bahia Drake edge -- the headline finding.
x1, y1 = centroids[PJ]
x2, y2 = centroids[DRAKE]
ax.plot([x1, x2], [y1, y2], color="black", linewidth=2.2, alpha=0.9, zorder=4)
ax.scatter([x1, x2], [y1, y2], s=60, facecolor="lime", edgecolor="black", linewidth=1.0, zorder=5)
ax.annotate("Puerto Jiménez\n(canton: 1 neighbor)\ndistrito edge to Bahía\nDrake: $J=8.19$",
            (x1, y1), xytext=(x1 + 55000, y1 - 55000), fontsize=7.5, ha="left",
            arrowprops=dict(arrowstyle="->", color="black", linewidth=0.8),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", linewidth=0.6, alpha=0.92))

for h in HUBS:
    hx, hy = centroids[h]
    ax.scatter([hx], [hy], s=140, facecolor="none", edgecolor="tab:red", linewidth=2.0, zorder=5)
ax.scatter([], [], s=140, facecolor="none", edgecolor="tab:red", linewidth=2.0,
           label=f"Highest degree (12): Toro Amarillo, Varablanca")

ax.set_axis_off()
ax.set_aspect("equal")
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)
ax.legend(loc="lower left", fontsize=8, frameon=True)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label(r"Coupling weight $J_{ij}$ (log scale, mean $=1.0$)")

# GAM-fringe inset: same near-tripoint phenomenon as the canton network,
# an order of magnitude more extreme here (down to J=0.0003). The single
# weakest edge overall (Tilaran, Guanacaste) is geographically far from
# this GAM-fringe cluster -- annotated separately in the caption/text
# rather than forced into this inset's bounding box.
gam_weakest = five_weakest[1:]
gam_nodes = {n for e in gam_weakest for n in e[:2]}
gxs = [centroids[n][0] for n in gam_nodes]
gys = [centroids[n][1] for n in gam_nodes]
gminx, gmaxx = min(gxs), max(gxs)
gminy, gmaxy = min(gys), max(gys)
gpad_x, gpad_y = (gmaxx - gminx) * 0.3, (gmaxy - gminy) * 0.3

axins = fig.add_axes([0.58, 0.60, 0.34, 0.34])
gdf.plot(ax=axins, facecolor="#eeeeee", edgecolor="#999999", linewidth=0.3)
for u, v, w in edges:
    x1e, y1e = centroids[u]
    x2e, y2e = centroids[v]
    axins.plot([x1e, x2e], [y1e, y2e], color=cmap(norm(w)), linewidth=0.6 + 2.5 * norm(w),
               alpha=0.9, zorder=2, solid_capstyle="round")
offsets = [(0, 22), (0, -22), (28, 10), (-30, -10)]
for (u, v, w), (dx, dy) in zip(gam_weakest, offsets):
    x1e, y1e = centroids[u]
    x2e, y2e = centroids[v]
    xm, ym = (x1e + x2e) / 2, (y1e + y2e) / 2
    axins.annotate(f"{w:.4f}", (xm, ym), textcoords="offset points", xytext=(dx, dy),
                    fontsize=6.5, color="black", ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", color="black", linewidth=0.5),
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="black", linewidth=0.4, alpha=0.9))
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
axins.set_title("Weakest edges (near-tripoints)\n(distrito boundaries meeting\nat a vanishing shared border)",
                 fontsize=7.5)

rect = Rectangle((inset_xlim[0], inset_ylim[0]),
                  inset_xlim[1] - inset_xlim[0], inset_ylim[1] - inset_ylim[0],
                  fill=False, edgecolor="black", linewidth=1.0, zorder=6)
ax.add_patch(rect)

fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}")
