#!/usr/bin/env python3
"""Domain-wall map for the GAM field result (Section "Domain-wall structure,
counterfactual sensitivity, and cascade testing" of the manuscript): where
the geography+GAM model's per-distrito error concentrates, relative to the
GAM/periphery boundary and the canton-level proxy's known misclassification
risk (Section "Gran Area Metropolitana (GAM) membership": Mora, Alajuela's
central canton, Aserri, Paraiso over-included wholesale).

Referee finding (round-3 panel, minor point): the domain-wall subsection is
the most spatially-narrative-heavy new content but had no accompanying map,
unlike every comparable spatial claim in the original paper -- this script
produces that map so a reader can judge the proxy-imprecision exposure
directly, rather than take the "Mora" narrative on faith.

Reads the per-node error_rate/is_gam/is_boundary already computed and saved
by run_gam_domain_wall_analysis.py (data/processed/gam_domain_wall_analysis_
{year}.csv) -- no new Monte Carlo run needed. Two panels (2026, 2022),
matching plot_historical_maps.py's per-election-panel convention.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from isingcr.ingestion import load_shapefile, normalize_distrito_code

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "manuscript" / "figures" / "domain_wall_map.png"
SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin3.shp"
PROVINCE_COL, CANTON_COL, DISTRITO_COL = "adm1_name", "adm2_name", "adm3_name"

# Official Plan GAM 2013-2030 polygon (MIVAH GeoExplora), overlaid so the
# reader sees the proxy's decision boundary against the official one; the
# earlier "risk canton" overlay is superseded by that comparison (round 8).
GAM_POLYGON = DATA_RAW / "gam" / "gam_limite" / "GAM_LIMITE_1.shp"

YEARS = [
    {"label": "2026 (single round)", "csv": DATA_PROCESSED / "gam_domain_wall_analysis_2026.csv"},
    {"label": "2022 (runoff)", "csv": DATA_PROCESSED / "gam_domain_wall_analysis_2022.csv"},
]


def canton_of(node_code: str) -> str:
    parts = node_code.split("|")
    return parts[0] + "|" + parts[1]


gdf = load_shapefile(SHAPEFILE_PATH, id_col=DISTRITO_COL)
gam_poly = gpd.read_file(GAM_POLYGON).to_crs(gdf.crs)
gdf["code"] = [normalize_distrito_code(p, c, d)
               for p, c, d in zip(gdf[PROVINCE_COL], gdf[CANTON_COL], gdf[DISTRITO_COL])]

# Exclude the remote offshore Isla del Coco (part of Puntarenas canton's
# multipolygon) when computing the plot extent, so the mainland isn't
# squeezed into a corner of the figure -- same fix as plot_admin_map.py.
exploded = gdf.explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03
xlim = (minx - pad_x, maxx + pad_x)
ylim = (miny - pad_y, maxy + pad_y)

fig, axes = plt.subplots(1, 2, figsize=(12.5, 6.8))
cbar_ax = fig.add_axes([0.93, 0.15, 0.018, 0.68])  # shared vertical colorbar, right edge

for i, (ax, year) in enumerate(zip(axes, YEARS)):
    df = pd.read_csv(year["csv"]).rename(columns={"node": "code"})
    merged = gdf.merge(df, on="code", how="left")

    plot = merged.plot(ax=ax, column="error_rate", cmap="Reds", vmin=0, vmax=1,
                        edgecolor="#999999", linewidth=0.15,
                        missing_kwds={"color": "lightgray"})
    if i == 0:
        sm = plt.cm.ScalarMappable(cmap="Reds", norm=plt.matplotlib.colors.Normalize(vmin=0, vmax=1))
        fig.colorbar(sm, cax=cbar_ax, orientation="vertical",
                     label="per-node error rate (16 pooled seeds)")

    # GAM canton-level boundary: thick black outline around the union of
    # GAM cantons (the field's own decision boundary).
    gam_union = merged[merged["is_gam"] == True].dissolve()
    if len(gam_union):
        gam_union.boundary.plot(ax=ax, edgecolor="black", linewidth=1.3)

    # Official boundary, dashed, so the reader can see where the proxy's
    # decision boundary departs from the official polygon.
    gam_poly.boundary.plot(ax=ax, edgecolor="#1a6fb0", linewidth=1.1, linestyle="--")

    ax.set_title(year["label"], fontsize=11)
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

handles = [
    plt.matplotlib.lines.Line2D([0], [0], color="black", linewidth=1.3,
                                 label="GAM boundary (canton-level proxy)"),
    plt.matplotlib.lines.Line2D([0], [0], color="#1a6fb0", linewidth=1.1, linestyle="--",
                                 label="official GAM boundary (Plan GAM 2013–2030)"),
]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
           bbox_to_anchor=(0.46, 0.0), fontsize=9)

fig.tight_layout(rect=[0, 0.09, 0.91, 1])
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}")
