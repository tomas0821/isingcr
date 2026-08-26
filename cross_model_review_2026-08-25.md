---
type: cross-model-review
draft: manuscript/main.tex
date: 2026-08-25
referees: [kimi (model id not printed by CLI), antigravity (Gemini 3.7 Flash High), deepseek-reasoner (failed both attempts, excluded), codex (gpt-5.6-terra), qwen (model id not printed by CLI), glm (glm-4.6)]
second_pass_verifier: fable-5
verdict: major revisions
---

# Cross-model review — IsingCR manuscript, round 3 (6-model panel)

## Summary assessment

Six independent model families reviewed the manuscript's then-current state (post round-2
fixes) against the same adversarial brief. DeepSeek failed twice with an identical opaque
server error (`UnknownError`, refs `err_02982697`/`err_722fe2d4`) and is excluded from this
round rather than silently dropped — see `referee_deepseek_2026-08-25.md` for the raw error.
The remaining five (kimi, agy, codex, qwen, glm) all independently converged on the same
handful of real defects — most notably a factual error about Korbel et al. (2026)'s dataset
timespan ("a century" vs. the correct "four decades, 1980-2020") and an overclaim about what
Korbel's methodology can and cannot do relative to this paper's own validation approach — while
diverging sharply on how much weight to put on the manuscript's own extensive, pre-existing
self-disclosure. kimi and agy did the most careful, individually-checkable work and surfaced
several genuine, previously-unflagged issues (an undefined field formula, a mislabeled
best-fit weight, an unstated Hamiltonian in the 2018 energy diagnostic, a missing citation to
the auto-logistic/Markov-random-field literature, a finite-size-scaling self-similarity
caveat). codex and qwen, by contrast, mostly re-flagged limitations the manuscript already
states in its own words — quoting the manuscript's own hedges back as if they were undisclosed
defects — and both effectively argue for a different research paradigm entirely (pre-registered
or held-out-validated confirmatory statistics) rather than identifying inconsistencies in the
paper as written; codex's "reject-and-rework" recommendation should be read with that in mind.
glm repeated several claims already refuted in the prior round's report (the p=0.0005-vs-p≈0
"inconsistency," the SD-overlap "invalid test" complaint, a Korbel "spatial structure"
mischaracterization, a padrón "not mentioned" claim) verbatim or near-verbatim; all four were
re-verified and refuted again here, consistent with round 2. A Fable-5 second pass on the ten
most consequential fixes applied this round caught one real error the orchestrator introduced
while fixing kimi's λ_pol=2 finding (a false claim that the λ_pol grid was "used in" the
ablation sections) — that fix has been corrected. Net: several real, previously-missed defects
fixed; a larger number of already-adequately-disclosed items correctly left alone; one
orchestrator-introduced error caught and repaired by the second-pass check.

## Major points

1. **[R-Kimi]** Manuscript states Korbel et al. (2026) calibrated on "a century of U.S. House
   elections," twice — Korbel's own paper says 1980-2020 (four decades) — "Korbel et al.\
   \citep{korbel2026} fit a double-random-field Ising-equivalent model to a century of U.S.
   House elections" — *Fix applied:* both occurrences corrected to "four decades of U.S. House
   elections (1980--2020)."
2. **[R-Kimi]** The paper's novelty claim said Korbel's closed-form mean-field model "does not
   pose" a coupling-vs-field decomposition — but Korbel's own paper runs exactly this kind of
   ablation (McNemar test, optimal homophily-active model vs. field-only null at T=1), and this
   manuscript's own McNemar methodology explicitly says "following the validation approach used
   in \citep{korbel2026}" — *Fix applied:* reworded to concede Korbel poses an analogous
   non-spatial decomposition, narrowing this paper's actual novel claim to isolating a literal,
   real geographic network topology's contribution specifically.
3. **[R-Kimi]** $\lambda_{pol}=2$ was called "the own-margin field's best-fit weight" in the
   Model section, while a separate part of the paper (sec:mideplan) shows alignment climbing
   monotonically well past $\lambda_{pol}=2$ on a wider $[0,8]$ grid, making "best-fit weight"
   an ill-defined, misleading label — *Fix applied:* verified via `data/processed/scan_3d_pol{0-4}_soc0.npz`
   that $\lambda_{pol}=2$ genuinely is the best point of a separate, dedicated $[0,2]$
   $\lambda_{pol}$-scan of the margin field (monotonic 67.64%→82.36%, $T=0.848$ matches
   exactly), then reworded to call it that grid's best-performing point, not a global optimum,
   with a forward reference to sec:mideplan's wider-grid result. *(A first version of this fix
   incorrectly attributed the $[0,2]$ grid to the ablation sections; corrected after Fable-5's
   second pass caught the false cross-reference — see footer.)*
