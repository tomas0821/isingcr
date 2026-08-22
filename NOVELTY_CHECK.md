# NOVELTY_CHECK — Ising-model sociophysics of Costa Rican electoral geography

**Status as of 2026-08-22: CLEAN, now including the two-field/GAM extension.** All
close papers read in full, including Tiwari, Yang & Sen (2021, §3) and Massoli (2026,
§2c). The original 2026-08-16 check was scoped to canton-level framing only; §2b
(2026-08-18) extended to distrito/cross-scale scope; §2c (2026-08-22) extends again to
the manuscript's second contribution (the two-field Hamiltonian and the GAM covariate
search) added this session — CLEAN, Massoli (2026) remains the closest adjacent work
and differs on network construction, field structure, dynamics, and domain (§2c).
Re-run again before submission regardless — this niche moves fast (3 of 8 adjacent
papers found in the original check were 2025/2026 publications in a single check).

All 16 references in §3 are filed in Zotero under Sociophysics ▸ IsingCR (added
2026-08-16 via the Zotero Web API, tagged `IsingCR-novelty-check`), all 16 PDFs attached
(user sourced them manually) and converted to Markdown 2026-08-16 via `marker` Mode A —
see `papers_md/CONVERSION_NOTES.md` for per-paper fidelity notes and known table-body
losses (4 papers lost at least one full table; captions survived in all cases, so the
losses are visible/documented, not silent).

## 1. The claim being defended

> Fitting an Ising-model Monte Carlo simulation — spins = binarized canton-level election
> outcomes, couplings J_ij = the REAL geographic border-adjacency network between cantons
> (not an inferred/mean-field/synthetic network), external field h_i = each canton's own
> vote margin — to real official Costa Rican electoral results (TSE data, canton level,
> 2018/2022/2026), with (a) an explicit h=0-vs-h=margin ablation decomposing geographic
> contagion from individual predisposition, and (b) a same-model historical comparison
> across multiple election cycles within one country, is a combination not yet published.

Falsified by a single paper that runs an Ising/spin-model Monte Carlo simulation on a real
subnational geographic border-adjacency network fit to real election results, for any
country, with anything resembling the ablation or multi-election comparison above.

**Not falsified** by the broader claim "an Ising/random-field model has been applied to
elections" — that broader framing is well-established and actively crowded (§2); the
claim above is deliberately the narrow surviving corner identified by `/seed-idea`
(`lit-gap-toolkit/physica-a/candidates/cr-electoral-ising-canton-network/SEED.md`), not
the general idea.

## 2. Queries run

```bash
cd /home/tomas/mnt/gdrive/Research/Current/lit-gap-toolkit
python3 check_novelty.py --rows 10 --query "Ising model elections"
python3 check_novelty.py --rows 5  --query "ferromagnets electoral instability"
python3 check_novelty.py --rows 8  --query "sociophysics Costa Rica elections"
python3 check_novelty.py --rows 8  --query "spatial Ising model election geographic network canton municipality"
python3 check_novelty.py --rows 8  --query "Ising model real adjacency network district level election results empirical"
```

Plus: FastTrack `run_duplication_test` (over-specified query → 0 hits, retrieval
artifact; simplified to `"Ising model elections spatial network"` → 10 neighbours, see
§3); Exa neural search (`"Ising model geographic adjacency network canton-level election
results Costa Rica"`, cost $0.007) — surfaced Spanish-language Costa Rican political-
science literature invisible to the English-biased keyword APIs (§3); one-hop OpenAlex
citation snowball on the single closest historical-comparison paper (Braha & de Aguiar
2017, 82 citing works enumerated, sorted by date, screened by title); full-text read
(via arXiv PDF, `arxiv.org/pdf/2510.00612`, all 6 pages) of the single closest
methodological paper (Korbel, Dahdoul & Thurner, PRL 2025/26).

- ⚠️ arXiv is unreachable from this sandbox's direct network (DNS resolution fails on
  `export.arxiv.org` via `curl`) — but reachable via the `WebFetch` tool, which pulls
  through a different path and successfully retrieved the full PDF. If a future check
  environment lacks WebFetch, arXiv coverage silently drops to zero — note this in the
  write-up rather than reporting a false "arXiv: clean."
