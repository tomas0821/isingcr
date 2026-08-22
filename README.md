# IsingCR

Sociophysics simulation of Costa Rican electoral dynamics: an Ising-like model of
opinion formation on the spatial adjacency network of cantons/distritos, fit
against empirical results from the Tribunal Supremo de Elecciones (TSE).

## Status

Initial deliverables are implemented and tested end to end **on synthetic data**:

1. Data ingestion pipeline (`isingcr.ingestion`): TSE results parser, vote
   binarization, shapefile-derived spatial adjacency graph, graph assembly.
2. Monte Carlo engine (`isingcr.simulation`): sparse-graph Ising Hamiltonian,
   Metropolis + Glauber dynamics, temperature scans, thermodynamic observables.
3. Visualization (`isingcr.visualization`): phase diagrams (magnetization,
   specific heat, susceptibility vs. T) and empirical-vs-simulated map comparisons.

**The full pipeline now runs end to end on real data.** `data/raw/tse_juntas/`
has the official per-junta "escrutinio definitivo" exports (2018, 2022 both
rounds, 2026), loaded/aggregated/pivoted by
`isingcr.ingestion.load_tse_juntas_consolidado` and verified against TSE's own
published national totals; `data/raw/boundaries/` has Costa Rica's real
84-canton geometry (from UN OCHA's HDX, see "Getting real data" below).
`scripts/run_real_pipeline.py` runs vote loading, binarization, real spatial
adjacency, the MC temperature scan, and real map comparisons, all on real 2026
presidential data -- pass `SKIP_SHAPEFILE=1` to run just the TSE half.

`run_real_pipeline.py` now binarizes 2026 as PUEBLO SOBERANO (48.5% nationally)
vs. a coalition of the next three largest parties (LIBERACION NACIONAL,
COALICION AGENDA CIUDADANA, FRENTE AMPLIO) -- a 51-vs-33-canton split, so the
majority-class baseline is 60.7%, not the ~94% a naive "traditional vs.
everyone else" split gave (that split is degenerate for this election: with
PUEBLO SOBERANO's landslide, "traditional parties" win almost no cantons, so
"predict majority" alone already explains ~94% of cantons and the model's
score can't be distinguished from that baseline). The current run scores
~73% best-T alignment against that 60.7% baseline -- a real, if noisy,
improvement (see the caveat on MC noise below).

`scripts/run_historical_comparison.py` runs the same model (same real canton
graph) across all three available elections (2018 and 2022 runoffs, winner vs.
runner-up by construction; 2026 round 1, winner vs. runner-up by vote count).
Like `run_ablation.py`, it pools `N_SEEDS=8` replicates per temperature (see
`isingcr.simulation.monte_carlo.pooled_temperature_scan`) and reports
best-T alignment as mean+/-std across seeds, with "beats baseline" requiring
the 1-sigma-low band to clear it, not just the point estimate -- an earlier
single-seed version of this comparison reported the same qualitative result
but without that rigor, right before `run_ablation.py` demonstrated
single-seed alignment gaps and susceptibility peaks can be pure noise, so it
needed re-checking rather than being trusted as-is. It held up:

| Election | Winner | Runner-up | N | Baseline | Best alignment | 1-sigma "beats baseline"? | McNemar (median p, seeds sig. at 0.05) |
|---|---|---|---|---|---|---|---|
| 2018 (runoff) | Acción Ciudadana | Restauración Nacional | 81 | 76.5% | 76.4%+/-0.4% | **No** | p=1.00, 0/8 |
| 2022 (runoff) | Progreso Social Democrático | Liberación Nacional | 82 | 64.6% | 71.0%+/-4.1% | Yes | p=0.35, 2/8 |
| 2026 (round 1) | Pueblo Soberano | Liberación Nacional | 84 | 75.0% | 79.0%+/-2.2% | Yes | p=0.37, 1/8 |

*Pueblo Soberano (2026) is the direct electoral successor of Progreso Social
Democrático (2022) -- same governing movement, different registered party
name, not an unrelated newcomer as the table might suggest.*

2018 not beating baseline is now a tight, confident result (76.4%+/-0.4% is
barely distinguishable from 76.5%), not an artifact of noise -- a genuine
difference in how well "geography + margin" predicts 2018's map vs.
2022's/2026's, **now explained** (`scripts/investigate_2018_anomaly.py`, ~7s,
no MC scan needed):

- **It isn't that 2018 lacks geographic structure.** Moran's I on the real
  adjacency graph shows all three elections' maps are significantly spatially
  clustered (p<0.01) -- and 2018 is the *most* clustered of the three
  (I=0.71 vs. 0.49 for 2022, 0.35 for 2026), on both the binarized spin and
  the continuous margin. That hypothesis is ruled out.
- **It's that 2018's true map is a much more energetically "expensive"
  pattern for this Hamiltonian, relative to the trivial "everyone votes for
  the winner" state, than 2022's or 2026's are.** Every election's trivial
  all-majority configuration has lower energy than its true map (expected --
  it's the null being compared against), but the size of that gap, normalized
  per canton, is 1.13 for 2018 vs. 0.77 (2022) and 0.59 (2026) -- roughly
  47% (2022) and 92% (2026) larger. A temperature scan starting from random
  initial spins is much less likely to ever land near the true minority
  pattern when that pattern costs this much more energy than the trivial
  alternative, which is exactly the historical-comparison result. (The true
  2018 map is still a locally stable configuration on its own -- pooled
  across 8 seeds (T=0 Glauber isn't fully deterministic), 90.1%+/-0.0% of it
  survives a zero-temperature relaxation starting *at* the truth, actually
  the most stable of the three (85.4%+/-0.0% for 2022, 80.5%+/-4.3% for
  2026) -- the problem is specifically that a *random-start* search never
  finds that basin in the first place.)

This cleanly separates 2018 from 2022/2026 as a category (the question that
was actually open); it doesn't perfectly rank 2022 vs. 2026 against each
other, which wasn't the question. Susceptibility/specific heat show the same low-T
divergence artifact described in `run_ablation.py`/`pooled_temperature_scan`
for all three elections (peaks at the T=0.05 scan edge, not an interior
bump) -- no evidence of a real critical point in any of the three.

**The 1-sigma "beats baseline" read for 2022/2026 doesn't survive a proper
paired significance test, and that's worth sitting with.** `mcnemar_test`
(McNemar's exact test, model vs. the constant majority-class null, following
Korbel et al. 2025/26's own validation methodology -- see `NOVELTY_CHECK.md`)
run per-seed at each election's best T finds only 1-2 of 8 seeds individually
significant at p<0.05 for 2022 and 2026, with median p-values of 0.35 and
0.37 -- nowhere near conventional significance. This isn't necessarily "the
effect isn't real": N~84 discordant-pair tests have limited statistical power
to begin with, and 4-9 percentage points over baseline is a small effect to
detect that way. But it means "2022 and 2026 clearly beat baseline" was an
overstatement of what the 1-sigma heuristic actually supports -- the honest
current read is "2018 is a confident null; 2022/2026 show a similarly-sized
positive point estimate that individual-seed significance testing can't yet
confirm." Don't cite the earlier framing without this caveat.

**MC noise caveat, applies only to `run_real_pipeline.py`** (single seed,
400-500 sweeps per T, to stay fast for a one-off demo run): its alignment/
susceptibility/specific-heat curves are visibly noisy run to run -- don't read
a single-point peak there as a precise critical temperature. `run_ablation.py`
and `run_historical_comparison.py` both use the pooled multi-seed approach
instead and take ~35-70s locally (12-core machine) -- there's no real reason
not to use it for anything meant to support a claim.

`scripts/run_ablation.py` separates the two ingredients of the 2026 result:
a "geography only" run (`h=0` everywhere, scored with
`symmetric_alignment_fraction` since h=0 makes the model's up/down labeling
arbitrary -- see that function's docstring) vs. the normal "geography +
predisposition" run (`h`=vote margin). It pools 8 independent MC seeds per
temperature (~35s on a 12-core machine) rather than the single-seed runs
above, with two results that only showed up once noise was under control:

- Best-T alignment: geography-only 67.6%+/-5.5%, geography+predisposition
  68.8%+/-3.5%, against a 60.7% baseline -- both clearly beat the baseline,
  but the +1.2-point gap between them is well within the overlapping error
  bars. With proper uncertainty estimates, this run can't actually
  distinguish "predisposition adds a little" from "predisposition adds
  nothing measurable" -- the single-seed run's +2.4-point gap wasn't real
  signal, it was noise that happened to point the intuitive direction.
- McNemar's exact test (model vs. majority-class null, per seed at the
  best T) tells the same "smaller than it looks" story from a different
  angle: geography-only is significant at p<0.05 in only 2/8 seeds
  (median p=0.087), geography+predisposition in 5/8 (median p=0.026) --
  h helps the *significance*, even though it barely moves the point
  estimate.
- The single-seed run's susceptibility/specific-heat "peaks" (~0.65 and
  ~1.55) also don't survive: pooled over 8 seeds, both curves instead show a
  monotonic blow-up as T->0 with no interior bump anywhere -- the signature
  of independent low-T chains freezing into different metastable
  configurations and chi/C's 1/T factor amplifying that disagreement (see
  `run_scan`'s docstring), not a real critical point. **No evidence of a
  genuine tipping point survives multi-seed averaging** for this election;
  the single-seed spikes reported earlier were an artifact.

`scripts/run_finite_size_scaling.py` takes the search for a real critical
point one step further with the technique built for exactly this: Binder
cumulant (`U4 = 1 - <m^4>/(3<m^2>^2)`) crossing between two system sizes,
which locates a genuine transition independent of N if one exists. Real
canton geometry (N=84) and real distrito geometry (N=488, `cri_admin3.shp`,
2 island distritos with no adjacency dropped -- see the script's docstring)
give the two sizes needed, same country, same election, same real adjacency
structure. Deliberately run at `h=0`: the technique's standard interpretation
assumes a symmetric order parameter, which only literally holds without a
symmetry-breaking field. Local run (2026 coalition split, 8 pooled seeds, 500/500 sweeps, ~2.5 min
locally): 6 crossings across the scanned range -- noise, not a confirmed
transition (two curves from a real transition cross once, not six times).
But the distrito curve also dipped below 0 at several T (U4 is only
physically valid in [0, 2/3] at true equilibrium), meaning N=488 wasn't
equilibrating properly at that sweep budget -- inconclusive, not a confident
"no transition."

**Resolved 2026-08-16** with a heavier re-run on the UCR HPC cluster
(`scripts/run_finite_size_scaling_heavy.py`, `shared` partition, 32 cores,
n_equil=n_sweeps=20000 -- 40x the local budget -- 16 pooled seeds, 32
temperatures, 34m32s wall time): **0 negative U4 values at either N** (was
several before), confirming the local run's undersampling diagnosis. With
proper equilibration confirmed, the crossing count is still 5 (still noise,
still not a confirmed transition) -- so the finding upgrades from
"inconclusive" to a confident **no critical point found in the scanned range,
at either canton or distrito granularity, for 2026**. Consistent with every
other pooled scan in this project (no interior susceptibility/specific-heat
bump anywhere once seed-pooling artifacts are controlled) -- this project has
not found a confirmed thermodynamic phase transition anywhere yet.

## Distrito-level ablation (2026)

`run_ablation.py`'s canton-level ablation (+1.2pp from adding `h`, not
distinguishable from zero) aggregates over units that can hide real internal
heterogeneity -- a canton can contain both dense central-valley distritos and
remote outlying ones. `scripts/run_distrito_ablation.py` re-runs the same
geography-only vs. geography+margin ablation one level down, at the N=488
distrito granularity, on the UCR HPC cluster (same settings as the heavy
finite-size-scaling run: n_equil=n_sweeps=20000, 16 pooled seeds, 32
temperatures, 32 cores, ~57 min wall time):

| Run | Best alignment | @T | Peak χ | McNemar p (median) | seeds sig. at 0.05 |
|---|---|---|---|---|---|
| A: geography only (h=0) | 66.2%+/-6.4% | 2.83 | 957.6 | 0.1798 | 4/16 |
| B: geography + margin | 74.8%+/-4.2% | 0.61 | 449.5 | 0.0009 | 12/16 |

Majority-class baseline: 66.9%. Marginal contribution of `h`: **+8.7pp**, a
real contrast with the canton-level result -- at distrito granularity the
gain from each unit's own vote margin is both larger (+8.7pp vs. +1.2pp) and
far more statistically robust (McNemar p=0.0009 with 12/16 seeds
significant, vs. the canton-level ablation's weaker read). Geography-only
alignment (66.2%) barely clears the 66.9% baseline and its significance is
weak (4/16 seeds) -- pure geographic contagion explains much less of the
real map at distrito scale than at canton scale, and predisposition is doing
real, resolvable work at this finer granularity. Not yet decomposed into
*which* distritos geography-only gets wrong (candidate follow-up: cross-
reference against MIDEPLAN's Índice de Desarrollo Social once ingested, see
`00_Master_Notebook.md` AI Handoff).

`scripts/run_demo.py` still exercises the same full pipeline (including
geometry) on a synthetic graph, and is what validates the Docker image without
depending on the real data files.

## Architecture

```
src/isingcr/
  simulation/     # IsingModel, dynamics, MC driver, observables
                  # -- pure numpy/scipy, NO pandas/networkx/geopandas imports.
  ingestion/      # TSE parsing, binarization, shapefile adjacency, graph assembly
                  # -- pandas/networkx/geopandas, produces an annotated nx.Graph
  utils/
    graph_arrays.py  # the ONE conversion point: nx.Graph -> (J, h) sparse arrays
    synthetic.py     # synthetic graph+data generator, for testing without real files
  visualization/  # matplotlib plots + geopandas/networkx map comparisons
```

`simulation` is deliberately decoupled from `ingestion`: it only consumes a
scipy sparse coupling matrix `J` and field vector `h`. `utils/graph_arrays.py`
is the sole conversion boundary. This means the MC engine can be swapped onto
an HPC backend (MPI, job arrays) without touching any ingestion code -- see
`temperature_scan(..., n_jobs=N)` in `simulation/monte_carlo.py`, which already
parallelizes independent temperatures via `ProcessPoolExecutor` and documents
how that maps onto a cluster job array.

## Quick start

### Docker (recommended -- handles the GDAL/geopandas system deps)

```bash
docker compose build
docker compose run --rm isingcr
```

This runs `scripts/run_demo.py` and writes figures to `./figures/`.

### Local (venv)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .
.venv/bin/pytest tests/ -q
.venv/bin/python scripts/run_demo.py
```

geopandas depends on GDAL/GEOS/PROJ; on Debian/Ubuntu without Docker you may
need `apt install gdal-bin libgdal-dev libgeos-dev libproj-dev` first.

## Getting real data

- **Election results -- done.** TSE's site (tse.go.cr, vr2026, and the
  ride.tse.go.cr results repository) is behind Radware/hCaptcha bot protection
  and can't be scripted; the results in `data/raw/tse_juntas/` were downloaded
  manually by hand through a browser. They're the official "resultados por
  junta receptora de votos" ZIP exports (2018, 2022 both rounds, 2026
  presidential), one CSV row per (junta, partido), plus a pre-aggregated
  `_consolidado_*.csv` member per ZIP covering every junta in one file.
  `load_tse_juntas_consolidado()` reads that member, filters to
  `tipo_territorio="NACIONAL"` (juntas abroad have no geographic adjacency and
  would corrupt the coupling graph if left in -- see its docstring), aggregates
  up to canton/provincia/distrito, and pivots parties into columns. Verified
  against TSE's own published national totals (see each ZIP's `LEEME.txt`).
  Costa Rica has 84 cantones nationally / 492 distritos; note 2018 reports a
  different "distrito electoral" unit than 2022/2026's administrative distrito
  (see that ZIP's `LEEME.txt`) -- canton level matches cleanly across years.
- **Shapefiles -- done, via a third-party source.** Costa Rica's own IGN/SNIT
  geoportal (snitcr.go.cr) has the authoritative boundaries, but its
  GeoServer-backed WFS requires a signed session token generated client-side
  in the site's JS, which couldn't be reproduced with plain HTTP requests
  (direct WFS calls come back 403 Forbidden) -- pushing further into forging
  that token would mean circumventing their access control, so that wasn't
  attempted (SNIT's map viewer, snitcr.go.cr/Visor/visor, remains the manual
  fallback if the HDX data below ever needs cross-checking). Instead,
  `data/raw/boundaries/` has Costa Rica's admin0-3 boundaries from
  [UN OCHA's Humanitarian Data Exchange](https://data.humdata.org/dataset/cod-ab-cri)
  (COD-AB dataset, CKAN API, no bot-wall), `cri_admin2.shp` = the 84-canton
  layer used here. Its canton names needed reconciling against TSE's own
  naming (see `isingcr.ingestion.canton_names.normalize_canton_code`): TSE
  calls each province's capital canton "CENTRAL" where this file names it
  after the province, and TSE keeps "Ñ" as a distinct letter (not folded to
  "N" like other accents, e.g. "Cañas") where naive accent-stripping would
  merge them. With both handled, all 84 cantons match exactly (verified in
  `scripts/run_real_pipeline.py`, no dropped/unmatched nodes). Costa Rica's
  official cadastral CRS is CRTM05 (EPSG:5367), which
  `shapefile_adjacency.load_shapefile()` reprojects into automatically.
- `scripts/run_real_pipeline.py` already points at both real data sources by
  default -- just run it (see its module docstring for a summary, and the
  caveat above about the current binarization's class imbalance before
  trusting the numbers it prints).

## A physics note: pick a symmetry-breaking field

With `h = 0` everywhere, the Hamiltonian has an exact up/down (Z2) symmetry:
flipping every spin leaves the energy unchanged. Below the ordering
temperature the system still spontaneously orders, but *which* of the two
macro-states ("traditional" vs. "emerging") it lands in is then arbitrary and
history-dependent (which run of the demo you get). Real elections aren't
symmetric this way. Two ways to anchor the sign:

- Derive `h_i` from something directional and real -- e.g. `binarize_votes`
  already returns a `margin` column (`(votes_a - votes_b) / total`) that's a
  natural, non-arbitrary candidate for `h_i`.
- If you do want `h = 0` (pure "does spatial coupling alone explain the map"
  test), compare simulated vs. empirical alignment using
  `max(fraction_matching, 1 - fraction_matching)` rather than the raw fraction,
  since the sign of the simulated ground state isn't otherwise meaningful.

`isingcr.utils.synthetic.synthetic_electoral_graph(..., field_scale=...)` uses
a smooth *spatial gradient* field rather than i.i.d. per-canton noise for this
reason: a disordered per-node random field turns the model into a Random Field
Ising Model, whose low-temperature landscape is glassy (many near-degenerate,
history-dependent minima) -- physically interesting, but not what you want
from a quick sanity demo.

## Extending

- **Edge weights beyond uniform/border-length**: `build_adjacency_graph(...,
  weight_by=...)` currently supports `"uniform"` and `"border_length"`; add a
  new branch there (or post-process the returned graph's edge `"weight"`
  attribute) to weight by demographic/economic similarity between adjacent
  units, as the spec calls out for later iterations.
- **HPC parallelization**: `temperature_scan`'s worker function
  (`_run_single_temperature`) takes plain arrays and a seed -- it's already
  the right shape for one task per HPC array-job index; replace the
  `ProcessPoolExecutor` dispatch with your scheduler's array-job mechanism.
- **Smoother phase diagrams**: `scripts/run_demo.py` uses short runs
  (`n_equil=300`, `n_sweeps=300`, one seed per T) to stay fast; for a real
  study, use `isingcr.simulation.monte_carlo.pooled_temperature_scan` (see
  `run_ablation.py`/`run_historical_comparison.py` for worked examples) to
  average multiple independent seeds per temperature instead -- single-seed
  runs demonstrably produced both a spurious alignment-gap finding and
  spurious susceptibility peaks in this project (see "Status" above).

## Testing

```bash
.venv/bin/pytest tests/ -q
```

57 tests cover: Ising energy/dynamics correctness (including a brute-force
check that the incremental `delta_energy`/`flip` bookkeeping matches
recomputing the energy from scratch, and that Glauber's sigmoid never
overflows at low T/large dE), low/high-T equilibrium behavior,
`temperature_scan`/`pooled_temperature_scan`, McNemar's test
(`mcnemar_test`/`mcnemar_seed_summary`), Moran's I spatial autocorrelation
(`morans_i`/`morans_i_test`), the TSE parser's column
auto-detection, the per-junta consolidado loader (aggregation, party
pivoting, NACIONAL/EXTRANJERO filtering, the 2018 distrito_electoral rename,
stray-whitespace stripping), vote binarization, canton- and distrito-name
reconciliation (province-capital "CENTRAL" folding, Ñ preservation), shapefile adjacency topology (via synthetic polygon
grids), the ingestion->simulation array
conversion, and the synthetic data generator.
