---
type: cross-model-review
draft: manuscript/main.tex
date: 2026-08-22
referees: [antigravity (model id not printed by CLI), deepseek-reasoner (via opencode)]
verdict: minor-to-major revisions
---

# Cross-model review — IsingCR

**kimi was not run.** `kimi-cli` (the binary actually installed under that name; the skill's
`kimi` alias resolves to it) is not authenticated — it requires an interactive OAuth login
(`kimi-cli login`) that cannot be completed headlessly. User was asked and chose to proceed
with a two-model panel (Antigravity, DeepSeek) rather than wait for a manual login. This is a
**two-referee**, not three-referee, review — weighted accordingly below.

## Summary assessment

The two referees diverged sharply in method and in verdict. **R-Antigravity** produced 16
findings and recommended **reject and rework**, but on verification, several of its MAJOR
findings restate limitations the manuscript already discloses explicitly and prominently
(sometimes near-verbatim) in its own Methods/Limitations sections — the median-p Bonferroni
heuristic, best-of-grid selection, classification-accuracy-vs-physical-observable framing, and
the artificial three-party coalition are all already flagged by the paper itself as known,
hedged limitations, not undisclosed flaws. One of its results-consistency findings (the
Abstract's "+9–12pp" vs. the table's "+8.7pp") is a misreading: the Abstract sentence explicitly
describes the range across robustness checks (+8.7 to +11.6pp), not the point estimate alone.

**R-DeepSeek** read the actual simulation code and the project's own `NOVELTY_CHECK.md`, not
just the manuscript text, and this paid off: it surfaced **six findings that are genuinely new**
— not caught by six prior same-model referee rounds this project already ran — three of them
substantive enough to affect how the paper's own claims should be read (an unstated coupling
normalization, an undisclosed break from the paper's own stated Bonferroni-correction policy
that would flip one reported finding's significance if applied, and two citations the project's
own novelty-tracking document already recommended adding but that never made it into the
manuscript text). One of DeepSeek's own findings (the headline p=0.0005 being "impossible" from
a 999-draw test) is independently verifiable as **false** — checked directly against the saved
permutation-test output on disk (below) — a useful reminder that DeepSeek's code-reading did not
make it infallible either.

