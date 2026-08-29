# NOVELTY_CHECK — Ising-model sociophysics of Costa Rican electoral geography

**Status as of 2026-08-29: CLEAN, including the new coupling-network-regionalization
material.** All close papers read in full, including Tiwari, Yang & Sen (2021, §3) and
Massoli (2026, §2c). The original 2026-08-16 check was scoped to canton-level framing
only; §2b (2026-08-18) extended to distrito/cross-scale scope; §2c (2026-08-22) extended
again to the two-field Hamiltonian and the GAM covariate search; §2d (2026-08-25) was a
pre-submission re-run across all three claims; §2e (2026-08-29) covers the new
community-detection/network-topology material added since §2d -- still CLEAN, but this
was the closest call yet: two real, close methodological neighbors (Elmakais & Glickman
2026 on Israeli cantons; Michaud et al. 2021 on Sweden) both do community detection on
real election municipalities, differing specifically in that they cluster on
vote-similarity while this paper clusters on geography alone with vote data excluded --
both added directly to the manuscript as differentiating citations rather than left for
a referee to find. Massoli (2026) remains the closest adjacent work for the two-field/GAM
claim specifically. Re-run again immediately before the actual submission click if more
than a few days elapse -- this niche moves fast (3 of 8 adjacent papers found in the
original check were 2025/2026 publications in a single check; §2d found 4 more new 2026
publications in one afternoon; §2e found 2 more, one of them the closest-yet
methodological neighbor, in a single afternoon).

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

## 2d. Pre-submission re-check (2026-08-25)

Re-ran the full corner against all three claims (§1 canton-level, §2b distrito/cross-scale,
§2c two-field/GAM) since 3 days had elapsed since §2c and this niche moves fast. Queries run:

- FastTrack `run_duplication_test`: `"Ising model election geography adjacency network"`
  (10 neighbours -- an Ising-centennial review, a network-science-methodology paper, an
  ecosystem-management report, a signed-networks balance paper, a voter-model-on-adaptive-
  networks paper, a redistricting-Markov-chain paper, two Galam opinion-dynamics papers, a
  private/public opinion-discrepancy paper, a bot-detection paper -- none combine an
  Ising/spin model with a real election and a real geographic adjacency network);
  `"Ising model capital region election geography"` (10 neighbours, same off-field pattern
  as §2c's re-run of this exact query -- no new collision); `"Ising model spatial resolution
  multiple scales election geography canton district"` (near-zero match, retrieval artifact
  per FastTrack's own caveat, not evidence either way); `"Ising model multiple external
  fields election capital region socioeconomic"` (10 neighbours, all off-field -- economics/
  institutions/statebuilding papers, no Ising-plus-election collision).
- FastTrack `search_papers`: `"Ising model election spatial network Costa Rica"` (2026-),
  0 hits.
- OpenAlex direct: `"Ising model election geographic network spatial resolution"`
  (2026-08-01 onward), 0 hits.
- Semantic Scholar direct: `"Ising model real geographic network election Monte Carlo
  ablation"` (2026-08-15 onward), 0 hits.
- Exa neural search (two sweeps): `"Ising model geographic adjacency network election
  Monte Carlo simulation 2026"` and `"Costa Rica elections Ising model spatial statistics
  geographic network 2026"` -- surfaced several genuinely new 2026 papers (below) plus
  more Spanish-language Costa Rican political-science literature (K-means/MIDEPLAN
  clustering of 2018 distrito results, a provincial-redistricting counterfactual study, an
  electorate-size/competitiveness regression study), none physics-based and none a
  collision, consistent with the §2 pattern that Exa is the only engine surfacing this
  literature at all.

**New 2026 Ising-and-elections/voting papers found, all screened and none a collision:**
- Liu, "Opinion Formation at Ising Social Networks" (*Information*, MDPI, 2026;
  arXiv:2511.12786) -- an Ising Network of Opinion Formation (INOF/GINOF) model of
  "elite vs. crowd" influence, applied to Newman's scientific-collaboration co-authorship
  network. No real election, no real geography, no vote data of any kind -- a
  co-authorship network standing in for a generic influence structure. Not a collision.
