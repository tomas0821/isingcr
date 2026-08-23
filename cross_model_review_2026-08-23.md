---
type: cross-model-review
draft: manuscript/main.tex
date: 2026-08-23
referees: [kimi-k3 (moonshot-ai, via kimi Code CLI), codex (gpt-5.6-terra, via OpenAI Codex CLI)]
verdict: fixed and re-verified -- see disposition below
---

# Cross-model review — IsingCR (round 2: kimi + codex)

This is a second cross-model round, run the day after the first (agy/deepseek, see
`cross_model_review_2026-08-22.md`) once kimi and codex became available. The manuscript
had already been revised in response to that first round and a subsequent abstract polish
pass, so this round reviewed the current, already-once-cross-model-reviewed draft — a
genuinely fresh read, not a re-run of the same version.

**kimi** ran as `kimi` (Moonshot's newer "Kimi Code" CLI, distinct from the `kimi-cli`
binary used unsuccessfully in round 1 — that one remained unauthenticated; this is a
different, now-working installation), default model `moonshot-ai/kimi-k3`. Two attempts
were needed: the first hung waiting on an unstated tool-approval prompt and was killed by
an 8-minute timeout with only a partial reasoning trace written; the second, run without
the conflicting `--yolo`/`--prompt` combination and given a long background timeout,
completed cleanly in full.

**codex** ran as `codex exec -s read-only`, model `gpt-5.6-terra`. Completed in one pass.

## Summary assessment

**kimi's review is the most valuable single pass this project has received from any
model, same or cross, across both rounds.** Every one of its four MAJOR findings pointed
at an actual, verifiable defect — three of them are numbers that disagree with each other
or with a value already on disk, not matters of interpretation, and the fourth is a real,
self-inconsistent methodological policy. All four independently verified true.
**codex's** review reused two claims already refuted in round 1 (the same 999-draw
misreading of the headline $p$-value, and the same misreading of an existing
self-reconciliation passage as an unaddressed inconsistency), several already-disclosed
limitations restated as fresh findings, and one claim (label-symmetric scoring) refuted
by a physics justification already in the text it quoted from two lines earlier — but it
also surfaced two independently checkable, real gaps (seed/stride reproducibility,
boundary-file provenance) that overlapped with kimi's own findings and are now fixed.

Of kimi's MINOR findings, most were also real and cheap to fix (missing Glauber/MAUP
citations, an imprecise Eq. 2 description, unstated $\lambda$-scan grid density, a
self-contradictory sentence in the Limitations section) and have been applied. A few were
correctly identified as real but require new computation (per-seed SD for two results
tables) or are genuine editorial judgment calls already decided in a prior round (the
title) — these are listed as open/deferred below, not silently dropped.

## Major points — all confirmed, all fixed