- ⚠️ Crossref's `query.bibliographic`/`query.title` are relevance-ranked bag-of-words,
  not boolean AND — a combined "Ising model election" query returned a *higher* count
  than either term alone (union-like behavior across the words "Ising", "model",
  "election" separately). Never trust a combined-term count as an intersection; read
  actual titles instead (used for the Physica A journal-fit check, see SEED.md).
- ⚠️ Over-specified FastTrack queries (a full descriptive sentence) return zero
  `nearest_neighbours` with a `retrieval_caveat` flagging it as an artifact, not a clean
  verdict — simplify to 3–6 core-concept words before reading a FastTrack result as
  evidence either way.
- ⚠️ Keyword APIs (Crossref/OpenAlex/S2) are English-title-biased and missed all of the
  directly-on-topic Spanish-language Costa Rican canton-level electoral-geography
  literature (§3) — the Exa semantic sweep is not optional for a non-English-language
  case study; run it before trusting a keyword-only "clean."

## 2b. Distrito/cross-scale re-check (2026-08-18)

The claim being defended here, additional to §1's canton-level claim: **fitting the same
Ising-model MC ablation to the same country's real geographic network at two different
real administrative granularities (canton and distrito), showing the geography-vs-
predisposition conclusion reverses depending on spatial resolution, is not yet
published.** Falsified by a single paper that runs an Ising/spin-model MC simulation on a
real subnational geographic adjacency network fit to real election results, compared
across two or more real spatial resolutions within the same country/dataset.

Queries run (OpenAlex, Semantic Scholar, FastTrack `run_duplication_test`, Exa neural
search — five distinct angles, all English since a distrito-scope Costa Rican-specific
hit is unlikely to exist yet if a canton-scope one didn't in §2):
- OpenAlex: `"Ising model election spatial resolution scale district municipality
  comparison"`, `"Ising model canton district election Costa Rica geography adjacency
  spin"`, `"spatial resolution finite-size scaling political geography agent based model
  election"`, `"spin model election granularity fine coarse spatial unit voting outcome
  prediction"` — all 0 hits.
- Semantic Scholar: `"modifiable areal unit problem spin model election geographic
  aggregation"` — 10 hits, all MAUP-in-disease-mapping/urban-planning/traffic, none
  touching Ising/spin models or elections.
- FastTrack `run_duplication_test` (question: Ising/spin model with real geographic
  adjacency fit to real election results, compared across two spatial resolutions within
  one country to test whether geography-vs-predisposition decomposition is
  resolution-sensitive) — 10 nearest neighbours, none combining an Ising/spin model with
  a multi-resolution real-election comparison. One genuinely adjacent hit not previously
  in §3: Godoy-Lorite & Jones, "Inference and Influence of Large-Scale Social Networks
  Using Snapshot Population Behaviour without Network Data" (arXiv:2003.07146, 2020) —
  a spin-based behavioral model explicitly using "social temperature" language, fit to
  the EU Referendum and two London Mayoral elections. Close on vocabulary and the
  spin/election/real-country combination, but the network is *inferred* from behavioral
  snapshots (not a real geographic adjacency network) and the multi-election comparison
  is across different election *types* in one city/country, not the same election
  compared across two spatial *resolutions*. Added to §3 below as a reference, not a
  collision.
- Exa neural search: `"Ising model election spatial resolution multiple scales
  geographic aggregation municipality precinct district comparison"` — surfaced strong,
  directly relevant political-geography/ecological-inference literature establishing
  that spatial-scale-sensitivity in electoral conclusions is a known, well-studied
  phenomenon outside physics (Russo & Beauguitte 2014 "Aggregation level matters:
  evidence from French electoral data"; Johnston et al., "Spatial scale and the
  geographical polarization of the American electorate"; a 2026 grid-cell electoral
  study; a UK multilevel spatial voting model) — none use an Ising/spin/statistical-
  mechanics framework. These are useful positioning references (the paper's
  resolution-dependence finding is consistent with, not contradicted by, the political-
  geography MAUP literature) but not collisions. One Ising-adjacent hit, Okamoto,
  "Maximizing gerrymandering through Ising model optimization" (*Sci. Rep.* 2021,
  10.1038/s41598-021-03050-z), uses Ising-model combinatorial optimization to construct
  gerrymandered districts on a synthetic 70-cell grid — a districting-*design* question
  on synthetic data, not a real-network fit to real results at multiple resolutions.

**Verdict: the distrito/cross-scale claim is CLEAN**, on the same footing as the
canton-level claim in §1. No paper found combines an Ising/spin Monte Carlo model, a
real geographic adjacency network, real election data, and an explicit comparison of the
same analysis across two or more real spatial resolutions. The Introduction's "cross-scale
replication" novelty claim is supported.

## 2c. Two-field extension / GAM covariate search re-check (2026-08-22)

The claim being defended here, additional to §1/§2b: **a two-field Ising extension on
a real geographic adjacency network, testing multiple independently-sourced candidate
predisposition fields (a socioeconomic development index, a non-circular
prior-election political field, and capital-metropolitan-area membership) against each
other, then characterizing the winning field's dynamical properties (multistability
across MC seeds, temperature-sensitivity under a counterfactual sweep, single-node
perturbation cascades) is not yet published.** Falsified by a paper that does the same
combination: a real-network Ising/spin model with two or more independently-sourced
external fields compared against each other for a real election, plus any of the
model-native dynamical diagnostics listed above.

