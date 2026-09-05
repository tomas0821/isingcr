# 📓 Lab Notebook — IsingCR

**Started:** 2026-08-16
**Author:** Tomas Rojas

---

## 📥 AI Handoff & Next Actions

- [x] Read Tiwari, Yang & Sen 2021 (Physica A, 10.1016/j.physa.2021.126287) in full —
      2026-08-16, user sourced the PDF, converted via marker Mode A
      (`papers_md/tiwari2021/`). Confirms the secondhand inference: purely synthetic
      128×128/256×256 square-lattice model, no real geography, no real election data.
      NOVELTY_CHECK.md upgraded to plain **CLEAN**.
- [x] Investigate why 2018 does not beat its majority-class baseline while 2022/2026
      show a positive point estimate — 2026-08-16, `scripts/investigate_2018_anomaly.py`.
      **Not** lack of geographic structure (the political-science/PAC-urban-base lead
      turned out to be the wrong direction — see Simulation Logs below for what it
      actually is). Answered, not just leaded.
- [x] Distrito-level (N=488) re-run done 2026-08-16 — `scripts/run_finite_size_scaling.py`,
      Binder cumulant crossing vs. canton (N=84). Result inconclusive (see Simulation Logs
      below), not a confirmed answer either way.
- [x] Re-run `run_finite_size_scaling.py` with more `n_equil`/`n_sweeps` for the distrito
      scan specifically — done 2026-08-16 on the UCR HPC cluster (`shared` partition),
      `scripts/run_finite_size_scaling_heavy.py` (40x the sweep budget, 16 seeds, 32
      temperatures). 0 negative U4 values at either N (vs. several before) — confirms
      the undersampling diagnosis and upgrades the verdict to a confident "no critical
      point found" (still 5 crossings, still noise). See Simulation Logs below.
- [x] Distrito-level ablation (`scripts/run_distrito_ablation.py`, same cluster run,
      2026-08-16) found a real +8.7pp gain from adding `h` at distrito granularity
      (McNemar p=0.0009, 12/16 seeds significant) — much stronger than the canton-level
      null. **Tempered 2026-08-18** after an adversarial referee-panel review of the
      manuscript (`referee_report_2026-08-17.md`) flagged that McNemar's independence
      assumption is violated by spatially autocorrelated data — added
      `spatial_block_permutation_test` (`isingcr.simulation.observables`) and reran
      (`scripts/run_spatial_robustness_check.py`, independent 16-seed sample at the
      already-known best T): McNemar still significant after Bonferroni-correcting for
      the 32-T grid (p=0.0030), but the spatial-block test gives p=0.064 — **not**
      significant. Effect size reproduces across both independent samples; only the
      *significance* is test-dependent. Manuscript now reports both tests and hedges
      accordingly rather than calling it "strongly significant." Still worth a
      follow-up: which specific distritos does geography-only get wrong that margin
      fixes? Candidate next step once/if the MIDEPLAN IDS-2023 covariate
      (Anexo 5 table, `/tmp/IDS_2023_DOCPLAN-03534.pdf`) gets ingested — cross-reference
      against low-IDS districts (Chirripó, Telire) to see if this is a
      socioeconomic-heterogeneity story, not just a "smaller units are noisier" one.
- [x] Public code/data repo — done 2026-08-18: github.com/tomas0821/isingcr (public),
      simulation code + all scripts + tests + processed J/h/spin_empirical adjacency
      networks for every headline result. Deliberately excludes raw TSE exports and raw
      boundary shapefiles (redistribution-terms concern) — README links both primary
      sources directly instead.
- [x] Funding statement — done 2026-08-18: "no external funding received" (confirmed
      accurate).
