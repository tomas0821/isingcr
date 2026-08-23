Reading additional input from stdin...
OpenAI Codex v0.149.0
--------
workdir: /home/tomas/research-current/IsingCR
model: gpt-5.6-terra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a02fc8-2ec6-7483-9f10-d707013af0f2
--------
user
Read manuscript/main.tex in this directory. Act as a hostile peer reviewer for a Physica A: Statistical Mechanics and its Applications submission. Read-only -- do not edit or write any files, only report findings.

Attack it across these four dimensions:
1. Methods/reproducibility -- are the Monte Carlo procedure, statistical tests, and data sources fully specified and internally consistent?
2. Novelty vs. prior art -- does the paper's own positioning against cited related work (Korbel et al., Massoli, Tiwari, Braha & de Aguiar, etc.) hold up?
3. Results/figures internal consistency -- do numbers match across the Abstract, body, tables, and Conclusion? Do figure captions match the text?
4. Journal fit/clarity -- is this appropriately scoped and written for Physica A, and is anything unclear, overclaimed, or under-hedged?

For every finding output exactly this format:
severity: MAJOR|MINOR
location: <section/paragraph>
quote: "<verbatim text from the draft>"
problem: <one sentence>
fix: <what would satisfy this referee>

A finding without a verbatim quote is invalid. End with a one-paragraph overall assessment and a recommendation (accept / minor revisions / major revisions / reject-and-rework).
warning: Codex could not find bubblewrap on PATH. Install bubblewrap with your OS package manager. See the sandbox prerequisites: https://developers.openai.com/codex/concepts/sandboxing#prerequisites. Codex will use the bundled bubblewrap in the meantime.
codex
I’ll review the LaTeX source strictly read-only, tracing the manuscript’s claims and cross-references for quoted, actionable referee findings.
exec
/bin/bash -lc "sed -n '1,260p' manuscript/main.tex" in /home/tomas/research-current/IsingCR
 succeeded in 191ms:
\documentclass[5p]{elsarticle}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}

\journal{Physica A: Statistical Mechanics and its Applications}

\begin{document}

\begin{frontmatter}

\title{Geography versus Predisposition in Costa Rican Presidential Elections:\\
A Real-Network Ising Model Across Spatial Scales and Election Cycles,\\
with a Search for Non-Circular Predisposition Fields}

\author[cicima,sede]{Tomas Rojas\corref{cor1}}
\ead{tomas.rojas_s@ucr.ac.cr}
\cortext[cor1]{Corresponding author.}
\address[cicima]{Centro de Investigaci\'on en Ciencia e Ingenier\'ia de Materiales (CICIMA), Universidad de Costa Rica, San Jos\'e, Costa Rica}
\address[sede]{Sede de Occidente, Universidad de Costa Rica, San Ram\'on, Costa Rica}

\begin{abstract}
We model Costa Rican presidential elections as an Ising system, each
administrative unit (canton or, at finer resolution, distrito) a binary
spin coupled to its geographic neighbors via a border-adjacency network,
biased by a field equal to its vote margin. Fitting Glauber Monte Carlo
scans to 2018/2022/2026 results, we ask whether the vote's spatial pattern
reflects geographic contagion (coupling) or predisposition (field): the
answer depends on resolution. At canton resolution ($N=84$, 2026), adding
the field improves alignment by only $+1.2$ points, not significant.
Repeating the ablation at distrito resolution ($N=488$) reverses this: the
marginal contribution grows to $+9$--$12$ points, reproducing across a
subsample and alternative binarization, though significance is
test/binarization-sensitive -- aggregation was masking a real effect. A
historical comparison finds the model's point estimate beats a
majority-class baseline for 2022/2026 but not 2018 (weakly confirmed by
per-seed testing), traced to 2018's vote pattern being energetically
disfavored, not weaker clustering; a finite-size-scaling analysis finds no
confirmed critical point for 2026 in the scanned range. Motivated by the
own-margin field's near-tautological match to its label ($99.8\%$ by
construction), we extend the Hamiltonian to a second field and test three
non-circular predisposition candidates. Membership in the capital
metropolitan area (GAM) is the strongest: $+13.4$ points, $p=0.0005$ for
2026 -- not significant for 2022 or at canton resolution, echoing the
scale-dependence lesson. Four diagnostics converge on a robustly determined
equilibrium, with uncertainty confined to a small set of fault-line
distritos -- three of which cannot be fully separated from a GAM-proxy
labeling artifact.
\end{abstract}

\begin{keyword}
sociophysics \sep Ising model \sep electoral geography \sep Monte Carlo
simulation \sep spatial adjacency network \sep predisposition fields \sep
Costa Rica
\end{keyword}

\end{frontmatter}

\section{Introduction}
\label{sec:intro}

Applying the mathematics of ferromagnetism to collective political behavior
is one of the oldest ideas in sociophysics, and it keeps being reinvented
because the underlying picture is genuinely apt: a voter's choice, like a
spin's orientation, is influenced both by an external bias (a policy
preference, a media environment, a personal history) and by the choices of
the voters around them (a neighbor-conformity or ``contagion'' pressure).
Recent work has used Ising-like and random-field models to study U.S.
electoral instability and the geometry of ``wasted votes''
\citep{siegenfeld2020,jordan2020}, to forecast a single high-profile election
\citep{galam2021}, to explain scaling laws in Brazilian state and municipal
returns \citep{cardoso2022,cardoso2023}, to study how media environments
shape polarization in agent-based election models \citep{dibenedetto2023},
and to fit an Ising model with an unconstrained random field to elections on
a synthetic $128\times128$/$256\times256$ square lattice \citep{tiwari2021}
-- the closest prior work in this specific journal, though with no real
geographic network and no real vote data behind either the coupling
structure or the field. Across a full century of U.S. presidential
elections, Braha and de Aguiar \citep{braha2017} analytically model
geography-driven ``voting contagion'' and find an abrupt transition in
contagion strength over time, but do so over an explicitly \emph{unknown}
network structure rather than a literal adjacency graph. Most closely to the
present approach, Korbel et al.\ \citep{korbel2026} fit a double-random-field
Ising-equivalent model to a
century of U.S. House elections -- but solve it analytically via closed-form
mean-field self-consistency equations on a configuration-model network, with
campaign spending (not vote margin) as the field, and with no Monte Carlo
simulation and no explicit spatial topology anywhere in the model. Closest on vocabulary, Godoy-Lorite \& Jones \citep{godoylorite2020} fit a
spin-based behavioral model with external fields, explicitly invoking
``social temperature,'' to real UK election outcomes (the EU Referendum,
two London Mayoral elections) -- but their network is \emph{inferred} from
behavioral snapshots in an abstract attribute space (Blau space), not the
literal geographic adjacency used here, and their multi-election comparison
is across different election \emph{types} in one city/country, not the
same election compared across real spatial \emph{resolutions}. Related
statistical-mechanics approaches to elections and territorial social systems
include agent-based geographic multi-election modeling via Dirichlet
processes \citep{mitra2026}, electoral-system-design susceptibility to
influence campaigns \citep{raducha2025}, and territorial socio-economic
dynamics more broadly \citep{massoli2026}; a recent review collects the
growing Ising-inspired sociophysics literature \citep{mullick2025}. What is
comparatively rare -- absent from all of the above -- is a model whose
coupling network is not an assumption -- a lattice, a mean-field all-to-all
approximation, or a configuration model -- but the literal geographic
adjacency structure of a real country, fit against that country's own
official results and simulated rather than solved analytically, with an
explicit accounting of how much of the outcome the network topology explains
on its own versus how much needs each unit's own political lean on top of
it -- the latter a decomposition a closed-form mean-field solution like
Korbel et al.'s \citep{korbel2026} cannot pose in the first place.

That is the gap this paper fills, specifically the combination of a real
geographic network, real multi-cycle election data, an explicit
geography-vs-predisposition ablation, and cross-scale replication -- not the
broader claim that Ising/random-field models have been applied to elections
at all, which is well established (see above). We build the real canton- and
distrito-level border-adjacency network of Costa Rica from official boundary
data, fit an Ising model with Glauber Monte Carlo dynamics against three
real national elections (2018, 2022, 2026) from the Tribunal Supremo de
Elecciones (TSE), and run a deliberate \emph{ablation}: the same model, same
data, same real network, once with the symmetry-breaking field switched off
(pure geographic contagion) and once with it set to each unit's real vote
margin (geography plus individual predisposition). The same question is
asked at two different spatial resolutions -- 84 cantons and 488 distritos
(Figure~\ref{fig:adminmap}) -- because Costa Rica's administrative geography
is unusually well suited to asking whether a finding at one level of
aggregation survives disaggregation,
and because the country's own political-science literature has documented
real geographic heterogeneity in party support at exactly this finer scale
\citep{cascantematamoros2006,camachosanchez2025,chavarriamora2022}. A
companion methodological point runs through every result reported here: a
single Monte Carlo run is not enough to trust a claim of this kind. Several
headline numbers in this paper's early analyses (not shown here in their
original, since-corrected form) reversed or vanished once replaced with
a properly pooled multi-seed estimate, and we flag every place that
distinction mattered.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{figures/admin_map.png}
  \caption{Costa Rica's two administrative granularities used in this paper:
  the 84 cantons (bold outlines), used for the main ablation
  (Section~\ref{sec:ablation-canton}), the historical comparison
  (Section~\ref{sec:historical}), and one of the two system sizes in the
  finite-size-scaling analysis (Section~\ref{sec:fss}); and the 492
  distritos (thin outlines, 488 after dropping isolated/unmatched nodes, see
  Section~\ref{sec:data}), the finer level -- each canton subdivides into
  several distritos.}
  \label{fig:adminmap}
\end{figure}

The paper's second contribution addresses a limitation of the first: the
own-vote-margin field used throughout Section~\ref{sec:ablation-distrito} is,
on inspection, close to tautological with the label it is scored against
(Section~\ref{sec:mideplan} makes this precise), so a field-driven
improvement in alignment risks partly just reflecting the field's own
construction rather than a genuine predisposition effect. We address this by
extending the Hamiltonian to accept a second, independently sourced field --
distinct from Korbel et al.'s \citep{korbel2026} double-random field, a
single field array with bimodal support, in that ours are two separate
field arrays from two separate data sources, tested against each other
rather than combined into one distribution -- (Section~\ref{sec:twofield})
and testing three non-circular candidates against
real distrito-level 2026/2022 data: a socioeconomic
development index published by Costa Rica's Ministry of National Planning
(MIDEPLAN), a non-circular political-continuity field built from the prior
election rather than the one being predicted, and membership in the Gran
\'Area Metropolitana (GAM), the capital metropolitan region -- by a wide
margin the strongest field found for 2026 (see Section~\ref{sec:gam} for
the 2022/canton-level caveats). We then run four further
diagnostics -- a multistability check, a domain-wall analysis, a
counterfactual temperature-sensitivity sweep, and a single-node cascade test
-- that interrogate the fitted dynamical system directly rather than
comparing static classification accuracy, addressing a fair question this
kind of covariate search otherwise invites: whether a real Monte Carlo model
is doing anything a spatial-lag regression on the same covariates could not.

The rest of the paper is organized as follows. Section~\ref{sec:data}
describes the electoral data and the two geographic networks, including the
new covariate sources. Section~\ref{sec:model} defines the model and
simulation procedure, including the two-field extension, in terms that
assume no prior familiarity with statistical mechanics.
Section~\ref{sec:results} reports the original six results in sequence -- an
illustrative comparison of a simulated and the real 2026 map; the
canton-level ablation; a historical comparison across all three elections; a
mechanistic explanation of why 2018 behaves differently; a finite-size-scaling
search for a genuine critical point; and the distrito-level ablation -- followed
by the second-contribution results: the MIDEPLAN composite and axis
decomposition, the non-circular political field, the GAM result, and the four
model-native diagnostics, closing with a canton-level polarization trend
across all three elections. Section~\ref{sec:discussion} discusses what the
scale-dependence of the ablation result implies and synthesizes the second
contribution's findings, and Section~\ref{sec:conclusion} concludes.

\section{Data and the electoral network}
\label{sec:data}

\subsection{Electoral results}

Official per-polling-station (\emph{junta}) results for the 2018 runoff, both
rounds of the 2022 election, and round 1 of the 2026 election were obtained
from TSE's public ``escrutinio definitivo'' releases and aggregated to the
canton and distrito level. The canton count itself grew across this span --
81 in 2018, 82 in 2022, 84 in 2026 -- as Costa Rica created three new
cantons in this period (R\'io Cuarto, split from Grecia in 2018; Monteverde,
split from Puntarenas in 2021; and Puerto Jim\'enez, split from Golfito in
2022), each first appearing as its own unit once created; this, not a data
gap, is why Figure~\ref{fig:realmaps} and Table~\ref{tab:historical} show
different $N$ per election. Two different binarizations of the vote are used
in this paper, deliberately kept separate:

\begin{itemize}
\item \textbf{Coalition split (2026 only, used in
  Sections~\ref{sec:ablation-canton}, \ref{sec:fss}, and
  \ref{sec:ablation-distrito}):} the leading party, Pueblo Soberano (48.5\%
  of the national vote), against a coalition of the next three largest
  parties (Liberaci\'on Nacional, Coalici\'on Agenda Ciudadana, Frente
  Amplio). This produces a competitive, non-degenerate split at both
  administrative levels; a naive ``leading party vs. everyone else'' split
  is degenerate for this election, since Pueblo Soberano's national
  landslide makes it the plurality winner in nearly every unit, leaving no
  real spatial pattern to explain.
\item \textbf{Winner vs. runner-up (Section~\ref{sec:historical}, all three
  elections):} for consistency across election cycles that differ in the
  number of competitive parties, the historical comparison instead binarizes
  each election as its top two vote-getters head to head, by construction
  for the 2018/2022 runoffs and by vote count for 2026 round 1.
\end{itemize}

