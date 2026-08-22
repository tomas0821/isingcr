---
type: referee-report
draft: manuscript/main.tex
date: 2026-08-17
verdict: major revisions
---

# Referee report — IsingCR (Physica A submission draft)

## Summary assessment

The paper's strongest point is its central methodological discipline: it is the only
manuscript in this niche (per the project's own novelty check) that fits a real
geographic-adjacency network to real multi-cycle election data with an explicit
geography-vs-predisposition ablation, and it is refreshingly honest in several places
about single-seed artifacts it previously corrected. Its weakest point is that this
honesty is inconsistently applied: the Abstract and Conclusion repeatedly state claims
in unhedged form that the paper's own body text explicitly instructs the reader not to
state that way, and the paper's central statistical workhorse (McNemar's exact test) is
applied to spatially autocorrelated data — data whose own Moran's I results the paper
reports as proof of strong spatial autocorrelation — without ever addressing that this
violates the test's independence assumption. Combined with two uncited pieces of closest
prior art (one in the *same target journal*), an admittedly outcome-selected binarization
underlying the headline results, a two-system-size finite-size-scaling claim presented as
more conclusive than standard FSS practice would support, and "available upon request"
code/data, this draft is not ready for submission as written. None of this appears to
reflect fabricated or unsound underlying computation — where the verification pass could
check against source data (e.g. the +8.7pp distrito gap), the numbers held up — the
problems are almost entirely in how findings are reported, hedged, positioned, and scoped
relative to what the underlying analysis actually supports. That makes this a **major
revisions** verdict rather than reject-and-rework: the fixes are demanding but concrete,
not a redesign of the study.

Four independent referees read the full draft (Methods/rigor, Novelty/positioning,
Results/figures, Journal fit/overreach). 35 MAJOR findings were raised; every one was
independently re-checked against the manuscript by a fifth, adversarial pass instructed to
try to refute it. 32 survived verification and are reported below (several were raised
independently by two or three referees from different angles — these are merged into one
numbered point, with all raising referees credited, since independent convergence from
different lenses is itself evidence the issue is real). 3 were refuted and are logged in
the footer, not the numbered list. 20 MINOR findings are listed after the majors.

---

## Major points

### A. Statistical validity of the headline significance claims

1. **[R1 Methods]** McNemar's exact test assumes independent paired trials, but the
   paper's own Moran's I results (I=0.706/0.485/0.354, all p<0.01, Section 4.4) confirm
   strong spatial autocorrelation in exactly the binarized outcome McNemar's test is run
   on. Applying an i.i.d. test to spatially autocorrelated data is anti-conservative
   (p-values too small), which cuts directly against the headline distrito result
   reported in the Abstract as "strongly statistically significant" (p=0.0009, N=488) —
   *"Statistical significance of a model's best-fit alignment against the trivial
   majority-class baseline is assessed with McNemar's exact test on the paired
   disagreements between the model's prediction and that baseline, following the
   validation approach used in \citep{korbel2026}."* (Section 3.4) — *Fix:* justify why
   independence holds here, or replace/supplement with a spatially-aware test (e.g. a
   spatial-block permutation test or an effective-N correction), applied everywhere
   McNemar p-values are used as headline evidence.

2. **[R1 Methods]** Every quantitative "best-fit" result in the paper is the alignment
   (and its associated p-value) at whichever temperature, out of a scanned grid, maximizes
   alignment — *"the value of $T$ that best reproduces the real map is itself an output of
   interest, not an input assumption"* (Section 3.3) — but no correction for this
   best-of-grid selection (Bonferroni/FDR, a max-statistic permutation null, or a
   held-out validation split) appears anywhere. This is a textbook optimism-bias/
   winner's-curse setup and it inflates every reported p-value in the paper, not just one
   result. — *Fix:* correct for the number of temperatures scanned, or split
   T-selection from significance testing (select on one binarization/subset, test on
   another).

3. **[R1 Methods]** The paper never states what its ubiquitous "±" figures actually are
   — sample SD across seeds, standard error, or a bootstrap CI — despite them driving
   every "beats baseline" and "overlapping error bars" judgment in the paper, including a
   dedicated table column literally headed *"1-$\sigma$ beats baseline?"* At n=8–16
   seeds the choice matters by roughly $\sqrt{n}$. — *Fix:* state explicitly, once, what
   ± denotes, and justify that choice at this seed count (a bootstrap CI would be more
   defensible than a raw SD at n=8).

