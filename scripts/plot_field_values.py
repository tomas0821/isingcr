#!/usr/bin/env python3
"""Map the canton-level field h_i (2026 own-margin), highlighting real outliers.

Companion to plot_coupling_weights.py/plot_coupling_weights_distrito.py.
Shows the field the Hamiltonian actually uses (h_i = own vote margin,
coalition-split binarization) as a choropleth, and connects the field to
the coupling story from those two figures directly: Puerto Jimenez and
Bahia Drake -- the distrito pair joined by the network's strongest edge
(J=8.19) -- are also both extreme, same-direction field outliers, a
concrete case of correlated field + strong coupling reinforcing each other.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

from isingcr.ingestion import (
    binarize_votes, build_adjacency_graph, build_electoral_graph, load_shapefile,
    load_tse_juntas_consolidado, normalize_canton_code, normalize_distrito_code,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = ROOT / "data" / "raw"
OUT = ROOT / "manuscript" / "figures" / "field_values.png"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]

CANTON_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
DISTRITO_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

MONTES_DE_OCA = "SAN JOSE|MONTES DE OCA"
PJ_CANTON = "PUNTARENAS|PUERTO JIMENEZ"
BUENOS_AIRES = "PUNTARENAS|BUENOS AIRES"
PJ_DISTRITO = "PUNTARENAS|PUERTO JIMENEZ|PUERTO JIMENEZ"
DRAKE = "PUNTARENAS|OSA|BAHIA DRAKE"

# --- Canton-level field ---
results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="canton")
binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)
gdf_c = load_shapefile(CANTON_SHAPEFILE, id_col=CANTON_COL)
gdf_c["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf_c[PROVINCE_COL], gdf_c[CANTON_COL])]
adj_c = build_adjacency_graph(gdf_c, id_col="code", weight_by="border_length")
Gc = build_electoral_graph(adj_c, binarized, code_col="code", h_col="margin")
arrays_c = graph_to_arrays(Gc)
nodes_c, h_c = arrays_c["nodes"], arrays_c["h"]
h_by_code = dict(zip(nodes_c, h_c))
gdf_c = gdf_c.set_index("code")
gdf_c["h"] = gdf_c.index.map(h_by_code)

print(f"Canton h range: [{h_c.min():.3f}, {h_c.max():.3f}], mean {h_c.mean():.3f}")
print(f"Most anti-incumbent: {nodes_c[np.argmin(h_c)]} h={h_c.min():.3f}")
print(f"Most pro-incumbent: {nodes_c[np.argmax(h_c)]} h={h_c.max():.3f}")

# --- Distrito-level field, just for the Puerto Jimenez / Bahia Drake pair ---
results_d = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="distrito")
binarized_d = binarize_votes(results_d, LEADING_PARTY, COALITION_PARTIES)
h_pj = float(binarized_d.set_index("code").loc[PJ_DISTRITO, "margin"])
h_drake = float(binarized_d.set_index("code").loc[DRAKE, "margin"])
print(f"Puerto Jimenez distrito h={h_pj:.3f}, Bahia Drake h={h_drake:.3f}")
print(f"(Recall: their coupling J_ij=8.19, one of the strongest edges in the distrito network.)")

gdf_d = load_shapefile(DISTRITO_SHAPEFILE, id_col=DISTRITO_COL)
gdf_d["code"] = [normalize_distrito_code(p, c, d)
                  for p, c, d in zip(gdf_d[PROVINCE_COL], gdf_d[CANTON_COL], gdf_d[DISTRITO_COL])]
gdf_d = gdf_d.set_index("code")

# --- Plot ---
exploded = gdf_c.reset_index().explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03

vmax = max(abs(gdf_c["h"].min()), abs(gdf_c["h"].max()))
norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
cmap = plt.get_cmap("RdBu_r")  # red = Pueblo Soberano (+1), blue = coalition (-1)

fig, ax = plt.subplots(figsize=(8, 8))
gdf_c.plot(column="h", cmap=cmap, norm=norm, ax=ax, edgecolor="black", linewidth=0.3)

for code, label, dx, dy in [
    (MONTES_DE_OCA, f"Montes de Oca\n$h={h_by_code[MONTES_DE_OCA]:.2f}$\n(most anti-incumbent)", -170000, 20000),
    (PJ_CANTON, f"Puerto Jiménez\n$h={h_by_code[PJ_CANTON]:.2f}$", 40000, -15000),
    (BUENOS_AIRES, f"Buenos Aires\n$h={h_by_code[BUENOS_AIRES]:.2f}$\n(most pro-incumbent)", -95000, -55000),
]:
    cx, cy = gdf_c.geometry[code].centroid.x, gdf_c.geometry[code].centroid.y
    ax.scatter([cx], [cy], s=90, facecolor="none", edgecolor="black", linewidth=1.6, zorder=5)
    ax.annotate(label, (cx, cy), xytext=(cx + dx, cy + dy), fontsize=7.5, ha="center",
                arrowprops=dict(arrowstyle="->", color="black", linewidth=0.8),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="black", linewidth=0.5, alpha=0.92),
                zorder=6)

ax.set_axis_off()
ax.set_aspect("equal")
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label(r"Field $h_i$ (own margin) $\to$ coalition $\quad\leftrightarrow\quad$ Pueblo Soberano $\leftarrow$")

# Inset: the Puerto Jimenez / Bahia Drake distrito pair -- strong J, correlated h.
# Only these two get highlighted borders/fill; neighbors render as plain
# background so the pair remains visually distinct despite similar h colors.
axins = fig.add_axes([0.06, 0.06, 0.34, 0.30])
gdf_d.plot(ax=axins, facecolor="#f2f2f2", edgecolor="#cccccc", linewidth=0.2)
gdf_d.loc[[PJ_DISTRITO]].plot(ax=axins, color=cmap(norm(h_pj)), edgecolor="black", linewidth=1.6)
gdf_d.loc[[DRAKE]].plot(ax=axins, color=cmap(norm(h_drake)), edgecolor="black", linewidth=1.6)
p1 = gdf_d.geometry[PJ_DISTRITO].centroid
p2 = gdf_d.geometry[DRAKE].centroid
axins.plot([p1.x, p2.x], [p1.y, p2.y], color="lime", linewidth=2.2, zorder=5)
axins.annotate("Puerto Jiménez", (p1.x, p1.y), fontsize=6.5, ha="center",
               xytext=(p1.x, p1.y - 6000), zorder=6)
axins.annotate("Bahía Drake", (p2.x, p2.y), fontsize=6.5, ha="center",
               xytext=(p2.x, p2.y + 4000), zorder=6)
axins.annotate(f"$J_{{ij}}=8.19$\n$h={h_pj:.2f}$ / $h={h_drake:.2f}$", ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2),
               xytext=(30, 30), textcoords="offset points", fontsize=7,
               arrowprops=dict(arrowstyle="-", color="black", linewidth=0.5),
               bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", linewidth=0.5, alpha=0.92))
bx0, by0, bx1, by1 = gdf_d.loc[[PJ_DISTRITO, DRAKE]].total_bounds
bpx, bpy = (bx1 - bx0) * 0.7, (by1 - by0) * 0.7
axins.set_xlim(bx0 - bpx, bx1 + bpx)
axins.set_ylim(by0 - bpy, by1 + bpy)
axins.set_xticks([])
axins.set_yticks([])
for spine in axins.spines.values():
    spine.set_visible(True)
    spine.set_edgecolor("black")
    spine.set_linewidth(1.2)
axins.set_title("Strong coupling, correlated field:\nPuerto Jiménez -- Bahía Drake", fontsize=7.5)

fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}")