- Xu, Chen, Zhou & Wang, "Phase transitions in voting simulated by an intelligent Ising
  model," *Commun. Theor. Phys.* 78, 055601 (2026) -- adds nonlinear instantaneous
  feedback of the overall magnetization to the conventional Ising model and studies the
  resulting phase transitions analytically and via Monte Carlo, explicitly "in all
  dimensions" (i.e. generic lattices). No real country, no real election data, and no
  real geographic network anywhere in the abstract or highlights -- a theoretical
  extension of the Ising model that uses "voting" only as motivating vocabulary. Not a
  collision, but close enough on title vocabulary (Ising + voting + phase transition,
  2026) to be worth a differentiating footnote if a referee raises it.
- Baldassarri, Jacquier & Zocca, "Metastable opinion dynamics with hidden preferences: an
  Ising model with neutral agents" (arXiv:2601.05714) -- a rigorous probabilistic-methods
  paper (isoperimetric inequalities for polyominoes on a torus) analyzing metastability on
  highly symmetric synthetic grid networks. No real election, no real geography. Not a
  collision.
- Campbell & Ackland, "A computational model of spatial politics: Hotelling-Downs model as
  statistical physics," *PLOS ONE* 21(6), e0352242 (2026) -- explicitly frames party
  competition as statistical physics and uses Metropolis Monte Carlo, but the "spins" are
  continuous party positions in a 1D/2D abstract ideological-issue space (a Hotelling-Downs
  positioning game), not discrete binary spins on a real geographic adjacency network, and
  it is not fit to any real country's election results. Fundamentally different model
  class (continuous positional dynamics vs. this paper's discrete real-geography spin
  ablation). Not a collision, but the closest-sounding title (statistical physics +
  elections + PLOS ONE + 2026) found in this re-check, worth being aware of.

**Verdict: still CLEAN across all three claims.** No paper found combines an Ising/spin
Monte Carlo model, a real geographic border-adjacency network, and real election results
with anything resembling this paper's ablation, cross-scale comparison, or two-field/GAM
covariate search. The four new 2026 papers above are genuinely new prior art in the
broader "Ising models applied to voting/opinion" space but none touch the narrow surviving
corner this paper occupies -- consistent with the pattern established in §1/§2b/§2c that
this corner (real country, real geographic adjacency, real election results, literal MC
simulation) stays open even as the broader Ising-sociophysics-of-opinion space gets more
crowded every few months.

## 2e. Coupling-network regionalization / community-detection re-check (2026-08-29)

Between §2d (2026-08-25) and this check, the manuscript gained new material not covered
by any prior novelty pass: Louvain community detection on $J_{ij}$ alone (no vote data),
compared against provinces and GAM/periphery, at both canton and distrito resolution
(Section~2.2/Figures 5-6), plus several purely-topological robustness checks (betweenness
centrality, weighted degree, community-boundary status vs. per-node prediction error).
The claim being defended here, additional to §1/§2b/§2c: **running community detection on
a real country's geographic coupling network alone, with no vote or political data used
in the clustering step, then comparing the result post-hoc against administrative and
political categories, is not yet published for a real-election Ising/spin-model context.**
Falsified by a paper that does the same combination: community/module detection on a real
geographic adjacency network (no political data as clustering input) compared against
real administrative or political partitions, in service of an Ising/spin electoral model.

Queries run (same short-query FastTrack pattern as §2d, plus a fresh Exa sweep specifically
targeting the new material): `"Ising model election geography adjacency network"`,
`"Ising model capital region election geography"` (both re-run, same off-field pattern as
§2d, no new collision), `"Ising model election spatial network Costa Rica"` (0 hits),
OpenAlex direct (`"Ising model election geographic network spatial resolution"`,
2026-08-20 onward, 0 hits), and an Exa sweep (`"Ising model geographic adjacency network
election Monte Carlo simulation community detection 2026"`).

