# IsingCR

Simulation code, processed networks and result files for

> T. Rojas, *Capital-region membership as an Ising field: geography, predisposition
> and spatial resolution in Costa Rican presidential elections*, submitted to
> Physica A (2026).

The paper fits an Ising model by Glauber Monte Carlo on Costa Rica's real
border-adjacency network, with cantons (N = 84) or distritos (N = 488) as spins,
shared border length as the coupling, and a local predisposition field, to the
2018, 2022 and 2026 presidential results. Its two findings:

- **The geography-versus-predisposition answer depends on resolution.** A unit's
  own vote margin as field adds +1.2 points of alignment at canton level but
  +8.7 to +11.6 at distrito level.
- **Membership in the Gran Área Metropolitana (GAM), the capital region, is the
  independent field that carries the 2026 map.** At unit weight it reproduces 81%
  of distritos (+13.4 points over geography alone, paired spatial-block
  p < 0.001), beats an equally correlated development index at every weight, and
  is reproduced by the official distrito-level GAM boundary. The model's one
  regional failure, Alajuela's central canton, lies inside the metropolitan
  region yet votes with the periphery.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22680955.svg)](https://doi.org/10.5281/zenodo.22680955)

The manuscript itself is versioned separately. Every number in it was produced
at the release tagged `v1.1-submission` in this repository, archived at
[doi:10.5281/zenodo.22680955](https://doi.org/10.5281/zenodo.22680955)
(concept DOI for all versions: 10.5281/zenodo.22680096).

## Layout

```
src/isingcr/
  simulation/      IsingModel, Metropolis/Glauber dynamics, temperature scans,
                   observables, McNemar and paired spatial-block tests
                   (pure numpy/scipy; no pandas/networkx/geopandas imports)
  ingestion/       TSE per-junta results, binarization, shapefile adjacency,
                   canton/distrito name reconciliation, MIDEPLAN IDS, GAM membership
  utils/           graph_arrays.py: the single nx.Graph -> (J, h) conversion point
  visualization/   phase diagrams and map comparisons
scripts/           one script per analysis (see the reproduction map below)
                   plus the SLURM submission files used on the UCR cluster
data/processed/    every .npz / .csv result the paper reports (tracked)
processed_networks/  J, h and empirical spins for the canton and distrito networks
data/raw/          TSE exports and boundary shapefiles (not tracked; see below),
                   plus the official GAM boundary polygon (tracked, with provenance)
docs/NOTES.md      development notes: what each script established and the
                   pitfalls found along the way
00_Master_Notebook.md  run-by-run log with the numbers behind every result
NOVELTY_CHECK.md   the prior-art check
tests/             68 tests
```

## Reproducing the paper

All main-text figures and tables, the script that produces the underlying
numbers, and the plotting or table script. Result files live in
`data/processed/` unless noted. Runs marked *cluster* were done on the UCR HPC
cluster (32 cores, 16 seeds, 32 temperatures, 20 000 equilibration and 20 000
measurement sweeps) with the SLURM file of the same name; everything else runs
on a laptop in seconds to about an hour.

| Item | Numbers | Figure / table |
|---|---|---|
| Fig. 1, administrative map | — | `plot_admin_map.py` |
| Fig. 2, resolution reversal | `run_ablation.py` (canton, `ablation.npz`); `run_distrito_ablation.py` (*cluster*, `distrito_ablation.npz`) | `plot_resolution_reversal.py` |
| Fig. 3 and Table 1, three elections | `run_historical_comparison.py`; `investigate_2018_anomaly.py` for the 2018 energetics | `plot_historical_maps.py` |
| Fig. 4 and the GAM headline (Section 4.6) | `run_gam_field.py` (*cluster*); paired test `run_gam_paired_test_highres.py`; province hold-out `run_gam_spatial_cv.py`; population confound `registered_voters.py` | `plot_fit_vs_real_map.py` |
| Fig. 5, field-weight scans | `run_gam_lambda_scan.py`, `run_prior_lambda_scan.py`, `run_gam_residual_field.py` (all *cluster*); `prior_lambda_scan_analysis.py`, `run_prior_paired_test_at_lambda.py`, `run_resid_paired_test.py` | `plot_gam_lambda_scan.py` |
| Table 2 and Fig. 6, official GAM boundary (Section 4.7) | `run_gam_true_field.py` (*cluster*), `run_true_gam_paired_test.py`, `run_true_gam_spatial_cv.py`, `run_official_readings_head_to_head.py` | `plot_gam_boundary_comparison.py`, `make_gam_boundary_table.py` |
| Regression baselines (Section 4.8) | `run_regression_baselines.py` | — |
| IDS and political fields (Section 4.5) | `run_3d_scan.py`, `run_3d_scan_2022.py`, `run_mideplan_axis_screen.py`, `run_prior_margin_field.py` (*cluster*); `analyze_3d_scan.py`, `run_soc_paired_test.py`, `run_axis_paired_test.py`, `gam_vs_ids_field_shape.py` | — |
| Multistability, counterfactual sweep, cascades (Sections 4.9, 4.10) | `run_gam_counterfactual_sweep.py` (*cluster*), `run_gam_cascade_analysis.py`, `run_gam_susceptibility_scan.py` (*cluster*), `run_gam_diagnostics_timeavg.py` (time-averaged spins, proxy and official fields) | `make_contested_distrito_tables.py` |
| Fig. 7, domain walls | `run_gam_domain_wall_analysis.py`, `run_domain_wall_topology_checks.py`, `run_gam_polarization_trend.py` | `plot_domain_wall_map.py` |
| Table 3, which results survive | the paired tests above plus `run_direct_paired_test.py`, `run_spatial_block_sensitivity.py` | — |
| Supplementary: Binder cumulant, subsampling, binarization checks, community detection | `run_finite_size_scaling_heavy.py` (*cluster*), `run_distrito_subsample_check.py`, `run_distrito_contiguous_subsample_check.py`, `run_ablation_wvru.py`, `run_distrito_ablation_wvru.py`, `run_spatial_robustness_check.py`, `run_energy_decomposition.py` | `plot_fss_replot.py`, `plot_community_detection*.py`, `plot_coupling_weights*.py`, `plot_field_values.py` |

Scripts read from `data/raw/` and write to `data/processed/` and
`manuscript/figures/`; each one's module docstring states its inputs, its
settings and the result it established. Plotting and table scripts need only
the tracked `data/processed/` files, so every figure can be regenerated without
re-running any Monte Carlo.

## Installation

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .
.venv/bin/pytest tests/ -q
```

geopandas needs GDAL, GEOS and PROJ; on Debian or Ubuntu install
`gdal-bin libgdal-dev libgeos-dev libproj-dev` first, or use the Docker image:

```bash
docker compose build
docker compose run --rm isingcr      # runs scripts/run_demo.py on synthetic data
```

## Data

**Election results.** The Tribunal Supremo de Elecciones publishes per-junta
"resultados por junta receptora de votos" exports for every election. Its site
sits behind bot protection, so the ZIPs in `data/raw/tse_juntas/` were
downloaded by hand from tse.go.cr and are not redistributed here; the loader
`isingcr.ingestion.load_tse_juntas_consolidado` reads the pre-aggregated
`_consolidado_*.csv` member of each ZIP, keeps only `tipo_territorio =
"NACIONAL"` (juntas abroad have no geographic adjacency), aggregates to canton
or distrito, and pivots parties into columns. Totals were verified against
TSE's published national figures. Note that 2018 reports a different
"distrito electoral" unit than the administrative distrito of 2022 and 2026;
canton level matches across all three years.

**Boundaries.** Canton (`cri_admin2.shp`) and distrito (`cri_admin3.shp`)
geometry come from UN OCHA's Humanitarian Data Exchange
([COD-AB Costa Rica](https://data.humdata.org/dataset/cod-ab-cri)), placed in
`data/raw/boundaries/`. Names are reconciled with TSE's conventions by
`isingcr.ingestion.canton_names` (each province's capital canton is "CENTRAL"
in TSE files; "Ñ" is a distinct letter). All 84 cantons and 490 of 492
distritos match; two alternate-name distritos are dropped. The official
cadastral CRS, CRTM05 (EPSG:5367), is applied on load.

**GAM boundary.** `data/raw/gam/` holds the Plan GAM 2013–2030 polygon
("GAM LIMITE 1") from MIVAH's GeoExplora open-data portal, with a README on
provenance, together with the derived per-distrito area fractions in
`data/processed/gam_distrito_fraction_2026.csv`.

**Social Development Index.** MIDEPLAN's IDS 2023 regional exports (public,
mideplan.go.cr) are parsed by `scripts/parse_mideplan_ids.py` into
`data/raw/mideplan_ids_2023.csv`; like the TSE ZIPs they are not tracked here,
but every derived result file is.

## A physics note

With `h = 0` everywhere the Hamiltonian has an exact up/down symmetry, so which
of the two ordered states a run lands in is arbitrary. Geography-only runs are
therefore scored with the symmetric alignment
`max(fraction_matching, 1 - fraction_matching)`, and every run that supports a
claim pools independent seeds per temperature
(`isingcr.simulation.monte_carlo.pooled_temperature_scan`): single-seed scans
produced both a spurious alignment gap and spurious susceptibility peaks early in
this project, which is why the pooled protocol is the standing rule
(`docs/NOTES.md`).

## Tests

```bash
.venv/bin/pytest tests/ -q
```

The 68 tests cover the Ising energy and dynamics bookkeeping (a brute-force
check that incremental flips match a full recomputation), equilibrium limits,
temperature scans, the McNemar and Moran's I statistics, the TSE loaders and
name reconciliation, vote binarization, shapefile adjacency on synthetic
polygon grids, the graph-to-array conversion and the synthetic data generator.

## License

MIT (see `LICENSE`). Electoral results are public data of the Tribunal Supremo
de Elecciones; boundary geometry is distributed by UN OCHA under its own terms;
the GAM polygon is MIVAH open data.
