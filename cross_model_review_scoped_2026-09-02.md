---
type: cross-model-review
scope: targeted -- material added 2026-09-02 only (Abstract, GAM lambda_soc-scan paragraph + fig:gam-lambda, the whole Conclusion, the in-sample/spatial-CV Limitations item, supplementary sec:supp-gam-detail + tab:gam-lambda, supplementary sec:supp-spatialcv + tab:spatialcv, highlights.tex), not a full-paper re-review
draft: manuscript/main.tex, manuscript/supplementary.tex, manuscript/highlights.tex
date: 2026-09-02
referees: [kimi (model id not printed by CLI), glm (glm-4.6), deepseek-reasoner (failed on the single permitted attempt, err_82f5b304, excluded)]
second_pass_verifier: fable-5
verdict: minor revisions (scoped material only) -- one MAJOR wording overclaim in the Abstract/Conclusion paragraph 1, no numerical or reproducibility defect anywhere in the new material
---

# Cross-model review — IsingCR manuscript, scoped round (2026-09-02 additions)

## Why scoped

Since the 2026-08-29 scoped round, the manuscript gained a nine-point $\lambda_{soc}$ scan of the
GAM field (new paragraph, new figure, new supplementary table with an energy decomposition), a
leave-one-province-out spatial cross-validation (new supplementary section, new Limitations item),
a rewritten Abstract, and an entirely new four-paragraph Conclusion built around two synthesis
claims ("no signature of criticality"; "predisposition is largely geography under another name").
This round targets only that material, with the referees explicitly told to read the rest for
context, recompute at least two numbers from the deposited `.npz` files, judge the two synthesis
claims at the strength stated, and check the Abstract (<=250 words) and highlights (<=85 chars).

## Summary assessment

Both referees agree that the new material is numerically clean: kimi recomputed every row of both
new tables, the energy decomposition, the structural ceiling, the paired seed-level $\lambda^*$
gap, the own-margin comparison curve, the size-weighted held-out mean, and the pinned commit's
contents, and found no discrepancy anywhere; GLM's smaller recomputation (seven quantities) agreed.
The orchestrator's own independent recomputation (before reading either transcript) agrees with
both. Where the referees diverge is entirely in the synthesis layer, and they diverge in opposite
directions on the two headline claims: kimi rated "no signature of criticality" a MAJOR overclaim
and "largely geography" acceptably hedged, while GLM rated criticality "SUPPORTED at the strength
stated" and "largely geography" a MAJOR overgeneralization. The Fable-5 second pass sided with GLM
on criticality (partially refuting kimi's physics objection with a specific, checkable reason: the
counterfactual sweep is a hundredfold-range scan of the fitted finite-field system, not a
single-point test) and with kimi on the geography claim (the Conclusion's paragraph-4 version is
hedged; the Abstract's and Conclusion-paragraph-1's are not). One MAJOR survives: the Abstract's
closing sentence, repeated nearly verbatim as Conclusion paragraph 1, states a 2026-only,
in-sample, three-candidate comparison as a general, mechanism-flavored fact, and its "not how
developed it is" clause is in direct tension with the paper's own population-confound paragraph
in the same section. DeepSeek failed on the single attempt permitted with the same opaque server
error as in the two previous rounds; a probable cause is noted in the footer.

## Major points

