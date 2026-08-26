Now I'll conduct a thorough peer review of the manuscript as requested, examining it across the four specified dimensions.

severity: MAJOR
location: Abstract
quote: "Repeating the ablation at distrito resolution ($N=488$) reverses this: the marginal contribution grows to $+9$--$12$ points, reproducing across a subsample and alternative binarization, though significance is test/binarization-sensitive -- aggregation was masking a real effect."
problem: The abstract overstates the statistical significance while burying the crucial caveat that significance is highly sensitive to methodological choices, creating a misleading impression of robust findings.
fix: Clearly state in the abstract that while the effect size appears consistent (+9-12 points), formal statistical significance ranges from non-significant to significant depending on the choice of test and binarization method, with no principled way to adjudicate between reasonable alternatives.

severity: MAJOR
location: Section 3.5 (Distrito-level ablation)
quote: "We therefore ran two further, more direct checks rather than leaning on any single significance test... Is the effect formally confirmed at conventional significance, independent of which reasonable methodological choice is made? The answer is no: McNemar alone says yes at $p=0.0009$; the same test under an alternative binarization says only $p=0.087$; a spatially-aware alternative to McNemar ranges from clearly non-significant to significant depending on an essentially arbitrary blocking choice"
problem: The paper acknowledges that its central finding lacks robust statistical confirmation due to sensitivity to arbitrary methodological choices, yet continues to present it as a key result without sufficient hedging.
fix: Either provide a principled justification for preferred methodological choices or substantially downgrade claims about statistical significance, focusing exclusively on effect size estimates with appropriate uncertainty quantification.

severity: MINOR
location: Section 2.3 (Monte Carlo dynamics)
quote: "We report a simple, conservative Bonferroni correction alongside every raw $p$-value below (raw $p$ times the number of grid points scanned, 24 or 32 depending on the analysis, capped at 1), rather than a more powerful max-statistic permutation null, since the latter would require rerunning each full temperature scan many times under label permutation, which we did not do."
problem: The authors acknowledge using a suboptimal correction method for multiple testing across temperature grids but don't quantify how this affects their conclusions.
fix: Either implement the more appropriate max-statistic permutation approach or provide simulation-based evidence that Bonferroni correction is adequate for their specific use case.

severity: MAJOR
location: Section 3.8 (Capital-region membership - GAM)
quote: "Three independent candidate fields (MIDEPLAN, the non-circular political field, GAM) were tested and only the winner's (GAM's) significance figure is reported as the headline result... stacking a further, equally conservative $3\times$ field-selection correction on top of that leaves $p\approx0.048$ -- still (barely) below the conventional 0.05 threshold, though with much less headroom than the uncorrected $p=0.0005$ might suggest."
problem: The paper performs multiple hypothesis testing across different field candidates but only applies partial correction, dramatically inflating Type I error rates.
fix: Apply proper multiple testing correction that accounts for both the temperature grid search and the field selection process, or clearly state that the GAM result should be considered exploratory/hypothesis-generating rather than confirmatory.

severity: MINOR
location: Figure 1 caption
quote: "Costa Rica's two administrative granularities used in this paper: the 84 cantons (bold outlines), used for the main ablation (Section~\ref{sec:ablation-canton}), the historical comparison (Section~\ref{sec:historical}), and one of the two system sizes in the finite-size-scaling analysis (Section~\ref{sec:fss}); and the 492 distritos (thin outlines, 488 after dropping isolated/unmatched nodes, see Section~\ref{sec:data})"
problem: The figure caption states there are 492 distritos but the text mentions different numbers (488 for 2026, 483 for 2022) without clear explanation of why these exclusions vary by year.
fix: Provide a clearer explanation in either the figure caption or main text about why different numbers of distritos are excluded in different analyses, including a table summarizing exclusions by year and reason.

severity: MAJOR
location: Section 3.4 (Is there a critical point?)
quote: "Costa Rica's administrative hierarchy gives us only two real granularities to work with -- canton ($N=84$) and distrito ($N=488$) -- for the same election and the same real adjacency structure; we do not have a natural third real system size, so the analysis below should be read as a two-size check rather than a full convergence study."
problem: The finite-size scaling analysis uses only two system sizes, which is insufficient to reliably identify critical points, as the authors themselves acknowledge, yet they still present this as a meaningful test.
fix: Either acknowledge more prominently that this analysis cannot definitively rule out critical behavior or supplement with synthetic system sizes to enable proper finite-size scaling.