- [x] Four more methodological robustness checks, done 2026-08-18 (spatial-block
      sensitivity + resolution-matched subsample + cross-binarization, prioritized in
      that order per cost/value): see `referee_report_2026-08-17.md`'s Limitations-flagged
      items. Findings:
      - Spatial-block permutation test is **not robust to blocking granularity**
        (`scripts/run_spatial_block_sensitivity.py`): p=0.377 (7 province blocks) →
        0.068 (84 canton blocks, matches the earlier-reported 0.064) → 0.019 (~165
        half-canton blocks) — crosses significance in both directions. No principled
        way to pick a "correct" granularity; reported as a range now, not one number.
      - Resolution-matched subsample check, spatially coherent version
        (`scripts/run_distrito_contiguous_subsample_check.py`, cluster/local): 10
        independent ~84-distrito subsamples built from whole random cantons (realistic
        ~140-edge networks) give effect size +10.1%±2.4% (range +5.2–13.7%), matching
        the full N=488 result and never shrinking toward canton level — **rules out a
        pure statistical-power artifact**. (An earlier uniformly-random-scatter attempt,
        `run_distrito_subsample_check.py`, gave +19.9% but was confounded by a badly
        sparse ~40-edge induced network — kept in the repo for reference, not used in
        the paper.)
      - Cross-binarization check (`scripts/run_distrito_ablation_wvru.py`, UCR cluster,
        job 121820): distrito ablation under winner-vs-runner-up instead of the
        coalition split gives +11.6pp (matches the effect size) but McNemar p=0.087
        (much weaker than the coalition split's p=0.0009).
      - **Net read**: the +8–12pp distrito-level effect *size* is now well-supported
        (survives two independent manipulations that could each have explained it
        away); its formal statistical *significance* is not — it swings from clearly
        significant to marginal/non-significant depending on test or binarization
        choice, with no principled way to prefer one. Manuscript's Abstract/Section
        4.6/Conclusion/Limitations rewritten to state this precisely (new Table 2 in
        Section 4.6 summarizes all four effect-size estimates side by side) rather than
        lean on the single most favorable p-value.
      - Still not done, by explicit user choice: a genuine third finite-size-scaling
        system size (no natural one exists in Costa Rica's admin hierarchy) and a
        max-statistic permutation null (far more expensive than the Bonferroni
        correction already applied).
- [x] If drafting for Physica A begins: re-run NOVELTY_CHECK.md §2 queries + a fresh Exa
      sweep first (see its §5 re-check schedule) — this niche moved fast even within one
      day of checking (3 of 8 adjacent papers found were 2025/2026 publications).
      Done 2026-08-18, prompted by round-2 referee finding that the manuscript's
      Introduction now claims "cross-scale replication" (the distrito-level finding) as
      part of its novelty positioning, a scope the original 2026-08-16 check never
      covered. Re-run at distrito/cross-scale scope specifically (NOVELTY_CHECK.md §2b):
      still CLEAN — no collision found across OpenAlex, Semantic Scholar, FastTrack
      duplication test, and Exa. Two new adjacent-but-not-colliding references surfaced
      and logged in §3 (Godoy-Lorite & Jones 2020; Okamoto 2021).
- [x] Two-field Hamiltonian (`E(s) = -ΣJs s - Σ(λ_pol h^pol + λ_soc h^soc)s`) + 3D
      `(λ_pol, λ_soc, T)` scan against real MIDEPLAN IDS 2023 socioeconomic data,
      2026-08-20/21 — see Simulation Logs below for the composite-index result and the
      follow-up axis decomposition (which one of IDS's 5 sub-dimensions actually carries
      the effect). **Not yet folded into the manuscript** — explicit user instruction
      ("ok lets hold on") pending (a) results settling and (b) a targeted novelty check
      on the two-field/socioeconomic-covariate angle, starting with `massoli2026`
      (already in the bibliography), before any manuscript-integration decision.
- [ ] 2022 padrón electoral (full national voter registry, `data/raw/tse_padron/
      padron_completo_2022.zip`, 3,541,908 rows) downloaded 2026-08-21 — recovered via
      Wayback Machine (TSE's *current* download page only ever serves the live/updated
      registry, no historical archive) from an orphaned-but-still-live URL, verified as
      a genuine ZIP (not a 404 masquerading as HTTP 200 — TSE's server returns
      `content-type: text/html` on everything regardless). Fields present: `CEDULA,
      CODELEC (geography), FECHACADUC (ID *expiry*, not birth), JUNTA, NOMBRE, two
      surnames` — **no sex or age/birthdate field**, contrary to what was expected
      going in; cédula numbers don't encode either in Costa Rica's system. Not yet used
      for anything. Live options if revisited: name-based sex inference from `NOMBRE`
      (real technique, imperfect on unisex/compound names, at least keeps 2022/2026
      comparable), or TSE's live interactive consulta tool for real sex/age aggregates
      (accurate but 2026-only, breaks year comparability the same way the MIDEPLAN IDS
      2023-on-2022-election timing gap already does).
- [x] Zotero collection wired up 2026-08-16: Sociophysics ▸ IsingCR (key `BA4KBCB9`),
      all 16 NOVELTY_CHECK.md §3 references added via the Zotero Web API and tagged
      `IsingCR-novelty-check`. All 16 PDFs attached (by the user) and converted to
      Markdown (`papers_md/<slug>/<slug>.md`) via marker Mode A — see
      `papers_md/CONVERSION_NOTES.md` for fidelity notes and 4 documented table-body
      losses (captions survived in every case; `korbel2026`'s TABLE III — per-decade
      fitted parameters — is the one worth a Mode B re-run if cited directly). No
      Better BibTeX / local Zotero API available (Zotero runs on Windows, not WSL, since
      2026-07-28) — `.bib` regeneration and `[[citekey]]` wikilinks (Step 5b/5c of the
      lab-notebook sync) aren't wired up; works are cited by DOI/title directly in this
      notebook and in `NOVELTY_CHECK.md` for now.

---

## Project Overview

Ising-model sociophysics simulation of Costa Rican electoral dynamics: spins = binarized
canton-level vote outcomes, couplings `J_ij` = real geographic canton border-adjacency,
external field `h_i` = local vote margin (predisposition proxy). Fit via Glauber/
Metropolis Monte Carlo temperature scans against real TSE (Tribunal Supremo de
Elecciones) results. Goal: find the "social temperature" at which simulated equilibrium
best reproduces the empirical map, and decompose how much of that map is explained by
pure geographic contagion vs. each canton's own political lean.

**Key observables:** magnetization `⟨|m|⟩`, specific heat `C = Var(E)/(N T²)`,
susceptibility `χ = N·Var(m)/T`, alignment fraction (simulated vs. empirical spin match)
and its Z2-safe variant `symmetric_alignment_fraction` (needed whenever `h` is zero or
weak — see `isingcr.simulation.observables`).

**Architecture:** `simulation/` (pure numpy/scipy, no data-ingestion deps) ↔
`ingestion/` (pandas/networkx/geopandas) ↔ `utils/graph_arrays.py` (the one conversion
boundary). See `README.md` for the full writeup and `CLAUDE.md` for the gotchas list
(Z2 symmetry, single-seed MC noise, canton-name reconciliation).

**Data:** real 2018/2022(×2 rounds)/2026 TSE per-junta results
(`data/raw/tse_juntas/`, hand-downloaded — TSE's site blocks scripted access) and real
84-canton boundaries from UN OCHA's HDX COD-AB dataset (`data/raw/boundaries/`, since
SNIT's own WFS needs a session token unobtainable non-interactively). All 84 cantons
match between the two sources after reconciling two naming quirks (province-capital
"CENTRAL" folding, Ñ preservation) — see `isingcr.ingestion.canton_names`.

**Publication status:** seeded via `/seed-idea` → `lit-gap-toolkit/physica-a/candidates/
cr-electoral-ising-canton-network/SEED.md` (verdict NARROWED — broad "Ising model for
elections" is a crowded active subfield; the real-geographic-adjacency + real-Costa-Rica
+ ablation + historical-comparison corner survives). Deep novelty check in
`NOVELTY_CHECK.md` (verdict CLEAN-pending-full-text). Target journal: **Physica A:
Statistical Mechanics and its Applications** (primary — publishes exactly this genre,
including recent Brazilian subnational-election sociophysics papers; scope explicitly
covers "cultural and political complexity"); **European Physical Journal B** (fallback).

---

## Simulation Logs

### Run: synthetic demo (`run_demo.py`) — 2026-08-15

Validates the full pipeline (ingestion → simulation → visualization) end to end without
depending on real data files; also what the Docker image build is checked against.

| Parameter | Value |
|---|---|
| Graph | synthetic, 84 nodes, Delaunay triangulation of random points |
| Field | smooth spatial gradient, `field_scale=1.5` (breaks Z2 symmetry deliberately — see `README.md` "A physics note") |
| Temperatures | 20 points, linspace(0.1, 4.0) |
| MC | `n_equil=300`, `n_sweeps=300`, 1 seed |

**Final values:**
| Observable | Value |
|---|---|
| Nodes / edges | 84 / 239 |
| Best empirical alignment | 98.8% at T=0.716 |

**Notes:** Classic ferromagnetic phase-diagram shape (magnetization high at low T,
decaying at high T; specific heat/susceptibility rising toward a broad transition
region). Single-seed run — noisy, as expected; superseded for anything meant to support
a claim by the pooled runs below.

![Synthetic phase diagram](figures/phase_diagram.png)
![Synthetic alignment curve](figures/alignment_curve.png)
![Synthetic map comparison](figures/map_comparison.png)

---

### Run: real pipeline, 2026 coalition split (`run_real_pipeline.py`) — 2026-08-16

First fully real run: real 2026 presidential results × real canton adjacency.
Binarization: PUEBLO SOBERANO (48.5% nationally) vs. a coalition of the next three
largest parties (LIBERACION NACIONAL, COALICION AGENDA CIUDADANA, FRENTE AMPLIO) — a
deliberate move away from a degenerate "traditional vs. everyone else" split that gave a
79-vs-5 canton majority-baseline (~94%, indistinguishable from guessing).

| Parameter | Value |
|---|---|
| TSE source | `data/raw/tse_juntas/DEFINITIVO_juntas_TSE_2026.zip`, `_consolidado_presidenciales.csv` |
| Boundary source | `data/raw/boundaries/extracted/cri_admin2.shp` (HDX COD-AB) |
| `h_i` | vote margin (`binarize_votes`' `margin` column) |
| Temperatures | 25 points, linspace(0.1, 4.0) |
| MC | `n_equil=500`, `n_sweeps=500`, 1 seed |

**Final values:**
| Observable | Value |
|---|---|
| Cantons matched | 84 / 84, zero dropped |
| Spin split | 51 (+1) vs. 33 (−1); majority-class baseline 60.7% |
| Best empirical alignment | 72.6% at T=0.263 |

**Notes:** Single-seed — this specific run's alignment/susceptibility/specific-heat
curves are visibly noisy (see `README.md`'s MC-noise caveat); superseded by the pooled
ablation run below for anything meant to support a claim. Kept as the fast one-off
sanity check (`SKIP_SHAPEFILE=1` runs just the vote-loading half in seconds).

![Real 2026 phase diagram](figures/phase_diagram_real.png)
![Real 2026 alignment curve](figures/alignment_curve_real.png)
![Real 2026 map comparison](figures/map_comparison_real.png)

---

### Run: historical comparison, 2018/2022/2026 (`run_historical_comparison.py`) — 2026-08-16

Same real canton adjacency graph, three real elections, winner-vs-runner-up
binarization each cycle (2018/2022 runoffs are winner-vs-runner-up by construction;
2026 was decided in round 1). Pools `N_SEEDS=8` independent MC replicates per
temperature via `pooled_temperature_scan` — this is the corrected, trustworthy version;
an earlier single-seed pass gave the same qualitative read but needed re-checking (see
`run_ablation.py`'s findings below, which is what motivated re-running this with rigor).

| Parameter | Value |
|---|---|
| Elections | 2018 ronda2, 2022 ronda2 (`_consolidado_definitivo.csv`), 2026 round 1 |
| Canton renames | `ALAJUELA\|VALVERDE VEGA` → `ALAJUELA\|SARCHI` (2018 only — same canton, later renamed) |
| `h_i` | vote margin |
| Temperatures | 24 points, linspace(0.05, 3.5) |
| MC | `n_equil=500`, `n_sweeps=500`, `N_SEEDS=8`, `n_jobs=8` |
| Wall-clock | ~66s (12-core local machine) |

**Final values:**
| Election | Winner | Runner-up | N | Baseline | Best alignment | Beats baseline? |
|---|---|---|---|---|---|---|
| 2018 (runoff) | Acción Ciudadana | Restauración Nacional | 81 | 76.5% | 76.4%±0.4% | **No** |
| 2022 (runoff) | Progreso Social Democrático | Liberación Nacional | 82 | 64.6% | 71.0%±4.1% | **Yes** |
| 2026 (round 1) | Pueblo Soberano | Liberación Nacional | 84 | 75.0% | 79.0%±2.2% | **Yes** |

**Notes:** N differs by year because Costa Rica genuinely gained 3 cantons since 2018
(Río Cuarto, Monteverde, Puerto Jiménez each split off from an existing canton) — real
administrative history, not a data bug; `build_electoral_graph` drops any adjacency node
with no matching results row for that year. 2018's non-result is a *tight*, confident
null (±0.4%), not noise — a genuine, still-unexplained asymmetry (see AI Handoff above
for the political-science lead). Susceptibility/specific heat show the same low-T
pooling artifact as the ablation run (monotonic blow-up toward T→0, no interior bump) in
all three elections — no confirmed critical point anywhere in this project yet.
**Correction, 2026-08-21:** 2026's Pueblo Soberano is the direct electoral successor of
2022's Progreso Social Democrático (same Chaves-aligned movement, different registered
vehicle — confirmed via press coverage, not a coincidental resemblance) — the table above
listed them as if unrelated parties. See the "non-circular prior-election political
field" run further below for what this continuity actually buys predictively (less than
expected — only 79.1% sign-agreement between the 2022 runoff winner and 2026's winner at
the same node, i.e. real but limited spatial loyalty, not a clean repeat).

![Historical comparison](figures/historical_comparison.png)

---

### Run: geography-vs-predisposition ablation (`run_ablation.py`) — 2026-08-16

The key methodological run. Same 2026 coalition-split data as above, two configurations:
Run A `h=0` everywhere (pure geographic/neighbor-conformity coupling only) vs. Run B
`h`=vote margin (geography + individual predisposition), both scored with
`symmetric_alignment_fraction` (Run A's `h=0` makes the model's up/down labeling
arbitrary — see that function's docstring). Pools `N_SEEDS=8`.

**This run's own history is the headline finding.** A first single-seed pass reported a
clean +2.4-point alignment gap between A and B and clean interior susceptibility/
specific-heat peaks (~0.65 and ~1.55) — a tidy, publication-shaped result. Re-run with 8
pooled seeds, both effects evaporated:

| Parameter | Value |
|---|---|
| Temperatures | 24 points, linspace(0.05, 3.5) |
| MC | `n_equil=500`, `n_sweeps=500`, `N_SEEDS=8`, `n_jobs=8` |
| Wall-clock | ~35-40s (12-core local machine) |

**Final values (pooled, trustworthy):**
| Run | N | Baseline | Best alignment | Peak χ (location) |
|---|---|---|---|---|
| A: geography only (h=0) | 84 | 60.7% | 67.6%±5.5% at T=2.60 | 590.98 at T=0.05 (edge — artifact, see Notes) |
| B: geography + h (margin) | 84 | 60.7% | 68.8%±3.5% at T=1.55 | 429.28 at T=0.05 (edge — artifact) |

**Marginal contribution of predisposition over pure geography: +1.2 points — within
overlapping 1-sigma error bars, not distinguishable from zero.**

**Notes:** Two things this run taught the project, both now written into
`pooled_temperature_scan`'s docstring and `CLAUDE.md` gotcha #7:
1. A single-seed alignment gap can point the intuitive direction purely by chance
   (+2.4pp → +1.2pp once pooled, well inside the error bars either way).
2. At low T, independent MC chains can each freeze into a *different* metastable domain
   configuration rather than all finding the same one within `n_sweeps`. Pooling then
   mixes real thermal fluctuation with between-chain disagreement, and since χ/C both
   divide by T, that disagreement inflates into a spurious divergence at the low-T scan
   edge — not a real thermodynamic peak. A real critical point is an interior bump in
   the pooled curve, not a monotonic blow-up toward T=0. **Every real-data run in this
   project shows the latter** — no confirmed critical point/tipping point found yet
   anywhere in this project once MC noise is properly accounted for.

![Ablation comparison](figures/ablation.png)

---

### Literature: Zotero collection + PDF conversion — 2026-08-16

Not a simulation run — logged here since it closed out the novelty-check work above.

16 references from `NOVELTY_CHECK.md` §3 added to Zotero (Sociophysics ▸ IsingCR,
`BA4KBCB9`) via the Zotero Web API (full metadata pulled from Crossref). User then
manually sourced and attached all 16 PDFs, including Tiwari et al. 2021 (paywalled,
couldn't be accessed programmatically). Converted all 16 to Markdown with `marker`
Mode A (`--disable_ocr` — text/table layer only, no LaTeX; the right call here since
none are scanned and none need equation fidelity badly enough to justify Mode B's
~100x runtime).

**Fidelity:** spot-checked `korbel2026` and `siegenfeld2020` against `pdftotext -layout`
on the source PDFs — all numbers/units/signs correct. Systematic table-loss check across
all 16 (comparing marker's `tables_total` vs. `tables_pdftext` log stats against actual
markdown table syntax) found 4 papers with at least one fully-lost table body (caption
survived, data didn't): `korbel2026` (3 tables, including the one with real fitted
numbers — TABLE III, per-decade T*/hc/accuracy), `tiwari2021` (2 parameter-glossary
tables), `cascantematamoros2006` (1, electoral-calendar/index averages by year),
`dibenedetto2023` (1, appendix). Full detail in `papers_md/CONVERSION_NOTES.md`.

**Resolved the NOVELTY_CHECK.md S0 gate**: reading `tiwari2021` in full confirmed the
paper is purely synthetic (128×128/256×256 square lattice, no real geography, no real
election data) — exactly what the secondhand citation-context inference predicted.
`NOVELTY_CHECK.md` upgraded from CLEAN-pending-full-text to plain **CLEAN**.

---

### Analysis: McNemar significance testing + finite-size scaling — 2026-08-16

Prompted by mining the 16 converted papers for techniques this project hadn't tried yet.
Two additions, both now in `isingcr.simulation.observables` and covered by tests.

**McNemar's exact test** (`mcnemar_test`, `mcnemar_seed_summary`) — model vs. constant
majority-class null, following Korbel et al. 2025/26's own validation methodology
(NOVELTY_CHECK.md). Applied to `run_ablation.py` and `run_historical_comparison.py` at
each run's best T, per seed. Result: **the "beats baseline" story from the 1-sigma
heuristic is weaker than it looked.** Ablation: geography-only significant in only 2/8
seeds (median p=0.087), geography+h in 5/8 (median p=0.026). Historical comparison: 2018
stays a confident null (0/8 significant, matches the tight point estimate), but 2022 and
2026 — previously reported as "clearly beat baseline" — are significant in only 2/8 and
1/8 seeds respectively (median p=0.35, 0.37). Not evidence the effects are fake (N~84-500
McNemar tests have limited power for a 4-9-point effect), but "clearly beats baseline"
was an overstatement of what the data supports. README/CLAUDE.md updated with this
caveat everywhere the earlier framing appeared.

**Finite-size scaling** (`run_finite_size_scaling.py`) — Binder cumulant (`binder_cumulant`,
already implemented, previously unused) crossing between canton (N=84) and distrito
(N=488, `cri_admin3.shp`, first real use of the distrito-level shapefile in this project).
Needed a new `normalize_distrito_code` (canton_names.py) for the same province-capital
"CENTRAL" quirk one level down — 430/492 naive match → 489/492 after the fix → 490/492
after also fixing a stray-whitespace bug found in TSE's raw 2026 distrito field
(`load_tse_juntas_consolidado` now strips geography columns). Run at `h=0` deliberately
(Binder cumulant's standard interpretation needs a symmetric order parameter). Also fixed
a real numerical bug found along the way: `glauber_step` could overflow `exp()` at low T
with large `dE` (harmless result, noisy `RuntimeWarning`) — replaced with a numerically
stable sigmoid.

**Result: inconclusive.** 6 crossings across the scanned range (a real transition crosses
once), and the distrito curve dips below the physically-valid U4 range ([0, 2/3] at
equilibrium) at several T — meaning N=488 isn't equilibrating at the 500/500-sweep budget
that works fine for N=84, a standard finite-size-scaling issue (larger systems need
longer runs), not evidence against a real transition. See AI Handoff above: worth a
heavier re-run (more `n_equil`/`n_sweeps` for distrito specifically) before trusting
either "no transition" or a specific crossing T.

![Finite-size scaling](figures/finite_size_scaling.png)

---

### Analysis: why does 2018 differ from 2022/2026? — 2026-08-16

Answers the open question from the historical-comparison run. Two cheap, deterministic
diagnostics (`scripts/investigate_2018_anomaly.py`, ~7s total, no MC temperature scan
needed), added as a reusable `isingcr.utils.spatial_stats` module (`morans_i`,
`morans_i_test` — Moran's I with a permutation significance test).

**Ruled out: lack of geographic structure.** The pre-registered political-science lead
(PAC's 2018 support being unusually urban/GAM-concentrated, weakening geographic signal)
pointed the wrong direction. Moran's I on the real adjacency graph shows **2018 is the
*most* spatially clustered of the three elections** (I=0.706, p<0.001), not the least
(2022: I=0.485; 2026: I=0.354 — both still significant, just less so). Same story on the
continuous margin field. 2018's empirical map is *not* short on real geography to exploit.

**The actual explanation: energetics, not geography.** Every election's trivial
"everyone votes for the winner" configuration has lower energy than its true map (the
null being compared against) — but the *size* of that gap, normalized per canton, is
what differs: 2018 costs 1.13 energy units/canton relative to the trivial state, vs.
0.77 (2022) and 0.59 (2026) — 47%/92% higher. A temperature scan starting from random
spins gravitates toward whichever basin is energetically favored; when the true minority
pattern is this much more disfavored relative to the trivial alternative, random restarts
rarely find their way near it. Confirmed this isn't about truth being locally unstable —
a T=0 relaxation starting *at* the empirical 2018 map, pooled across 8 seeds (T=0 Glauber
isn't fully deterministic — a single-seed run had been used here before, corrected
2026-08-17 per an adversarial referee-panel review, see `referee_report_2026-08-17.md`),
keeps 90.1%+/-0.0% of it intact (actually the *most* stable of the three,
85.4%+/-0.0%/80.5%+/-4.3% for 2022/2026) — the problem is specifically
that nothing guides a random-start search into that basin in the first place.

Cleanly separates 2018 from 2022/2026 as a category, which was the actual open question;
doesn't rank 2022 vs. 2026 against each other (their E_gap/N doesn't match their relative
McNemar significance ordering, but that's a different, lower-priority question).

---

### Run: Finite-size scaling, heavy re-run (UCR HPC cluster) — 2026-08-16

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_finite_size_scaling_heavy.py` |
| Where | UCR HPC cluster, `shared` partition, node cn002, 32 CPUs (p-serial QoS cap) |
| n_equil / n_sweeps | 20000 / 20000 (40x the local 500/500 run) |
| n_seeds | 16 (vs. 8 locally) |
| Temperatures | 32, linspace(0.05, 3.5) |
| Wall time | 34m32s |
| Throughput (bench) | ~2.03 ms/sweep at distrito scale (N=488), 1 core |

**Final values:**
| Observable | Value |
|------------|-------|
| Negative U4 count (canton, N=84) | 0 (was several at 500/500) |
| Negative U4 count (distrito, N=488) | 0 (was several at 500/500) |
| Crossings found | 5 (T = 0.579, 0.846, 2.798, 3.072, 3.232) |

**Notes:** This is the heavier re-run flagged in the AI Handoff above. The headline
change is **not** the crossing count (still 5, still read as noise — a real transition
crosses once) but that both curves now equilibrate cleanly: 0 negative U4 values at
either N, vs. several before. That upgrades the verdict from "inconclusive, likely
undersampled" to a confident **no critical point found in the scanned range**, for 2026,
at either canton or distrito granularity, h=0. Consistent with every other pooled scan in
this project (run_ablation.py, run_historical_comparison.py) finding no interior
susceptibility/specific-heat bump once seed-pooling artifacts are accounted for — this
project has not found a confirmed thermodynamic phase transition anywhere yet.

![Finite-size scaling (heavy)](figures/finite_size_scaling_heavy.png)

---

### Run: Distrito-level ablation, 2026 (UCR HPC cluster) — 2026-08-16

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_distrito_ablation.py` |
| Where | UCR HPC cluster, `shared` partition, node cn002, 32 CPUs |
| n_equil / n_sweeps | 20000 / 20000 |
| n_seeds | 16 |
| Temperatures | 32, linspace(0.05, 3.5) |
| N (distrito, after dropping 2 island isolates) | 488 |
| Wall time | 56m56s (Run A ~34m, Run B ~23m) |

**Final values:**
| Run | Best alignment | @T | Peak χ | McNemar p (median) | sig/16 |
|-----|----------------|-----|--------|---------------------|--------|
| A: geography only (h=0) | 66.2%±6.4% | 2.83 | 957.6 | 0.1798 | 4/16 |
| B: geography + margin | 74.8%±4.2% | 0.61 | 449.5 | 0.0009 | 12/16 |

Majority-class baseline: 66.9%. Marginal contribution of `h` over pure geography:
**+8.7pp**.

**Notes:** This is the "among distritos there are severe differences" angle the user
flagged as the actually-interesting one for 2026 — first ablation run at distrito rather
than canton granularity. The result is a real contrast with the canton-level ablation
(+1.2pp, not distinguishable from zero, see AI Handoff/run_ablation.py history): at
distrito scale the gain from adding each unit's own vote margin is both **larger**
(+8.7pp vs. +1.2pp) and **far more statistically robust** (McNemar p=0.0009, 12/16 seeds
significant, vs. run_ablation.py's weaker canton-level McNemar read). Geography-only
alignment (66.2%) barely clears the 66.9% majority baseline at all, and its McNemar
significance is weak (4/16 seeds) — pure geographic contagion explains much less of the
real distrito-level pattern than it does at canton level, and predisposition (h) is doing
real, resolvable work at this finer granularity. Caveat: geography-only's peak χ sits at
T=2.83, well inside the range, but note both runs' *best-alignment* T (2.83 and 0.61) and
peak-χ T don't coincide — not read as a critical-point signal here (this scan wasn't run
at h=0, so the Binder-cumulant machinery above is the right tool for that question, not
this ablation). Not yet decomposed into *which* distritos geography-only gets wrong — see
AI Handoff for the IDS-2023 follow-up.

![Distrito ablation](figures/distrito_ablation.png)

![2018 anomaly explanation](figures/2018_anomaly.png)

---

### Run: 3D scan, geography x political field x MIDEPLAN social-development field — 2026-08-20/21

New two-field Hamiltonian `E(s) = -Σ J_ij s_i s_j - Σ(λ_pol h_i^pol + λ_soc h_i^soc) s_i`,
implemented as `combine_fields`/`two_field_energy` (`isingcr.simulation.two_field_energy`)
— deliberately does *not* touch `IsingModel`; a combined field collapses exactly to the
existing single-field engine, so this is physically exact, not an approximation.
`h^soc` = MIDEPLAN Índice de Desarrollo Social 2023, z-scored per distrito
(`isingcr.ingestion.mideplan_ids`), fetched via 6 regional Google-Sheets CSV exports
(`data/raw/mideplan_source/tabla{15..20}.csv` → `scripts/parse_mideplan_ids.py` →
`data/raw/mideplan_ids_2023.csv`, 490 rows/84 cantons, 0 missing, matches MIDEPLAN's own
stated coverage exactly).

| Parameter | Value |
|-----------|-------|
| Scripts | `scripts/run_3d_scan.py` (2026), `run_3d_scan_2022.py` (2022 runoff) |
| Where | UCR HPC cluster, `shared` partition, 32 CPUs/task |
| n_equil / n_sweeps / n_seeds | 20000 / 20000 / 16 |
| Grid | 5×5 (λ_pol, λ_soc ∈ [0, 2]) × 32 T, linspace(0.05, 5.0) |
| N (distrito) | 488 (2026) / 483 (2022, winner-vs-runner-up binarization) |

**Final values (λ_pol=0 row — isolates the social-development contribution):**
| Year | Geography-only (λ_soc=0) | Peak λ_soc | Best accuracy | Gain |
|------|---------------------------|-----------|----------------|------|
| 2026 | 67.64% (p=0.1985) | 1.5 | 74.42% (p=0.0147) | **+6.78pp** |
| 2022 | 62.46% (p=0.1481) | 0.5 | 63.59% (p=0.5312) | +1.13pp |

**Direct paired test** (`scripts/run_soc_paired_test.py`, `spatial_block_permutation_test_paired`,
canton blocks, geography-only vs. λ_soc-peak, each arm at its own best-T, 16 seed-pairs —
same head-to-head methodology `run_direct_paired_test.py` already established for
geography-vs-margin, since testing each arm only against the trivial majority baseline
was the referee-flagged gap that motivated that script):
- 2026: median p=**0.058**, significant in 8/16 seed-pairs — borderline real.
- 2022: median p=**0.405**, significant in 0/16 seed-pairs — clean null.

**λ_pol extension scan (0-8, λ_soc=0) — NOT a research result, see Notes:** accuracy
climbs 67.64%→92.70% and best-T drifts sharply low (2026: 2.605→0.369) as λ_pol grows
(`scripts/run_3d_scan.py`, `scripts/submit_3d_scan_polext_2026.slurm`, job 125832,
9-point array over λ_pol∈[0,8]/λ_soc=0/32 T, results in
`data/processed/scan_3d_polext_pol{0-8}_soc0.npz`). Checked this against the
metastable-freezing artifact (CLAUDE.md gotcha #7 — the classic failure this project has
been burned by twice before) with a targeted per-seed spread check: at a normal grid
point (λ_pol=2, T=0.848) 16 seeds spread std=2.5pp (mean=81.38%); at the concerning tail
(λ_pol=8, T=0.369) std=**0.6pp** (mean=92.58%) — *tighter*, not looser, agreement
(`data/processed/lambda_pol_circularity_perseed_2026.npz`). That rules out the artifact
(which predicts more disagreement, not less) and instead confirms field-dominance:
`sign(h^pol)` matches `spin_empirical` on 487/488 nodes (99.8%) by construction (h^pol is
derived from the same vote margin that defines the label), so a strong λ_pol just
reproduces its own input. Real MC behavior, but circular — not reported as a finding.

**Correction (2026-08-22):** this entry originally read "accuracy climbs 62-68%→81-82%,"
which was wrong — those numbers were 2022's extension range
(`scan_3d_2022_polext_pol{0..8}_soc0.npz`), not 2026's; no 2026 extension file existed on
disk at the time despite the manuscript citing 2026-specific numbers from it. Caught by
the round-3 referee panel (`referee_report_2026-08-22.md`, finding #1) and confirmed
independently before the fix: searched the whole filesystem, found no 2026 polext file.
The best-T trajectory claim (2.6→0.37) and the per-seed-spread claim (2.5pp→0.6pp) were
both already correct — only the accuracy-range numbers were mixed up between years. Fixed
by re-running the actual 2026 scan (above) rather than editing the text to hedge around
missing data.

**Notes:** the composite social-development effect is real-but-borderline for 2026 and a
clean null for 2022 — the *contrast* between years is the more defensible result than
either point estimate alone. Pure-political λ_pol=2.0 (82.36% 2026 / 70.10% 2022, both
significant) remains the strongest single field either year; adding social-dev on top of
the best political weight gives +0.00% in both years (the political field alone already
saturates what the model can capture once it's not near-tautological). See the axis
decomposition run below for which part of MIDEPLAN's composite actually carries the
2026 signal.

---

### Run: MIDEPLAN IDS axis decomposition — 2026-08-21

Follow-up to the run above: MIDEPLAN's composite IDS score is itself a blend of five
published sub-dimensions — SALUD (health), PARTICIPA (participation), SEGURIDAD
(security), EDUCACION (education), ECONOMICO (economic) — already sitting in the same
source tables, unused until now. `parse_mideplan_ids.py` extended to emit all five
(purely additive; `mideplan_ids_2023.csv` still 490/84/0-missing).

**Free correlation check first** (no MC, `--check-correlations`): 2026 — `economico`
tracks the outcome almost as well as the composite (r=-0.525 vs. -0.555); `seguridad` is
nearly orthogonal to every other axis (r=0.05-0.08) and weak against the outcome
(r=-0.21); `salud`/`educacion`/`economico` form a tightly intercorrelated
"development" cluster (r=0.51-0.69 pairwise). 2022 — correlations weaker across the
board (consistent with the composite's null), and `participa` leads (r=-0.377), not
`economico` — a different axis in each year.

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_mideplan_axis_screen.py` |
| Where | UCR HPC cluster, `mpi` partition (`shared`/`debug`/`lab` all found fully `drained` at submit time — external maintenance window, not a bug; `mpi` had 576 idle cores), 64 CPUs/task (`mpi`'s p-parallel QoS enforces a 64-core *minimum*) |
| Fixed weights | λ_pol=0 (isolates the axis), λ_axis=1.5 (matches the composite's own peak) |
| n_equil / n_sweeps / n_seeds / T-grid | 20000 / 20000 / 16 / 32 pts, linspace(0.05, 5.0) |
| Grid | 5 axes × 2 years = 10 tasks, ~30 min/task |

**Final values — paired significance vs. geography-only** (`scripts/run_axis_paired_test.py`,
same `spatial_block_permutation_test_paired` machinery, geography-only arm computed once
per year and reused across all 5 axes; Bonferroni α=0.05/5=0.01 since 5 axes = 5
hypothesis tests):

| Axis | 2026 acc | 2026 paired p | sig/16 | 2022 acc | 2022 paired p | sig/16 |
|------|----------|----------------|--------|----------|----------------|--------|
| educacion | 76.18% | 0.038 | 9/16 | 62.66% | 0.470 | 2/16 |
| economico | 74.88% | 0.050 | 8/16 | 62.45% | 0.395 | 3/16 |
| salud | 75.00% | 0.055 | 7/16 | 63.48% | 0.481 | 3/16 |
| seguridad | 70.65% | 0.617 | 3/16 | 65.59% | 0.345 | 3/16 |
| participa | 64.37% | 0.252 | 2/16 | 63.46% | 0.608 | 1/16 |

**Notes:** none of the five axes individually clears the Bonferroni bar — this is not a
single cleaner smoking-gun finding than the composite. But the pattern is informative:
`educacion`/`economico`/`salud` (the correlated "development" cluster from the free check)
sit in the same borderline band as the composite itself (p=0.038-0.055, 7-9/16 seed-pairs
— statistically indistinguishable *from each other*, the gaps between them are smaller
than this project's own measured seed-to-seed noise floor, ~0.6-2.5pp SE depending on the
point), while `seguridad` and `participa` show essentially no signal (p=0.25, 0.62).
`participa`'s own grid accuracy (64.37%) is actually *below* the geography-only baseline
(67.64%) despite having decent raw correlation with the outcome (r=-0.551 with h^pol) —
correlation with the raw covariate doesn't guarantee the MC dynamics translate it into
better classification. 2022 replicates the composite's clean null for every axis (no
exceptions) — whatever carries 2026's borderline signal is specific to that election, not
a general property of any one MIDEPLAN axis. **Known inefficiency, not yet fixed:** the
cluster script's own `MAX_CORES_PER_TASK` constant (borrowed from `run_3d_scan.py`, tuned
for `shared`'s 32-core cap) wasn't updated for the `mpi` move, so each task only used 32
of its 64 allocated cores — didn't block completion, just ran at `shared`-partition
speed despite the extra allocation; fix before reusing this script on `mpi` again.

---

### Run: non-circular prior-election political field, 2022 runoff → 2026 — 2026-08-21

Motivated by a factual correction: Pueblo Soberano (2026's leading party) is the direct
electoral successor of Progreso Social Democrático (PPSD, 2022's winner) -- same
Chaves-aligned movement, different registered vehicle, confirmed via press coverage
(El Observador CR, AmeliaRueda), not just a naming coincidence. Every `h^pol` used
elsewhere in this project is built from the SAME election's own vote margin it
predicts, which is the circularity behind the `run_3d_scan.py` extension result above.
This tests a genuinely non-circular alternative: **2022's PPSD-vs-PLN runoff margin**
as the sole political field for predicting real 2026 votes (single field, no `lambda`
weighting -- matches `run_distrito_ablation.py`'s Run B methodology exactly, just
swapping in a non-circular `h`). No new data acquisition (2022 runoff data already in
`data/raw/tse_juntas/`).

**Free correlation check first** (no MC): tested two candidate sources. 2022 **round 1**
(fragmented 25-candidate race) barely correlates with 2026 (r=0.147 with the outcome).
2022 **round 2** (the actual PPSD-vs-PLN runoff, already computed as `h^pol` by
`run_3d_scan_2022.py`) correlates strongly: r=0.704 with 2026's own margin, r=0.565 with
the 2026 outcome -- comparable magnitude to MIDEPLAN's composite IDS (r=-0.555). Used
round 2.

| Parameter | Value |
|-----------|-------|
| Scripts | `scripts/run_prior_margin_field.py`, `run_direct_paired_test.py` helpers |
| Where | UCR HPC cluster, `shared` partition, node cn002, 32 CPUs |
| n_equil / n_sweeps / n_seeds | 20000 / 20000 / 16 |
| Temperatures | 32, linspace(0.05, 5.0) |
| N (2026 distrito) | 488, with 2022 runoff margin joined on (6/488 missing -- h=0, not dropped) |

**Final values:**
| Field | Best accuracy | @T | McNemar p (vs. baseline) | Paired p (vs. geography-only) | sig/16 |
|-------|----------------|-----|---------------------------|-------------------------------|--------|
| Geography only (h=0) | 67.64% | 2.605 | 0.1985 | -- | -- |
| 2022 runoff margin (non-circular) | 69.79% | 2.924 | 0.2651 | **0.260** | **5/16** |

**Notes:** despite the promising raw correlation (r=0.565, similar magnitude to
MIDEPLAN's composite), this field **underperforms** MIDEPLAN's composite (paired
p=0.058, 8/16) and every individual "development cluster" axis from the run above
(educacion/economico/salud, p=0.038-0.055) once run through the actual MC dynamics.
Diagnosed why: `sign(2022 runoff margin)` matches 2026's actual winner on only **79.1%**
of distritos -- that's the real ceiling on what this field can deliver, vs. the circular
own-2026-margin field's 99.8% sign-match (by construction, see the run above). About 1
in 5 distritos changed which side they were on between the 2022 runoff and 2026's first
round, even though it's nominally the same movement continuing. The field is also
weaker in raw magnitude (std=0.167 vs. 0.280 for the own-margin field), compounding the
effect. **Reportable finding in its own right**: political loyalty for the same
movement was not as spatially stable from 2022 to 2026 as the "same coalition
returning" narrative would suggest -- geography and current-cycle-specific factors
evidently matter more here than raw historical partisan continuity. Like the MIDEPLAN
work above, not yet folded into the manuscript.

---

### Run: GAM (Gran Área Metropolitana) membership field — 2026-08-21

The strongest result of this whole covariate search. Motivated by the historical-
comparison section's own existing qualitative note (Section "Does the same model work
across election cycles?"): the winner's opposition/minority concentrates in and around
San José in every one of the three elections modeled -- never turned into an actual
field and tested until now. Unlike MIDEPLAN IDS (2023-only snapshot) or the prior-
election political field (2022-only, diluted by real allegiance shifts), GAM membership
is a **static administrative boundary** -- the same field applies unchanged to every
election year, no comparability caveat needed.

**GAM definition, and a real limitation, stated upfront:** 31 cantons across San José
(13), Alajuela (3: Alajuela, Atenas, Poás), Cartago (6), Heredia (9), per Plan GAM
2013-2030 (Decreto Ejecutivo 38145-PLAN-MINAE-MIVAH-MOPT-S-MAG, La Gaceta N°82, 30 abril
2014). This is a **canton-level proxy**, not the precise distrito-level boundary --
official sources describe the real GAM as "184 distritos, en algunos casos fracciones
de distritos," meaning the true boundary cuts through some cantons at the distrito
level and doesn't respect administrative distrito lines everywhere. The distrito-level
annex/shapefile could not be retrieved (MIVAH's site blocks automated access with a
403, a GeoNode GIS layer at a municipal geoportal refused the TLS connection outright,
an academic atlas PDF that looked promising is now login-gated). A second discrepancy
surfaced during the search: a different search result cited **157 districts/30
cantons** for something called "Anillo de Contención Plan GAM 82" -- almost certainly
the older 1982 boundary (a tighter urban containment ring), not the 2013-2030 boundary
used here. Two different official GAM delimitations exist depending on era; this run
uses the current one. `scripts/run_gam_field.py`'s docstring documents the full 31-canton
list and this limitation for anyone building on it.

**Free correlation check first** (no MC): the strongest of any field tried this
session. r=-0.589 with 2026's outcome (r=-0.653 with 2026's own margin); r=-0.277 with
2022's outcome (r=-0.387 with 2022's own margin) -- weaker than 2026 but still clearly
non-zero, unlike MIDEPLAN's essentially-null 2022 read. 186/488 (2026) and 184/483
(2022) distritos fall in GAM -- a reasonable, non-degenerate ~38% split. The underlying
magnitude is large: in 2026, only 31.7% of GAM distritos are on the leading (Pueblo
Soberano) side vs. 88.7% of periphery distritos (57.0pp gap); in 2022, GAM is an even
split (50.0%) vs. 76.9% in the periphery (26.9pp gap) -- 2026's divide is roughly double
2022's. (Logged here 2026-08-22 per referee finding: originally reported live in the
manuscript without a corresponding notebook entry; recomputed and reproduced exactly
from `build_graph_and_gam_field` in `scripts/run_gam_field.py`, no new MC run needed --
this is a free vote-share tabulation, not a simulation output.)

| Parameter | Value |
|-----------|-------|
| Scripts | `scripts/run_gam_field.py`, `run_direct_paired_test.py` helpers |
| Where | UCR HPC cluster, `shared` partition, node cn002, 32 CPUs/task, 2-task array |
| n_equil / n_sweeps / n_seeds | 20000 / 20000 / 16 |
| Temperatures | 32, linspace(0.05, 5.0) |
| Field | h = +1 if canton in the 31-canton GAM list, else -1 (symmetric, single field, no `lambda` weighting -- matches `run_distrito_ablation.py`'s Run B / the prior-margin-field run above) |

**Final values:**
| Year | Geography-only | GAM field | Gain | Paired p (vs. geography-only) | sig/16 |
|------|-----------------|-----------|------|-------------------------------|--------|
| 2026 | 67.64% @ T=2.605 | **81.07%** @ T=1.008 | **+13.4pp** | **0.0005** | **15/16** |
| 2022 | 62.46% @ T=3.563 | 67.16% @ T=1.008 | +4.7pp | 0.239 | 4/16 |

**Notes:** for 2026 this is a real, robust, decisive result -- stronger correlation,
stronger accuracy gain, and dramatically stronger paired significance than MIDEPLAN's
composite (p=0.058, 8/16), every individual MIDEPLAN axis (best was educacion at
p=0.038, 9/16), or the non-circular prior-election political field (p=0.260, 5/16).
15/16 individually-significant seed-pairs is essentially unambiguous by this project's
own standard, a first for any non-circular field tested here. 2022 again shows the same
now-familiar pattern: real point-estimate gain (+4.7pp) that does not survive the
paired test (p=0.239) -- whatever is driving 2026's strong result is specific to that
election, consistent with every other covariate tried this session. **Caveat repeated
deliberately**: the canton-level GAM proxy over-includes a handful of large, mostly-
rural cantons that only partially qualify under the real boundary (Atenas, Aserrí,
Paraíso, etc.) -- getting the true distrito-level boundary (or the GIS shapefile
itself) would let this be re-run more precisely; worth doing if this result is used for
anything beyond an exploratory finding. Not yet folded into the manuscript, same status
as the MIDEPLAN and prior-margin-field runs above.

---

### Analysis: GAM domain-wall (which distritos does the field get wrong) — 2026-08-21

The first analysis this session to use the model's spatial-coupling structure itself,
not just fit another covariate. Question: does geography+GAM's ~19% error rate
concentrate at the *interface* between GAM and periphery -- distritos pulled between
"agree with your GAM-status field" and "agree with a differently-labeled neighbor" --
or is it scattered randomly? Only a spatially-coupled model can even pose this
question. Free (no new MC config): reused the exact spin configurations from the GAM
paired test (T=1.008, 16 seeds, `scripts/run_gam_domain_wall_analysis.py`), computing
each distrito's per-seed error rate and flagging it "boundary" if any `J`-neighbor has
the opposite GAM status.

**Confirmed the hypothesis, then found something richer:**

| | Boundary (n) | Interior (n) |
|---|---|---|
| **GAM** | 47.0% error (35) | 27.5% error (151) |
| **Periphery** | 30.8% error (44) | **9.6% error (258)** |

Boundary distritos overall: 38.0% error vs. interior's 16.2% -- more than double, the
expected domain-wall signature. But the four-way split shows an asymmetry: periphery-
interior is by far the model's most confident category (9.6% error), while GAM-interior
is still notably error-prone (27.5%) *even away from any boundary* -- periphery support
is far more internally uniform than GAM opposition is.

**The top-error list (many distritos wrong in all 16/16 seeds) pointed somewhere
specific**: Pavas, Los Guido (Desamparados), Purral (Goicoechea), León XIII/Cinco
Esquinas (Tibás), most of Alajuelita, Mora's rural fringe -- well-known working-class/
lower-income neighborhoods *inside* GAM, voting like periphery despite being
geographically in the capital region. Checked directly against MIDEPLAN's economic axis
(already ingested, no new data): within GAM only, error rate correlates with the
economic axis at r=-0.391 (participation: r=-0.308; health: r=-0.192; education/
security: ~0). High-error GAM distritos (error>=0.5, n=55) average an economic score of
54.4 vs. 65.1 for low-error GAM distritos (n=130; GAM-wide mean 61.9).

**Notes:** the GAM/periphery divide that drove the strong result above isn't a clean
geographic split -- it substantially overlaps with a within-capital economic
marginalization pattern. The *between*-region GAM-vs-periphery signal (r=-0.589
overall) is real and strong, but part of what the coarse binary is picking up is "poor
core neighborhoods vote like periphery," not distance-from-capital per se. Doesn't
undercut the GAM result's significance (that's about prediction accuracy gained, not
mechanism) but does sharpen what "GAM matters" actually means. Raw per-distrito data:
`data/processed/gam_domain_wall_analysis_2026.csv`.

**2022 repeat (`--year 2022` flag added to the script, 2026-08-21): same physics,
different story.** The boundary-vs-interior gap replicates -- boundary 51.0% error vs.
interior 29.7% (2026: 38.0% vs. 16.2%) -- confirming the domain-wall effect isn't a
2026 fluke, it's a structural feature of the model whenever a field organizes the
system at all. Four-way breakdown keeps the same ordering (GAM-boundary worst at
60.4%, periphery-interior best at 20.2%) but every number is uniformly higher, matching
2022's much weaker overall GAM signal (67.16% vs. 62.46% baseline, not significant --
see the run above).

**But the top-error list has an almost entirely different composition.** 2026's was
dominated by GAM=True (poor capital-region neighborhoods voting like periphery); 2022's
19/20 top-error distritos are GAM=**False** -- remote coastal Nicoya-peninsula
Puntarenas (Lepanto, Paquera, Acapulco, Arancibia, Guacimal) and northern
Guanacaste/Nicaragua-border cantons (La Cruz, Hojancha, Tilarán, Nandayure), plus rural
Puriscal. The economic-axis relationship that explained 2026's pattern is much weaker
here too: within-GAM error-vs-economico correlation drops from r=-0.391 (2026) to
r=-0.263 (2022, same direction, muted); within-periphery it's weaker still (r=-0.159),
while participation shows a positive correlation instead (r=0.362, opposite sign from
any 2026 pattern). So 2022's confusion looks driven by geographic remoteness/border-
coastal character specifically, not a clean economic gradient the way 2026's was.
**Bottom line**: the domain-wall structure (boundaries are harder than interiors) is a
general, reproducible property of this model whenever a field is present -- but *which*
specific places get confused, and *why* (economic marginalization vs. geographic
remoteness), is election-specific, same as every other covariate result this session.
Raw data: `data/processed/gam_domain_wall_analysis_2022.csv`.

---

### Analysis: GAM susceptibility/crossover scan, 2026 — 2026-08-21

Second physics-native follow-up (alongside the domain-wall analysis above). Question:
`run_gam_field.py` found the GAM field's best accuracy at T=1.008, well below
geography-only's T=2.605 -- does that reflect a genuine crossover between a
geography-dominated and a field-dominated regime, characterizable via susceptibility
chi(T)/specific heat C(T), or just a single favorable point?

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_gam_susceptibility_scan.py` |
| Where | UCR HPC cluster, `shared` partition, node cn002, 32 CPUs |
| n_equil / n_sweeps / n_seeds | 20000 / 20000 / 16 |
| Temperatures | 32, linspace(0.05, 5.0), same grid as `run_gam_field.py` |

**Result: no real crossover found -- an honest null, same verdict as every other
susceptibility/Binder-cumulant scan in this project.** chi and C both rise
*monotonically* toward the scan's low-T edge (chi: 0.10 at T~1.0 -> 116.4 at T=0.05; C:
0.14 -> 6843.3), never turning over into an interior peak. This is exactly the known
between-chain-disagreement artifact (CLAUDE.md gotcha #7) -- a real thermodynamic
signature is an *interior* bump, not a monotonic blow-up toward T=0, and this project
has now checked for one under h=0 (finite-size-scaling runs) and now under a real,
strong field (this run) without finding one either way. **The one genuinely
well-behaved curve is classification accuracy itself**, which has a smooth, real
interior maximum at T=1.008 (81.07%) -- but that's an empirical-match quantity, not a
thermodynamic one, and doesn't imply a genuine phase transition or crossover exists.
**Conclusion**: "GAM's best-T is lower than geography-only's" is a real fact about
where the model best reproduces the map, but there's no confirmed thermodynamic
crossover behind it -- extends this project's standing null (no confirmed critical
point/phase transition found anywhere, across every h=0 and now h!=0 scan run so far)
rather than overturning it. Raw data: `data/processed/gam_susceptibility_scan_2026.npz`.

---

### Analysis: GAM polarization trend, 2018/2022/2026 (canton-level) — 2026-08-21

Third physics-native follow-up: does Costa Rica's capital-vs-periphery divide look
sharper or weaker across successive elections? Canton-level (not distrito), reusing
`run_historical_comparison.py`'s exact election-loading machinery and canton-scale MC
budget (n_equil=n_sweeps=500, 8 seeds -- that script's own validated-sufficient budget
for N~84, no need for distrito-scale 20000/20000). A bonus of canton level: GAM's
31-canton list applies *exactly* here, no partial-inclusion imprecision (unlike the
distrito-level proxy used in every GAM run above).

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_gam_polarization_trend.py` (local, ~similar wall-clock to `run_historical_comparison.py`'s ~66s) |
| Elections | 2018 ronda2, 2022 ronda2, 2026 round 1 (same as `run_historical_comparison.py`) |
| Paired test | `spatial_block_permutation_test_paired`, **province-blocked** (7 blocks -- matches `run_direct_paired_test.py`'s canton-level convention; canton-level blocks would be degenerate at this granularity) |

**Final values:**
| Election | Raw GAM-periphery gap | Geography-only | Geography+GAM | Gain | Paired p | sig/8 |
|----------|------------------------|-----------------|-----------------|------|----------|-------|
| 2018 | 38.0pp | 72.69% @ T=0.65 | 63.12% @ T=0.35 | **-9.6pp** | 0.7978 | 0/8 |
| 2022 | 52.1pp | 66.31% @ T=2.75 | 79.88% @ T=0.65 | +13.6pp | 0.2162 | 0/8 |
| 2026 | 47.3pp | 76.49% @ T=2.30 | 83.04% @ T=1.25 | +6.6pp | 0.1962 | 0/8 |

**Notes, two separable findings:**
1. **The raw magnitude trend is real and model-independent**: 38.0pp (2018) -> 52.1pp
   (2022) -> 47.3pp (2026) -- a sharp jump in the capital/periphery vote-share gap
   after 2018, staying elevated since. Consistent with 2018 already being established
   as a categorically different election (see the 2018-anomaly analysis above).
2. **None of the three years reach paired significance at canton level (0/8 each) --
   including 2026, which was p=0.0005/15/16 at distrito level.** Not read as
   contradicting that result: this is the exact granularity pattern already documented
   once before in this project (the original margin ablation: +8.7pp/significant at
   distrito vs. +1.2pp/not-significant at canton). Two compounding reasons specific to
   this test: only 7 province blocks (the coarsest blocking this project has used --
   its own spatial-block-sensitivity check already showed coarser blocking washes out
   significance the most) and N~84 nodes is a small sample for an effect that showed up
   cleanly across N~488 distritos. **2018 is stranger still**: GAM's raw signal is
   *maximal* there (100% of GAM cantons on one side vs. 62% in periphery) yet
   geography+GAM performs *worse* than geography alone (-9.6pp) -- plausibly connects to
   2018's already-documented energetic anomaly (its true map costs 47-92% more energy
   relative to the trivial state than 2022/2026's do), so forcing a uniform GAM field on
   top of an already-hard-to-find pattern may fight the geographic contagion rather than
   help it, within this lighter canton-scale budget. **Not yet attempted**: the true
   distrito-level 2018 version, which would need 2018's different geographic reporting
   unit ("distrito electoral," not the administrative distrito used since) reconciled
   first -- nontrivial, not done. Raw data: `data/processed/gam_polarization_trend.npz`.

---

### Analysis: population confound check (registered voters per distrito) — 2026-08-21

Checked whether the domain-wall error patterns above are just small-sample noise, and
whether GAM itself is confounded with population density. First attempt used the
padrón electoral files (`data/raw/tse_padron/`, both years already downloaded) --
**dead end, documented so it isn't retried**: the padrón's own `distelec.txt` geographic
units are finer than this project's administrative distritos (individual neighborhoods
like "Barrio México," "Barrio Luján," plus foreign consulates show up as separate
units) -- only 355/488 nodes matched by name, not a safe join. Pivoted to a source
already used throughout this project instead: the vote-results consolidado CSVs'
`electores_inscritos` (registered voters) column, aggregated per junta -> distrito the
same way `load_tse_juntas_consolidado` already does -- 488/488 and 488/483 matched
exactly, since it's the same aggregation this whole project's graphs are built from.

**Check 1 -- error rate vs. population: cleared, no confound.** r(error_rate,
population) = 0.029 (2026) / -0.012 (2022); r with log(population) = -0.016 / -0.139 --
negligible either way. High- and low-error distritos have nearly identical median
population in both years (2026: 4188 vs. 4852; 2022: 3807 vs. 4803). The poor-GAM-
neighborhood pattern (2026) and remote-periphery pattern (2022) from the domain-wall
analysis above are **not** small-sample-size artifacts.

**Check 2 -- GAM status vs. population: a real, moderate confound, worth stating
plainly.** GAM distritos have roughly double the median population of periphery ones,
in *both* years identically: 7300 vs. 3612 (2026), 7180 vs. 3404 (2022); r(is_gam,
log(population)) = 0.346 in both years. Part of what "GAM" captures is genuinely
"more populous/urban," not purely "closer to the capital" -- unsurprising (urban
density and capital-proximity co-occur in real geography) but means the GAM result
shouldn't be read as a clean geographic-distance effect in isolation; population
density is riding along with it. Doesn't undercut the paired-significance result (that
measures real predictive power beyond geography, regardless of mechanism) but sharpens
what it should be described as. Raw data: `data/processed/registered_voters_{2026,2022}.csv`.

---

### Note: how much the canton-level GAM proxy's imprecision actually matters — 2026-08-21

Follow-up to the "problematic cantons" discussion above (which specific distritos the
canton-level proxy likely misclassifies -- Mora's rural fringe, large cantons like
Alajuela Central/Paraíso/Aserrí flagged as most at-risk, general geography reasoning
only, not verified against the real boundary). Worked out where that imprecision
actually has teeth and where it doesn't, since the two results built on GAM aren't
equally exposed.

**The headline significance result (p=0.0005, 15/16, +13.4pp) is essentially immune.**
The proxy's aggregate count (186 distritos) is very close to the official true-boundary
count (184) -- the mismatch is probably ~10-15 distritos out of N=488, concentrated in
a few large rural cantons. A result with this much headroom (p=0.0005 is nowhere near
the 0.05 line) cannot plausibly be flipped by relabeling a dozen nodes. Contrast with
MIDEPLAN's composite (p=0.058, right at the edge) where this kind of imprecision would
matter far more -- it just doesn't apply there since MIDEPLAN isn't proxy-based.

**The domain-wall analysis's specific-distrito narrative is meaningfully more exposed,
and one piece of its interpretation should be walked back.** That analysis is directly
about classifying *individual* distritos and naming specific places as interesting
cases -- exactly where a dozen mislabeled nodes matters. The Mora trio cited there
(Guayabo, Quitirrisí, Piedras Negras) as evidence of "poor neighborhoods within GAM
voting like periphery" are precisely the kind of rural canton-fringe distritos most
likely to be proxy misclassifications in the first place -- if they're actually
periphery, not GAM, that piece of the "within-GAM economic marginalization" story isn't
a socioeconomic finding at all, it's the proxy failing on the exact nodes it was always
going to fail on. **Revision**: the within-GAM economic-marginalization pattern (r=-0.391
correlation with the economic axis, restated here for context) should be treated as
*plausible but not cleanly established* -- some fraction of the highest-error "GAM"
distritos driving that correlation may just be mislabeled periphery, not genuine
capital-region economic outliers. Doesn't affect the *between*-region GAM-vs-periphery
result or its significance; does affect confidence in the specific *within*-GAM
mechanism story. Getting the real distrito-level boundary (still not retrieved) would
resolve this cleanly; not done given the headline result doesn't need it.

---

### Analysis: multistability check (does the model have a unique equilibrium?) — 2026-08-21

Prompted by a fair challenge: most of this session's covariate work (MIDEPLAN, prior-
margin, even GAM's headline correlation) can be argued nearly as well from raw vote
margins alone -- a spatial-lag regression would show similar results faster. This is
the first analysis this session that asks something genuinely inaccessible to a
regression: does the real network + GAM field have a *unique* equilibrium, or does the
same physical setup settle into different answers depending on nothing but random
initialization (multistability)? Free -- pure reanalysis of the domain-wall CSVs
already on disk (`error_rate` per node across 16 independently-seeded runs at the GAM
field's best-T), no new MC. `multistability := min(error_rate, 1-error_rate)`: 0 means
all 16 seeds agree with each other regardless of whether they're right; 0.5 means an
even 8-8 split.

**Most of the map is a robust, essentially unique equilibrium.** 73.4% (2026) / 78.3%
(2022) of distritos are fully locked (multistability=0). Only 1.0% (2026) / 1.9%
(2022) show real multistability (>=4/16 minority seeds). Mean multistability score
0.023 / 0.021 -- low. For most of the country, geography + GAM pin down one outcome
regardless of noise or starting point; the real map's shape isn't a coin flip for the
vast majority of nodes -- a statement no regression coefficient can make.

**Multistability concentrates hard at the boundary, sharpening the domain-wall
finding.** Boundary distritos: mean multistability 0.054 (2026) / 0.067 (2022) vs.
interior's 0.017 / 0.011 -- a 3-6x gap. Fully-locked share drops from ~80% (interior)
to ~55% (boundary). This distinguishes two different kinds of boundary error the plain
error-rate number alone couldn't: some boundary distritos are *consistently, confidently
wrong* (locked onto the wrong answer every run -- systematic bias), others are
*genuinely undecided* (settling into different answers on different runs -- real
dynamical ambiguity).

**Cross-year consistency in the specific list is the strongest evidence this is
structural, not noise.** `SAN JOSE|MORA|TABARCIA` and `SAN JOSE|ASERRI|MONTERREY` are
both highly multistable in *both* 2026 and 2022 independently; `SAN JOSE|ACOSTA|
PALMICHAL` hits a literal exact 8-8 split in 2022. All mountainous fringe cantons at
the metro area's southern edge -- exactly where a gradual, genuinely ambiguous
GAM/periphery transition would be expected rather than a sharp administrative line.
Also refines the earlier proxy-imprecision caveat: Tabarcia specifically looks like a
genuine dynamical multistability case, not a mislabeled-canton artifact like the
Guayabo/Quitirrisí/Piedras Negras cases flagged above -- worth distinguishing "boundary
error from proxy imprecision" from "boundary error from genuine multistability," not
treating all high-error GAM-adjacent distritos as the same kind of problem.

---

### Analysis: counterfactual temperature-sensitivity sweep — 2026-08-21

Second genuinely model-native follow-up (after the multistability check above). Fixes
the real 2026 network and the real GAM field, then asks something a regression
literally cannot answer: how much would the equilibrium map have looked different if
collective conformity pressure (T) had been higher or lower than what best matches
reality (T=1.008)? Requires actually re-simulating the dynamical system at different
temperatures and measuring how the equilibrium itself shifts, not fitting a
coefficient.

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_gam_counterfactual_sweep.py` |
| Where | UCR HPC cluster, `shared` partition, node cn002, 13 CPUs (sized to match -- `pooled_temperature_scan` parallelizes over T, and only 13 T points were used, so requesting the usual 32 would have wasted 19 cores) |
| n_equil / n_sweeps / n_seeds | 20000 / 20000 / 16 |
| Temperatures | 13, curated (not the full 32-point grid -- this question needs the *shape* of the sensitivity curve, not every point) |
| Metric | fraction of distritos whose per-node majority-vote spin (across 16 seeds) differs from the T=1.008 reference map's majority-vote spin, using `symmetric_alignment_fraction` for the Z2-safe comparison |

**Final values:**
| T | Accuracy | Frac. flipped vs. T=1.008 reference |
|---|----------|----------------------------------------|
| 0.05 | 73.04% | 2.9% |
| 0.689 | 80.02% | 0.6% |
| 1.008 (reference) | 81.24% | 0.0% |
| 1.327 | 80.57% | 0.0% |
| 2.605 | 77.92% | 1.2% |
| 3.563 | 74.35% | 4.5% |
| 5.0 | 70.75% | 10.9% |

(full 13-point table in `data/processed/gam_counterfactual_sweep_2026.npz`)

**Notes:** the real map is remarkably robust across a wide range of social temperature
-- divergence from the reference grows smoothly and symmetrically as T moves away from
1.008 in either direction, but stays small even at extremes (2.9% at T=0.05, only
10.9% even at T=5.0, 5x the best-fit T). For the large majority of distritos, the
outcome looks strongly determined by geography+GAM rather than finely tuned to hitting
exactly the right amount of social noise -- consistent with, and complementary to, the
multistability check above (that showed robustness across random seeds at *fixed* T;
this shows robustness across *different* T entirely). Accuracy itself peaks smoothly
at T=1.008 and decays gracefully on both sides, same non-critical shape as every
susceptibility/accuracy curve in this project -- no sharp transition, consistent with
"no confirmed critical point anywhere in this project" holding here too.

**Why this matters for the "does this need the Ising model" question**: this and the
multistability check above are the first two analyses this session that are
*structurally* inaccessible to a vote-margin comparison or regression -- both required
actually re-running the coupled dynamical system (different random seeds; different
temperatures) and measuring how the *equilibrium itself* moves, not fitting a
coefficient to one dataset. The covariate-hunting work earlier in this session (MIDEPLAN,
GAM's headline correlation, prior-margin field) is legitimate and rigorous but could
mostly be reproduced by spatial-lag regression; these two cannot.

---

### Analysis: temperature-fragile/boundary cross-check + single-node cascade test — 2026-08-21

Third and fourth model-native follow-ups, both prompted by the same push-back as the
two above: do these findings need the Ising model, or could vote margins alone show
them?

**Cross-check (free, no new MC)**: does the counterfactual sweep's set of temperature-
fragile nodes (flip between T=0.05/T=5.0 and the T=1.008 reference) overlap with the
domain-wall's boundary/multistable flags? Real but partial overlap: 66 nodes are
temperature-fragile; boundary rate among them is 27.3% vs. 14.5% among temperature-
stable nodes (~2x enrichment), mean multistability 0.041 vs. 0.020 (~2x). Not a clean
1:1 match -- most temperature-fragile nodes aren't boundary-flagged. Revealed a new,
distinct category: some nodes (e.g. `SAN JOSE|MORA|PIEDRAS NEGRAS`) are perfectly
locked across random seeds at fixed T (multistability=0) but still flip when T itself
changes -- temperature-fragility and seed-multistability are related but not
identical kinds of uncertainty. Also surfaced a cluster of far-flung, low-degree
Talamanca/Limón coastal nodes that only flip at the extreme T=5.0 edge -- plausibly
just noise-sensitivity from sparse connectivity, not genuine GAM-boundary tension;
worth not lumping in with the substantive boundary cases.

**Single-node cascade test**: pick a distrito, flip its individual GAM field value,
re-equilibrate the whole real network at T=1.008, count how many *other* distritos'
equilibrium spin changes vs. the unperturbed baseline (reusing the counterfactual
sweep's saved reference map). 10 candidates curated to span every category surfaced so
far: genuinely multistable fault lines, seed-locked-but-temperature-fragile, locked-
but-consistently-wrong (`SAN JOSE|CENTRAL|PAVAS`, highest-population GAM distrito), and
locked+correct high-population controls on both the GAM and periphery sides.

| Parameter | Value |
|-----------|-------|
| Script | `scripts/run_gam_cascade_analysis.py` (local, 12 cores) |
| n_equil / n_sweeps / n_seeds | 20000 / 20000 / 16, T=1.008 fixed |

**Two real bugs hit and fixed during this run, worth documenting so they aren't
repeated**: (1) the first version called `pooled_temperature_scan(..., [T], n_seeds=16,
...)` -- `pooled_temperature_scan`'s own seed-loop is a plain Python list
comprehension, NOT parallelized; only the *temperatures* list inside each replicate
is, via `n_jobs`. With a single-element temperatures list this silently ran all 16
seeds sequentially on 1 core (~950-980s/candidate instead of ~300s) -- same
`min(cores, n_temperatures)` trap as the MIDEPLAN axis screen's `mpi`-partition
inefficiency logged above, different manifestation. Fixed by switching to
`temperature_scan(J, h, [T]*n_seeds, ..., n_jobs=...)`, the same pattern
`run_direct_paired_test.py`'s `best_t_final_spins_aligned` already used correctly
throughout this project -- should have reused that pattern from the start rather than
reaching for `pooled_temperature_scan`. (2) A variable-name collision (`results` used
for both the per-candidate scan output and the cross-candidate summary accumulator)
silently discarded the accumulator every iteration, and `nodes` turned out to be a
plain list (not ndarray), crashing on boolean-array indexing in the results printout.
Both fixed; verified with a syntax check and a reduced-budget timing test before the
real run.

**Final values, ranked by cascade size:**
| Target | Category | Cascade size |
|--------|----------|----------------|
| `CARTAGO\|PARAISO\|OROSI` | multistable + boundary + temp-fragile | **4** |
| `SAN JOSE\|ACOSTA\|PALMICHAL` | multistable + boundary | **1** |
| `SAN JOSE\|MORA\|TABARCIA` | multistable (top overall) | 0 |
| `SAN JOSE\|ASERRI\|MONTERREY` | multistable | 0 |
| `SAN JOSE\|MORA\|PIEDRAS NEGRAS` | seed-locked, temp-fragile | 0 |
| `SAN JOSE\|CENTRAL\|PAVAS` | locked, consistently wrong | 0 |
| `SAN JOSE\|CENTRAL\|HATILLO` | locked, temp-fragile | 0 |
| `HEREDIA\|CENTRAL\|SAN FRANCISCO` | locked+correct GAM control | 0 |
| `GUANACASTE\|LIBERIA\|LIBERIA` | locked+correct periphery control | 0 |
| `SAN JOSE\|PEREZ ZELEDON\|SAN ISIDRO DE EL GENERAL` | locked+correct periphery control | 0 |

**Notes -- a genuinely surprising, clean result**: 8/10 perturbations, including the
single most dynamically-uncertain distrito in the entire network (Tabarcia), produce
*zero* downstream effect on any other distrito. Only the two candidates flagged by
*multiple* independent diagnostics (both multistable and boundary; Orosí additionally
temperature-fragile) propagate at all, and even then only to immediately adjacent
distritos (1 and 4 nodes respectively) -- not a spreading cascade. **The real network
absorbs local political shocks rather than amplifying them.** This is the third
independent line of evidence (after the multistability check and the counterfactual
sweep) converging on the same picture: the real 2026 map is a robustly-determined
equilibrium for the vast majority of the country, with genuine uncertainty concentrated
in a small, specific, geographically-identifiable set of fault-line distritos that
mostly stay contained even when directly triggered. None of this -- the cascade
question itself, or the finding that it doesn't happen -- has any analog in a vote-
margin comparison; it required literally re-equilibrating the coupled system under a
perturbation and observing what does and doesn't move.

### Analysis: GAM lambda_soc scan (optimal field-to-coupling ratio; peak vs. saturation) — 2026-09-02

**Script**: `scripts/run_gam_lambda_scan.py` (SLURM: `scripts/submit_gam_lambda_scan.slurm`, UCR
`shared`, job 126956, 9 array tasks, ~30 min each, no restarts). **Data**:
`data/processed/gam_lambda_scan_2026_lam{0..8}.npz` (each saves the 16 best-T final spin
configurations, so the energy decomposition below needs no re-run). Budget identical to
every headline run (16 seeds, 20000+20000 sweeps, 32 T in [0.05, 5.0]). Closes the gap the
Supplementary Material stated explicitly: GAM had only ever been run unweighted (lambda=1).

| lambda_soc | best alignment | T* | McNemar median p | \|E_J\| | \|E_h\| | field share | follows field |
|---|---|---|---|---|---|---|---|
| 0.25 | 73.09% ± 4.57% | 1.647 | 3.6e-4 | 1218 | 69 | 0.053 | 78.1% |
| 0.50 | 76.05% ± 2.33% | 1.168 | 2.7e-4 | 1241 | 198 | 0.138 | 90.7% |
| 0.75 | 80.06% ± 1.04% | 1.168 | 2.8e-6 | 1245 | 341 | 0.215 | 96.6% |
| 1.00 | 81.07% ± 0.45% | 1.008 | 4.4e-7 | 1248 | 472 | 0.274 | 98.4% |
| **1.50** | **81.47% ± 0.20%** | 0.848 | 1.8e-7 | 1251 | 722 | 0.366 | 99.3% |
| 2.00 | 81.38% ± 0.12% | 0.848 | 2.6e-7 | 1249 | 966 | 0.436 | 99.5% |
| 3.00 | 81.24% ± 0.26% | 1.647 | 2.9e-7 | 1245 | 1449 | 0.538 | 99.5% |
| 4.00 | 81.15% ± 0.00% | 0.529 | 4.3e-7 | 1244 | 1944 | 0.610 | 99.8% |
| 8.00 | 80.97% ± 0.07% | 2.285 | 6.8e-7 | 1235 | 3902 | 0.760 | 100.0% |

(lambda=0 baseline 67.64%. lambda=1 row reproduces `gam_field_2026.npz`'s headline exactly under
the same seeds -- consistency check passes. "Field share" = |E_h|/(|E_J|+|E_h|) over best-T
spins; "follows field" = fraction of nodes with s_i = sign(h_GAM_i) up to global Z2.)

**Findings**:
1. **Finite peak, lambda* = 1.5** -- NOT the monotonic climb the circular own-margin field showed
   under the same extension (67.64% -> 92.70% toward a 99.8% ceiling). GAM rises to ~81.5%
   then declines slowly to 80.97% at lambda=8. Since h_GAM = ±1 and mean J = 1, lambda* IS the
   field-to-coupling ratio: **the capital/periphery divide is worth ~1.5 units of mean
   neighbor contagion.** At lambda*, the field carries 37% of equilibrium energy, coupling 63%.
2. **The plateau is GAM's structural ceiling.** 80.9% of distritos sit on the side of the 2026
   split GAM predicts. By lambda ~1.5 the equilibrium follows the field on >99% of nodes, so
   accuracy is pinned there; the decline past lambda* is the coupling term losing its ability
   to fix the remaining ~19%. Genuine-field signature (bounded relationship to the outcome),
   opposite of a label leak.
3. **Peak is shallow**: +0.4pp over lambda=1 (~1 sigma); everything in [1, 8] is within 0.5pp
   of the peak. Headline +13.4pp (at lambda=1) is therefore slightly conservative (+13.8 at
   lambda*), and the GAM-vs-MIDEPLAN comparison is now controlled for optimization budget in
   GAM's favor.
4. T* well-determined on the rising flank (1.65 -> 0.85), ill-determined on the plateau
   (jumps 0.53-2.29 for lambda >= 3) -- flat in lambda implies nearly flat in T.

**Manuscript**: new paragraph in the GAM section (main.tex), one sentence each in Abstract and
Conclusion (hierarchy: resolution > field choice > magnitude), full table + discussion in
supplementary.tex "GAM: lambda_soc scan and population confound detail". Also incidental
during this run: VPN dropped mid-job and openconnect's vpnc-script left UCR's internal
nameservers in /mnt/wsl/resolv.conf -- restore `nameserver 172.31.192.1` (or let WSL
regenerate) before reconnecting, or nothing resolves including the gateway.

### Note: why GAM does not replicate in 2022 -- the ceiling is the baseline — 2026-09-03

Free computation, no MC (`build_graph_and_gam_field` for both years; sign-agreement ceiling
= max over global Z2 orientation of the fraction of units with s_emp = sign(h_GAM)):

| year | N | GAM on leading side | periphery on leading side | gap | GAM ceiling | majority baseline | headroom |
|---|---|---|---|---|---|---|---|
| 2026 | 488 | 31.7% | 88.7% | 57.0 | 80.9% | 67.01% | **+13.9** |
| 2022 | 483 | 50.0% | 76.9% | 26.9 | 66.7% | 66.67% | **+0.0** |

In 2022 a ±1 GAM field cannot beat the trivial majority class even in principle -- the capital
split 50/50 in the runoff, so the side GAM predicts contains exactly the majority-class units and
nothing more. In 2026 the headroom is 13.9 pt and the observed gain was 13.4 (at lambda=1; 13.8 at
lambda*). The 2022 non-replication is therefore an arithmetic consequence of the election's
shape, not evidence GAM stopped organizing the vote. Added as a paragraph in main.tex's GAM
section and a clause in the Discussion. Consistent with the 2022 GAM run reaching 67.16% ~ its
own 66.7% ceiling.

### Note: does "GAM" mean "developed"? and why the +/-1 GAM field beats the continuous IDS field — 2026-09-04

**Script**: `scripts/gam_vs_ids_field_shape.py` (no MC; fields + empirical map on the N=488 2026 network).

GAM largely IS the developed part of the country: r(GAM, IDS z) = 0.625; mean IDS z +0.79 (GAM) vs
-0.49 (periphery); 87% of GAM distritos are above the national median IDS, 2% in the bottom quartile;
87% of top-quartile-IDS distritos are GAM. Raw correlations with the 2026 outcome are nearly equal
(IDS -0.554, GAM -0.589), yet as Ising fields GAM gave +13.4 and IDS +6.8. The difference is field
SHAPE, not information content:

1. Ceiling: sign(IDS z) puts 69.3% of distritos on the correct side (the vote flips at HIGH
   development, not at the mean); the capital-region line puts 80.9%. Best single IDS cut (z=+0.64,
   chosen on the outcome -> ceiling comparison, not a fair field) would reach 82.8%.
2. Push allocation: the top-|z| quartile carries 49% of the IDS field's magnitude -- the easy, already
   decided extremes; the contested middle gets almost none. +/-1 pushes every unit equally.
3. Fighting the coupling: on the real map the IDS field opposes a unit's neighbor majority on 32% of
   distritos, GAM on 15%; GAM agrees with the coupling everywhere inside the region and disagrees only
   at its edge (= the domain-wall error band).
Within GAM, development still discriminates: leading-side GAM distritos average IDS z +0.39 vs +0.98.

**Manuscript**: new paragraph in the GAM section; collinearity sentence in the confound paragraph;
"not development" wording in Abstract/Conclusion replaced by "largely coincides with high development
yet outperforms the development index itself as a field".

### Analysis: is the Alajuela held-out failure a GAM-proxy artifact? (yes) — 2026-09-04

**Script**: `scripts/run_gam_spatial_cv_proxyfix.py`; **data**: `data/processed/gam_spatial_cv_proxyfix_2026.npz`.
Same leave-one-province-out procedure as `run_gam_spatial_cv.py` (T=1.008, 16 seeds, sign resolved on
training folds), with the GAM field modified. Local, ~4.5 min per variant.

| variant | in-sample (median) | Alajuela held-out gap (p) | Cartago gap | San Jose gap | Heredia gap |
|---|---|---|---|---|---|
| baseline (proxy as published, 186 GAM) | 81.05% | -19.0 (<0.001) | 0.0 | +9.3 | +10.6 |
| A: Alajuela Central -> periphery (172) | **84.73%** | **-3.4 (0.29)** | 0.0 | +9.8 | +10.6 |
| B: all four flagged cantons -> periphery (152) | 82.79% | -3.4 (0.29) | **-13.5** | +8.1 | +10.6 |

Findings: (1) relabeling Alajuela Central alone removes the Alajuela failure and raises in-sample
alignment by +3.7 pt (consistent with the earlier post-hoc exclusion estimate of +3.1); the published
81.07% is conservative. (2) Relabeling all four is worse: Cartago collapses (Paraiso genuinely
belongs in GAM), so the proxy's error is concentrated in Alajuela Central, not spread over the four.
(3) Caveat: the relabel is chosen because Alajuela failed, so this is a diagnostic/sensitivity
result, not a new headline; the paper keeps the proxy as published and reports this in the SM CV
section and the Limitations item.

### Correction: the GAM paired-test p-value was below the permutation test's resolution — 2026-09-05

**Script**: `scripts/run_gam_paired_test_highres.py`; **data**: `data/processed/gam_paired_test_highres_2026.npz`.
Found during the submission-readiness review: `gam_paired_test.npz` (999 sign-flip draws) has 8 of 16 seed
pairs at exactly p=0.000, so the reported median 0.0005 was (0.000+0.001)/2, i.e. below resolution, and the
"x3 field-selection correction leaves p~0.048, still significant" claim rested on it. Re-run with 99,999
draws, same arms/T/seeds/blocks (geography-only T=2.605, GAM T=1.008, 16 seeds, canton blocks):

| convention | median p | sig (<0.05) | x32 Bonferroni | x32x3 | x32x8 |
|---|---|---|---|---|---|
| plain exceedance fraction | 0.00126 | 15/16 | 0.040 | 0.12 | 0.32 |
| (b+1)/(m+1) | 0.00127 | 15/16 | 0.041 | 0.12 | 0.33 |

Per-seed raw p range: <1e-4 to 0.058. Conclusion: headline survives the temperature-grid correction
(0.040) but NOT a stacked field-selection correction (0.12 for 3 fields; 0.33 for 8 tests counting the
five IDS axes). Manuscript now reports p=0.0013 / 0.040 and states the result does not survive the field
search correction.

Also recorded in this review pass (no new runs): the political-continuity field's sign-agreement ceiling
on the coalition split actually used to score its MC run is 80.6% (n=479 with a non-neutral field), not
the 79.1% computed on the winner-vs-runner-up binarization -- i.e. the same ceiling as GAM (80.9%), so the
ceiling does not explain that field's weak gain; the unstandardized magnitude (sigma=0.167 at lambda=1, no
lambda scan) is the more likely cause. Multistability cross-year names corrected from the CSVs:
Tabarcia (6/16, 4/16) and Palmichal (4/16, 8/16) are the >=4/16-in-both-years distritos; Monterrey is 3/16
and 4/16. The N=488 Binder curve is non-smooth between adjacent T (0.50->0.23->0.50 at T=1.61-1.83), so the
FSS verdict is downgraded from "negative" to "no crossing resolved".
