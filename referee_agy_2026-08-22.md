### Dimension 1: Methods & Reproducibility

severity: MAJOR
location: Section 3.2, Paragraph 1
quote: "where $J_{ij} > 0$ is the coupling between geographically adjacent units $i$ and $j$ (set by shared border length; zero for non-adjacent pairs), and $h_i$ is unit $i$'s local field."
problem: The coupling strength $J_{ij}$ is defined only qualitatively as being "set by shared border length" without specifying its units, normalization factor, or relative scaling against the dimensionless field $h_i$, making the Hamiltonian and effective temperature scale completely un-reproducible.
fix: Explicitly define the mathematical formula, normalization factor (e.g., mean border length or perimeter ratio), and dimensional units used to construct the $J_{ij}$ coupling matrix.

severity: MAJOR
location: Section 3.4, Paragraph 4
quote: "Where a figure is pooled across seeds (Section~\ref{sec:observables}), we apply this correction directly to the \emph{median} of the per-seed raw $p$-values, as a conservative screening heuristic rather than a formally derived family-wise-error-rate guarantee for that aggregated quantity -- correcting each seed's raw $p$-value individually before vote-counting would be the more rigorous alternative, which we did not implement."
problem: Multiplying the median of correlated per-seed $p$-values by the grid size is a mathematically invalid heuristic with no theoretical basis for family-wise error rate control.
fix: Correct each seed's $p$-value individually before pooling, or employ a formal combined-significance test (e.g., Fisher's or Stouffer's method adjusted for dependence) across replicates.

severity: MAJOR
location: Section 3.4, Paragraph 4
quote: "Because every headline alignment/significance figure in this paper is reported at whichever $T$ in the grid maximizes alignment, these are best-of-grid statistics rather than results at a single pre-specified $T$."
problem: Evaluating model performance at the post-hoc empirical argmax of temperature on the actual election outcome without a train/test partition or cross-validation constitutes in-sample overfitting.
fix: Calibrate the operating temperature $T$ on a separate training partition (e.g., spatial cross-validation or prior election cycle) before evaluating predictive alignment on test data.

severity: MINOR
location: Section 3.5, Paragraph 3
quote: "Every spatial-block $p$-value below is estimated from 999 Monte Carlo sign-flip draws (matching the Moran's $I$ test's 999-permutation budget above), not exact enumeration even where the block count would make that feasible; the resulting Monte Carlo standard error is $\sqrt{p(1-p)/999} \approx 0.005$--$0.015$ over the range of $p$ values reported below."
problem: Running 999 Monte Carlo random draws with replacement when the entire permutation space consists of only $2^7 = 128$ province sign-flips introduces unnecessary sampling noise rather than computing the exact permutation distribution.
fix: Replace Monte Carlo sampling with exact enumeration of all $2^{n_{\text{blocks}}}$ permutations for canton-level ($n=7$) block tests and state the exact discrete $p$-value resolution limit ($2/128 = 0.0156$).

severity: MINOR
location: Section 3.5, Paragraph 1
quote: "Spatial autocorrelation of the empirical vote pattern itself (independent of any simulation) is measured with Moran's $I$ \citep{moran1950}, using a 999-permutation test for significance."
problem: The spatial weight matrix formulation and row-standardization scheme used to compute Moran's $I$ are entirely omitted.
fix: Provide the exact algebraic specification and standardization convention (e.g., binary adjacency vs. shared border length weighting) used for the spatial weight matrix $W$.

severity: MINOR
location: Section 2.2, Paragraph 1
quote: "two further distritos (Pejivalle/Pejibaye and Los Angeles/\'Angeles) could not be reconciled between the electoral and boundary data sources due to genuine alternate-name variants and were dropped as well, leaving $N=488$ usable distrito-level nodes."
problem: Dropping mainland distritos due to minor typographic discrepancies creates artificial topological boundaries and distorts border-coupling sums for all neighboring nodes.
fix: Reconcile the two distritos using official TSE administrative codes and restore them to the contiguous graph topology.

---

### Dimension 2: Novelty vs. Prior Art

severity: MAJOR
location: Section 1, Paragraph 1
quote: "What is comparatively rare -- absent from all of the above -- is a model whose coupling network is not an assumption -- a lattice, a mean-field all-to-all approximation, or a configuration model -- but the literal geographic adjacency structure of a real country, fit against that country's own official results and simulated rather than solved analytically, with an explicit accounting of how much of the outcome the network topology explains on its own versus how much needs each unit's own political lean on top of it"
problem: Claiming that simulating an empirical geographic adjacency network with local fields is "absent from all of the above" ignores extensive sociophysics and spatial opinion dynamics literature on real administrative and census graphs.
fix: Reframe the positioning to acknowledge existing spatial-network sociophysics models and clearly specify that the novelty lies in the multi-scale ablation protocol rather than the empirical graph simulation itself.