Two limitations of the coalition split are worth stating plainly rather than
leaving implicit. First, it was chosen \emph{because} the more obvious
``leading party vs.\ everyone else'' split is degenerate for 2026, not
pre-registered independently of the outcome; the canton- and
distrito-resolution ablation results in
Sections~\ref{sec:ablation-canton}/\ref{sec:ablation-distrito} (though not
the $h=0$ finite-size-scaling result of Section~\ref{sec:fss}, which does not
depend on this choice) should be read with that in mind, pending a
robustness check against alternative groupings (next-two, next-four parties)
that this paper does not yet report. Second, Liberaci\'on Nacional,
Coalici\'on Agenda Ciudadana, and Frente Amplio span
traditional-establishment, centrist, and left positions and did not contest
2026 as an actual alliance; collapsing their combined vote into one field
value treats a canton split three ways between them identically to one
unanimously behind a single one of the three. We use it as a statistically
convenient macro-grouping that yields a competitive split, not a claim that
it corresponds to a single coherent political cleavage, and the two
binarizations used in this paper are not cross-validated against each other
for 2026 -- a check left to future work. Each unit's field value is its
normalized vote margin between the two sides
of whichever binarization is in use (positive toward the majority label,
negative toward the minority label). Reconciling TSE's naming conventions
with the boundary data below required correcting two systematic quirks:
TSE names each province's capital canton (and, one level down, its first
distrito) ``Central,'' where boundary files name it after the province or
canton itself; and TSE preserves ``\~{N}'' as distinct from ``N,'' where
generic accent-stripping folds the two together.


exec
/bin/bash -lc "sed -n '261,620p' manuscript/main.tex" in /home/tomas/research-current/IsingCR
 succeeded in 106ms:
\subsection{Geographic adjacency network}

