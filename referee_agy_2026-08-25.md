# Referee Report for *Physica A: Statistical Mechanics and its Applications*

**Manuscript Title:** *Geography versus Predisposition in Costa Rican Presidential Elections: A Real-Network Ising Model Across Spatial Scales and Election Cycles, with a Search for Non-Circular Predisposition Fields*  
**Author:** Tomas Rojas  

---

## 1. Dimension 1: Methods and Reproducibility

severity: MAJOR  
location: Section 2.1, paragraph 4  
quote: "Each unit's field value is its normalized vote margin between the two sides of whichever binarization is in use (positive toward the majority label, negative toward the minority label)."  
problem: The exact mathematical definition of the normalized vote margin is never formally defined, preventing exact numerical replication of the Hamiltonian's external field term.  
fix: Provide the explicit algebraic expression defining $h_i$ in terms of candidate vote counts $V_{i,1}$, $V_{i,2}$, and total/valid turnout.

---

severity: MAJOR  
location: Section 3.4, paragraph 3  
quote: "Where a figure is pooled across seeds (Section~\ref{sec:observables}), we apply this correction directly to the \emph{median} of the per-seed raw $p$-values, as a conservative screening heuristic rather than a formally derived family-wise-error-rate guarantee for that aggregated quantity -- correcting each seed's raw $p$-value individually before vote-counting would be the more rigorous alternative, which we did not implement."  
problem: Multiplying the median of sample $p$-values across Monte Carlo replicates by the grid size is mathematically invalid as a family-wise error rate control.  
fix: Correct each replicate's $p$-value individually for grid multiplicity before pooling or implement an omnibus max-statistic permutation test over the full temperature trajectory.

---

severity: MAJOR  
location: Section 3.6, paragraph 1  
quote: "Pooling introduces its own subtlety worth stating plainly: at low temperature, independent chains can each freeze into a \emph{different} locally stable configuration rather than all finding the same one, and because both $\chi$ and $C$ divide by $T$, that between-chain disagreement can be amplified into an apparent divergence at the low-$T$ edge of a scan that is not a real thermodynamic effect."  
problem: The reported low-temperature divergence in magnetic susceptibility is an artifact of computing the variance across symmetry-broken pure states rather than evaluating the connected susceptibility within single pure states.  
fix: Redefine the magnetic susceptibility as the connected fluctuation $\chi = N(\langle m^2 \rangle - \langle |m| \rangle^2)/T$ computed within individual Markov chains prior to seed averaging.

---

severity: MINOR  
location: Section 3.4, paragraph 2  
quote: "The canton-level ablation (Section~\ref{sec:ablation-canton}) and historical comparison (Section~\ref{sec:historical}) use $T \in [0.05, 3.5]$, a 24-point grid, with 500 equilibration and 500 measurement sweeps per replicate. The finite-size-scaling analysis (Section~\ref{sec:fss}) and distrito-level ablation (Section~\ref{sec:ablation-distrito}) use $T \in [0.05, 3.5]$ as well but a 32-point grid, with 20{,}000 equilibration and 20{,}000 measurement sweeps per replicate, run on a computing cluster -- the heavier budget needed for the larger $N=488$ system to equilibrate properly, as Section~\ref{sec:fss} discusses directly."  
problem: The canton-level simulations use a 40-fold lighter Monte Carlo budget (500 sweeps) than the distrito level (20,000 sweeps) without demonstrating that 500 sweeps guarantees convergence on the $N=84$ graph.  
fix: Re-run the canton-level scans with 20,000 equilibration and measurement sweeps to confirm that the canton null result is not an artifact of insufficient sampling.

---