severity: MAJOR
location: Section 3.3, Paragraph 1
quote: "which collapses exactly to Eq.~\eqref{eq:hamiltonian} when either $\lambda_{pol}=0$ or $\lambda_{soc}=0$ -- a genuinely equivalent generalization of the single-field model, not an approximation to it, since $\lambda_{pol} h_i^{pol} + \lambda_{soc} h_i^{soc}$ is itself just a single effective field handed to the same, otherwise unmodified Monte Carlo engine."
problem: Branding a linear combination of two external covariate vectors as a "generalization of the Hamiltonian" overstates a basic parameter reweighting of a standard random-field Ising model.
fix: State plainly that the model uses a composite local field $h_i^{\text{eff}} = \lambda_{\text{pol}} h_i^{\text{pol}} + \lambda_{\text{soc}} h_i^{\text{soc}}$ without portraying it as a new physical extension to the Ising Hamiltonian.

severity: MAJOR
location: Section 5.1, Paragraph 5
quote: "the two models differ on network construction (real geographic adjacency here versus a conceptual-similarity network there), field structure (two independently-weighted fields here versus a single PCA-aggregated composite there), dynamics (a temperature scan for best fit here versus simulated annealing initialized at the observed configuration there), uncertainty quantification (multistability, counterfactual, and cascade diagnostics here versus conformal prediction there), and domain (Costa Rican elections here versus Italian municipal hub classification there)."
problem: Distinguishing the paper's novelty from Massoli (2026) via a laundry list of mechanical implementation variations fails to establish a distinct conceptual or physical advance.
fix: Articulate the fundamental physical mechanisms and theoretical questions that this formulation resolves which cannot be addressed within Massoli's statistical mechanics framework.

severity: MINOR
location: Section 5.1, Paragraph 5
quote: "Third, this paper's own novelty relative to closely related territorial socio-economic modeling work \citep{massoli2026} has been re-checked specifically against the two-field extension and the GAM finding, not only against the original single-field model (see the novelty-tracking document accompanying this project's code repository):"
problem: Referencing an informal "novelty-tracking document" from an internal repository to defend originality is unacceptable in a peer-reviewed submission.
fix: Remove the parenthetical reference to the internal repository file and incorporate all necessary scholarly differentiation directly into the manuscript text.

---

### Dimension 3: Results & Figures Internal Consistency

severity: MAJOR
location: Abstract, Paragraph 1
quote: "Repeating the ablation at distrito resolution ($N=488$) reverses this: the marginal contribution grows to $+9$--$12$ points, reproducing across a subsample and alternative binarization, though formal significance is test/binarization-sensitive."
problem: The Abstract claims an effect size of "+9--12 points" despite the headline full-sample baseline in Table 2 and Section 4.5 being strictly $+8.7$ percentage points (66.2% to 74.8%).
fix: Report the primary full-sample result of $+8.7$ percentage points in the Abstract before citing the range of subsidiary robustness checks.

severity: MAJOR
location: Section 3.4, Paragraph 3
quote: "the geography-only distrito-level baseline is reported at two slightly different values depending on which grid produced it -- 66.2\% in Table~\ref{tab:distrito} ($T\in[0.05,3.5]$) versus 67.64\% in Section~\ref{sec:mideplan} ($T\in[0.05,5.0]$) -- both real best-of-grid numbers for the identical underlying quantity, differing only in how much of the low-$T$ tail the wider grid samples."
problem: Reporting two conflicting numerical values (66.2% vs. 67.64%) for the identical physical and geographic baseline across sections creates internal confusion.
fix: Adopt a single standardized temperature grid across all runs and report one canonical baseline value throughout the text and tables.

severity: MINOR
location: Section 4.3, Figure 4 Caption
quote: "Gray cantons have no matching result row for that election (see Section~\ref{sec:data}) and are excluded from that election's $N$ in Table~\ref{tab:historical}."
problem: The caption directs the reader to Section 2 for missing cantons across cycles, but Section 2 contains no mention of the administrative creation of Río Cuarto, Monteverde, and Puerto Jiménez that accounts for $N$ changing from 81 to 82 to 84.
fix: Add a brief note in Section 2 explaining the historical canton additions across the 2018, 2022, and 2026 election cycles.

---

### Dimension 4: Journal Fit, Clarity & Physics Grounding