4. **[R1 Methods]** The +1.2 percentage-point canton-level gap between h=0 and h=margin
   — *"a gap of $+1.2$ percentage points that sits well within the two runs' overlapping
   error bars"* (Section 4.2) — is asserted "not significant" purely by eyeballing
   whether two independently-computed intervals overlap, a well-known conservative
   fallacy. No direct paired test comparing the two models' predictions against *each
   other* (as opposed to each separately against the trivial baseline) is run anywhere in
   the paper. — *Fix:* run a direct paired test (McNemar or permutation) on the h=0 vs.
   h=margin prediction difference itself.

5. **[R1 Methods]** The paper's only method for combining significance across 8–16 seed
   replicates is vote-counting (fraction of per-seed McNemar tests with p<0.05, plus
   median p) — e.g. *"only 2 of 8 seeds for 2022 and 1 of 8 for 2026 reach individual
   significance at $p<0.05$"* (Section 4.3) — a documented low-power way to synthesize
   repeated tests, used with no formal combined-evidence method (Fisher's/Stouffer's) and
   no citation acknowledging the limitation, despite grounding major claims like "far more
   statistically robust" for the distrito result. — *Fix:* add a formal p-value
   combination method, or cite and discuss vote-counting's known weaknesses.

6. **[R3 Results]** The finite-size-scaling analysis uses exactly two system sizes
   (N=84, N=488) and calls this *"the canonical way to establish a genuine critical point
   independent of system size"* (Section 4.5) — but standard Binder-cumulant FSS practice
   requires three or more system sizes to confirm a crossing is genuinely
   size-independent rather than an artifact of one specific curve pair (any two
   non-identical curves generically cross somewhere). The paper's "confident no critical
   point found" conclusion overclaims what a two-N study can support. — *Fix:* add a
   third system size, or soften to "no evidence of a crossing between these two specific
   system sizes" with the two-size limitation stated as a reason for provisionality.

7. **[R1 Methods]** The 5-crossing "noise, not a transition" judgment in the
   finite-size-scaling section — *"the crossing count remains 5 across the scanned range
   ... still consistent with noise rather than a genuine transition"* (Section 4.5) — is
   asserted qualitatively ("a real transition produces exactly one") with no null-model
   simulation or bootstrap quantifying the expected crossing count from noise alone,
   despite the paper using formal tests elsewhere for comparable claims. — *Fix:*
   simulate/bootstrap a null distribution for spurious crossing count and report where 5
   falls in it.

8. **[R3 Results]** The temperature range and grid spacing actually scanned is never
   stated anywhere in the paper (only the count, "32 temperatures") — *"confident
   \textbf{no critical point found} in the scanned temperature range"* (Section 4.5) —
   yet the entire strength of a "no critical point found" claim depends on whether that
   range plausibly contains any true transition. — *Fix:* state $T_{\min}$, $T_{\max}$,
   and step size wherever a scan is reported, and justify the range's physical
   plausibility.

9. **[R1 Methods]** The general Monte Carlo procedure — *"runs a fixed number of
   \emph{equilibration} sweeps to let the system settle, then runs a further number of
   \emph{measurement} sweeps"* (Section 3.3) — never states sweep counts or the T-grid
   for the paper's two central results (the canton ablation, Section 4.2, and the
   historical comparison, Section 4.3). Sweep counts and grid size appear *only* for the
   finite-size-scaling section, which itself demonstrates that an under-resourced budget
   (500+500) produced invalid, non-equilibrated results at N=488 — leaving the reader
   unable to judge whether the canton-level results used an adequate budget. — *Fix:*
   state exact sweep counts and T-grid for every quantitative result, not only Section
   4.5.

10. **[R3 Results]** The canton-level ablation (N=84, baseline 60.7%) and distrito-level
    ablation (N=488, baseline 66.9%) — described as *"The result reverses the
    canton-level conclusion"* (Section 4.6) — differ not only in resolution but in N
    (statistical power), baseline difficulty, and headroom to 100% (39.3pp vs. 33.1pp),
    none of which is controlled for or acknowledged, despite the paper elsewhere showing
    clear awareness that N~84 gives McNemar tests "genuinely limited power" (Section
    4.3). The paper cannot currently rule out that part of the larger, more significant
    distrito gap is a mechanical artifact of ~5.8× more units and a different baseline,
    rather than purely a resolution effect. — *Fix:* report gaps normalized by
    available headroom, or run the canton ablation on a size-matched random subsample of
    distritos to isolate the resolution effect from the N/power effect.

### B. Abstract/Conclusion overclaiming relative to the paper's own hedged body text

