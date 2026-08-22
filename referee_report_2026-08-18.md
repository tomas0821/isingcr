---
type: referee-report
draft: manuscript/main.tex
date: 2026-08-18
verdict: major revisions
---

# Referee report — IsingCR (Physica A submission draft), Round 2

## Summary assessment

This is a second round on a draft that already went through one major-revisions cycle
(`referee_report_2026-08-17.md`). The revision made real progress: of that report's 32
confirmed MAJOR findings, roughly 28 are now substantively resolved — new citations for
previously-orphaned prior art, exact sweep counts and T-grids everywhere, a spatially-aware
test introduced alongside McNemar's, a Bonferroni correction for the temperature-grid
search, a resolution-matched subsample check and a cross-binarization check for the
distrito headline finding, a Limitations subsection, and a funding statement. That is a
genuine, substantive response, not a cosmetic one — most of round 1's specific numbers were
independently re-verified against the current file this round and hold up.

But four of round 1's MAJOR points remain substantively unresolved rather than fixed: data
and code are still "available upon request" rather than deposited (round 1 #24), no direct
paired test between the two ablation arms' own predictions was ever added (round 1 #4), the
canton-side ablation still has zero robustness check against an alternative binarization or
coalition composition (round 1 #20/22), and the paper's only positive headline finding is
still established purely via classification accuracy with no physical-observable translation
(round 1 #26) — in each case the fix applied was to *disclose* the gap more clearly in
Limitations, not to close it. More concerning: the machinery added to fix round 1 introduced
its own new problems that got past authorial review — an internal contradiction between a
table and its own adjoining prose on a number that backs a headline robustness claim, an
Abstract/Conclusion that quietly rounds a body-text-labeled "significant" result into
"marginal or non-significant," a Bonferroni correction applied to a median-of-p-values
without justification (plus an unexplained arithmetic gap), and a newly introduced
significance test whose reported p-values carry no stated sample size or Monte Carlo error.
Separately, the revision's Introduction now folds the distrito-level "cross-scale" finding
into the paper's explicit novelty claim, but the project's own `NOVELTY_CHECK.md` was run
and dated entirely at canton-level scope, with its own tracked re-check step for
distrito-level scope still unchecked. None of this suggests unsound underlying computation —
where checked, the paper's numbers are internally traceable to source, and the added
robustness checks are real, useful work — the problems are concentrated in the same place
round 1's were: how precisely results are characterized in the highest-visibility text
(Abstract, Conclusion, table captions) relative to what the body actually supports. That
keeps this at **major revisions**, not reject-and-rework: the outstanding items are demanding
but concrete, and several are cheap fixes (state a seed count, fix a table cell, soften two
words) even where others require new work (deposit code, run one more robustness check).

Four independent referees re-read the current draft (Methods, Novelty/positioning,
Results/figures, Journal fit/overreach), each also checking their own lens's round-1 points
for genuine resolution. 13 MAJOR findings were raised; every one was independently
re-checked by a fifth, adversarial pass instructed to try to refute it. 12 survived
verification and are merged below into 10 numbered points (two pairs were raised
independently by two lenses from different angles and are counted once, both referees
credited). 1 was refuted and is logged in the footer. 13 MINOR findings are listed after the
majors, merged to 12 for the same reason.

---

## Major points

### A. Round-1 fixes that remain disclosed, not resolved

1. **[R1 Methods, R4 Fit]** The paper's central canton-level null claim — Abstract: *"adding
   the field improves best-fit alignment with the real map by only $+1.2$ percentage points
   over geography alone, statistically indistinguishable from zero"* — is still not backed
   anywhere by a direct paired test between the two ablation arms' own predictions. Section
   4.2 admits as much: *"This overlap check is a conservative heuristic, not a direct paired
   test of the two models' predictions against each other (no such test is run in this paper
   -- see the caveat below)"* — but no such caveat exists anywhere else in the document (the
   word "caveat" appears exactly once, at this sentence, and resolves to nothing). Round 1
   finding #4 asked for exactly this test and it was not added; the Abstract states the
   heuristic's conclusion as an unqualified statistical fact. — *Fix:* run McNemar's or a
   permutation test directly on the paired disagreement between the h=0 and h=margin
   predictions (canton and distrito), report the p-value, and either support or soften the
   Abstract's "statistically indistinguishable from zero" accordingly.

2. **[R1 Methods, R4 Fit]** Data and code availability is unchanged in substance: *"Simulation
   code and the processed adjacency networks ($J$, $h$, and empirical spins for every
   headline result in this paper) are available from the corresponding author upon
   request."* Round 1 finding #24 asked for deposit in a persistent public repository
   (Zenodo/OSF/GitHub-DOI) given Elsevier/FAIR-data norms and the paper's own heavy
   reproducibility framing. The revision's only change was to name this as a limitation
   (*"rather than deposited in a persistent public repository"*) rather than fix it — no DOI,
   repository URL, or archive citation appears anywhere in the document. — *Fix:* deposit
   code and the processed $J$/$h$/spin arrays in a citable repository and cite the DOI, or
   explicitly own the "upon request" choice as a deliberate decision (e.g. embargo,
   institutional policy) rather than an unaddressed gap.

3. **[R2 Novelty]** Section 4.2's headline canton-level null and Section 4.6's headline
   distrito-level reversal are compared directly (*"the choice of spatial resolution... was
   not a mere technical convenience but qualitatively changed the conclusion"*) despite the
   canton side having zero robustness check against an alternative binarization or coalition
   composition — only the distrito side got the winner-vs-runner-up and resolution-matched
   subsample checks added this round. Round 1 points 20/22 asked for this on both sides; the
   Limitations subsection now honestly discloses the gap (*"we did not repeat either check
   for the canton-level ablation... and did not try alternative coalition groupings"*) but the
   check itself still doesn't exist. — *Fix:* rerun the canton-level ablation under at least
   the winner-vs-runner-up binarization (2026 data already used for this in Section 4.3) to
   confirm the near-zero canton gap isn't itself an artifact of the specific 3-party
   coalition choice.

4. **[R4 Fit]** The Limitations subsection now explicitly names the concern round 1 raised as
   point 26 — that the paper's only positive finding (the distrito ablation) is a paired
   classification-accuracy comparison, while the genuine thermodynamic machinery
   (susceptibility, specific heat, Binder cumulant) is used only to support the null FSS
   result — but adds no physical translation of the +8.7pp effect (no effective coupling/field
   estimate, no correlation length, no $T_c$ shift argument). If anything this round's three
   new robustness checks (spatial-block sensitivity, resolution-matched subsample,
   cross-binarization — collectively ~170 lines, by far the paper's longest results
   subsection) push the paper further toward spatial-statistics methodology and further from
   statistical mechanics, without adding compensating physical content to the headline claim.
   Honest disclosure of a desk-reject risk is not the same as removing it. — *Fix:* either
   compute a genuine physical observable tied to the distrito effect (effective field/coupling
   magnitude at the best-fit $T$, or a correlation-length estimate), or address Physica A fit
   explicitly in the cover letter rather than relying on the Limitations sentence alone.

### B. New problems introduced by this round's own revisions

5. **[R1 Methods]** The newly introduced spatial block permutation test — now the paper's main
   answer to the McNemar-independence critique, and the basis for walking back the headline
   McNemar significance claim — never states how many permutation draws were used. Exact
   enumeration is feasible for the 7-province blocking ($2^7$ configurations) but not for the
   84-block or ~165-block cases that produce the headline $p=0.064/0.377/0.068/0.019$ figures
   ($2^{84}$, $2^{165}$ configurations), meaning Monte Carlo sampling of the permutation null
   must have been used — yet no sample count, convergence check, or Monte Carlo standard error
   is reported for p-values quoted to 2–4 significant figures (e.g. $p=0.0001$, $p=0.019$). —
   *Fix:* state the number of permutation draws (or confirm exact enumeration where feasible)
   for every spatial-block result, with a Monte Carlo SE or CI wherever sampling was used.

6. **[R1 Methods]** The resolution-matched subsample check — cited in the Abstract as ruling
   out a pure statistical-power artifact behind the distrito headline finding — never states
   the seed count, sweep budget, or temperature grid used per subsample, unlike every other
   quantitative result in the paper. Table 2's own *"underpowered per-sample (2/10 sig.)"*
   entry suggests McNemar was run once per subsample rather than pooled across seeds within
   each subsample — which, if true, is exactly the single-seed pattern the paper elsewhere
   insists must be pooled before being trusted (Section 3.5). — *Fix:* state the seed count,
   sweep budget, and T-grid for the 10 subsamples, and clarify whether each subsample's
   figure is itself seed-pooled.

7. **[R1 Methods]** The Bonferroni correction, defined in Section 3.3 as raw $p$ times grid
   size for a single test, is applied throughout Sections 4.2/4.3/4.6 to the *median* of
   per-seed McNemar p-values instead — a quantity with no stated argument for why multiplying
   it by the grid size still controls the intended family-wise error rate. Separately, the
   displayed arithmetic doesn't reproduce: $0.026 \times 24 = 0.624$, not the stated
   *"corrected $p=0.633$"* — plausibly just a rounding-order artifact (as the paper correctly
   disclosed for the +8.7pp figure elsewhere), but no full-precision median is given here to
   let a reader confirm that. — *Fix:* justify Bonferroni-correcting a median-of-p-values (or
   correct each seed's raw p-value individually before vote-counting), and report
   full-precision medians wherever a corrected figure is quoted.

8. **[R2 Novelty]** The Introduction's novelty-claim sentence now explicitly includes
   *"cross-scale replication"* — i.e. the canton-vs-distrito ablation reversal, elsewhere
   billed as *"this paper's central new finding"* — as part of the paper's defended novel
   contribution. But `NOVELTY_CHECK.md`'s CLEAN verdict was run and scoped entirely at
   canton-level (§1's claim-under-defense: *"binarized canton-level election outcomes"*,
   *"the REAL geographic border-adjacency network between cantons"*; all §2 queries are
   canton/municipality phrasing), and its own §5 re-check schedule explicitly flags: *"If
   scope expands to distrito-level (492 nodes)... re-run the corner queries at that
   finer/broader scope -- the current 'clean' result is specific to canton-level, single-country
   framing."* `00_Master_Notebook.md` still carries an unchecked `[ ]` item to do exactly this
   before drafting for Physica A — and drafting has manifestly proceeded well past that
   checkpoint. — *Fix:* re-run the NOVELTY_CHECK.md §2 queries at distrito scope and update
   the verdict to explicitly cover the cross-scale claim, or soften the Introduction to keep
   only the canton-level-scoped claim as the stated novelty, presenting the distrito finding
   as a result rather than part of the positioning claim.

9. **[R3 Results]** Table 2's *"Contiguous subsample avg., coalition split... underpowered
   per-sample (2/10 sig.)"* directly contradicts the adjoining prose describing the identical
   check: *"the individual subsamples in the $N$-matched check are each too small to reach
   significance on their own"* — "each too small" asserts 0/10, not 2/10. This is a
   table-vs-text mismatch on the number backing the paper's key evidence against a
   statistical-power artifact in its central new finding, and the table's own column header
   (*"McNemar $p$ (seeds sig.)"*) isn't satisfied by this row at all — no p-value is given. —
   *Fix:* reconcile the two (report the correct fraction and, ideally, the per-subsample
   p-value range, consistent with the column header), or correct whichever number is wrong.

10. **[R3 Results]** The Abstract and Conclusion both compress the three-granularity
    spatial-block sensitivity sweep into *"marginal or non-significant"* — but the body text
    it's drawn from explicitly labels the three values differently: *"gives median
    $p=0.377$, $0.068$, and $0.019$ respectively: clearly non-significant, marginal, and
    significant, in that order."* $p=0.019$ is significant at the paper's own stated
    $\alpha=0.05$ threshold. The body does offer a real reason to distrust that endpoint (finer
    blocking converges toward McNemar's own anti-conservative answer), but that reasoning
    never reaches the Abstract or Conclusion — both simply drop the one result that would
    complicate the paper's hedged narrative. — *Fix:* state the range with its correct label
    ("non-significant to significant, depending on blocking choice") in the Abstract and
    Conclusion, or carry the discounting rationale forward explicitly rather than silently
    rounding it away.

---

## Minor points

- **[R1]** Round-1 finding #3 asked the paper to state *and justify* what "±" denotes; the
  revision states it (sample SD across seeds) but never justifies the choice over a bootstrap
  CI at n=8–16, despite that specific suggestion being made in round 1.
- **[R1]** The 66.9% distrito baseline is explicitly computed pre-exclusion (N=492, *"before
  the 4 exclusions"*) but reused unchanged as "the" baseline throughout the N=488
  post-exclusion analysis, including the headroom calculation.
- **[R1]** The block-size sensitivity sweep (*"a further independent replicate"*, singular)
  reports a "median $p$," which requires multiple seeds — but the seed count is never stated,
  unlike every other Monte Carlo result in the paper.
- **[R2]** Round-1 point 18 asked for braha2017 to be cited and differentiated in Section 4.3,
  since that section's entire premise ("does the model work across election cycles?") is
  Braha & de Aguiar's question; the citation was added, but only in the Introduction — the
  string "braha" never appears in Section 4.3 itself.
- **[R2]** The McNemar validation protocol's direct adoption from korbel2026 ("following the
  validation approach used in") is byte-for-byte unchanged since round 1's minor-points list
  asked for this to be acknowledged explicitly.
- **[R2]** mitra2026 (Dirichlet-Swing) — per NOVELTY_CHECK.md, the closest cited work to the
  paper's district-level, geography-driven, multi-election angle — gets a bare namedrop with
  no differentiation, unlike tiwari2021/braha2017/korbel2026, especially notable now that the
  distrito-level finding is foregrounded as the paper's central contribution.
- **[R2, R4]** The Abstract/Conclusion describe the spatial block permutation test as
  something *"we introduce,"* overstating its novelty; the body correctly and more modestly
  credits it as *"a restricted-randomization design in the sense of \citep{besagclifford1989}"*
  — a reader who only skims the Abstract won't see that attribution.
- **[R3]** Round-1 finding #8 asked for $T_{\min}$, $T_{\max}$, and step size; endpoints and
  point-count are now stated everywhere, a real improvement, but whether the grid is linearly
  or log-spaced is still never stated explicitly (inferable only by back-solving Table 2's
  "T at best" values).
- **[R3]** The Conclusion's Bonferroni-corrected $p=0.0030$ for the distrito result is drawn
  from a separate, later independent 16-seed replicate at a single already-selected
  temperature, not from re-scanning the original headline grid — a reader cannot tell these
  are different runs from the Conclusion text alone.
- **[R4]** The Abstract runs to roughly 400 words, close to double a typical Physica A
  abstract, now layered with nested statistical caveats added in response to round-1
  fixes — satisfying "don't overclaim" at a real cost to accessibility for a physics
  audience.
- **[R4]** Section 4.6 (distrito ablation) has grown into by far the longest, most
  statistically dense results subsection — three separate robustness checks plus two tables —
  disproportionate to the paper's other five results subsections and light on physical
  interpretation relative to test-choice sensitivity.
- **[R4]** The single-seed-vs-pooled methodological point is still stated at near-full length
  twice (Introduction and Section 3.5), unchanged since round 1 flagged this as redundant.

---

## What was checked and found sound

- All three previously-uncited pieces of prior art (tiwari2021, braha2017) and the
  previously-orphaned references (massoli2026, mitra2026, raducha2025) remain correctly cited
  in the body; all 19 bibliography entries are cited somewhere in the text (re-verified this
  round, not just carried over from round 1).
- The funding statement, the fixed "barely clearing baseline" direction error, the fixed
  +8.7pp rounding-provenance note, the narrowed title, and the grammar/figure-reference fixes
  from round 1 all remain in place and were not re-flagged by any referee this round.
- The +8.7 and +11.6 percentage-point distrito effect-size figures were independently
  re-traced through Table 2 and the surrounding prose and are internally consistent (aside
  from the "2/10 sig." vs. "each too small" contradiction in finding 9, which concerns
  significance reporting, not the effect-size numbers themselves).
- The Abstract's "ruling out a pure statistical-power or binarization-choice artifact"
  parenthetical was challenged by R4 as overclaiming relative to the body's softer "evidence
  against" language — but on adversarial re-check this was refuted (see footer): the very
  next clause of the same Abstract sentence explicitly states that formal significance is
  *not* robust to test/binarization choice, so the "ruling out" language is correctly scoped
  to effect size only, not significance, and is not buried elsewhere in the document.
- The two new citations added this round (besagclifford1989 for the spatial block
  permutation test, karasiak2021 for the McNemar-under-spatial-autocorrelation pitfall) were
  checked for fit and are appropriate, substantive additions, not padding.

**Dropped findings** (raised by a referee, refuted on adversarial verification, not counted
above):
- R4 raised the Abstract's "ruling out a pure statistical-power or binarization-choice
  artifact" phrase as overclaiming relative to the body — refuted: the same Abstract
  sentence's very next clause already states that formal significance "ranges from strongly
  significant... to marginal or non-significant... showing that... statistical confirmation
  remains sensitive to test and binarization choices," so the caveat the referee said was
  missing is present, unmissable, and in the same sentence, not buried elsewhere.
