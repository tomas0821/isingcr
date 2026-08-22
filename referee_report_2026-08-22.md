---
type: referee-report
draft: manuscript/main.tex
date: 2026-08-22
verdict: major revisions
---

# Referee report — IsingCR (Physica A submission draft), Round 3 (second contribution: two-field extension and GAM covariate search)

## Summary assessment

This round is scoped narrowly to the material added since round 2
(`referee_report_2026-08-18.md`): the two-field Hamiltonian extension (Eq. 2), the
MIDEPLAN/non-circular-political-field/GAM covariate search, and the four model-native
dynamical diagnostics (domain-wall structure, multistability, counterfactual temperature
sensitivity, single-node cascade). Round 1 and round 2's findings, all concerning the
first contribution, are not re-litigated here and are presumed still in whatever state
round 2 left them.

The second contribution's headline result — capital-region (GAM) membership beating both
a socioeconomic development index and a non-circular political-continuity field as a
distrito-level predisposition proxy, at $p=0.0005$ with 15 of 16 seed-pairs individually
significant — is the single most statistically decisive number in the entire manuscript,
first or second contribution. That result itself was not contradicted by any lens this
round. What was found instead is a cluster of problems characteristic of a large block of
new material added under time pressure and not yet given the same scrutiny pass the first
contribution received across two prior rounds: a load-bearing statistical claim (the
λ_pol circularity check) that cannot be traced to any 2026 computation on disk and is
contradicted by the one comparable computation that does exist; a stale novelty claim
that flatly contradicts the project's own novelty-tracking document, so pervasively that
five independent reviewing lenses caught it independently without coordinating; a genuine
internal contradiction about how the paper's own central new equation (Eq. 2) is actually
used in the section that is supposed to instantiate it; a proxy-imprecision caveat that
the paper applies to one new subsection but not to two others resting on the identical
at-risk data; several overclaims in the highest-visibility text (Abstract, Discussion)
that outrun what the cited numbers show; and a scope/curation problem — title, keywords,
and abstract were not updated to reflect that roughly half the paper is now a second,
largely self-contained study, and one new subsection restates the same four-diagnostics
synthesis sentence four times. None of this calls into question the underlying Monte
Carlo results, which check out wherever independently traced to source data this round —
the problems are concentrated, as in both prior rounds, in how the new findings are
reported, hedged, and cross-referenced relative to what the underlying analysis and the
project's own tracking documents actually support. That keeps this at **major
revisions**: the fixes are demanding — one item requires either locating or re-running a
genuine 2026 λ_pol scan, and the curation question needs an actual editorial decision, not
just a caveat — but none require redesigning the second contribution's actual science.