11. **[R1 Methods, R3 Results, R4 Fit — raised independently by all three]** The
    Abstract and Conclusion state *"the model tracks 2022 and 2026 better than a
    majority-class baseline, but not 2018"* as an established finding, but Section 4.3
    explicitly instructs against exactly this framing after running McNemar's test (only
    2/8 and 1/8 seeds individually significant, median p=0.35/0.37): *"the historical
    result should be reported as '2018 is a confident null; 2022 and 2026 show a
    similarly sized positive point estimate that individual-seed significance testing
    cannot yet confirm,' not as an unqualified '2022 and 2026 clearly beat baseline.'"*
    Notably, the same Abstract *does* carry the significance caveat for the distrito
    result (p=0.0009) — showing the paper knows how to do this and simply didn't here.
    — *Fix:* add the McNemar caveat to the Abstract and Conclusion, or soften the claim
    to match Section 4.3's own preferred phrasing.

12. **[R1 Methods, R3 Results — raised independently by both]** Section 4.6 states the
    geography-only distrito model *"achieves $66.2\% \pm 6.4\%$ best-fit alignment --
    barely clearing the baseline at all"* — but the stated baseline is 66.9%, and 66.2%
    is *below* it, not barely above it. The paper gets the analogous 2018 canton case
    right three paragraphs earlier ("barely distinguishable from the 76.5% baseline
    itself" for a point estimate also below baseline), showing the authors know the
    correct phrasing and didn't apply it here. Fixing this would actually *strengthen*
    the paper's own reversal narrative. — *Fix:* correct to "at or slightly below
    baseline."

13. **[R3 Results, R4 Fit — raised independently by both]** The Abstract states 2018's
    true map costs *"$\sim$90\% more energy... than 2022's or 2026's patterns do"* — but
    the body's own numbers (1.13/0.77/0.59 energy units/canton) give ~47% more than 2022
    and ~92% more than 2026, a range the body itself correctly states as "roughly 50–90%
    higher." Collapsing this into one "~90%" figure applied to *both* comparators
    roughly doubles the true 2018-vs-2022 gap. — *Fix:* state the range in the Abstract,
    as the body already does.

14. **[R3 Results]** The +8.7 percentage-point distrito gain (Abstract, Section 4.6,
    Conclusion) does not arithmetically follow from Table 2's own displayed values
    (74.8% − 66.2% = 8.6, not 8.7). Verification against the underlying data
    (`data/processed/distrito_ablation.npz`) confirms 8.7 is correct from
    full-precision values (74.846% − 66.163%) — so the number itself is not wrong, but as
    displayed in the paper's own table, a reader cannot reproduce it. — *Fix:* report
    unrounded alignment values, or note the rounding order explicitly, wherever +8.7pp is
    stated.

15. **[R4 Fit]** The Conclusion's closing sentence — *"the choice of spatial resolution
    is not a mere technical convenience in sociophysical election models but can
    qualitatively change the scientific conclusion"* — generalizes to "sociophysical
    election models" as a class from one country, one election (2026, for 3 of the
    paper's 4 headline findings), and one granularity pair, with no other country,
    electoral system, or granularity pair examined anywhere in the paper. — *Fix:*
    restrict the claim to the demonstrated scope ("in this case...") and flag broader
    generalization as future work.

16. **[R4 Fit]** The title, *"A Real-Network Ising Model Across Spatial Scales and
    Election Cycles,"* promises a study across election cycles, but of the paper's four
    headline findings, only the historical comparison actually spans 2018/2022/2026 — the
    canton ablation, the finite-size-scaling analysis, and the distrito ablation
    (self-described as *"this paper's central new finding,"* Section 1) are all 2026-only.
    Three of four headline results, including the paper's own central contribution, do
    not cross election cycles. — *Fix:* narrow the title, or actually replicate the
    distrito ablation and/or FSS analysis on 2018/2022 to substantiate it as written.

### C. Novelty positioning and binarization choices

17. **[R2 Novelty]** Tiwari, Yang & Sen (2021, *Physica A* 582:126287) — an Ising model
    with a random field applied to elections, published in the *same target journal* five
    years earlier, and flagged by the project's own NOVELTY_CHECK.md as the second-closest
    prior art — sits in `references.bib` but is never cited anywhere in the manuscript
    body (confirmed by grep: the string "tiwari" appears nowhere in `main.tex`). A
    Physica A referee familiar with the journal's back-catalog will notice this omission
    immediately. — *Fix:* cite and explicitly differentiate from tiwari2021 in the
    Introduction (real adjacency network + real vote margins vs. Tiwari's synthetic
    square lattice + unconstrained field + no real election data).

18. **[R2 Novelty]** Braha & de Aguiar (2017, *PLoS ONE*) — per the project's own
    NOVELTY_CHECK.md, *"the single closest historical-comparison paper"* to this
    manuscript's own multi-election-cycle question — is also in `references.bib` but is
    never cited in the text at all (not even via `\nocite`), despite Section 4.3's entire
    premise being "does the same model work across election cycles?" — *Fix:* cite
    braha2017 explicitly in Section 4.3 and state how this paper's real-adjacency,
    real-multi-election comparison differs from Braha & de Aguiar's analytically-derived,
    "unknown network structure" model.

19. **[R2 Novelty]** The manuscript's positioning against Korbel, Dahdoul & Thurner
    (2025/26, cited as the closest prior work) is generic — *"a model whose coupling
    network is not an assumption -- a lattice, a mean-field all-to-all approximation, or
    a configuration model -- but the literal geographic adjacency structure..."*
    (Introduction) — and never states the concrete differentiating facts that the
    project's own NOVELTY_CHECK.md already established: that Korbel et al.'s model is
    solved analytically via closed-form mean-field equations with zero Monte Carlo
    simulation and zero explicit spatial network, using campaign spending (not vote
    margin) as the field. A subfield-expert referee is left to infer this unaided, and
    could plausibly read the present paper as "Korbel's idea, done with MC, on a smaller
    country" — an incremental variation, not a conceptually distinct contribution. —
    *Fix:* name Korbel et al.'s actual method explicitly and explain why the specific
    difference (not just "more real") changes what can be learned — e.g. that it enables
    the ablation a mean-field solution cannot pose.

20. **[R2 Novelty]** The coalition-split binarization underlying the paper's central
    canton/distrito ablation results is explicitly admitted to be chosen *after* seeing
    that the more natural choice was degenerate: *"a naive 'leading party vs. everyone
    else' split is degenerate for this election... This produces a competitive,
    non-degenerate split"* (Section 2.1). No pre-registration, no political-science
    criterion, and no robustness check against alternative groupings (next-2, next-4
    parties, vote-share-weighted) is offered anywhere, even though this single choice
    underlies the +1.2pp and +8.7pp headline numbers (the finite-size-scaling result, run
    at h=0, is not affected by this — the criticism does not extend to that finding). —
    *Fix:* report results under at least one alternative coalition construction to show
    the headline gaps are not an artifact of this specific 3-party grouping.

21. **[R2 Novelty]** The three parties combined into the "coalition" (Liberación
    Nacional, Coalición Agenda Ciudadana, Frente Amplio) span traditional-establishment,
    centrist, and left — did not run as an actual alliance — and the manuscript never
    argues this grouping corresponds to a real, coherent political cleavage, defending it
    solely by the statistical property of not being degenerate. Reading the resulting
    margin as "individual predisposition" (the paper's own framing) conflates internally
    divided opposition cantons with unanimous ones. — *Fix:* justify the grouping on
    substantive political-science grounds, or explicitly flag it as a statistical
    convenience and temper "predisposition" language accordingly.

22. **[R2 Novelty]** The paper uses two *different* binarizations for its two most
    citable results — coalition split for the canton→distrito ablation reversal,
    winner-vs-runner-up for the historical asymmetry — and never cross-checks either
    finding under the other scheme, even though 2026 data exists for both. This leaves
    open whether either headline finding is sensitive to which specific two-way split was
    used for that section. — *Fix:* report the ablation reversal under both
    binarizations for 2026 (data already exists per Table 1), and/or extend the
    historical comparison to the coalition-split scheme.

23. **[R2 Novelty]** The Discussion cites Korbel et al.'s reported polarization
    transition only via a bare "in contrast" citation with no substantive comparison of
    why that model finds a transition and this one doesn't — while, in the same
    paragraph, framing the real-geography constraint that the Introduction touts as this
    paper's central advance as *also* *"a limitation inherent to working with a single
    nation's real administrative geography rather than a synthetic lattice that can be
    scaled arbitrarily."* The paper argues, unreconciled, both that real geography is the
    key advantage and that it is the likely cause of the central null result. — *Fix:*
    either substantively compare model structures with Korbel et al., or reframe the
    "real network" contribution more modestly given this admitted constraint.

### D. Reproducibility and journal fit

24. **[R1 Methods, R4 Fit — raised independently by both, as MAJOR and MINOR
    respectively]** "Simulation code and the processed adjacency networks used in this
    paper are available from the corresponding author upon request" is, by current
    Elsevier/FAIR-data norms, functionally unavailable to reviewers and readers, and is
    in tension with the paper's own heavy emphasis on reproducibility (the
    pooled-vs-single-seed methodology point made repeatedly). Combined with the missing
    sweep counts/T-grids (point 9) and no stated RNG seeding scheme, the paper cannot
    currently be reproduced even in principle. — *Fix:* deposit code and processed
    networks in a persistent public repository (Zenodo/GitHub-DOI/OSF) before submission.

25. **[R1 Methods]** The T=0 relaxation stability statistics used to explain the 2018
    anomaly ("keeps 90.1% of it intact after 100 sweeps", 85.4%, 83.3%) are reported with
    no seed count, no error bars, and no pooling language — unlike every other
    quantitative claim in the paper — directly contradicting the paper's own stated
    principle that *"every result in this paper pools 8–16 independent Monte Carlo
    replicates... rather than reporting a single run."* Checking the underlying script
    confirms this really is a single-seed run, and Glauber dynamics at T=0 is not fully
    deterministic (ties at ΔE=0 still flip with probability 1/2), so "T=0 needs no
    pooling" cannot be assumed and is never stated. — *Fix:* pool this analysis across
    multiple seeds with reported uncertainty, or explicitly justify why a single run
    suffices here.

26. **[R4 Fit]** The paper's self-declared central new finding (the distrito ablation) is
    mechanically a McNemar-tested paired-classification-accuracy comparison, while the
    paper's genuine statistical-mechanics apparatus (susceptibility, specific heat, Binder
    cumulant) is used only to establish a *null* result (no critical point). The physical
    machinery functions as a fitting/search procedure for a classification task rather
    than as the source of the paper's positive physical insight — a real desk-reject risk
    for a physics journal, since a referee could reasonably read this as spatial
    statistics wearing Ising vocabulary. — *Fix:* either foreground a genuinely physical
    observable (effective coupling shift, correlation length, a $T_c$ estimate) as the
    central result, or address Physica A fit explicitly rather than assuming it.