4. **[R-Kimi]** The 2018 energy-diagnostic section never states which Hamiltonian ($h=0$ or
   $h=$margin) the reported per-canton energy gaps are computed under, and justifies the
   trivial-state-has-lower-energy observation with a non-sequitur ("expected, since it is the
   null the model is scored against") — *Fix applied:* confirmed via
   `scripts/investigate_2018_anomaly.py` (`h_col="margin"`) that $h=$margin is used; the text
   now states this explicitly and replaces the non-sequitur with the actual physical mechanism
   (a uniform configuration always zeroes the coupling term's domain-wall cost, and that saving
   outweighs the field term's pull toward the true, spatially uneven pattern).
5. **[R-Kimi]** The Conclusion's finding (4) described the distrito-level own-margin ablation
   result as revealing "a real, reproducible... contribution of individual political
   predisposition" without noting that field is, by the paper's own admission elsewhere, 99.8%
   sign-identical to the label it is scored against — exactly the circularity concern the
   paper's entire second contribution exists to escape — *Fix applied:* added a caveat clause
   noting the near-tautology and pointing to finding (5) (the non-circular GAM/MIDEPLAN/political
   fields) as the actual non-circular confirmation.
6. **[R-Antigravity]** The field value $h_i$ ("normalized vote margin") is never given an exact
   formula, blocking numerical replication — *Fix applied:* confirmed the exact formula in
   `src/isingcr/ingestion/binarize.py` (`margin = (votes_a - votes_b)/(votes_a + votes_b)`) and
   added it inline: $h_i = (V_{i,A}-V_{i,B})/(V_{i,A}+V_{i,B}) \in [-1,1]$.
7. **[R-Antigravity]** The Introduction's novelty claim ("comparatively rare -- absent from all
   of the above -- is a model whose coupling network is... the literal geographic adjacency
   structure of a real country") ignores the decades-old spatial-statistics auto-logistic/Markov
   random field tradition (Besag 1974) that does exactly this for other kinds of spatial binary
   data — *Fix applied:* added `\citep{besag1974}` (verified citation details: JRSS-B 36(2),
   192-225, 1974) and a sentence acknowledging this older tradition while correctly narrowing
   "comparatively rare" to the electoral-sociophysics literature specifically surveyed in that
   paragraph.
8. **[R-Antigravity]** Standard finite-size-scaling theory assumes the compared systems are the
   same lattice/network type at different linear sizes (same universality class); Costa Rica's
   canton ($N=84$) and distrito ($N=488$) networks are two genuinely different real graphs with
   different degree distributions, not rescalings of one topology — *Fix applied:* added a
   caveat in sec:fss scoping the analysis as "a real-network check in the spirit of finite-size
   scaling rather than a textbook-conditions test of it."
9. **[R-Antigravity / R-Codex]** The paper claimed none of the four model-native diagnostics
   (multistability, domain-wall, counterfactual sweep, cascade test) have any regression
   analog — but a spatial-lag model's impact-multiplier matrix $(I-\rho W)^{-1}$ formally
   computes exactly the kind of localized shock propagation the cascade test performs — *Fix
   applied:* narrowed the claim in both the Discussion and Conclusion to concede this
   specifically for the cascade test (conceding the linear analog exists, noting what the
   stochastic dynamics adds beyond it) while retaining "no analog" for multistability and the
   counterfactual sweep, which genuinely have none.
10. **[R-Codex]** The code-availability statement points only to a mutable GitHub URL with no
    fixed reference point for a paper with "extensive post hoc corrections" — *Fix applied:*
    added the specific commit hash (`2b2beb4`) the reported results were produced at, plus a
    note that a DOI-archived release will be created at publication (not yet claiming a DOI
    exists).
11. **[R-Kimi, several MINOR]** ~13 additional MINOR fixes applied: grid-spacing explanation
    corrected (kimi's arithmetic showed the original "how far into the high-$T$ range"
    explanation was wrong since both best-$T$ values are interior points); Moran's $I$ values
    disambiguated between the binarized-spin and continuous-margin fields (previously the same
    numbers were presented as covering both); the historical-comparison table/text now states
    which field arm ($h=$margin) it reports; abstract/body/conclusion's rounded "+9 to +12
    points" corrected to the exact "+8.7 to +11.6" everywhere; "pp" vs "%" unified in the
    robustness table; GAM's "$p\approx0$" replaced with the actual value ($4.4\times10^{-7}$,
    $1.4\times10^{-5}$ after correction); FSS caption/text "confirming proper equilibration"
    softened to "consistent with"; the GAM 31-canton-list "applies exactly" overclaim corrected
    to acknowledge residual canton-level imprecision; the 2022 GAM check now states explicitly
    it uses 2026's best-fit $T$, not 2022's own; Conclusion finding (5)'s "identical
    scale-dependence" softened to distinguish the significance-pattern echo from the differing
    canton-level point estimates; the 2018 relaxation's exactly-zero cross-seed variance is now
    explained (unconditionally-unstable cantons flip regardless of seed/order; 2026's nonzero
    spread reflects order-dependent cascades); seed independence justified via NumPy's
    PCG64-based `Generator`; two cited political-science works' "exactly this finer scale" claim
    corrected to "canton scale and below," since both are canton-level studies; abstract's
    "three" antecedent disambiguated.

## Minor points (selection; not exhaustive — see per-referee raw transcripts for full lists)

- **[R-Kimi]** GAM's "more robust" framing lacked a within-2026 qualifier given its own 2022
  result is not significant — fixed.
- **[R-Kimi]** The 79.1% majority-class baseline (distrito, winner-vs-runner-up) and the
  separate 79.1% "sign(2022 margin) matches 2026's actual winner" figure are numerically
  identical but independent computations — clarified in-text as a coincidence, not a shared
  quantity.
- **[R-Kimi]** The alternative-binarization robustness check's "+11.6pp, close to the
  coalition-split effect size" framing obscured that geography-only falls *below* the trivial
  baseline under that binarization while the full model barely clears it — both readings now
  stated.
- Several rounding/table nitpicks flagged by glm (Table 4.4's 66.16%/74.85%→8.7pp arithmetic;
  the "robust to 1-sigma but weak McNemar" framing in the historical table) were checked and
  found to be correct as stated, or an already-explicit both-facts-stated design, not errors —
  no change needed.

## Where the models disagreed

kimi and agy did close, verifiable, line-level work and found genuine gaps a careful author
read would also catch (undefined formulas, a mislabeled grid point, an unstated Hamiltonian).
codex and qwen, given the *identical* brief and the *identical* draft, instead re-surfaced the
manuscript's own already-stated hedges (best-of-grid selection, McNemar's independence
violation with a spatial-block alternative already reported, the own-margin field's
near-tautology, binarization not cross-validated) as if they were undisclosed — codex reaching
"reject-and-rework" almost entirely on this basis. This is a real and useful signal about how
differently model families weigh "the paper discloses X as a limitation" against "X is present
at all," not a factual disagreement about the draft's content. glm sits in between: it
independently found one genuinely new item (seed independence not justified) but also repeated,
nearly verbatim, four claims from round 2 that were refuted then and are refuted again here.