Five independent lenses (Statistics, Novelty/positioning, Internal consistency,
Overclaiming, Scope/journal fit) each read the newly added second-contribution material in
full. 19 MAJOR findings were raised; all 19 were independently re-checked against the
manuscript and the project's supporting documents by an adversarial verification pass
instructed to try to refute each one, and all 19 survived (0 were refuted — see the footer
for how the one finding with a partially-overstated sub-claim was handled). They are
merged below into 14 numbered points: one point was raised independently by all five
lenses from five different angles, and one further point by two lenses; both are counted
once, with every raising lens credited, since independent convergence from unrelated
starting points is itself evidence the issue is real. 8 MINOR findings are listed after
the majors (one further minor duplicated a major finding's citation gap and was folded
into that major point's credit list instead of listed separately).

---

## Major points

### A. Data traceable? Two load-bearing statistical claims fail to check out against the underlying data

1. **[Statistics]** The paragraph introducing the two-field Hamiltonian's own-margin field
   (Section "A second predisposition field: socioeconomic development", lines 1043–1066)
   defends against the obvious circularity objection — that a field built from 2026's own
   margin will trivially reproduce 2026's own map — by citing a specific extension scan:
   *"scanning $\lambda_{pol} \in [0,8]$ with $\lambda_{soc}=0$ ... best-fit alignment climbs
   monotonically from 62–68% to 81–82% and the best-fit temperature drifts sharply
   downward"* and *"at the extension's low-T tail ($\lambda_{pol}=8$, $T=0.37$) [alignment
   std] is 0.6 points."* No file matching this description exists anywhere in the repository
   for 2026: the only λ_pol-extension data on disk is
   `data/processed/scan_3d_2022_polext_pol{0..8}_soc0.npz` — 2022, N=483, not 2026's N=488
   — and `git log --all` confirms only 2022-scoped files were ever committed under this
   pattern. Loading that 2022 file gives $\lambda_{pol}=8$: best_T=0.6887, best
   accuracy=80.99% — not $T=0.37$. The manuscript's own "62–68%" and "81–82%" ranges appear
   to be spliced from two different years at two different λ endpoints (2026's λ=0 value,
   67.64%, and 2022's λ=8 value, 80.99%, plus 2026's actual λ=2 grid point, 82.36%).
   00_Master_Notebook.md line 544 attributes the T=0.37 figure explicitly to 2026
   ("best-T drifts sharply low (2026: 2.6→0.37)"), so this is not a labeling slip in the
   manuscript alone — it traces back into the lab notebook. The specific per-seed spread
   check (std=2.5pp at λ=2 vs. std=0.6pp at λ=8) has no corresponding saved artifact for
   either year. This is the single piece of evidence offered to rule out the tautology
   confound as an artifact rather than a real problem, and it is currently unreproducible
   for 2026 and contradicted by the one comparable run that exists. — *Fix:* either locate
   or re-run the actual 2026 λ_pol∈[0,8] extension scan and re-derive the paragraph's
   numbers from it, or, if that scan genuinely never ran, replace the paragraph with an
   honest statement that the extension check was not completed for 2026 and the tautology
   concern is only partially addressed by the λ∈[0,2] main grid.

2. **[Statistics]** The GAM canton-level proxy's "headroom" argument (Limitations, lines
   1564–1569, echoing Section 2.4/lines 327–333) states the headline distrito-level GAM
   result is robust to proxy misclassification because *"the proxy's aggregate distrito
   count is close to the official figure, implying at most ~10-15 misclassified distritos
   out of 488."* This does not follow: aggregate/net agreement (186 proxy vs. 184 official
   = net 2) bounds only false-positives minus false-negatives, not their sum, which is the
   quantity that actually determines how many individual distritos are mislabeled and which
   can be arbitrarily larger while the net stays near zero if errors partially cancel. The
   paper's own Data section names the mechanism that produces exactly this kind of
   one-sided error (*"large, mostly rural cantons that only partially qualify (e.g. Mora,
   Alajuela's central canton, Aserrí, Paraíso)"* over-included wholesale by the canton
   proxy) but never estimates or even discusses the compensating under-inclusion
   (false negatives) that would be needed to keep the net near 2 despite this. No
   stratified sensitivity check or per-unit verification against the true distrito-level
   GAM boundary was ever run. The underlying qualitative conclusion (a $p=0.0005$ result
   with a 13.4pp effect is probably robust to this much noise) may well still be true given
   the effect size, but the specific "~10–15" bound and the phrase "implying at most" are
   not established by the reasoning given. — *Fix:* either derive the bound rigorously
   (e.g., a stratified false-positive/false-negative estimate using the named at-risk
   cantons, or an actual distrito-level GAM boundary lookup for a sample of contested
   cantons), or soften to something like "the aggregate count is close to official, though
   this does not by itself bound the number of individually misclassified units" and rely
   on the effect-size argument alone.

### B. A single stale claim, independently caught by all five reviewing lenses