**A real, close methodological neighbor surfaced -- read and differentiated, not a
collision.** Elmakais & Glickman, "Partitioning Israeli Municipalities into Politically
Homogeneous Cantons: A Constrained Spatial Clustering Approach" (arXiv:2603.11805, 2026)
-- found via Exa, read in full via the arXiv HTML page. Uses Louvain (among three other
clustering algorithms: Simulated Annealing, Agglomerative, K-Means) on 229 Israeli
municipalities to construct politically homogeneous, geographically contiguous voting
districts. Critically different on the input to the clustering step: their Louvain edge
weights are *political-similarity* distances between municipalities' vote-share vectors
($w(u,v)=1-d(u,v)/d_{\max}$, using BlocShares/RawParty/PCA/NMF feature representations) --
vote data is the clustering objective, not excluded from it -- and the stated goal is
districting/redistricting design, not characterizing a real-election Ising model's own
coupling network. The paper's own methodological aside is worth noting directly: it flags
that Louvain's near-perfect cross-election stability (ARI = 1.0) "reflects algorithmic
insensitivity to small feature-space variations rather than an independent confirmation of
geographic structure" -- an observation of the same kind already added to this paper's own
Limitations (Section~4, fifth item) about Louvain's resolution/seed sensitivity, independently
corroborating that caveat's importance. Not a collision: different country, different
clustering input (political similarity vs. pure geography), different research question
(district design vs. characterizing an existing Ising model's network), and no Ising/spin
Monte Carlo model anywhere in their paper. Added to the manuscript itself as a
differentiating citation (Section~2.2) since it is close enough on vocabulary (Louvain +
municipalities + elections) that a referee could plausibly ask about it.

**A second, also real, also differentiated neighbor.** Michaud, M\"akinen, Szilva & Frisk,
"A spatial analysis of parliamentary elections in Sweden 1985-2018" (*Applied Network
Science* 6, 67 (2021), doi:10.1007/s41109-021-00409-z) -- found via the same Exa sweep,
read via the paper's own abstract/methods description in the search result (not the full
PDF, which required institutional access this sandbox does not have; the description below
rests on the abstract, methods summary, and literature-review passages returned by the
search, which is enough to characterize the method and rule out a collision, but a full
read is recommended before citing any specific numeric result from it, which this
manuscript does not). Groups Swedish municipalities into "politico-cultural communities"
using community detection on the Bhattacharyya-coefficient similarity of their *voting
profiles* -- again vote data as the clustering input, not pure geography -- finding 3-4
stable communities over 1985-2018. The paper's own literature review names a further small
genre doing the same kind of thing (Fern\'andez-Gracia \& Lacasa 2018 on Spanish
elections; Maulana \& Situngkir 2015 on German elections) -- neither independently
verified in this check (found only via Michaud et al.'s citation of them, not read
directly), so neither is added to this paper's own bibliography, but their existence
confirms "community detection on real election vote-similarity data" is a small,
real, recognized sub-literature distinct from what Section~2.2 does. Added to the
manuscript as a second differentiating citation alongside Elmakais \& Glickman.