## What was checked and found sound

- The paper's existing Bonferroni-on-median-$p$ heuristic and its explicit disclaimer ("a
  conservative screening heuristic rather than a formally derived family-wise-error-rate
  guarantee... which we did not implement") — flagged as MAJOR by agy and codex independently,
  but the manuscript's own text already states precisely what they ask for; no gap to fix.
- The low-temperature susceptibility/specific-heat divergence explanation (agy) — already
  disclosed in the same terms agy's own quote uses.
- The "GAM's double-random-field" characterization of Korbel et al. (agy) — a misreading; the
  manuscript correctly uses "double-random field" as Korbel's own model name, then separately
  and accurately describes it as a single bimodal field, contrasting with this paper's two
  independently-sourced fields.
- The multistability-terminology hedge ("we use `equilibrium' here in the practical sense...")
  — agy and (implicitly) prior rounds both flagged the term "multistability" itself as
  conflating algorithmic non-convergence with thermodynamic phase coexistence; the manuscript
  already carries an explicit, first-use disclaimer scoping the term operationally. Judged
  adequately hedged; no global rename applied.
- The three-party "coalition" binarization / suggestion to use a $q$-state Potts model instead
  (agy) — already considered and declined in a prior round for the same reasons.
- 9 of the 10 fixes applied this round, independently re-verified by a Fable-5 second pass
  against the actual manuscript text, source code, and cited papers.

## Pipeline notes

- kimi: succeeded on the fourth attempt after two CLI flag errors (`--print` is not a valid
  flag for this Kimi Code CLI version; `-p`/`--prompt` cannot combine with `-y`/`--yolo`) and
  one Bash-tool timeout on a third, foreground attempt; the fourth run, backgrounded with no
  `-y`, completed in ~25-30 minutes. 1123-line report, 4 MAJOR + ~24 MINOR findings.
