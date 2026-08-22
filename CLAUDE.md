---
type: project
stage: implementing
last_activity: 2026-08-16
---

# CLAUDE.md

Guidance for working in this repository.

Publication tracking lives in `NOVELTY_CHECK.md` (verdict: CLEAN) and
`00_Master_Notebook.md` (run-by-run log with figures). Target journal: Physica A:
Statistical Mechanics and its Applications (fallback: EPJB). Seed stub:
`lit-gap-toolkit/physica-a/candidates/cr-electoral-ising-canton-network/SEED.md`.
Reference library: Zotero ▸ Sociophysics ▸ IsingCR (18 items), all 18 converted to
Markdown in `papers_md/` (see `papers_md/CONVERSION_NOTES.md` for known table-loss
caveats). 16 are actually cited in the manuscript; 2 (Godoy-Lorite & Jones 2020,
Okamoto 2021) are adjacent-but-not-colliding novelty-check references only
(NOVELTY_CHECK.md §2b/§3), not cited in the manuscript.

## What this is

An Ising-model sociophysics simulation of Costa Rican electoral dynamics: spins
= binarized canton/distrito vote outcomes, couplings = geographic adjacency,
external field = incumbency/media-pressure proxy. Goal: find the "social
temperature" at which simulated equilibrium best reproduces the empirical TSE
map. Full spec context lives in the original project brief (electoral Ising
model on TSE data, Feb 2026 election / 2024 municipal elections).

## Current state (2026-08-16)

All three initial deliverables (ingestion, MC engine, visualization) are
implemented and pass `pytest tests/ -q` (57 tests). Eight scripts, in order of
what they're for:

- `scripts/run_demo.py` -- full pipeline on synthetic data, validates the
  Docker image without needing the real data files.