1. **[kimi]** Table~\ref{tab:historical}'s 2026 row (`$p=0.37$, 1/8`) and the near-identical
   text passage cross-checking the coalition split against winner-vs-runner-up binarization
   (`McNemar median $p=0.363$, 0 of 8 seeds significant`) report the *same* underlying
   2026 canton, winner-vs-runner-up run — identical point estimate (79.0%±2.2%), identical
   baseline (75.0%), identical median $p$ (0.36 vs. 0.37, rounding) — but disagreed on the
   seed-significance count. Checked against `00_Master_Notebook.md` (line 366-368, "2022
   and [2026] respectively (median p=0.35, 0.37)... 1/8 seeds"), which confirms 1/8 is the
   correct, notebook-recorded figure; the prose passage's "0 of 8" was a transcription
   slip. *Fixed*: corrected to "1 of 8" with an explicit note that this is the same run as
   Table~\ref{tab:historical}, restated for the binarization comparison.

2. **[kimi]** Internal inconsistency in multiple-testing policy: `sec:mideplan` states its
   fixed-best-$T$ direct paired test "is not itself a best-of-grid statistic... and so
   needs no such correction," while `sec:ablation-distrito`, addressing the identically
   structured fixed-best-$T$ paired test, explicitly applies the 32-point Bonferroni
   correction anyway ("we... computed both a Bonferroni correction for the 32-point
   temperature grid and the spatial block permutation test," giving $p=0.064 \to 1.000$
   once corrected). Verified directly by reading both passages side by side. *Fixed*:
   applied the same conservative correction to the MIDEPLAN and GAM paired tests for
   consistency (MIDEPLAN: $p=0.058 \to 1.000$, GAM: $p=0.0005 \to 0.016$, still
   significant under the stricter treatment) and reworded the "needs no correction"
   claim to instead describe applying it as a conservative check, matching
   `sec:ablation-distrito`'s own practice.

3. **[kimi]** The 2022 distrito-level network's $N=483$ (vs. 2026's $N=488$) is used
   throughout `sec:mideplan`--`sec:polarization-trend` with no explanation anywhere in the
   Data section, which only documents the 492→488 exclusion process for 2026. Verified by
   rebuilding the 2022 network directly (`build_distrito_graph_and_fields()` from
   `run_3d_scan_2022.py`): confirms 7 adjacency nodes (not 2026's 2) have no matching 2022
   results row, on top of the same 2 isolated-island drops (492 − 2 − 7 = 483). Two of the
   seven are explained by administrative history already established elsewhere in the
   paper (Monteverde and Puerto Jim\'enez were created as independent distritos only after
   the 2022 election); the remaining five (Birrisito, La Victoria, Puente Salas, \'Angeles,
   Lagunillas) are additional 2022-specific name-reconciliation gaps not individually
   traced. *Fixed*: added this explanation to `sec:data`, distinguishing the traced two
   from the untraced five rather than implying a complete explanation.

4. **[kimi, codex — independently, overlapping]** Reproducibility gaps in Methods:
   (a) the base seed and stride behind "a fixed base seed offset by $k$ times a large
   stride" were never given numerically. Verified against `scripts/run_3d_scan.py`
   (`FULL_SEED = 7`) and `src/isingcr/simulation/monte_carlo.py`
   (`seed_stride: int = 10_000`, never overridden anywhere in the scripts checked).
   (b) the boundary shapefile's version, valid-as-of date, and CRS were never stated.
   Verified directly against the shapefile's own attribute table
   (`cri_admin3.shp`: `version='v01'`, `valid_on=2024-12-03`, `crs=EPSG:5367`
   / CRTM05). *Fixed*: both added to `sec:data` with the verified concrete values.

## Minor points — fixed

- **[kimi]** Glauber dynamics introduced with no citation while Binder, McNemar, and
  Moran all receive theirs. *Fixed*: added `\citep{glauber1963}` (Glauber, J. Math. Phys.
  4, 294 (1963), DOI 10.1063/1.1703954 -- verified).
- **[kimi]** The MAUP paragraph credits only a 2014 empirical study, omitting the
  foundational reference a geographically literate reader would expect. *Fixed*: added
  Openshaw (1984), CATMOG No. 38 -- the standard foundational MAUP citation -- alongside
  Russo & Beauguitte.
- **[kimi]** "Collapses exactly to Eq.~1... when $\lambda_{pol}=0$ or $\lambda_{soc}=0$" is
  imprecise: the surviving term is $\lambda h^{\cdot}$, which equals Eq.~1's fixed,
  unweighted $h_i$ only when the surviving weight is additionally 1. *Fixed*: reworded to
  state the effective field explicitly and note the exact-recovery condition includes the
  unit-weight case used throughout the paper.
- **[kimi]** The Limitations section's field-selection-multiplicity sentence reported a
  Bonferroni-style correction and then said in the same breath that "the correction itself
  was not applied or reported" -- self-contradictory as written. *Fixed*: reworded now
  that finding #2 above means the correction genuinely has been applied and reported.
- **[kimi]** `tab:robustness`'s stated reason for retaining the pre-exclusion 66.9\%
  baseline ("for consistency with... the underlying Monte Carlo runs") is a non sequitur
  -- the baseline is a post-hoc scoring reference, not an MC input. *Fixed*: reworded to
  cite consistency with the already-generated figure/table only.
- **[kimi]** "$U_4$'s physically valid range $[0, 2/3]$" overstates the bound as an
  absolute mathematical constraint; negative $U_4$ is not itself forbidden and is a
  recognized diagnostic of sampling that mixes distinct metastable configurations, not
  purely of non-equilibration. *Fixed*: reworded to "the range $U_4$ is expected to
  occupy at true equilibrium" and added one clause noting negative values are a
  recognized (not merely erroneous) diagnostic, while still correctly attributing this
  paper's specific dips to insufficient equilibration.
- **[kimi]** "A closed-form mean-field solution like Korbel et al.'s... cannot pose [the
  ablation] in the first place" overreaches -- nothing prevents re-solving a mean-field
  model at zero field and comparing; the ablation is un-*posed* in Korbel et al., not
  un-*poseable*. *Fixed*: reworded to "does not pose," with the reason (no literal network
  topology to isolate a contribution from) stated explicitly instead of implied.