- agy: succeeded first try with `--dangerously-skip-permissions` (explicit user approval
  obtained beforehand). 148-line report, 16 findings.
- deepseek: failed twice with an identical opaque `UnknownError` server error
  (`err_02982697`, `err_722fe2d4`) via `opencode run --model deepseek/deepseek-reasoner`,
  treated as a genuine service outage and not retried a third time. **Excluded from this
  round** — not silently folded into a five-model panel.
- codex: succeeded via `codex exec -s read-only --skip-git-repo-check`. 2300-line raw output
  (includes one verbatim-duplicated findings block, consistent with prior codex runs); 20
  unique findings after dedup.
- qwen: succeeded via `qwen -p`, no approval flag needed. 71-line report, 8 findings.
- glm: succeeded via `opencode run --model zai/glm-4.6`, no duplication this run. 257-line
  report, 27 findings.

## Second-pass verification (Fable 5)

Ten of this round's confirmed-and-applied MAJOR fixes were independently re-checked by a
Fable-5 subagent instructed to try to refute each one against the actual manuscript text,
source code, data files, and cited papers (not against the orchestrator's own summary).
**9 of 10 survived.** One was refuted on a specific, checkable ground: the fix for kimi's
$\lambda_{pol}=2$ finding (item 3 above) originally claimed the dedicated $[0,2]$
$\lambda_{pol}$-scan grid was "used in Sections~\ref{sec:ablation-canton}--\ref{sec:ablation-distrito}"
— false, and internally contradicted by the manuscript's own text ten lines later, which states
those sections use the unweighted $\lambda=1$ margin-field convention with no $\lambda$ grid at
all. Corrected to attribute the grid accurately (a dedicated scan of the margin field's own
$\lambda_{pol}$ weight, distinct from the unweighted convention used elsewhere) before this
report was finalized. Full second-pass transcript retained in the session log; not saved as a
separate file per the skill's guidance (no fixed output artifact specified beyond this report).

## Dropped / refuted findings (with reasoning)

Findings below were investigated and explicitly **not** applied, with reasoning — logged here
per the skill's rule against silently dropping findings.

- **[R-Antigravity, MAJOR]** Bonferroni-on-median-$p$ "invalid FWER control" — refuted: the
  manuscript's own text already states this exact limitation in the same terms the referee's
  quote uses; there is no undisclosed gap to fix.
- **[R-Antigravity, MAJOR]** Low-$T$ susceptibility/specific-heat divergence "artifact of
  symmetry-broken pure states" — refuted: already disclosed in the manuscript in the same terms
  the referee's own quote uses.
- **[R-Antigravity, MAJOR]** "Korbel et al.'s double-random field" terminology "conflates" an
  analytical random-field distribution with this paper's deterministic two-covariate field —
  refuted: misreading of the sentence's grammar; "double-random field" is used correctly as
  Korbel's own model name, immediately followed by an accurate description of its actual
  (single, bimodal) field structure.
- **[R-Antigravity, MAJOR]** Headline result reported via classification accuracy rather than a
  physical observable (correlation length, etc.) — refuted as a "gap": the manuscript's own
  quoted text already states this is a deliberate, disclosed choice ("an honest description of
  what this specific model and dataset can currently support rather than a limitation to paper
  over"). A fair suggestion for future work; not a text-fix-level defect.
- **[R-Antigravity, MAJOR]** "Multistability" terminology conflates finite-time Markov-chain
  mixing with true thermodynamic phase coexistence — declined: the manuscript already carries
  an explicit, first-use scoping disclaimer for exactly this concern; judged adequately hedged
  rather than requiring a paper-wide rename.
- **[R-Antigravity, MAJOR]** Artificial three-party coalition should be a $q$-state Potts model
  — declined: already considered and declined in a prior round.
- **[R-Antigravity, MINOR]** Canton-level 500-sweep budget not proven sufficient (vs.
  distrito's 20,000) — declined: would require new MC runs, out of scope for a text-fix pass;
  noted for future work.
- **[R-Antigravity, MINOR]** Table 1 omits the geography-only baseline shown in Table 6 —
  declined: would require pulling $h=0$ figures across all three historical elections, a
  nontrivial data-completeness addition rather than a text fix; the table's own caption and
  surrounding text already state what is being compared.
- **[R-Antigravity, MINOR]** Massoli (2026) differentiation sequestered in Limitations rather
  than Introduction — declined as low-value reorganization given the Introduction already cites
  Massoli among related work and the Limitations discussion is explicit and detailed.
- **[R-Codex, most MAJOR findings]** Own-margin field "leaks the label"; best-of-grid selection
  bias; McNemar independence violation; arbitrary spatial-blocking choice; binarization "not
  cross-validated"; GAM proxy imprecision; "most decisive result" overstatement — all declined
  as fixes: every one of these is already extensively and explicitly disclosed in the
  manuscript's own text (in several cases the referee's own quote *is* the manuscript's
  disclosure). codex's suggested fixes mostly amount to "run a different, pre-registered/
  held-out-validated study," which is a legitimate methodological preference but not a
  correctable defect in the paper as written.
- **[R-Codex, MAJOR]** "Confirming the earlier dips were an equilibration artifact" (Binder
  cumulant range argument) — partially addressed via kimi's overlapping finding (softened to
  "consistent with"); codex's stronger request (trace plots, autocorrelation/ESS diagnostics)
  would require new analysis, out of scope for this pass.
- **[R-Codex, MINOR]** Pre-exclusion vs. post-exclusion baseline figure (66.9% vs. 67.0%)
  retained for consistency — refuted as a defect: the manuscript already transparently
  discloses this exact 0.1-percentage-point difference and states it is immaterial to every
  downstream figure; codex's fix (regenerate all figures/tables) is disproportionate to a
  disclosed, immaterial discrepancy.
- **[R-Codex, MINOR]** "Robust to the 1-sigma uncertainty band" language in the historical
  comparison — same refutation as the GLM SD-overlap finding below; the paper states both facts
  (1-sigma comparison and weak McNemar significance) adjacently and explicitly, by design.
- **[R-Qwen, most MAJOR/MINOR findings]** Nearly all restate the manuscript's own already-stated
  hedges (significance sensitivity to test/binarization choice, two-point FSS insufficiency,
  GAM proxy misclassification not quantified) as undisclosed; declined for the same reason as
  the corresponding codex findings above.
- **[R-Qwen, MINOR]** Figure 1 caption's "492 distritos" vs. body text's 488/483 without
  explanation — refuted: the caption explicitly points to Section~\ref{sec:data}, which gives
  the exact exclusion accounting (2 isolated islands + 2 unreconciled name variants for 2026;
  2 isolated + 7 missing results rows for 2022).
- **[R-Qwen, MAJOR]** 2018's GAM-lowers-alignment anomaly is "post-hoc explanation without
  testing alternatives" — declined: the manuscript already hedges this as "plausibly
  connected," not proven; a controlled test (varying MC budget for 2018 specifically) would
  require new computation, out of scope for this pass.
- **[R-GLM]** p=0.0005-vs-p≈0 "inconsistency" — refuted again (same grounds as round 2: two
  clearly distinct, consistently-used statistics, not a reporting error).
- **[R-GLM]** SD-overlap "not a valid statistical test" — refuted again (the manuscript's very
  next sentence, in both this and the historical-comparison sections, explicitly states this is
  a conservative heuristic and reports the actual paired test alongside it).
- **[R-GLM]** Korbel "spatial structure" mischaracterization — refuted again via direct
  re-reading of `papers_md/korbel2026/korbel2026.md` (explicitly a configuration-model, no
  spatial correlation).
- **[R-GLM]** Padrón electoral "not mentioned elsewhere in the paper" — refuted again (present
  in sec:data-population, confirmed by direct grep).
- **[R-GLM]** Table 4.4 arithmetic "doesn't match" (66.16%→74.85%, +8.7pp) — refuted: 74.85 −
  66.16 = 8.69, which correctly rounds to 8.7; no discrepancy.
- **[R-GLM]** GAM's population confound "not actually tested" — refuted as a defect: the
  manuscript explicitly states this is an uncontrolled caveat on mechanism, not significance,
  and does not claim to have controlled for it; nothing to correct.
- **[R-GLM]** Results-section length/structure, title-content mismatch, literature review
  breadth — declined as low-actionability scope/style feedback, consistent with prior rounds.

---

*Not applied this round for reasons of scope (would require new computation, not a text fix):*
codex's request for a spatial-lag/CAR/SAR benchmark comparison; a formal null distribution for
the FSS crossing-count read; a full parameter table with pseudocode for every scan grid and the
`spatial_block_permutation_test_paired` algorithm (raised independently by kimi and codex);
exact enumeration instead of 999 Monte Carlo draws for the 7-block spatial permutation test
(kimi); a systematic literature review of the spatial-statistics MRF/auto-logistic tradition
beyond the single Besag (1974) citation added this round.