27. **[R4 Fit]** The only explicit limitation statement in the entire manuscript is one
    sentence, scoped narrowly to the finite-size-scaling result. There is no dedicated
    Limitations subsection and no discussion of external validity for the other three
    findings beyond Costa Rica (a two-round presidential system with a fragmented
    multi-party first round) — in tension with the Conclusion's field-wide methodological
    claim (point 15). — *Fix:* add a Limitations subsection covering single-country/
    single-electoral-system scope, reliance on one granularity pair, the 2026-only scope
    of 3 of 4 headline results, and reproducibility constraints.

---

## Minor points

- **[R1]** No description of the seed-generation/numbering scheme (Section 3.5) — needed
  for exact reproducibility and to confirm the 8–16 replicates are genuinely independent.
- **[R1]** The Binder cumulant, Moran's I, and McNemar's test are used with no citation to
  their originating/standard references (Binder 1981; Moran 1950; McNemar 1947).
- **[R1]** The number of permutations used for the Moran's I test is never stated, though
  p<0.001 is reported — implying at least ~1000 permutations the reader must infer.
- **[R1]** The 2018/2022/2026 energy-cost-per-canton figures (Section 4.4) are reported
  as bare point values with no stated uncertainty, unspecified as deterministic or
  estimated.
- **[R1]** Table 1's 2018 row (76.4% vs. 76.5% baseline) shows the best-of-grid search
  never exceeds baseline for 2018 at all — worth stating explicitly as an additional,
  more direct piece of evidence for Section 4.4's explanation.