severity: MAJOR  
location: Section 3.3, paragraph 1  
quote: "The non-circular political field (Section~\ref{sec:noncircular}) and the GAM field (Section~\ref{sec:gam}--\ref{sec:cascade}) each instantiate Eq.~\eqref{eq:hamiltonian2} with $\lambda_{pol}=0$ and the field under test placed in the $h^{soc}$ slot, unweighted ($\lambda_{soc}=1$), matching the convention already used for $h=$margin in Sections~\ref{sec:ablation-canton}/\ref{sec:ablation-distrito}."  
problem: Evaluating unweighted $\lambda_{soc}=1$ field comparisons across covariates with drastically different intrinsic variances ($\sigma=1.00$ for GAM and $z$-scored MIDEPLAN versus $\sigma=0.167\text{--}0.280$ for vote margins) creates an uncalibrated, six-fold bias in the effective Zeeman coupling strength.  
fix: Standardize all candidate fields to unit variance prior to insertion into the Hamiltonian, or perform identical $\lambda$-grid parameter scans for every tested field.

---

## 2. Dimension 2: Novelty vs. Prior Art

severity: MAJOR  
location: Section 1, paragraph 3  
quote: "distinct from Korbel et al.'s \citep{korbel2026} double-random field, a single field array with bimodal support, in that ours are two separate field arrays from two separate data sources, tested against each other rather than combined into one distribution --"  
problem: The manuscript conflates an analytical random-field probability distribution over quenched disorder with a deterministic two-covariate linear Zeeman term to manufacture a theoretical distinction from Korbel et al. (2026).  
fix: Acknowledge that the two-field extension is a standard multivariable deterministic external field rather than framing it as a novel statistical mechanics field distribution.

---

severity: MAJOR  
location: Section 1, paragraph 1  
quote: "What is comparatively rare -- absent from all of the above -- is a model whose coupling network is not an assumption -- a lattice, a mean-field all-to-all approximation, or a configuration model -- but the literal geographic adjacency structure of a real country, fit against that country's own official results and simulated rather than solved analytically, with an explicit accounting of how much of the outcome the network topology explains on its own versus how much needs each unit's own political lean on top of it"  
problem: The claim that simulating Ising spin systems on literal border-adjacency graphs with site-dependent fields is absent from prior literature ignores decades of spatial statistical mechanics on geographic Markov Random Fields and auto-logistic models.  
fix: Situate the model within the established spatial Markov Random Field / auto-logistic literature (e.g., Besag 1974, 1986) and moderate the novelty claim regarding geographic graph adjacency.

---

severity: MINOR  
location: Section 5.1, paragraph 3  
quote: "Third, this paper's own novelty relative to closely related territorial socio-economic modeling work \citep{massoli2026} has been re-checked specifically against the two-field extension and the GAM finding, not only against the original single-field model (see the novelty-tracking document accompanying this project's code repository): the two models differ on network construction (real geographic adjacency here versus a conceptual-similarity network there), field structure (two independently-weighted fields here versus a single PCA-aggregated composite there), dynamics (a temperature scan for best fit here versus simulated annealing initialized at the observed configuration there), uncertainty quantification (multistability, counterfactual, and cascade diagnostics here versus conformal prediction there), and domain (Costa Rican elections here versus Italian municipal hub classification there)."  
problem: A primary defense of novelty against the most closely related contemporary sociophysics paper (Massoli, *Social Indicators Research* 2026) is sequestered in the Limitations section rather than being addressed directly in the Introduction.  
fix: Move the comparative differentiation against Massoli (2026) into Section 1 alongside the reviews of Korbel et al., Tiwari et al., and Borghesi & Bouchaud.

---

severity: MAJOR  
location: Section 5, paragraph 6  
quote: "The multistability check has no regression analog -- it asks whether the identical physical setup can land on different equilibria under random initialization alone, a question a point-estimate classifier cannot pose. The counterfactual temperature sweep and the cascade test go further still, requiring the dynamical system to be literally re-solved under a perturbation -- a generative use of the fitted model with no regression-coefficient analog."  
problem: The assertion that counterfactual perturbations and cascade sweeps have no econometric analog is incorrect, as spatial autoregressive multiplier matrices and spatial agent-based models evaluate identical localized perturbation dynamics.  
fix: Reframe these diagnostics as non-linear Monte Carlo realizations of spatial feedback rather than claiming point-estimate spatial regressions are incapable of calculating shock propagation.