3. **[Statistics, Novelty, Internal consistency, Overclaiming, Scope — raised
   independently by all five lenses, the only finding this round to be]** The Limitations
   section states: *"this paper's own novelty relative to closely related territorial
   socio-economic modeling work \citep{massoli2026} has not yet been re-checked
   specifically against the two-field extension and the GAM finding, only against the
   original single-field model (see the novelty-tracking document accompanying this
   project's code repository); we flag this as an open item rather than an implicit claim
   of novelty for the second contribution"* (lines 1577–1583). But `NOVELTY_CHECK.md`'s own
   header states *"Status as of 2026-08-22: CLEAN, now including the two-field/GAM
   extension"*, and its §2c, dated the same day, documents a completed check — a FastTrack
   duplication test, a search query, and a full re-read of massoli2026 across five
   differentiating axes (network construction, field structure, dynamics, uncertainty
   methodology, domain) — concluding: *"Verdict: the two-field/GAM extension is CLEAN...
   Massoli (2026)... differs on every one of these axes."* The manuscript sentence
   explicitly points the reader to this exact document as its source, and that document
   contradicts it. This is not a subtle inconsistency: it is the kind of thing an editor or
   referee catches by following the manuscript's own footnote, and it was independently
   flagged by every lens that touched this paragraph — the statistics referee found it while
   checking the λ_pol paragraph two sections earlier, novelty and consistency found it while
   checking positioning claims, overclaiming found it while checking whether hedges match
   underlying status, and scope found it while assessing whether the second contribution's
   framing is up to date. That degree of independent convergence is itself strong evidence
   the paragraph was simply never revisited after §2c completed. — *Fix:* replace the "open
   item" language with a statement that the check was completed and returned CLEAN, citing
   §2c's specific five-axis differentiation from massoli2026 (this is a five-minute fix that
   also strengthens the paper — there is no reason to undersell a check the authors already
   ran and passed).

### C. Internal consistency of the second contribution's own central device