- **[R2]** 3 further bibliography entries (massoli2026, mitra2026, raducha2025) are never
  cited in the text, alongside tiwari2021 and braha2017 above — 5 of 16 references
  orphaned, suggesting the `.bib` was carried over wholesale from the Zotero collection
  rather than curated to the manuscript.
- **[R2]** The McNemar validation protocol is adopted directly from korbel2026
  ("following the validation approach used in") — worth acknowledging explicitly to
  sharpen which parts of the pipeline are genuinely new vs. adopted from the closest
  prior work.
- **[R2]** "That is the gap this paper fills" (Introduction) states a vaguer, more
  general novelty claim than the specific, narrower combination the project's own
  internal novelty check established as actually defensible — risking the paper being
  judged against a broader bar than it can defend.
- **[R3]** Figure `fig:historical` is never cited via `\ref` anywhere in the running text,
  unlike every other figure in the paper.
- **[R3]** "roughly 50–90% higher" (Section 4.4) loosely rounds 46.8% down to "50%,"
  slightly overstating how close the 2018-vs-2022 gap is to the 2018-vs-2026 gap.
- **[R3]** "a 4–9 percentage point effect" (Section 4.3) conflates the N~84 historical
  comparison's own gaps (4.0–6.4pp) with the later N=488 distrito result's ~8.7pp,
  introduced three subsections later at a different N.
