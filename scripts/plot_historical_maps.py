#!/usr/bin/env python3
"""Canton-level winner-vs-runner-up maps for 2018/2022/2026 -- the same
binarization used in run_historical_comparison.py / Section 4.3 of the
manuscript, plotted directly from the real TSE results (no simulation)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/home/tomas/mnt/gdrive/Research/Current/IsingCR/src")))

import matplotlib.pyplot as plt
from isingcr.ingestion import (
    binarize_votes, load_shapefile, load_tse_juntas_consolidado, normalize_canton_code,
)

DATA_RAW = Path("/home/tomas/mnt/gdrive/Research/Current/IsingCR/data/raw")
OUT = Path("/home/tomas/mnt/gdrive/Research/Current/IsingCR/manuscript/figures/historical_maps.png")
SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL, CANTON_COL = "adm1_name", "adm2_name"

TSE_JUNTAS = DATA_RAW / "tse_juntas"
ELECTIONS = [
    {
        "label": "2018 (runoff)",
        "zip": TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2018.zip",
        "member": "ronda2/_consolidado_presidenciales.csv",
        "rename": {"ALAJUELA|VALVERDE VEGA": "ALAJUELA|SARCHI"},
    },
    {
        "label": "2022 (runoff)",
        "zip": TSE_JUNTAS / "juntas_TSE_2022_ronda2_provisional_y_definitivo.zip",
        "member": "_consolidado_definitivo.csv",
        "rename": {},
    },
    {
        "label": "2026 (round 1)",
        "zip": TSE_JUNTAS / "DEFINITIVO_juntas_TSE_2026.zip",
        "member": "_consolidado_presidenciales.csv",
        "rename": {},
    },
]

WINNER_COLOR = "#7a1f2b"   # maroon, matches map_comparison_real.png's minority/leading-party color
RUNNERUP_COLOR = "#2b5f8a"  # blue, matches map_comparison_real.png's majority-coalition color


def _top_two_parties(results, party_cols):
    totals = results[party_cols].sum().sort_values(ascending=False)
    return totals.index[0], totals.index[1]


def _title_case(party):
    return " ".join(w.capitalize() for w in party.split())


gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
gdf["code"] = [normalize_canton_code(p, c) for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]

# Exclude the remote offshore Isla del Coco (part of Puntarenas canton's
# multipolygon, ~500km from the mainland) when computing the plot extent.
exploded = gdf.explode(index_parts=False)
mainland = exploded[exploded.geometry.bounds["minx"] > 200000]
minx, miny, maxx, maxy = mainland.total_bounds
pad_x, pad_y = (maxx - minx) * 0.03, (maxy - miny) * 0.03
xlim = (minx - pad_x, maxx + pad_x)
ylim = (miny - pad_y, maxy + pad_y)

fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

for ax, election in zip(axes, ELECTIONS):
    results = load_tse_juntas_consolidado(election["zip"], member=election["member"], level="canton")
    for old, new in election["rename"].items():
        results.loc[results["code"] == old, "code"] = new

    party_cols = [c for c in results.columns
                  if c not in ("code", "name", "provincia_pais", "canton_ciudad")]
    winner, runner_up = _top_two_parties(results, party_cols)
    binarized = binarize_votes(results, [winner], [runner_up])

    merged = gdf.merge(binarized, on="code", how="left")
    merged.plot(ax=ax, column="spin", categorical=True,
                cmap=plt.matplotlib.colors.ListedColormap([RUNNERUP_COLOR, WINNER_COLOR]),
                edgecolor="white", linewidth=0.4, missing_kwds={"color": "lightgray"})

    n_winner = int((binarized["spin"] == 1).sum())
    n_total = len(binarized)
    ax.set_title(f"{election['label']}\n{_title_case(winner)} ({n_winner}/{n_total} cantons)\n"
                 f"vs. {_title_case(runner_up)}", fontsize=10)
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

fig.tight_layout()
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(f"wrote {OUT}")