- **[kimi, codex — independently, same substance]** Genuinely relevant real-election
  spatial-statistics prior art (Borghesi \& Bouchaud 2010's diffusive field model on
  French vote data; Fern\'andez-Gracia et al. 2014's noisy voter model with
  recurrent-mobility networks on US county returns) was absent from the related-work
  survey despite using real vote data at real spatial units, closer in that specific
  respect than most of the cited physics literature. Both verified as real, correctly
  cited papers via web search (DOIs confirmed). *Fixed*: added to the Introduction with
  brief method differentiation (diffusion equation / voter model, not a literal
  border-adjacency Ising Monte Carlo fit).

## A conceptual point, addressed with a scope clarification rather than a retraction

- **[kimi]** GAM membership is, substantively, a geographic classification (capital-region
  membership) even though it enters the Hamiltonian in the field slot the paper labels
  "predisposition" -- so the headline finding "GAM beats socioeconomic development and
  political continuity" is not evidence that non-geographic individual predisposition
  matters more than geography in some mechanism-neutral sense; it is evidence that this
  specific geographically defined classification carries more of what the field term can
  capture than the two alternatives tested. This is a real, non-trivial scope point, not a
  factual error -- the paper's own population-confound paragraph already gestures at
  something similar without stating it this directly. *Addressed*: added one paragraph to
  `sec:gam` immediately after the population-confound discussion, making this distinction
  explicit rather than leaving a reader to infer it.

## What was checked and refuted

- **[codex]** "A 999-draw Monte Carlo randomization test cannot yield [$p=0.0005$'s]
  individual-seed resolution" -- the same claim round 1's deepseek referee made and that
  was refuted there by checking the actual saved permutation output
  (`data/processed/gam_paired_test.npz`): 8 of 16 per-seed raw $p$-values are exactly
  0, one is 0.001001; the median of 16 values is the average of the 8th/9th order
  statistics, giving exactly 0.0005005. Ordinary median arithmetic over a discrete
  distribution, not a bug. Re-refuted on re-check.
- **[codex]** Table 3's 66.9\%-baseline-on-492-units "is formally inconsistent" with the
  $N=488$ analysis sample -- codex quoted the manuscript's own explicit reconciliation of
  this exact discrepancy (lines 878-885: "...a 0.1 percentage-point difference immaterial
  to every gap and significance figure reported in this section...") as if it were an
  unaddressed error. The quoted text is the reconciliation, not the problem -- the same
  failure mode round 1's agy referee showed on a parallel 66.2\%/67.64\% claim. (kimi's
  narrower, correct point on the same passage -- that the stated *reason* for the
  retention is a non sequitur, not that the retention itself is wrong -- survives and is
  fixed above.)
- **[codex]** Label-symmetric scoring "not based on a common scoring rule" between the
  $h=0$ and $h\neq0$ arms -- refuted directly by the text two paragraphs earlier
  (`sec:model`, Formal definition): "at $h=0$ the Hamiltonian is symmetric under flipping
  every spin simultaneously... so the model cannot distinguish 'traditional' from
  'emerging' labeling on its own; all $h=0$ comparisons... therefore use a label-symmetric
  alignment score." This is a deliberate, physically justified asymmetry (the field breaks
  the labeling ambiguity at $h\neq0$), not an inconsistency.
- **[kimi]** GAM's "most decisive result... including the own-margin field" claim is not
  like-for-like because the own-margin field's separately-discussed "best-fit weight"
  ($\lambda_{pol}=2$, part of the circularity-check extension scan) was never run through
  the same paired test GAM won. Checked: the comparison GAM's claim is actually based on is
  against the *original* ablation's Arm B at the paper's standard unweighted ($\lambda=1$)
  convention -- the same convention GAM itself uses -- which *is* run through the identical
  paired test (`sec:ablation-distrito`, $p=0.020$, 10/16). The $\lambda_{pol}=2$/8
  extension is a separate, explicitly non-headline methodological check (the paper itself
  says so: "not reported as a finding... a methodological check ruling out an artifact").
  Comparing GAM against that inflated, self-flagged-as-not-a-finding number would be the
  actual error; comparing against the standard-convention own-margin result, as the paper
  does, is the correct like-for-like comparison.