Queries run:
- FastTrack `run_duplication_test` (question: two-field Ising model on a real
  geographic adjacency network, testing an independent socioeconomic covariate and a
  capital-region/metropolitan-area membership indicator against each other as
  predisposition-field candidates for real election outcomes, then characterizing the
  stronger field's multistability, temperature-sensitivity, and single-node cascade
  behavior) — 10 nearest neighbours returned, all off-field (air-pollution CAR models,
  neuroimaging, COVID spatio-temporal review, colorectal cancer survival). This is an
  over-specified, multi-clause query, exactly the pattern §2's own methodology caveat
  flags as producing unreliable `nearest_neighbours` (round-3 referee panel, 2026-08-22,
  correctly caught this as a retrieval-quality risk in the original write-up, not
  confirmatory evidence) — retained below for completeness but not relied upon; the
  two shorter, 3-6-word re-runs below are the load-bearing checks.
- FastTrack `search_papers`: `"Ising model multiple external fields election geography
  capital metropolitan region predisposition"` (2023–) — 3 total hits, none physics or
  Ising-related. Same over-specification caveat as above.
- FastTrack `run_duplication_test`, re-run 2026-08-22 with a short (5-word) query per
  §2's own methodology: `"Ising model capital region election geography"` — 10 nearest
  neighbours, all off-field (a general Ising-model-history review, an economics/social-
  interactions survey, an econophysics/sociophysics milestones review, and several
  unrelated human-geography/political-economy papers) — no Ising-plus-real-election
  collision.
- FastTrack `search_papers`, short (5-word) query targeting the model-native
  diagnostics specifically: `"Ising model multistability perturbation cascade
  election"` (2020–) — 2 hits, both the same non-Ising control-theory paper (Bizyaeva,
  Franci & Leonard, "Nonlinear Opinion Dynamics With Tunable Sensitivity," *IEEE Trans.
  Autom. Control* 2022, arXiv:2009.04332): a continuous-time multi-option opinion-
  dynamics model that does produce multistability, tunable sensitivity, and opinion
  cascades on a network — genuinely adjacent vocabulary — but it is a control-theory
  formalism (not Ising/statistical-mechanics), tested on no real election data, and
  with no geographic adjacency network. Added to §3 below as a reference, not a
  collision.