---

## 3. Dimension 3: Results and Figures Internal Consistency

severity: MINOR  
location: Section 3.4, paragraph 2  
quote: "consequently, the geography-only distrito-level baseline is reported at two slightly different values depending on which grid produced it -- 66.2\% in Table~\ref{tab:distrito} ($T\in[0.05,3.5]$) versus 67.64\% in Section~\ref{sec:mideplan} ($T\in[0.05,5.0]$) -- both real best-of-grid numbers for the identical underlying quantity, differing only in how far into the high-$T$ range the wider grid extends (both share the same low-$T$ endpoint)."  
problem: Reporting two competing baseline alignment figures (66.2% vs 67.64%) and different optimal temperatures ($T=2.83$ vs $T=2.605$) for the exact same null model ($h=0$, 2026 coalition split, $N=488$) causes internal friction across result tables.  
fix: Re-tabulate Table 3 using the full $[0.05, 5.0]$ grid so that a single unified baseline of 67.64% is used across Sections 4.6, 4.7, 4.8, and 4.9.

---

severity: MINOR  
location: Section 4.3, Table 1  
quote: "2026 (round 1) & 84 & 75.0\% & $79.0\% \pm 2.2\%$ & Yes & $p=0.37$, 1/8 \\"  
problem: Table 1 presents the 2026 winner-vs-runner-up model alignment ($79.0\%$) solely relative to the majority baseline ($75.0\%$) while omitting the geography-only baseline ($76.49\%$), creating an inconsistency with Table 6 where that baseline is explicitly reported.  
fix: Include the geography-only baseline ($h=0$) column in Table 1 to allow direct comparison with Table 6 and Section 4.2.

---

severity: MINOR  
location: Abstract, paragraph 1  
quote: "Membership in the capital metropolitan area (GAM) is the strongest: $+13.4$ points, $p=0.0005$ for 2026 -- not significant for 2022 or at canton resolution, echoing the scale-dependence lesson."  
problem: Stating without qualification in the Abstract that GAM is "not significant at canton resolution" obscures the fact that the point estimate gains $+6.6$pp in 2026 and $+13.6$pp in 2022, failing significance primarily due to low test power ($N=84$ with 7 province blocks).  
fix: Explicitly state in the Abstract that the lack of significance at the canton scale reflects statistical power limitations rather than a zero effect size.

---

## 4. Dimension 4: Journal Fit, Scoping, and Theoretical Clarity

severity: MAJOR  
location: Section 4.5, paragraph 1  
quote: "A standard way to look for a genuine critical point independent of system size is a size-independent crossing of the Binder cumulant $U_4(T)$ computed at two or more different $N$; canonical finite-size-scaling practice typically uses three or more sizes to confirm that a crossing is a consistent, size-independent property rather than an incidental feature of one specific curve pair, since any two non-identical curves generically intersect somewhere. Costa Rica's administrative hierarchy gives us only two real granularities to work with -- canton ($N=84$) and distrito ($N=488$) -- for the same election and the same real adjacency structure; we do not have a natural third real system size, so the analysis below should be read as a two-size check rather than a full convergence study."  
problem: Applying Binder cumulant crossings to two administrative networks ($N=84$ and $N=488$) that possess fundamentally different degree distributions, average degrees, and topological dimensions invalidates the self-similarity prerequisite of finite-size scaling theory.  
fix: Explicitly state that Binder cumulant crossings assume topologically self-similar graphs and clarify that the 5 crossings reflect structural/degree heterogeneity between the two administrative levels rather than thermal fluctuations.

---

