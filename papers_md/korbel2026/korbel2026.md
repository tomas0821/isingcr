# Empirical validation of the polarization transition in a double-random field model of elections

Jan Korbel,<sup>1</sup> Remah Dahdoul,<sup>1</sup> and Stefan Thurner2, 1, 3, [<sup>∗</sup>](#page-0-0)

<sup>1</sup>Complexity Science Hub, Metternichgasse 8, 1030, Vienna, Austria

<sup>2</sup>Section for the Science of Complex Systems, Center for Medical Data Science,

Medical University of Vienna, Spitalgasse 23, A-1090 Vienna, Austria

<sup>3</sup>Santa Fe Institute, 1399 Hyde Park Road, Santa Fe, New Mexico 87501, USA

We model bipartisan elections where voters are exposed to two forces: local homophilic interactions and external influence from two political campaigns. The model is mathematically equivalent to the random field Ising model with a bimodal field. When both parties exceed a critical campaign spending, the system undergoes a phase transition to a highly polarized state where homophilic influence becomes negligible, and election outcomes mirror the proportion of voters aligned with each campaign, independent of total spending. The model predicts a hysteresis region, where the election results are not determined by campaign spending but by incumbency. Calibrating the model with historical data from US House elections between 1980 and 2020, we find the critical campaign spending to be ∼ 1.8 million USD. Campaigns exceeding critical expenditures increased in 2018 and 2020, suggesting a boost in political polarization.

Classical statistical physics provides a framework for understanding collective phenomena. It typically assumes weakly interacting constituents, governed by a single, time-invariant force, which allows computation of phase diagrams and identification of critical points where system-wide change occurs. This framework has long been applied to social phenomena, including financial markets [\[1–](#page-4-0)[3\]](#page-4-1), pedestrian and crowd dynamics [\[4,](#page-4-2) [5\]](#page-4-3), anthropology [\[6,](#page-5-0) [7\]](#page-5-1), judicial systems [\[8\]](#page-5-2), and opinion formation [\[9–](#page-5-3)[12\]](#page-5-4). In particular, it underpins opinion dynamics models such as bounded confidence [\[13,](#page-5-5) [14\]](#page-5-6), social validation [\[15\]](#page-5-7), and cultural dissemination [\[16\]](#page-5-8).

In voting behavior, one of the most influential physicsinspired models is the voter model [\[17\]](#page-5-9), where agents adopt neighbors' opinions on lattices or heterogeneous networks [\[18\]](#page-5-10). Extensions include stochastic noise [\[19\]](#page-5-11), committed agents or "zealots" [\[20\]](#page-5-12), and the interplay of micro- and macrodynamics [\[21\]](#page-5-13). It has been shown that the voter model reproduces statistical features of US presidential elections [\[22\]](#page-5-14); see also [\[23\]](#page-5-15) for a review.

A more recent class of opinion dynamics models builds on two sociological principles: homophily—the tendency to associate with similar others [\[24\]](#page-5-16)—and social balance—the reduction of cognitive dissonance in triads [\[25,](#page-5-17) [26\]](#page-5-18). Extending the voter model, these approaches capture more realistic interactions. Their combined effects have been studied jointly [\[27,](#page-5-19) [28\]](#page-5-20) and integrated into a unified framework [\[29\]](#page-5-21), applied to group formation [\[30\]](#page-5-22), and recently validated experimentally [\[31\]](#page-5-23). Many such models, including voter- and homophily-based ones, are inspired by the Ising model, long a versatile tool in various interdisciplinary contexts [\[32\]](#page-5-24), especially in opinion dynamics [\[33](#page-5-25)[–35\]](#page-5-26). In elections, it explained the universal scaling of vote distributions in proportional systems [\[36\]](#page-5-27), predicted margins of victory from turnout [\[37\]](#page-5-28), and modeled temporal effects through an external field [\[38\]](#page-5-29).

A central challenge in complex adaptive systems such as societies is the variety of time-dependent interactions, co-evolution, herding, and anticipation of others' actions [\[39\]](#page-5-30). While some aspects are easy to model, calibration and validation remain difficult, requiring great care to ensure testable models. Here, we address opinion formation with multiple interaction types, as in political elections. Voters exchange views within social networks of family, friends, and colleagues, while also following political campaigns—typically only those of their preferred party. We model these two processes through Ising interactions for homophily and a bimodal random field for campaign influence. Together, they form a Random Field Ising Model (RFIM), extending spin-spin interactions with site-dependent random external fields. An equivalent mean-field description can be derived from a master-equation of stochastic opinion switching with preference and adaptation terms, as originally introduced in the context of sociodynamics [\[40,](#page-5-31) [41\]](#page-5-32).

Despite its simplicity, the RFIM captures rich behavior such as quenched disorder and complex phase diagrams [\[42–](#page-5-33)[44\]](#page-5-34). Variants with bimodal random fields, where the field takes two values [\[45–](#page-5-35)[47\]](#page-5-36), exhibit tri-critical points marking the transition from second- to first-order phase changes [\[48,](#page-6-0) [49\]](#page-6-1). In the context of an election campaign, the RFIM represents a bipartisan electorate where each voter holds a binary preference. Voters occupy a social (friendship) network and are randomly assigned one of two field values: the sign encodes campaign affiliation, while the magnitude reflects campaign strength, with spending serving as a proxy. A schematic illustration is shown in End Matter, Fig. [3.](#page-7-0) RFIM approaches have long been used in sociophysics [\[50,](#page-6-2) [51\]](#page-6-3), specifically to illustrate qualitative campaign effects [\[38\]](#page-5-29), but have never been calibrated to an Ising-type model with data on campaign spending. The model employs concepts such as temperature and external fields, which should be understood as effective parameters that summarize complex

<span id="page-0-0"></span><sup>∗</sup> [stefan.thurner@meduniwien.ac.at](mailto:stefan.thurner@meduniwien.ac.at)

social, cognitive, and economic processes and not as literally physical quantities.

The aim of this paper is to understand how the interplay between homophily and campaign-following leads to the emergence of campaign polarization in ways that can be calibrated to data. Campaign polarization is defined as the normalized difference between the average opinions of voters exposed to each campaign. Low polarization indicates that both groups vote similarly, with decisions mainly shaped by homophily, whereas high polarization means that groups align with campaigns and are less influenced by neighbors. We compute the phase diagram as a function of the "temperature," representing susceptibility to opinion change, and the campaign spending of the two parties.

We focus on the effects of increasing campaign intensity. At low spending, opinions are shaped mainly by homophily, but as campaign influence grows, voter preferences are increasingly influenced by campaign messaging. Key questions are: when does campaign alignment outweigh homophilic similarity, how does polarization evolve at this point, and how does this transition affect social tension and election outcomes? A strength of our model is that it can be calibrated and tested on empirical data; we use the US House elections between 1980 and 2020, particularly. Calibration allows us to infer the "temperature" and the critical spending threshold above which campaign polarization rises sharply, and to track how many races exceeded this threshold over four decades. To our knowledge, this is the first time that thermodynamic parameters and a critical spending threshold are directly extracted from historical election data and used to predict levels of polarization in society.

Election model as an RFIM with a bimodal field. — We consider N voters with binary opinions s<sup>i</sup> ∈ ±1, representing preference for one of two parties in a bipartisan election. Voters form a social network encoded in the adjacency matrix Aij and interact through homophily, tending to align with neighbors. Each voter also follows one of the two campaigns, modeled by an external field h<sup>i</sup> drawn from a bimodal distribution,

p(hi) = p δ(h<sup>i</sup> − h <sup>+</sup>) + (1 − p) δ(h<sup>i</sup> + h <sup>−</sup>), (1)

where δ(x) is the Dirac delta function and p ≡ p(h <sup>+</sup>) is the probability of following the first party's campaign. With h <sup>+</sup>, h<sup>−</sup> ≥ 0, the field takes values h <sup>+</sup> or −h <sup>−</sup>. The system Hamiltonian is

H(s1, . . . , s<sup>N</sup> ) = −J X i<j Aij sis<sup>j</sup> − X i his<sup>i</sup> . (2)

To solve the model, we apply two approximations: the configuration model and a mean-field approximation (see Supplemental Material). Denoting the average magnetization by m = ⟨si⟩, we arrive at the meanfield Hamiltonian HMF (s1, . . . , s<sup>N</sup> ) = − P i (Jm˜ + hi)s<sup>i</sup> , where J˜ = J⟨k⟩ and ⟨k⟩ is the average node degree. The equilibrium distribution is therefore p(s|h <sup>±</sup>) = exp h −β(Jm˜ ± h <sup>±</sup>)s i /Z<sup>±</sup>, where β = (kT) −1 is the inverse temperature (for the rest of the paper, we set k = 1), and Z <sup>±</sup> = 2 cosh h β(Jm˜ ± h ±) i is the partition function. Here, the temperature T represents social volatility—the willingness of individuals to adopt new opinions, even if this increases social stress.

The average magnetization under field ±h <sup>±</sup> is m<sup>±</sup> ≡ ⟨s⟩ <sup>±</sup> = tanh[β(Jm˜ ± h <sup>±</sup>)]. The population magnetization is m = pm<sup>+</sup> + (1 − p)m−, representing the election outcome (m = ±1 corresponds to an unanimous result; m = 0 represents 50:50 split). It satisfies the selfconsistency equation,

<span id="page-1-0"></span>m = p tanh[β(Jm˜ +h <sup>+</sup>)]+(1−p) tanh[β(Jm˜ −h <sup>−</sup>)] . (3)

Equation [\(3\)](#page-1-0) can be alternatively derived from a masterequation of stochastic opinion switching with preference and adaptation terms; the explicit derivation and parameter mapping are given in the Supplemental Material. Setting m = 0 yields

<span id="page-1-1"></span>p tanh(βh<sup>+</sup>) = (1 − p) tanh(βh<sup>−</sup>), (4)

which reduces to h <sup>+</sup> = h <sup>−</sup> for p = 1 2 . We define campaign polarization as π = 2 (m<sup>+</sup> − m<sup>−</sup>), the difference between average opinions of voters following opposite campaigns. If both groups share the same opinion, π = 0; if they hold opposite views (m<sup>+</sup> = 1, m<sup>−</sup> = −1), then π = 1.

Critical parameters. — We first summarize the known results for the symmetric case p = 1 2 and h <sup>+</sup> = h <sup>−</sup> ≡ h. We set J˜ = 1. As shown in [\[49\]](#page-6-1) and in the Supplemental Material, the model exhibits a continuous crossover for T > 1. For T < 1, it undergoes a second-order transition at <sup>h</sup><sup>c</sup> <sup>=</sup> <sup>T</sup> arctanh √ 1 − T . A first-order transition occurs for lower temperatures, with tricritical point T<sup>t</sup> = 2 3 and h<sup>c</sup> = 2 3 arctanh √ 1 ≈ 0.439.

3 We extend this result to the non-symmetric case using Eq. [\(4\)](#page-1-1), which links h <sup>+</sup> and h <sup>−</sup>, and by expanding the self-consistency equation [\(3\)](#page-1-0) around m = 0. Unlike the symmetric case, the quadratic term does not vanish, yielding the critical curves

<span id="page-1-2"></span>h + <sup>c</sup> <sup>=</sup> <sup>T</sup> arctanh r (1 − T) 1 − p p , (5)

<span id="page-1-3"></span>h − <sup>c</sup> <sup>=</sup> <sup>T</sup> arctanh r (1 − T) p 1 − p . (6)

The full derivation is given in the Supplemental Material.

Phase diagram. — In the (h <sup>+</sup>, h<sup>−</sup>) plane, we solve Eq. [\(3\)](#page-1-0) numerically to obtain the phase diagrams shown in Fig. [1.](#page-2-0) For T ≥ 1, the system has a single stable solution: the candidate with higher campaign spending wins, with the boundary given by Eq. [\(4\)](#page-1-1). For T < 1 and low fields, a hysteresis region appears around the curve given by Eq. [\(4\)](#page-1-1) until reaching the critical values of

<span id="page-2-0"></span>![](_page_2_Figure_1.jpeg)

FIG. 1: Phase diagrams of the election model. Phase diagram for magnetization, m (a-d), and polarization, π, (e-h) in the (h <sup>+</sup>, h<sup>−</sup>) plane for temperature T = 1 (a,c,e,g), and for T = 0.75 (b,d,f,h), and a prior probability, p = 0.5 (a,b,e,f) and p = 0.6 (c,d,g,h). The black dashed line shows m = 0. The purple point marks the maximal point of the hysteresis, as derived in the main text. For T = 1, the expected behavior is that the magnetization is directly affected by the relative strength of the two fields, affected by p. For T = 0.75, we observe a more interesting behavior of the phase diagram. For the case of low field strength, we observe hysteresis (striped region). In both cases, the campaign polarization, π, increases rapidly when both field strengths exceed a critical value, h<sup>c</sup> (red).

Eqs. [\(5\)](#page-1-2) and [\(6\)](#page-1-3). This implies voter behavior depends on prior states, which we interpret as an incumbency effect where officeholders retain an advantage even with lower spending than predicted by Eq. [\(4\)](#page-1-1). The incumbency effect is well documented [\[52,](#page-6-4) [53\]](#page-6-5) and considered central to campaign strategy [\[54\]](#page-6-6).

Campaign polarization π remains near zero when at least one external field is weak and increases only when both exceed their critical values, h <sup>+</sup> ≳ h + <sup>c</sup> and h <sup>−</sup> ≳ h − c . Like magnetization, polarization undergoes a phase transition for T < 1. In the high-polarization regime, the overall magnetization is nearly constant, m ≈ 2p − 1, as predicted by Eq. [\(4\)](#page-1-1) for h <sup>+</sup>, h<sup>−</sup> ≫ 1, an effect most pronounced at low T. Thus, campaign influence dominates homophily: voters aligned with a campaign tend to vote uniformly for that party, regardless of neighbors. This matches recent results [\[55\]](#page-6-7) linking strong campaign polarization to voter extremism, where voters adopt increasingly extreme positions under intense pressure. Finally, polarization here corresponds to affective polarization [\[56–](#page-6-8)[58\]](#page-6-9), where individuals bond more with their political group than with ideology. Our model captures this as the interplay of ideological and partisan homophily, amplified by campaign intensity.

Calibration to US House election data. — To test the model against real data, we analyze all US House campaigns in 435 districts across 21 elections (presidential and midterms) from 1980–2020. Campaign spending and results are publicly available via the Federal Election Commission (FEC) [\[59\]](#page-6-10) and in machine-readable form at [\[60\]](#page-6-11). We focus on House races because congressional districts have relatively uniform populations, enabling meaningful spending comparisons. To ensure bipartisan competition, we restrict to races contested solely between Democratic and Republican candidates, excluding those with significant third-party or independent contenders. This yields 6357 races from 9135 in the period. All campaign expenditures are inflation-adjusted to 2020 USD using the Consumer Price Index (CPI). For each race, the campaign share parameter p is set by the previous election result in the same district. For the first election in our dataset (1980), p is taken from the 1978 publicly available results.

To estimate model parameters, we build a classification framework based on the proposed dynamics to predict race winners. Outside the hysteresis region, the winner is determined by the sign of total magnetization; within the hysteresis region, outcomes depend on incumbency when an incumbent is present. This scheme is illustrated in Fig. [2\(](#page-3-0)a,b) and detailed in the Supplemental Material.

We first consider the symmetric case p ≈ 0.5. For p = 0.5, the classification model predicts the same outcome for all T ≥ 1: the higher-spending candidate wins (Fig. [2\(](#page-3-0)a)). For T < 1, a hysteresis region emerges (yellow) where incumbency dominates. This region centers near h DEM = h REP , with its shape depending on T and h<sup>c</sup> (Fig. [2\(](#page-3-0)b)). By fitting the empirical boundaries of this region, we infer T and hc. Optimal parameters are estimated by maximizing classification accuracy over T and hc, yielding T <sup>∗</sup> = 0.922 and h<sup>c</sup> = \$1.83M

<span id="page-3-0"></span>![](_page_3_Figure_1.jpeg)

FIG. 2: Estimation of model parameters for US House of Representatives. We compare campaign spending and election results for 6357 of 9135 races between 1980–2020, focusing on close races (p = 0.5 ± 0.05). (a) For T ≥ 1, the classification model (see Supplemental Material) predicts the higher-spending candidate wins. (b) For T < 1, it predicts an incumbency region (yellow) where incumbents win despite lower spending. (c) Optimal parameters T and h<sup>c</sup> are estimated by maximizing classification accuracy across all 6357 races, yielding T <sup>∗</sup> = 0.922 and h<sup>c</sup> = \$1.83M. Cases where incumbents win with lower spending are highlighted, with additional black borders for points in the hysteresis region. The spending diagram is truncated to show the incumbency region (yellow). (d) Accuracy across T is shown, with the maximum marked by a red star. The inset shows a McNemar contingency table comparing the optimal model (T = T ∗ ) to the null model (T = 1). The McNemar test gives p < 0.0001, indicating significantly better performance of the optimal model.

(Fig. [2\(](#page-3-0)c)). The figure highlights all closely contested races (p = 0.5 ± 0.05), marking cases where incumbents win despite lower spending (black-bordered dots).

In the End Matter, we present a similar analysis for races with p ≈ 0.6, i.e., Republican-leaning races (p = 0.6 ± 0.05, Fig. [5\)](#page-8-0) and p ≈ 0.4, i.e., Democratleaning races (p = 0.4 ± 0.05, Fig. [6\)](#page-8-1). Applied to these two subsets, the parameters shift slightly (T <sup>∗</sup> = 0.845 for Republican-leaning races, T <sup>∗</sup> = 0.865 for Democratleaning races, h<sup>c</sup> ∼ \$2M), but the qualitative behavior — hysteresis and emergence of polarization — remains unchanged.

Figure [2\(](#page-3-0)d) shows classification accuracy as a function of temperature, with h<sup>c</sup> chosen at each T to maximize accuracy. To test statistical significance against a baseline, we compare the optimal classifier to a null model without hysteresis (T ≥ 1) using the McNemar test (see Supplemental Material). The inset shows the contingency table of correctly and incorrectly classified results for both models.

We find a statistically significant improvement in accuracy (χ <sup>2</sup> = 24.69, p-value p = 6.76 · 10−<sup>7</sup> ), though the absolute gain is small. This reflects that in most races incumbents outspend challengers, so both the null model (T ≥ 1) and optimal model (T = T ⋆ ) yield similar predictions. This aligns with prior findings that incumbency strengthens fundraising, with incumbents typically attracting more support [\[61\]](#page-6-12).

In the End Matter, we further extend our analysis to the emergence of polarization. By estimating the critical spending threshold hc, we test how many races fall in the polarization region, i.e., when both parties exceed h<sup>c</sup> (Fig. [4\)](#page-7-1). Panel (a) shows the full spending region including the polarized area, while panel (b) presents results for p ≈ 0.5. At low spending, outcomes are decisive; above hc, results cluster near 50:50, consistent with the prediction that for p ≈ 0.5 most outcomes in the polarized region satisfy m ≈ 0. Panel (c) compares the number of races where both campaigns exceeded h<sup>c</sup> across election cycles, revealing a sharp rise in 2018 and 2020. While these results rest on model predictions and need further empirical validation, the trend matches recent observations of rising campaign polarization [\[62\]](#page-6-13).

To further test the robustness of our approach, we present two additional analyses in the Supplemental Material: in the first analysis, we divide the dataset into four decades and estimate the parameters for each decade separately. We observe that while the temperature slightly decreases over time, the critical spending slightly increases. Second, we compare our approach to a machine learning approach based on a support vector machine classification model. We show that the SVM can estimate the incumbency region (with slightly lower test accuracy); however, it cannot provide additional interpretation of the model, such as the presence of a polarization region.

Discussion. — We introduced a simple election model combining two mechanisms influencing voter decisions: homophily, i.e., interactions with family, friends, and close contacts, and political campaign influence. Despite its simplicity, the model can be calibrated with real-world data (US House elections) and reproduces rich behavior absent in earlier work. The fact that voters typically follow only one campaign leads to a phase transition: campaign polarization rises sharply once both parties exceed a critical spending threshold. In this regime, most outcomes are 50:50 when p ≈ 0.5 (swing states), regardless of the detailed spending. For biased states (p ̸≈ 0.5), the model allows us to estimate the challenger's minimum spending above which 50:50 outcomes become possible.

We identified a hysteresis region in the phase diagram that leads to an incumbency effect, enabling quantitative assessment of incumbents' advantage. The model shows that challengers must overcome an initial threshold of about \$140, 000 even if incumbents spend nothing. This barrier decreases with higher overall spending but remains significant: for instance, when the incumbent spends 0.5h<sup>c</sup> (≈ \$900, 000), the challenger still faces a disadvantage of about 20% of total campaign cost. This quantifies a structural incumbency advantage beyond candidate-specific factors. By quantifying incumbency strength, we estimate the effective temperature of the social system and identify a polarization threshold. Notably, even without a universal definition of "temperature" in social contexts, it can be inferred indirectly from observable critical phenomena such as hysteresis and field-driven phase transitions.

Several studies reported a decline in incumbency strength in recent decades [\[63\]](#page-6-14), raising the question of whether this relates to shifts in effective "temperature". It remains open whether this temperature is universal or varies across elections, contexts, or regions. Since incumbency is central to electoral strategy [\[64\]](#page-6-15), further work should examine how decisions such as planned retirements shape challengers' prospects by mitigating incumbents' inherent advantage.

The model can be naturally extended in several ways. Multipartisan systems can be described by an extension to a double-random field Potts model [\[65\]](#page-6-16) with more than two opinion states. More realistic scenarios could be added through extensions to heterogeneous friendship networks, explicit party membership, or mechanisms such as primaries. Homophily may also vary across ties—for instance, individuals might ignore co-workers' views but adopt those of parents or close friends. Such modifications would better capture electoral complexity. Moreover, campaign intensity may not scale linearly with spending, as noted in earlier work [\[66,](#page-6-17) [67\]](#page-6-18), suggesting future models should consider nonlinear or contextdependent effects.

Despite its simplicity, the model predicts complex game-theoretic behavior. Strategic aspects of campaigns have been studied from this perspective [\[68,](#page-6-19) [69\]](#page-6-20), and our results deepen this understanding. The model suggests that candidates may rationally raise spending to induce polarization; once reached, it is difficult for opponents to reverse, locking in an advantage. This is especially effective in partisan districts, where dominant candidates benefit from driving the electorate into a polarized phase. Yet this strategy carries social costs: polarization erodes ties across divides and exacerbates fragmentation. A key implication of the model is that regulatory interventions, such as caps on campaign spending, may be needed to prevent undesirable outcomes. While spending limits are under renewed discussion [\[70\]](#page-6-21), our results add a novel perspective by emphasizing the broader societal costs of unbounded campaign intensity.

Note that similar results were found in the context of polarization in the US Congress itself [\[71\]](#page-6-22). The study shows that the polarization in the US Congress increased after the 2010 Supreme Court approval of Super PACs, which enabled an increase in donor influence. Also, other aspects such as social connectivity can increase polarization, not only in the context of elections [\[72,](#page-6-23) [73\]](#page-6-24).

Elections are not the only context in which homophily competes with external influence. Similar dynamics appear in marketing, where peer effects and advertising shape consumer behavior. A classic case is the Coca-Cola vs. Pepsi rivalry [\[74\]](#page-6-25), showing how competing campaigns polarize preferences. Our framework illustrates how polarization generally arises from the tension between social ties and persuasive efforts.

Acknowledgments. — We thank Mirta Galesic and Henrik Olsson for helpful discussions. We also thank three anonymous referees for their constructive comments. We acknowledge support from the Austrian Science Fund (FWF) under Grants No. 10.55776/P34994 and EFP5 ReMASS, funding from the Austrian Federal Ministry for Climate Action, Environment, Energy, Mobility, Innovation, and Technology under GZ 2023- 0.841.266, through the Postdoc Program for Complexity Science and Data Competence.

<span id="page-4-3"></span><span id="page-4-2"></span><span id="page-4-1"></span>Data availability statement. — he data that support the findings of this article are openly available [\[59,](#page-6-10) [60\]](#page-6-11).

<span id="page-4-0"></span>[1] R. N. Mantegna and H. E. Stanley, Scaling behaviour in the dynamics of an economic index, [Nature](https://doi.org/10.1038/376046a0) 376, 46 [\(1995\).](https://doi.org/10.1038/376046a0) [2] X. Gabaix, P. Gopikrishnan, V. Plerou, and H. E. Stanley, A theory of power-law distributions in financial market fluctuations, Nature 423[, 267 \(2003\).](https://doi.org/10.1038/nature01624) [3] J.-P. Bouchaud, From statistical physics to social sciences: the pitfalls of multi-disciplinarity, [J. Phys. Com](https://doi.org/10.1088/2632-072X/ad104a)plex. 4[, 041001 \(2023\).](https://doi.org/10.1088/2632-072X/ad104a) [4] D. Helbing and P. Moln´ar, Social force model for pedestrian dynamics, Phys. Rev. E 51[, 4282 \(1995\).](https://doi.org/10.1103/PhysRevE.51.4282) [5] I. Karamouzas, B. Skinner, and S. J. Guy, Universal

- <span id="page-5-21"></span><span id="page-5-0"></span>power law governing pedestrian interactions, [Phys. Rev.](https://doi.org/10.1103/PhysRevLett.113.238701) Lett. 113[, 238701 \(2014\).](https://doi.org/10.1103/PhysRevLett.113.238701) [6] J. S. Lansing, S. Thurner, N. N. Chung, A. Coudurier-Curveur, C¸ a˘gil Karaka¸s, K. A. Fesenmyer, and L. Y. Chew, Adaptive self-organization of bali's ancient rice terraces, PNAS 114[, 6504 \(2017\).](https://doi.org/10.1073/pnas.1605369114) [7] Y. Gandica, J. S. Lansing, N. N. Chung, S. Thurner, and
- <span id="page-5-24"></span><span id="page-5-23"></span><span id="page-5-22"></span><span id="page-5-3"></span><span id="page-5-2"></span><span id="page-5-1"></span>L. Y. Chew, Bali's ancient rice terraces: A hamiltonian approach, Phys. Rev. Lett. 127[, 168301 \(2021\).](https://doi.org/10.1103/PhysRevLett.127.168301) [8] E. D. Lee, C. P. Broedersz, and W. Bialek, Statistical mechanics of the us supreme court, [J. Stat. Phys.](https://doi.org/10.1007/s10955-015-1253-6) 160, [275 \(2015\).](https://doi.org/10.1007/s10955-015-1253-6) [9] S. Galam, Application of statistical physics to politics, Physica A 274[, 132 \(1999\).](https://doi.org/https://doi.org/10.1016/S0378-4371(99)00320-9) [10] J. Neirotti and N. Caticha, Legislative rebellions and impeachments in a neural network society, [Phys. Rev. E](https://doi.org/10.1103/PhysRevE.110.054110) 110[, 054110 \(2024\).](https://doi.org/10.1103/PhysRevE.110.054110) [11] P. Klimek, R. Lambiotte, and S. Thurner, Opinion formation in laggard societies, [Europhys. Lett.](https://doi.org/10.1209/0295-5075/82/28008) 82, 28008 [\(2008\).](https://doi.org/10.1209/0295-5075/82/28008) [12] C. Castellano, S. Fortunato, and V. Loreto, Statistical physics of social dynamics, [Rev. Mod. Phys.](https://doi.org/10.1103/RevModPhys.81.591) 81, 591 [\(2009\).](https://doi.org/10.1103/RevModPhys.81.591) [13] R. Hegselmann and U. Krause, Opinion Dynamics and Bounded Confidence Models, Analysis and Simulation,
- <span id="page-5-29"></span><span id="page-5-28"></span><span id="page-5-27"></span><span id="page-5-26"></span><span id="page-5-25"></span><span id="page-5-9"></span><span id="page-5-8"></span><span id="page-5-7"></span><span id="page-5-6"></span><span id="page-5-5"></span><span id="page-5-4"></span>[J. Artif. Soc. Soc. Simul.](https://ideas.repec.org/a/jas/jasssj/2002-5-2.html) 5, 1 (2002). [14] G. Deffuant, D. Neau, F. Amblard, and G. Weisbuch, Mixing beliefs among interacting agents, [Adv. Complex](https://doi.org/10.1142/S0219525900000078) Syst. 03[, 87 \(2000\).](https://doi.org/10.1142/S0219525900000078) [15] K. Sznajd-Weron and J. Sznajd, Opinion evolution in closed community, [Int. J. Mod. Phys. C](https://doi.org/10.1142/S0129183100000936) 11, 1157 (2000). [16] R. Axelrod, The dissemination of culture: A model with local convergence and global polarization, [J. Confl. Res](http://www.jstor.org/stable/174371)olut. 41[, 203 \(1997\).](http://www.jstor.org/stable/174371) [17] T. M. Liggett, Voter models, in [Stochastic Interact](https://doi.org/10.1007/978-3-662-03990-8_3)[ing Systems: Contact, Voter and Exclusion Processes](https://doi.org/10.1007/978-3-662-03990-8_3) (Springer Berlin Heidelberg, Berlin, Heidelberg, 1999) pp. 139–208. [18] V. Sood and S. Redner, Voter model on heterogeneous graphs, Phys. Rev. Lett. 94[, 178701 \(2005\).](https://doi.org/10.1103/PhysRevLett.94.178701) [19] B. L. Granovsky and N. Madras, The noisy voter model, [Stoch. Process. Their Appl.](https://doi.org/https://doi.org/10.1016/0304-4149(94)00035-R) 55, 23 (1995). [20] M. Mobilia, Does a single zealot affect an infinite group of voters?, Phys. Rev. Lett. 91[, 028701 \(2003\).](https://doi.org/10.1103/PhysRevLett.91.028701) [21] H.-U. Stark, C. J. Tessone, and F. Schweitzer, Decelerating microdynamics can accelerate macrodynamics in the voter model, Phys. Rev. Lett. 101[, 018701 \(2008\).](https://doi.org/10.1103/PhysRevLett.101.018701) [22] J. Fern´andez-Gracia, K. Suchecki, J. J. Ramasco,
- <span id="page-5-33"></span><span id="page-5-32"></span><span id="page-5-31"></span><span id="page-5-30"></span><span id="page-5-14"></span><span id="page-5-13"></span><span id="page-5-12"></span><span id="page-5-11"></span><span id="page-5-10"></span>M. San Miguel, and V. M. Egu´ıluz, Is the voter model a model for voters?, Phys. Rev. Lett. 112[, 158701 \(2014\).](https://doi.org/10.1103/PhysRevLett.112.158701) [23] S. Redner, Reality-inspired voter models: A mini-review,
- <span id="page-5-36"></span><span id="page-5-35"></span><span id="page-5-34"></span><span id="page-5-20"></span><span id="page-5-19"></span><span id="page-5-18"></span><span id="page-5-17"></span><span id="page-5-16"></span><span id="page-5-15"></span>C. R. Phys. 20[, 275 \(2019\).](https://doi.org/https://doi.org/10.1016/j.crhy.2019.05.004) [24] M. McPherson, L. Smith-Lovin, and J. M. Cook, Birds of a feather: Homophily in social networks, [Annu. Rev.](https://doi.org/https://doi.org/10.1146/annurev.soc.27.1.415) Sociol. 27[, 415 \(2001\).](https://doi.org/https://doi.org/10.1146/annurev.soc.27.1.415) [25] F. Heider, Attitudes and cognitive organization, [J. Psy](https://doi.org/10.1080/00223980.1946.9917275)chol. 21[, 107 \(1946\).](https://doi.org/10.1080/00223980.1946.9917275) [26] S. A. Marvel, S. H. Strogatz, and J. M. Kleinberg, Energy landscape of social balance, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.103.198701) 103, 198701 [\(2009\).](https://doi.org/10.1103/PhysRevLett.103.198701) [27] T. Minh Pham, I. Kondor, R. Hanel, and S. Thurner, The effect of social balance on social fragmentation, [J.](https://doi.org/10.1098/rsif.2020.0752)
- R. Soc. Interface 17[, 20200752 \(2020\).](https://doi.org/10.1098/rsif.2020.0752) [28] P. J. G´orski, K. Bochenina, J. A. Ho lyst, and R. M. D'Souza, Homophily based on few attributes can impede structural balance, Phys. Rev. Lett. 125[, 078302 \(2020\).](https://doi.org/10.1103/PhysRevLett.125.078302) [29] T. M. Pham, J. Korbel, R. Hanel, and S. Thurner, Empirical social triad statistics can be explained with dyadic homophylic interactions, PNAS 119[, e2121103119](https://doi.org/10.1073/pnas.2121103119) [\(2022\).](https://doi.org/10.1073/pnas.2121103119) [30] J. Korbel, S. D. Lindner, T. M. Pham, R. Hanel, and
  - S. Thurner, Homophily-based social group formation in a spin glass self-assembly framework, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.130.057401) 130[, 057401 \(2023\).](https://doi.org/10.1103/PhysRevLett.130.057401) [31] M. Galesic, H. Olsson, T. M. Pham, J. Sorger, and
  - S. Thurner, Experimental evidence confirms that triadic social balance can be achieved through dyadic interactions, [npj Complexity](https://doi.org/10.1038/s44260-024-00022-y) 2, 1 (2025). [32] M. W. Macy, B. K. Szymanski, and J. A. Ho lyst, The ising model celebrates a century of interdisciplinary contributions, [npj Complexity](https://doi.org/10.1038/s44260-024-00012-0) 1, 10 (2024). [33] P. Mullick and P. Sen, Sociophysics models inspired by the ising model, [The European Physical Journal B](https://doi.org/10.1140/epjb/s10051-025-01053-7) 98, [206 \(2025\).](https://doi.org/10.1140/epjb/s10051-025-01053-7) [34] M. Starnini, F. Baumann, T. Galla, D. Garcia,
  - G. I˜niguez, M. Karsai, J. Lorenz, and K. Sznajd-Weron, [Opinion dynamics: Statistical physics and be](https://arxiv.org/abs/2507.11521)[yond](https://arxiv.org/abs/2507.11521) (2025), [arXiv:2507.11521 \[physics.soc-ph\].](https://arxiv.org/abs/2507.11521) [35] G. Caldarelli, O. Artime, G. Fischetti, S. Guarino,
  - A. Nowak, F. Saracco, P. Holme, and M. de Domenico, [The physics of news, rumors, and opinions](https://arxiv.org/abs/2510.15053) (2025), [arXiv:2510.15053 \[physics.soc-ph\].](https://arxiv.org/abs/2510.15053) [36] S. Fortunato and C. Castellano, Scaling and universality in proportional elections, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.99.138701) 99, 138701 [\(2007\).](https://doi.org/10.1103/PhysRevLett.99.138701) [37] R. Pal, A. Kumar, and M. S. Santhanam, Universal statistics of competition in democratic elections, [Phys.](https://doi.org/10.1103/PhysRevLett.134.017401) Rev. Lett. 134[, 017401 \(2025\).](https://doi.org/10.1103/PhysRevLett.134.017401) [38] M. Tiwari, X. Yang, and S. Sen, Modeling the nonlinear effects of opinion kinematics in elections: A simple Ising model with random field-based study, [Physica A](https://doi.org/https://doi.org/10.1016/j.physa.2021.126287) 582, [126287 \(2021\).](https://doi.org/https://doi.org/10.1016/j.physa.2021.126287) [39] S. Thurner, R. Hanel, and P. Klimek, Introduction to the Theory of Complex Systems (Oxford University Press, 2018). [40] W. Weidlich, Physics and social science—the approach of synergetics, [Phys. Rep.](https://doi.org/10.1016/0370-1573(91)90024-G) 204, 1 (1991). [41] W. Weidlich and G. Haag, Concepts and models of a quantitative sociology: The dynamics of interacting populations, Vol. 14 (Springer Science & Business Media, 2012). [42] Y. Imry and S.-k. Ma, Random-field instability of the ordered state of continuous symmetry, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.35.1399) 35[, 1399 \(1975\).](https://doi.org/10.1103/PhysRevLett.35.1399) [43] J. Bricmont and A. Kupiainen, Lower critical dimension for the random-field Ising model, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.59.1829) 59, [1829 \(1987\).](https://doi.org/10.1103/PhysRevLett.59.1829) [44] N. G. Fytas, V. Mart´ın-Mayor, M. Picco, and N. Sourlas, Review of recent developments in the random-field Ising model, [J. Stat. Phys.](https://doi.org/10.1007/s10955-018-1955-7) 172, 665 (2018). [45] A. K. Hartmann and U. Nowak, Universality in three dimensional random-field ground states, [Eur. Phys. J. B](https://doi.org/10.1007/s100510050593) 7[, 105 \(1999\).](https://doi.org/10.1007/s100510050593) [46] J. Sinova and G. Canright, Nature and number of distinct phases in the random-field Ising model, [Phys. Rev. B](https://doi.org/10.1103/PhysRevB.64.094402) 64, [094402 \(2001\).](https://doi.org/10.1103/PhysRevB.64.094402) [47] N. G. Fytas and A. Malakis, Phase diagram of the 3d bimodal random-field Ising model, [Eur. Phys. J. B](https://doi.org/10.1140/epjb/e2008-00039-7) 61,

- [111 \(2008\).](https://doi.org/10.1140/epjb/e2008-00039-7) [48] A. Aharony, Tricritical points in systems with random fields, Phys. Rev. B 18[, 3318 \(1978\).](https://doi.org/10.1103/PhysRevB.18.3318) [49] I. Hadjiagapiou, The random-field Ising model with asymmetric bimodal probability distribution, [Physica A](https://doi.org/https://doi.org/10.1016/j.physa.2010.05.033) 389[, 3945 \(2010\).](https://doi.org/https://doi.org/10.1016/j.physa.2010.05.033) [50] S. Galam, Rational group decision making: A random field ising model at t = 0, Physica A 238[, 66 \(1997\).](https://doi.org/https://doi.org/10.1016/S0378-4371(96)00456-6) [51] J.-P. Bouchaud, Crises and collective socio-economic phenomena: Simple models and challenges, [J. Stat. Phys.](https://doi.org/10.1007/s10955-012-0687-3) 151[, 567 \(2013\).](https://doi.org/10.1007/s10955-012-0687-3) [52] S. P. Anderson and G. Glomm, Incumbency effects in political campaigns, [Public Choice](https://doi.org/10.1007/BF00140768) 74, 207 (1992). [53] A. Fowler, A Bayesian explanation for the effect of incumbency, [Elect. Stud.](https://doi.org/https://doi.org/10.1016/j.electstud.2018.03.005) 53, 66 (2018). [54] J. N. Druckman, M. J. Kifer, and M. Parkin, Campaign rhetoric and the incumbency advantage, [Am. Politics](https://doi.org/10.1177/1532673X18822314) Res. 48[, 22 \(2020\).](https://doi.org/10.1177/1532673X18822314) [55] A. V. Hirsch, Polarization and campaign spending in elections, J. Politics 85[, 240 \(2023\).](https://doi.org/10.1086/722045) [56] S. Iyengar, G. Sood, and Y. Lelkes, Affect, not ideology: A social identity perspective on polarization, [Public](https://doi.org/10.1093/poq/nfs038) Opin. Q. 76[, 405 \(2012\).](https://doi.org/10.1093/poq/nfs038) [57] Y. Lelkes, Mass polarization: Manifestations and measurements, [Public Opin. Q.](https://doi.org/10.1093/poq/nfw005) 80, 392 (2016). [58] S. Iyengar, Y. Lelkes, M. Levendusky, N. Malhotra, and
- <span id="page-6-12"></span><span id="page-6-11"></span><span id="page-6-10"></span><span id="page-6-9"></span><span id="page-6-8"></span><span id="page-6-7"></span><span id="page-6-6"></span>S. J. Westwood, The origins and consequences of affective polarization in the united states, [Annu. Rev. Poltical Sci.](https://doi.org/10.1146/annurev-polisci-051117-073034) 22[, 129 \(2019\).](https://doi.org/10.1146/annurev-polisci-051117-073034) [59] [https://www.fec.gov/.](https://www.fec.gov/) [60] A. Bonica, Database on ideology, money in politics, and elections (dime), <https://data.stanford.edu/dime> (2024), Stanford, CA. [61] A. Fouirnaies and A. B. Hall, The financial incumbency advantage: Causes and consequences, [J. Politics](https://doi.org/10.1017/S0022381614000139) 76, 711 [\(2014\).](https://doi.org/10.1017/S0022381614000139) [62] Pew Research Center, [The partisan divide on political](https://www.pewresearch.org/politics/2017/10/05/the-partisan-divide-on-political-values-grows-even-wider/) [values grows even wider](https://www.pewresearch.org/politics/2017/10/05/the-partisan-divide-on-political-values-grows-even-wider/) (2017). [63] G. C. Jacobson, It's nothing personal: The decline of the incumbency advantage in us house elections, [J. Politics](https://doi.org/10.1086/681670) 77[, 861 \(2015\).](https://doi.org/10.1086/681670) [64] W. J. Stone, S. A. Fulton, C. D. Maestas, and L. S. Maisel, Incumbency reconsidered: Prospects, strategic retirement, and incumbent quality in u.s. house elections,
- <span id="page-6-22"></span><span id="page-6-21"></span><span id="page-6-20"></span><span id="page-6-19"></span><span id="page-6-18"></span><span id="page-6-17"></span><span id="page-6-16"></span><span id="page-6-15"></span><span id="page-6-14"></span><span id="page-6-13"></span>J. Politics 72[, 178 \(2010\).](https://doi.org/10.1017/S0022381609990557) [65] D. Blankschtein, Y. Shapir, and A. Aharony, Potts models in random fields, Phys. Rev. B 29[, 1263 \(1984\).](https://doi.org/10.1103/PhysRevB.29.1263) [66] G. C. Jacobson, The effects of campaign spending in congressional elections, [Am. Political Sci. Rev.](https://doi.org/10.2307/1954105) 72, 469–491 [\(1978\).](https://doi.org/10.2307/1954105) [67] G. C. Jacobson, The effects of campaign spending in house elections: New evidence for old arguments, [Am.](http://www.jstor.org/stable/2111450)
- <span id="page-6-25"></span><span id="page-6-24"></span><span id="page-6-23"></span><span id="page-6-5"></span><span id="page-6-4"></span><span id="page-6-3"></span><span id="page-6-2"></span><span id="page-6-1"></span><span id="page-6-0"></span>[J. Political Sci.](http://www.jstor.org/stable/2111450) 34, 334 (1990). [68] R. S. Erikson and T. R. Palfrey, Equilibria in campaign spending games: Theory and data, [Am. Political Sci.](https://doi.org/10.2307/2585833) Rev. 94[, 595–609 \(2000\).](https://doi.org/10.2307/2585833) [69] K. E. Schnakenberg and I. R. Turner, Helping friends or influencing foes: Electoral and policy effects of campaign finance contributions, [Am. J. Political Sci.](https://doi.org/https://doi.org/10.1111/ajps.12534) 65, 88 (2021). [70] E. Avis, C. Ferraz, F. Finan, and C. Varj˜ao, Money and politics: The effects of campaign spending limits on political entry and competition, [Am. Econ. J. Appl. Econ.](https://doi.org/10.1257/app.20200296) 14[, 167–99 \(2022\).](https://doi.org/10.1257/app.20200296) [71] X. Lu, J. Gao, and B. K. Szymanski, The evolution of polarization in the legislative branch of government, [J.](https://doi.org/10.1098/rsif.2019.0010)
  - R. Soc. Interface 16[, 20190010 \(2019\).](https://doi.org/10.1098/rsif.2019.0010) [72] S. Thurner, M. Hofer, and J. Korbel, Why more social interactions lead to more polarization in societies, [PNAS](https://doi.org/10.1073/pnas.2517530122) 122[, e2517530122 \(2025\).](https://doi.org/10.1073/pnas.2517530122) [73] T. Pham, S. Redner, L. Waldorp, J. Armas, and H. L. J. van der Maas, [Polarisation in increasingly connected so](https://arxiv.org/abs/2503.24098)[cieties](https://arxiv.org/abs/2503.24098) (2025), [arXiv:2503.24098 \[physics.soc-ph\].](https://arxiv.org/abs/2503.24098) [74] A. Golan, L. S. Karp, and J. M. Perloff, Estimating Coke's and Pepsi's price and advertising strategies, [J.](https://doi.org/10.1080/07350015.2000.10524880) [Bus. Econ. Stat.](https://doi.org/10.1080/07350015.2000.10524880) 18, 398 (2000).

### END MATTER

<span id="page-7-0"></span>![](_page_7_Diagram_2.jpeg)

![](_page_7_Figure_3.jpeg)

FIG. 3: Illustration of the model of voters influenced by homophily and election campaign. Every individual has a binary opinion, expressing their voting preference. Everyone is following one of the political campaigns, while also being influenced by their local social environment (friends) in homophilic interactions with the neighbors in the social network.

<span id="page-7-1"></span>![](_page_7_Figure_5.jpeg)

FIG. 4: Emergence of campaign polarization in the US House of Representatives elections. We compare campaign spending and election results for races from 1980–2020, focusing on close contests with p = 0.5 ± 0.05. (a) Phase diagram as in Fig. [2,](#page-3-0) now covering the full range of spending, including the polarized region; the gray area marks races with close spending. (b) Election outcomes near h DEM ≈ h REP , where |h DEM − h REP | < \$100, 000. The x-axis shows average spending <sup>1</sup> 2 (h DEM + h REP ). Below hc, outcomes are mostly decisive, with only 39% close races (|m| < 0.1) and stronger incumbency effects. Above hc, over 70% of outcomes are near 50:50, consistent with RFIM predictions. (c) Percentage of close races where both campaigns exceed hc, i.e., within the polarized region π. This share rises sharply in 2018 and 2020.

<span id="page-8-0"></span>![](_page_8_Figure_1.jpeg)

FIG. 5: Estimation of model parameters for US House of Representatives for Republican-leaning races (p = 0.6 ± 0.05). Similarly to [2](#page-3-0) in the main text, we use the classification model for p = 0.6 to estimate the parameters of the model. (a) Classification model for T = 1 without hysteresis. (b) Classification model for T < 1 with incumbent region. (c) The plot of the election results with the campaign spending, with the incumbent region predicted by the optimal model. (d) The accuracy of the classification model in a range of temperatures; the star denotes the model with the best accuracy, corresponding to T <sup>⋆</sup> = 0.845.

<span id="page-8-1"></span>![](_page_8_Figure_3.jpeg)

FIG. 6: Estimation of model parameters for US House of Representatives for Democrat-leaning races (p = 0.4 ± 0.05). We use the classification model for p = 0.4 to estimate the parameters of the model. (a) Classification model for T = 1 without hysteresis. (b) Classification model for T < 1 with incumbent region. (c) The plot of the election results with the campaign spending, with the incumbent region predicted by the optimal model. (d) The accuracy of the classification model in a range of temperatures; the star denotes the model with the best accuracy, corresponding to T <sup>⋆</sup> = 0.865.

### SUPPLEMENTAL MATERIAL

### Detailed derivation of the self-consistency equation

We start with the Hamiltonian

H(s1, . . . , s<sup>N</sup> ) = −J X i<j Aij sis<sup>j</sup> − X i his<sup>i</sup> .

In order to decouple the Hamiltonian into the Hamiltonian for a single individual, we use the two approximations. The first one is the configuration model approximation, where we assume that the adjacency matrix of a random network can be approximated as Aij ≈ kik<sup>j</sup> N⟨k⟩ , where k<sup>i</sup> is the degree (i.e., connectivity) of the node i and ⟨k⟩ is the average degree. The second approximation we use is the mean-field approximation. Expressing the spin in terms of its average value as s<sup>i</sup> = ⟨si⟩ + δs<sup>i</sup> enables us to omit the term quadratic in fluctuations. By denoting the average magnetization as m = ⟨si⟩, we can rewrite the Hamiltonian as

H(s1, . . . , s<sup>N</sup> ) ≈ Jm<sup>2</sup>N⟨k⟩ 2 − J X i ⟨k⟩ ms<sup>i</sup> − X i his<sup>i</sup> .

The first term can be omitted from the Hamiltonian, as it is an additive constant of the energy and will be canceled when the equilibrium distribution is calculated. Thus, the mean-field Hamiltonian can be expressed as

HMF (s1, . . . , s<sup>N</sup> ) = − X i (Jm˜ + hi)s<sup>i</sup>

where J˜ = J⟨k⟩. Note that h<sup>i</sup> is a random variable with the distribution

p(hi) = pδ(h<sup>i</sup> − h <sup>+</sup>) + (1 − p)δ(h<sup>i</sup> + h <sup>−</sup>).

The equilibrium distribution is therefore

p(s|h <sup>±</sup>) = exp −β(Jm˜ ± h <sup>±</sup>)s /Z<sup>±</sup>

where β = 1 kT is the inverse temperature (we set k = 1), and

Z <sup>±</sup> = 2 cosh β(Jm˜ ± h ±) 

is the partition function. The average magnetization of spins coupled to external field ±h <sup>±</sup> is

m<sup>±</sup> = ⟨s⟩ <sup>±</sup> = X s=±1 sp(s|h <sup>±</sup>) = tanh β(Jm˜ ± h ±) .

The total magnetization can be expressed as

m = ⟨m⟩<sup>h</sup> = pm<sup>+</sup> + (1 − p)m<sup>−</sup> <sup>=</sup> <sup>p</sup> tanh β(Jm˜ + h +) + (1 <sup>−</sup> <sup>p</sup>) tanh β(Jm˜ − h −) .

## Derivation of the critical curve and tricritical point for symmetric case

Let us now focus on the symmetric case, i.e., when p = 1 2 and h <sup>+</sup> = h <sup>−</sup> ≡ h. We investigate how the phase diagram depends on the strength of the field and the temperature. Without loss of generality, we consider that J˜ = 1. To this end, we expand the right-hand side of the self-consistency equation around m = 0 and get

m = 1 − ξ 2 T m + 4ξ <sup>2</sup> − 3ξ <sup>4</sup> − 1 <sup>3</sup>T<sup>3</sup> <sup>m</sup><sup>3</sup> <sup>+</sup> <sup>O</sup>(m<sup>5</sup> )

where ξ ≡ tanh(h/T). This cubic equation has three solutions: one trivial m<sup>0</sup> = 0 and two non-trivial solutions

m<sup>±</sup> = ± p 3(1 − T − ξ 2) q T <sup>2</sup>+3ξ <sup>4</sup>−4ξ T <sup>2</sup> .

By comparing when the non-trivial solutions become trivial, i.e., m<sup>0</sup> = m±, we obtain the critical curve

<sup>h</sup><sup>c</sup> <sup>=</sup> <sup>T</sup>arctanh(√ 1 − T).

Finally, by plugging the critical curve into the self-consistency equation, we can determine the order of the phase transition from the sign of the third-order coefficient. The coefficient is along the critical curve equal to <sup>2</sup>−3<sup>T</sup> <sup>3</sup><sup>T</sup> <sup>2</sup> so the critical point where the phase transition changes its order is

T <sup>∗</sup> = 2 3 , h<sup>∗</sup> = 2 3 arctanh 1 √ 3 ≈ 0.439 .

# Derivation of the critical curve and tricritical point for the asymmetric case

Let us now focus on the general case when p ̸= 2 . We take the condition for m = 0, which is

p tanh(βh<sup>+</sup>) = (1 − p) tanh(βh<sup>−</sup>)

and expand the self-consistency equation

<sup>m</sup> <sup>=</sup> <sup>p</sup> tanh β(Jm˜ + h +) + (1 <sup>−</sup> <sup>p</sup>) tanh β(Jm˜ − h −) .

around m = 0 while keeping the dependence between h <sup>+</sup> and h <sup>−</sup> determined from the condition on m = 0 above. We use the Taylor expansion of tanh(β(m + h)) which is

tanh(β(m ± h <sup>±</sup>)) = ± tanh(βh<sup>±</sup>) + βm 1 − tanh<sup>2</sup> (βh<sup>±</sup>) ∓ β <sup>2</sup>m<sup>2</sup> tanh(βh<sup>±</sup>)(1 − tanh<sup>2</sup> (βh<sup>±</sup>)) + O(m<sup>3</sup> ).

By denoting ξ <sup>±</sup> = tanh(h <sup>±</sup>/T), one can rewrite the self-consistency equation as

m = p ξ <sup>+</sup> + m 1 − (ξ +) 2 T − m<sup>2</sup> ξ <sup>+</sup>(1 − (ξ +) 2 ) T<sup>2</sup> + (1 − p) −ξ <sup>−</sup> + m 1 − (ξ −) 2 T + m<sup>2</sup> ξ <sup>−</sup>(1 − (ξ −) 2 ) T<sup>2</sup> + O(m<sup>3</sup> ).

Since p ξ<sup>+</sup> − (1 − p) ξ <sup>−</sup> = 0, the constant term is zero. Therefore, we can rearrange the terms as

 T − p(1 − (ξ +) 2 ) − (1 − p)(1 − (ξ −) 2 ) T m + pξ<sup>+</sup>(1 − (ξ +) 2 ) − (1 − p)ξ <sup>−</sup>(1 − (ξ −) 2 ) T<sup>2</sup> m<sup>2</sup> = 0 .

The solution is therefore either m<sup>0</sup> = 0 or

m<sup>1</sup> = −T T − p(1 − (ξ +) 2 ) − (1 − p)(1 − (ξ −) 2 ) pξ<sup>+</sup>(1 − (ξ<sup>+</sup>) <sup>2</sup>) − (1 − p)ξ<sup>−</sup>(1 − (ξ<sup>−</sup>) 2)

.

Now, the critical point is given by the condition m<sup>1</sup> = m<sup>0</sup> ≡ 0, which is equivalent to

T = p(1 − (ξ + c ) 2 ) + (1 − p)(1 − (ξ − c ) 2 ).

By plugging in from the condition ξ <sup>−</sup> = p 1−p ξ <sup>+</sup>, we obtain

T = p(1 − (ξ + c ) 2 ) + (1 − p) " 1 − p 1 − p 2 (ξ + c ) 2 # = 1 − p 1 − p (ξ + c ) 2 .

By plugging back for the ξ + <sup>c</sup> = tanh(h + <sup>c</sup> /T), we can express h + <sup>c</sup> on T as

h + <sup>c</sup> <sup>=</sup> <sup>T</sup> arctanhr (1 − T) 1 − p p .

Similarly, by expressing h − c from the condition, we get that

h − <sup>c</sup> <sup>=</sup> <sup>T</sup> arctanhr (1 − T) p 1 − p .

#### Alternative derivation of the self-consistency equation from the Weidlich master-equation model

In this section, we show that the mean-field description used in the main text can alternatively be obtained from a master-equation approach to opinion dynamics, following the sociodynamics framework introduced by Weidlich and Haag. This demonstrates that the polarization transition does not rely on the Hamiltonian formulation with spatial interactions, but emerges generically from stochastic opinion switching driven by individual preferences and social adaptation.

Let us consider a population of N voters with binary opinions s<sup>i</sup> ∈ ±1. Let us define the number of voters with a positive opinion as n, and the fraction of voters with opinion s = +1 as x = n/N ∈ [0, 1]. The natural connection to the magnetization defined in the main paper is m = 2x − 1. The system undergoes a Markovian evolution described by a master equation, fully characterized by the transition rates W+1 → −1(n) ≡ W+<sup>−</sup>(n) and W−<sup>1</sup> <sup>→</sup> +1(n) ≡ W−+(n). The master equation can therefore be expressed as

dP(n) dt = (N − n + 1)W−+(n − 1)P(n − 1, t) + (n + 1)W+<sup>−</sup>(n + 1)P(n + 1, t) − [(N − n)W−+(n) + nW+<sup>−</sup>(n)]P(n, t).

In the classic formulation of sociodynamics, the individual opinion changes are governed by two conceptually distinct mechanisms. First, individuals possess intrinsic preferences that are independent of the current social configuration and may reflect long-standing inclinations, prior beliefs, or external information. In the election setting, this corresponds to the election campaign they follow

Second, individuals exhibit an adaptive response to the prevailing opinion, whereby the propensity to adopt a given opinion increases with its share of the population, reflecting conformity or social pressure. This mechanism is somewhat similar to the homophily, although it does not necessarily require the assumption on the spatial distribution of interactions. These preference and adaptation tendencies act simultaneously at the individual level and may have independent strengths. The particular choice that is widely used in sociodynamics literature is

W−+(n) = ν exp(θ + Kx), W+<sup>−</sup>(n) = ν exp(−(θ + Kx)),

where θ quantifies the former mechanism, while Kx the latter one. In our setting, θ represents the strength of the election campaign. Thus, in our scenario, we divide the population into two subpopulations, one following the campaign of s = +1 of size N <sup>+</sup> and the other following the campaign of s = −1 of size N <sup>−</sup>. We denote the number of individuals following the first campaign with a positive opinion as n <sup>+</sup> and analogously n <sup>−</sup>. The campaign intensities are θ <sup>+</sup> and −θ <sup>−</sup>, and the transition rates for gives subpopulations are therefore

W<sup>+</sup> <sup>−</sup>+(n <sup>+</sup>) = ν exp(θ <sup>+</sup> + Kx), W<sup>+</sup> <sup>+</sup><sup>−</sup>(n <sup>+</sup>) = ν exp(−(θ <sup>+</sup> + Kx)), W<sup>−</sup> <sup>−</sup>+(n <sup>−</sup>) = ν exp(−θ <sup>−</sup> + Kx), W<sup>−</sup> <sup>+</sup><sup>−</sup>(n <sup>−</sup>) = ν exp(−(−θ <sup>−</sup> + Kx)).

Here, individuals pursue their own campaigns but still seek to align with the majority of the population, regardless of the campaign. This is reflected by the term Kx. By calculating the first moment of the probability distribution from the master equation for each population in the case of N ≫ 1, we obtain

x˙ <sup>+</sup> = (1 − x <sup>+</sup>)νe<sup>θ</sup> <sup>+</sup>+Kx − x <sup>+</sup>νe−(<sup>θ</sup> <sup>+</sup>+Kx) , x˙ <sup>−</sup> = (1 − x <sup>−</sup>)νe−<sup>θ</sup> <sup>−</sup>+Kx − <sup>x</sup> <sup>−</sup>νe−(−<sup>θ</sup> <sup>−</sup>+Kx) .

At the stationary point, we obtain, after a straightforward calculation

x <sup>±</sup> = 1 2 -1 + tanh Kx ± θ ± .

By defining p = N <sup>+</sup>/N, we can rewrite normalization as x = px<sup>+</sup> + (1 − p)x <sup>−</sup>, and therefore we obtain

x = p 1 2 -1 + tanh(Kx + θ +) + (1 − p) 1 2 -1 + tanh(Kx − θ −) .

Using the relation m = 2x−1, the term Kx can be rewritten as Km <sup>2</sup> + K <sup>2</sup> where the constant contribution is absorbed into a redefinition of the effective fields. Thus, by choosing the following transformation

m = 2x − 1 , 2βJ˜ = K , βh<sup>+</sup> = θ <sup>+</sup> + K 2 , βh<sup>−</sup> = θ <sup>−</sup> − K 2 ,

we obtain the equation for m

<sup>m</sup> <sup>=</sup> <sup>p</sup> tanh β(Jm˜ + h +) + (1 <sup>−</sup> <sup>p</sup>) tanh β(Jm˜ − h −) 

which is exactly the self-consistency equation from the main text.

# Classification model

Here, we describe the classification models used in the main text. The classification model is directly based on the results of the Random Field Ising model. Without loss of generality, we assign h <sup>+</sup> = h REP as the spending of the Republican party candidate, h <sup>−</sup> = h DEM as the spending of the Democratic party candidate. The prediction of the classification model, based on the magnetization m goes as follows:

- If (h DEM, hREP ) lie in the hysteresis region, then the model predicts the incumbent as the winner.
- If (h DEM, hREP ) lie outside of the hysteresis region, or if there is an open seat (i.e., the incumbent does not run as a candidate), a Republican wins if m > 0, and a Democrat wins if m < 0.

Since, for the temperature T ≥ 1, we observe no hysteresis in the region, only the second condition applies. Specifically, when p = 0.5, the condition on the sign of magnetization m boils down to the condition whether h REP > hDEM (corresponding to m > 0) or the other way around. In this case, the classification model does not depend on temperature T (when T ≥ 1). We call this model the null model. This model catches the intuitive idea that in the case of equal campaign coverage, the candidate who spends more money on the campaign wins the election.

## Model accuracy

<span id="page-12-0"></span>In order to measure the performance of the classification model, we use the model accuracy. The confusion table between the predicted classification and the actual classification (here, the prediction is that a Republican candidate wins an election) is then defined in Tab. [I.](#page-12-0) The accuracy is defined as

ACC = nT P + nT N nT P + nT N + nF P + nF N .

TABLE I: Confusion table of the classification model.

#### McNemar test

<span id="page-13-0"></span>The McNemar test is used to demonstrate whether one of the two classification models used on a given data set is better than the other. For each observation, a classification model gives a predicted classification, which is compared with the actual classification. For example, in the election races, the classification model predicts the winner of the election based on the campaign spending and incumbency (see the second above), which is then compared with the actual election result. For two classification models M1,M2, the contingency table between correctly and incorrectly classified observations can be written as shown in Tab. [II.](#page-13-0)

TABLE II: Contingency table for the McNemar test.

The null hypothesis is that both marginals are the same, and therefore the probability that the first model is correct and the second model is wrong is the same as that the first model is wrong and the second model is correct. The McNemar test statistic is

χ <sup>2</sup> = (n<sup>12</sup> − n21) 2 n<sup>12</sup> + n<sup>21</sup> .

Under the assumption of the null hypothesis, and for large enough n<sup>12</sup> and n21, the statistic follows a χ <sup>2</sup> distribution with one degree of freedom. We can therefore reject the null hypothesis if the observed statistic is significant (i.e., the p-value is smaller than the desired statistical level).

# Calibration to US House election data for Republican-leaning races (p = 0.6 ± 0.05)

To illustrate the effectiveness of the classification model also on the case of a subset of races, we choose the races whose previous results were in the range corresponding to p = 0.6 ± 0.05. The subset consists of 1145 election races. We find the optimal classification model by finding T and h<sup>c</sup> that maximize accuracy. We find out that while the optimal parameters slightly change (T <sup>⋆</sup> = 0.845, h<sup>c</sup> = 2 million USD), the overall behavior does not change. We should also stress that since the smaller size of the subset, the statistical tests like the McNemar test exhibit a bit weaker (but still significant) value, which is caused by the fact that the number of points that are classified differently by the optimal model (T = T ⋆ ) and the null model (T = 1) is relatively low.

### Comparison of calibration of US House election data for different time periods

To exemplify the robustness of the method and to investigate some aspects of the time-dependence of the thermodynamic quantities, we divide the data into four decades and estimate the model parameters separately. Since the number of data points for the original range of p would be too small, we slightly increase it to p = 0.5 ± 0.1. The fits are shown in Fig. [7,](#page-14-0) specifically, the incumbency regions are depicted in Fig. [8;](#page-15-0) the estimated parameters, together with the accuracy and average spending in the respective period, are summarized in Table [III.](#page-14-1) We observe that the temperature is decreasing slightly over time, while the critical spending is increasing. We also observe that the number of incumbents winning despite spending less decreases over time. The accuracy remains almost constant; its slightly smaller value (compared to the values in the main text) is due to the wider region of p.

# Comparison of calibration of US House election data with a support vector machine model

Finally, we compare our method with a standard machine learning classification method, particularly the support vector machine. Again, we focus on the close races, i.e., all races with p = 0.5 ± 0.05. In order to utilize the natural

<span id="page-14-0"></span>![](_page_14_Figure_1.jpeg)

<span id="page-14-1"></span>FIG. 7: Comparison of fitted parameters for US House elections in four decades.

TABLE III: Summary of estimated temperature T, critical spending h<sup>c</sup> and accuracy for each decade.

symmetry of the system, i.e., h <sup>+</sup> = h <sup>−</sup> leading to m = 0, we transform the spending data into the following features:

σ<sup>h</sup> = h <sup>+</sup> + h − 2 , δ<sup>h</sup> = h <sup>+</sup> − h − .

We then use the linear SVM on quadratic features, which is equivalent to the degree-2 polynomial SVM. Additionally, we add a binary feature indicating whether the winner was an incumbent. Since the training data is very unbalanced, we had to upsample the data to approximately equalize the number of instances: more spending by the winner and less spending by the incumbent. The trained accuracy is very high (94%). By transforming the SVM back into the original space using

h <sup>+</sup> = σ<sup>h</sup> + δh/2 , h <sup>−</sup> = σ<sup>h</sup> − δh/2 .

<span id="page-15-0"></span>![](_page_15_Figure_1.jpeg)

FIG. 8: Comparison of fitted parameters for US House elections in four decades corresponding to the previous plots, focused on incumbency regions.

We transform the classifier into the original space. The fitted region is depicted in Fig. [9.](#page-16-0) By measuring the intersection of the incumbency region with the diagonal (h <sup>+</sup> = h <sup>−</sup>), we obtain the estimate for the equivalent of the critical threshold, which is here h <sup>∗</sup> = \$2.68M. This threshold is higher than predicted by the model in the main text. Furthermore, the accuracy on the whole dataset is lower (only 80%), possibly due to overfitting.

<span id="page-16-0"></span>![](_page_16_Figure_1.jpeg)

FIG. 9: Application of SVM to estimate the incumbency region.