Costa Rica's 84 official cantons (real geometry from UN OCHA's HDX COD-AB
boundary dataset) were converted to a border-adjacency graph: two cantons
are coupled if and only if they share a physical border, weighted by shared
border length normalized so the mean edge weight is 1.0 (i.e.\
$J_{ij} = l_{ij}/\bar{l}$, where $l_{ij}$ is the shared border length and
$\bar{l}$ the mean over all edges). The same procedure was applied one administrative level down
to the country's 492 distritos, after which two entirely isolated distritos
with no land neighbors (Isla del Coco and Chira) were dropped, since at zero
field an isolated spin is a pure coin flip regardless of temperature and
contributes no usable information to a coupling-driven analysis; two further
distritos (Pejivalle/Pejibaye and Los Angeles/\'Angeles) could not be
reconciled between the electoral and boundary data sources due to genuine
alternate-name variants and were dropped as well, leaving $N=488$ usable
distrito-level nodes.

\subsection{Socioeconomic development (MIDEPLAN IDS 2023)}
\label{sec:data-mideplan}

Costa Rica's Ministry of National Planning and Economic Policy (MIDEPLAN)
publishes a distrito-level \'Indice de Desarrollo Social (IDS), a composite
0--100 score blending five published sub-dimensions: SALUD (health),
PARTICIPA (civic participation), SEGURIDAD (security), EDUCACION (education),
and ECONOMICO (economic conditions). We use the 2023 edition, obtained as six
regional tables (one per planning region) totaling 490 distrito rows across
84 cantons -- 0 missing province/score values, matching MIDEPLAN's own stated
coverage exactly. Joined against this paper's $N=488$ electoral distrito
network, 486 of 488 nodes match (2 distritos created after the 2023
publication get a neutral field value rather than being dropped). Since a
0--100 score has no natural zero, each dimension (composite and all five
axes) is $z$-scored per distrito before use as a field:
$h_i = (\text{score}_i - \overline{\text{score}})/\sigma_{\text{score}}$.

\subsection{Gran \'Area Metropolitana (GAM) membership}
\label{sec:data-gam}

The GAM is Costa Rica's officially delimited metropolitan planning region,
governed by Plan GAM 2013--2030 (Decreto Ejecutivo
38145-PLAN-MINAE-MIVAH-MOPT-S-MAG, \emph{La Gaceta} No.~82, 30 April 2014),
covering 31 cantons across four provinces: San Jos\'e (13), Alajuela (3:
Alajuela, Atenas, Po\'as), Cartago (6), and Heredia (9). We use a
\emph{canton-level proxy} -- a distrito is flagged GAM if its parent canton is
one of the 31 -- not the true distrito-level boundary, which we could not
retrieve (the government planning ministry's site blocks automated access, a
GIS boundary layer at a municipal geoportal refused the connection, and an
academic atlas that would have had the annex is login-gated). This is a real,
stated imprecision: official sources describe the true boundary as covering
``184 distritos, in some cases fractions of distritos,'' meaning it does not
respect administrative distrito lines everywhere, and our canton-level proxy
correspondingly over-includes some large, mostly rural cantons that only
partially qualify (e.g.\ Mora, Alajuela's central canton, Aserr\'i, Para\'iso). The
proxy's aggregate count (186 distritos for 2026, 184 for 2022) is close to the
official 184-distrito figure, which bounds only the \emph{net}
over-count-minus-under-count, not the total number of individually
misclassified units -- a large canton like Mora being wholesale
over-included could in principle be offset by an equally large
under-inclusion elsewhere while the net count stays near zero;
Section~\ref{sec:limitations} discusses how this bears on each result that
uses the field. The field is symmetric
and unweighted: $h_i^{GAM} = +1$ if distrito $i$'s canton is in the GAM list,
$-1$ otherwise.

\subsection{A non-circular political field}
\label{sec:data-political}

Every field used through Section~\ref{sec:ablation-distrito} is built from
the same election's own vote margin, which we show in
Section~\ref{sec:mideplan} is close to tautological with the label it
predicts. As a genuinely independent alternative, we build a field from a
\emph{different} election's results: 2026's leading party, Pueblo Soberano, is
the direct electoral successor of Progreso Social Democr\'atico (PPSD),
2022's winner -- the same Rodrigo Chaves-aligned movement (``chavismo'')
under a different registered vehicle, reported contemporaneously by
Costa Rican outlets (\emph{El Observador}, 4 September 2025,
``Chavismo elige a Pueblo Soberano como partido para Elecciones 2026'';
\emph{AmeliaRueda.com}, ``Pueblo Soberano ser\'a el partido que buscar\'a
continuidad del gobierno de Rodrigo Chaves en 2026'') rather than a
peer-reviewed source, which we note as the nature of this evidence rather
than treat as an established scholarly fact; the empirical correlation
with 2026's own margin reported below ($r=0.70$) provides some independent
support regardless. The field is PPSD's margin in the 2022 runoff (already
computed for Section~\ref{sec:historical}'s winner-vs-runner-up
binarization), joined onto the 2026 distrito network (482 of 488 nodes
match; missing nodes get a neutral value). We considered two candidate
sources for this field and selected empirically: 2022's fragmented
25-candidate first round, where PPSD's raw vote share barely correlates with
the 2026 outcome ($r=0.15$), versus the runoff itself (PPSD vs.\ Liberaci\'on
Nacional head-to-head), which correlates strongly ($r=0.70$ with 2026's own
margin, $r=0.57$ with the 2026 outcome) -- the runoff is where voters
consolidated for or against the movement, and is the field used below.

\subsection{Registered-voter counts}
\label{sec:data-population}

To check whether any result below is confounded by unit population size, we
use registered-voter counts (\emph{electores\_inscritos}) already present in
the same per-junta TSE consolidado files used throughout this paper,
aggregated to distrito level by the identical procedure as every other
electoral variable -- guaranteeing an exact match (488 of 488, 483 of 483
nodes) against this paper's networks, unlike TSE's separately published
national voter registry (\emph{padr\'on electoral}), whose own geographic
labels are a finer, non-administrative reporting unit and could not be
reliably joined to this paper's distrito network (only 355 of 488 nodes
matched by name); we do not use the padr\'on itself below.

\section{Model and simulation}
\label{sec:model}

\subsection{The model, in plain terms}

Picture each canton (or distrito) as a small compass needle that can point
only ``up'' or ``down'' -- the two sides of whichever binary vote outcome is
being modeled. Two forces act on each needle. The first is peer pressure
from its geographic neighbors: a needle feels a pull toward whatever
direction most of its neighbors are already pointing, exactly as adjacent
magnetic domains align in a ferromagnet. The second is the needle's own
intrinsic bias, independent of what its neighbors do -- in this analysis,
each unit's own real vote margin. The competition between these two forces,
and between both of them and thermal noise (a stand-in for all the
unmodeled idiosyncrasy of real voters), is exactly the physics of the Ising
model with an external field, and it is what lets the ablation in this paper
be posed as a clean either/or: turn the second force off entirely, and only
neighbor-to-neighbor influence can produce a spatial pattern; turn it on,
and see how much more of the real map that intrinsic bias explains.

\subsection{Formal definition}

Each administrative unit $i$ carries a spin $s_i \in \{-1, +1\}$. The
energy of a configuration $\mathbf{s}$ is the standard Ising Hamiltonian
with an external field,
\begin{equation}
  E(\mathbf{s}) = -\sum_{\langle i,j \rangle} J_{ij}\, s_i s_j - \sum_i h_i s_i,
  \label{eq:hamiltonian}
\end{equation}
where $J_{ij} > 0$ is the coupling between geographically adjacent units $i$
and $j$ (set by mean-normalized shared border length as defined in
Section~\ref{sec:data}; zero for non-adjacent pairs), and
$h_i$ is unit $i$'s local field. Two field settings are compared throughout:
$h_i = 0$ for every $i$ (``geography only'') and $h_i = $ unit $i$'s real
vote margin (``geography plus predisposition''). Note that at $h=0$ the
Hamiltonian is symmetric under flipping every spin simultaneously ($s_i \to
-s_i \;\forall i$), so the model cannot distinguish ``traditional'' from
``emerging'' labeling on its own; all $h=0$ comparisons against the real map
therefore use a label-symmetric alignment score (Section~\ref{sec:observables}).

\subsection{A second, independent field}
\label{sec:twofield}

Sections~\ref{sec:mideplan}--\ref{sec:cascade} test predisposition candidates
other than a unit's own vote margin. Rather than replace $h_i$ ad hoc, we
extend Eq.~\eqref{eq:hamiltonian} to accept two independently sourced fields
with tunable weights,
\begin{equation}
  E(\mathbf{s}) = -\sum_{\langle i,j \rangle} J_{ij}\, s_i s_j
  - \sum_i \left(\lambda_{pol}\, h_i^{pol} + \lambda_{soc}\, h_i^{soc}\right) s_i,
  \label{eq:hamiltonian2}
\end{equation}
which collapses exactly to Eq.~\eqref{eq:hamiltonian} when either
$\lambda_{pol}=0$ or $\lambda_{soc}=0$ -- a genuinely equivalent
generalization of the single-field model, not an approximation to it, since
$\lambda_{pol} h_i^{pol} + \lambda_{soc} h_i^{soc}$ is itself just a single
effective field handed to the same, otherwise unmodified Monte Carlo engine.
Section~\ref{sec:mideplan} uses Eq.~\eqref{eq:hamiltonian2} with $h^{pol}=$
2026's own margin and $h^{soc}=$ the MIDEPLAN field: a 1D scan over
$\lambda_{soc} \in [0,2]$ at $\lambda_{pol}=0$ isolates the social field
cleanly (this is the section's main result), and a single fixed check at
$\lambda_{pol}=2$ (the own-margin field's best-fit weight) with the
peak $\lambda_{soc}$ added on top tests whether the two fields combine --
not a full joint $(\lambda_{pol}, \lambda_{soc})$ grid. The non-circular
political field (Section~\ref{sec:noncircular}) and the GAM field
(Section~\ref{sec:gam}--\ref{sec:cascade}) each instantiate
Eq.~\eqref{eq:hamiltonian2} with $\lambda_{pol}=0$ and the field under test
placed in the $h^{soc}$ slot, unweighted ($\lambda_{soc}=1$), matching the
convention already used for $h=$margin in
Sections~\ref{sec:ablation-canton}/\ref{sec:ablation-distrito}.

\subsection{Monte Carlo dynamics}

Equilibrium configurations at a given social temperature $T$ (a single free
parameter controlling how much thermal noise competes against the coupling
and field terms) are sampled with single-spin-flip Glauber dynamics: at each
step a unit $i$ is chosen and its spin is flipped with probability
$p = 1/(1 + e^{\Delta E_i/T})$, where $\Delta E_i$ is the energy change that
flip would cause. One \emph{sweep} is $N$ such attempts (one per unit, in
random order). Each simulation begins from a random spin configuration,
runs a fixed number of \emph{equilibration} sweeps to let the system settle,
then runs a further number of \emph{measurement} sweeps during which
observables are recorded. A full \emph{temperature scan} repeats this
procedure independently at each of a grid of $T$ values, since -- exactly as
in a real magnet -- the qualitative behavior of the system can change
sharply with temperature, and the value of $T$ that best reproduces the real
map is itself an output of interest, not an input assumption. Two grids are
used across this paper's analyses. The canton-level ablation
(Section~\ref{sec:ablation-canton}) and historical comparison
(Section~\ref{sec:historical}) use $T \in [0.05, 3.5]$, a 24-point grid, with
500 equilibration and 500 measurement sweeps per replicate. The
finite-size-scaling analysis (Section~\ref{sec:fss}) and distrito-level
ablation (Section~\ref{sec:ablation-distrito}) use $T \in [0.05, 3.5]$ as
well but a 32-point grid, with 20{,}000 equilibration and 20{,}000
measurement sweeps per replicate, run on a computing cluster -- the heavier
budget needed for the larger $N=488$ system to equilibrate properly, as
Section~\ref{sec:fss} discusses directly. The second contribution's runs
(Sections~\ref{sec:mideplan}--\ref{sec:cascade}: MIDEPLAN, the non-circular
political field, GAM, and their downstream diagnostics) extend this same
32-point/20{,}000-sweep budget to $T \in [0.05, 5.0]$, a wider upper bound
added to accommodate the counterfactual sweep's own extreme $T=5.0$
measurement (Section~\ref{sec:counterfactual}); consequently, the
geography-only distrito-level baseline is reported at two slightly
different values depending on which grid produced it -- 66.2\% in
Table~\ref{tab:distrito} ($T\in[0.05,3.5]$) versus 67.64\% in
Section~\ref{sec:mideplan} ($T\in[0.05,5.0]$) -- both real best-of-grid
numbers for the identical underlying quantity, differing only in how far
into the high-$T$ range the wider grid extends (both share the same
low-$T$ endpoint). The corresponding best-$T$ also differs between the two
grids (2.83 versus 2.605) for the same reason.
Because every headline alignment/significance figure in this paper is
reported at whichever $T$ in the grid maximizes alignment, these are
best-of-grid statistics rather than results at a single pre-specified $T$.
We report a simple, conservative Bonferroni correction alongside every raw
$p$-value below (raw $p$ times the number of grid points scanned, 24 or 32
depending on the analysis, capped at 1), rather than a more powerful
max-statistic permutation null, since the latter would require rerunning
each full temperature scan many times under label permutation, which we did
not do. Where a figure is pooled across seeds (Section~\ref{sec:observables}),
we apply this correction directly to the \emph{median} of the per-seed raw
$p$-values, as a conservative screening heuristic rather than a formally
derived family-wise-error-rate guarantee for that aggregated quantity --
correcting each seed's raw $p$-value individually before vote-counting
would be the more rigorous alternative, which we did not implement. Reported
corrected values are computed from full, unrounded medians; multiplying a
displayed rounded median by the grid size can therefore appear to disagree
with a displayed corrected value by up to the last digit of rounding (e.g.\
Section~\ref{sec:ablation-canton} reports median $p=0.02637 \times 24 =
0.633$, not the $0.624$ a reader would get from the rounded display
$0.026 \times 24$).

\subsection{Observables}
\label{sec:observables}

Alignment with the real map is scored with the fraction of units whose
simulated and empirical spins agree, using a label-symmetric variant
(agreement under either global labeling, $\max$ of the two) whenever $h=0$,
for the reason given above. Reported $\pm$ figures throughout this paper are
one sample standard deviation of that alignment across the pooled seed
replicates at the same $T$, not a standard error or confidence interval.
Two standard thermodynamic response functions are tracked as functions of
$T$: the specific heat $C = \mathrm{Var}(E)/(NT^2)$ and the magnetic
susceptibility $\chi = N\,\mathrm{Var}(m)/T$, where $m$ is the mean spin.
Both are expected to peak sharply at a genuine phase transition and are the
standard first signature searched for one. Where a symmetric order
parameter is available ($h=0$), the Binder cumulant
$U_4 = 1 - \langle m^4\rangle / (3\langle m^2\rangle^2)$ \citep{binder1981}
is also computed; unlike $\chi$ and $C$, $U_4$ curves at two different
system sizes $N$ are expected to cross at a single, size-independent
temperature if a genuine critical point exists, which makes it the more
reliable diagnostic used in Section~\ref{sec:fss}. Statistical significance
of a model's best-fit alignment against the trivial majority-class baseline
is assessed with McNemar's exact test \citep{mcnemar1947} -- which asks
whether the model and the baseline disagree with the true map in
significantly different sets of units, using only the units where exactly
one of the two is right -- on the paired disagreements between the model's
prediction and that baseline, following the validation approach used in
\citep{korbel2026}. Spatial autocorrelation of the empirical vote pattern
itself (independent of any simulation) is measured with Moran's $I$
\citep{moran1950}, using a 999-permutation test for significance.

McNemar's test assumes the per-unit paired outcomes are independent, which
is not strictly true here: cantons and distritos are coupled by the very
adjacency structure this paper's model is built around, and the Moran's $I$
values reported in Section~\ref{sec:2018} confirm that empirical vote
patterns are themselves significantly spatially autocorrelated. Spatial
autocorrelation in the compared labels tends to make McNemar's test
anti-conservative (its $p$-values understate true uncertainty); this is a
known pitfall for paired classification-accuracy comparisons on spatially
structured data more generally \citep{karasiak2021}. We therefore
supplement McNemar's test everywhere below with a \emph{spatial block
permutation test}, a restricted-randomization design in the sense of
\citep{besagclifford1989}: rather than randomizing at the level of
individual units, it only randomizes the sign of each unit's
discordant/concordant outcome within spatial blocks (each canton's parent
province, or each distrito's parent canton), so units that share local
spatial information move together under the null instead of being treated
as independent draws. This is a weaker (more conservative) test by
construction -- with only a handful of provinces as blocks at canton
resolution, it can only resolve $p$-values as fine as roughly
$2/2^{n_{\text{blocks}}}$ -- so we report both tests' results rather than
picking one as final. Every spatial-block $p$-value below is estimated from
999 Monte Carlo sign-flip draws (matching the Moran's $I$ test's
999-permutation budget above), not exact enumeration even where the block
count would make that feasible; the resulting Monte Carlo standard error is
$\sqrt{p(1-p)/999} \approx 0.005$--$0.015$ over the range of $p$ values
reported below.
Separately, wherever we summarize significance across the pooled seed
replicates (Sections~\ref{sec:ablation-canton}--\ref{sec:ablation-distrito}),
we report the fraction of individual seeds significant at $p<0.05$ and the
median $p$-value across seeds rather than a formal combined-evidence
statistic (e.g.\ Fisher's or Stouffer's method); this vote-counting-style
summary is a simpler but less powerful way to synthesize repeated
significance tests than formal $p$-value combination, and we use it for
transparency (each seed's result stays individually visible) rather than
because it is the strongest available approach.

\subsection{Why many independent simulations, not one}

Every result in this paper pools $8$--$16$ independent Monte Carlo replicates
(different random seeds) per temperature before computing any observable,
rather than reporting a single run; replicate $k$'s seed is a fixed base
seed offset by $k$ times a large stride, so replicates are independent
draws from a single reproducible seed sequence rather than shared or
arbitrarily chosen. This is not a stylistic preference: in
earlier stages of this project, single-seed alignment gaps and
susceptibility peaks that looked like clean, publishable signals reversed
sign or vanished entirely once replaced with a pooled multi-seed estimate
with proper uncertainty bars (Section~\ref{sec:ablation-canton}). Pooling
introduces its own subtlety worth stating plainly: at low temperature,
independent chains can each freeze into a \emph{different} locally stable
configuration rather than all finding the same one, and because both $\chi$
and $C$ divide by $T$, that between-chain disagreement can be amplified into
an apparent divergence at the low-$T$ edge of a scan that is not a real
thermodynamic effect. A genuine critical point is an interior peak in the
pooled curve, not a monotonic blow-up toward $T \to 0$; every temperature
scan in this paper is read with that distinction in mind.

\section{Results}
\label{sec:results}

\subsection{An illustrative snapshot: simulated versus real 2026 map}

Figure~\ref{fig:map} shows a single simulated configuration at its best-fit
temperature, side by side with the real 2026 canton-level result, purely to
give an intuitive sense of what ``alignment with the real map'' means before
the more careful pooled analyses that follow. This particular snapshot uses
a single Monte Carlo seed and is illustrative only; all quantitative claims
in this paper use the pooled multi-seed procedure described above.

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/map_comparison_real.png}
  \caption{Illustrative comparison of the real 2026 canton-level result
  (coalition split) against a single simulated configuration at its
  best-fit temperature. Single-seed snapshot for visual intuition only;
  see Section~\ref{sec:ablation-canton} for the pooled, statistically
  characterized result.}
  \label{fig:map}
\end{figure*}

\subsection{How much of the map does geography alone explain? (canton-level ablation)}
\label{sec:ablation-canton}

At canton resolution ($N=84$), the majority-class baseline for the 2026
coalition split is 60.7\% (51 of 84 cantons won by Pueblo Soberano). Pooling
$8$ seeds per temperature, the geography-only model ($h=0$) achieves a
best-fit label-symmetric alignment of $67.6\% \pm 5.5\%$; adding the real
vote margin as a field improves this to only $68.8\% \pm 3.5\%$ -- a gap of
$+1.2$ percentage points that sits well within the two runs' overlapping
standard-deviation bands. This overlap check is a conservative heuristic,
not a direct paired test of the two models' predictions against each other;
we therefore also ran the two arms' own best-fit configurations directly
against each other with \texttt{spatial\_block\_permutation\_test\_paired}

exec
/bin/bash -lc "sed -n '621,1040p' manuscript/main.tex" in /home/tomas/research-current/IsingCR
 succeeded in 96ms:
(province blocks, $n_{\text{blocks}}=7$, matching the spatial-block test's
canton-level granularity elsewhere in this paper), paired seed-by-seed
across the 8 pooled replicates: median $p=0.678$, significant in 0 of 8
seed-pairs -- a direct head-to-head comparison confirms the two arms'
predictions are not distinguishable from each other at canton resolution,
consistent with the baseline-referenced picture above. McNemar's test
against the trivial baseline sharpens the picture from a different angle:
the geography-only model's
best-$T$ configuration is significantly different from the majority-class
baseline in only 2 of 8 seeds (median $p=0.08740$; spatial-block median
$p=0.449$), while geography-plus-margin reaches significance in 5 of 8
(median $p=0.02637$; spatial-block median $p=0.240$) -- so adding the field
helps the model's individual-seed reliability more than it moves the
headline point estimate, though neither run's McNemar significance survives
Bonferroni correction for the 24-point temperature grid (corrected
$p=1.000$ and $p=0.633$ respectively, i.e.\ $0.08740\times24$ capped at $1$
and $0.02637\times24$), and neither survives the
spatially-aware test even before that correction. Neither run shows an interior peak in $\chi$ or
$C$: both curves rise monotonically as $T \to 0$, the low-temperature
pooling artifact described in Section~\ref{sec:model} rather than evidence
of a genuine transition. Figure~\ref{fig:ablation} shows all three curves
for both runs.

An earlier, single-seed version of this same comparison had reported a
larger $+2.4$ percentage point gap and a clean interior susceptibility
peak; both turned out to be artifacts of using one Monte Carlo chain rather
than a pooled estimate, and are the reason every subsequent analysis in this
paper uses the pooled procedure by default.

Is this near-zero canton-level gap itself an artifact of the specific
three-party coalition construction (Section~\ref{sec:data})? We reran the
same ablation under the winner-vs-runner-up binarization used in
Section~\ref{sec:historical} and the distrito-level cross-check of
Section~\ref{sec:ablation-distrito} (Pueblo Soberano vs. Liberaci\'on
Nacional), same $N=84$ network and budget. The gain from adding $h$ was
$+2.5$ percentage points ($76.5\% \pm 6.2\%$ to $79.0\% \pm 2.2\%$ against a
75.0\% baseline) -- a different binarization moves the point estimate
somewhat, but it remains small and, if anything, less individually
significant than the coalition-split result (McNemar median $p=0.363$, 0 of
8 seeds significant, versus coalition-split's $p=0.026$, 5 of 8). The
canton-level near-null conclusion is therefore not an artifact of the
three-party coalition choice specifically: both binarizations tested give a
small, largely non-significant gain from adding $h$ at this granularity.

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/ablation.png}
  \caption{Canton-level ablation for the 2026 election ($N=84$, coalition
  split, 8 pooled Monte Carlo seeds per temperature). Left: label-symmetric
  alignment with the real map vs.\ temperature, geography only ($h=0$, gray)
  vs.\ geography plus predisposition ($h=$margin, red), against the 60.7\%
  majority-class baseline (dotted) and 50\% chance level (dashed). Center:
  susceptibility. Right: specific heat.}
  \label{fig:ablation}
\end{figure*}

\subsection{Does the same model work across election cycles?}
\label{sec:historical}

Figure~\ref{fig:realmaps} shows the real canton-level winner-vs-runner-up
result being modeled in each of the three elections. Qualitatively, 2022 and
2026 look similar: the eventual winner sweeps almost the entire country
except for a compact cluster of cantons around the capital. 2018 looks
different in kind, not just degree -- the winner's support is itself
concentrated in and around the capital metropolitan area (GAM) while the
runner-up holds most of the periphery, a spatial pattern closer to a
contiguous split than a sweep-with-an-enclave. This visual contrast
foreshadows Section~\ref{sec:2018}'s explanation of why 2018 behaves
differently under the model.

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/historical_maps.png}
  \caption{Real canton-level results, winner vs.\ runner-up binarization
  (the same binarization used throughout this subsection), all three
  elections. Gray cantons have no matching result row for that election (see
  Section~\ref{sec:data}) and are excluded from that election's $N$ in
  Table~\ref{tab:historical}.}
  \label{fig:realmaps}
\end{figure*}

Repeating the same canton-level fitting procedure, with the winner-vs-runner-up
binarization, across all three available elections produces
Table~\ref{tab:historical}. 2022 and 2026 both show a positive best-fit
alignment gap over their respective majority-class baselines, robust to the
1-sigma uncertainty band; 2018 does not, and unlike the coalition-split
canton ablation's originally reported gap in Section~\ref{sec:ablation-canton}
(which shrank from $+2.4$ to $+1.2$ points once pooled), this null is not an
artifact of pooling: $76.4\% \pm 0.4\%$ is a tight estimate barely
distinguishable from the 76.5\% baseline itself. McNemar's
test tempers the 2022/2026 reads further, in the same direction as the
canton ablation above: only 2 of 8 seeds for 2022 and 1 of 8 for 2026 reach
individual significance at $p<0.05$ (median $p=0.35$ and $0.37$; Bonferroni
correction for the 24-point grid leaves neither below $p=1.000$; the
spatial-block test gives median $p=0.57$ and $p=0.64$). This is
consistent with $N\!\sim\!84$ discordant-pair tests having genuinely limited
power to detect a 4--6 percentage point effect (the size of the gaps in this
table specifically; Section~\ref{sec:ablation-distrito} later reports a
distrito-level, $N=488$ effect roughly twice as large), not necessarily
evidence the effect is illusory -- but it means the historical result should be reported
as ``2018 is a confident null; 2022 and 2026 show a similarly sized positive
point estimate that individual-seed significance testing cannot yet confirm,''
not as an unqualified ``2022 and 2026 clearly beat baseline.''
Figure~\ref{fig:historical} shows the full temperature dependence underlying
these best-fit values.

\begin{table*}[htbp]
\centering
\caption{Historical comparison, canton level, winner vs.\ runner-up
binarization, 8 pooled Monte Carlo seeds per election.}
\label{tab:historical}
\begin{tabular}{lccccc}
\toprule
Election & $N$ & Baseline & Best alignment & 1-$\sigma$ beats baseline? & McNemar (median $p$, seeds sig.) \\
\midrule
2018 (runoff)  & 81 & 76.5\% & $76.4\% \pm 0.4\%$ & No  & $p=1.00$, 0/8 \\
2022 (runoff)  & 82 & 64.6\% & $71.0\% \pm 4.1\%$ & Yes & $p=0.35$, 2/8 \\
2026 (round 1) & 84 & 75.0\% & $79.0\% \pm 2.2\%$ & Yes & $p=0.37$, 1/8 \\
\bottomrule
\end{tabular}
\end{table*}

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/historical_comparison.png}
  \caption{Best-fit alignment, susceptibility, and specific heat vs.\
  temperature for all three elections, canton level, winner-vs-runner-up
  binarization, 8 pooled seeds each.}
  \label{fig:historical}
\end{figure*}

\subsection{Why is 2018 different?}
\label{sec:2018}

Two competing explanations were checked for why 2018 fails to beat its
baseline while 2022 and 2026 do. The first, motivated by the political
science literature on 2018's winning party having an unusually urban,
capital-metropolitan-area (GAM)-concentrated support base
\citep{camachosanchez2025}, was that 2018's real map might simply lack the
geographic clustering the model relies on. This is ruled out directly:
Moran's $I$ on the real adjacency network shows 2018 is in fact the
\emph{most} spatially clustered of the three elections ($I=0.706$,
permutation $p<0.001$), not the least (2022: $I=0.485$; 2026: $I=0.354$;
both also significant at $p<0.01$), on both the binarized outcome and the
continuous margin field.

The actual explanation is energetic rather than structural. Every
election's trivial ``everyone votes for the winner'' configuration has
lower energy under Eq.~\eqref{eq:hamiltonian} than that election's true map
-- expected, since it is the null the model is scored against -- but the
size of that gap, normalized per unit, differs sharply: 2018's true map
costs 1.13 energy units per canton relative to the trivial state, versus
0.77 for 2022 and 0.59 for 2026 -- 47\% and 92\% higher, respectively. A temperature
scan that starts from a random configuration is a search that gravitates
toward whichever basin the energy landscape favors; when the true minority
pattern is this much more energetically disfavored relative to the trivial
alternative, a random-start search is correspondingly less likely to ever
find its way there within a finite number of sweeps -- exactly what the
historical comparison observes. This is not because 2018's true pattern is
itself unstable: a zero-temperature relaxation started \emph{at} the true
map and pooled across 8 seeds (T=0 Glauber dynamics is not fully
deterministic -- ties are still broken randomly) keeps $90.1\% \pm 0.0\%$ of
the 2018 map intact after 100 sweeps, actually the most stable of the three
elections ($85.4\% \pm 0.0\%$ for 2022, $80.5\% \pm 4.3\%$ for 2026). The
problem is specifically that nothing in a random-start search guides it
into that basin in the first place. Figure~\ref{fig:2018} summarizes both
diagnostics.

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/2018_anomaly.png}
  \caption{Left: energy cost per canton of the true map relative to the
  trivial all-majority state, all three elections -- higher means more
  energetically disfavored under a random-start search. Right: Moran's $I$
  of the empirical spin pattern, all three elections, all significant at
  $p<0.01$ -- 2018 is the most spatially clustered, ruling out ``lack of
  geographic structure'' as the explanation.}
  \label{fig:2018}
\end{figure*}

\subsection{Is there a critical point?}
\label{sec:fss}

A standard way to look for a genuine critical point independent of system
size is a size-independent crossing of the Binder cumulant $U_4(T)$ computed
at two or more different $N$; canonical finite-size-scaling practice
typically uses three or more sizes to confirm that a crossing is a
consistent, size-independent property rather than an incidental feature of
one specific curve pair, since any two non-identical curves generically
intersect somewhere. Costa Rica's administrative hierarchy gives us only two
real granularities to work with -- canton ($N=84$) and distrito ($N=488$) --
for the same election and the same real adjacency structure; we do not have
a natural third real system size, so the analysis below should be read as a
two-size check rather than a full convergence study. This analysis is run at
$h=0$ deliberately, since the standard interpretation of a $U_4$ crossing
assumes a symmetric order parameter.

An initial run (8 pooled seeds, 500 equilibration and 500 measurement
sweeps) found 6 crossings across the scanned range -- already suspicious,
since a genuine transition produces exactly one -- but was inconclusive
rather than a confirmed null: the $N=488$ curve dipped below the
physically valid range for $U_4$ ($[0, 2/3]$ at true equilibrium) at
several temperatures, indicating the larger system was not equilibrating
properly at that sweep budget, a standard finite-size-scaling complication
(larger systems generically need longer runs to equilibrate at fixed
temperature).

This was resolved with a substantially heavier re-run on a computing
cluster: 16 pooled seeds, 20{,}000 equilibration and 20{,}000 measurement
sweeps (40$\times$ the original budget), across 32 temperatures. Under this
budget, \emph{zero} $U_4$ values fall outside the valid range at either
system size, confirming the earlier dips were indeed an equilibration
artifact rather than a sign of ambiguous physics. With equilibration no
longer in question, the crossing count is 5 across the scanned range
(Figure~\ref{fig:fss}). We read this qualitatively as more consistent with
noise than with a genuine transition, since a real transition is expected to
produce a single, consistent crossing rather than several scattered ones,
but we have not fit a formal null distribution for the expected crossing
count under noise alone, so this reading is not a quantified statistical
test. The finding therefore upgrades from ``inconclusive'' to
\textbf{no critical point found} in the scanned temperature range, at either
of the two spatial resolutions examined, for the 2026 election -- consistent
with every other pooled scan in this paper, none of which shows an interior
susceptibility or specific-heat peak once low-temperature pooling artifacts
are accounted for. Given the two-size limitation above, this should be read
as no evidence of a crossing between these two specific granularities within
the scanned range, not as a claim that no transition could exist at any
system size or temperature.

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/finite_size_scaling_heavy.png}
  \caption{Binder cumulant $U_4$ vs.\ temperature, canton ($N=84$) and
  distrito ($N=488$) geometry, $h=0$, 2026 coalition split. 16 pooled
  seeds, 20{,}000+20{,}000 sweeps. Shaded band marks the physically valid
  $U_4$ range $[0, 2/3]$; both curves stay within it throughout, confirming
  proper equilibration. Vertical lines mark the 5 crossings found, read as
  noise rather than a genuine transition.}
  \label{fig:fss}
\end{figure*}

\subsection{Zooming in: the distrito-level ablation}
\label{sec:ablation-distrito}

Section~\ref{sec:ablation-canton}'s canton-level result -- that adding each
unit's own predisposition barely moves alignment beyond what geography alone
achieves -- aggregates over units that can themselves contain substantial
internal heterogeneity; a single canton in Costa Rica can span both dense,
centrally located distritos and remote outlying ones. Costa Rica's own
political-science literature has documented real geographic heterogeneity in
party support at exactly this finer scale
\citep{cascantematamoros2006,camachosanchez2025}, which motivates repeating
the ablation one administrative level down, at $N=488$ distritos, using the
same heavy Monte Carlo budget validated in Section~\ref{sec:fss} (16 pooled
seeds, 20{,}000+20{,}000 sweeps, 32 temperatures).

The result reverses the canton-level conclusion, though how confidently
depends on which significance test is used, discussed below. Against a
66.9\% majority-class baseline (329 of the 492 distritos nationally, before
the 4 exclusions of Section~\ref{sec:data}; recomputed directly on the
$N=488$ post-exclusion sample actually used below, the baseline is
$67.0\%$, 327 of 488 -- a $0.1$ percentage-point difference immaterial to
every gap and significance figure reported in this section, so we retain
the pre-exclusion figure used throughout the underlying Monte Carlo runs
for consistency with Figure~\ref{fig:distrito} and Table~\ref{tab:distrito}),
the geography-only model
achieves $66.2\% \pm 6.4\%$ best-fit alignment -- statistically
indistinguishable from, and nominally \emph{below}, the baseline, and not
significant in its own right (McNemar median $p=0.180$, only 4 of 16 seeds
individually significant). Adding the real distrito-level vote margin
raises best-fit alignment to $74.8\% \pm 4.2\%$, a gain of $+8.7$ percentage
points (the full-precision values behind Table~\ref{tab:distrito}'s rounded
66.2\%/74.8\% are 66.16\% and 74.85\%) that is substantially larger than the
canton-level result's $+1.2$ points, and by McNemar's test alone strongly
significant: median $p=0.0009$, with 12 of 16 seeds individually
significant at $p<0.05$. Unlike the canton-level ablation, this comparison
does not rest only on each arm's own significance against the trivial
baseline: a direct paired test of the two arms' best-fit configurations
against each other (\texttt{spatial\_block\_permutation\_test\_paired},
canton blocks, $n_{\text{blocks}}=84$, paired seed-by-seed across the 16
pooled replicates) gives median $p=0.020$, significant in 10 of 16
seed-pairs -- geography-plus-margin's predictions are directly, and
spatially-conservatively, distinguishable from geography-alone's, not only
each arm's distinguishability from the majority-class baseline separately.

That McNemar reading does not survive replacing McNemar's test with the
spatially-aware alternative introduced in Section~\ref{sec:observables}. We
reran both arms at their already-identified best-fit temperature with an
independent set of 16 seeds and computed both a Bonferroni correction for
the 32-point temperature grid and the spatial block permutation test
(blocks = each distrito's parent canton, 84 blocks). For arm B
(geography+margin): McNemar median $p=0.0001$ on this independent
replicate -- consistent with the original run's strong McNemar reading,
Bonferroni-corrected to $p=0.0030$, still comfortably significant -- but the
spatial block permutation test gives median $p=0.064$, \emph{not}
significant at the conventional 0.05 threshold, and $p=1.000$ once also
Bonferroni-corrected. For arm A (geography only): already weak under
McNemar (Bonferroni-corrected $p=0.562$), and not significant under the
spatial-block test either ($p=0.217$, Bonferroni-corrected $p=1.000$).

That single spatial-block $p=0.064$ is itself not a stable number: it
depends on the blocking granularity, which has no principled correct
choice. Sweeping arm B's spatial-block test across three block sizes on a
further independent replicate -- coarser (7 province-level blocks), the
canton-level blocking reported above (84 blocks), and finer (distritos
split into $\sim$165 half-canton blocks) -- gives median $p=0.377$, $0.068$,
and $0.019$ respectively: clearly non-significant, marginal, and
significant, in that order. Finer blocking approaches individual-unit
independence and converges toward McNemar's own (anti-conservative) answer,
which is the expected mechanical behavior of this test, not a flaw in it --
but it means no single spatial-block $p$-value can be reported as \emph{the}
corrected significance level without also specifying, non-arbitrarily, how
coarse the blocks should be, which we do not have a principled way to do.

We therefore ran two further, more direct checks rather than leaning on any
single significance test. First, an $N$/power check: is the distrito-level
effect just a statistical-power artifact of $N=488 \gg 84$? We reran the
same ablation on 10 independent $\sim$80--93-distrito subsamples, each built
from whole randomly-selected cantons merged together (preserving realistic
local adjacency density, unlike an earlier attempt at uniformly-random
individual-distrito sampling, which produced a badly sparse, spatially
incoherent network -- $\sim$40 edges among 84 nodes versus $\sim$140 here --
and is not reported further), using the same 24-point, $T\in[0.05,3.5]$
grid and 500+500-sweep budget as the canton-level ablation (matched $N$
warrants the lighter, canton-scale budget rather than the heavier
distrito-scale one), with 8 pooled Monte Carlo seeds per subsample -- so
each of the 10 per-subsample McNemar figures below is itself already a
pooled, not single-seed, estimate. The gain from adding $h$ averaged
$+10.1\% \pm 2.4\%$ (range $+5.2\%$ to $+13.7\%$) across all 10 independent
subsamples, matching the full-sample $N=488$ effect size closely and never
approaching the near-zero canton-level result -- evidence against a pure
power artifact, since matching $N$ to canton level did not shrink the
effect. Second, a binarization check: is the effect specific to the
particular three-party coalition construction (Section~\ref{sec:data})? We
reran the full distrito ablation under the winner-vs-runner-up binarization
used in Section~\ref{sec:historical} instead. The gain from adding $h$ was
$+11.6$ percentage points ($69.7\% \pm 8.8\%$ to $81.3\% \pm 1.2\%$ against a
79.1\% baseline) -- again close to the coalition-split effect size -- but
its McNemar significance was markedly weaker (median $p=0.087$, 5 of 16
seeds significant, versus the coalition split's $p=0.0009$, 12 of 16).
Table~\ref{tab:robustness} summarizes these checks alongside the spatial
block permutation sensitivity sweep above.

\begin{table*}[htbp]
\centering
\caption{Robustness of the distrito-level $h$-effect: three effect-size
checks (rows below) plus a fourth, the spatial block permutation
sensitivity sweep, which does not itself produce a single effect-size
estimate and is discussed in prose above ($p=0.019$--$0.377$ across
blocking granularities). Effect size = best-fit alignment gain from adding
$h$ over geography alone. McNemar $p$ is reported as-is, uncorrected, for
comparability across rows; see text for why it should not be read as a
calibrated significance level on its own.}
\label{tab:robustness}
\begin{tabular}{lccc}
\toprule
Check & $N$ & Effect size & McNemar $p$ (seeds sig.) \\
\midrule
Full sample, coalition split (headline) & 488 & $+8.7$pp & $0.0009$ (12/16) \\
Contiguous subsample avg., coalition split & $\sim$84 & $+10.1\% \pm 2.4\%$ & median $0.199$ (2/10 sig.) \\
Full sample, winner-vs-runner-up & 488 & $+11.6$pp & $0.087$ (5/16) \\
\bottomrule
\end{tabular}
\end{table*}

Read together, these checks separate two questions that a single
significance test conflates. Is the effect \emph{size} real -- i.e., not an
artifact of sample size or of the specific binarization chosen? The answer
looks like yes: $+8.7$ to $+11.6$ percentage points, consistently, across a
resolution-matched subsample and an entirely different binarization. Is the
effect formally \emph{confirmed} at conventional significance, independent
of which reasonable methodological choice is made? The answer is no: McNemar
alone says yes at $p=0.0009$; the same test under an alternative
binarization says only $p=0.087$; a spatially-aware alternative to McNemar
ranges from clearly non-significant to significant depending on an
essentially arbitrary blocking choice; and in the $N$-matched check, where
each subsample is itself already pooled across 8 seeds, only 2 of the 10
subsamples individually reach significance at $p<0.05$ (median $p$ across
subsamples $=0.199$), even though their gains are consistently positive
(range $+5.2\%$ to $+13.7\%$, none near zero). This paper's central new
finding should therefore be read as a real, reproducible effect size whose
formal statistical confirmation is currently sensitive to test and
binarization choices we do not have a principled way to adjudicate between,
not as an unconditionally settled result.

As a final, cruder cross-check, we also normalized each granularity's raw
gap by its own headroom to 100\% alignment, since the canton run ($N=84$,
baseline 60.7\%, 39.3 points of headroom) and distrito run ($N=488$,
baseline 66.9\%, 33.1 points of headroom) differ in how much room the model
has to improve on the baseline as well as in $N$: $+1.2/39.3 \approx 3\%$ of
headroom at canton level versus $+8.7/33.1 \approx 26\%$ at distrito level --
still close to an order-of-magnitude difference, consistent with the direct
subsample check above rather than contradicting it. Table~\ref{tab:distrito}
summarizes the original two runs; Figure~\ref{fig:distrito} shows the full
temperature dependence.

\begin{table*}[htbp]
\centering
\caption{Distrito-level ablation, 2026 coalition split ($N=488$), 16 pooled
Monte Carlo seeds, 20{,}000+20{,}000 sweeps, 32 temperatures. Baseline:
66.9\%.}
\label{tab:distrito}
\begin{tabular}{lcccc}
\toprule
Run & Best alignment & $T$ at best & McNemar (median $p$) & Seeds sig.\ at 0.05 \\
\midrule
A: geography only ($h=0$)        & $66.2\% \pm 6.4\%$ & 2.83 & 0.180  & 4/16  \\
B: geography + margin ($h=$margin) & $74.8\% \pm 4.2\%$ & 0.61 & 0.0009 & 12/16 \\
\bottomrule
\end{tabular}
\end{table*}

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/distrito_ablation.png}
  \caption{Distrito-level ablation for the 2026 election ($N=488$, coalition
  split, 16 pooled seeds). Left: label-symmetric alignment vs.\ temperature,
  geography only (gray) vs.\ geography plus predisposition (red), against
  the 66.9\% majority-class baseline (dotted). Center: susceptibility.
  Right: specific heat.}

exec
/bin/bash -lc "sed -n '1041,1460p' manuscript/main.tex" in /home/tomas/research-current/IsingCR
 succeeded in 0ms:
  \label{fig:distrito}
\end{figure*}

In short: at canton resolution, pure geographic contagion already explains
nearly everything the model can explain about the real map, and each unit's
own political lean adds essentially nothing measurable on top of it; at
distrito resolution, geographic contagion alone explains comparatively
little, and predisposition is associated with a substantially larger gain in
alignment ($+9$ to $+12$ percentage points) that reproduces across a
resolution-matched subsample and an alternative binarization, but whose
formal statistical confirmation shifts between clearly significant and not
significant depending on which reasonable test or binarization is used.
Canton-level aggregation was, at minimum, masking a real effect size; whether
it was also masking an unconditionally statistically confirmable one is not
yet settled by this paper.

\subsection{A second predisposition field: socioeconomic development}
\label{sec:mideplan}

The own-margin field used throughout Sections~\ref{sec:ablation-canton}--\ref{sec:ablation-distrito}
has a property worth stating precisely rather than leaving as a background
assumption: at distrito resolution, $\mathrm{sign}(h_i)$ matches 2026's
empirical label $s_i^{\text{emp}}$ on 487 of 488 nodes (99.8\%) by
construction, since both are derived from the same vote count. A field this
close to its own label risks reproducing the real map at large enough
$\lambda$ without that reproduction reflecting a genuine predisposition
effect. We checked this directly: scanning $\lambda_{pol} \in [0,8]$ with
$\lambda_{soc}=0$ in Eq.~\eqref{eq:hamiltonian2}, best-fit alignment climbs
monotonically from 67.64\% to 92.70\% -- a substantial rise toward, though
not full convergence with, the field's own 99.8\% sign-agreement ceiling --
and the best-fit temperature drifts sharply downward (from $T=2.605$ to
$T=0.369$), exactly the signature of the
field simply overwhelming the coupling term at large $\lambda$. We checked
this is not the low-temperature between-chain disagreement artifact of
Section~\ref{sec:model} (which predicts \emph{more} seed-to-seed
disagreement in this regime): at a normal grid point ($\lambda_{pol}=2$,
$T=0.848$) the 16 pooled seeds have alignment standard deviation 2.5
percentage points; at the extension's low-$T$ tail ($\lambda_{pol}=8$,
$T=0.369$) it is 0.6 points -- \emph{tighter}, not looser,
agreement, consistent with field-dominance rather than non-convergence. We do
not report the extension scan as a finding for this reason; it is a
methodological check ruling out an artifact, not a result.

This motivates testing a field with no such construction issue. MIDEPLAN's
composite IDS 2023 score (Section~\ref{sec:data-mideplan}) is used as
$h^{soc}$ in Eq.~\eqref{eq:hamiltonian2} with $\lambda_{pol}=0$ (isolating the
social field cleanly) and $h^{pol}$ unused in this section. At the
distrito-level $N=488$ network, scanning $\lambda_{soc} \in [0,2]$: 2026's
geography-only baseline (67.64\%, McNemar $p=0.199$, Bonferroni-corrected
$p=1.000$, against the trivial majority baseline) rises to a peak of
74.42\% at $\lambda_{soc}=1.5$ ($+6.78$ percentage points, McNemar
$p=0.015$, Bonferroni-corrected $p=0.48$ for the 32-point $T$ grid --
not significant once corrected against the trivial baseline this way).
A direct paired test between geography-only and this peak configuration
(\texttt{spatial\_block\_permutation\_test\_paired}, canton blocks
$n_{\text{blocks}}=84$, 16 seed-pairs, matching
Section~\ref{sec:ablation-distrito}'s methodology) is not itself a
best-of-grid statistic (each arm is evaluated once, at its own
already-identified best-fit $T$) and so needs no such correction: it
gives median $p=0.058$, significant in 8 of 16 seed-pairs -- borderline,
not below the conventional 0.05 threshold on the median but close, and
half the individual seed-pairs do clear it, a separate and more
favorable read than the corrected McNemar figure above. Repeating the identical procedure for the
2022 runoff (winner-vs-runner-up, $N=483$) gives a much weaker point estimate
($+1.13$pp at $\lambda_{soc}=0.5$, geography-only 62.46\% to 63.59\%) and a
clean null on the direct paired test (median $p=0.405$, 0 of 16 seed-pairs
significant). The socioeconomic field's contribution, unlike the distrito
margin effect of Section~\ref{sec:ablation-distrito}, is specific to 2026, not
a general property replicated across election cycles. Adding the social field
on top of the best-fit political weight ($\lambda_{pol}=2$) gives $+0.0$pp in
both years -- the political field alone already saturates what the model
captures once $\lambda_{pol}$ is large enough to be informative without yet
being in the tautological regime described above.

\subsection{Which axis carries it?}
\label{sec:mideplan-axes}

MIDEPLAN's composite score blends five published sub-dimensions
(Section~\ref{sec:data-mideplan}). We repeated the identical single-field
procedure above ($\lambda_{pol}=0$, $\lambda_{axis}=1.5$ -- the composite's own
peak weight, for direct comparability) for each axis separately, at both
elections, testing whether the composite's borderline 2026 signal is diffuse
across all five or concentrated in one or two. Table~\ref{tab:mideplan-axes}
reports the results, with a Bonferroni correction applied to the significance
threshold ($\alpha = 0.05/5 = 0.01$ per axis) since testing five axes is five
hypothesis tests.

\begin{table*}[htbp]
\centering
\caption{MIDEPLAN axis decomposition, distrito level, $\lambda_{pol}=0$,
$\lambda_{axis}=1.5$, 16 pooled seeds. Paired $p$ is the direct paired test
against geography-only (canton blocks, $n_{\text{blocks}}=84$), matching
Section~\ref{sec:mideplan}'s methodology; Bonferroni threshold
$\alpha=0.01$ per axis.}
\label{tab:mideplan-axes}
\begin{tabular}{lcccccc}
\toprule
& \multicolumn{3}{c}{2026} & \multicolumn{3}{c}{2022} \\
Axis & Alignment & Paired $p$ & Seeds sig. & Alignment & Paired $p$ & Seeds sig. \\
\midrule
Educaci\'on & 76.18\% & 0.038 & 9/16 & 62.66\% & 0.470 & 2/16 \\
Econ\'omico & 74.88\% & 0.050 & 8/16 & 62.45\% & 0.395 & 3/16 \\
Salud       & 75.00\% & 0.055 & 7/16 & 63.48\% & 0.481 & 3/16 \\
Seguridad   & 70.65\% & 0.617 & 3/16 & 65.59\% & 0.345 & 3/16 \\
Participa   & 64.37\% & 0.252 & 2/16 & 63.46\% & 0.608 & 1/16 \\
\bottomrule
\end{tabular}
\end{table*}

No single axis individually clears the Bonferroni-corrected threshold, so this
is not a single cleaner result than the composite. But the pattern is
informative: educaci\'on, econ\'omico, and salud -- a mutually correlated
``development'' cluster in a free correlation check run before any Monte
Carlo (pairwise $r=0.51$--$0.69$) -- cluster in a borderline $p=0.038$--$0.055$
band among themselves, just outside which sits the composite's own paired
$p=0.058$ (Section~\ref{sec:mideplan}), with gaps between all four smaller
than this study's own measured seed-to-seed noise floor ($\sim$0.6--2.5
percentage points standard deviation, Section~\ref{sec:mideplan}), so none
of the four is individually distinguishable from the others. Seguridad and participaci\'on
show essentially no signal ($p=0.62$, $p=0.25$); participaci\'on's own
best-fit alignment (64.37\%) is in fact \emph{below} the geography-only
baseline (67.64\%) despite non-trivial raw correlation with the political
field ($r=-0.55$), illustrating that correlation with a raw covariate does not
guarantee the Monte Carlo dynamics translate it into better classification.
2022 replicates the composite's clean null for every axis, no exceptions.
The composite's borderline 2026 signal is carried by general socioeconomic
development, not by security or civic participation specifically, but that
development signal is itself diffuse across three correlated dimensions
rather than concentrated in one.

\subsection{Testing the non-circular political field}
\label{sec:noncircular}

Section~\ref{sec:data-political} motivates and constructs a field built
entirely from the 2022 runoff, applied to predict 2026 -- sharing no vote
information with the outcome it predicts, unlike every field used so far. A
free correlation check found this promising ($r=0.70$ with 2026's own
margin, $r=0.57$ with the 2026 outcome, comparable in magnitude to
MIDEPLAN's composite). Run through Eq.~\eqref{eq:hamiltonian2} with
$\lambda_{pol}=0$ and this field placed in the $h^{soc}$ slot at
$\lambda_{soc}=1$ (no weighting, matching Section~\ref{sec:ablation-distrito}'s
Run B convention), the result is more modest: best-fit alignment 69.79\% at $T=2.924$ (versus 67.64\% for
geography-only), a $+2.15$ percentage-point gain, McNemar $p=0.265$ against
the trivial baseline. The direct paired test against geography-only gives
median $p=0.260$, significant in only 5 of 16 seed-pairs -- weaker than the
MIDEPLAN composite and every individual development-cluster axis above,
despite the stronger raw correlation.

The gap between correlation and Monte Carlo performance is explained by a
direct check: $\mathrm{sign}$(2022 runoff margin) matches 2026's actual
winner on only 79.1\% of distritos -- the real ceiling on what this field can
deliver, versus the circular own-2026-margin field's 99.8\%
(Section~\ref{sec:mideplan}). About one in five distritos changed which side
of the political divide it was on between the 2022 runoff and 2026's first
round, even though it is nominally the same movement continuing in power;
the field is also weaker in raw magnitude (standard deviation 0.167 versus
0.280 for the own-margin field), compounding the effect. This is a
reportable finding in its own right: political loyalty for the same movement
was not as spatially stable from 2022 to 2026 as a ``same coalition
returning'' narrative would suggest -- suggesting factors other than raw
historical partisan continuity, whether geographic or specific to this
election cycle, played a larger role, though this paper does not isolate or
test any such cycle-specific covariate directly.

\subsection{Capital-region membership (GAM)}
\label{sec:gam}

Gran \'Area Metropolitana membership (Section~\ref{sec:data-gam}) is, by a
wide margin, the strongest field tested in this paper beyond the own-margin
field itself, for 2026 (the 2022/canton-level caveats follow below). A free
correlation check already suggested this before any
Monte Carlo: $r=-0.589$ with 2026's outcome ($r=-0.653$ with 2026's own
margin), and, unlike MIDEPLAN's essentially null 2022 read, still clearly
non-zero for 2022 ($r=-0.277$ with the outcome, $r=-0.387$ with 2022's own
margin). The underlying magnitude is large: in 2026, only 31.7\% of GAM
distritos are on the leading side versus 88.7\% of periphery distritos (a
57.0 percentage-point gap); in 2022, GAM is an even split (50.0\%) versus
76.9\% in the periphery (26.9 points) -- 2026's divide is roughly double
2022's.

Run through Eq.~\eqref{eq:hamiltonian2} with $\lambda_{pol}=0$ and this field
in the $h^{soc}$ slot at $\lambda_{soc}=1$ ($h_i=+1$ if GAM else $-1$) --
unweighted, matching the original own-margin-field convention, not
$\lambda$-optimized the way MIDEPLAN's peak was (Section~\ref{sec:mideplan}),
so this comparison is not fully controlled for optimization budget; GAM's
un-optimized result below already exceeds MIDEPLAN's own optimized peak by
a wide margin, but a $\lambda_{soc}$ scan for GAM was not run and could in
principle move its own number further: 2026
best-fit alignment reaches 81.07\% at $T=1.008$, a $+13.4$
percentage-point gain over the 67.64\% geography-only baseline, McNemar
$p\approx0$ (remains $\approx0$ after the 32-point Bonferroni correction).
The direct paired test against geography-only gives median
$p=0.0005$, significant in 15 of 16 seed-pairs -- the most decisive result of
any field tested in this paper, including the own-margin field. 2022 does
not replicate this: 67.16\% at the same $T$ (a $+4.7$pp gain over its 62.46\%
baseline), paired median $p=0.239$, only 4 of 16 seed-pairs significant --
the same pattern as every other non-circular field tested above,
2026-specific rather than a general property. The best-fit temperature drop
from geography-only's $T=2.605$ to GAM's $T=1.008$ mirrors the same
qualitative pattern seen for the own-margin field
(Section~\ref{sec:ablation-distrito}, $T=0.61$): a stronger, better-aligned
field lets the fitted system settle at lower effective noise.

Population is a real, stated confound on mechanism, not on significance: GAM
distritos have roughly double the median registered-voter count of
periphery distritos in both years identically (7300 vs.\ 3612 in 2026, 7180
vs.\ 3404 in 2022; $r(\text{GAM}, \log(\text{population}))=0.346$ both
years, Section~\ref{sec:data-population}). Part of what the GAM field
captures is genuinely ``more urban/populous,'' not purely ``closer to the
capital'' in isolation -- unsurprising, since urban density and
capital-proximity co-occur in real geography, but it means the GAM result
should not be read as a clean geographic-distance effect on its own. This
does not undercut the paired-significance result, which measures predictive
power gained regardless of mechanism, but it sharpens what ``GAM matters''
should be understood to mean.

\subsection{Does the network have a unique equilibrium?}
\label{sec:multistability}

A question with no regression analog: does the real network plus the GAM
field settle into a unique equilibrium, or can the identical physical setup
land on different answers depending only on random initialization? Reusing
the 16 seeds' per-node outcomes, we define a multistability score
$\min(\text{error rate}, 1-\text{error rate})$: zero means all 16 seeds agree
with each other regardless of correctness; 0.5 means an even 8--8 split.
Most of the map is robustly, essentially uniquely determined: 73.4\% (2026)
and 78.3\% (2022) of distritos are fully locked (score $=0$); only 1.0\%
and 1.9\% show real multistability ($\geq4$ of 16 minority seeds). Boundary
distritos concentrate the remaining uncertainty: mean multistability 0.054
(2026) / 0.067 (2022) versus interior's 0.017 / 0.011, a 3--6$\times$ gap, and
the fully-locked share drops from $\sim$80\% (interior) to $\sim$55\%
(boundary) -- distinguishing genuinely undecided boundary distritos from
ones that are simply, consistently wrong. Two specific distritos
(\texttt{SAN JOS\'E\textbar MORA\textbar TABARCIA},
\texttt{SAN JOS\'E\textbar ASERR\'I\textbar MONTERREY}) are highly
multistable independently in \emph{both} 2026 and 2022. This cross-year
consistency is consistent with a structural feature of the network, but it
cannot on its own rule out a competing explanation: both distritos sit in
Mora and Aserr\'i, exactly the cantons Section~\ref{sec:data-gam} names as
most likely to be misclassified by the canton-level GAM proxy, and since GAM
is a static field reused unchanged across years, a proxy labeling error
would reproduce identically in both 2026 and 2022 by construction --
cross-year consistency alone cannot distinguish that from genuine dynamical
multistability (Section~\ref{sec:limitations} discusses this further).

\subsection{Domain-wall structure, counterfactual sensitivity, and cascade testing}
\label{sec:domainwall}
\label{sec:counterfactual}
\label{sec:cascade}

Three further diagnostics use the fitted GAM system itself to ask questions
a static classification comparison cannot pose, complementing
Section~\ref{sec:multistability}'s multistability check above; we summarize
them together here since all three converge on the qualitative picture that
check already makes most cleanly.

\emph{Domain-wall structure.} Does the model's $\sim$19\% error rate
concentrate at the interface between GAM and periphery -- distritos with at
least one geographic neighbor of the opposite GAM status -- rather than
being scattered randomly? Using the 16 pooled seeds' final configurations at
each election's GAM best-$T$, boundary distritos show a substantially
higher per-node error rate than interior ones: more than double for 2026
(38.0\% versus 16.2\%, a $2.35\times$ ratio) and, while short of double,
still a large gap for 2022 (51.0\% versus 29.7\%, a $1.72\times$ ratio) --
the absolute point-gap is similar across both years ($\sim$21--22 points)
even though the ratio is not. Within GAM specifically, error rate correlates with
MIDEPLAN's economic axis ($r=-0.391$ for 2026): the highest-error GAM
distritos average an economic score of 54.4 versus 65.1 for low-error GAM
distritos -- plausible but not cleanly established, since several of the
highest-error distritos driving this correlation sit in cantons (e.g.\
Mora) most likely misclassified by the canton-level GAM proxy
(Section~\ref{sec:data-gam}); if they are actually periphery, this piece of
the story is partly a proxy artifact rather than a genuine socioeconomic
finding, distinct from the between-region GAM-versus-periphery result of
Section~\ref{sec:gam}, whose significance does not depend on it.
Figure~\ref{fig:domainwall} maps the per-distrito error rate directly
against both the GAM boundary and the four proxy-misclassification-risk
cantons, so this exposure can be judged geographically rather than taken on
the summary statistics alone: the highest-error cluster sits immediately
along the GAM/periphery interface in both years, and visibly overlaps the
risk-canton outlines in the south and west of the metropolitan area.

\begin{figure*}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/domain_wall_map.png}
  \caption{Per-distrito error rate under the fitted geography+GAM model (16
  pooled seeds, each election's own GAM best-$T$), with the GAM canton-level
  proxy boundary (solid black) and the four cantons named in
  Section~\ref{sec:data-gam} as most likely over-included by that proxy
  (dashed blue: Mora, Alajuela's central canton, Aserr\'i, Para\'iso)
  overlaid. Gray distritos have no matching result row (see
  Section~\ref{sec:data}).}
  \label{fig:domainwall}
\end{figure*}

\emph{Counterfactual temperature sensitivity.} Fixing the real 2026 network
and field, how much would the equilibrium map differ if $T$ had been higher
or lower than the value that best matches reality ($T=1.008$) -- a question
requiring the dynamical system to be re-solved at each $T$, not answerable
from a fitted coefficient? Scanning 13 temperatures, divergence from the
$T=1.008$ reference stays small even at the scan's extremes: 2.9\% at
$T=0.05$, only 10.9\% at $T=5.0$ (five times the best-fit temperature). For
most distritos the outcome is strongly determined by geography plus GAM
rather than finely tuned to a specific noise level, consistent with no
confirmed critical point (Section~\ref{sec:fss}) holding here as well. We
label a distrito \emph{temperature-fragile} if its majority-vote spin at
either scan extreme ($T=0.05$ or $T=5.0$) differs from its $T=1.008$
reference value -- the category used below in the cascade test's candidate
selection.

\emph{Single-node cascade test.} Does a local political shift propagate
through the real network, or is it absorbed locally? For 10 candidate
distritos -- multistable fault lines, seed-locked-but-temperature-fragile
nodes, a locked-but-consistently-wrong node, and locked-and-correct
high-population controls on both sides -- we flip that one node's GAM field
value, re-equilibrate the whole network at $T=1.008$, and count how many
\emph{other} distritos' equilibrium spin changes (Table~\ref{tab:cascade}).
Eight of ten, including the single most dynamically uncertain distrito in
the network (Tabarcia), produce zero downstream effect anywhere else. Only
the two candidates already flagged by multiple diagnostics above (both
multistable and boundary; Orosi additionally temperature-fragile) propagate
at all, and only to immediately adjacent distritos.

\begin{table*}[htbp]
\centering
\caption{Single-node cascade test, 2026, GAM field, $T=1.008$, 16 pooled
seeds. Cascade size = other distritos whose majority-vote equilibrium spin
changes when the named distrito's GAM field value is flipped.}
\label{tab:cascade}
\begin{tabular}{lcc}
\toprule
Target distrito & Category & Cascade size \\
\midrule
Cartago\textbar Para\'iso\textbar Orosi & multistable + boundary + temp-fragile & 4 \\
San Jos\'e\textbar Acosta\textbar Palmichal & multistable + boundary & 1 \\
San Jos\'e\textbar Mora\textbar Tabarcia & multistable (top overall) & 0 \\
San Jos\'e\textbar Aserr\'i\textbar Monterrey & multistable & 0 \\
San Jos\'e\textbar Mora\textbar Piedras Negras & seed-locked, temp-fragile & 0 \\
San Jos\'e\textbar Central\textbar Pavas & locked, consistently wrong & 0 \\
San Jos\'e\textbar Central\textbar Hatillo & locked, temp-fragile & 0 \\
Heredia\textbar Central\textbar San Francisco & locked+correct, GAM control & 0 \\
Guanacaste\textbar Liberia\textbar Liberia & locked+correct, periphery control & 0 \\
San Jos\'e\textbar P\'erez Zeled\'on\textbar San Isidro & locked+correct, periphery control & 0 \\
\bottomrule
\end{tabular}
\end{table*}

Orosi, the single largest cascade above, sits in Para\'iso, another canton
flagged in Section~\ref{sec:data-gam} as GAM-proxy-misclassification-prone --
the same caveat noted for multistability's flagship cases above applies
here too. Together with Section~\ref{sec:multistability}, these three
diagnostics indicate the real network absorbs local perturbations rather
than amplifying them, evidence the fitted system is doing genuine
dynamical work; Section~\ref{sec:discussion} synthesizes what all four
diagnostics jointly show.

\subsection{A canton-level polarization trend, 2018--2022--2026}
\label{sec:polarization-trend}

Since GAM membership is a static administrative boundary (unlike MIDEPLAN's
2023-only snapshot or the 2022-only political field), it can be tested
identically against all three elections used in
Section~\ref{sec:historical}, at canton level (where the 31-canton GAM list
applies exactly, without Section~\ref{sec:data-gam}'s distrito-level proxy
imprecision). Table~\ref{tab:polarization-trend} reports the raw
GAM-versus-periphery gap alongside the same single-field Monte Carlo
procedure and direct paired test (province blocks, $n_{\text{blocks}}=7$,
matching Section~\ref{sec:ablation-canton}'s canton-level convention) used
throughout this section.

\begin{table*}[htbp]
\centering
\caption{GAM polarization trend, canton level, winner-vs-runner-up
binarization, 8 pooled seeds per election. Paired $p$ against geography-only,
province blocks ($n_{\text{blocks}}=7$).}
\label{tab:polarization-trend}
\begin{tabular}{lccccc}
\toprule
Election & Raw gap & Geography-only & Geography+GAM & Gain & Paired $p$ (seeds sig.) \\
\midrule
2018 (runoff)  & 38.0pp & $72.69\%$ & $63.12\%$ & $-9.6$pp  & $0.798$, 0/8 \\
2022 (runoff)  & 52.1pp & $66.31\%$ & $79.88\%$ & $+13.6$pp & $0.216$, 0/8 \\
2026 (round 1) & 47.3pp & $76.49\%$ & $83.04\%$ & $+6.6$pp  & $0.196$, 0/8 \\
\bottomrule
\end{tabular}
\end{table*}

Two findings that should not be conflated. The raw magnitude trend is
model-independent and real: the capital/periphery vote-share gap jumps from
38.0 to 52.1 percentage points between 2018 and 2022 and stays elevated in
2026 (47.3pp), consistent with 2018 already being established
(Section~\ref{sec:2018}) as a categorically different election. The Monte
Carlo significance picture is weak across all three years (0 of 8
seed-pairs each) -- including 2026, decisively significant at distrito level
($p=0.0005$, Section~\ref{sec:gam}) but not at canton level here, the same
granularity pattern already documented for the own-margin field
(Sections~\ref{sec:ablation-canton}/\ref{sec:ablation-distrito}: $+8.7$pp/significant
at distrito versus $+1.2$pp/not-significant at canton) and consistent with only 7 province
blocks -- the coarsest blocking used anywhere in this paper -- combined with
$N\!\sim\!84$ giving limited power. 2018 is the strangest case: GAM's raw
signal there is maximal (100\% of GAM cantons on one side versus 62\% in the
periphery) yet adding it \emph{lowers} alignment by 9.6 points, plausibly
connected to 2018's already-documented energetic anomaly
(Section~\ref{sec:2018}) -- forcing a uniform field on top of an
already-hard-to-find pattern may fight the geographic contagion rather than
help it, at this lighter canton-scale Monte Carlo budget.

\section{Discussion}
\label{sec:discussion}

The central methodological lesson of this paper is that the same ablation
question -- how much of a real spatial voting pattern is geography and how
much is individual predisposition -- can have opposite-looking answers
depending purely on the spatial resolution at which it is asked, using the
identical model, data source, election, and fitting procedure. This is not
a contradiction to be resolved in favor of one answer over the other; both
are correct descriptions of their respective scales. Canton-level
aggregation averages together distritos that can differ sharply in their
own political lean, and that averaging is itself information-destroying in
exactly the direction that would suppress a field-driven effect: if two

exec
/bin/bash -lc "sed -n '1461,1810p' manuscript/main.tex && rg -n '\\\\bibitem|korbel|massoli|tiwari|braha|godoy|mcnemar|karasiak|besag|TSE|HDX' manuscript/main.tex manuscript/*.bib" in /home/tomas/research-current/IsingCR
 succeeded in 95ms:
manuscript/references.bib:1:@article{besagclifford1989,
manuscript/references.bib:12:@article{karasiak2021,
manuscript/references.bib:34:@article{mcnemar1947,
manuscript/references.bib:56:@article{braha2017,
manuscript/references.bib:146:@article{korbel2026,
manuscript/references.bib:157:@misc{godoylorite2020,
manuscript/references.bib:177:@article{massoli2026,
manuscript/references.bib:232:@article{tiwari2021,
manuscript/main.tex:78:a synthetic $128\times128$/$256\times256$ square lattice \citep{tiwari2021}
manuscript/main.tex:82:elections, Braha and de Aguiar \citep{braha2017} analytically model
manuscript/main.tex:86:present approach, Korbel et al.\ \citep{korbel2026} fit a double-random-field
manuscript/main.tex:91:simulation and no explicit spatial topology anywhere in the model. Closest on vocabulary, Godoy-Lorite \& Jones \citep{godoylorite2020} fit a
manuscript/main.tex:103:dynamics more broadly \citep{massoli2026}; a recent review collects the
manuscript/main.tex:113:Korbel et al.'s \citep{korbel2026} cannot pose in the first place.
manuscript/main.tex:123:Elecciones (TSE), and run a deliberate \emph{ablation}: the same model, same
manuscript/main.tex:162:distinct from Korbel et al.'s \citep{korbel2026} double-random field, a
manuscript/main.tex:205:from TSE's public ``escrutinio definitivo'' releases and aggregated to the
manuscript/main.tex:254:negative toward the minority label). Reconciling TSE's naming conventions
manuscript/main.tex:256:TSE names each province's capital canton (and, one level down, its first
manuscript/main.tex:258:canton itself; and TSE preserves ``\~{N}'' as distinct from ``N,'' where
manuscript/main.tex:263:Costa Rica's 84 official cantons (real geometry from UN OCHA's HDX COD-AB
manuscript/main.tex:358:the same per-junta TSE consolidado files used throughout this paper,
manuscript/main.tex:361:nodes) against this paper's networks, unlike TSE's separately published
manuscript/main.tex:519:is assessed with McNemar's exact test \citep{mcnemar1947} -- which asks
manuscript/main.tex:524:\citep{korbel2026}. Spatial autocorrelation of the empirical vote pattern
manuscript/main.tex:536:structured data more generally \citep{karasiak2021}. We therefore
manuscript/main.tex:539:\citep{besagclifford1989}: rather than randomizing at the level of
manuscript/main.tex:1478:with Korbel et al.\ \citep{korbel2026}, who report a polarization transition in their
manuscript/main.tex:1549:regression \citep{karasiak2021}; its value here is corroborative rather
manuscript/main.tex:1648:via name-based sex inference or TSE's interactive consulta tool) was left
manuscript/main.tex:1651:modeling work \citep{massoli2026} has been re-checked specifically against

exec
/bin/bash -lc "sed -n '1,270p' manuscript/references.bib && rg -n '2026|Pueblo Soberano|2026' README.md manuscript --glob '"'!main.tex'"'" in /home/tomas/research-current/IsingCR
 succeeded in 33ms:
@article{besagclifford1989,
  author  = {Besag, Julian and Clifford, Peter},
  title   = {Generalized {M}onte {C}arlo significance tests},
  journal = {Biometrika},
  year    = {1989},
  volume  = {76},
  number  = {4},
  pages   = {633--642},
  doi     = {10.1093/biomet/76.4.633}
}

@article{karasiak2021,
  author  = {Karasiak, Nicolas and Dejoux, Jean-Fran\c{c}ois and Monteil, Claude and Sheeren, David},
  title   = {Spatial dependence between training and test sets: another pitfall of classification accuracy assessment in remote sensing},
  journal = {Machine Learning},
  year    = {2021},
  volume  = {111},
  number  = {7},
  pages   = {2715--2740},
  doi     = {10.1007/s10994-021-05972-1}
}

@article{binder1981,
  author  = {Binder, K.},
  title   = {Finite size scaling analysis of {I}sing model block distribution functions},
  journal = {Zeitschrift f\"ur Physik B Condensed Matter},
  year    = {1981},
  volume  = {43},
  number  = {2},
  pages   = {119--140},
  doi     = {10.1007/BF01293604}
}

@article{mcnemar1947,
  author  = {McNemar, Quinn},
  title   = {Note on the sampling error of the difference between correlated proportions or percentages},
  journal = {Psychometrika},
  year    = {1947},
  volume  = {12},
  number  = {2},
  pages   = {153--157},
  doi     = {10.1007/BF02295996}
}

@article{moran1950,
  author  = {Moran, P. A. P.},
  title   = {Notes on continuous stochastic phenomena},
  journal = {Biometrika},
  year    = {1950},
  volume  = {37},
  number  = {1-2},
  pages   = {17--23},
  doi     = {10.1093/biomet/37.1-2.17}
}

@article{braha2017,
  author  = {Braha, Dan and de Aguiar, Marcus A. M.},
  title   = {Voting contagion: Modeling and analysis of a century of {U.S.} presidential elections},
  journal = {PLOS ONE},
  year    = {2017},
  volume  = {12},
  number  = {5},
  pages   = {e0177970},
  doi     = {10.1371/journal.pone.0177970}
}

@article{camachosanchez2025,
  author  = {S{\'a}nchez, Sharon Camacho},
  title   = {Partidos con o sin base territorial en {C}osta {R}ica: an{\'a}lisis de la distribuci{\'o}n geogr{\'a}fica de los apoyos partidarios 1998 al 2022},
  journal = {GEOgraphia},
  year    = {2025},
  volume  = {27},
  number  = {58},
  doi     = {10.22409/geographia2025.v27i58.a66944}
}

@article{cardoso2022,
  author  = {Cardoso, M. and Silva, L. M. C. and Neli, R. R. and Souza, W. E.},
  title   = {Electorate involvement disorder: Universal relationship between the amplitude and electorate size in second round of {B}razilian {P}residential {E}lection},
  journal = {Physica A: Statistical Mechanics and its Applications},
  year    = {2022},
  volume  = {591},
  pages   = {126778},
  doi     = {10.1016/j.physa.2021.126778}
}

@article{cardoso2023,
  author  = {Cardoso, M. and Souza, J. T. G. and Neli, R. R. and Souza, W. E.},
  title   = {Scaling laws from {B}razilian state election results point out that the candidate's chance to win increases by investing more campaign efforts in smaller electorates},
  journal = {Physica A: Statistical Mechanics and its Applications},
  year    = {2023},
  volume  = {619},
  pages   = {128683},
  doi     = {10.1016/j.physa.2023.128683}
}

@article{cascantematamoros2006,
  author  = {Cascante Matamoros, Mar{\'i}a Jos{\'e} and Camacho S{\'a}nchez, Sharon},
  title   = {El sistema de partidos en los cantones: an{\'a}lisis de la distribuci{\'o}n territorial de los apoyos (1953-2016)},
  journal = {Revista de Derecho Electoral},
  year    = {2019},
  number  = {28},
  pages   = {195--216},
  doi     = {10.35242/rde_2019_28_11}
}

@article{chavarriamora2022,
  author  = {El{\'i}as, Chavarr{\'i}a Mora},
  title   = {Una mirada cantonal mediante estad{\'i}stica espacial al efecto del desarrollo humano sobre el apoyo electoral en la segunda ronda de la elecci{\'o}n presidencial de 2018},
  journal = {Revista de Derecho Electoral},
  year    = {2022},
  doi     = {10.35242/rde_2022_22_33_5}
}

@article{dibenedetto2023,
  author  = {Di Benedetto, Andrea and Wieners, Claudia E. and Dijkstra, Henk A. and Stoof, Henk T. C.},
  title   = {Media preference increases polarization in an agent-based election model},
  journal = {Physica A: Statistical Mechanics and its Applications},
  year    = {2023},
  volume  = {626},
  pages   = {129014},
  doi     = {10.1016/j.physa.2023.129014}
}

@article{galam2021,
  author  = {Galam, Serge},
  title   = {Will {T}rump win again in the 2020 election? {A}n answer from a sociophysics model},
  journal = {Physica A: Statistical Mechanics and its Applications},
  year    = {2021},
  volume  = {570},
  pages   = {125835},
  doi     = {10.1016/j.physa.2021.125835}
}

@article{jordan2020,
  author  = {Jordan, Soren},
  title   = {From ferromagnets to electoral instability},
  journal = {Nature Physics},
  year    = {2020},
  volume  = {16},
  number  = {2},
  pages   = {125--126},
  doi     = {10.1038/s41567-019-0761-8}
}

@article{korbel2026,
  author  = {Korbel, Jan and Dahdoul, Remah and Thurner, Stefan},
  title   = {Empirical validation of the polarization transition in a double-random field model of elections},
  journal = {Physical Review Letters},
  year    = {2026},
  volume  = {136},
  number  = {12},
  pages   = {127402},
  doi     = {10.1103/9gjj-1df6}
}

@misc{godoylorite2020,
  author       = {Godoy-Lorite, Antonia and Jones, Nick S.},
  title        = {Inference and Influence of Large-Scale Social Networks Using Snapshot Population Behaviour without Network Data},
  year         = {2020},
  eprint       = {2003.07146},
  archiveprefix = {arXiv},
  primaryclass = {cs.SI}
}

@article{russobeauguitte2014,
  author  = {Russo, Luca and Beauguitte, Laurent},
  title   = {Aggregation level matters: evidence from {F}rench electoral data},
  journal = {Quality \& Quantity},
  year    = {2014},
  volume  = {48},
  number  = {2},
  pages   = {923--938},
  doi     = {10.1007/s11135-012-9814-0}
}

@article{massoli2026,
  author  = {Massoli, Pierpaolo},
  title   = {Unveiling complex territorial socio-economic dynamics: a statistical mechanics approach},
  journal = {Social Indicators Research},
  year    = {2026},
  volume  = {183},
  number  = {3},
  pages   = {40},
  doi     = {10.1007/s11205-026-03887-9}
}

@article{mitra2026,
  author  = {Mitra, Adway},
  title   = {Dirichlet-{S}wing: understanding spatio-temporal aspects of political elections in heterogeneous societies through agent-based simulation},
  journal = {PLOS One},
  year    = {2026},
  volume  = {21},
  number  = {3},
  pages   = {e0344018},
  doi     = {10.1371/journal.pone.0344018}
}

@article{mullick2025,
  author  = {Mullick, Pratik and Sen, Parongama},
  title   = {Sociophysics models inspired by the {I}sing model},
  journal = {The European Physical Journal B},
  year    = {2025},
  volume  = {98},
  number  = {9},
  pages   = {206},
  doi     = {10.1140/epjb/s10051-025-01053-7}
}

@article{raducha2025,
  author  = {Raducha, Tomasz and Klamut, Jaros{\l}aw and Cremades, Roger and Bouman, Paul and Wili{\'n}ski, Mateusz},
  title   = {Susceptibilities of democratic electoral systems},
  journal = {IEEE Transactions on Computational Social Systems},
  year    = {2025},
  volume  = {12},
  number  = {5},
  pages   = {2186--2201},
  doi     = {10.1109/tcss.2024.3464092}
}

@article{siegenfeld2020,
  author  = {Siegenfeld, Alexander F. and Bar-Yam, Yaneer},
  title   = {Negative representation and instability in democratic elections},
  journal = {Nature Physics},
  year    = {2020},
  volume  = {16},
  number  = {2},
  pages   = {186--190},
  doi     = {10.1038/s41567-019-0739-6}
}

@article{tiwari2021,
  author  = {Tiwari, Mukesh and Yang, Xiguang and Sen, Surajit},
  title   = {Modeling the nonlinear effects of opinion kinematics in elections: a simple {I}sing model with random field based study},
  journal = {Physica A: Statistical Mechanics and its Applications},
  year    = {2021},
  volume  = {582},
  pages   = {126287},
  doi     = {10.1016/j.physa.2021.126287}
}
README.md:20:rounds, 2026), loaded/aggregated/pivoted by
README.md:25:adjacency, the MC temperature scan, and real map comparisons, all on real 2026
README.md:28:`run_real_pipeline.py` now binarizes 2026 as PUEBLO SOBERANO (48.5% nationally)
README.md:41:runner-up by construction; 2026 round 1, winner vs. runner-up by vote count).
README.md:55:| 2026 (round 1) | Pueblo Soberano | Liberación Nacional | 84 | 75.0% | 79.0%+/-2.2% | Yes | p=0.37, 1/8 |
README.md:57:*Pueblo Soberano (2026) is the direct electoral successor of Progreso Social
README.md:64:2022's/2026's, **now explained** (`scripts/investigate_2018_anomaly.py`, ~7s,
README.md:70:  (I=0.71 vs. 0.49 for 2022, 0.35 for 2026), on both the binarized spin and
README.md:74:  the winner" state, than 2022's or 2026's are.** Every election's trivial
README.md:77:  per canton, is 1.13 for 2018 vs. 0.77 (2022) and 0.59 (2026) -- roughly
README.md:78:  47% (2022) and 92% (2026) larger. A temperature scan starting from random
README.md:86:  2026) -- the problem is specifically that a *random-start* search never
README.md:89:This cleanly separates 2018 from 2022/2026 as a category (the question that
README.md:90:was actually open); it doesn't perfectly rank 2022 vs. 2026 against each
README.md:96:**The 1-sigma "beats baseline" read for 2022/2026 doesn't survive a proper
README.md:101:significant at p<0.05 for 2022 and 2026, with median p-values of 0.35 and
README.md:105:detect that way. But it means "2022 and 2026 clearly beat baseline" was an
README.md:107:current read is "2018 is a confident null; 2022/2026 show a similarly-sized
README.md:119:`scripts/run_ablation.py` separates the two ingredients of the 2026 result:
README.md:158:symmetry-breaking field. Local run (2026 coalition split, 8 pooled seeds, 500/500 sweeps, ~2.5 min
README.md:166:**Resolved 2026-08-16** with a heavier re-run on the UCR HPC cluster
README.md:174:at either canton or distrito granularity, for 2026**. Consistent with every
README.md:179:## Distrito-level ablation (2026)
README.md:260:- **Election results -- done.** TSE's site (tse.go.cr, vr2026, and the
README.md:264:  junta receptora de votos" ZIP exports (2018, 2022 both rounds, 2026
README.md:273:  different "distrito electoral" unit than 2022/2026's administrative distrito
manuscript/references.bib:146:@article{korbel2026,
manuscript/references.bib:150:  year    = {2026},
manuscript/references.bib:177:@article{massoli2026,
manuscript/references.bib:181:  year    = {2026},
manuscript/references.bib:188:@article{mitra2026,
manuscript/references.bib:192:  year    = {2026},
manuscript/README.md:11:  directory as of 2026-08-16 (canton-level ablation, historical comparison,
manuscript/README.md:19:2026) and should compile as-is on Overleaf.
manuscript/README.md:30:First full draft, 2026-08-16 -- covers all current results (canton-level
manuscript/README.md:31:ablation, historical comparison across 2018/2022/2026, the 2018 anomaly

web search: 
web search: https://doi.org/10.1103/9gjj-1df6
codex
severity: MAJOR  
location: Model and simulation / Observables  
quote: "Alignment with the real map is scored with the fraction of units whose simulated and empirical spins agree, using a label-symmetric variant (agreement under either global labeling, $\max$ of the two) whenever $h=0$"  
problem: The ablation compares a post-hoc label-optimized geography-only score with a non-symmetrized field score, so its reported gain is not based on a common scoring rule.  
fix: Use the same pre-specified, label-invariant scoring/calibration procedure for both arms, or determine the global orientation on training data and evaluate both arms on held-out data.

severity: MAJOR  
location: Model and simulation / Monte Carlo dynamics  
quote: "Because every headline alignment/significance figure in this paper is reported at whichever $T$ in the grid maximizes alignment, these are best-of-grid statistics rather than results at a single pre-specified $T$."  
problem: Temperature selection, field choice, binarization selection, and later direct comparisons are all performed on the same election map being scored, so Bonferroni correction over temperatures alone does not make the claimed predictive or confirmatory inferences valid.  
fix: Define a validation design with held-out elections/units or nested resampling, and correct jointly for all analyzed temperatures, fields, binarizations, and model choices.

severity: MAJOR  
location: Observables / spatial block permutation test  
quote: "Every spatial-block $p$-value below is estimated from 999 Monte Carlo sign-flip draws"  
problem: This specification is internally inconsistent with the later reported direct paired-test median "$p=0.0005$," because a 999-draw Monte Carlo randomization test cannot yield that individual-seed resolution under the stated procedure.  
fix: Provide the exact permutation statistic, p-value convention, per-seed p-values, and code/output sufficient to reconcile the stated 999 draws with every reported p-value.

severity: MAJOR  
location: Distrito-level ablation  
quote: "a direct paired test of the two arms' best-fit configurations against each other ... gives median $p=0.020$"  
problem: The two configurations are selected at their respective best temperatures using the outcome map and then treated as if the paired test were a single pre-specified comparison.  
fix: Incorporate temperature selection into the permutation/null procedure or conduct the paired comparison on independent validation data.

severity: MAJOR  
location: Methods/reproducibility / Monte Carlo dynamics  
quote: "replicate $k$'s seed is a fixed base seed offset by $k$ times a large stride"  
problem: Neither the base seed nor stride, exact temperature values, update implementation, recorded-state definition, or rule converting measurement sweeps into the “model's prediction” for McNemar testing is specified.  
fix: State all numerical settings and prediction aggregation rules in the manuscript or a versioned supplement, with a permanent code/data release matching the submitted results.

severity: MAJOR  
location: Data and the electoral network / Geographic adjacency network  
quote: "two cantons are coupled if and only if they share a physical border, weighted by shared border length normalized so the mean edge weight is 1.0"  
problem: The manuscript omits the boundary-file version/date, coordinate reference system, geometric tolerance, treatment of point contacts and topology repairs, and the reproducible crosswalk used after name reconciliation.  
fix: Deposit the raw-source identifiers and processed crosswalk/edge list, and specify the GIS operations and thresholds needed to reconstruct the graph exactly.

severity: MAJOR  
location: Distrito-level ablation and Table 3  
quote: "recomputed directly on the $N=488$ post-exclusion sample actually used below, the baseline is $67.0\%$, 327 of 488"  
problem: Table 3 and its figure nevertheless use a 66.9% baseline calculated on 492 units, while the model is evaluated on 488, making the displayed benchmark formally inconsistent with the analysis sample.  
fix: Recalculate all baselines, gaps, headroom calculations, figures, and tests on the identical post-exclusion sample, and report the pre-exclusion value only as ancillary information.

severity: MAJOR  
location: Finite-size scaling  
quote: "both curves stay within it throughout, confirming proper equilibration."  
problem: Remaining within the nominal Binder-cumulant range is not evidence of equilibration, and five crossings from only two non-nested, differently shaped real networks cannot support the stronger physical interpretation offered.  
fix: Demonstrate stationarity and mixing with trace/autocorrelation and independent-start diagnostics, report uncertainty bands on $U_4$, and present this strictly as an exploratory two-network comparison rather than finite-size scaling.

severity: MAJOR  
location: Does the network have a unique equilibrium?  
quote: "does the real network plus the GAM field settle into a unique equilibrium, or can the identical physical setup land on different answers depending only on random initialization?"  
problem: At finite temperature a finite Glauber chain has a unique stationary distribution under ordinary conditions, whereas the reported seed-dependent final states diagnose finite-run mixing/metastability rather than multiple equilibria.  
fix: Rename and analyze this as initialization sensitivity or metastability, with convergence and autocorrelation evidence, and avoid claiming a unique equilibrium from 16 final configurations.

severity: MAJOR  
location: Introduction / novelty positioning  
quote: "What is comparatively rare -- absent from all of the above -- is a model whose coupling network is not an assumption ... but the literal geographic adjacency structure of a real country"  
problem: This universal novelty claim is not established by the selective citations supplied and is central to the paper’s positioning.  
fix: Add a systematic, verifiable comparison table covering real-data electoral Ising/spatial-interaction studies, explicitly delimit the claimed novelty, and remove “absent from all” unless it is demonstrably supportable.

severity: MAJOR  
location: Second independent field  
quote: "which collapses exactly to Eq.~\eqref{eq:hamiltonian} when either $\lambda_{pol}=0$ or $\lambda_{soc}=0$"  
problem: More generally the proposed two-field Hamiltonian is only a single effective field, and the manuscript does not identify separately interpretable field effects or fit a joint model.  
fix: Reframe this as covariate-derived effective-field sensitivity analysis, or estimate and validate a genuinely identifiable joint model with pre-specified scaling and collinearity treatment.

severity: MAJOR  
location: Capital-region membership (GAM)  
quote: "We use a \emph{canton-level proxy} -- a distrito is flagged GAM if its parent canton is one of the 31 -- not the true distrito-level boundary"  
problem: The paper’s strongest non-circular result relies on a knowingly misclassified exposure whose individual misclassification rate and direction are unknown, while its mechanism is also confounded by population and urbanization.  
fix: Obtain and use the official distrito/fractional GAM geometry, perform misclassification sensitivity analysis, and compare GAM against population/urbanization covariates in a jointly evaluated model.

severity: MAJOR  
location: Introduction and Conclusion  
quote: "pure geographic contagion already explains nearly everything the model can explain about the real map"  
problem: A static border-adjacency prior and an outcome-derived field cannot identify interpersonal geographic contagion, so this language overstates an associative map-fitting exercise as a causal mechanism.  
fix: Replace “contagion” and “explains” with predictive/associative language, or supply temporal/individual-level identification that distinguishes social influence from spatially correlated confounding.

severity: MINOR  
location: Data / electoral results  
quote: "the two binarizations used in this paper are not cross-validated against each other for 2026 -- a check left to future work."  
problem: The coalition split was selected after observing degeneracy of the obvious alternative and groups ideologically heterogeneous parties, which leaves the headline label construction materially outcome-dependent.  
fix: Report a pre-specified family of all plausible party groupings with multiplicity-aware inference, or substantially demote the coalition-split result.

severity: MINOR  
location: Discussion  
quote: "the real map is a robust equilibrium for most distritos, with uncertainty concentrated in a small, reproducible, geographically identifiable set of fault lines"  
problem: This conclusion is under-hedged because the principal fault lines overlap explicitly acknowledged GAM-proxy errors and are inferred from selected final-state diagnostics rather than validated equilibrium estimates.  
fix: Restrict the conclusion to descriptive seed sensitivity under the proxy field and defer substantive fault-line claims until the true GAM boundary and convergence checks are available.

Overall assessment: This is potentially a useful Costa Rican case study with unusually candid limitations, but the main claims remain undermined by outcome leakage, post-selection inference, non-comparable scoring, incomplete computational specification, and causal language unsupported by the design. The novelty claim also needs a more defensible literature comparison, while the GAM result cannot carry the paper in its current proxy-based form. Recommendation: **reject-and-rework**.
tokens used
58,629
severity: MAJOR  
location: Model and simulation / Observables  
quote: "Alignment with the real map is scored with the fraction of units whose simulated and empirical spins agree, using a label-symmetric variant (agreement under either global labeling, $\max$ of the two) whenever $h=0$"  
problem: The ablation compares a post-hoc label-optimized geography-only score with a non-symmetrized field score, so its reported gain is not based on a common scoring rule.  
fix: Use the same pre-specified, label-invariant scoring/calibration procedure for both arms, or determine the global orientation on training data and evaluate both arms on held-out data.

severity: MAJOR  
location: Model and simulation / Monte Carlo dynamics  
quote: "Because every headline alignment/significance figure in this paper is reported at whichever $T$ in the grid maximizes alignment, these are best-of-grid statistics rather than results at a single pre-specified $T$."  
problem: Temperature selection, field choice, binarization selection, and later direct comparisons are all performed on the same election map being scored, so Bonferroni correction over temperatures alone does not make the claimed predictive or confirmatory inferences valid.  
fix: Define a validation design with held-out elections/units or nested resampling, and correct jointly for all analyzed temperatures, fields, binarizations, and model choices.

severity: MAJOR  
location: Observables / spatial block permutation test  
quote: "Every spatial-block $p$-value below is estimated from 999 Monte Carlo sign-flip draws"  
problem: This specification is internally inconsistent with the later reported direct paired-test median "$p=0.0005$," because a 999-draw Monte Carlo randomization test cannot yield that individual-seed resolution under the stated procedure.  
fix: Provide the exact permutation statistic, p-value convention, per-seed p-values, and code/output sufficient to reconcile the stated 999 draws with every reported p-value.

severity: MAJOR  
location: Distrito-level ablation  
quote: "a direct paired test of the two arms' best-fit configurations against each other ... gives median $p=0.020$"  
problem: The two configurations are selected at their respective best temperatures using the outcome map and then treated as if the paired test were a single pre-specified comparison.  
fix: Incorporate temperature selection into the permutation/null procedure or conduct the paired comparison on independent validation data.

severity: MAJOR  
location: Methods/reproducibility / Monte Carlo dynamics  
quote: "replicate $k$'s seed is a fixed base seed offset by $k$ times a large stride"  
problem: Neither the base seed nor stride, exact temperature values, update implementation, recorded-state definition, or rule converting measurement sweeps into the “model's prediction” for McNemar testing is specified.  
fix: State all numerical settings and prediction aggregation rules in the manuscript or a versioned supplement, with a permanent code/data release matching the submitted results.

severity: MAJOR  
location: Data and the electoral network / Geographic adjacency network  
quote: "two cantons are coupled if and only if they share a physical border, weighted by shared border length normalized so the mean edge weight is 1.0"  
problem: The manuscript omits the boundary-file version/date, coordinate reference system, geometric tolerance, treatment of point contacts and topology repairs, and the reproducible crosswalk used after name reconciliation.  
fix: Deposit the raw-source identifiers and processed crosswalk/edge list, and specify the GIS operations and thresholds needed to reconstruct the graph exactly.

severity: MAJOR  
location: Distrito-level ablation and Table 3  
quote: "recomputed directly on the $N=488$ post-exclusion sample actually used below, the baseline is $67.0\%$, 327 of 488"  
problem: Table 3 and its figure nevertheless use a 66.9% baseline calculated on 492 units, while the model is evaluated on 488, making the displayed benchmark formally inconsistent with the analysis sample.  
fix: Recalculate all baselines, gaps, headroom calculations, figures, and tests on the identical post-exclusion sample, and report the pre-exclusion value only as ancillary information.

severity: MAJOR  
location: Finite-size scaling  
quote: "both curves stay within it throughout, confirming proper equilibration."  
problem: Remaining within the nominal Binder-cumulant range is not evidence of equilibration, and five crossings from only two non-nested, differently shaped real networks cannot support the stronger physical interpretation offered.  
fix: Demonstrate stationarity and mixing with trace/autocorrelation and independent-start diagnostics, report uncertainty bands on $U_4$, and present this strictly as an exploratory two-network comparison rather than finite-size scaling.

severity: MAJOR  
location: Does the network have a unique equilibrium?  
quote: "does the real network plus the GAM field settle into a unique equilibrium, or can the identical physical setup land on different answers depending only on random initialization?"  
problem: At finite temperature a finite Glauber chain has a unique stationary distribution under ordinary conditions, whereas the reported seed-dependent final states diagnose finite-run mixing/metastability rather than multiple equilibria.  
fix: Rename and analyze this as initialization sensitivity or metastability, with convergence and autocorrelation evidence, and avoid claiming a unique equilibrium from 16 final configurations.

severity: MAJOR  
location: Introduction / novelty positioning  
quote: "What is comparatively rare -- absent from all of the above -- is a model whose coupling network is not an assumption ... but the literal geographic adjacency structure of a real country"  
problem: This universal novelty claim is not established by the selective citations supplied and is central to the paper’s positioning.  
fix: Add a systematic, verifiable comparison table covering real-data electoral Ising/spatial-interaction studies, explicitly delimit the claimed novelty, and remove “absent from all” unless it is demonstrably supportable.

severity: MAJOR  
location: Second independent field  
quote: "which collapses exactly to Eq.~\eqref{eq:hamiltonian} when either $\lambda_{pol}=0$ or $\lambda_{soc}=0$"  
problem: More generally the proposed two-field Hamiltonian is only a single effective field, and the manuscript does not identify separately interpretable field effects or fit a joint model.  
fix: Reframe this as covariate-derived effective-field sensitivity analysis, or estimate and validate a genuinely identifiable joint model with pre-specified scaling and collinearity treatment.

severity: MAJOR  
location: Capital-region membership (GAM)  
quote: "We use a \emph{canton-level proxy} -- a distrito is flagged GAM if its parent canton is one of the 31 -- not the true distrito-level boundary"  
problem: The paper’s strongest non-circular result relies on a knowingly misclassified exposure whose individual misclassification rate and direction are unknown, while its mechanism is also confounded by population and urbanization.  
fix: Obtain and use the official distrito/fractional GAM geometry, perform misclassification sensitivity analysis, and compare GAM against population/urbanization covariates in a jointly evaluated model.

severity: MAJOR  
location: Introduction and Conclusion  
quote: "pure geographic contagion already explains nearly everything the model can explain about the real map"  
problem: A static border-adjacency prior and an outcome-derived field cannot identify interpersonal geographic contagion, so this language overstates an associative map-fitting exercise as a causal mechanism.  
fix: Replace “contagion” and “explains” with predictive/associative language, or supply temporal/individual-level identification that distinguishes social influence from spatially correlated confounding.

severity: MINOR  
location: Data / electoral results  
quote: "the two binarizations used in this paper are not cross-validated against each other for 2026 -- a check left to future work."  
problem: The coalition split was selected after observing degeneracy of the obvious alternative and groups ideologically heterogeneous parties, which leaves the headline label construction materially outcome-dependent.  
fix: Report a pre-specified family of all plausible party groupings with multiplicity-aware inference, or substantially demote the coalition-split result.

severity: MINOR  
location: Discussion  
quote: "the real map is a robust equilibrium for most distritos, with uncertainty concentrated in a small, reproducible, geographically identifiable set of fault lines"  
problem: This conclusion is under-hedged because the principal fault lines overlap explicitly acknowledged GAM-proxy errors and are inferred from selected final-state diagnostics rather than validated equilibrium estimates.  
fix: Restrict the conclusion to descriptive seed sensitivity under the proxy field and defer substantive fault-line claims until the true GAM boundary and convergence checks are available.

Overall assessment: This is potentially a useful Costa Rican case study with unusually candid limitations, but the main claims remain undermined by outcome leakage, post-selection inference, non-comparable scoring, incomplete computational specification, and causal language unsupported by the design. The novelty claim also needs a more defensible literature comparison, while the GAM result cannot carry the paper in its current proxy-based form. Recommendation: **reject-and-rework**.
