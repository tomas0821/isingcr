#!/usr/bin/env python3
"""Louvain community detection on the canton-level coupling network J_ij --
computed from geography alone, with no vote/political data of any kind --
compared against the two administrative/political partitions the rest of
the paper actually uses (the 7 official provinces, and GAM/periphery).

Answers a question the electoral data alone cannot: does the geographic
coupling structure this paper's model is built on imply its own "natural"
regions, and if so, do they look like the country's actual administrative
map, or something else entirely?
"""
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.stats import entropy

from isingcr.ingestion import build_adjacency_graph, load_shapefile, normalize_canton_code

DATA_RAW = ROOT / "data" / "raw"
OUT = ROOT / "manuscript" / "figures" / "community_detection.png"

SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL, CANTON_COL = "adm1_name", "adm2_name"

GAM_CANTONS = {
    "SAN JOSE|CENTRAL", "SAN JOSE|ESCAZU", "SAN JOSE|DESAMPARADOS", "SAN JOSE|ASERRI",
    "SAN JOSE|MORA", "SAN JOSE|GOICOECHEA", "SAN JOSE|SANTA ANA", "SAN JOSE|ALAJUELITA",
    "SAN JOSE|VAZQUEZ DE CORONADO", "SAN JOSE|TIBAS", "SAN JOSE|MORAVIA",
    "SAN JOSE|MONTES DE OCA", "SAN JOSE|CURRIDABAT",
    "ALAJUELA|CENTRAL", "ALAJUELA|ATENAS", "ALAJUELA|POAS",
    "CARTAGO|CENTRAL", "CARTAGO|PARAISO", "CARTAGO|LA UNION", "CARTAGO|OREAMUNO",
    "CARTAGO|ALVARADO", "CARTAGO|EL GUARCO",
    "HEREDIA|CENTRAL", "HEREDIA|BARVA", "HEREDIA|SANTO DOMINGO", "HEREDIA|SANTA BARBARA",
    "HEREDIA|SAN RAFAEL", "HEREDIA|SAN ISIDRO", "HEREDIA|BELEN", "HEREDIA|FLORES",
    "HEREDIA|SAN PABLO",
}


def nmi(labels_a, labels_b):
    a_vals, a_idx = np.unique(labels_a, return_inverse=True)
    b_vals, b_idx = np.unique(labels_b, return_inverse=True)
    contingency = np.zeros((len(a_vals), len(b_vals)))
    for i, j in zip(a_idx, b_idx):
        contingency[i, j] += 1
    n = contingency.sum()
    pxy = contingency / n
    px, py = pxy.sum(axis=1), pxy.sum(axis=0)
    mi = sum(pxy[i, j] * np.log(pxy[i, j] / (px[i] * py[j]))
             for i in range(len(a_vals)) for j in range(len(b_vals)) if pxy[i, j] > 0)
    hx, hy = entropy(px), entropy(py)
    return mi / np.sqrt(hx * hy) if hx > 0 and hy > 0 else float("nan")


gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
G = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

comms = nx.algorithms.community.louvain_communities(G, weight="weight", seed=42, resolution=1.0)
modularity = nx.algorithms.community.modularity(G, comms, weight="weight")
comm_of = {n: i for i, c in enumerate(comms) for n in c}
print(f"{len(comms)} communities, modularity={modularity:.4f}")

gdf = gdf.set_index("code")
province_of = gdf[PROVINCE_COL].to_dict()
nodes = list(G.nodes)
comm_labels = np.array([comm_of[n] for n in nodes])
prov_labels = np.array([province_of[n] for n in nodes])
gam_labels = np.array([n in GAM_CANTONS for n in nodes])

nmi_prov = nmi(comm_labels, prov_labels)
nmi_gam = nmi(comm_labels, gam_labels)
print(f"NMI(community, province) = {nmi_prov:.3f}")
print(f"NMI(community, GAM) = {nmi_gam:.3f}")

purity_prov = sum(Counter(prov_labels[comm_labels == i]).most_common(1)[0][1] for i in range(len(comms))) / len(nodes)
purity_gam = sum(Counter(gam_labels[comm_labels == i]).most_common(1)[0][1] for i in range(len(comms))) / len(nodes)
print(f"Province purity = {purity_prov:.3f}, GAM purity = {purity_gam:.3f}")

gdf["community"] = [comm_of[c] for c in gdf.index]

exploded = gdf.reset_index().explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03

fig, axes = plt.subplots(1, 2, figsize=(14, 8))

cmap = plt.get_cmap("tab10")
ax = axes[0]
gdf.plot(ax=ax, column="community", cmap=cmap, categorical=True, edgecolor="black", linewidth=0.4)
gdf.dissolve(by=PROVINCE_COL).boundary.plot(ax=ax, edgecolor="white", linewidth=1.8)
gdf.dissolve(by=PROVINCE_COL).boundary.plot(ax=ax, edgecolor="black", linewidth=0.9, linestyle="--")
ax.set_title(f"{len(comms)} communities from $J_{{ij}}$ alone\n(dashed: the 7 official provinces)", fontsize=10)
ax.set_axis_off()
ax.set_aspect("equal")
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)

ax = axes[1]
gam_color = gdf.index.map(lambda c: "tab:red" if c in GAM_CANTONS else "#dddddd")
gdf.plot(ax=ax, color=gam_color, edgecolor="black", linewidth=0.4)
for i, comm in enumerate(comms):
    sub = gdf.loc[list(comm)]
    sub_dissolved = sub.dissolve()
    sub_dissolved.boundary.plot(ax=ax, edgecolor=cmap(i), linewidth=2.0)
ax.set_title("Same communities (colored outlines) vs.\nGAM (red) / periphery (gray)", fontsize=10)
ax.set_axis_off()
ax.set_aspect("equal")
ax.set_xlim(minx - pad_x, maxx + pad_x)
ax.set_ylim(miny - pad_y, maxy + pad_y)

fig.suptitle(f"NMI(community, province) = {nmi_prov:.2f}     NMI(community, GAM) = {nmi_gam:.2f}", fontsize=11)
fig.tight_layout()
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}")