- Exa neural search: `"Ising model two independent fields election metropolitan region
  socioeconomic covariate spatial network"` — surfaced `massoli2026` again (confirming
  it remains the closest hit under a fresh query angle), the already-known
  `korbel2026`/`siegenfeld2020`/`mullick2025`, and one new not-yet-reviewed title, "An
  Ising Similarity Regression Model for Modeling Multivariate Binary Data" (*Statistica
  Sinica*) — a statistics-methods paper on Ising-model-structured regression for
  correlated binary outcomes generally, with no election application and no geographic
  network in the abstract; screened by title/venue only (a general statistical-methods
  journal, not a match for this paper's political-geography domain) and not read in
  full, since nothing in the available summary suggests a collision on this paper's
  specific real-network/two-field/election combination. No other new hits.

Given the sparse-embedding-match pattern above, we also re-read `massoli2026`
(`papers_md/massoli2026/massoli2026.md`, already cited in the Introduction as adjacent
"territorial socio-economic dynamics" work per §3) in full, specifically checking it
against the two-field/GAM extension rather than only the original single-field claim it
was already positioned against. Confirmed substantially different on every axis that
would matter for a collision:
- **Network**: Massoli's $J$ connects municipalities sharing *similar territorial
  attributes* (altitude, population, urbanization, coastal status) — explicitly a
  conceptual similarity graph, "independently of strict geographical proximity"
  (Massoli §4.1) — not a real border-adjacency network. Our entire paper's premise
  (Section~2.2) is the opposite: literal geographic adjacency, no conceptual-similarity
  substitute anywhere.
- **Field**: Massoli aggregates six composite indices into a *single* field via PCA
  (Eq. 13); no analog of comparing multiple independently-sourced fields against each
  other, no two-field Hamiltonian, no finding that one field-type (geography-linked)
  beats another (development-linked) the way GAM beats MIDEPLAN/political-continuity
  here.
- **Dynamics**: Simulated Annealing initialized *at* the observed configuration, fixed
  hyperbolic cooling $T(t)=T_0/t$, searching for nearby energetically favorable
  configurations — not a temperature *scan* searching for the best-fit "social
  temperature," which is this paper's central device throughout. No analog of a
  multistability check (independent random-start seeds), a counterfactual
  temperature-sensitivity sweep, or a single-node cascade test anywhere in Massoli.
- **Uncertainty**: Massoli's uncertainty tool is Conformal Prediction on per-unit
  marginal probabilities across $K$ independent sample batches — a genuinely different
  (and itself novel) approach, not multistability/cascade-style dynamical
  perturbation.
- **Domain**: Italian central-hub-vs-peripheral-area municipal classification from an
  administrative statistical register, no election data, no political geography, no
  party-continuity concept — a different substantive question from Costa Rican
  electoral geography entirely.

**Verdict: the two-field/GAM extension is CLEAN.** No paper found combines a real
geographic-adjacency Ising model, a genuine multi-field comparison among independently
sourced predisposition candidates, and dynamical-system diagnostics (multistability,
counterfactual temperature sensitivity, cascade testing) for a real election. Massoli
(2026), the closest adjacent work in the existing bibliography, differs on every one of
these axes and remains correctly positioned as adjacent-not-colliding. This verdict now
rests on the same standard as §1/§2b: two short (3-6 word) FastTrack queries in addition
to the original over-specified one, plus an Exa neural sweep, none of which surfaced a
domain-relevant collision (2026-08-22, addressing a round-3 referee-panel finding that
the original §2c write-up leaned on a single over-specified query and treated its
off-topic results as more probative than the sparse-match pattern actually supports).

## 3. Adjacent prior art — references, not collisions

| Work | DOI / ID | Relationship |
|---|---|---|
| Korbel, Dahdoul & Thurner, "Empirical validation of the polarization transition in a double-random field model of elections," *Phys. Rev. Lett.* (2025/26) | arXiv:2510.00612 | **Closest methodological collision — read in full.** Random-field Ising-equivalent model of US House elections 1980–2020; field = campaign spending (bimodal, randomly assigned per voter), not vote margin. Critically, the "homophilic" network is solved via **configuration-model + mean-field approximation** (closed-form self-consistency equations 3–6), not a real geographic border-adjacency graph and not an actual Monte Carlo simulation on any explicit network — no district-adjacency structure, no spatial topology, no MC seeds/replicates at all (fully analytical). Country, field source, network representation, and core method (analytical mean-field vs. our real-network MC) all differ. Confirms the surviving corner is not this paper. |
| Tiwari, Yang & Sen, "Modeling the nonlinear effects of opinion kinematics in elections: A simple Ising model with random field based study," *Physica A* 582, 126287 (2021) | 10.1016/j.physa.2021.126287 | **Read in full 2026-08-16 (`papers_md/tiwari2021/tiwari2021.md`) — confirms the secondhand inference.** Purely synthetic/theoretical: agents on a regular **128×128 / 256×256 square lattice** (not a real geographic network of any kind), random field is an unconstrained model input (not derived from any real vote data), results are ensemble averages over 100 synthetic realizations. No real country, no real election, no real geography anywhere in the paper. Confirms the surviving corner is not this paper — S0 gate closed. |
| Braha & de Aguiar, "Voting contagion: Modeling and analysis of a century of U.S. presidential elections," *PLoS ONE* (2017) | 10.1371/journal.pone.0177970 | Closest on the "disentangle geography/contagion from other factors across election history" angle — analytically derives county vote-share distributions and finds an abrupt phase transition in contagion strength over ~100 years of US elections. Abstract explicitly states it works with an **"unknown network structure"** (distributional/analytical, not a literal MC simulation on a real adjacency graph). Country and network-explicitness differ. |
| Siegenfeld & Bar-Yam, "Negative representation and instability in democratic elections," *Nature Physics* (2020) | 10.1038/s41567-019-0739-6 | Complex-systems/critical-phenomena analogy for electoral-system (PR vs. majoritarian) response to opinion shifts — a voting-*rule-design* question, not a real-geography Ising MC fit to one country's results. Different angle. |
| Mullick & Sen, "Sociophysics models inspired by the Ising model" (review), *Eur. Phys. J. B* (2025) | 10.1140/epjb/s10051-025-01053-7 | Comprehensive 2025 review of Ising-inspired sociophysics (opinion dynamics, finance, segregation, epidemics, language, political polarization). Does not flag real-geographic-adjacency election networks as an established sub-area — weak supporting signal the corner is open. Essential related-work citation regardless. |
| "Dirichlet-Swing: understanding spatio-temporal aspects of political elections in heterogeneous societies through agent-based simulation," *PLoS ONE* (2026) | 10.1371/journal.pone.0344018 | Found via one-hop citation snowball on Braha & de Aguiar (2017). India, district-based seat elections; agent-based Dirichlet-Process model of geographic proximity + multi-election vote swing. Conceptually adjacent (geography + multi-election comparison) but a completely different formalism (Bayesian nonparametrics, not Ising/spin MC) — no phase transition, no h/J structure. |
| "Susceptibilities of Democratic Electoral Systems," *IEEE Trans. Comput. Soc. Syst.* (2024) | OpenAlex W4403391230 | Terminology overlap only ("susceptibility") — compares electoral *system design* (proportional vs. plurality) robustness to influence campaigns via simulation, not a real-country geographic Ising fit. Not a collision. |
| Godoy-Lorite & Jones, "Inference and Influence of Large-Scale Social Networks Using Snapshot Population Behaviour without Network Data" (2020) | arXiv:2003.07146 | Found 2026-08-18 (§2b); filed in Zotero 2026-08-19 (item `CJICD2I5`, tagged `IsingCR-novelty-check`, not cited in the manuscript); converted to Markdown 2026-08-19 (`papers_md/godoylorite2020/`, see `CONVERSION_NOTES.md`). Spin-based behavioral model explicitly using "social temperature" language, fit to the EU Referendum and two London Mayoral elections. Network is *inferred* from behavioral snapshots, not a real geographic adjacency network; compares election *types*, not spatial *resolutions* of the same election. Close on vocabulary, not on method or question. Not a collision, but close enough on terminology that a Physica A referee could ask about it — worth a short differentiating mention if reviewer feedback raises it. |
| Okamoto, "Maximizing gerrymandering through Ising model optimization," *Sci. Rep.* (2021) | 10.1038/s41598-021-03050-z | Found 2026-08-18 (§2b); filed in Zotero 2026-08-19 (item `ICQ37ZIC`, tagged `IsingCR-novelty-check`, not cited in the manuscript); converted to Markdown 2026-08-19 (`papers_md/okamoto2021/`, see `CONVERSION_NOTES.md`). Ising-model combinatorial optimization to construct maximally gerrymandered districts on a synthetic 70-cell grid — a districting-*design* question on synthetic data, not a real-network fit to real results. Not a collision. |
| Elías Chavarría-Mora, "Una mirada cantonal mediante estadística espacial al efecto del desarrollo humano sobre el apoyo electoral en la segunda ronda de la elección presidencial de 2018" (2022) | — (found via Exa; not in Crossref/OpenAlex/S2) | **Direct system-level precedent, different method.** Canton-level spatial statistics (not Ising/physics) on the *same* 2018 Costa Rican runoff this project models. Must be cited; may help explain this project's own open finding that 2018 behaves differently from 2022/2026 (see IsingCR `README.md`/`CLAUDE.md` "Current state"). |
| "PARTIDOS CON O SIN BASE TERRITORIAL EN COSTA RICA: ANÁLISIS DE LA DISTRIBUCIÓN GEOGRÁFICA DE LOS APOYOS PARTIDARIOS 1998 AL 2022" | — (found via Exa) | Political-science (not physics) analysis of the *same* multi-election geographic territory this project spans (1998–2022 ⊃ our 2018/2022/2026). Confirms PAC (2018's winner) has a documented urban/Gran Área Metropolitana-concentrated support base unlike PLN's consolidated national territorial base (per WebSearch summary of secondary sources) — a plausible political-science lead for *why* 2018's geography-vs-baseline result differs from 2022/2026's. Must cite; worth following up as a substantive explanation, not just a novelty reference. |
| Bizyaeva, Franci & Leonard, "Nonlinear Opinion Dynamics With Tunable Sensitivity," *IEEE Trans. Autom. Control* (2022) | 10.1109/tac.2022.3159527 (arXiv:2009.04332) | Found 2026-08-22 (§2c, short-query re-check). A continuous-time multi-option opinion-dynamics model on a network that genuinely produces multistable agreement/disagreement, tunable sensitivity, and opinion cascades -- vocabulary directly adjacent to this paper's multistability/counterfactual/cascade diagnostics (Sections 4.9-4.11). But it is a control-theory formalism (nonlinear ODEs with saturating exchange, not an Ising/spin Monte Carlo model), tested on no real election data, and with no geographic adjacency network -- not a collision, but close enough on the diagnostic vocabulary that a referee could ask about it. |

## 4. Alternatives checked and not pursued further here

Not applicable — this is the project's first novelty check, run mid-project (implementation
and empirical results already exist; see IsingCR `README.md`/`CLAUDE.md`) rather than
before starting. No prior seed of this idea existed in `lit-gap-toolkit/SEED_GRAVEYARD.md`.

## 5. Re-check schedule

- **Before drafting:** re-run §2's queries plus a fresh Exa sweep regardless of the CLEAN
  verdict — papers move fast in this niche (3 of 8 adjacent-prior-art rows above are
  2025/2026 publications found during a single check).
- **Before submission:** same as above, plus check whether `korbel2026`'s TABLE III
  (per-decade fitted T*/hc/accuracy, lost in the Mode A conversion — see
  `papers_md/CONVERSION_NOTES.md`) needs a Mode B re-run if its numbers end up cited
  directly.
- **If scope expands to distrito-level (492 nodes) or to other countries:** ~~re-run the
  corner queries at that finer/broader scope~~ — done 2026-08-18, see §2b (CLEAN, distrito
  scope specifically covered). Re-run again if scope expands further (e.g. a third
  country, or a granularity finer than distrito).
- **If scope expands to a multi-field extension or additional covariates:** ~~re-run the
  corner queries against the two-field Hamiltonian and any new predisposition fields~~ —
  done 2026-08-22, see §2c (CLEAN, MIDEPLAN/political-continuity/GAM covariate search
  and the four model-native dynamical diagnostics specifically covered). Re-run again if
  a further field or diagnostic is added.