4. **[Internal consistency]** Section "A second, independent field" (sec:twofield,
   lines ~413–437), which defines Eq. 2, states: *"Section~\ref{sec:mideplan} uses
   Eq.~\eqref{eq:hamiltonian2} with $h^{pol}=$ 2026's own margin and $h^{soc}=$ the
   MIDEPLAN field, scanning $(\lambda_{pol}, \lambda_{soc})$ jointly."* But sec:mideplan
   itself (lines 1043–1090) states: *"MIDEPLAN's composite IDS 2023 score... is used as
   $h^{soc}$ in Eq.~\eqref{eq:hamiltonian2} with $\lambda_{pol}=0$ (isolating the social
   field cleanly) and $h^{pol}$ unused in this section. At the distrito-level $N=488$
   network, scanning $\lambda_{soc} \in [0,2]$..."* — a 1D scan with $h^{pol}$ explicitly
   unused, not the joint 2D scan sec:twofield describes. No figure or table in sec:mideplan
   reports a genuine $(\lambda_{pol},\lambda_{soc})$ grid; the only combined data point is a
   single fixed check at $\lambda_{pol}=2$ (*"Adding the social field on top of the
   best-fit political weight... gives $+0.0$pp"*), not a scan over a range. The same
   defining subsection also states the non-circular political field (Section 4.10) and GAM
   (Sections 4.11–4.14) are each tested *"with $\lambda_{pol}=0$ and the single remaining
   field unweighted,"* implying both are plugged into the $h^{soc}$ slot Eq. 2 defines
   specifically as "the MIDEPLAN field" — but neither downstream section restates or
   clarifies this generic reuse; both simply describe a plain $\lambda=1$, $h_i$ single-field
   procedure with no reference to Eq. 2's pol/soc typing at all. A reader comparing Eq. 2's
   defining subsection against the three sections that are supposed to instantiate it cannot
   reconcile the two descriptions from the text as written. — *Fix:* either run the joint
   scan sec:twofield claims and report it in sec:mideplan, or correct sec:twofield's
   description to match the 1D-scan-plus-one-fixed-point procedure actually used, and add one
   clarifying sentence to sec:noncircular and sec:gam stating that each instantiates Eq. 2
   with $\lambda_{pol}=0$ and the tested field in the $h^{soc}$ slot.

5. **[Internal consistency]** The Abstract, Introduction, and Conclusion each state the
   paper tests *"five non-circular predisposition candidates"* — but every one of the three
   occurrences is immediately followed by an enumeration of exactly three items (the
   MIDEPLAN development index, the non-circular political-continuity field, and GAM
   membership), and no fourth or fifth top-level candidate field is ever defined anywhere in
   the manuscript. The five MIDEPLAN sub-axes tested individually in Section 4.8 (educación,
   económico, salud, seguridad, participa) cannot rescue the count, since that decomposition
   applies only to the MIDEPLAN candidate and the same "five" sentences already list the
   political field and GAM as separate items alongside it — no consistent reading of the
   text produces five. This is a headline numerical claim appearing identically in the three
   places (Abstract, Introduction, Conclusion) editors and readers check most carefully for
   self-consistency. — *Fix:* change "five" to "three" throughout, or, if a fourth/fifth
   candidate was intended and simply never made it into the draft, add it and its results.

6. **[Novelty, Internal consistency — raised independently by both]** The two flagship
   examples offered as the strongest evidence that network multistability is a genuine
   structural feature rather than noise — *"SAN JOSÉ|MORA|TABARCIA"* and
   *"SAN JOSÉ|ASERRÍ|MONTERREY,"* justified by *"cross-year consistency in the specific
   list is the strongest evidence this reflects a structural feature of the network rather
   than noise"* (Section 4.9/sec:multistability, lines 1268–1273) — sit in exactly the two
   cantons (Mora, Aserrí) that Section 2.4 names as most likely to be misclassified by the
   canton-level GAM proxy (*"large, mostly rural cantons that only partially qualify"*,
   line 329). Since the GAM field is a static, time-invariant canton-level assignment reused
   identically for 2018/2022/2026, a proxy misclassification would mechanically reproduce
   identically across years — making "cross-year consistency" unable to discriminate between
   genuine dynamical multistability and a static labeling error, contrary to how the text
   uses it. The same gap recurs in the cascade table (Table 4, sec:cascade line 1320), whose
   single largest reported cascade (size 4) is again in a flagged canton (Cartago|Paraíso|
   Orosi), again with no caveat. Section 4.8 (domain-wall), one subsection earlier, correctly
   applies exactly this caveat to its own within-GAM finding (*"we flag there that part of
   its within-GAM economic-marginalization reading may reflect proxy misclassification"*),
   and the Limitations section extends that caveat only to domain-wall, never to
   multistability or cascade, even though both build headline "structural, not noise" /
   "the real network absorbs local shocks" claims on the identical at-risk cantons.
   00_Master_Notebook.md shows the authors half-noticed this for Tabarcia specifically
   (asserting, without any actual test, that it "looks like a genuine dynamical
   multistability case, not a mislabeled-canton artifact") but this nuance never reached the
   manuscript, and the notebook's own cascade table separately classifies a different
   Mora-canton distrito (Piedras Negras) as "seed-locked, temp-fragile" — a different
   category from Tabarcia's "multistable" despite an identical proxy-error exposure,
   undermining any implicit claim that these can be cleanly triaged by category alone. —
   *Fix:* extend the Limitations proxy-imprecision caveat explicitly to sec:multistability
   and sec:cascade (not only sec:domainwall), and drop or soften "the strongest evidence this
   reflects a structural feature of the network rather than noise" until a test that can
   actually distinguish the two hypotheses (e.g., checking against a genuine distrito-level
   GAM boundary for just these few cantons) is run.

### D. Overclaiming in the highest-visibility text

7. **[Overclaiming]** Section 3.4's blanket Methods claim *"All scans use $T \in [0.05,
   3.5]$"* (line 455) is contradicted by the paper's own new content: the counterfactual
   temperature-sensitivity sweep reports a measurement *"at $T=5.0$"* (line 1287, glossed as
   "five times the best-fit temperature"), and 00_Master_Notebook.md confirms the second
   contribution's runs (MIDEPLAN, GAM, non-circular political field, and their downstream
   diagnostics) actually used $T \in [0.05, 5.0]$, a different, never-disclosed grid from the
   original ablation/FSS work. This also leaves an unreconciled internal discrepancy visible
   to any careful reader: the identical "geography-only, distrito-level, 2026" quantity is
   reported as 66.2% in Table tab:distrito (Section 4.6, the original $T\in[0.05,3.5]$
   ablation) and as 67.64% in the MIDEPLAN section (line 1072, run on the $T\in[0.05,5.0]$
   grid), with sec:mideplan itself implying an identical setup (*"the same heavy Monte Carlo
   budget validated in Section 4.5"*) — the only actual difference is the undisclosed T-grid
   change, never flagged anywhere including in the Limitations section. — *Fix:* update
   Section 3.4 to state both grids and which sections use which, and add one sentence
   reconciling the 66.2%/67.64% discrepancy so a reader doesn't have to infer it.

8. **[Overclaiming]** The Abstract's account of the GAM field's 2022-vs-2026 result
   attributes a year-to-year replication failure to the paper's spatial-resolution
   (canton-vs-distrito) scale-dependence finding: *"[GAM is] ... $p=0.0005$... for 2026,
   though this result does not replicate for 2022 ($p=0.24$), echoing this paper's own
   canton-versus-distrito scale-dependence lesson at the level of which predisposition field
   matters in which year"* (lines 76–81). These are two separate, mechanistically unconnected
   null results: the true echo of the paper's canton-vs-distrito scale-dependence finding is
   that GAM is non-significant at canton resolution for all three elections including 2026
   itself (0/16 seed-pairs each year, per the polarization-trend table) — a resolution
   effect at fixed year — not the 2022-vs-2026 replication failure, which is a year effect at
   fixed (distrito) resolution and is separately, correctly attributed in the body to being
   "2026-specific rather than a general property." The Conclusion states the analogous
   result more carefully, listing the year non-replication and the canton non-significance as
   two separate facts before invoking the scale-dependence echo; the Abstract collapses them
   into one sentence that names the wrong axis. — *Fix:* rewrite the Abstract sentence to
   name canton-resolution non-significance (not the 2022 non-replication) as the
   scale-dependence echo, matching the Conclusion's more careful phrasing.

9. **[Overclaiming, Internal consistency — the citation gap independently flagged by both]**
   The Discussion elevates GAM outperforming the other two candidates in 2026 alone into an
   unhedged general claim: *"That GAM outperforms socioeconomic development and political
   history as a predisposition proxy is itself informative about what organizes this
   election's geography: a structural center-versus-periphery cleavage, consistent with
   2026's leading movement being characterized in Costa Rican political discourse as an
   outsider, anti-capital-establishment coalition, rather than individual economic
   circumstance or historical party loyalty being the dominant axis"* (lines 1437–1443).
   Two problems compound here: (a) this is drawn from a single election year — GAM's own
   section states the result does not replicate for 2022 ($p=0.24$) — yet is phrased with
   unhedged terms ("dominant axis," "structural... cleavage") that break from the register
   the paper uses everywhere else for comparable claims, including its own GAM/domain-wall
   caveat two subsections earlier; and (b) the clause "characterized in Costa Rican political
   discourse as an outsider, anti-capital-establishment coalition" carries no citation
   anywhere in the document, unlike every other political-science claim in the paper (e.g.
   \citep{camachosanchez2025} for the analogous 2018 characterization). — *Fix:* hedge to
   "in 2026" rather than "this election's geography" generally, and either cite a source for
   the political characterization or drop the clause.

### E. Novelty-check methodology for the new material is thinner than the rest of the same document

10. **[Novelty]** NOVELTY_CHECK.md §2c's CLEAN verdict for the two-field/GAM extension rests
    on markedly thinner search coverage than §1 and §2b: those sections each ran a 4–5-engine
    sweep (OpenAlex, Semantic Scholar, FastTrack, Exa, plus a citation snowball for §1) before
    reaching CLEAN, while §2c runs only two FastTrack calls and no OpenAlex, Semantic
    Scholar, or Exa search at all — despite §2's own stated caveat that *"the Exa semantic
    sweep is not optional"* because keyword APIs are English-title-biased and miss
    Spanish-language literature exactly on this topic. Separately, §2c's primary
    `run_duplication_test` query is a single long, multi-clause descriptive sentence, which
    is exactly the over-specified-query pattern §2's own methodology caveat warns produces
    unreliable `nearest_neighbours` results ("simplify to 3–6 core-concept words"); the
    write-up nonetheless reads the resulting 10 off-topic neighbors (air-pollution CAR
    models, neuroimaging, a COVID review, colorectal cancer survival) as substantive
    confirmatory evidence rather than flagging the retrieval-quality risk the document itself
    documents for this query pattern. The CLEAN verdict may still be correct — it is not
    contradicted by anything found — but as written it is supported by weaker, internally
    inconsistent search practice than the rest of the same document. — *Fix:* add an Exa
    sweep and one or two shorter (3–6 word) FastTrack queries scoped to the two-field/GAM
    extension before relying on §2c for submission (this is cheap — the document's own
    template for §1/§2b can be reused directly).

### F. Scope and curation of the merged manuscript

11. **[Scope]** The title (*"Geography versus Predisposition in Costa Rican Presidential
    Elections: A Real-Network Ising Model Across Spatial Scales, with a Historical
    Comparison Across Election Cycles"*) and keywords mention nothing about the two-field
    Hamiltonian extension, the socioeconomic/political-continuity/GAM covariate search, or
    the four dynamical diagnostics — content occupying 9 of the paper's ~15 Results
    subsections and containing, per the paper's own Abstract, its single most statistically
    decisive finding (GAM, $p=0.0005$, 15/16 seed-pairs significant). A Physica A editor or
    reader forms their first impression of scope from the title, and this title promises a
    narrower paper than what is delivered. — *Fix:* either retitle to signal both
    contributions, or, if the intended fix is to compress the second contribution to a
    supporting role (see point 14), keep the title as-is and trim content to match.

12. **[Scope]** The abstract is 630 words — roughly 2–3× a typical Physica A abstract, and
    essentially double what round 2 already flagged as too long (~400 words) before the
    second contribution was added. It reads as two abstracts concatenated: the first ~40
    lines summarize the first contribution's four findings with a dense nested significance
    hedge, then it pivots at *"We then extend the Hamiltonian to a second, independently
    sourced field..."* into a comparably detailed second summary of MIDEPLAN, the
    non-circular political field, GAM, and the four diagnostics, with its own nested
    significance caveats. — *Fix:* cut the second contribution's abstract content to 2–3
    sentences (headline GAM result plus the scale-dependence echo), moving the
    MIDEPLAN/axis-decomposition/non-circular-field detail to the body; this shrinks further
    if point 14's compression is adopted.

13. **[Scope]** The same synthesis sentence — that the four model-native diagnostics
    converge on a robust equilibrium with uncertainty concentrated in a small,
    geographically identifiable fault-line set — is stated in near-verbatim form four
    separate times: the Abstract (lines 85–89), the end of the cascade subsection
    (lines 1339–1345), the Discussion (lines 1452–1458, somewhat more paraphrased), and the
    Conclusion (lines 1634–1639, nearly identical to the Abstract). All four occurrences fall
    within or immediately follow this round's new material. This fits a pattern both prior
    reports already flagged in the original paper (the single-seed-vs-pooled point stated
    twice, still unresolved as of round 2) — the new content reintroduces the same habit in a
    different spot. — *Fix:* state the synthesis fully once (Discussion is the natural
    place) and have the Abstract/Results-close/Conclusion each reference it in one clause.

14. **[Scope]** Three groups of new subsections are not load-bearing for any of the paper's
    five numbered headline Conclusion findings and are candidates for compression: (a) the
    MIDEPLAN axis decomposition (Section 4.8, Table 3), which reports a fully null
    Bonferroni-corrected result; (b) three of the four model-native diagnostics —
    domain-wall, counterfactual sweep, and cascade — which mainly re-demonstrate the same
    qualitative point multistability already makes most cleanly (this sub-claim is the
    strongest of the three: none of these three get a numbered Conclusion finding, and the
    Discussion itself treats their convergence as one point, already restated at the
    "one paragraph plus one table" level of granularity a compression would produce); and
    (c) the canton-level GAM polarization trend (Section 4.14). Verification found (c) as
    originally framed is not accurate as stated: its Monte Carlo null result (GAM
    non-significant at canton resolution across all three elections) is exactly what backs
    Conclusion finding (5)'s scale-dependence claim (see point 8) and the Discussion's
    explicit cross-reference to it — so this section's statistical apparatus, though not its
    raw descriptive vote-share-gap numbers, is load-bearing and should not be cut. Group (a)
    is also weaker than first appears, since it feeds the Discussion's comparative framing
    for finding (5). Only group (b) — domain-wall/counterfactual/cascade alongside
    multistability — clearly survives as a genuine, actionable compression target. — *Fix:*
    compress domain-wall, counterfactual, and cascade into one combined paragraph plus one
    summary table, keeping multistability at full length in the main text and moving the
    full breakdowns to supplementary material; leave Sections 4.8 and 4.14 as is, since both
    feed numbered headline findings once traced through the Discussion.

---

## Minor points

- **[Statistics]** "confirmed directly" (line ~1050) overclaims: the scanned ceiling
  (81–82%) is far from "almost perfectly" reproducing the real map, which the field's own
  99.8% sign-agreement would imply as the achievable ceiling if it truly overwhelmed the
  coupling term at large λ; the scan as reported shows a monotonic trend, not convergence to
  that ceiling.
- **[Novelty]** korbel2026's "double-random field" (a single field array with bimodal
  support) is genuinely different from this paper's two independently-sourced field arrays
  (Eq. 2), but the manuscript uses "double-random-field" to describe Korbel one paragraph
  before introducing its own "second, independently sourced field" without ever drawing the
  contrast explicitly, and NOVELTY_CHECK.md §2c doesn't revisit korbel2026 at all (only
  massoli2026) — a referee is likely to ask this directly; one clarifying sentence would
  close it off cheaply.
- **[Novelty]** The distrito-level GAM vote-share breakdown (31.7%/88.7%/57.0pp for 2026;
  50.0%/76.9%/26.9pp for 2022, lines ~1188–1192) does not trace to any matching entry in
  00_Master_Notebook.md, unlike nearly every other headline number in the new content —
  likely an unlogged ad hoc computation rather than an error, but should be logged and
  re-verified before submission per the project's own stated practice.
- **[Internal consistency]** Section 4.8 attaches the MIDEPLAN axes' own p-value range
  ("$p=0.038$–$0.055$") to "the composite itself," but the composite's actual paired
  p-value, stated in Section 4.7, is $p=0.058$, just outside that range — the range belongs
  to the three individual axes, reported two paragraphs later.
- **[Overclaiming]** The Discussion's claim that the domain-wall analysis is "directly
  enabled by the network coupling the regression would omit" overstates its exclusivity to
  the Ising/MC approach — a boundary-vs-interior error breakdown is computable from any
  classifier's predictions plus the adjacency graph, including a spatial-lag regression,
  which the paper itself elsewhere cites (\citep{karasiak2021}) as incorporating the same
  adjacency structure by construction. The other three diagnostics (multistability,
  counterfactual sweep, cascade) are legitimately MC-native; bundling domain-wall in weakens
  this preemptive defense.
- **[Overclaiming]** The Limitations section states the padrón-electoral demographic angle
  "was abandoned," more final than 00_Master_Notebook.md's own unchecked TODO, which lists
  live options if revisited (name-based sex inference, TSE's interactive consulta tool) —
  worth softening for consistency with the paper's otherwise careful hedging.
- **[Scope]** The Discussion's paragraph order interleaves the two contributions
  (first / second / second / first / first) rather than grouping each contribution's
  synthesis together, orphaning the finite-size-scaling and 2018-explanation paragraphs
  after the second-contribution synthesis; regrouping, or splitting into explicit
  first-contribution/second-contribution Discussion subsections (mirroring the Conclusion's
  own 1–4/5 numbering), would read as one coherent argument.
- **[Scope]** The domain-wall subsection (4.8) is the most spatially-narrative-heavy new
  content — it names specific neighborhoods and a four-way boundary/interior error pattern —
  but gets no accompanying map, unlike every comparable spatial claim in the original paper.
  This is also the one subsection the Limitations paragraph already flags as most exposed to
  GAM proxy imprecision; a map showing which distritos drive the correlation would let a
  reader judge that exposure directly.

---

## What was checked and found sound

- The GAM headline result itself (+13.4pp, direct paired $p=0.0005$, 15/16 seed-pairs
  individually significant for 2026) was not contradicted by any lens and is the paper's
  strongest number, first or second contribution.
- The Section 4.8 MIDEPLAN axis p-values (educación 0.038, económico 0.050, salud 0.055)
  and the composite's own $p=0.058$ were independently traced and are internally consistent
  with each other — only their cross-reference in the surrounding prose (minor point above)
  is off.
- The $T=5.0$ counterfactual measurement and the 2026 $\lambda_{pol}=0$ (67.64%,
  $T=2.6048$) and $\lambda_{pol}=2$ (82.36%, $T=0.848$) grid points are genuine, traceable
  2026 computations — the problem with point 1 (λ_pol circularity) and point 7 (T-grid) is
  specifically the untraced high-λ tail and the undisclosed grid change, not these
  underlying numbers.
- massoli2026's actual differentiation content in NOVELTY_CHECK.md §2c (network
  construction, field structure, dynamics, uncertainty methodology, domain) is substantive
  and, as far as this review checked, an accurate five-axis comparison — the problem is
  purely that the manuscript's own prose has not been updated to report it (point 3), not
  that the underlying novelty argument is weak.
- The cascade table (Table 4) and multistability percentages were checked against
  00_Master_Notebook.md and are internally consistent with the reported figures; the
  concern in point 6 is about the proxy-exposure caveat's uneven application, not about the
  numbers themselves.

**Dropped/partially-refuted findings** (raised by a referee, and either fully refuted or
found to survive only in part on adversarial re-check):

- The "three subsection groups not load-bearing" finding (point 14) was raised covering
  MIDEPLAN axes (4.8), the three secondary diagnostics (4.10/4.12/4.13), and the canton-level
  polarization trend (4.14). On adversarial re-check, the polarization-trend sub-claim was
  found to be backwards — its Monte Carlo null result is exactly what backs Conclusion
  finding (5)'s scale-dependence claim via the Discussion's own cross-reference — and the
  MIDEPLAN-axes sub-claim is weaker than stated for the same reason. Only the
  three-secondary-diagnostics sub-claim clearly survives. The finding is retained above
  (point 14) with this correction folded in, rather than dropped, since a genuine and
  actionable compression target remains.
