#!/usr/bin/env python3
"""Figure: the 31-canton GAM proxy against the official Plan GAM 2013-2030
polygon, with the distritos the proxy over-includes (area-majority outside
the polygon) and the proxy model's always-wrong distritos marked."""
import sys
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from isingcr.ingestion import load_shapefile
from isingcr.ingestion.canton_names import normalize_distrito_code, normalize_canton_code
from run_gam_field import GAM_CANTONS

fr = pd.read_csv(ROOT / "data" / "processed" / "gam_distrito_fraction_2026.csv")
err = pd.read_csv(ROOT / "data" / "processed" / "gam_domain_wall_analysis_2026.csv")[["node", "error_rate"]]
fr = fr.merge(err, on="node", how="left")
d = load_shapefile(ROOT / "data/raw/boundaries/extracted/cri_admin3.shp", id_col="adm3_name").to_crs(5367)
d["node"] = [normalize_distrito_code(p, c, x) for p, c, x in zip(d["adm1_name"], d["adm2_name"], d["adm3_name"])]
d = d.merge(fr, on="node", how="left")
c = load_shapefile(ROOT / "data/raw/boundaries/extracted/cri_admin2.shp", id_col="adm2_name").to_crs(5367)
c["code"] = [normalize_canton_code(p, x) for p, x in zip(c["adm1_name"], c["adm2_name"])]
gam = gpd.read_file(ROOT / "data/raw/gam/gam_limite/GAM_LIMITE_1.shp").to_crs(5367)
minx, miny, maxx, maxy = gam.total_bounds; pad = 12000

fig, ax = plt.subplots(figsize=(10, 6.6))
d.plot(ax=ax, facecolor="#f0eee8", edgecolor="#b5b5b5", linewidth=0.3)
d[d["proxy"] == True].plot(ax=ax, facecolor="#f4d9d4", edgecolor="#b5b5b5", linewidth=0.3)
d[(d["proxy"] == True) & (d["gam_majority"] == False)].plot(ax=ax, facecolor="#e08a2d", edgecolor="#8a5a1a", linewidth=0.5)
aw = d[(d["error_rate"] >= 0.999)]
aw.plot(ax=ax, facecolor="none", edgecolor="#1f4e79", hatch="////", linewidth=0.5)
c[c["code"].isin(GAM_CANTONS)].dissolve().boundary.plot(ax=ax, edgecolor="#8a2e26", linewidth=1.4, linestyle="--")
gam.boundary.plot(ax=ax, edgecolor="black", linewidth=1.8)
for name, code in [("Alajuela", "ALAJUELA|CENTRAL"), ("Mora", "SAN JOSE|MORA"), ("Aserrí", "SAN JOSE|ASERRI"), ("Paraíso", "CARTAGO|PARAISO"), ("Atenas", "ALAJUELA|ATENAS"), ("Desamparados", "SAN JOSE|DESAMPARADOS")]:
    g = c[c["code"] == code].geometry.iloc[0]; p = g.representative_point()
    ax.annotate(name, (p.x, p.y), ha="center", va="center", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
ax.set_xlim(minx - pad, maxx + pad); ax.set_ylim(miny - pad, maxy + pad); ax.set_axis_off(); ax.set_aspect("equal")
x0, y0 = minx - pad + 4000, miny - pad + 4000
ax.plot([x0, x0 + 20000], [y0, y0], color="black", lw=2.5); ax.text(x0 + 10000, y0 + 1500, "20 km", ha="center", fontsize=8)
ax.legend(handles=[Line2D([0], [0], color="black", lw=1.8, label="official GAM polygon (Plan GAM 2013--2030)"),
                   Line2D([0], [0], color="#8a2e26", lw=1.4, ls="--", label="31-canton proxy boundary"),
                   Patch(facecolor="#f4d9d4", edgecolor="#b5b5b5", label="proxy GAM distrito (186)"),
                   Patch(facecolor="#e08a2d", edgecolor="#8a5a1a", label="proxy distrito with area-majority outside the polygon (24)"),
                   Patch(facecolor="none", edgecolor="#1f4e79", hatch="////", label="always wrong under the proxy model (all 16 seeds)")],
          loc="lower right", fontsize=8, framealpha=0.92)
fig.tight_layout(); out = ROOT / "manuscript" / "figures" / "gam_boundary_comparison.png"; fig.savefig(out, dpi=300, bbox_inches="tight"); print("wrote", out)
# breakdown for the text
po = fr[(fr.proxy) & (~fr.gam_majority)]
lead = 1 if (fr.empirical == 1).mean() > 0.5 else -1
print(f"proxy-only (24): on leading side {np.mean(po.empirical==lead):.0%}, mean proxy-model error {po.error_rate.mean():.2f}, always-wrong {int((po.error_rate>=0.999).sum())}")
inside = fr[fr.gam_majority]
print(f"true GAM (162): on leading side {np.mean(inside.empirical==lead):.1%}, mean error {inside.error_rate.mean():.2f}")
ala = fr[fr.node.str.startswith("ALAJUELA|CENTRAL")]
print(f"Alajuela Central: {len(ala)} distritos, area-majority inside {int(ala.gam_majority.sum())}, fully inside(>=0.99) {int((ala.frac_in_gam>=0.99).sum())}, on leading side {np.mean(ala.empirical==lead):.0%}, always-wrong {int((ala.error_rate>=0.999).sum())}")
print(po[["node","frac_in_gam","error_rate"]].sort_values("frac_in_gam").to_string())