Net: this is not a "reject and rework" manuscript, but it is not the clean pass the project's own
six same-model referee rounds converged toward either. Cross-model review earned its cost here —
every one of the confirmed novel findings below came from a lens (reading the actual `.py`
source and the project's own novelty-check file, not just the LaTeX) that six rounds of
same-model review never applied.

## Major points

1. **[R-DeepSeek, R-Antigravity — independently, same finding]** The Hamiltonian's coupling
   $J_{ij}$ is described in the text only as "set by shared border length," with no stated
   normalization — "problem: The manuscript never states the normalization of the border-length
   weights — the code divides each shared border length by the mean over edges (mean weight
   1.0) — so the coupling matrix, the temperature scale... are not reproducible from the text."
   Verified directly against `src/isingcr/ingestion/shapefile_adjacency.py:36-39`: `weight_by:
   "uniform" (all edges weight 1.0) or "border_length" (edge weight proportional to the
   shared-border length, normalized so the mean weight is 1.0...)`. The manuscript text (line
   381) omits this normalization entirely. *Fix:* add one sentence to Section 3.2 stating
   $J_{ij} = l_{ij}/\bar{l}$ (shared border length normalized to mean weight 1.0).

2. **[R-DeepSeek]** The Methods section states a blanket policy — "We report a simple,
   conservative Bonferroni correction alongside every raw $p$-value below" (line 461) — but this
   is not honored for the MIDEPLAN section's headline McNemar $p=0.015$ (line 1072) or the GAM
   section's McNemar "$p\approx0$" (line 1199): neither shows a corrected value, and neither is
   flagged as a deliberate exception the way Table `tab:robustness` explicitly is ("McNemar $p$
   is reported as-is, uncorrected, for comparability across rows," line 952). Applying the
   stated $\times32$ correction to MIDEPLAN's $p=0.015$ gives $p=0.48$ — not significant, versus
   the "borderline" reading the current text implies. *Fix:* either show the corrected value
   alongside every such raw $p$ per the stated policy, or add an explicit, disclosed exception
   matching the `tab:robustness` pattern.

3. **[R-DeepSeek]** The Abstract and Conclusion both say "two flagship cases cannot be fully
   separated from a GAM-proxy labeling artifact" (lines 49, 1678), but the Limitations section
   they point to actually names **three**: "the multistability check's two flagship
   cross-year-consistent fault-line distritos... and the cascade test's single largest
   propagating case... Orosi" (lines 1599-1605) — Tabarcia, Monterrey, and Orosi. Verified by
   direct line search; this is a genuine undercount, and traces to a prior fix round (this
   session's own round-5 pass) that added the "two flagship cases" hedge without checking how
   many the Limitations section it cites actually enumerates. *Fix:* change to "three flagship
   cases" in both the Abstract and Conclusion, or clarify the count is two-from-multistability
   plus one-from-cascade if that distinction matters.

4. **[R-DeepSeek]** Godoy-Lorite & Jones (arXiv:2003.07146, 2020) — a spin-based behavioral
   model with external fields, explicit "social temperature" language, and a network-vs-field
   decomposition, fit to real UK election outcomes — is never cited in the manuscript text,
   despite the Introduction's claim that this kind of decomposition is "absent from all of the
   above." Verified: zero occurrences of "godoylorite" or "social temperature" (as a citation
   context) in `main.tex` or `references.bib`. This is not a fresh discovery — the project's own
   `NOVELTY_CHECK.md` §2b already flagged it in nearly identical terms: "close enough on
   terminology that a Physica A referee could ask about it — worth a short differentiating
   mention if reviewer feedback raises it" — but that recommended mention was never added to the
   manuscript. *Fix:* add the one differentiating sentence `NOVELTY_CHECK.md` already drafted the
   case for (inferred Blau-space network vs. literal geographic adjacency; election-type
   comparison vs. spatial-resolution comparison).

5. **[R-DeepSeek]** The paper's central "geography-vs-predisposition reverses under spatial
   aggregation" finding is presented without engaging the modifiable-areal-unit-problem (MAUP)
   literature in political geography, where scale-sensitivity of exactly this kind is a
   well-documented phenomenon (e.g. Russo & Beauguitte 2014, "Aggregation level matters:
   evidence from French electoral data"). Verified: zero occurrences of "MAUP," "modifiable
   areal," or "Russo" in the manuscript. Again already identified as a positioning reference in
   the project's own `NOVELTY_CHECK.md` §2b but never added to the text. *Fix:* one sentence in
   the Discussion positioning the paper's contribution as a physics-framed confirmation and
   real-network instantiation of a known political-geography effect, not a new empirical
   discovery of scale-sensitivity itself.

6. **[R-DeepSeek]** GAM is evaluated at a single fixed $\lambda_{soc}=1$ with no $\lambda$-scan
   (matching the paper's original own-margin-field convention), while MIDEPLAN is evaluated at
   its own scanned peak ($\lambda_{soc}=1.5$ of a $[0,2]$ scan) before the two are compared and
   GAM is declared "the strongest field tested in this paper." Verified: `main.tex` lines
   1069-1072 (MIDEPLAN, scanned) vs. 1196-1197 (GAM, fixed $\lambda=1$, no scan) — confirmed
   asymmetric. This does not overturn the ranking (GAM's un-optimized 81.07% already exceeds
   MIDEPLAN's optimized 74.42% peak by a wide margin), but the comparison is not fully
   controlled and this is not disclosed anywhere. *Fix:* one sentence noting GAM was evaluated
   unweighted (matching the established single-field convention) rather than $\lambda$-optimized,
   and that even so it exceeds MIDEPLAN's own optimized peak.

7. **[R-DeepSeek]** No selection-aware correction is applied or disclosed for having tested
   three independent candidate fields (MIDEPLAN, the non-circular political field, GAM) and
   reporting only the winner's (GAM's) $p=0.0005$ as "the most decisive result of any field
   tested in this paper" — a classic winner's-curse setup. This would not change the qualitative
   conclusion (even a 3× correction leaves $p\approx0.0015$), but it is an undisclosed gap in an
   otherwise unusually multiple-testing-conscious manuscript. *Fix:* one sentence acknowledging
   the field-selection multiplicity and noting the headline result's robustness to a
   conservative correction for it.

## Minor points

- **[R-DeepSeek]** "weakly significant in its own right (McNemar median $p=0.180$, only 4 of 16
  seeds individually significant)" (line 870) is confusing: $p=0.180$ is not significant by any
  conventional threshold, so "weakly significant" reads as self-contradictory alongside the same
  sentence's "statistically indistinguishable from... the baseline." The underlying numbers are
  correct — this is a wording defect, not an analytical one. *Fix:* reword to "not significant in
  its own right."
- **[R-DeepSeek]** The geography-only baseline's best-fit $T$ also differs between the two
  temperature grids (2.83 in Table `tab:robustness` vs. 2.605 in the MIDEPLAN section) — the
  manuscript already reconciles the *accuracy* discrepancy this causes (66.2% vs. 67.64%) but
  does not mention the parallel $T$ discrepancy. Verified at lines 1008 and 1052. *Fix:* one
  clause noting best-$T$ is grid-dependent too.
- **[R-DeepSeek]** `references.bib`'s `cascantematamoros2006` entry has `year = {2006}` but DOI
  `10.35242/rde_2019_28_11`, whose suffix (2019, issue 28) and the article's own title range
  ("1953-2016") both indicate a ~2019 publication. Verified directly in `references.bib`. *Fix:*
  correct the year field (and check the citation key/year elsewhere in the text if it's used for
  chronological framing).
- **[R-DeepSeek, R-Antigravity — independently, same finding]** Figure 4's caption and the
  historical-comparison table report $N=81/82/84$ cantons for 2018/2022/2026 respectively, and
  the caption points to Section 2 ("see Section~\ref{sec:data}") for why some cantons have no
  matching result row — but Section 2 never actually explains the count change (new cantons were
  created between cycles). Verified: no explanation found anywhere in the Data section. *Fix:*
  one sentence in Section 2.1 noting the canton count grew across cycles due to administrative
  creation of new cantons.
- **[R-DeepSeek]** No URLs, release versions, or access dates are given for the TSE result ZIPs,
  the HDX boundary release, or the MIDEPLAN IDS tables, and the two Costa Rican news sources
  supporting the PPSD/Pueblo Soberano claim are cited inline with no formal reference entry.
  *Fix:* low-priority; add access dates/versions if the journal's own guide requires them, and
  consider promoting the two news citations to `references.bib` entries for consistency with
  every other source in the paper.

## Where the models disagreed

The clearest disagreement is verdict severity, not fact. R-Antigravity's "reject and rework" and
R-DeepSeek's "major revisions" were built from almost entirely non-overlapping evidence:
Antigravity never opened the source code or the novelty-tracking document and built its case
from a single read of the LaTeX, treating several of the paper's own disclosed limitations as if
they were undisclosed; DeepSeek explicitly cross-referenced the codebase and `NOVELTY_CHECK.md`
and, on its own account, "could not find a single arithmetic mismatch across the four headline
findings" — a materially more charitable starting point than Antigravity's, arrived at through
more work, not less scrutiny. On the one point they did converge on independently (the missing
canton-count explanation), both were right.

## What was checked and found sound

- The headline second-contribution $p=0.0005$ figure: verified directly against
  `data/processed/gam_paired_test.npz` — 8 of the 16 per-seed raw p-values from the 999-draw
  spatial-block permutation test are exactly 0, one is 0.001001; the median of 16 values is the
  average of the 8th/9th order statistics, giving exactly $0.0005005$. R-DeepSeek's claim that
  this "cannot be produced by the stated 999-draw method" is **refuted** — this is ordinary
  median arithmetic over a discrete distribution, not a bug.
- The Abstract's "+9–12 points" distrito-ablation range: verified against the body's own
  "+8.7 to +11.6 percentage points" (full sample vs. alternative binarization) and the
  resolution-matched subsample's "+10.1%" — the abstract figure is a defensible rounding of the
  range across all three robustness checks, not (as R-Antigravity claimed) an inconsistency with
  a single "+8.7pp" headline number. **Refuted.**
- The manuscript's own explicit reconciliation of the 66.2%/67.64% two-grid baseline discrepancy
  (lines 453-457): R-Antigravity quoted this reconciliation sentence itself as evidence of an
  unresolved "internal confusion" — the quoted text is the fix, not the problem. **Refuted** as
  stated, though DeepSeek's narrower, correct point about the parallel best-$T$ discrepancy
  survives (see Minor points).
- R-Antigravity's four other MAJOR findings (median-$p$ Bonferroni heuristic as "mathematically
  invalid"; best-of-grid selection as "in-sample overfitting"; classification-accuracy framing as
  poorly aligned with the journal's scope; the three-party coalition binarization as
  "undermining physical and political validity") all restate limitations the manuscript already
  discloses explicitly, in some cases in nearly the same words, in its own Methods and
  Limitations sections. Not incorrect as observations, but not actionable findings either — the
  paper already says this about itself.

---

**Dropped findings** (raised, checked, did not survive verification):
- R-DeepSeek: headline $p=0.0005$ "cannot be produced by" the stated 999-draw method — refuted,
  ordinary median arithmetic (see above).
- R-Antigravity: Abstract "+9–12pp" vs. "+8.7pp" internal inconsistency — refuted, misreads the
  abstract sentence as describing the point estimate rather than the stated robustness-check
  range.
- R-Antigravity: 66.2%/67.64% baseline discrepancy as unresolved "internal confusion" — refuted,
  the quoted text is the manuscript's own explicit reconciliation.
- R-Antigravity: median-$p$ Bonferroni heuristic, best-of-grid selection, classification-accuracy
  framing, three-party coalition binarization — not dropped as *wrong*, but downgraded out of the
  findings list as *not novel*: each restates a limitation the manuscript already discloses
  explicitly in its own text.
- R-Antigravity: novelty positioning vs. "extensive sociophysics... literature on real
  administrative and census graphs" — no specific paper was named to check the claim against;
  left unverified and not included as a finding (contrast with R-DeepSeek's findings 4 and 5
  above, which named specific, checkable papers).
- R-Antigravity: Eq. 2 "branding... as a generalization of the Hamiltonian" overstating a basic
  linear reweighting — the manuscript's own language already frames this modestly ("just a
  single effective field handed to the same, otherwise unmodified Monte Carlo engine," line
  ~410); does not match a close read as an overclaim.
- R-Antigravity: Massoli differentiation as a "laundry list" failing to establish conceptual
  advance — a stylistic/subjective critique of scientific-writing register, not a checkable
  factual defect; the underlying five-axis differentiation is itself substantive (verified in
  this project's own prior novelty-check rounds).
