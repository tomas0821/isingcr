# OPEN ACCESS

**Citation:** Mitra A (2026) Dirichlet-Swing: understanding spatio-temporal aspects of political elections in heterogeneous societies through agent-based simulation. PLoS One 21(3): e0344018. [https://doi.org/10.1371/](https://doi.org/10.1371/journal.pone.0344018) [journal.pone.0344018](https://doi.org/10.1371/journal.pone.0344018)

**Editor:** Omar El Deeb, The University of Warwick, UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND

**Received:** August 27, 2025

**Accepted:** February 13, 2026

**Published:** March 17, 2026

**Peer Review History:** PLOS recognizes the benefits of transparency in the peer review process; therefore, we enable the publication of all of the content of peer review and author responses alongside final, published articles. The editorial history of this article is available here: [https://doi.org/10.1371/journal.](https://doi.org/10.1371/journal.pone.0344018) [pone.0344018](https://doi.org/10.1371/journal.pone.0344018)

**Copyright:** © 2026 Adway Mitra. This is an open access article distributed under the terms of the [Creative Commons Attribution License](http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution,

#### RESEARCH ARTICLE

# **Dirichlet-Swing: understanding spatio-temporal aspects of political elections in heterogeneous societies through agent-based simulation**

**Adway Mitra** [\\*](#page-0-0)

Indian Institute of Technology Kharagpur, Paschim Medinipur, West Bengal, India

<span id="page-0-0"></span>\* [adway@ai.iitkgp.ac.in](mailto:adway@ai.iitkgp.ac.in)

# **Abstract**

![](_page_0_Picture_7.jpeg)

Many countries have a system of electing members to their governing bodies through district-based elections. In each district, the party with maximum votes wins the corresponding "seat" in the governing body. However, the final seat distribution is strongly dependent on the geographical distribution of voters of different parties, and the party with most (or least) voters may not win the most (or least) number of seats if their voters are non-homogeneously distributed over the districts. This is further complicated in heterogeneous societies, where political preference of voters depends on their social identities, which is also related to their districts of residence. Projections of outcomes by sample surveys tend to fail in such situations. The aim of this paper is to explore how electoral outcomes are influenced by the geographical distribution of voters and community-centric voting preferences. We consider agent-based modeling of voters along with their locations, community memberships and voting preference. Our models represent the relations between these factors with their uncertainties through conditional probability distributions involving latent variables with Dirichlet Processes. Our models also represent spatio-temporal factors in elections – how geographical proximity between districts influence the voting preferences, and swing of votes across successive elections. We propose two novel models for vote swing between successive elections based on Dirichlet Processes, which is far more powerful than the existing models of Uniform Swing and Proportional Swing. For any choice of parameters, our models can be used to simulate a full election by Monte Carlo Sampling, and such simulations provide us a range of possible outcomes. We can also simulate surveys and study how their projections can deviate from the actual results. We discuss inference approaches to estimate the parameters to fit the model to actual district-based elections held in India.

## **1 Introduction**

Many countries have a system of electing members to their governing bodies like parliament through district-based elections. In this system, the country is geographically divided into districts, and voters cast votes in their respective districts of residence. They vote in favor of any of the local candidates, who may belong to political parties. A common democratic setup is the district-based system in which the country is spatially divided into a number of regions called districts (or constituencies). There is a seat in the governing body corresponding to each district. The residents of each district elect a representative from a set of candidates, according to any voting rule (e.g., approval, ranked choice etc). In many countries, these candidates are representatives of political parties, and electors may cast their votes in favour of the parties rather than individual candidates. The winning candidate(s) is/are determined according to a scoring rule (e.g., plurality, Borda count etc). The winning candidate's party is considered to have won the corresponding seat in the governing body. The election results are understood in terms of the number of seats won by different parties, rather than the total number of votes obtained by them.

<span id="page-1-7"></span><span id="page-1-6"></span><span id="page-1-5"></span><span id="page-1-4"></span><span id="page-1-3"></span><span id="page-1-2"></span><span id="page-1-1"></span><span id="page-1-0"></span>The relation between relative popularity of the different parties (as reflected by their aggregate vote shares) and the number of seats won by them in an election is a crucial and puzzling issue in Political Sciences, as analyzed by [\[1\]](#page-20-0). If the relative popularity of the different parties is spatially homogeneous across all the districts, then the most popular party may win all the seats. But this is very rarely the case. One reason for this may be the individual popularity of candidates may vary across districts, which may influence the voting decisions more than popularity of the parties. But a more complex reason is the spatial variation of demography across the country, since the popularity of different parties often varies with demography [[2](#page-20-1)]. Demographics vary spatially as people usually prefer to choose residences based on social identities, such as race, religion, language, caste, profession and economic status. This process is sometimes called "ghettoization," where people with similar social identities huddle together in geographical regions [\[3](#page-20-2),[4](#page-20-3)]. Such spatial heterogeneity plays a very important role in district-based elections if different political parties represent the interests of different social groups. Even if a political party is not popular overall, it can win a few seats if its supporters are densely concentrated in a small number of districts, which forms strongholds of the party. On the other hand, a party which is overall quite popular, may fail to win many seats if its supporters are spread all over without concentration. Also, electors often vote according to the advice of local community leaders and other local factors [[5\]](#page-20-4), which causes "polarization" of voters in favour of one/two parties inside each district. There are relatively few statistical models for simulation of district-based elections. Eggenberger and Polya used the concept of Polya's urn to propose a statistical voting model, which simulates the effect that if one candidate gets a vote, there are likely to get more [\[6\]](#page-20-5). There have been attempts to extend these to multiple districts [\[7\]](#page-20-6). Another popular approach is Mallow's Model, which assumes a 'central' ranking over the candidates, and simulates individual votes by perturbing it. The impact of spatial distribution of voters on district-based elections have been studied by [[8–](#page-21-0)[10](#page-21-1)] in an analytical framework.

and reproduction in any medium, provided the original author and source are credited.

**Data availability statement:** The data used here can be found in the official website of the Election Commission of India: [https://www.](https://www.eci.gov.in/statistical-reports) [eci.gov.in/statistical-reports.](https://www.eci.gov.in/statistical-reports) In case the above link does not work, here is the link to the data extracted from the above website for the 4 specific elections that have been considered in this paper (GJ17, GJ22, WB19, WB21). [https://](https://zenodo.org/records/18207734) [zenodo.org/records/18207734](https://zenodo.org/records/18207734). The relevant file in this repository is IndiaElection\_WB\_ GJ.xlsx The names of the parties have been anonymized.

**Funding:** This study was supported by Indian Institute of Technology Kharagpur in the form of a salary for A.M. The specific roles of this author are articulated in the 'author contributions' section. The funders had no role in study design, data collection and analysis, decision to publish, or preparation of the manuscript.

**Competing interests:** The author has declared that no competing interests exist.

<span id="page-2-0"></span>Though the aim of these works is to study *gerrymandering* (i.e., changing district boundaries to favor a party), they add a model to simulate the geographical distribution of voters. The work [[1](#page-20-0)] studies *misrepresentation ratio*, a measure of distortion in the outcome due to the geographical distribution of voters. In this study, some simple models of probabilistic election simulation are used to back their theoretical results.

When successive elections are held in a demographic polity over regular intervals, they may or may not produce similar results. Outcomes of elections may change as the overall popularity of the parties may change due to contemporary factors. It can also happen that a party loses popularity within some segments of the population, but gains popularity in other segments. The change of popularity between successive elections is known as *vote swing*. One well-known model of vote swing is *uniform swing*, which assumes that the swing is similar in all the districts, which may result in a surge in favor of a party all over the country. Another model is *proportional swing*. The work [\[11](#page-21-2)] lays down an axiomatic definition of swing models, and consider alternative models based on a function that relates the swing in each district to the overall swing. Another work [\[12\]](#page-21-3) focuses at voter level, as it tries to predict the behavior of *swing voters* based on factors influencing the voting decisions at the last minute.

<span id="page-2-2"></span><span id="page-2-1"></span>Surveys are often carried out to forecast the election results. These surveys may be conducted by various agencies before or after the election. Usually a survey involves a small sample of the electorate, based on whose responses the vote share of the different parties is estimated. The number of seats to be won by the different parties can be estimated as well from this sample. However, the accuracy of these estimates depends on how well these samples represent the entire population. For example, the chosen samples may cover only a few districts, or misrepresent the true vote share of the different parties. This may arise either due to practical constraints (such as the difficulty of reaching certain geographical areas) or due to malicious intent or partisan bias of the survey agency. Furthermore, if a party is popular among some communities but unpopular among other communities, and the communities are unevenly distributed across districts, then such surveys will find it very difficult to predict the results accurately. These issues give rise to an important question: given a particular election, how likely is a particular survey to project the correct outcome in terms of seat distribution?

<span id="page-2-4"></span><span id="page-2-3"></span>A significant amount of research work exists in predicting the election results from a survey under different conditions. Most of these works like [[13](#page-21-4)–[17\]](#page-21-5) focus on finding the minimum number of samples needed by a survey to forecast the winner and/or the margin of victory with a given confidence, and efficient algorithms for the same. [[18](#page-21-6)] extends this analysis to district-based settings, and provides algorithms to carry out the survey over a limited number of districts and a limited number of persons in each district. However, none of these works, to the best of our knowledge, predict the number of seats won by the parties in either deterministic or probabilistic way. One of the few works which attempts an alternative statistical approach based on regression and stratified sampling to forecast election results based on surveys is [[19](#page-21-7)], who also apply their framework to forecast the Indian General Election 2019 using surveys conducted through Amazon Mechanical Turk in addition to socio-economic data of voters and their voting preferences. However, this work uses the Uniform Swing theory to convert their vote share projections to seat share projections.

<span id="page-2-6"></span><span id="page-2-5"></span>One of the few research works using agent-based modeling for elections [\[20](#page-21-8)], where ABMs are used to forecast election outcomes. In this work, the authors use various attributes like age, gender etc of voters to predict their votes. The work also considers live experiments for election forecasting, where surveys are augmented by agent-based models. However, this work is not aimed at district-based elections.

The aims of this work are four-fold. First of all, we attempt to estimate the possible number of seats won by different parties. Secondly, we study the spatial correlation of results across districts, and attempt to incorporate it in our models. Third, we study the spatial variation of swing in results across successive elections, and provide a novel treatment for it. Our final aim is to evaluate the above for actual district-based political elections held in India, for which we need to solve a parameter estimation problem, and we propose ways of doing so.

<span id="page-3-0"></span>Our approach depends heavily on the simulation of election outcomes. Recently, there have been attempts to systematically represent various aspects of district-based elections through voter-centric agent-based statistical models [[21](#page-21-9)[–23\]](#page-21-10). In this work, we utilize some of these models to simulate complete election results, by considering every elector's vote as a latent random variable. We aim to capture different voting trends seen in societies through these models. When it comes to vote swings in elections, uniform swing and proportional swing are unable to explain the situation when a party loses votes overall, but manages to win a few new seats. We present models based on Dirichlet Processes for this purpose. Our next target is to study election surveys and projection of results based on them. We build upon the model to simulate surveys developed by [\[24](#page-21-11)], and carry out further analysis on the limitations of survey strategies to predict election results. Our simulations suggest an important result – it is generally more sample-efficient to estimate the swing with respect to the past election than to directly estimate the results of the current election.

# **2 Notations and problem definition**

We consider district-based 1-plurality elections, i.e., the candidate/party with maximum votes in a district wins the corresponding seat. Consider *N* voters divided among *S* districts as {*N*1, *...* , *NS*}. There are *K* parties in fray, each of whom has a candidate in each district. Denote by *Z* the **complete election**, where *Z* ={*Z*1, *Z*2, *...* , *ZS*} where *Zs* ={*Zs*1, *...* , *ZsK*} denotes the total number of votes of the parties in district *s*.

For each district *s*, we denote by *θ<sup>s</sup>* ={*θs*1, *...* , *θsK*} as the local vote share. Clearly, *θsk* = *Zsk Ns* . Again, *<sup>θ</sup>* ={*θ*1, *...* , *<sup>θ</sup>K*} denotes the overall vote shares of the parties, where *θ<sup>k</sup>* = ∑ *<sup>k</sup> Zsk <sup>N</sup>* .

Denote by *Us*, the winning party in district *s*, and by *Wk*, the number of districts where the candidate from party *k* is the winner. Clearly, ∑ *<sup>k</sup> Wk* = *S*. Finally, denote by *X*: the actual electoral outcome. It has two parts: *X* ={*X*1, *X*2} where *X*<sup>1</sup> ={*θ*1, *...* , *θK*}, and *X*<sup>2</sup> ={ *<sup>W</sup>*<sup>1</sup> *<sup>S</sup>* , *...* , *WK <sup>S</sup>* }, i.e., the vote shares and seat shares of the parties.

An election is defined by *Z*, since the overall vote share and seat share of all parties can be easily calculated from it. *Z* is a combinatorial structure, as each *Zs* specifies a *K*-way partition of *Ns*. However, not all partitions are equally likely (for example, it is very unlikely that all voters in a district vote for the same party). An election simulation model considers *Z* as a random variable, and attempts to specify a probability distribution over it. But since it is difficult to define a distribution over such a complex structure, it can be implicitly at voter level, through random variable *Vsi* which indicates the vote by the *i*-th voter of district *s*. This is the approach of *Agent-based Modeling*, where each voter is considered as an agent. Clearly, *Zsk* <sup>=</sup> ∑*Ns <sup>i</sup>*=1 *I*(*Vsi* = *k*), where *I* denotes the indicator variable. One of our aims in this paper is to understand the distribution over *Z* that is represented by the models, and to compare it with actual district-based elections in India. This analysis can establish how realistic our models are. Another aim is to study the distribution of the election outcome *X* (which is a function of *Z*) as induced by the simulation model.

Denote by *Y*: the projected results based on the surveys, which also has two parts: {*Y*1, *Y*2} which are the projected vote shares and seat shares of all the parties. A survey model simulates *Z*ˆ from *Z*, by drawing samples of voters from a random subset of the districts and querying their votes. *Y* is obtained by estimating the vote and seat shares from *Z*ˆ and extrapolating them to the whole electorate. However, *Y* can be very different from *X*, if *Z*ˆ is not a good representative of *Z*. Another aim of this paper is to study the distribution of *Y* under sampling strategies conditioned on *Z*, i.e., to study how likely a survey is to predict the correct outcome of a particular election.

A schematic diagram of the entire process flow is provided in [Fig 1](#page-4-0).

## **3 Agent-based models**

We will now discuss a series of agent-based models to simulate voter behavior. These models proceed by assigning political preferences and locations to each voter by sampling from suitable probability distributions, and using these to simulate the election.

![](_page_4_Diagram_1.jpeg)

## **3.1 Spatial distribution models**

<span id="page-4-1"></span>Earlier works like [\[21](#page-21-9)[,22](#page-21-12),[25](#page-21-13)] introduced some agent-based voter models like the District-wise Polarization Model (DPM) and Partywise Concentration Model (PCM). The DPM model aims to represent the fact that many voters prefer to vote based on local factors, rather than overall popularity of the different parties. In DPM model, each vote is simulated by sampling from either the overall or the local popularity (vote share) of the parties, which is decided by a Bernoulli distribution with a concentration parameter *α*. High value of *α* suggests more importance of local popularity than overall, which allows parties which are less popular to win some seats. Low value of *α*, on the other hand, tends to preserve the overall popularity trends in each district, hence the most popular party is likely to win most seats.

<span id="page-4-3"></span>*prob*(*Vsi* <sup>=</sup> *<sup>k</sup>*) *∝* (*αsθsk* + (1 – *<sup>α</sup>s*)*θk*) (1)

<span id="page-4-2"></span>The PCM model, also discussed in [\[22](#page-21-12),[25\]](#page-21-13) aims to represent the geographical variation in concentration of voters of each party. Here, each voter of each party *k* is stochastically assigned to a district, based on the logic that they are more likely to be assigned to a district where that party is already popular, but this likeliness is again controlled by a concentration parameter *η<sup>k</sup>*

. This is supposed to represent the phenomena that supporters of a party tend to be residing closely, as political partisanship often depends on demographics or community membership. So in this model, we do not simulate *Vsi* directly, but rather sample the vote *Vi* for voter *i* based on overall vote shares, and then assign them to a district *Di* as discussed above.

*prob*(*Vi* <sup>=</sup> *<sup>k</sup>*) *∝ <sup>θ</sup><sup>k</sup> prob*(*Di* <sup>=</sup> *<sup>s</sup>*|*Vi* <sup>=</sup> *<sup>k</sup>*) *∝* (*ηkθsk* + (1 – *<sup>η</sup>k*)*U*(1, *<sup>K</sup>*)) (2)

The power of this model is that *ηk* is specific to parties, so different parties can have different levels of concentration, thereby allowing a wider range of possibilities on *Z*. In general, high concentration is useful for parties with low vote share as it enables them to win seats, but parties with higher vote share may win more seats if their votes are less concentrated spatially.

<span id="page-4-0"></span>**Fig 1. A schematic diagram of the process flow in this paper, showing the different types of models, including their inputs and outputs.** <https://doi.org/10.1371/journal.pone.0344018.g001>

It may be noted that the conditional distributions of both the above models are related to the famous Chinese Restaurant Process [[26\]](#page-21-14), which is a derivative of Dirichlet Processes. It follows the logic of *rich-getting-richer*, i.e., a voter is more likely to vote for a candidate who is already popular (in case of DPM), or likely to reside in a district where there are already many voters of the same party (in case of PCM).

#### **3.2 District geography model**

When two districts are geographically aligned, studies like [\[27](#page-21-15)] show that their voting patterns are quite similar. Accordingly, we aim develop models that consider that the districts are geographically located, and for each district there is a set of neighboring districts. We re-cast the DPM and PCM models in this scenario. In case of DPM model, we consider that the popularity of different parties in each district is influenced not just by their overall popularity, but also by the popularity in the neighboring districts. For any district *s*, *ϕ*(*s*) denotes the districts that are geographical neighbors of *s*. We add an extra parameter *β*, which indicates the influence of the neighboring districts. Accordingly, we add another term to the conditional distribution of the DPM model:

*prob*(*Vsi* <sup>=</sup> *<sup>k</sup>*) *∝ <sup>α</sup>sθsk* <sup>+</sup> *<sup>β</sup>s*(1 – *<sup>α</sup>s*)*θϕ*(*s*)*<sup>k</sup>* + (1 – *<sup>α</sup>s*)(1 – *<sup>β</sup>s*)*θ<sup>k</sup>* (3)

Here, *nϕ*(*s*)*k* indicates the average share of votes for party *k* in the neighboring districts of *s*. Clearly, both *α*, *<sup>β</sup> ∈* (0, 1). Also, high value of *β* indicates a stronger influence of neighboring regions, indicating that a party's votes in any district will be more correlated with its votes in the neighboring districts. We call this new model as Geography-augmented District Polarization Model (GDPM).

In case of PCM model, when the assignment of voters to districts is dictated not only by the popularity of parties in those districts, but also to neighboring districts. Once again, we add a new parameter *β* to include the impact of neighboring districts into the probability of assigning voter *i* to district *s*. We add a term to the conditional distribution that is related to the average vote share of the same party *k* in the neighboring districts *ϕ*(*s*) of *s*.

<span id="page-5-0"></span>*prob*(*Vi* <sup>=</sup> *<sup>k</sup>*) *∝ <sup>θ</sup><sup>k</sup> prob*(*Di* <sup>=</sup> *<sup>s</sup>*|*Vi* <sup>=</sup> *<sup>k</sup>*) *∝ <sup>η</sup>kθsk* <sup>+</sup> *<sup>β</sup>kθϕ*(*s*)*<sup>k</sup>* + (1 – *<sup>β</sup>k*)(1 – *<sup>η</sup>k*)*U*(1, *<sup>K</sup>*) (4)

Once again, a high value of *β* indicates that voters of any party tend to reside in nearby districts. This version of the model will be called as Geography-augmented Partywise Concentratation Model (GPCM).

#### **3.3 Social identity model**

<span id="page-5-1"></span>Apart from geographical proximity, another major factor that is known to influence voting patterns is community membership. Studies like [\[27](#page-21-15)] have shown that people belonging to the same social community tend to exhibit similar voting patterns, even if they belong to districts that are geographically far apart. Now, we present another model where the social communities and their political preferences are directly parameterized. Assume that there are *C* social communities, and *κc* denotes the proportion of the electorate from community *c*. To every voter *i*, we assign their community as *<sup>C</sup>*(*i*) *∼ Categorical*(*κ*) (*<sup>κ</sup>* ={*κ*1, *...* , *<sup>κ</sup>C*}). Voters from the same community tend to reside in the same district. Voter *i* is assigned to district *D*(*i*) by following a Chinese Restaurant Process [[26\]](#page-21-14) with parameter *ηc*. Voter *i* from community *C*(*i*)= *c* is assigned to district *s* with probability proportional to *η<sup>c</sup>* ∑*i*–1 *<sup>j</sup>*=1 *I*(*C*(*j*)= *c*)*I*(*S*(*j*)= *s*) (i.e., number of voters from same community as *i* already residing in district *s*), or to any district chosen uniformly at random with probability proportional to (1 – *ηc*). This ensures that for each community, certain districts turn into strongholds. Note that this is very similar to PCM, with the exception that we are considering community memberships instead of political preference in assigning voters to districts.

Each community is associated with a prior over the political preferences of its members. For community *c* and party *k*, we assign Φ*ck ∈* {–1, 0, 1}, indicating if the relation between them is bad (−1), neutral (0) or good (1). Also, a variance *σk* is associated with each party (which may be drawn from a Gamma prior with parameters specific to the party). Finally, for each voter *i*, their valuation of party *k* is denoted by *λik ∼N* (Φ*ck*, *<sup>σ</sup>k*) where *<sup>c</sup>* <sup>=</sup> *<sup>C</sup>*(*i*). A party with high *σ* is strongly liked by some voters and strongly disliked by other voters across communities (indicating its "polarizing" nature), but for a party with low value of *σ*, most members of each community have similar values. Clearly, this valuation *λik* can be either positive or negative. While these valuations definitely influence each voter's voting choice, voters may also get influenced their social network. The *i*-th voter combines their own valuations *λik* with the mean valuations of other voters in the same district, as *λ*ˆ*ik* = *µλik* + (1 – *µ*)*λ*¯*ik* where *λ*¯*ik* = ∑*N <sup>j</sup>*=1 *I*(*S*(*j*)=*S*(*i*))*λjk* ∑*N <sup>j</sup>*=1 *<sup>I</sup>*(*S*(*j*)=*S*(*i*)) , and *<sup>µ</sup> ∼ Beta*(*a*, *<sup>b</sup>*). This local influence is independent of community affiliation. Finally, voter *i* casts their vote *Vi* in favor of the party for which their moderated valuation *λ*¯*i* is maximum.

In a nutshell, the election model may be written as:

*<sup>C</sup>*(*i*) *∼ Categorical*(*κ*)*∀<sup>i</sup> ∈* {1, *<sup>N</sup>*} *<sup>D</sup>*(*i*) *∼ CRP*(*C*, *<sup>η</sup>*)*∀<sup>i</sup>*, *<sup>σ</sup><sup>k</sup> ∼ Gamma*(*γk*)*∀<sup>k</sup> <sup>λ</sup>ik ∼N* (*ϕck*, *<sup>σ</sup>k*) where *<sup>c</sup>* <sup>=</sup> *<sup>C</sup>*(*i*), *∀<sup>i</sup>*, *<sup>k</sup> <sup>µ</sup> ∼ Beta*(*a*, *<sup>b</sup>*), *<sup>λ</sup>*ˆ*ik* <sup>=</sup> *µλik* + (1 – *<sup>µ</sup>*)*λ*¯*ik∀<sup>i</sup>*, *<sup>k</sup>* where *λ*¯*ik* = ∑*N <sup>j</sup>*=1 *I*(*D*(*j*)= *D*(*i*))*λjk* ∑*N <sup>j</sup>*=1 *I*(*D*(*j*)= *D*(*i*)) *Vi* = *argmaxkλ*¯*ik* (5)

It may be noted that while DPM and PCM require the overall vote share *θ* (*X*<sup>1</sup> ) and concentration parameter *α* or *η* as input, the SIM takes parameters *κ*, *η*, *ϕ*, *σ* as the inputs to generate the full result *Z*. From this, both *X*<sup>1</sup> and *X*2 can be easily calculated.

Once again, we can consider a Geography-augmented version of the SIM (GSIM), where the assignment of voter *i* to any district *s* considers not only the number of members of the same community in district *s*, but also in the neighboring districts. This encourages the members of each community to reside in geographical clusters, which may span multiple districts. Once again, this is realistic in most societies.

A summary of all of these models is provided in [Fig 2.](#page-7-0)

## **4 Modeling vote swing across elections**

Elections are not one-time events, but are held regularly, at regular intervals. When we analyze one election, it is natural to compare and contrast the results of one election with the next – which party gained/lost how many votes and/or seats. The change in vote shares *θ*(*t*) and *θ*(*t* + 1) between successive elections is referred to as *swing*. We denote it by ∆*θ*(*t*)= *θ*(*t* + 1) – *θ*(*t*).

Clearly, the above definition is related to change in overall vote share across the country. However, to understood how this translates to changes in seat distribution, we need to understand the swings at district level, as denoted by ∆*θs*(*t*)= *<sup>θ</sup>s*(*<sup>t</sup>* + 1) – *<sup>θ</sup>s*(*t*). The question is, how is ∆*θs*(*t*) related to ∆*θ*(*t*)? Clearly, ∆*θ*(*t*)= ∑ *s ns <sup>N</sup>* ∆*θs*(*t*), and hence *E*(∆*θs*(*t*)) = *E*(∆*θ*(*t*)). As already mentioned, the most common model assumes uniform swing, i.e., ∆*θs*(*t*)= ∆*θ*(*t*). However, as will be illustrated in the Experiments section, in many elections we find that a party improves its vote share in some districts even as it loses votes overall. This cannot be explained by either the Uniform or the Proportional Swing Theories. In this work, we have proposed two models of swing.

#### **4.1 Dirichlet swing model**

<span id="page-7-1"></span>First, we consider a Dirichlet Process Mixture Model [[28\]](#page-21-16) for vote swing. We note that ∑ *<sup>k</sup>* ∆*θk*(*t*)=0, as the gain in vote share of some parties is offset by loss of the others, and ∑ *<sup>k</sup> θ*(*t*)=1. So there is no standard probability distribution that can be used to model ∆*θ*(*t*). However, if we make the assumption that |∆*kθ*(*t*)| < <sup>1</sup> *<sup>K</sup>* , i.e., no party's vote share swings by more than <sup>1</sup> *<sup>K</sup>* , then we can consider a new variable ∆ˆ*kθ*(*t*)= <sup>∆</sup>*kθ*(*t*)+ <sup>1</sup> *<sup>K</sup>*. Here, ∆ˆ *<sup>θ</sup>*(*t*) lies on the (*K* – 1)-simplex, i.e., it can be considered as a *K*-categorical Probability Mass Function. Naturally, we can model ∆ˆ *θ*(*t*) with a Dirichlet Distribution.

Specifically, we consider a swing prior ∆ˆ *θ*0(*t*) which follows a Dirichlet Process with a base distribution *H* and parameters *γ*0. We choose *H* to be a Dirichlet Distribution with parameters *ν* ={*ν*1, *...* , *νK*}. Hence, every *atom* drawn from this base distribution is a *K*-categorical PMF, and ∆ˆ *θ*0(*t*) is a discrete mixture distribution over such *atoms*. The weights of each atom is obtained by a stick-breaking process (GEM) with parameter *γ*0. The swing in each district is one of these atoms, drawn from ∆ˆ *θ*0(*t*).

∆ˆ *<sup>θ</sup>*0(*t*) *∼ DP*(*H*, *<sup>γ</sup>*0) ∆ˆ *<sup>θ</sup>s*(*t*) *∼ Categorical*(∆ˆ *<sup>θ</sup>*0(*t*)) *<sup>θ</sup>s*(*<sup>t</sup>* + 1) = *<sup>θ</sup>s*(*t*)+ <sup>∆</sup>*θs*(*t*), where <sup>∆</sup>*θsk*(*t*)= ∆ˆ *<sup>θ</sup>sk*(*t*)– <sup>1</sup> *K* (6)

Note that the overall swing ∆*θ*(*t*) is not explicitly included in the model, but it can be calculated from the district-wise swings.

The hyperparameters *ν* and *γ*0 are very vital in this construct. A low value of *γ*0 indicates that the stick-breaking process will attach small weights to each atom. So when samples are drawn from the mixture distribution ∆ˆ *θ*0(*t*), they are likely to

<span id="page-7-0"></span>**Fig 2. A summary of the different models proposed in this paper.**

be all distinct, i.e., different districts will have different swings. On the other hand, a large value of *γ*0 suggests that one atom can have a large weight, i.e., most districts will have the same swing, which is similar to the Uniform Swing Theory. The Dirichlet hyperparameters *ν*, on the other hand, are estimators of the overall swing, since *E*(ˆ*θk*(*t*)) = *<sup>E</sup>*(ˆ*θsk*(*t*)) = ∑*<sup>ν</sup><sup>k</sup> <sup>j</sup> ν<sup>j</sup>* . However, it can be shown that high magnitudes of *νk* promote low variance of ˆ*θsk*(*t*), i.e., most district-wise swings will be similar. But low values of *νk* promote high variance of ˆ*θsk*(*t*), suggesting the different districts can have very different swings.

## **4.2 Dirichlet swing matrix model**

Next, we consider a more sophisticated model based on the swing matrix, that accounts for how the voters of party *k* in the previous election, voted in the current election. In other words, we attempt to parameterize the quantity *Mskl*(*t*)= *<sup>p</sup>*(*Vsi*(*<sup>t</sup>* + 1) = *<sup>l</sup>*|*Vsi*(*t*)= *<sup>k</sup>*). We define a transition matrix *Ms*(*t*) of size *<sup>K</sup> × <sup>K</sup>*, where each row is a PMF corresponding to the voters of party *k* in the previous election. For any party *k*, we first define a latent prior *M*<sup>0</sup> *<sup>k</sup>*, based on which the party's transition matrix in any district *s* is defined. Once again, this is modeled through a Dirichlet Process, as below:

*M*0 *<sup>k</sup>* (*t*) *∼ DP*(*Hk*, *<sup>γ</sup>k*)*∀<sup>k</sup> ∈* {1, *<sup>K</sup>*} *Msk*(*t*) *∼ Categorical*(*M*<sup>0</sup> *<sup>k</sup>* (*t*))*∀<sup>s</sup> ∈* {1, *<sup>S</sup>*}, *∀<sup>k</sup> ∈* {1, *<sup>K</sup>*} *Vsi*(*<sup>t</sup>* + 1) *∼ Categorical*(*Msk*(*t*))*∀<sup>i</sup> ∈* {1, *ns*} where *<sup>k</sup>* <sup>=</sup> *Vsi*(*t*) (7)

Clearly, the base distribution *Hk* is a Dirichlet distribution specific to party *k*, with parameters {*ρk*1, *...* , *ρkK*}. Usually, *ρkk* will be higher than the rest, as most voters of party *k* in previous election are likely to stick to the same party in the current election too. Each atom drawn from the base distribution is a transition distribution for the previous voters of party *k*, and for each district *s*, we draw a one such atom from the mixture distribution *M*<sup>0</sup> *<sup>k</sup>* (*t*). Once again, low magnitudes of *ρ* promote high variance across the districts, while high magnitudes encourage similar behavior across all districts. This model is inspired by previous models like [\[29](#page-21-17)[,30](#page-21-18)] that considers transition matrix of voter preferences, and develops maximum-likelihood estimates of this matrix. However, we not only extend this idea to district-based elections, but also propose a generative model for the transition matrix.

<span id="page-8-0"></span>A summary of all of these models is provided in [Fig 2.](#page-7-0)

## **5 Exploring the outcome space**

Having defined the models, we now conduct a series of simulation studies based on these models. These simulations are done in an idealized, synthetic setting with *N* = 10000000, *S* = 100. The districts are considered to be of equal population, and arranged in the form of an uniform square grids with neighborhoods defined accordingly. We study the impacts of varying the different parameters on the outcomes in case of the different models.

## **5.1 Vote share vs seat share**

In this experiment, we explore how a certain vote share can translate into seat shares. For this, we consider 3 different values of vote shares for *K* =2, *K* =3 and *K* =4, and run the DPM and PCM under different settings of their parameters *α* and *η* to obtain the seat shares. The numbers reported are averaged over 10 runs over each setting, and the standard deviation is also reported. The results are shown in [Table 1](#page-9-0). We find that while the most popular party (highest vote share) can win nearly all the seats in some settings, it may be able to win just above half the seats in some other settings, if the voters of the parties are spatially more concentrated, as indicated by higher values of *α* and *η*.

For the GDPM and GPCM models, for suitable choice of the spatial coherence parameter *β*, the seat distribution over parties may remain the same as those of DPM and PCM, but their geographical distribution changes, as we see adjacent

seats having similar vote shares and same winners more frequently than in the original models. In [Fig 3,](#page-10-0) we show the winner maps for two such elections over *S* = 100, one using DPM and the other with GDPM, for the same vote share *X*<sup>1</sup> = [0.45, 0.35, 0.2]. We can observe higher spatial coherence in the second election.

In case of the SIM model, both the vote share and seat share are generated. So we run the experiments for different number *C* of communities, their proportions *η* and different community-party relations *Φ*. We consider four scenarios – two involving *C* =3 communities, and two more involving *C* =5 communities. In case of *C* =3, we set the community proportions as *η* = {0.5, 0.3, 0.2}, i.e., one large, medium and small community. For *C* =5, their proportions are set to *<sup>η</sup>* = {0.35, 0.35, 0.1, 0.1, 0.1}, i.e., two large and three small communities. We constrain *φ* such that for each party *k*, ∑*<sup>C</sup> <sup>c</sup>*=1 *<sup>η</sup>cϕck ≤* 0.5, i.e., we assume that a party cannot satisfy many persons without dissatisfying some others. In each case, Scenario 1 (polarized) involves Party 1 that is favored by the larger communities and opposed by the smaller ones, Party 2 that is favored by the smaller communities and opposed by the larger ones, and Party 3 which is neutral to all communities. The third party, however has *σ* =2, higher than the other two with *σ* =1 indicating that it has strong individual supporters and opponents. These relations are represented by *ϕ*<sup>1</sup>. In Scenario 2 (non-polarized), each party is favored by one or more communities, but not opposed by the rest. One party again has high *σ* =2, the others have *σ* =1. These relations are represented by *ϕ*<sup>2</sup>. We report the resulting vote shares and seat shares in [Table 2,](#page-10-1) along with standard deviation of votes across seats. Once again, we report the numbers over 10 runs of experiments in each setting. It is seen that in polarized scenario of *ϕ*1, the neutral party fails to win any seat with fewer communities, but can do well with more communities involved. Also, with more communities involved, there is very less difference between *ϕ*1 and *ϕ*2. Local influence is found to benefit the parties that support the larger communities and harms the centrist party, particularly when fewer communities are involved.

<span id="page-9-0"></span>**Table 1. Exploring space of outcomes (Seat shares) for different vote shares using DPM and PCM models with different concentration parameter settings.**

| Model |   | Param                      | X 1  |      |     |     |      |      |      |      |
|-------|---|----------------------------|------|------|-----|-----|------|------|------|------|
|       |   |                            | 1    | X 1  |     |     |      |      |      |      |
|       |   |                            |      | 2    | X 1 |     |      |      |      |      |
|       |   |                            |      |      | 3   | X 1 |      |      |      |      |
|       |   |                            |      |      |     | 4   | X 2  |      |      |      |
|       |   |                            |      |      |     |     | 1    | X 2  |      |      |
|       |   |                            |      |      |     |     |      | 2    | X 2  |      |
|       |   |                            |      |      |     |     |      |      | 3    | X 2  |
| DPM-1 | α | = 0.8                      | 0.6  | 0.4  | x   | x   | 1.0  | 0    | x    | x    |
| DPM-2 | α | = 0.9                      | 0.6  | 0.4  | x   | x   | 0.84 | 0.16 | x    | x    |
| DPM-3 | α | = 0.95                     | 0.6  | 0.4  | x   | x   | 0.73 | 0.27 | x    | x    |
| DPM-4 | α | = 0.8                      | 0.45 | 0.35 | 0.2 | x   | 0.94 | 0.06 | 0    | x    |
| DPM-5 | α | = 0.9                      | 0.45 | 0.35 | 0.2 | x   | 0.74 | 0.23 | 0.03 | x    |
| DPM-6 | α | = 0.95                     | 0.45 | 0.35 | 0.2 | x   | 0.58 | 0.3  | 0.12 | x    |
| DPM-7 | α | = 0.8                      | 0.4  | 0.3  | 0.2 | 0.1 | 0.97 | 0.03 | 0    | 0    |
| DPM-8 | α | = 0.9                      | 0.4  | 0.3  | 0.2 | 0.1 | 0.75 | 0.2  | 0.04 | 0.01 |
| DPM-9 | α | = 0.95                     | 0.4  | 0.3  | 0.2 | 0.1 | 0.55 | 0.26 | 0.14 | 0.05 |
| PCM-1 | η | = [0.5, 0.95]              | 0.6  | 0.4  | x   | x   | 0.82 | 0.18 | x    | x    |
| PCM-2 | η | = [0.95, 0.5]              | 0.6  | 0.4  | x   | x   | 0.72 | 0.28 | x    | x    |
| PCM-3 | η | = [0.95, 0.95]             | 0.6  | 0.4  | x   | x   | 0.73 | 0.27 | x    | x    |
| PCM-4 | η | = [0.5, 0.95, 0.95]        | 0.45 | 0.35 | 0.2 | x   | 0.71 | 0.24 | 0.05 | x    |
| PCM-5 | η | = [0.95, 0.5, 0.95]        | 0.45 | 0.35 | 0.2 | x   | 0.54 | 0.39 | 0.07 | x    |
| PCM-6 | η | = [0.95, 0.95, 0.95]       | 0.45 | 0.35 | 0.2 | x   | 0.59 | 0.34 | 0.07 | x    |
| PCM-7 | η | = [0.5, 0.5, 0.95, 0.95]   | 0.4  | 0.3  | 0.2 | 0.1 | 0.92 | 0    | 0.08 | 0    |
| PCM-8 | η | = [0.5, 0.95, 0.95, 0.95]  | 0.4  | 0.3  | 0.2 | 0.1 | 0.71 | 0.22 | 0.07 | 0    |
| PCM-9 | η | = [0.95, 0.95, 0.95, 0.95] | 0.4  | 0.3  | 0.2 | 0.1 | 0.57 | 0.3  | 0.11 | 0.02 |

#### **5.2 Vote swing vs seat swing**

Next, we study the process of swings between successive elections. For each of the elections simulated by DPM, PCM, SIM in the previous analysis (referred to as DPM-1, PCM-2 etc in [Tables 1](#page-9-0) and [2\)](#page-10-1), we simulated the *next election* using both the Dirichlet Swing Model (DSM) and the Dirichlet Swing Matrix Model (DSMM). We consider different values of the swing ∆*θ*(*t*). The base distribution parameters *ν* is chosen as *B*∆ˆ*θ*(*t*), where hyperparameter *B* controls the variance across the atoms, i.e., district-wise swings. In each case, we estimate the new vote share and the corresponding seat share. The detailed results are shown in [Table 1](#page-9-0) in the Supporting Information.

An example is illustrated in [Fig 4,](#page-11-0) in an election over *S* = 100 seats, where the first election is simulated by DPM, and second elections by DSM using *B* =1 and *B* = 10 based on the first election. For *B* =1, we see a different winner in 54 seats, while for *B* = 10 only 33 seats change hands. Similar results are also found for DSMM. We illustrate the results graphically in [Fig 5](#page-12-0). We plot the change is vote share of party *k*, i.e., *θk*(*t*)= *X*1(*k*, *t* + 1) – *X*1(*k*, *t*) against its corresponding change in seat share, i.e., *X*2(*k*, *t* + 1) – *X*2(*k*, *t*). We plot this separately for each party *k* = {1, 2, 3} (denoted by 'o', '+' and '\*' in the figure). *X*1(*t* + 1), *X*2(*t* + 1) are estimated using DSM with different parameter settings (denoted by different colors).

<span id="page-10-0"></span>**Fig 3. Winner maps of two elections over 100 seats, simulated by DPM (left) and GDPM (right).** The vote share is same in both cases [0.45, 0.35, 0.2] and also the seat share [0.52, 0.34, 0.14].

<https://doi.org/10.1371/journal.pone.0344018.g003>

<span id="page-10-1"></span>**Table 2. Social identity model in two scenarios** *ϕ***<sup>1</sup> ,** *ϕ***<sup>2</sup>, for** *C* **=3 and** *C* **=5. Above: individual preference, Below: local influence variants of SIM.**

| Model |   |   | Param |    | X 1    |      |      |      |      |      |
|-------|---|---|-------|----|--------|------|------|------|------|------|
|       |   |   |       |    | 1      | X 1  |      |      |      |      |
|       |   |   |       |    |        | 2    | X 1  |      |      |      |
|       |   |   |       |    |        |      | 3    | X 2  |      |      |
|       |   |   |       |    |        |      |      | 1    | X 2  |      |
|       |   |   |       |    |        |      |      |      | 2    | X 2  |
| SIM-1 | ϕ | 1 | ( C   | =3 | ) 0.35 | 0.34 | 0.31 | 0.49 | 0.35 | 0.16 |
| SIM-2 | ϕ | 2 | ( C   | =3 | ) 0.37 | 0.38 | 0.25 | 0.42 | 0.40 | 0.18 |
| SIM-3 | ϕ | 1 | ( C   | =5 | ) 0.33 | 0.36 | 0.31 | 0.35 | 0.30 | 0.35 |
| SIM-4 | ϕ | 2 | ( C   | =5 | ) 0.33 | 0.36 | 0.31 | 0.35 | 0.31 | 0.34 |
| SIM-5 | ϕ | 1 | ( C   | =3 | ) 0.36 | 0.34 | 0.3  | 0.47 | 0.31 | 0.22 |
| SIM-6 | ϕ | 2 | ( C   | =3 | ) 0.43 | 0.35 | 0.22 | 0.45 | 0.33 | 0.22 |
| SIM-7 | ϕ | 1 | ( C   | =5 | ) 0.35 | 0.32 | 0.33 | 0.38 | 0.24 | 0.38 |
| SIM-8 | ϕ | 2 | ( C   | =5 | ) 0.35 | 0.32 | 0.33 | 0.37 | 0.24 | 0.38 |

![](_page_11_Diagram_1.jpeg)

![](_page_11_Figure_2.jpeg)

We find that for low values of *B* the seat swing can be very significant and even counter-intuitive, for example in some cases we find Party 1 gaining 3% votes but still losing seats on average. Such swings are more moderated for higher values of *B*. Furthermore, we vary the Dirichlet Base Distribution parameters for both DSM and DSMM, which regulates the variance of swings across the districts.

## **6 Simulating Indian elections with parameter estimation**

Next, we consider political elections held in India, which is known as the largest parliamentary democracy in the world. The aim is to examine if these theoretical models can simulate these elections under appropriate parameter settings. We study individual elections as well as swings across consecutive elections. Elections are district-based, based on plurality voting, which suits the framework considered here. Also, elections are held at regular intervals of time, either for the state assemblies or for the national parliament, and vote swing between successive elections is a politically significant phenomena which is studied by many political scientists. For this study, we consider 4 state-level elections held in India in recent times. The details of the election are given in [Table 3.](#page-12-1)

## **6.1 Simulation by models**

<span id="page-11-0"></span>**Fig 4. Swing from previous election (left) to next election (right) under Dirichlet Swing Model, with parameter** *B* =1 **(top right) and** *B* = 10 **(bottom right).**

![](_page_12_Figure_1.jpeg)

- 1. *Calibration for Validation*: verify if the proposed models can simulate the election results (seat share) given the vote shares under suitably chosen parameters
- 2. *Counterfactual Analysis*: to explore what could have been the results of these elections had the voters of the different parties been geographically distributed in a different way. In other words, we aim to see the impact of the district boundaries on the results.

We use the DPM, GDPM, PCM and GPCM models for these analyses. We cannot use the SIM model, since we do not have community-wise information about either residence or voting preferences.

In the first experiment, we consider the seat share of different parties in each of the elections, for both optimal and two standard parameter settings. The optimal parameter setting is chosen by grid search, however there are other approaches to finding the optimal values of the parameters (discussed later). The two standard parameter settings include one with low values of the concentration parameters (*α* for DPM and *η* for PCM) – which suggest spatially homogeneous distribution of each party's voters, and another with high values of these parameters, suggesting strong spatial heterogeneity, and encouraging each party's supporters to be spatially concentrated. [Table 4](#page-13-0) shows the results for DPM and PCM. Apart from the seat share, we also indicate the standard deviation of votes received by each party across the districts, in both the actual and the simulated elections. We find that under the optimal parameter settings, both DPM and PCM models

<span id="page-12-0"></span>**Fig 5. Vote Share Swing vs Seat Share Swing for different parties under different different swing models and parameters.** Left panel: Districtwise Swing Matrix Model (DSMM), Right Panel: Districtwise Swing Model (DSM). Circle 'o' denotes Party 1, Plus '+' denotes Party 2, Star '\*' denotes Party 3. Each color (blue, red, green, black) indicates a different parameter setting.

<https://doi.org/10.1371/journal.pone.0344018.g005>

<span id="page-12-1"></span>**Table 3. Details of a few past elections from different states in India.**

| Election | State       | Year | N        | S   | X 1  |      |      |
|----------|-------------|------|----------|-----|------|------|------|
|          |             |      |          |     | 1    | X 1  |      |
|          |             |      |          |     |      | 2    | X 1  |
| GJ17     | Gujarat     | 2017 | 30251142 | 182 | 0.49 | 0.42 | 0.09 |
| GJ22     | Gujarat     | 2022 | 29580492 | 182 | 0.56 | 0.3  | 0.14 |
| WB19     | West Bengal | 2019 | 55158913 | 294 | 0.45 | 0.13 | 0.42 |
| WB21     | West Bengal | 2019 | 57373983 | 294 | 0.51 | 0.09 | 0.4  |

can recreate the actual results. We also see from the 2 default parameter settings that the results could have been very different, had the voters been distributed differently.

<span id="page-13-4"></span><span id="page-13-3"></span><span id="page-13-2"></span>The optimal choice of the parameters, to fit a given model to actual election results may be determined in various ways. The simplest approach, used in this work is grid search over the parameter space. However, this approach can be quite inefficient, especially for models like PCM with multiple parameters, and for elections with a large number of voters. Possible other alternative approaches include Bayesian Optimization [\[31](#page-21-19)] and Simulation-based Inference [[32,](#page-21-20)[33\]](#page-21-21), where the main idea is to explore the parameter space efficiently, as we need to run the simulation with each candidate parameter value and compare the result with the observations. The general idea is to first run trial simulations using a few parameter values from a prior distribution, identify those which produce results similar to the observations, and search further around them till a good match with the observations are obtained. There are also neural network-based surrogates, which can make simulation-based inference more efficient by predicting the outcomes instead of running the full simulations at each candidate value [[34](#page-21-22)[–37](#page-22-0)]. Finally, the recently developed paradigm of Differentiable Agent-based Modeling [[38](#page-22-1)–[40\]](#page-22-2) such as GradABM allows us to implement the aforementioned Agent-based Models as differentiable functions, whose parameters can be estimated through back-propagating the error between the simulated results and observations.

### <span id="page-13-8"></span><span id="page-13-7"></span><span id="page-13-6"></span><span id="page-13-5"></span>**6.2 Geographical coherence**

<span id="page-13-1"></span>The next experiment examines the question of geographical coherence – i.e., do adjacent districts have similar vote shares and winners? This question has been examined by some earlier studies like [\[30](#page-21-18)]. We evaluate this in both the actual and the simulated elections. In any state of India, the districts are numbered in such a way that any two consecutively numbered districts are geographically adjacent to each other. First of all, we compare the vote shares *θs* and *θs*+1 between every pair of consecutively numbered (neighboring) districts using Kullback-Leibler (K-L) Divergence. Similarly, we compare the vote share *θs* and *θs′* where *s′* is chosen randomly from among the districts that are not neighbouring to *s*. We define a measure Vote Spatial Coherence (VSC) as the ratio of the average K-L Divergence between neighboring and non-neighbouring districts are thus compared, as *mean*(*KL*(*s*,*s′* )) *mean*(*KL*(*s*,*s*+1)). A high value of this ratio suggests that the vote shares in two non-neighboring districts are less similar than those in two neighboring districts. A corollary of the strong correlation of vote shares between adjacent seats is that, adjacent seats are often won by the same party. The next analysis is to check the winners. We calculate a Winner Coherence Score (WSC) as ∑ *<sup>s</sup> I*(*Vs* = *Vs*+1) for both real and simulated elections.

<span id="page-13-0"></span>**Table 4. Simulation of seat shares in 4 Indian elections by DPM (middle) and PCM (below) under optimal and default parameter settings.**The actual seat shares in these elections are shown in the upper part of the table. Simulated results in case of optimal parameter settings match the actual results in all cases.

| Election | Opt. Param. |      |      | Def. Param. 1 |      |      | Def. Param. 2 |      |      |
|----------|-------------|------|------|---------------|------|------|---------------|------|------|
|          | X 2         |      |      |               |      |      |               |      |      |
|          | 1           | X 2  |      |               |      |      |               |      |      |
|          |             | 2    | X 2  |               |      |      |               |      |      |
|          |             |      | 3    | X 2           |      |      |               |      |      |
|          |             |      |      | 1             | X 2  |      |               |      |      |
|          |             |      |      |               | 2    | X 2  |               |      |      |
|          |             |      |      |               |      | 3    | X 2           |      |      |
|          |             |      |      |               |      |      | 1             | X 2  |      |
|          |             |      |      |               |      |      |               | 2    | X 2  |
| GJ17     | 0.53        | 0.44 | 0.03 | x             | x    | x    | x             | x    | x    |
| GJ22     | 0.88        | 0.09 | 0.03 | x             | x    | x    | x             | x    | x    |
| WB19     | 0.54        | 0.05 | 0.41 | x             | x    | x    | x             | x    | x    |
| WB21     | 0.75        | 0.01 | 0.24 | x             | x    | x    | x             | x    | x    |
| GJ17     | 0.53        | 0.42 | 0.05 | 0.71          | 0.29 | 0.0  | 0.49          | 0.43 | 0.08 |
| GJ22     | 0.88        | 0.1  | 0.02 | 0.99          | 0.01 | 0.0  | 0.61          | 0.26 | 0.13 |
| WB19     | 0.56        | 0.02 | 0.42 | 0.59          | 0.01 | 0.4  | 0.46          | 0.12 | 0.42 |
| WB21     | 0.71        | 0.03 | 0.26 | 0.84          | 0    | 0.16 | 0.52          | 0.09 | 0.39 |
| GJ17     | 0.53        | 0.44 | 0.03 | 0.97          | 0.03 | 0.0  | 0.53          | 0.44 | 0.03 |
| GJ22     | 0.86        | 0.10 | 0.04 | 1.0           | 0.0  | 0.0  | 0.68          | 0.26 | 0.06 |
| WB19     | 0.53        | 0.03 | 0.44 | 0.86          | 0.0  | 0.14 | 0.5           | 0.06 | 0.44 |
| WB21     | 0.73        | 0.01 | 0.26 | 1.0           | 0.0  | 0.0  | 0.58          | 0.03 | 0.39 |

The results are illustrated in [Table 5.](#page-14-0) We find that both VSC and WSC are quite high for the elections that we have considered. We repeat the same analysis for the elections simulated by DPM, GDPM, PCM and GPCM, and it is found that GDPM and GPCM definitely increases the spatial concentration in terms of both vote share and winner compared to DPM and PCM. While WSC scores from the simulated elections tend to match the actual election, the VSC tends to be overestimated.

#### **6.3 Simulation of swings**

The third experiment in this section is to analyze the swing between successive elections. We consider two pairs of successive elections in India – (Gujarat2017 vs Gujarat2022) and (Bengal2019 vs Bengal2021). In each case, we start with the full results *Z*(*t*) of the earlier election, as well as the vote shares *θ*(*t* + 1) in the later election. Using these, we try to predict the results *Z*(*t* + 1) of the later election. In this case, prediction means not only estimation of seat shares, but also predicting the winner in each district (since we already know the winner of each district in the earlier election). Using both the DSM and DSMM, we estimate the results in each district. From *θ*(*t* + 1) we calculate ∆ˆ *θ*(*t*), which is used as the parameters of the base distribution *H*, multiplied by a constant *B*. High values of *B* encourage low variance, i.e., similar swings in each district, and its low values encourage high variance, i.e., different swings in different districts. We calculate the following:

- In how many seats does each party register an increase in vote share? (denoted by Gain-1, Gain-2 etc). This is measured as *Gaink*(*t*)= ∑ *<sup>s</sup> I*(*θsk*(*t* + 1) > *θsk*(*t*)). This can be calculated for both actual and simulated values of *θ*(*t* + 1).
- How many seats change hands from one party to another? This is measured by *Flip*(*t*)= ∑ *<sup>s</sup> <sup>I</sup>*(*Us*(*<sup>t</sup>* + 1) *̸*<sup>=</sup> *Us*(*t*)), and can be calculated in both actual and simulated elections.
- In how many seats are the winners correctly predicted (Accuracy)? Note that, for our Swing models, the results for each district varies from one simulation to another, as these are random variables. Hence it is futile to calculate the seatwise accuracy in each run of the simulation. Instead, we run the simulations 10 times, and the winning party for each seat is noted in each simulation. The probabilities of each party winning a particular seat is calculated accordingly, and the accuracy is calculated using these probabilities. Hence we measure *Acc*(*t*)= ∑ *<sup>s</sup> Prob*(*U*ˆ*s*(*t*)= *Us*(*t*)), where *U* is the actual winner in district *s* and *U*ˆ is the winner according to simulations by a model.

<span id="page-14-1"></span>The results are provided in [Table 6](#page-15-0). For both Gujarat (GJ17) and West Bengal (WB19), we run simulations to predict GJ22 and WB21 respectively, using both DSM and DSMM using different values of *B*. We can actually make maximum-likelihood estimates of *B* (using Minka's algorithm for estimating Dirichlet parameters [\[41\]](#page-22-3)) from the actual results of GJ22 and WB21, which turn out to be *B* = 10 and *B* = 18 respectively. Clearly, in case of DSM, smaller value of *B* indicates larger swings of vote shares and flipping of winners across the districts. We also calculate the fraction of districts where each party improves its vote share, i.e., *X*<sup>1</sup> *<sup>k</sup>* (*s*, *t* + 1) > *X*<sup>1</sup> *<sup>k</sup>* (*s*, *t*), denoted by Gn1, Gn2, Gn3. We find that DSMM model outperforms DSM in predicting the results of the second election in both cases, and in terms of both vote shares

<span id="page-14-0"></span>**Table 5. Comparing spatial correlations between vote shares (VSC) and winners (WSC) in actual elections and elections simulated by DPM, GDPM, PCM, GPCM.**The simulated results that are closest to the actual results are highlighted.

| Election | Actual VSC | WSC  | DPM VSC | WSC  | GDPM VSC | WSC  | PCM VSC | WSC  | GPCM VSC | WSC  |
|----------|------------|------|---------|------|----------|------|---------|------|----------|------|
| GJ17     | 1.2        | 0.6  | 0.99    | 0.45 | 1.2      | 0.5  | 1.07    | 0.55 | 1.33     | 0.6  |
| GJ22     | 1.48       | 0.78 | 0.86    | 0.78 | 5.3      | 0.8  | 0.87    | 0.78 | 1.25     | 0.77 |
| WB19     | 3.8        | 0.73 | 1.05    | 0.47 | 12.4     | 0.57 | 1.00    | 0.47 | 1.92     | 0.69 |
| WB21     | 1.4        | 0.8  | 1.0     | 0.62 | 14.8     | 0.68 | 0.98    | 0.6  | 2.27     | 0.8  |

and seat shares. This is particularly true when we use *B* = 10 as the parameter of DSMM model. However, DSMM tends to underestimate the vote share swings and winner-flips across the districts.

A graphical illustration of the above results is provided in [Fig 6](#page-16-0), where we plot the errors between the actual results and the results simulated by both the DSM and DSMM models for both the Indian states mentioned above. The errors are calculated with respect to both the vote share and seat share. Specifically, if the actual vote share and seat shares are denoted by *X*<sup>1</sup> *<sup>a</sup>*(*t* + 1), *X*<sup>2</sup> *<sup>a</sup>*(*t* + 1), and those simulated by a model are denoted by *X*<sup>1</sup> *<sup>m</sup>*(*t* + 1), *X*<sup>2</sup> *<sup>m</sup>*(*t* + 1), then we compare *e*1 *<sup>m</sup>* = *X*<sup>1</sup> *<sup>m</sup>*(*t* + 1) – *X*<sup>1</sup> *<sup>a</sup>*(*t* + 1) and *e*<sup>2</sup> *<sup>m</sup>* = *X*<sup>2</sup> *<sup>m</sup>*(*t* + 1) – *X*<sup>2</sup> *<sup>a</sup>*(*t* + 1). Once again, we show the errors separately for each party (denoted by 'o','+','\*') and each model with different parameter settings (denoted with different colors). We see that in both cases, the seat share errors are quite high for DSM with *b* = 10 (blue color), but for DSMM these errors are much less.

### **7 Simulation of election surveys**

The aim of a survey is to estimate the underlying reality by examining a small number of samples. In this case, the underlying reality is *Z*, and the aim of the survey is to predict the vote shares *X*<sup>1</sup> and seat shares *X*2. This is obtained by selecting a small subset of the voters and finding out their preferences (it is assumed that they respond truthfully) from which a projection *Y* ={*Y*1, *Y*2} is made. Since this is a theoretical work, we cannot carry out actual surveys, and hence we aim to simulate surveys on real or simulated elections. For this purpose, we consider the survey model presented in [\[24](#page-21-11)]. While this paper explored the *p*(*X*|*Y*), i.e., possible actual outcomes given a survey projection, here we analyze *p*(*Y*|*X*), i.e., possible projections by survey of an election.

#### **7.1 Uniform and stratified sampling**

<span id="page-15-2"></span><span id="page-15-1"></span>First we consider the survey model of [\[24](#page-21-11)], which simulates uniform sampling. The main question here is, how to choose these respondents. As already discussed, voting preferences may vary from district to district. While it may not be possible to cover all districts, an unbiased survey can be considered to choose a few districts uniformly at random, and also choose respondents uniformly at random from these districts. This approach of *Uniform Sampling* has been discussed by other works like [\[18](#page-21-6)], which provided lower bounds on the fraction of districts to be sampled, and the number of people to be queried in each district to be able to predict the winner correctly. In our model, we represent these as parameters *fs* and *fn*. We further assume that the number of people are queried in each chosen district is proportional to the number of voters in that district.

<span id="page-15-0"></span>**Table 6. Comparing swings in vote and seat shares across successive elections in reality and as simulated by DSM and DSMM.**Upper 5 rows are for swings across GJ17 and GJ22, while the bottom rows are for swings across WB19 and WB21. The results of GJ17 are *X*1(*t*) = [0.49, 0.42, 0.09], *X*2(*t*) = [0.53, 0.44, 0.03], and those of WB19 are *X*1(*t*) = [0.44, 0.42, 0.14], *X*2(*t*) = [0.54, 0.41, 0.05].

| Swing(B) Reality | X 1( t + 1) [0.56,0.30,0.14] | X 2( t + 1) [0.88,0.09,0.03] | Flips 0.45 | Gn1 0.87 | Gn2 0.13 | Gn3 0.62 | Acc – |
|------------------|------------------------------|------------------------------|------------|----------|----------|----------|-------|
| DSM(1)           | [0.51,0.27,0.22]             | [0.52,0.22,0.26]             | 0.58       | 0.49     | 0.23     | 0.26     | 0.49  |
| DSM(10)          | [0.55,0.29,0.15]             | [0.77,0.16,0.07]             | 0.39       | 0.67     | 0.14     | 0.6      | 0.72  |
| DSMM(1)          | [0.57,0.31,0.12]             | [0.77,0.19,0.04]             | 0.29       | 0.91     | 0.05     | 0.62     | 0.72  |
| DSMM(10)         | [0.58,0.3,0.12]              | [0.93,0.05,0.02]             | 0.4        | 0.95     | 0.01     | 0.84     | 0.84  |
| Reality          | [0.51,0.4,0.09]              | [0.75,0.25,0]                | 0.3        | 0.85     | 0.34     | 0.13     | –     |
| DSM(1)           | [0.46,0.36,0.18]             | [0.46,0.34,0.2]              | 0.55       | 0.47     | 0.36     | 0.35     | 0.46  |
| DSM(10)          | [0.49,0.39,0.12]             | [0.6,0.35,0.05]              | 0.34       | 0.62     | 0.39     | 0.35     | 0.65  |
| DSM(18)          | [0.5,0.39.0.11]              | [0.63,0.33,0.04]             | 0.3        | 0.67     | 0.39     | 0.31     | 0.68  |
| DSMM(1)          | [0.5,0.4,0.1]                | [0.64,0.33,0.03]             | 0.16       | 0.93     | 0.37     | 0.07     | 0.76  |
| DSMM(10)         | [0.5,0.4,0.1]                | [0.7,0.29,0.01]              | 0.19       | 0.93     | 0.28     | 0.1      | 0.81  |

![](_page_16_Figure_1.jpeg)

The survey model mentioned above does not consider community identities of the respondents. An alternative survey model is *Stratified Sampling*, where the respondents are first chosen according to a proportion *η*ˆ*s* of communities in district *s*. *η*ˆ may be different from *η* either due to the surveyors' lack of knowledge about the social structure, or systemic biases. Thus, the numbers of respondents from different communities are {*cs*1, *...* , *csC*} *∼ Mult*({*Nsfn*,(*η*ˆ*s*1, *...* , *<sup>η</sup>*ˆ*sC*)}), and these respondents can be queried. This can be simulated using the (*V*, *C*, *S*) variables of the SIM.

#### **7.2 Projection of results**

Suppose in district *s*, a survey finds {*ns*1, *...* , *nsK*} respondents in favour of the *K* parties. Clearly, this follows a Multinomial Distribution with parameters {*Nsfn*,(*θs*1, *...* , *θsK*)/*Ns*}. The next question is, given the survey results, how to project the outcome {*Y*1, *Y*2}. Our model estimates the total vote share by simply aggregating the number of respondents across all districts, who expressed preferences for different parties. In other words, *Y*1(*k*)= ∑ *<sup>s</sup> nsk Nfn* (*Nfn* is the total number of respondents) for party *k*. Next, in each of the *Sfs* districts where we carried out the survey, we identify the party with maximum number of votes among the respondents from that district. Thus, we find the number of districts {*v*1, *...* , *vK*} "won" by the different parties, and we use this as our estimate *Y*<sup>2</sup> of the overall seat share, i.e., *Y*2(*k*)= *vk Sfs* . We call this the **Direct Projection** approach.

We next consider another alternative approach: to estimate the swing with respect to the previous election. For this, we can consider the Dirichlet Swing Matrix Model, where the aim is to estimate the transition matrix. Here, each respondent is queried on the party they voted for in the current and the previous election, from which we can estimate the swing matrix in each of the queried district, where *M*ˆ *skl*(*t*)= ∑ *<sup>i</sup> <sup>I</sup>*(*Vsi*(*t*)=*k*)*I*(*Vsi* ∑ (*t*+1)=*l*) *<sup>i</sup> <sup>I</sup>*(*Vsi*(*t*)=*k*) . Though these estimates may be used to estimate the vote share in those particular districts, they do not say much about the remaining districts. We use these estimated transitions to make Maximum Likelihood estimates of the Base Dirichlet hyperparameters. Using the properties of Dirichlet Distribution, it can be derived easily that the Maximum Likelihood estimate of *ρkl* is *Mskl*. Using these parameters, we carry

<span id="page-16-0"></span>**Fig 6. Comparing the error in predicted Vote Share (X-axis) and prediced Seat Share Swing (Y-axis) for different parties under different swing models and parameters.** Left panel: Predictions of West Bengal Elections 2021 (WB21) based on West Bengal Elections 2019 (WB19). Right panel: Predictions of Gujarat Elections 2022 (GJ22) based on Gujarat Elections 2017 (GJ17). Circle 'o' denotes Party 1, Plus '+' denotes Party 2, Star '\*' denotes Party 3. Blue and Red colors indicate predictions by DSM model, while Green and Black colors indicate predictions by DSMM model.

out simulations using the Dirichlet Swing Matrix Model, which gives us a projected outcome. We can carry out a number of such simulations and project the mean value of their outcomes. We call this approach as **Swing Projection**.

We discuss some measures for comparing projected results *Y*<sup>2</sup> and actual results *X*<sup>2</sup>. We do not compare *X*<sup>1</sup> and *Y*<sup>1</sup> , as uniform sampling is likely to estimate the vote shares correctly.

First of all, we consider the **Manhattan Distance** between *X*<sup>1</sup> and *Y*<sup>1</sup> , which is given by *dM*(*X*2, *<sup>Y</sup>*2)= ∑ *<sup>k</sup>* |*X*<sup>2</sup> *<sup>k</sup>* – *Y*<sup>2</sup> *k* | . We calculate the mean value of this quantity over *G* runs of a particular survey strategy and settings, *dM*(*X*2, *Y*2)= <sup>1</sup> *<sup>k</sup>* |*X*<sup>2</sup> *<sup>k</sup>* – *Y*<sup>2</sup> *ik*|, where {*Y*<sup>2</sup> 1, *...* , *Y*<sup>2</sup> *<sup>G</sup>*} are the projected outcomes of these surveys.

*G* ∑*G i*=1 ∑ Another measure we consider is, how likely is a survey to project accurate results? We consider *Y*2 to be an accurate estimate of *X*<sup>2</sup> if ∑ *<sup>k</sup>* |*X*<sup>2</sup> *<sup>k</sup>* – *Y*<sup>2</sup> *<sup>k</sup>* |< *δ*. We are interested in the quantity *prob*( ∑ *<sup>k</sup>* |*X*<sup>2</sup> *<sup>k</sup>* – *Y*<sup>2</sup> *<sup>k</sup>* |< *δ*), which is approximated as 1 *G* ∑ *i I*( ∑ *<sup>k</sup>* |*X*<sup>2</sup> *<sup>k</sup>* – *Y*<sup>2</sup> *ik*|< *δ*).

#### **7.3 Direct survey vs swing survey**

The aim of this section is to compare the different survey strategies discussed above. We simulate surveys on elections simulated by the aforementioned models like DPM and SIM, and also on actual elections from the Indian election dataset. The main aims of the experiments is to estimate how likely the different strategies are to project accurate results, under different values of (*fn*, *fs*) parameters. In our experiments, we consider *G* = 100.

In the first experiment, we consider the importance of spatial coverage *fs* and person coverage *fn*. In general, we can expect that if there is significant diversity in terms of vote share across the districts, performance should improve if we consider more districts in our survey. But if such diversity does not exist, then surveying more districts (high *fs*) has no advantage. Similarly, if the vote shares of different parties are close to each other then sampling more voters (high *fn*) can improve the estimates, but this does may not be true if the vote shares are well-separated. We consider i) four elections simulated by the GDPM model with different levels of popular support and the concentration parameter *α*, ii) four elections simulated by G-PCM with different levels of popular support and the concentration parameter *η*, iii) 2 elections simulated by SIM (one where different communities have comparable preferences, and one where different communities have markedly different preferences). The results are illustrated in [Figs 7](#page-18-0)[–9](#page-19-0) respectively, while the full results in tabular form are provided in the Supporting Information. We find that there is no straightforward relation between projection performance and *fn* or *fs*. Performance tends to improve with *fs* in case of the elections simulated by DPM and PCM, but less so in case of SIM. The reverse is true in case of *fn*. The projection performance generally tends to be significantly worse in case of the elections simulated by SIM, as it is a more sophisticated model capable of adding more layers of uncertainty through community-based preferences of voters. The same experiment is repeated for the 4 Indian elections, and the results are shown in [Table 7](#page-19-1). In all cases we find that increasing district coverage *fs* is more effective than increasing person coverage *fn*. We also notice that for GJ-17 and WB-19, where the first two parties had quite close vote/seat shares, the probability of successful projection was below 40%, but this was much higher in GJ-17 and WB-21 when the first party had a big lead over the rest.

The aim of the second experiment is to compare direct projections with swing-based projections. The hypothesis is that, if we can estimate the vote swings with respect to the previous election from surveys, we can achieve better projection accuracy with a certain number of respondents, than trying to directly estimate the current election's result. We perform this experiment on two Indian elections too – Gujarat Assembly Elections of 2017 and 2022, and West Bengal Elections in 2019 and 2021. We simulate surveys in the new elections on different values of (*fs*, *fn*), to make projections for them. These are compared with the direct projections based on the simulated surveys on the second election. Once again, we calculate both Manhattan distance and Projection Accuracy, and compare them in [Table 8](#page-19-2). We use *B* = 10 for West Bengal and *B* =6 for Gujarat. We find that in most cases, using Swing-based projection gives better results in terms of both Manhattan Distance and Probability of Accurate Projection, especially if the district coverage is lower.

![](_page_18_Figure_1.jpeg)

## **8 Conclusion**

Election analysis and result prediction through surveys is a problem that is not only of practical interest to journalists and policymakers, but also of academic interest to political scientists, theoretical computer scientists and statisticians. However, simulations of elections based on detailed voter-centric models are not common. This paper provides an approach that can not only be used to estimate the election outcomes (seat shares of parties) based on their vote shares, but also provides hypothetical results, that could have been realized if the voters were spatially distributed in a different way, or if

<span id="page-18-0"></span>**Fig 7. Change in seat projection errors (Manhattan Distance) due to variation of** *fs*, *fn* **on elections simulated by DPM (upper part: DPM-6, lower part: DPM-7).**

![](_page_18_Figure_3.jpeg)

**Fig 8. Change in seat projection errors (Manhattan Distance) due to variation of** *fs*, *fn* **on elections simulated by PCM (upper part: PCM-6, lower part: PCM-9).**

![](_page_19_Figure_1.jpeg)

<span id="page-19-1"></span>**Table 7. Accuracy of seat projections due to variation of** *fs***,** *fn* **on some Indian elections.** We report the mean Manhattan Distance in each case, while the probability of accurate projection is shown in brackets.

| fs    | fn   | GJ-17       | GJ-22       | WB-19       | WB-21       |
|-------|------|-------------|-------------|-------------|-------------|
| 0.001 | 0.1  | 0.21 (0.12) | 0.15 (0.19) | 0.17 (0.1)  | 0.12 (0.19) |
| 0.001 | 0.25 | 0.12 (0.18) | 0.08 (0.26) | 0.12 (0.21) | 0.07 (0.49) |
| 0.001 | 0.5  | 0.09 (0.33) | 0.05 (0.53) | 0.08 (0.32) | 0.06 (0.43) |
| 0.01  | 0.1  | 0.2 (0.11)  | 0.13 (0.22) | 0.19 (0.08) | 0.1 (0.26)  |
| 0.01  | 0.25 | 0.12 (0.12) | 0.07 (0.31) | 0.1 (0.28)  | 0.07 (0.41) |
| 0.01  | 0.5  | 0.08 (0.31) | 0.05 (0.54) | 0.07 (0.38) | 0.04 (0.68) |

<https://doi.org/10.1371/journal.pone.0344018.t007>

<span id="page-19-2"></span>**Table 8. Change in seat projections due to variation of** *fs***,** *fn* **on Indian elections for direct and swing-based projections.**

| Election          | fn ↓  | Man. Dis. |      |      | Acc. |      |      |
|-------------------|-------|-----------|------|------|------|------|------|
| fs →              |       | 0.1       | 0.25 | 0.5  | 0.1  | 0.25 | 0.5  |
| WB21 (Direct)     | 0.001 | 0.13      | 0.07 | 0.05 | 0.15 | 0.44 | 0.6  |
| WB19-WB21 (Swing) | 0.001 | 0.1       | 0.06 | 0.05 | 0.25 | 0.47 | 0.56 |
| WB21 (Direct)     | 0.01  | 0.12      | 0.07 | 0.05 | 0.20 | 0.43 | 0.59 |
| WB19-WB21 (Swing) | 0.01  | 0.09      | 0.05 | 0.05 | 0.37 | 0.59 | 0.61 |
| GJ22 (Direct)     | 0.001 | 0.14      | 0.08 | 0.06 | 0.14 | 0.20 | 0.50 |
| GJ17-GJ22 (Swing) | 0.001 | 0.10      | 0.07 | 0.06 | 0.28 | 0.35 | 0.45 |
| GJ22 (Direct)     | 0.01  | 0.14      | 0.08 | 0.05 | 0.16 | 0.27 | 0.61 |
| GJ17-GJ22 (Swing) | 0.01  | 0.09      | 0.07 | 0.05 | 0.33 | 0.43 | 0.52 |

<https://doi.org/10.1371/journal.pone.0344018.t008>

<span id="page-19-0"></span>**Fig 9. Change in seat projection errors (Manhattan Distance) due to variation of** *fs*, *fn* **on elections simulated by SIM (upper part: SIM-1, lower part: SIM-2).**

the community-party relationships were different. Such analysis can lead to understanding the fairness and robustness of a given districting system or voting policy, such as plurality or first-past-the-post. Additionally, we also look into swing of votes across successive elections, and propose two new models that are far more realistic than the uniform or proportional swing models, as it allows for the possibility that even a party that loses votes overall can gain new seats. We also simulate election surveys, and show the complex relationships between accuracy of projections and district coverage or sample size of respondents. We also find that if the district coverage or sample size is small, then better projection results can be obtained by estimating the swing matrix with respect to the previous election, than directly trying to estimate the seat share of the current election. These results can provide directions to polling agencies regarding their sampling and querying approach. Our results are validated on actual elections held in different states of India.

# **Supporting information**

**[S1 File. A](http://journals.plos.org/plosone/article/asset?unique&id=info:doi/10.1371/journal.pone.0344018.s001)dditional analyses and results.**  (PDF)

# **Acknowledgments**

Adway Mitra thanks Indian Institute of Technology Kharagpur for partial support for this research.

# **Author contributions**

**Conceptualization:** Adway Mitra.

**Data curation:** Adway Mitra.

**Formal analysis:** Adway Mitra.

**Investigation:** Adway Mitra.

**Methodology:** Adway Mitra.

**Resources:** Adway Mitra.

**Software:** Adway Mitra.

**Validation:** Adway Mitra.

**Visualization:** Adway Mitra.

**Writing – original draft:** Adway Mitra.

**Writing – review & editing:** Adway Mitra.

# **References**

- <span id="page-20-0"></span>**[1.](#page-2-0)** Bachrach Y, Lev O, Lewenberg Y, Zick Y. Misrepresentation in District Voting. In: IJCAI, 2016. 81–7.
- <span id="page-20-1"></span>**[2.](#page-1-0)** Brooks C, Nieuwbeerta P, Manza J. Cleavage-based voting behavior in cross-national perspective: evidence from six postwar democracies. Social Science Research. 2006;35(1):88–128. <https://doi.org/10.1016/j.ssresearch.2004.06.005>
- <span id="page-20-2"></span>**[3.](#page-1-1)** Dawkins CJ. Measuring the Spatial Pattern of Residential Segregation. Urban Studies. 2004;41(4):833–51. [https://doi.](https://doi.org/10.1080/0042098042000194133) [org/10.1080/0042098042000194133](https://doi.org/10.1080/0042098042000194133)
- <span id="page-20-3"></span>**[4.](#page-1-2)** Dawkins CJ. SPACE AND THE MEASUREMENT OF INCOME SEGREGATION. Journal of Regional Science. 2007;47(2):255–72. [https://doi.](https://doi.org/10.1111/j.1467-9787.2007.00508.x) [org/10.1111/j.1467-9787.2007.00508.x](https://doi.org/10.1111/j.1467-9787.2007.00508.x)
- <span id="page-20-4"></span>**[5.](#page-1-3)** Braha D, de Aguiar MAM. Voting contagion: Modeling and analysis of a century of U.S. presidential elections. PLoS One. 2017;12(5):e0177970. <https://doi.org/10.1371/journal.pone.0177970> PMID: [28542409](http://www.ncbi.nlm.nih.gov/pubmed/28542409)
- <span id="page-20-5"></span>**[6.](#page-1-4)** Berg S, Lepelley D. On probability models in voting theory. Statistica Neerlandica. 1994;48(2):133–46. [https://doi.org/10.1111/j.1467-9574.1994.](https://doi.org/10.1111/j.1467-9574.1994.tb01438.x) [tb01438.x](https://doi.org/10.1111/j.1467-9574.1994.tb01438.x)
- <span id="page-20-6"></span>**[7.](#page-1-5)** Pritchard G, Wilson MC. Multi-district preference modelling. Qual Quant. 2022;57(1):587–613.<https://doi.org/10.1007/s11135-022-01377-x>

- <span id="page-21-0"></span>**[8.](#page-1-6)** Lewenberg Y, Lev O, Rosenschein JS. Divide and Conquer: Using Geographic Manipulation to Win District-Based Elections. In: International Joint Conference on Autonomous Agents and Multiagent Systems, 2017. 624–32.<https://doi.org/10.65109/lxne6781>
- **9.** Borodin A, Lev O, Shah N, Strangway T. Big city vs. the great outdoors: voter distribution and how it affects gerrymandering. In: IJCAI, 2018. 98–104.
- <span id="page-21-1"></span>**[10.](#page-1-7)** Borodin A, Lev O, Shah N, Strangway T. Little House (Seat) on the Prairie: Compactness, Gerrymandering, and Population Distribution. In: AAMAS, 2022. 154–62.
- <span id="page-21-2"></span>**[11.](#page-2-1)** Wilson MC, Grofman BN. Models of inter-election change in partisan vote share. Journal of Theoretical Politics. 2022;34(4):481–98. [https://doi.](https://doi.org/10.1177/09516298221123263) [org/10.1177/09516298221123263](https://doi.org/10.1177/09516298221123263)
- <span id="page-21-3"></span>**[12.](#page-2-2)** Irvani D, Sadik K, Kurnia A, Saefuddin A, Erfiani. Swing Voters' Vote Choice Prediction Using Multilevel Logit Model to Improve Election Survey Accuracy. J Phys: Conf Ser. 2021;1863(1):012021. <https://doi.org/10.1088/1742-6596/1863/1/012021>
- <span id="page-21-4"></span>**[13.](#page-2-3)** Bhattacharyya A, Dey P. Predicting winner and estimating margin of victory in elections using sampling. Artificial Intelligence. 2021;296:103476. <https://doi.org/10.1016/j.artint.2021.103476>
- **14.** Perse EM, Lambe J. Media effects and society. Routledge. 2016.
- **15.** Dwi Prasetyo N, Hauff C. Twitter-based Election Prediction in the Developing World. In: Proceedings of the 26th ACM Conference on Hypertext & Social Media - HT '15, 2015. 149–58.<https://doi.org/10.1145/2700171.2791033>
- **16.** Leigh A, Wolfers J. Competing Approaches to Forecasting Elections: Economic Models, Opinion Polling and Prediction Markets\*. Economic Record. 2006;82(258):325–40.<https://doi.org/10.1111/j.1475-4932.2006.00343.x>
- <span id="page-21-5"></span>**[17.](#page-2-4)** Kennedy R, Wojcik S, Lazer D. Improving election prediction internationally. Science. 2017;355(6324):515–20. [https://doi.org/10.1126/science.](https://doi.org/10.1126/science.aal2887) [aal2887](https://doi.org/10.1126/science.aal2887) PMID: [28154078](http://www.ncbi.nlm.nih.gov/pubmed/28154078)
- <span id="page-21-6"></span>**[18.](#page-15-1)** Kar D, Dey P, Sanyal S. Sampling-Based Winner Prediction in District-Based Elections. In: International Joint Conference on Autonomous Agents and Multiagent Systems, 2023. 2661–3.<https://doi.org/10.65109/osjx7491>
- <span id="page-21-7"></span>**[19.](#page-2-5)** Cerina R, Duch R. Polling India via regression and post-stratification of non-probability online samples. PLoS One. 2021;16(11):e0260092. [https://](https://doi.org/10.1371/journal.pone.0260092) [doi.org/10.1371/journal.pone.0260092](https://doi.org/10.1371/journal.pone.0260092) PMID: [34843519](http://www.ncbi.nlm.nih.gov/pubmed/34843519)
- <span id="page-21-8"></span>**[20.](#page-2-6)** Gao M, Wang Z, Wang K, Liu C, Tang S. Forecasting elections with agent-based modeling: Two live experiments. PLoS One. 2022;17(6):e0270194. <https://doi.org/10.1371/journal.pone.0270194> PMID: [35771877](http://www.ncbi.nlm.nih.gov/pubmed/35771877)
- <span id="page-21-9"></span>**[21.](#page-4-1)** Mitra A. Electoral David-vs-Goliath: Probabilistic Models of Spatial Distribution of Electors to Simulate District-Based Election Outcomes. In: 2021 Winter Simulation Conference (WSC), 2021. 1–12.<https://doi.org/10.1109/wsc52266.2021.9715325>
- <span id="page-21-12"></span>**[22.](#page-4-2)** Mitra A. Agent-based Simulation of District-based Elections with Heterogeneous Populations. In: International Joint Conference on Autonomous Agents and Multiagent Systems, 2023. 2730–2.<https://doi.org/10.65109/zjun6635>
- <span id="page-21-10"></span>**[23.](#page-3-0)** Palombi F, Toti S. Voting Behavior in Proportional Elections from Agent – Based Models. Physics Procedia. 2015;62:42–7. [https://doi.org/10.1016/j.](https://doi.org/10.1016/j.phpro.2015.02.009) [phpro.2015.02.009](https://doi.org/10.1016/j.phpro.2015.02.009)
- <span id="page-21-11"></span>**[24.](#page-15-2)** Mitra A, Dey P. Evaluating District-based Election Surveys with Synthetic Dirichlet Likelihood. In: Proceedings of the 2024 International Conference on Autonomous Agents and Multiagent Systems, 2024. 1400–8.
- <span id="page-21-13"></span>**[25.](#page-4-3)** Mitra A. Electoral David vs Goliath: How does the spatial concentration of electors affect district-based elections?. arXiv preprint. 2020. [https://doi.](https://doi.org/arxiv:200611865) [org/arxiv:200611865](https://doi.org/arxiv:200611865)
- <span id="page-21-14"></span>**[26.](#page-5-0)** Pitman J. Exchangeable and partially exchangeable random partitions. Probab Th Rel Fields. 1995;102(2):145–58. [https://doi.org/10.1007/](https://doi.org/10.1007/bf01213386) [bf01213386](https://doi.org/10.1007/bf01213386)
- <span id="page-21-15"></span>**[27.](#page-5-1)** Villaseñor-Ibáñez J, Del Castillo-Mussot M, El Deeb O. Religion or class? Measuring voting clustering on religious and socioeconomic lines in US presidential elections. PLoS One. 2025;20(10):e0331959. <https://doi.org/10.1371/journal.pone.0331959> PMID: [41052131](http://www.ncbi.nlm.nih.gov/pubmed/41052131)
- <span id="page-21-16"></span>**[28.](#page-7-1)** Basu S, Chib S. Marginal Likelihood and Bayes Factors for Dirichlet Process Mixture Models. Journal of the American Statistical Association. 2003;98(461):224–35. <https://doi.org/10.1198/01621450338861947>
- <span id="page-21-17"></span>**[29.](#page-8-0)** Antweiler W. Estimating voter migration in Canada using generalized maximum entropy. Electoral Studies. 2007;26(4):756–71. [https://doi.](https://doi.org/10.1016/j.electstud.2007.07.005) [org/10.1016/j.electstud.2007.07.005](https://doi.org/10.1016/j.electstud.2007.07.005)
- <span id="page-21-18"></span>**[30.](#page-13-1)** Deeb OE. Entropic spatial auto-correlation of voter uncertainty and voter transitions in parliamentary elections. Physica A: Statistical Mechanics and its Applications. 2023;617:128675. <https://doi.org/10.1016/j.physa.2023.128675>
- <span id="page-21-19"></span>**[31.](#page-13-2)** Gutmann MU, Corander J. Bayesian optimization for likelihood-free inference of simulator-based statistical models. The Journal of Machine Learning Research. 2016;17(1):4256–302.
- <span id="page-21-20"></span>**[32.](#page-13-3)** Cranmer K, Pavez J, Louppe G. Approximating likelihood ratios with calibrated discriminative classifiers. arXiv preprint. 2015. [https://arxiv.org/](https://arxiv.org/abs/1506.02169) [abs/1506.02169](https://arxiv.org/abs/1506.02169)
- <span id="page-21-21"></span>**[33.](#page-13-4)** Thomas O, Dutta R, Corander J, Kaski S, Gutmann MU. Likelihood-free inference by ratio estimation. arXiv preprint. 2016. [https://doi.](https://doi.org/10.48550/arXiv.161110242) [org/10.48550/arXiv.161110242](https://doi.org/10.48550/arXiv.161110242)
- <span id="page-21-22"></span>**[34.](#page-13-5)** Papamakarios G, Sterratt D, Murray I. Sequential neural likelihood: Fast likelihood-free inference with autoregressive flows. In: 2019. 837–48.

- **35.** Wong W, Jiang B, Wu T, Zheng C. Learning Summary Statistic for Approximate Bayesian Computation via Deep Neural Network. STAT SINICA. 2018.<https://doi.org/10.5705/ss.202015.0340>
- **36.** Åkesson M, Singh P, Wrede F, Hellander A. Convolutional Neural Networks as Summary Statistics for Approximate Bayesian Computation. arXiv preprint. 2020. <https://arxiv.org/abs/2001.11760>
- <span id="page-22-0"></span>**[37.](#page-13-6)** Lueckmann JM, Bassetto G, Karaletsos T, Macke JH. Likelihood-free inference with emulator networks. In: Symposium on Advances in Approximate Bayesian Inference. In: 2019. 32–53.
- <span id="page-22-1"></span>**[38.](#page-13-7)** Quera-Bofarull A, Chopra A, Calinescu A, Wooldridge M, Dyer J. Bayesian calibration of differentiable agent-based models. 2023. [https://arxiv.org/](https://arxiv.org/abs/2305.15340) [abs/2305.15340](https://arxiv.org/abs/2305.15340)
- **39.** Chopra A, Rodríguez A, Subramanian J, Quera-Bofarull A, Krishnamurthy B, Prakash BA. Differentiable agent-based epidemiology. In: 2022. <https://doi.org/arXiv:220709714>
- <span id="page-22-2"></span>**[40.](#page-13-8)** Andelfinger P. Differentiable Agent-Based Simulation for Gradient-Guided Simulation-Based Optimization. In: Proceedings of the 2021 ACM SIG-SIM Conference on Principles of Advanced Discrete Simulation, 2021. 27–38. <https://doi.org/10.1145/3437959.3459261>
- <span id="page-22-3"></span>**[41.](#page-14-1)** Minka T. Estimating a Dirichlet distribution. MIT. 2000.