severity: MINOR
location: Section 2.2 (A second, independent field)
quote: "Section~\ref{sec:mideplan} uses Eq.~\eqref{eq:hamiltonian2} with $h^{pol}=$ 2026's own margin and $h^{soc}=$ the MIDEPLAN field: a 1D scan over $\lambda_{soc} \in [0,2]$ at $\lambda_{pol}=0$ isolates the social field cleanly... The non-circular political field (Section~\ref{sec:noncircular}) and the GAM field (Section~\ref{sec:gam}--\ref{sec:cascade}) each instantiate Eq.~\eqref{eq:hamiltonian2} with $\lambda_{pol}=0$ and the field under test placed in the $h^{soc}$ slot, unweighted ($\lambda_{soc}=1$)"
problem: The paper inconsistently applies optimization to different fields (optimizing MIDEPLAN's weight but not GAM's), making comparisons between field performance potentially unfair.
fix: Apply consistent optimization procedures across all tested fields or explicitly justify why different approaches are appropriate for different field types.

severity: MAJOR
location: Section 3.10 (A canton-level polarization trend)
quote: "2018 is the strangest case: GAM's raw signal there is maximal (100% of GAM cantons on one side versus 62% in the periphery) yet adding it lowers alignment by 9.6 points, plausibly connected to 2018's already-documented energetic anomaly (Section~\ref{sec:2018}) -- forcing a uniform field on top of an already-hard-to-find pattern may fight the geographic contagion rather than help it, at this lighter canton-scale Monte Carlo budget."
problem: The paper offers post-hoc explanations for anomalous results without testing alternative hypotheses or providing quantitative evidence for the proposed mechanism.
fix: Test the proposed explanation directly through controlled experiments (e.g., varying Monte Carlo budget systematically for 2018) or acknowledge more explicitly that this remains speculative.

severity: MINOR
location: Section 4 (Discussion)
quote: "The explanation for 2018's anomalous behavior (Section~\ref{sec:2018}) illustrates a general point about fitting physically motivated models to real, historically contingent data: a pattern can be both genuinely spatially clustered (high Moran's $I$) and poorly reproduced by a random-start energy-minimization search, because those are different properties."
problem: The discussion conflates model limitations with fundamental properties of the data, suggesting that the inability to reproduce 2018's pattern reflects something inherent about that election rather than potential model misspecification.
fix: Acknowledge that the failure to reproduce 2018's pattern could indicate model limitations rather than just properties of the specific election, and discuss potential model improvements that might better capture such patterns.

severity: MAJOR
location: Section 3.9 (Domain-wall structure)
quote: "Within GAM specifically, error rate correlates with MIDEPLAN's economic axis ($r=-0.391$ for 2026): the highest-error GAM distritos average an economic score of 54.4 versus 65.1 for low-error GAM distritos -- plausible but not cleanly established, since several of the highest-error distritos driving this correlation sit in cantons (e.g. Mora) most likely misclassified by the canton-level GAM proxy"
problem: The paper identifies potential confounding from GAM proxy misclassification but doesn't quantify its impact on key findings, leaving readers unable to assess result reliability.
fix: Conduct sensitivity analyses that explicitly model the potential impact of GAM misclassification on all affected results, or substantially qualify claims dependent on individual distrito classifications.

Overall Assessment:

This manuscript presents an ambitious application of Ising models to Costa Rican electoral geography with thoughtful methodological innovations, particularly the resolution-dependent analysis and model-native diagnostics. However, the paper suffers from significant issues with statistical inference and result interpretation that undermine confidence in its central claims. The authors admirably acknowledge many limitations, including the sensitivity of significance testing to methodological choices, the inadequacy of two-point finite-size scaling, and potential confounding from GAM proxy misclassification. Yet they continue to present key findings with insufficient hedging, creating tension between their cautious methodological discussions and stronger result claims.

The most serious issue is the central finding about distrito-level predisposition effects: while the effect size (+9-12 percentage points) appears reasonably consistent across analyses, the paper explicitly states that formal statistical significance "is not robust to reasonable alternative choices of test or binarization" and depends on "essentially arbitrary" decisions. Presenting this as a confirmed discovery rather than a hypothesis-generating observation is problematic for a journal like Physica A that emphasizes rigorous statistical mechanics.

Additionally, the multiple hypothesis testing issues—both across temperature grids and field candidates—are not adequately addressed, despite clear acknowledgment of the problem in the limitations section. The paper would benefit from either implementing more appropriate statistical corrections or substantially reframing its conclusions to match the actual evidentiary strength.

Recommendation: Major revisions required. The paper has valuable insights about scale-dependence in spatial voting models and innovative methodological approaches, but the statistical presentation needs substantial strengthening before publication. The authors should either provide more robust statistical evidence for their claims or significantly moderate their conclusions to reflect the acknowledged limitations in statistical confirmation.