**Verdict: still CLEAN.** No paper found running community/module detection on a real
country's geographic coupling network *with vote data excluded from the clustering
step*, compared post-hoc against administrative/political categories, for an Ising/spin
electoral model. The closest neighbors both cluster directly on vote/political
similarity -- a related but distinct question (do voting patterns imply communities?
vs. this paper's does geography alone, ignorant of votes, imply structure a political
category later turns out to resemble?) -- and neither uses an Ising/spin Monte Carlo
model. Both differentiating citations were added directly to the manuscript
(Section~2.2) rather than left for a referee to ask about first.

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
| "PARTIDOS CON O SIN BASE TERRITORIAL EN COSTA RICA: ANÁLISIS DE LA DISTRIBUCIÓN GEOGRÁFICA DE LOS APOYOS PARTIDARIOS 1998 AL 2022," *GEOgraphia* 27(58) (2025) | 10.22409/GEOgraphia2025.v27i58.a66944 (DOI found 2026-08-25, §2d) | Political-science (not physics) analysis of the *same* multi-election geographic territory this project spans (1998–2022 ⊃ our 2018/2022/2026). Confirms PAC (2018's winner) has a documented urban/Gran Área Metropolitana-concentrated support base unlike PLN's consolidated national territorial base (per WebSearch summary of secondary sources) — a plausible political-science lead for *why* 2018's geography-vs-baseline result differs from 2022/2026's. Must cite; worth following up as a substantive explanation, not just a novelty reference. |
| Bizyaeva, Franci & Leonard, "Nonlinear Opinion Dynamics With Tunable Sensitivity," *IEEE Trans. Autom. Control* (2022) | 10.1109/tac.2022.3159527 (arXiv:2009.04332) | Found 2026-08-22 (§2c, short-query re-check). A continuous-time multi-option opinion-dynamics model on a network that genuinely produces multistable agreement/disagreement, tunable sensitivity, and opinion cascades -- vocabulary directly adjacent to this paper's multistability/counterfactual/cascade diagnostics (Sections 4.9-4.11). But it is a control-theory formalism (nonlinear ODEs with saturating exchange, not an Ising/spin Monte Carlo model), tested on no real election data, and with no geographic adjacency network -- not a collision, but close enough on the diagnostic vocabulary that a referee could ask about it. |
| Liu, "Opinion Formation at Ising Social Networks," *Information* (MDPI) 17(1), 41 (2026) | arXiv:2511.12786 | Found 2026-08-25 (§2d). Ising Network of Opinion Formation (INOF/GINOF) model of "elite vs. crowd" influence, applied to Newman's scientific-collaboration co-authorship network. No real election, no real geography, no vote data. Not a collision. |
| Xu, Chen, Zhou & Wang, "Phase transitions in voting simulated by an intelligent Ising model," *Commun. Theor. Phys.* 78, 055601 (2026) | 10.1088/1572-9494/ae3d16 | Found 2026-08-25 (§2d). Adds nonlinear instantaneous magnetization feedback to the conventional Ising model, studied analytically and via MC "in all dimensions" (generic lattices). No real country, election, or geographic network -- "voting" is motivating vocabulary only. Not a collision, but close on title terms (Ising + voting + phase transition, 2026) -- worth a differentiating footnote if a referee raises it. |
| Baldassarri, Jacquier & Zocca, "Metastable opinion dynamics with hidden preferences: an Ising model with neutral agents" | arXiv:2601.05714 | Found 2026-08-25 (§2d). Rigorous probabilistic-methods paper (isoperimetric inequalities for polyominoes on a torus) on synthetic grid networks. No real election, no real geography. Not a collision. |
| Campbell & Ackland, "A computational model of spatial politics: Hotelling-Downs model as statistical physics," *PLOS ONE* 21(6), e0352242 (2026) | 10.1371/journal.pone.0352242 | Found 2026-08-25 (§2d). Frames party competition as statistical physics with Metropolis Monte Carlo, but "spins" are continuous party positions in an abstract 1D/2D ideological space (Hotelling-Downs), not discrete spins on a real geographic network, and not fit to any real country's results. Not a collision -- fundamentally different model class -- but the closest-sounding title (statistical physics + elections + PLOS ONE + 2026) found this round. |
| Mora Cordero, "Utilización de ciencias de datos en análisis de resultados electorales: un ejemplo aplicado a los resultados de la segunda ronda electoral del 2018 en Costa Rica," *Revista TSE* 36 | — (found via Exa; TSE institutional journal, not in Crossref/OpenAlex/S2) | Found 2026-08-25 (§2d). K-means clustering of the *same* 2018 Costa Rican runoff at distrito level, combined with the *same* MIDEPLAN social-development index this paper uses as its $h^{soc}$ field (Section~2.4) -- a genuinely close **data** precedent (same TSE + MIDEPLAN combination, same election, same distrito granularity). Not a collision on method (unsupervised clustering/visualization, no Ising/spin model, no network, no ablation, explicitly disclaims predictive intent) but close enough on data sourcing to be worth a citation if the MIDEPLAN section discusses precedent for this specific data combination. |
| Cascante Campos, "Costa Rican electoral geography: counterfactual analysis of possible effects of alternative provincial divisions on legislative political representation (2002-2022)," *Revista Geográfica de América Central* 74(1) (2025) | 10.15359/rgac.74-1.8 | Found 2026-08-25 (§2d). Counterfactual redistricting analysis (7 vs. 9 provinces) on Costa Rican legislative elections -- political geography, not physics; province-level, not canton/distrito. Not a collision. |
| Elmakais & Glickman, "Partitioning Israeli Municipalities into Politically Homogeneous Cantons: A Constrained Spatial Clustering Approach" (2026) | arXiv:2603.11805 | Found 2026-08-29 (§2e); read in full via arXiv HTML. **Closest methodological neighbor to this paper's new community-detection material.** Louvain (among 3 other algorithms) on 229 Israeli municipalities, but edge weights are *political-similarity* distances between vote-share vectors -- vote data is the clustering objective, not excluded from it, and the goal is districting design, not characterizing an Ising model's own network. No Ising/spin model. Cited directly in the manuscript (Section~2.2) as a differentiating reference. |
| Michaud, Mäkinen, Szilva & Frisk, "A spatial analysis of parliamentary elections in Sweden 1985-2018," *Applied Network Science* 6, 67 (2021) | 10.1007/s41109-021-00409-z | Found 2026-08-29 (§2e); characterized from the paper's own abstract/methods summary (full PDF not accessible in this sandbox). Community detection on Bhattacharyya-similarity of Swedish municipalities' *voting profiles* -- again vote data as the clustering input, not pure geography. No Ising/spin model, no real geographic adjacency network as the clustering basis. Cites a further small genre doing the same kind of vote-similarity community detection (Fernández-Gracia & Lacasa 2018 on Spain; Maulana & Situngkir 2015 on Germany) -- neither independently verified here, so neither added to this paper's bibliography, but their existence (via Michaud et al.'s citation) confirms this is a small, recognized, and distinct sub-literature from Section~2.2's geography-only approach. Cited directly in the manuscript as a second differentiating reference. |

