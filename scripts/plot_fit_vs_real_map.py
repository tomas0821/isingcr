#!/usr/bin/env python3
"""Figure: the real 2026 distrito map beside the fitted geography+GAM
equilibrium (canton proxy, unit weight, T=1.008, 16 seeds), the paper's
headline result drawn as a map. Left: empirical winner per distrito. Right:
seed-majority equilibrium spin; distritos where the fit disagrees with the
returns are hatched. Reads the per-seed site means from
gam_diagnostics_timeavg_2026.npz (sign<s_i> over the measurement sweeps) if
present, else the end-of-run snapshots saved by run_true_gam_paired_test.py."""
import sys
from pathlib import Path
import numpy as np, geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from isingcr.ingestion import load_shapefile
from isingcr.ingestion.canton_names import normalize_distrito_code, normalize_canton_code
from run_gam_field import GAM_CANTONS
P = ROOT / "data" / "processed"

f = P / "gam_diagnostics_timeavg_2026.npz"
if f.exists():
    z = np.load(f, allow_pickle=True); nodes, emp = z["nodes"], z["emp"]
    S = np.where(z["means_proxy"] >= 0, 1, -1); how = "seed-majority sign<s_i>"
else:
    z = np.load(P / "true_gam_paired_test_any_lam1_2026.npz", allow_pickle=True)
    from run_gam_true_field import build_true_field
    _, _, nodes, emp, _ = build_true_field("any", verbose=False); nodes = np.asarray(nodes)
    S = z["spins_proxy"]; how = "seed-majority snapshot"
fit = np.where(S.sum(0) >= 0, 1, -1)
print(f"fitted map ({how}): alignment of majority map {np.mean(fit == emp):.4%}")

d = load_shapefile(ROOT / "data/raw/boundaries/extracted/cri_admin3.shp", id_col="adm3_name").to_crs(5367)
d["node"] = [normalize_distrito_code(p, c, x) for p, c, x in zip(d["adm1_name"], d["adm2_name"], d["adm3_name"])]
val = dict(zip(nodes, emp)); fv = dict(zip(nodes, fit))
d["emp"] = d["node"].map(val); d["fit"] = d["node"].map(fv)
c = load_shapefile(ROOT / "data/raw/boundaries/extracted/cri_admin2.shp", id_col="adm2_name").to_crs(5367)
c["code"] = [normalize_canton_code(p, x) for p, x in zip(c["adm1_name"], c["adm2_name"])]
gam_outline = c[c["code"].isin(GAM_CANTONS)].dissolve().boundary
ex = d.explode(index_parts=False); ml = ex[ex.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = ml.total_bounds; px, py = (maxx - minx) * 0.02, (maxy - miny) * 0.02
LEAD, COAL = "#7a1f2b", "#2b5f8a"

fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
for ax, col, title in zip(axes, ("emp", "fit"), ("2026 returns (single round)", "fitted equilibrium, geography + GAM field")):
    d.plot(ax=ax, color="lightgray", edgecolor="white", linewidth=0.2)
    d[d[col] == 1].plot(ax=ax, color=LEAD, edgecolor="white", linewidth=0.2)
    d[d[col] == -1].plot(ax=ax, color=COAL, edgecolor="white", linewidth=0.2)
    if col == "fit":
        d[(d["fit"].notna()) & (d["fit"] != d["emp"])].plot(ax=ax, facecolor="none", edgecolor="black", hatch="////", linewidth=0.3)
    gam_outline.plot(ax=ax, edgecolor="black", linewidth=1.2)
    ax.set_title(title, fontsize=11); ax.set_axis_off(); ax.set_aspect("equal")
    ax.set_xlim(minx - px, maxx + px); ax.set_ylim(miny - py, maxy + py)
fig.legend(handles=[Patch(facecolor=LEAD, label="Pueblo Soberano"), Patch(facecolor=COAL, label="coalition of the next three parties"),
                    Line2D([0], [0], color="black", lw=1.2, label="GAM (canton proxy)"),
                    Patch(facecolor="none", edgecolor="black", hatch="////", label="fit disagrees with returns")],
           loc="lower center", ncol=4, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=[0, 0.06, 1, 1])
out = ROOT / "manuscript" / "figures" / "fit_vs_real_map.png"; fig.savefig(out, dpi=300, bbox_inches="tight"); print("wrote", out)