- `scripts/run_real_pipeline.py` -- full pipeline on real 2026 data:
  `data/raw/tse_juntas/` (official per-junta "escrutinio definitivo" ZIPs,
  hand-downloaded since TSE's site blocks scripted access) and
  `data/raw/boundaries/` (real canton geometry from UN OCHA HDX's COD-AB
  dataset, since SNIT's own WFS needs a signed session token that couldn't be
  obtained non-interactively -- see README "Getting real data" for both). All
  84 cantons match between the two sources. Binarizes PUEBLO SOBERANO vs. a
  coalition of the next three largest parties. Single MC seed -- fast, but see
  the ablation/historical scripts for why that's not enough to trust a claim.
- `scripts/run_ablation.py` -- isolates how much of the real map pure
  geography (`h=0`) explains vs. geography + each canton's own vote margin,
  pooling 8 MC seeds per temperature (`pooled_temperature_scan`, ~35s
  locally). **Both this script's original headline results were wrong under
  1 seed and got overturned once pooled**: the "+2.4pp from adding h" gap
  shrank to +1.2pp, well inside overlapping error bars (not distinguishable
  from zero); and the clean single-seed susceptibility/specific-heat peaks
  turned out to be a low-T pooling artifact (see gotcha #7 below), not a real
  critical point. Also reports `mcnemar_seed_summary` (McNemar's exact test,
  model vs. majority-class null, per seed) -- only 2/8 (geography-only) and
  5/8 (geography+h) seeds are individually significant at p<0.05, tempering
  even the pooled point estimates further (see gotcha #8). Current numbers
  are in README "Status".
- `scripts/run_historical_comparison.py` -- same pooled approach across all
  three available elections (2018/2022 runoffs, 2026 round 1, winner vs.
  runner-up each cycle). 2018 is a tight, confident null (76.4%+/-0.4% vs. a
  76.5% baseline, McNemar 0/8 seeds significant) vs. 2022/2026's positive
  point estimate. But 2022/2026's "beats baseline" read is weaker than the
  1-sigma point estimate suggests once McNemar-tested (median p=0.35/0.37,
  only 2/8 and 1/8 seeds individually significant) -- don't cite "2022 and
  2026 clearly beat baseline" without that caveat.
- `scripts/investigate_2018_anomaly.py` -- **explains** the 2018 asymmetry
  above, cheaply (~7s, no MC scan). Not lack of geographic structure: Moran's
  I shows 2018 is the *most* spatially clustered of the three elections
  (I=0.71 vs. 0.49/0.35). It's that the true 2018 map costs ~1.13 energy
  units/canton relative to the trivial all-majority state under this
  Hamiltonian, vs. ~0.77 (2022) / ~0.59 (2026) -- 47%/92% more energetically
  disfavored, so a random-start MC search is much less likely to ever find
  its basin, even though the true map is itself locally stable (90.1%+/-0.0%
  of it survives a T=0 relaxation starting *at* the truth, pooled across 8
  seeds -- the highest of the three, vs. 85.4%+/-0.0%/80.5%+/-4.3% for
  2022/2026). Cleanly separates 2018 from 2022/2026 as a category; doesn't rank
  2022 vs. 2026 against each other, which wasn't the open question.
- `scripts/run_finite_size_scaling.py` -- Binder cumulant (`U4`) crossing
  between canton (N=84) and distrito (N=488, `cri_admin3.shp`) geometry, the
  canonical way to locate a real critical point independent of system size.
  Run at `h=0` deliberately (the technique needs a symmetric order parameter).
  Local run (500/500 sweeps, 8 seeds): 6 crossings (noise, not a real
  transition -- a genuine one crosses once), but the distrito curve dipped
  below the physically-valid U4 range ([0, 2/3] at equilibrium) at several T,
  meaning N=488 wasn't equilibrating at that sweep budget --
  **inconclusive**, not a confirmed "no transition".
- `scripts/run_finite_size_scaling_heavy.py` -- same question, resolved
  2026-08-16 on the UCR HPC cluster (`shared` partition, 32 cores,
  n_equil=n_sweeps=20000 -- 40x local -- 16 seeds, 32 temperatures, 34m32s
  wall). **0 negative U4 values at either N** (confirms the local run was
  undersampled, not that the physics was ambiguous). Crossing count is still
  5 (still noise) -- so this upgrades the verdict to a confident **no
  critical point found**, at either granularity, for 2026. Still no
  confirmed thermodynamic phase transition anywhere in this project.
- `scripts/run_distrito_ablation.py` -- the canton-level ablation's question
  (geography-only vs. geography+margin), one level down at distrito
  granularity (N=488) -- the "severe differences among distritos" angle.
  Same cluster settings/run, 2026-08-16 (~57 min wall). Geography-only:
  66.2%+/-6.4% vs. a 66.9% baseline (barely clears it, McNemar only 4/16
  seeds significant). Geography+margin: 74.8%+/-4.2% (McNemar p=0.0009,
  12/16 seeds significant). **+8.7pp marginal gain from h at distrito
  scale, both larger and far more statistically robust than the canton-level
  ablation's +1.2pp/not-significant result** -- pure geographic contagion
  explains much less of the real map at this finer granularity, and
  predisposition does real, resolvable work. Not yet decomposed into which
  specific distritos geography-only misses.

## Things worth knowing before touching this code

1. **`simulation/` must stay free of pandas/networkx/geopandas imports.** The
   whole point of the `utils/graph_arrays.py` boundary is that the MC engine
   can be dropped onto an HPC backend without dragging ingestion deps along.
   If a PR adds a `networkx` import inside `simulation/`, that's a regression
   of the architecture, not a convenience.
2. **The Z2 symmetry gotcha** (see README "A physics note"): with `h=0` the
   model can't tell "traditional" from "emerging" -- the label is arbitrary
   below the ordering temperature. Any real run should derive `h_i` from the
   vote margin (`binarize_votes` already computes it) rather than leaving it
   at the default zero, or the alignment-vs-T curve will look randomly bimodal
   at low T for no reason related to the actual physics.
3. **`IsingModel.flip` is O(degree), not O(N).** It incrementally patches the
   cached local-field array using the sparse row's neighbor list. Don't
   "simplify" this back to `J.dot(spins)` recomputation inside the MC sweep
   loop -- that turns an O(N * avg_degree) sweep into O(N^2).
4. **TSE column names are not stable across releases.** `load_tse_results`
   auto-detects common patterns but silently guessing wrong is worse than
   erroring, so it raises when it can't find a code/name/party column rather
   than picking something plausible-looking. Expect to pass explicit
   `code_col`/`name_col`/`party_cols` for whatever specific file you're given.
5. **The real TSE data in `data/raw/tse_juntas/` needs `load_tse_juntas_consolidado`,
   not `load_tse_results`.** These ZIPs are per-junta long format (one row per
   junta x party), not the flat per-canton wide CSV `load_tse_results` expects.
   Always filter to `tipo_territorio="NACIONAL"` (the default) before building
   a graph -- juntas abroad have no geographic adjacency and will corrupt the
   coupling matrix if left in.
6. **Never join TSE canton names to a boundary file by naive string equality.**
   Use `isingcr.ingestion.canton_names.normalize_canton_code` -- TSE names
   each province's capital canton "CENTRAL" where most boundary files name it
   after the province, and TSE keeps "Ñ" as a distinct letter where generic
   accent-stripping folds it to "N". Skipping this silently drops cantons
   (see `build_electoral_graph`'s "no matching results row" warning) rather
   than erroring, so a naive join can look like it worked while quietly
   losing nodes.
7. **Never trust a single-seed `temperature_scan` result enough to state a
   finding from it -- use `pooled_temperature_scan` instead.** This bit twice
   in this project already (see run_ablation.py/run_historical_comparison.py
   in "Current state"): (a) a single-seed alignment gap can point the
   intuitive direction purely by chance and vanish once pooled, and (b) at
   low T, independent chains can each freeze into a *different* metastable
   domain configuration; pooling then mixes real thermal fluctuation with
   between-chain disagreement, and since susceptibility/specific heat both
   divide by T, that disagreement inflates into a spurious divergence at the
   low-T scan edge. A real critical point is an interior bump in the pooled
   curve, not a monotonic blow-up toward T=0 -- every real-data run so far
   shows the latter, i.e. no confirmed critical point yet anywhere in this
   project.
8. **A best-T accuracy clearing baseline by more than its 1-sigma error bar
   is not the same as statistical significance -- run `mcnemar_seed_summary`
   before calling a result "beats baseline."** N~84-500 discordant-pair
   McNemar tests have real trouble reaching p<0.05 even for a genuine
   4-9-point effect; the ablation and historical-comparison scripts both
   found weaker significance than their 1-sigma heuristic implied (see
   "Current state"). This isn't grounds to call the effect fake -- it's
   grounds to report both numbers and let the reader judge, not just the
   point estimate.
9. **Distrito-level joins need `normalize_distrito_code`, not
   `normalize_canton_code`.** Same province-capital "CENTRAL" quirk recurs
   one level down (a boundary file's admin3 layer names a canton's first
   distrito after the canton; TSE still calls the canton "CENTRAL" in
   `canton_ciudad` regardless) -- confirmed 430/492 naive matches, 489/492
   after the fix, 490/492 after also stripping stray whitespace in TSE's raw
   geography fields (a real 2026 row has a leading space in `distrito`,
   fixed in `load_tse_juntas_consolidado`). The 2 remaining mismatches
   (Pejivalle/Pejibaye, Los Angeles/Angeles) are genuine alternate-name
   variants, accepted as dropped nodes rather than special-cased.