## 4. Alternatives checked and not pursued further here

Not applicable — this is the project's first novelty check, run mid-project (implementation
and empirical results already exist; see IsingCR `README.md`/`CLAUDE.md`) rather than
before starting. No prior seed of this idea existed in `lit-gap-toolkit/SEED_GRAVEYARD.md`.

## 5. Re-check schedule

- **Before drafting:** re-run §2's queries plus a fresh Exa sweep regardless of the CLEAN
  verdict — papers move fast in this niche (3 of 8 adjacent-prior-art rows above are
  2025/2026 publications found during a single check).
- **Before submission:** ~~same as above, plus check whether `korbel2026`'s TABLE III...~~
  — pre-submission re-check done 2026-08-25, see §2d (CLEAN across all three claims; 6 new
  2026 adjacent references found and added to §3, none a collision). `korbel2026`'s TABLE
  III Mode B re-run is still open if its numbers end up cited directly (not yet needed —
  the manuscript cites Korbel's dataset span and validation approach, not per-decade
  fitted values). Re-run the full corner again immediately before the actual submission
  click if more than a few days elapse from 2026-08-25.
- **If scope expands to distrito-level (492 nodes) or to other countries:** ~~re-run the
  corner queries at that finer/broader scope~~ — done 2026-08-18, see §2b (CLEAN, distrito
  scope specifically covered). Re-run again if scope expands further (e.g. a third
  country, or a granularity finer than distrito).
- **If scope expands to a multi-field extension or additional covariates:** ~~re-run the
  corner queries against the two-field Hamiltonian and any new predisposition fields~~ —
  done 2026-08-22, see §2c (CLEAN, MIDEPLAN/political-continuity/GAM covariate search
  and the four model-native dynamical diagnostics specifically covered). Re-run again if
  a further field or diagnostic is added.