- **[R3]** Grammar: "is not a artifact of pooling" → "an artifact" (Section 4.3).
- **[R3]** The distrito-level baseline (66.9%) is given with no analogous "(X of 488)"
  count, unlike the canton-level baseline, which gives an exact count.
- **[R4]** "available from the corresponding author upon request" is weaker than the
  deposited-repository standard increasingly expected by Elsevier journals.
- **[R4]** Grammar: "is not a artifact of pooling" → "an artifact" (duplicate catch,
  Section 4.3).
- **[R4]** "unlike 2026's result above" is an ambiguous cross-reference — could plausibly
  be misread as pointing to the same section's own 2026 row rather than the earlier,
  differently-binarized canton ablation.
- **[R4]** McNemar's test gets no plain-language gloss despite the paper explicitly
  aiming its physics explanations at readers with "no prior familiarity with statistical
  mechanics" — an accessibility asymmetry (physics explained to non-physicists, but not
  statistics to physicists).
- **[R4]** The single-seed-vs-pooled methodological point is stated at near-full length
  twice (Introduction and Section 3.5) — redundant, could be consolidated.
- **[R4]** A leftover `% TODO(author): add a funding/acknowledgments statement` comment
  remains in the source — resolve before submission (a "no funding" statement is standard
  even when true).
- **[R4]** "we ask a single decomposition question throughout" (Abstract) mildly
  overstates thematic unity — the finite-size-scaling search and the 2018-anomaly
  explanation don't answer the geography-vs-predisposition question at all.

---

## What was checked and found sound

- The headline +8.7 percentage-point distrito-level gain is numerically correct when
  traced to full-precision source data (`data/processed/distrito_ablation.npz`) — it is a
  reporting/rounding-display issue (point 14), not a fabricated or miscalculated number.
- The 2018/2022/2026 per-canton energy-cost figures (1.13/0.77/0.59) and the Moran's I
  values (0.706/0.485/0.354) were checked against the body text and are internally
  consistent with each other and with the qualitative "2018 is the most clustered, most
  energetically disfavored" narrative built on them.
- The "masking, not merely diluting" claim (Section 4.6/Discussion) — that canton-level
  aggregation makes the predisposition effect statistically undetectable rather than
  merely smaller — is directly supported by the paper's own significance contrast
  (canton: +1.2pp, p=0.180, not significant; distrito: +8.7pp, p=0.0009, significant) and
  survives scrutiny; two referees attempted to challenge it as an unverified causal
  overreach but were refuted on adversarial re-check (see footer) because the paper
  already and correctly hedges the *specific micro-mechanism* (opposite-margin distritos
  canceling within a canton) as untested future work, separately from the top-level
  detectability claim.
- The paper's McNemar procedure, once applied, is applied with a *uniform* yardstick
  across every result (canton ablation, historical comparison, distrito ablation) — a
  "selective rigor" charge (applying skepticism only to inconvenient results) was raised
  and refuted on adversarial re-check; the real, uniform gap is the independence-
  assumption issue (point 1), not selective application.
- The Introduction's plain-language walkthrough of the Ising model itself (compass-needle
  analogy) was checked by all four referees for clarity and was not flagged as a weakness
  by any of them.

**Dropped findings** (raised by a referee, refuted on adversarial verification, not
counted above):
- R1 raised a "selective rigor" charge (skepticism applied to the historical comparison
  but not the distrito headline result) — refuted: the McNemar procedure is applied
  uniformly across all results; the paper's silence on multiple-comparisons/spatial-
  independence caveats is uniform across the whole paper, not selectively withheld from
  the headline finding.
- R3 raised "masking, not merely diluting" (Section 4.6) as an unverified causal
  overreach — refuted: the detectability claim is directly supported by the paper's own
  significance contrast; only the specific micro-mechanism is speculative, and that part
  is already correctly hedged as future work.
- R4 raised the same "masking, not merely diluting" point independently — refuted for the
  same reason.