1. **[R-Kimi; R-GLM raised the Conclusion-paragraph-4 variant; Fable-5: NOT REFUTED]** The
   Abstract's closing sentence -- "At coarse resolution the vote map is a coupling phenomenon; at
   fine resolution a field phenomenon; and the field that does the work is geographic -- where a
   unit sits relative to the capital, not how developed it is or how it voted before." -- and
   Conclusion paragraph 1's near-identical "The take-home message of this paper can be stated in
   one sentence..." are unqualified, general, present-tense claims, but the supporting GAM result
   is (a) 2026-only (the body says so: "2022 does not replicate this... 2026-specific rather than
   a general property"; canton level is null in all three years), (b) in-sample (the paper's own
   new leave-one-province-out check fails significantly in Alajuela, $-19.0$ points, $p<0.001$),
   and (c) a comparison among exactly three tested candidates, one geographic and two not. The
   Abstract's only scope qualifier ("2026 only", line 40) is attached to the $+13.4$ number, not
   to the closing sentence, and the Abstract opens by naming three elections. Worse, "not how
   developed it is" is a mechanism claim the paper's own GAM section explicitly declines to make:
   "Part of what the GAM field captures is genuinely 'more urban/populous,' not purely 'closer
   to the capital' in isolation, so the GAM result should not be read as a clean
   geographic-distance effect on its own" (main.tex lines 940--943). Conclusion paragraph 4
   already has the right calibration ("suggests... at least here... claims a single-country,
   largely single-election study can raise but not settle"); the Abstract and paragraph 1 do not.
   *Proposed fix:* in both places, scope and frame comparatively, e.g. "...and, in 2026 and among
   the candidates tested, the field that does the work is geographic -- capital-region membership
   -- rather than a development index or prior vote"; if "not how developed it is" is kept, it
   must read as the MIDEPLAN comparison outcome, not as a statement that development/urbanization
   plays no role. Watch the Abstract word count while doing this (see Minor point 8).

## Minor points

1. **[R-Kimi, downgraded from MAJOR on second-pass verification; R-GLM explicitly disagreed]**
   "Finite-size scaling, a counterfactual temperature sweep, and cascade tests show no signature
   of criticality: a field-pinned equilibrium that absorbs local perturbations." (Abstract) and
   highlight 5 "No signature of criticality: a field-pinned equilibrium that absorbs local shocks"
   both drop the hedges the Conclusion itself carries ("within the scanned range"; "It holds
   within the scanned temperature range, the two real system sizes..., and 2026 specifically"),
   and "Finite-size scaling... show" gives no hint that the supplement concedes it is "a two-size
   check rather than a full convergence study" on "two genuinely different real graphs -- not
   rescalings of one topology". Kimi's stronger physics objection (that the Binder check at
   $h=0$ is a different system from the fitted one and that the other two tests are single-point)
   was partially refuted: the counterfactual sweep scans the fitted, finite-field system across
   $T=0.05$--$5.0$ (2.9%--10.9% divergence), the $h=0$ choice is stated and justified (line 658),
   and "no signature of" is already absence-of-evidence wording. *Fix:* add "within the scanned
   range, for 2026" to the Abstract sentence; reword highlight 5 to carry the scope within 85
   characters, e.g. "No signature of criticality in the scanned range: a field-pinned 2026
   equilibrium" (81 chars).
2. **[R-Kimi]** Conclusion paragraph 2 pools "three results this paper obtains separately and
   that are, on inspection, the same result" -- but the Binder cumulant was run on the $h=0$
   system, not on "the 2026 map, as this model represents it" (which has a nonzero field on every
   node). *Fix:* one clause distinguishing the zero-field crossing search (a symmetric-reference
   check on the coupling network) from the two field-pinned stability tests.
3. **[R-Kimi; verified]** "accuracy is pinned at that structural ceiling and the coupling term
   can no longer correct the remaining $19\%$; more weight buys nothing because the field has
   nothing more to give" (sec:gam) is slightly stronger than the data: the peak $81.47\%\pm0.20\%$
   sits $0.53$ points above the $80.9\%$ ceiling, and from the saved spins $0.88\%$ / $0.60\%$ /
   $0.03\%$ of nodes are correct *against* the field's sign at $\lambda_{soc}=1$ / $1.5$ / $8$ --
   the coupling is still correcting a handful of nodes at $\lambda^*$ and only stops at
   $\lambda_{soc}=8$. *Fix:* "pinned just above the ceiling, with the coupling term's residual
   correction shrinking from about $0.6$ points at $\lambda^*$ toward zero".
4. **[R-Kimi]** Abstract "it peaks at its own structural ceiling" and highlight 4 "the field peaks
   at its own ceiling": the peak is measurably above the ceiling and decays onto it
   ($80.97\%$ at $\lambda_{soc}=8$). *Fix:* "peaks just above its structural ceiling and settles
   onto it" (highlight 4 alternative within 85 chars: "GAM peaks just above its own ceiling;
   optimal field-to-coupling ratio $\approx1.5$", 74 chars).
5. **[R-Kimi]** Conclusion paragraph 1 "carrying $37\%$ of the fitted equilibrium's energy there,
   and no more, because it saturates at its own structural ceiling": as written "and no more"
   attaches to the energy share, which is not bounded at 37% (it reaches 0.76 at
   $\lambda_{soc}=8$, tab:gam-lambda); what is bounded is the accuracy contribution. *Fix:* make
   the bounded quantity explicit ("...at its optimum -- and buying no further accuracy beyond it,
   because...").
6. **[R-Kimi; verified in `run_gam_lambda_scan.py` line 117]** tab:gam-lambda's caption never
   states the McNemar null (it is the majority-class baseline), and a vs-baseline $p$ is
   uninformative on the plateau -- every row from $\lambda_{soc}=0.75$ up shows $p\sim10^{-6}$--$10^{-7}$,
   including $\lambda_{soc}=8$ where accuracy has declined from the peak, so the column cannot
   speak to the table's own peak-vs-plateau claim. *Fix:* state the null in the caption; if a
   significance handle on the shallow peak is wanted, report the paired seed-level difference
   $\lambda^*$ vs. $\lambda_{soc}=1$ (kimi computed it: mean $+0.397$ pp, std of difference
   $0.478$ pp, 13/16 seeds improved -- which also confirms the supplement's "about one
   seed-to-seed standard deviation" wording).
7. **[R-Kimi; verified]** tab:spatialcv's "vs. baseline" column does not reproduce from the
   rounded entries as printed: Heredia $83.0-72.3=10.7$ (printed $+10.6$; true $10.64$),
   Alajuela $90.5-71.6=18.9$ (printed $-19.0$; true $18.97$). *Fix:* print baseline and held-out
   accuracy to two decimals, or compute the gap column from the rounded entries.
8. **[R-Kimi, R-GLM, orchestrator]** Abstract length: 250 words if the free-standing em dash is
   not counted (kimi), 251 if it is (GLM; orchestrator, which is what MS Word would report) --
   zero or negative margin against a 250-word limit. *Fix:* trim two or three words, remembering
   that the Major-point fix above adds words. Highlights: 81 / 82 / 76 / 72 / 81 characters,
   all within 85 (three independent counts agree; GLM's 77 for bullet 4 came from rendering
   `\approx` as the word "approx").
9. **[R-GLM, downgraded from MAJOR in Step 3]** Conclusion paragraph 4, "which suggests that
   what such models call 'predisposition' is, at least here, largely geography under another
   name": the sentence is hedged ("suggests", "at least here", next sentence "can raise but not
   settle") so it is not an overclaim at the stated strength, but its evidence base is one
   geographic candidate beating two non-geographic ones in one election, and "largely" is
   undefined. *Fix:* make the base explicit ("the one geographic candidate tested carried more
   of the field term than the two non-geographic ones") and consider dropping "largely".
10. **[R-Kimi]** "every point from $\lambda_{soc}=1$ to $8$ lies within $0.5$ points of the peak"
    is true by $0.001$ pp (the $\lambda_{soc}=8$ point is $0.499$ pp below the peak); rounding
    either number differently flips it. *Fix:* "within half a point" or quote the $0.499$.
11. **[Orchestrator, not raised by either referee]** tab:spatialcv reports per-province
    *medians* across 16 seeds; the deposited `gam_spatial_cv_2026.npz` shows that one seed
    (index 13) lands in a flipped-periphery configuration -- Limón $0.0\%$, Puntarenas $59.3\%$,
    Heredia $72.3\%$ held-out on that seed, against $100\%$ / $98.3\%$ / $83$--$85\%$ on the
    other fifteen. The text's "the model simply ties them and the fold tests nothing" is true at
    the median but not seed-by-seed, and this is exactly the metastability the paper's own
    multistability check documents. *Fix:* one sentence noting that 1 of 16 seeds equilibrates
    to the periphery-flipped basin (so the median, not the mean, is the right summary), or add
    a seed-range column.

## Where the models disagreed

- **"No signature of criticality."** Kimi: MAJOR overclaim (the Binder test is on a different,
  $h=0$ system; a nonzero field forbids a sharp transition by construction; the other two tests
  are single-point). GLM: "SUPPORTED at the strength stated", citing the 5-crossing Binder
  result, the 2.9%--10.9% counterfactual range, the 8/10 cascade nulls, and the absence of
  interior susceptibility peaks. Fable-5's second pass found kimi factually wrong on the
  single-point claim (the counterfactual sweep is 13 temperatures over a hundredfold range of
  the fitted system) and judged the $h=0$ choice deliberate and complementary rather than a
  category error, leaving only the hedge-stripping residual -- recorded as Minor point 1.
  The orchestrator concurs after re-reading lines 1038--1046 directly.
- **"Largely geography under another name."** Kimi: acceptably hedged in Conclusion paragraph
  4, overclaimed only in the Abstract. GLM: MAJOR overgeneralization in paragraph 4 itself,
  from one geographic vs. two non-geographic candidates. The orchestrator and Fable-5 side with
  kimi: paragraph 4 carries three explicit hedges, the Abstract and paragraph 1 carry none;
  GLM's base-rate point (one geographic candidate) is real and is kept as Minor point 9.
- **Abstract word count.** 250 (kimi) vs. 251 (GLM, orchestrator), the difference being whether
  the free-standing em dash counts; the fix is the same either way.
- **Spatial-CV framing.** GLM alone called the supplementary summary a MAJOR minimization of a
  "catastrophic" failure; kimi called the Limitations item "candid and accurate about what the
  new cross-validation does and does not test (including the Alajuela failure and the
  no-per-fold-$T$ caveat)". Dropped as MAJOR in Step 3 (see footer).

## What was checked and found sound

- **Every number in tab:gam-lambda** (nine rows: best alignment, std, $T^*$, McNemar median $p$,
  $|E_J|$, $|E_h|$, field share, follows-field) reproduced from `gam_lambda_scan_2026_lam{0..8}.npz`
  and the rebuilt 2026 graph/field, independently by kimi, GLM (partial), and the orchestrator.
  The $\lambda_{soc}=1$ row reproduces the headline `gam_field_2026.npz` run exactly, as the
  supplement claims.
- **Every number in tab:spatialcv** (seven rows) and the $81.0\%$ size-weighted mean (exactly
  $395.5/488=81.045\%$), the $81.05\%$ in-sample sanity check, and the $T=1.008$ fixed value.
- **Derived claims in the new GAM paragraph:** $\lambda^*=1.5$; $+0.397\to+0.4$ pp over
  $\lambda_{soc}=1$; $+13.83\to+13.8$ at $\lambda^*$; field share $0.366\to37\%$ / $63\%$;
  follows-field $99.3\%$ at $\lambda^*$; structural ceiling $395/488=80.94\%$; mean nonzero
  $J_{ij}=0.9995$ ("mean $J_{ij}=1$ by construction"); the own-margin curve's monotonic
  $67.64\to92.70\%$ climb from `scan_3d_polext_pol{0..8}_soc0.npz`; the $T^*$ pattern
  ($1.65\to0.85$ on the rising flank; $0.53$--$2.29$ for $\lambda_{soc}\ge3$).
- **The figure** `gam_lambda_scan.png` matches the data (red peak at 1.5 with error bars, gray
  monotonic curve without, both ceiling lines, geography-only baseline, $\lambda^*$ marker).
- **Conclusion cross-references to the body:** $2.9\%$/$10.9\%$ counterfactual range, "8 of 10"
  cascade nulls with the two propagating cases nearest-neighbor only, "one in five distritos
  changed sides" ($79.1\%$ sign agreement), $+1.2$ vs. $+8.7$--$11.6$, $+13.4$ / $p=0.0005$,
  canton-level GAM "not significant" (0 of 8 seed-pairs, sec:polarization-trend), MIDEPLAN
  "borderline, 2026-only", Alajuela's central canton "14 distritos with a $93\%$ in-sample
  error rate" ($93.3\%$, sec:supp-gam-boundary), and "four provinces whose baselines already
  exceed $80\%$" (Cartago $80.8\%$).
- **Highlights** all within 85 characters (81/82/76/72/81).
- **Provenance:** the pinned commit `d7ba3fa` is the current HEAD and contains
  `run_gam_lambda_scan.py`, `plot_gam_lambda_scan.py`, `run_gam_spatial_cv.py`, and the nine
  scan result files; nothing in the new material is unreproducible at the pinned commit.

## Second-pass verification (Fable 5)

Two MAJOR findings survived the orchestrator's Step 3 and were handed to a Fable-5 subagent
instructed to refute them against the actual manuscript text. **Finding 1 (Abstract/Conclusion-1
overclaim): not refuted**, with the additional observation that Conclusion paragraph 1 repeats the
Abstract's unhedged sentence and must be fixed alongside it, and that the Alajuela failure is
supporting evidence for adding "in-sample" rather than the core of the finding. **Finding 2
("no signature of criticality"): partially refuted** on two specific, checkable grounds (the
counterfactual sweep is a 13-temperature scan of the fitted finite-field system, main.tex lines
1042--1045, not a single-point test; the $h=0$ Binder choice is stated and justified at line 658
and is complementary, not a category error); the orchestrator re-read both passages and agrees.
The residual (hedges present in the Conclusion but stripped from the Abstract and highlight 5) is
real and is kept as Minor point 1.

## Dropped / not applied (with reasoning)

- **[R-GLM, MAJOR -- dropped in Step 3]** "This characterization minimizes a major out-of-sample
  failure... Do not lead with the size-weighted aggregate that masks this failure pattern"
  (sec:supp-spatialcv). The quoted passage itself says "that aggregate is misleading on its own",
  then enumerates precisely the pattern GLM asks to be reported (four uninformative ties, two
  non-significant gains, one "systematic, significant failure, not noise"), and the Limitations
  item repeats all of it in the main text. The finding asks for content that is already there;
  the residual disagreement ("partial, not uniform" vs. "poor") is a matter of adjectives.
- **[R-Kimi, MAJOR -- dropped as MAJOR on second-pass verification, retained as Minor point 1]**
  See "Second-pass verification" above. This is an orchestrator-level correction: the Step 3
  pass accepted kimi's "single fitted point" characterization of the counterfactual sweep
  without checking it against lines 1038--1046.
- **[R-GLM, MAJOR -- downgraded in Step 3, retained as Minor point 9]** Conclusion paragraph 4
  "largely geography under another name": the problem statement ("concluding that predisposition
  is 'largely geography' is premature") misreads a sentence that says "suggests", "at least
  here", and is immediately followed by "claims a single-country, largely single-election study
  can raise but not settle".
- **[R-GLM, MINOR -- not applied]** Change "$37\%$" to "$36.6\%$" in sec:gam. The paper rounds
  the companion "$63\%$" the same way and reports the three-decimal value ($0.366$) in
  tab:gam-lambda; kimi and the orchestrator both reproduced $0.366$ and accepted $37\%$.

---

*Referee transcripts:* `referee_kimi_scoped_2026-09-02.md` (123 lines; kimi again recomputed
every checkable quantity from the deposited `.npz` files and the rebuilt graph before writing a
single finding, including a paired seed-level test of the $\lambda^*$ gap the manuscript does not
itself report), `referee_glm_scoped_2026-09-02.md` (107 lines).
`referee_deepseek_scoped_2026-09-02.md` contains only the single permitted attempt's server error
(`err_82f5b304`), the fourth consecutive identical failure across three rounds. Probable cause,
for the author: `opencode models` on this machine lists `deepseek/deepseek-v4-flash`,
`deepseek/deepseek-v4-flash-vision-exp`, and `deepseek/deepseek-v4-pro` but no
`deepseek/deepseek-reasoner`; the model id the review skill hard-codes appears to no longer exist
on the provider, so future rounds should try `deepseek/deepseek-v4-pro` instead of retrying the
same id.
