#!/usr/bin/env python3
"""Figure 1: Costa Rica's canton (N=84) and distrito (N=492) geometry, with
province outlines and labels, the 31-canton GAM proxy (the field's own
boundary) and a scale bar, so every later map can be located."""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from isingcr.ingestion import load_shapefile
from isingcr.ingestion.canton_names import normalize_canton_code
from run_gam_field import GAM_CANTONS

DATA_RAW = ROOT / "data" / "raw"
OUT = ROOT / "manuscript" / "figures" / "admin_map.png"

canton = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp", id_col="adm2_name")
distrito = load_shapefile(DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp", id_col="adm3_name")
canton["code"] = [normalize_canton_code(p, c) for p, c in zip(canton["adm1_name"], canton["adm2_name"])]
canton["is_gam"] = canton["code"].isin(GAM_CANTONS)
assert canton["is_gam"].sum() == 31, canton["is_gam"].sum()

exploded = canton.explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03

fig, ax = plt.subplots(figsize=(10, 7.2))
distrito.plot(ax=ax, facecolor="#e9eef4", edgecolor="#9a9a9a", linewidth=0.25)
gam = canton[canton["is_gam"]].dissolve()
gam.plot(ax=ax, facecolor="#f2c9c2", edgecolor="none", alpha=0.85)
distrito.plot(ax=ax, facecolor="none", edgecolor="#9a9a9a", linewidth=0.25)
canton.plot(ax=ax, facecolor="none", edgecolor="#333333", linewidth=0.6)
prov = canton.dissolve(by="adm1_name")
prov.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=1.6)
gam.boundary.plot(ax=ax, edgecolor="#b23a2d", linewidth=1.8)

# province labels at representative interior points (mainland only)
labels = {"San José": "San José", "Alajuela": "Alajuela", "Cartago": "Cartago", "Heredia": "Heredia",
          "Guanacaste": "Guanacaste", "Puntarenas": "Puntarenas", "Limón": "Limón"}
for name, geom in prov.geometry.items():
    parts = [g for g in getattr(geom, "geoms", [geom]) if g.bounds[0] > 200000]
    big = max(parts, key=lambda g: g.area)
    pt = big.representative_point()
    key = name.title()
    txt = labels.get(key, key)
    dx, dy = 0, 0
    if key == "Heredia": dx, dy = 0, 12000
    if key == "San José": dx, dy = 8000, -18000
    if key == "Cartago": dx, dy = 12000, -8000
    ax.annotate(txt, (pt.x + dx, pt.y + dy), ha="center", va="center", fontsize=11, fontweight="bold",
                color="#111111", path_effects=None,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))

# scale bar: 50 km (CRTM05 is metric)
x0, y0 = minx + (maxx - minx) * 0.04, miny + (maxy - miny) * 0.06
ax.plot([x0, x0 + 50000], [y0, y0], color="black", linewidth=2.5)
ax.text(x0 + 25000, y0 + 4000, "50 km", ha="center", va="bottom", fontsize=9)

ax.legend(handles=[Line2D([0], [0], color="black", lw=1.6, label="province (7)"),
                   Line2D([0], [0], color="#333333", lw=0.6, label=f"canton ({len(canton)})"),
                   Line2D([0], [0], color="#9a9a9a", lw=0.5, label=f"distrito ({len(distrito)})"),
                   Patch(facecolor="#f2c9c2", edgecolor="#b23a2d", lw=1.5, label="GAM, canton-level proxy (31 cantons)")],
          loc="upper right", fontsize=9, frameon=True, framealpha=0.9)
ax.set_axis_off(); ax.set_aspect("equal")
ax.set_xlim(minx - pad_x, maxx + pad_x); ax.set_ylim(miny - pad_y, maxy + pad_y)
fig.tight_layout()
fig.savefig(OUT, dpi=300, bbox_inches="tight")
print(f"wrote {OUT}: cantons {len(canton)}, distritos {len(distrito)}, GAM cantons {int(canton['is_gam'].sum())}")
