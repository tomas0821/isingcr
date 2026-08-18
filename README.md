# IsingCR — simulation code and processed networks

Code and processed adjacency networks for "Geography versus Predisposition
in Costa Rican Presidential Elections: A Real-Network Ising Model Across
Spatial Scales, with a Historical Comparison Across Election Cycles"
(manuscript: https://github.com/tomas0821/isingcr-manuscript).

## What's here

- `src/isingcr/` — the simulation package. `simulation/` (pure numpy/scipy:
  the Ising model, Glauber/Metropolis Monte Carlo, thermodynamic observables,
  significance tests) is kept free of `ingestion/`'s pandas/networkx/geopandas
  dependencies by design, so the MC engine can be dropped onto an HPC backend
  without dragging ingestion deps along.
- `scripts/` — the analysis scripts behind every result in the paper (see
  each script's docstring for what it does and which manuscript section it
  supports).
- `tests/` — the test suite (`pytest tests/ -q`).
- `processed_networks/*.npz` — the exact `J` (sparse coupling matrix), `h`
  (external field), `spin_empirical` (ground-truth binarized vote), and
  `nodes` (canton/distrito codes, in array order) arrays used in the paper's
  headline results: the 2026 coalition-split canton and distrito networks
  (Sections 4.2/4.5/4.6), and the 2018/2022/2026 winner-vs-runner-up canton
  networks (Section 4.3). Load with:

  ```python
  import numpy as np, scipy.sparse as sp
  d = np.load("processed_networks/2026_coalition_distrito.npz", allow_pickle=True)
  J = sp.coo_matrix((d["J_data"], (d["J_row"], d["J_col"])), shape=tuple(d["J_shape"])).tocsr()
  h, spin_empirical, nodes = d["h"], d["spin_empirical"], d["nodes"]
  ```

  These are ready to pass straight into
  `isingcr.simulation.monte_carlo.pooled_temperature_scan` to reproduce any
  temperature scan in the paper without re-deriving the network from raw
  data.

## What's *not* here, and why

- **Raw TSE per-junta election results.** Costa Rica's Tribunal Supremo de
  Elecciones (TSE) publishes official "escrutinio definitivo" results
  publicly, but its site blocks scripted/bulk access (bot protection) —
  the data behind this project was obtained by hand through a browser, one
  election at a time. Since TSE does not offer a documented bulk-redistribution
  license, we don't re-host their raw exports here; download them directly
  from TSE (`tse.go.cr` / `ride.tse.go.cr`) for the corresponding election.
  The `processed_networks/*.npz` files above are the aggregated,
  already-binarized *output* of that data (vote margins and win/loss labels
  per canton/distrito), not a republication of TSE's raw per-junta tables.
- **Raw canton/distrito boundary shapefiles.** From UN OCHA's Humanitarian
  Data Exchange (COD-AB dataset,
  https://data.humdata.org/dataset/cod-ab-cri) — download directly from HDX
  rather than from a mirror here, so you always get their current version
  under their own license terms. `processed_networks/*.npz` contains only
  the derived border-adjacency structure (which units are neighbors, and by
  how much shared border length), not the geometry itself.

To regenerate everything from scratch, place TSE's per-junta ZIPs in
`data/raw/tse_juntas/` and the HDX shapefiles in `data/raw/boundaries/`
(see each script's `DATA_RAW` path) and run the scripts directly.

## Installation

```bash
pip install -r requirements.txt
pytest tests/ -q
```

`simulation/` only needs numpy/scipy. `ingestion/` additionally needs
pandas, networkx, and geopandas (which needs GDAL/GEOS/PROJ — see the
manuscript repo or use `conda-forge` if pip install fails on those).

## Citation

If you use this code, please cite the manuscript (link above). This
repository does not currently have an archived DOI (e.g. via Zenodo) — a
release will be tagged and archived at submission time.

## License

Code: MIT. See `LICENSE`. The processed network files are derived data;
see "What's not here, and why" above for the underlying data sources'
own terms.
