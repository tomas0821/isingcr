#!/usr/bin/env python3
"""Run the full pipeline on real TSE results + real canton boundaries.

TSE side: data/raw/tse_juntas/, the official per-junta "escrutinio definitivo"
exports, loaded via load_tse_juntas_consolidado. Verified against TSE's own
published national totals.

Boundary side: data/raw/boundaries/, Costa Rica's admin2 (canton) layer from
UN OCHA's Humanitarian Data Exchange COD-AB dataset
(https://data.humdata.org/dataset/cod-ab-cri) -- TSE's own site blocks
scripted downloads with a CAPTCHA, and SNIT's WFS needs a signed session token
we couldn't obtain non-interactively, so this is a third-party source rather
than straight from IGN/TSE. Matches the real TSE canton list for 78/84
cantons directly; the other 6 are each province's capital canton, which this
boundary file names after the province (e.g. canton "San Jose") while TSE
calls it "CENTRAL" -- normalize_canton_code() reconciles that.

Set SKIP_SHAPEFILE=1 to run just the TSE loading/binarization step.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.ingestion import (
    binarize_votes,
    build_adjacency_graph,
    build_electoral_graph,
    load_shapefile,
    load_tse_juntas_consolidado,
    normalize_canton_code,
)
from isingcr.simulation.monte_carlo import temperature_scan
from isingcr.utils.graph_arrays import graph_to_arrays
from isingcr.visualization.maps import plot_comparison_map
from isingcr.visualization.plots import plot_alignment_curve, plot_phase_diagram

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"

SHAPEFILE_PATH = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
PROVINCE_COL = "adm1_name"
CANTON_COL = "adm2_name"

# EDITORIAL CHOICE, not a technical default -- this is a modeling decision, not
# neutral data processing. PUEBLO SOBERANO (2026 winner, 48.5% nationally) vs.
# a coalition of the next three largest parties (LIBERACION NACIONAL 33.65%,
# COALICION AGENDA CIUDADANA 4.91%, FRENTE AMPLIO 3.76% -- the only other
# parties that cleared ~4%). The other ~16 parties are left out of both
# buckets: individually too small (each well under 3%) to meaningfully call
# part of "the coalition". This gives a much more balanced canton split than
# an ideological traditional-vs-emerging framing would for this election (see
# README's alignment-score caveat) -- reconsider before treating any output as
# a real analysis. See binarize_votes' `margin` column for a continuous
# alternative that avoids choosing a binary split at all.
LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)

    results = load_tse_juntas_consolidado(TSE_RESULTS_ZIP, member=TSE_MEMBER, level="canton")
    binarized = binarize_votes(results, LEADING_PARTY, COALITION_PARTIES)

    if os.environ.get("SKIP_SHAPEFILE"):
        print(binarized["spin"].value_counts())
        print(f"{len(binarized)} cantons loaded and binarized; "
              f"unset SKIP_SHAPEFILE to run the full pipeline.")
        return

    gdf = load_shapefile(SHAPEFILE_PATH, id_col=CANTON_COL)
    gdf["code"] = [normalize_canton_code(p, c)
                   for p, c in zip(gdf[PROVINCE_COL], gdf[CANTON_COL])]
    adjacency = build_adjacency_graph(gdf, id_col="code", weight_by="border_length")

    # h_i from vote margin, not left at 0 -- see README "A physics note": with
    # h=0 the model's up/down symmetry makes "traditional" vs "emerging" an
    # arbitrary label below the ordering temperature.
    G = build_electoral_graph(adjacency, binarized, code_col="code", h_col="margin")
    arrays = graph_to_arrays(G)
    J, h, nodes, empirical = arrays["J"], arrays["h"], arrays["nodes"], arrays["spin_empirical"]
    print(f"{J.shape[0]} cantons, {J.nnz // 2} adjacency edges")

    temperatures = np.linspace(0.1, 4.0, 25)
    scan = temperature_scan(J, h, temperatures, n_equil=500, n_sweeps=500,
                             dynamics="glauber", seed=7, n_jobs=4)

    plot_phase_diagram(scan, N=J.shape[0], savepath=FIGURES_DIR / "phase_diagram_real.png")
    plot_alignment_curve(scan, empirical, savepath=FIGURES_DIR / "alignment_curve_real.png")

    accuracies = [np.mean(r["final_spins"] == empirical) for r in scan]
    best_idx = int(np.argmax(accuracies))
    best = scan[best_idx]
    print(f"Best empirical alignment at T = {temperatures[best_idx]:.3g} "
          f"({accuracies[best_idx]:.1%} match)")

    sim_by_code = dict(zip(nodes, best["final_spins"]))
    gdf_annotated = gdf.merge(_graph_to_frame(G), on="code", how="inner")
    plot_comparison_map(gdf_annotated, id_col="code", simulated_spins=sim_by_code,
                         savepath=FIGURES_DIR / "map_comparison_real.png")
    print(f"Figures written to {FIGURES_DIR}")


def _graph_to_frame(G):
    import pandas as pd
    return pd.DataFrame(
        {"code": n, "spin_empirical": d["spin_empirical"]} for n, d in G.nodes(data=True)
    )


if __name__ == "__main__":
    main()