- **[kimi]** Figure~\ref{fig:domainwall}'s caption ("each election's own GAM best-$T$")
  implies a different protocol from `sec:gam`'s "67.16\% at the same $T$" for 2022.
  Checked against `data/processed/gam_field_2022.npz`: 2022's own independently-scanned
  best-$T$ genuinely is $T=1.008$ (identical to 2026's), confirmed directly from the saved
  scan output (`best_T: 1.008...`, `best_accuracy: 0.6716`). Not a protocol mismatch --
  the two years' independent optima happen to coincide.

## What was checked and left as-is (already disclosed, or a standing editorial decision)

- **[codex]** Best-of-grid selection bias / no held-out validation / no max-statistic
  permutation null -- restated, more forcefully, a limitation the manuscript already
  discloses at length in multiple places (`sec:model`'s Bonferroni-correction paragraph
  explicitly declines the max-statistic null and says why; `sec:limitations` repeats this).
  Not a fresh gap; implementing genuine cross-validation or a max-statistic null is a
  substantial new analysis, not a text fix, and is out of scope for this pass.
- **[codex]** Coalition-split binarization chosen post hoc, not pre-registered --
  restated, almost verbatim, `sec:data`'s own existing disclosure ("it was chosen
  \emph{because} the more obvious... split is degenerate for 2026, not pre-registered
  independently of the outcome").
- **[codex]** GAM proxy confounded by population/urbanization -- restated `sec:gam`'s own
  existing population-confound paragraph.
- **[kimi]** Two results tables (`tab:mideplan-axes`, `tab:polarization-trend`) report
  point-estimate alignments with no $\pm$ SD, inconsistent with the paper's own stated
  convention. Confirmed real: checked the saved `.npz` artifacts for these runs and found
  only the pooled scalar `best_accuracy` was retained, not per-seed values -- the SD is
  genuinely not recoverable without a new run that collects per-seed data. **Deferred**,
  not fixed: this needs new computation (a cluster re-run), not a text edit, and was not
  authorized in this pass.
- **[kimi]** The three-clause title is unwieldy and the "Search for..." framing undersells
  the contribution. Same finding as round 3's N12 (in the earlier same-model referee
  sequence) and round 5's F5-adjacent discussion -- already explicitly considered and left
  as a deliberate author choice ("a judgment call, not a correctness issue"). Not re-opened.
- **[kimi]** The paper reads as two papers stapled together at ten results subsections;
  consider splitting or moving detail to a supplement. A scope/curation judgment call
  already extensively worked through in the prior same-model referee sequence (compression
  of three subsections into one, abstract restructuring). Not re-opened without further
  instruction.
- **[kimi]** Three novelty-critical references (korbel2026, massoli2026, mitra2026) carry
  2026 publication dates -- flagged by kimi as needing verification they are final
  published versions. In this project's own established timeline (current date
  2026-08-23 throughout this session), 2026 is simply the current year, and these
  citations were independently verified earlier in this project's history (DOIs resolve,
  full text read in `papers_md/`). Not a defect.

## Not acted on

- **[kimi]** Add full bibliography entries for the two PPSD/Pueblo Soberano news sources
  (currently cited inline in prose, not in `references.bib`). Considered and declined:
  the manuscript's own established convention for non-scholarly sources (the GAM decree,
  cited as "Decreto Ejecutivo 38145-..., \emph{La Gaceta} No.~82, 30 April 2014" inline,
  never added to `references.bib`) is inline citation only. Adding bib entries for these
  two specific news sources while the decree remains inline-only would introduce a new
  inconsistency rather than fix one.

---

**Both repos recompiled clean** (`pdflatex`/`bibtex`, 23 pages, 0 errors, 0 undefined
references, all 4 new citations resolve, abstract confirmed at 249/250 words, LaTeX
environments balanced 28/28).