severity: MAJOR  
location: Section 5.1, paragraph 5  
quote: "Finally, this paper's positive headline result (Section~\ref{sec:ablation-distrito}) is established via a paired classification-accuracy comparison rather than translated into a physical observable such as an effective coupling shift or a critical-temperature estimate; the genuine thermodynamic machinery in this paper (susceptibility, specific heat, the Binder cumulant) is used here to establish the null result of Section~\ref{sec:fss}, not the positive one, which we consider an honest description of what this specific model and dataset can currently support rather than a limitation to paper over."  
problem: For a manuscript submitted to *Physica A*, relying exclusively on classification accuracy percentages and McNemar tests for positive claims while relegating thermodynamic response functions to null checks reduces the statistical physics framework to a computational heuristic.  
fix: Calculate the empirical spin-spin spatial correlation function $G(r) = \langle s_i s_j \rangle - \langle s_i \rangle \langle s_j \rangle$ across network geodesic distance $r$ to extract physical correlation lengths $\xi(T)$ under both $h=0$ and $h \neq 0$.

---

severity: MAJOR  
location: Section 4.10, paragraph 1  
quote: "A question with no regression analog: does the real network plus the GAM field settle into a unique equilibrium, or can the identical physical setup land on different answers depending only on random initialization? We use ``equilibrium'' here in the practical sense of this specific equilibration budget, not as a formal ergodic-theory claim about the infinite-time stationary distribution; seed-to-seed disagreement at fixed $T$ diagnoses finite-run mixing behavior (whether independent chains reach the same final configuration within the sweeps allotted), which is the operationally relevant question for a fitted model reporting a single best-fit configuration."  
problem: In single-spin-flip Glauber dynamics at non-zero temperature with finite $N$, the Gibbs distribution is strictly ergodic and unique; describing finite-sweep Markov chain trapping as physical "multistability" conflates algorithmic non-convergence with true thermodynamic phase coexistence.  
fix: Replace the unphysical term "multistability" with "kinetic trapping in metastable states" or "finite-time non-ergodic sampling."

---

severity: MAJOR  
location: Section 2.1, paragraph 3  
quote: "Second, Liberaci\'on Nacional, Coalici\'on Agenda Ciudadana, and Frente Amplio span traditional-establishment, centrist, and left positions and did not contest 2026 as an actual alliance; collapsing their combined vote into one field value treats a canton split three ways between them identically to one unanimously behind a single one of the three."  
problem: Fabricating a post-hoc three-party artificial "coalition" to enforce a binary Ising representation on an unaligned multi-party election undermines the sociophysical foundation of the spin Hamiltonian.  
fix: Formulate the multi-party electoral system natively as a $q$-state Potts model ($q=4$) on the actual party vote shares, or restrict the analysis strictly to two-candidate runoff elections.

---

## Overall Assessment and Recommendation

This manuscript investigates the interplay between geographic network adjacency and political predisposition across spatial scales in Costa Rican presidential elections using an Ising model with Glauber dynamics. The work contains valuable empirical honesty regarding multi-seed uncertainty and provides extensive ablation diagnostics across administrative granularities. However, from the perspective of *Physica A: Statistical Mechanics and its Applications*, the manuscript suffers from fundamental statistical physics and methodological deficiencies: it applies finite-size scaling to topologically incommensurate graphs, conflates finite-time Markov chain mixing with thermodynamic multistability, lacks rigorous field standardization across covariates, invents an ungrounded $p$-value multiplicity heuristic, and frames its positive claims almost entirely around classification accuracy rather than extracting physical observables such as spatial correlation functions. Furthermore, forcing an artificial three-party coalition into a binary Ising spin representation rather than deploying a $q$-state Potts model compromises the underlying sociophysical modeling. 

**Recommendation:** **Major Revisions** (bordering on Reject-and-Rework if physical correlation functions and proper Potts/standardized formulations cannot be supplied).