severity: MAJOR
location: Section 5.1, Paragraph 4
quote: "Finally, this paper's positive headline result (Section~\ref{sec:ablation-distrito}) is established via a paired classification-accuracy comparison rather than translated into a physical observable such as an effective coupling shift or a critical-temperature estimate; the genuine thermodynamic machinery in this paper (susceptibility, specific heat, the Binder cumulant) is used here to establish the null result of Section~\ref{sec:fss}, not the positive one, which we consider an honest description of what this specific model and dataset can currently support rather than a limitation to paper over."
problem: The manuscript relies entirely on machine learning classification accuracy metrics for its positive claims while its statistical physics machinery produces only null results, making it poorly aligned with the core scope of *Physica A*.
fix: Re-anchor the positive claims in statistical physics observables (such as domain wall surface tension, spatial correlation functions, or energy barrier distributions) rather than raw classification accuracy.

severity: MAJOR
location: Section 2.1, Paragraph 3
quote: "Second, Liberaci\'on Nacional, Coalici\'on Agenda Ciudadana, and Frente Amplio span traditional-establishment, centrist, and left positions and did not contest 2026 as an actual alliance; collapsing their combined vote into one field value treats a canton split three ways between them identically to one unanimously behind a single one of the three."
problem: Constructing an artificial, post-hoc three-party coalition to force a binary spin representation undermines the physical and political validity of the system being modeled.
fix: Implement a multi-state spin model (e.g., Potts model) to represent the genuine multi-party electoral landscape, or restrict the primary analysis to actual head-to-head runoff elections.

severity: MAJOR
location: Section 5.1, Paragraph 6
quote: "three other second-contribution results are more exposed, since each depends on classifying specific individual units correctly rather than an aggregate significance test: the domain-wall analysis's within-GAM economic-marginalization reading (Section~\ref{sec:domainwall}, already flagged there as plausible but not cleanly established), the multistability check's two flagship cross-year-consistent fault-line distritos (Section~\ref{sec:multistability}, both sitting in cantons named above as misclassification-prone, which undermines cross-year consistency as a way of distinguishing genuine dynamics from a static labeling artifact), and the cascade test's single largest propagating case (Section~\ref{sec:cascade}, Orosi, in another such canton)."
problem: Devoting multiple subsections to domain walls, multistability, and single-node cascades when the flagship cases are acknowledged artifacts of an inaccurate canton-level proxy invalidates the physical conclusions drawn from those diagnostics.
fix: Acquire the genuine distrito-level GAM boundary layer and re-run all domain-wall, multistability, and cascade simulations on the true geometry before drawing dynamical inferences.

severity: MINOR
location: Section 4.4, Paragraph 4
quote: "The finding therefore upgrades from ``inconclusive'' to \textbf{no critical point found} in the scanned temperature range, at either of the two spatial resolutions examined, for the 2026 election -- consistent with every other pooled scan in this paper, none of which shows an interior susceptibility or specific-heat peak once low-temperature pooling artifacts are accounted for."
problem: Categorically concluding "no critical point found" based on Binder cumulant behavior across only two discrete system sizes exceeds the methodological capability of finite-size scaling.
fix: Soften the claim to state that Binder cumulants for $N=84$ and $N=488$ show no scale-invariant intersection within the scanned temperature range.

severity: MINOR
location: Section 1, Paragraph 2
quote: "Several headline numbers in this paper's early analyses (not shown here in their original, since-corrected form) reversed or vanished once replaced with a properly pooled multi-seed estimate, and we flag every place that distinction mattered."
problem: Discursive references to discarded preliminary drafts and internal project history clutter the Introduction with irrelevant meta-narrative.
fix: Remove all narrative references to prior unshown draft iterations and present the multi-seed methodology directly.

---

### Overall Assessment & Recommendation

This manuscript models Costa Rican presidential elections using an Ising framework on empirical border-adjacency networks. While the exploration of spatial scale dependence is methodologically interesting and the authors exhibit commendable transparency regarding statistical caveats, the manuscript suffers from severe foundational vulnerabilities that make it unsuitable for publication in *Physica A* in its present form. First, the paper's positive findings are articulated almost entirely as classification-accuracy gains scored at post-hoc best-fit temperatures, while the actual statistical mechanics apparatus (susceptibility, specific heat, Binder cumulants) delivers exclusively null results or low-temperature multi-chain freezing artifacts. Second, the primary 2026 configuration relies on an artificial, post-hoc agglomeration of three disparate political parties into a fictitious binary coalition, while the spatial GAM analyses depend on an admitted canton-level proxy whose misclassifications directly drive the paper's flagship domain-wall, multistability, and cascade findings. Third, the statistical methodology includes ad-hoc heuristics (such as Bonferroni-correcting median $p$-values across seeds) and conflicting baseline definitions across sections. Substantial rework is required to ground the findings in authentic statistical physics observables, obtain exact boundary geometries, implement proper out-of-sample parameter validation, and remove informal meta-commentary.

**Recommendation:** Reject and rework
