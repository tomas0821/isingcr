![](_page_0_Picture_2.jpeg)

# **Maximizing gerrymandering through ising model optimization OPEN**

**Yasuharu Okamoto**

**By using the Ising model formulation for combinatorial optimization with 0–1 binary variables, we investigated the extent to which partisan gerrymandering is possible from a random but even distribution of supporters. Assuming that an electoral district consists of square subareas and that each subarea shares at least one edge with other subareas in the district, it was possible to find the most tilted assignment of seats in most cases. However, in cases where supporters' distribution included many enclaves, the maximum tilted assignment was usually found to fail. We also discussed the proposed algorithm is applicable to other fields such as the redistribution of delivery destinations.**

Gerrymandering is a generic term for methods that rig electoral districts assuming advantage to a specific party. As long as geographical districts are adopted, the demarcation of districts is inevitable. Electoral districts are also a unit of voters artificially defined by electoral legislation. If this artificial demarcation is intentional, the neutrality of being a geographical division will disappear, and the problem of partisan gerrymandering arises. In terms of its practical effect on the exercise of voting rights, gerrymandering corresponds to systematic control of wasted votes.

There are two techniques widely known in gerrymandering: cracking and packin[g1](#page-6-0) . The former means the cracking of the opposing party's voters' concentration not to form a majority of the district. On the other hand, the latter is to pack as many of the opposing party's voters as possible into the same district when it is unavoidable to form a district with most of the opposition. Packing will dilute the number of opponents who may have formed a majority in other districts. Thus, cracking and packing is practically equivalent to a combination of a narrow victory and a big defeat. Cracking and packing make it possible to minimize the number of wasted votes for governing party while maximizing it for the opposition. A voter who is assigned a wasted vote by gerrymandering effectively loses the opportunity to elect a representative. In other words, such a voter would enjoy only the right to cast a wasted vote, which leads to the danger of distorting the normative imperatives established in our time to reflect the people's diverse will.

Gerrymandering has been studied through jurisprudential or sociological approaches since it occurred in the early nineteenth centur[y2–](#page-7-0)[5](#page-7-1) , however, it has also been studied in mathematical science in recent year[s6](#page-7-2)[–9](#page-7-3) . Studies based on Markov chain Monte Carlo help evaluate districting's intentionality, which would be necessary for gerrymandering certification in court. Puppe and Tasnádi proved that determining whether given geography admits an unbiased districting is an NP-complete problem[9](#page-7-3) . Furthermore, in recent years, with the development of information and communication technology, information gerrymanderin[g10](#page-7-4) and digital gerrymandering[11](#page-7-5) have aroused concern. Although there is no clear definition of digital gerrymandering, it suggests that voting behavior is biased through social networks[12](#page-7-6) and public opinion manipulation by extensive data analysis. Thus, the concept of gerrymandering is expanding in recent times, and it becomes a research area that requires closer integration of social and mathematical science. Such mathematical studies on gerrymandering are still in the early stages. Therefore, various approaches from different disciplines are important and worth considering to shed new light on it.

The combinatorial optimization based on the Ising model employed in this study means the approach where the objective function is formulated by the Ising model with 0–1 binary variables and optimized through metaheuristics such as simulated annealing or tabu search[13](#page-7-7). The approach attains considerable attention recently in terms of the development of quantum annealin[g14](#page-7-8). Furthermore, with the progress of quantum annealing, it is noteworthy that dedicated computer[s15](#page-7-9), and algorithms for Ising models are appearing in classical computatio[n16](#page-7-10)[,17](#page-7-11). Consequently, the combinatorial optimization based on the Ising model begins to be applied to various fields and problems such as logistics (delivery route planning[\)18,](#page-7-12) factories (automated guided vehicle operation)[19](#page-7-13), services (nurse scheduling[\)20](#page-7-14), finance (risk management of financial assets[\)21](#page-7-15), materials science (metamaterials design[\)22,](#page-7-16) and drug design (molecular similarity search[\)23](#page-7-17).

1 System Platform Research Laboratories, NEC Corporation, 1753 Shimonumabe, Nakahara‑ku, Kawasaki, Kanagawa 211‑8666, Japan. 2 NEC-AIST Quantum Technology Cooperative Research Laboratories, 1‑1‑1 Umezono, Tsukuba, Ibaraki 305‑8568, Japan. email: y-okamoto@aist.go.jp

![](_page_1_Figure_1.jpeg)

In this paper, by using combinatorial optimization based on the Ising model[13,](#page-7-7) we investigated the extent to which partisan gerrymandering under a two-party system is possible to tilt seats in favor of one party starting from a random but even distribution of supporters for both parties. Our model consists of 70 cells that express the distribution of supporters. Supporters of either Party A or B govern each cell. All districts consist of 5 cells, and the total number of seats in the model is 14. If there is support for three or more cells out of 5 cells in a district for either party, the party will get the seat. We observed that both parties could assign the theoretically maximum number of seats by gerrymandering in 8 out of 10 cases of random distribution of the equivalent supporters when a rook constraint forbade enclaves in a district.

## **Methods of computation**

**Model of single‑seat district.** The model examined in this study contains *N*g single-seat districts, and each district consists of *N*c cells. Therefore, the total number of cells in the model is *N*g×*N*c (≡ *N*s). As shown in Fig. [1,](#page-1-0) we arrange the *N*s cells in a rectangle of length *m* and width *l*. The party with a majority of the *N*c cells that make up a district gets the seat. Both parties control half of the *N*s cells. Therefore, the powers of both parties are in equilibrium as a whole. Besides, we assume that *N*s is even, and *N*c is odd to balance the two parties' power and decide which wins in each district. We randomly give the cells' position where Party A governs in the (m×l) rectangle as the initial value. We set *N*g, *N*c, *m*, and *l* as 14, 5, 7, and 10, respectively, unless otherwise stated.

If we can rig the redistricting completely freely in favor of one party from both parties' even distribution, the number of seats won by the party will be Ns/<sup>2</sup> ⌈Nc/2⌉ (<sup>≡</sup> Nmax) at the maximum, where ⌈x⌉ denotes the ceiling function and means the smallest integer greater than or equal to x. Similarly, ⌊x⌋ denotes the floor function and means the largest integer less than or equal to x.

However, we should note that redistricting is usually not unconditional. Thus, we impose a condition to forbid the occurrence of the enclave, called a rook constraint. The rook constraint means that cells in the same district share at least one edge with other cells in the district. In the following, we will explain by assuming that Party A enjoys an advantage over Party B.

**Constrains for districts and cells in the Ising model.** We give the constraints that must be satisfied by districts and cells as follows,

where x g <sup>s</sup> represents 0/1 binary variables, if we assign cell *s* (*s*=0, 1…, *N*s-1) to district *g*, then <sup>x</sup> g <sup>s</sup> is one. Otherwise, it is zero. The first term in RHS means the constraint that the number of cells comprising each district is *N*c. The second term in RHS means the constraint that each cell belongs to only one district. If these constraints fail, the energy of the objective function will increase as a penalty.

**Counting the number of governing cells in each district.** Assuming that *j* is the number of cells in which Party A governs in the district *g*, *j* must satisfy the following constraints.

where y g <sup>j</sup> represents 0/1 ancillary binary variables, if the number of cells where Party A dominates in the district *g* is equal to *j*, then y g <sup>j</sup> is one. Otherwise, it is zero. Besides, <sup>f</sup> (s) represents that if Party A governs cell *s*, then f (s) is one. Otherwise, it is zero. Note that, unlike other binary variables determined through optimization, we give *f*(*s*) as the input data that reflect Party A or B supporters' distribution. The first term in RHS means that y g

H1 cst = N �g−1 g=0 �N �s−1 s=0 x g <sup>s</sup> − Nc �2 + N �s−1 s=0 N �g−1 g=0 x g s − 1 2

H2 cst = N �g−1 g=0 �Nc j=0 y g <sup>j</sup> − <sup>1</sup> + N �g−1 g=0 �Nc j=0 j × y g <sup>j</sup> − N �s−1 s=0 f (s) × xg s 

<span id="page-1-0"></span>**Figure 1.**A model of electoral districts with 70 cells arranged in a 7×10 rectangle (Case 1) where 1(0) means a cell that Party A(B) has an advantage over B(A). Party A controls 35 cells, whereas Party B controls the remaining 35 cells. Red or blue dotted rectangle designates the areas where Party B has a significant advantage.

is a one-hot vector corresponding to 0 to *N*c. The second term in RHS is a constraint that the number of cells in which Party A governs in the district *g* is *j*.

For gerrymandering, we require a driving force to decrease the energy of the objective function during the optimization by redistricting *N*s cells in favor of Party A. We introduce a driving force as follows.

where *p*(*j*) acts to increase the number of districts in favor of Party A. Let *j* be the number of cells in each district where party A governs. If j ≤⌈ Nc <sup>2</sup> ⌉ − <sup>1</sup>, we set <sup>p</sup> j <sup>&</sup>gt; <sup>0</sup> to reduce the districts that are disadvantageous to Party A. On the other hand, if j ≥⌈ Nc <sup>2</sup> ⌉, we set <sup>p</sup> j <sup>&</sup>lt; <sup>0</sup> to increase the districts that are advantageous to Party A. After some trial error, we determined *p*(*j*) as follows,

In this setting of *p*(*j*), losing a seat raises the energy whereas gaining a seat lowers the energy, especially when a party just barely wins at j =⌈ Nc <sup>2</sup> ⌉ number of votes, which lowers the energy significantly.

Finally, we introduce the rook constraint. Two cells that share an edge led to decreasing the energy of the objective function. We give the rook constraint as follows.

Here, *S*rook designates a set in which the two cells *s* and *s*' share an edge. Thus, the Hamiltonian (*H*Ising) of the Ising model is given by

A, B, C, and D represent hyperparameters that regulate the strength of the constraints and objective function. We determined them by Bayesian optimization (BO) using a Gaussian proces[s24.](#page-7-18) The method is suitable for global optimization of black-box functions with low variable dimensionality but high function evaluation cost, such as the problem treated here. It is also advantageous in that no derivative of the function is required for optimization.

We can find the minimum of *H*Ising by optimizing the Hamiltonian. We used tabu search (TS)[25](#page-7-19),[26](#page-7-20) to optimize it because TS gave better results than simulated annealing in our preliminary tests. We used Qbsolv for TS; an application program interface supported in D-Wave Ocean (software development kit developed by D-Wave Systems)[27](#page-7-21). Note that Qbsolv is a quantum–classical hybrid solver for quadratic unconstrained optimization problems with binary variables (QUBO), however, in this paper it is simply used as a classical solver that solves QUBO by TS. Although *H*Ising consists of four partial Hamiltonians (HIsing <sup>=</sup> <sup>A</sup>×H<sup>1</sup> cst <sup>+</sup> B <sup>×</sup> H<sup>2</sup> cst <sup>+</sup> <sup>C</sup> <sup>×</sup> Hgerr <sup>+</sup> <sup>D</sup> <sup>×</sup> Hrook), the division is for the purpose of explaining the formulation, and Qbsolv actually solves one QUBO corresponding to *H*Ising, which is the sum of these terms.

Although *H*rook favors cells that share an edge, we observed that this alone did not prevent the district from containing enclaves. If we regard a district as a graph, the absence/presence of enclaves corresponds to the connected/disconnected graph. It is easy to determine whether a graph is connected or not by using graph theory algorithms. We count the number of districts that have enclaves among *N*g districts and use the number (*N*dis) as a penalty to the objective function of BO (*H*BO) expressed as,

N<sup>1</sup> cst represents the expectation value of H<sup>1</sup> cst by the solution vector *x*opt obtained from optimizing *H*Ising by TS, namely N<sup>1</sup> cst =�xopt|H<sup>1</sup> cst|xopt�. If the solution vector satisfies the constraint given by H<sup>1</sup> cst, then N<sup>1</sup> cst will be zero. Consequently, this value is an indicator of how much the constraint is not satisfied. The same is true for N<sup>2</sup> cst =�xopt|H<sup>2</sup> cst|xopt�. *N*dis also becomes zero if there are no enclaves in all *N*g districts. *N*seat is the number of seats won by Party A, calculated from the solution vector *x*opt. Note that *H*BO will be -*N*max if gerrymandering could assign seats completely tilted manner. However, due to the rook constraint, the value may not be reached depending on the supporters' initial distribution. It is noteworthy that BO takes care of the adjustment of hyperparameters in *H*Ising and the prohibition of enclaves in the districts. We observed that the prohibition of enclaves was difficult to achieve by simply optimizing the Ising model. In this study, we have updated BO a thousand times, and we optimize *H*Ising by TS of 1250 or 5000 trials in each BO update. We carried out BO by using gp\_minimize in scikit-optimiz[e28.](#page-7-22) The parameters for gp\_minimize was set as n\_calls=1000 (number of function calls), and acq\_func='EI' (negative expected improvement).

**Rook constraint.** Fig. [1](#page-1-0) shows an example of supporters' distribution. Hereafter, we refer to this example as Case 1. It requires at least 33 governing cells to set the number of assigned seats (*N*seat) to *N*max(=11 [in this study]) with 3 to 2 hard-won victories (in other words, the seat is won by one vote). Due to the even distribution in the initial condition, the number of cells where each party governs is 35 among 70 cells; thereby, the allowed

Hgerr = N g−1 g=0 Nc j=0 p(j) × y g

p � j � = +<sup>3</sup> <sup>2</sup> <sup>0</sup> <sup>≤</sup> <sup>j</sup> ≤⌈ Nc <sup>2</sup> ⌉− 1 <sup>−</sup><sup>2</sup> j =⌈ Nc <sup>2</sup> ⌉ −<sup>1</sup> <sup>2</sup> ⌈ Nc <sup>2</sup> ⌉ + 1 ≤ j < Nc

Hrook =− N g−1 g=0 s,s ∈Srook x s x g s

HIsing <sup>=</sup> A×H<sup>1</sup> cst <sup>+</sup> <sup>B</sup> <sup>×</sup> <sup>H</sup><sup>2</sup> cst + C × Hgerr + D × Hrook

HBO <sup>=</sup> N<sup>1</sup> cst <sup>+</sup> <sup>N</sup><sup>2</sup> cst + Ndis − Nseat

![](_page_3_Figure_1.jpeg)

number of wasted votes for the governing party is at most two. Only three districts fail to secure seats in *N*<sup>g</sup> districts. When the number of wasted votes is 2 for the governing party, there are two cases: two districts losing 0 to 5 and one losing 2 to 3, or a combination of one district losing 0 to 5 and two losing 1 to 4. Concerning the distribution of supporters of Case 1 (Fig. [1\)](#page-1-0), under the condition that Party A has an advantage (left side in Fig. [2\)](#page-3-0), it has lost seats in districts 0, 6, and 9. In districts 0 and 6, it lost 0 to 5, whereas, in district 9, it lost 2 to 3. On the other hand, under the condition that Party B has an advantage (right side in Fig. [2\)](#page-3-0), it has lost seats in districts 0, 4, and 6. In districts 0 and 4, it lost 1 to 4, whereas, in district 6, it lost 0 to 5.

It is noteworthy that 87.5% of the cells surrounded by the red dotted lines in Fig. [1](#page-1-0) belong to Party B. Packing contributes to Party A by decreasing the own wasted vote and ensuring that Party B's power does not extend outside the area. All three districts where party A was defeated are related to the part surrounded by the red dotted lines. On the other hand, although 75% of the cells surrounded by the blue dotted lines in Fig. [1](#page-1-0) belong to Party B, proper cracking of the area is helpful for Party A to win 3 to 2 by controlling the concentration of supporters of Party B. By controlling the wasted vote in this way, the governing party achieves hard-won victories and great defeats, which maximizes the number of seats won. Note that it would be possible that the number of wasted votes for the governing party could be zero or one, but we had not observed such cases in the present study.

In the above example, the number of seats (*N*seat) won by both A and B reached *N*max. However, there were cases where the value was less than *N*max. Figure [3](#page-4-0) shows such examples. In Case 2, the setting that favors Party A results in a *N*seat of only 9. In this case, cells (1,0), (0,2), and (0,5) are enclaves away from the other cells governed by Party A. Similarly, cells (3,5), (4,6), and (5,8) are also enclaves because although they share vertices with other cells governed by Party A, none of them share the edges needed to satisfy the rook constraint. Comparing these six enclaves with the assigned seats, five cells other than the cell (1,0) result in wasted votes. Due to a large number of wasted votes, the *N*seat of Party A remains at 9. As another example, we show Case 3, where *N*seat remains at 10 in the setting in which Party B has an advantage. It is noteworthy that five cells (1,0), (0,2), (1,3), (1,5), and (0,6) are enclaves, and cells (1,0) and (1,5) become wasted votes. These results suggest that whether or not the number of seats won reaches *N*max depends on the number of enclaving cells for a governing party. It appears difficult for enclaves to form a majority because there are no own party cells around them. To verify this, we examined seven more cases. We show a figure similar to Fig. [3](#page-4-0) as Fig. S1 in Supplementary Information (SI). In a total of 20 optimizations for these 10 cases, the number of times *N*seat=*N*max was 16, whereas the number of times *N*seat<*N*max was 4. The average values of the enclaves were 1.94 (*N*seat=*N*max) and 5 (*N*seat<*N*max), respectively. However, although it appears to be a rare example, it is noteworthy that *N*seat is possible to reach *N*max even from a distribution with many enclaves as in Case 6 (Party A) of Fig. S1 in SI. Besides, the Ising model-based approach does not guarantee optimality, thereby even in the examples where *N*seat<*N*max, the possibility exists that the true optimum is *N*seat=*N*max.

In this study, we optimized the Hamiltonian of the Ising model by TS with every BO update, but its accuracy depended on the number of TS trials (*N*TS). When *N*TS was 1250, *N*seat reached *N*max in 11 out of 20 BOs. When we increased *N*TS to 5000 for nine distributions that did not reach *N*max with an *N*TS of 1250, *N*seat reached *N*max in five of them. Consequently, *N*max was reached 16 times out of 20 BOs. Table [1](#page-4-1) shows the change in the number of feasible solutions obtained during 1000 BO updates by increasing *N*TS from 1250 to 5000. The result indicates

<span id="page-3-0"></span>**Figure 2.**Calculated result of maximizing the number of seats so that party A or B has an advantage with imposing the rook constraint concerning the supporter's distribution shown in Fig. [1](#page-1-0) (Case 1). The top panels show the calculated correspondence between the cells and the 14 districts indexed from 0 to 13. The bottom panels show the assignment of seats based on the calculated districting.

![](_page_4_Figure_1.jpeg)

that the improvement of the probability of finding a feasible solution by increasing *N*TS led to the improved the entire solution's accuracy, including BO.

**Queen constraint.** In addition to the rook constraint where cells share edges, the queen constraint where cells share vertices is a representative constraint for districting. We observed that the latter constraint makes it more difficult for *N*seat to reach *N*max than the former constraint starting from even distribution. We subsequently considered why the computation with the queen constraint being difficult. As shown (A) in Fig. [4](#page-5-0), both the rook and queen constraints have four adjacent cells that satisfy the constraints. However, at the boundary (B) and corner (C), the number of adjacent cells satisfying the constraints is 3 and 2, respectively, in the case of the rook constraint. On the other hand, in the case of the queen constraint, the number of adjacent cells is 2 (at the boundary) and 1 (at the corner). The decrease of the number of adjacent cells at the boundary and the corner in the queen constraint results in an energy disadvantage. Although this is a little ad hoc approach, we changed the energy decrease due to vertex sharing in the partial Hamiltonian of *H*rook at boundaries and corners to twice as much for the queen constraint. As shown in Fig. [5,](#page-5-1) we observed districts that give the maximum number of seats (*N*max) to party A with the queen constraint.

Moreover, although this is a mathematical model that deviates from reality, if we assume that there are periodic boundary conditions on the arrangement of cells (distribution of supporters and districts) to eliminate the effect of boundaries and corners, we can calculate the districts that allow the maximum number of seats (*N*max) to one party with the queen constraint starting from even distribution (Fig. S2 in SI).

<span id="page-4-0"></span>**Figure 3.**Two cases of gerrymandering with rook constraint. In each case, the top panel shows the distribution of the dominant cells where 1(0) means a cell that Party A(B) has an advantage over B(A). Middle panels show the calculated correspondence between the cells and the 14 districts indexed from 0 to 13. The bottom panels show the assignment of seats based on the calculated districting.

<span id="page-4-1"></span>**Table 1.**Comparing the number of times we obtained a feasible solution during 1000 BO updates by TSs with 1250 or 5000 trials. The number in parentheses indicates the number of seats assigned (*N*seat). The TS with 1250 trials was run three times with different random number seeds for the initial value.

|      |                 | N       | TS=1250 |        |           |
|------|-----------------|---------|---------|--------|-----------|
| Case | Governing party |         |         |        |           |
|      |                 | 1       | 2       | 3      | N TS=5000 |
| 1    | B               | 46(10)  | 96(10)  | 30(10) | 53(11)    |
| 2    | A               | 40(9)   | 36(9)   | 27(8)  | 75(9)     |
| 3    | B               | 28(9)   | 28(10)  | 13(10) | 47(10)    |
| 4    | B               | 57(10)  | 63(10)  | 64(10) | 84(11)    |
| 5    | A               | 83(10)  | 91(9)   | 93(10) | 97(11)    |
| 6    | A               | 46(10)  | 46(10)  | 51(10) | 69(11)    |
| 6    | B               | 51(10)  | 50(10)  | 49(10) | 110(10)   |
| 7    | A               | 101(10) | 71(10)  | 90(10) | 150(10)   |
| 8    | A               | 46(10)  | 32(10)  | 42(10) | 71(11)    |

![](_page_5_Diagram_1.jpeg)

**Multiple votes per cell.** In the simulations so far, the number of votes in each cell (*N*v) has been set to one. However, it is easy to extend the formulation to treat the number of votes per cell to *N*v(>1). In this case, the total number of votes in each district changes from *N*c to *N*c×*N*v (≡ *N*<sup>t</sup> ). Therefore, in the partial Hamiltonian related to the total number of votes per district, we must change *N*c to *N*<sup>t</sup> . Specifically, we change *N*c to *N*<sup>t</sup> in *H*<sup>2</sup> cst and *H*gerr. This is a trivial change in terms of formulation, but we found that it was quite difficult to get the correct result because of the expansion of search space through the increased total number of votes.

An example of the calculation is shown below. In a model of eight districts containing a total of 40 cells, each district consists of five cells, and the number of votes per cell is *N*v=3. The left panel of Fig. [6](#page-5-2) shows the number of votes in each cell supporting Party A. The sum of these values in all cells is 60. Since the total number of votes is 120 (=3×40), the number of votes supporting Party B is also 60, and the distribution is even in the initial condition. Since the total number of votes in one district is 15 (=3×5), if either party gets eight or more votes, it will be the winner in that district. Therefore, the maximum number of acquired seats without the constraint of prohibiting enclaves is 7 (=⌈ <sup>60</sup> <sup>8</sup> ⌉). The center of Fig. [6](#page-5-2) shows the redistricting results obtained from the optimization with rook constraint, and the right panel shows the results of the allocation to Party A and Party B based on the redistricting. We observed Party A has acquired the maximum number of seats that can be allocated.

<span id="page-5-0"></span>**Figure 4.**(**A**) The blue and red arrows point to adjacent cells with the rook and queen constraints, respectively. (**B**) At the boundary, the number of adjacent cells under the rook constraint is 3, whereas the number of adjacent cells under the queen constraint is 2. (**C**) At the corner, the number of adjacent cells under the rook constraint is 2, whereas the number of adjacent cells under the queen constraint is 1.

![](_page_5_Figure_3.jpeg)

<span id="page-5-1"></span>**Figure 5.**Gerrymandering with queen constraint. The left panel shows the distribution of the supporters where 1(0) means a cell that Party A(B) has an advantage over B(A). Middle panel shows the calculated correspondence between the cells and the 14 districts indexed from 0 to 13. The right panel shows the assignment of seats based on the calculated districting.

![](_page_5_Figure_5.jpeg)

<span id="page-5-2"></span>**Figure 6.**Gerrymandering in a multiple votes case (3 votes/cell) with rook constraint. The left panel shows the number of votes in each cell for Party A. Center panel shows the calculated correspondence between the cells and the eight districts indexed from 0 to 7. The right panel shows the assignment of seats based on the calculated districting.

![](_page_6_Figure_1.jpeg)

**Application to other fields.** The essence of the algorithm proposed here is to redistribute the disjointed small parts into a compact form according to a set of rules. There appear to be various fields to which such features can be applied. As an example, we will discuss the redistribution of delivery destinations. Company 0 and Company 1 deliver the same product to their customers. Figure [7](#page-6-1) (left) shows which company is in charge of each delivery destination at present. Here, the number of delivery destinations handled by company 0 and company 1 is 49 and 21, respectively, so the share ratio is 7:3. The scattered delivery destinations in the figure cause poor efficiency and long transportation distance, increasing carbon dioxide emissions.

Therefore, we group several destinations to form a group, and one of the companies is in charge of all the destinations in a group. The distribution of the group to each company should reflect its current share as much as possible. Within a group, we do not allow enclaves to reduce the transportation distance and increase the delivery efficiency. Besides, we assign each group to the company having more delivery destinations at present. The rule is important because they do not want to give up their trade area to their competitors. If we combine the five destinations into one group, we get a total of 14 groups. We divide the 14 groups into 10 and 4 groups i.e.,70 cells into 50 and 20 cells, for companies 0 and 1, respectively. The allotment is the closest to the current share ratio of 7:3. If we denote the number of groups allocated to Company 1 determined by the Ising model is *N*<sup>g</sup> 1 , we can use |*N*<sup>g</sup> 1 —*4*| as a component in the objective function of Bayesian optimization (*H*BO) instead of -*N*seat. By redistributing the delivery destinations, we can create 14 compact groups with no enclaves in each group (center and left panels in Fig. [7\)](#page-6-1).

Returning to the subject of electoral redistricting, as the delivery destination optimization example above, the proposed algorithm can also allocate seats in proportion to the total (assumed) number of votes in a state. However, this seemingly fair approach of allocating seats may not be upheld by the U.S. Supreme Court with respect to the U.S. House of Representatives elections, where gerrymandering is most notable. According to Rucho v. Common Caus[e29](#page-7-23), the US Constitution does not require proportional representation, and it cannot be said that each voter has the right to ensure that the party he/she supports wins a number of seats commensurate with its statewide support. Besides, it is impossible to find a clear and court-operable standard as to whether a given districting is excessive partisan gerrymandering or not. The judgement indicated that the U.S. Supreme Court was reluctant to intervene because gerrymandering was a nonjusticiable political question.

# **Conclusion**

We examined the problem of redistricting 70 cells into 14 electoral districts that consist of 5 cells, where the number of cells in which party A or B governs is equal. Besides, a cell in one district must share at least one edge with the other cells in the district (rook constraint). Consequently, enclaves are forbidden. With this assumption, a combined approach of the Ising model optimization by TS and BO maximizes the seats' biased assignment. BO adjusts the hyperparameters in the Ising model and penalizes the formation of enclaves in each district. The approach reached the theoretical upper limit without the rook constraint in 16 out of 20 trials. However, we observed that it was difficult for a party to reach the limit when the cells that the party governed had many enclaves. The essence of this algorithm that redistributing the disjointed small parts into a compact form according to a set of rules appears to have various fields of application. As such an example, we also discussed the redistribution of delivery destinations.

The problem addressed in this paper may be regarded as a kind of puzzle and be included in constraint optimization problem (COP) in the more general category. It has been proposed to solve COP as Boolean satisfiability problem (SAT)[30.](#page-7-24) However, although SAT is a very general approach, it appears to be difficult to express all constraints of this problem in propositional logic formulas efficiently. If the related hardware and software's ability to combinatorial optimization based on the Ising model consistently proceeds, it will be possible to handle more realistic models such as larger districts and multiple votes per cell soon.

<span id="page-6-0"></span>

<span id="page-6-1"></span>**Figure 7.**Companies in charge of each delivery destination at preset (left). Calculated correspondence between the delivery destinations and the 14 groups indexed from 0 to 13 (center). The assignment of company to manage new groups (right).

- <span id="page-7-0"></span>2. Amy, D. J. *Real choices/new voices: The Case for Proportional Representation Elections in the United States* (Columbia. Univ, 1993).
- 3. Dickson, P. & Clancy, P. *The congress dictionary: The ways and meanings of Capitol Hill* (Wiley, 1993).
- 4. Vickrey, W. On the prevention of Gerrymandering. *Polit. Sci. Q.* **76**, 105 (1961).
- <span id="page-7-1"></span>5. Niemi, R. G., Grofman, B., Carlucci, C. & Hofeller, T. Measuring compactness and the role of a compactness standard in a test for partisan and racial Gerrymandering. *J. Polit.* **52**, 1155 (1990).
- <span id="page-7-2"></span>6. Duchin, M. Geometry v. Gerrymandering. *Sci. Am.* **319**, 48 (2018).
- 7. Duchin, M. Gerrymandering metrics: How to measure? What's the baseline? arXiv: 1801.02064 (2018).
- 8. Herschlag, G. *et al.* Quantifying Gerrymandering in North Carolina. *Stat. Public Policy* **7**, 30 (2020).
- <span id="page-7-3"></span>9. Puppe, C. & Tasnádi, A. A computational approach to unbiased districting. *Math. Comput. Model.* **48**, 1455–1460 (2008).
- <span id="page-7-4"></span>10. Stewart, A. J. *et al.* Information gerrymandering and undemocratic decisions. *Nature* **573**, 117 (2019).
- <span id="page-7-5"></span>11. Berghel, H. Chasing Elbridge's Ghost: The digital Gerrymander. *Computer* **49**, 91 (2016).
- <span id="page-7-6"></span>12. Bond, R. M. *et al.* A 61-million-person experiment in social influence and political mobilization. *Nature* **489**, 295 (2012).
- <span id="page-7-7"></span>13. Lucas, A. Ising formulations of many NP problems. *Front. Phys.* **12**, 00005 (2014).
- <span id="page-7-8"></span>14. Johnson, M. W. *et al.* Quantum annealing with manufactured spins. *Nature* **473**, 194 (2011).
- <span id="page-7-9"></span>15. Aramon, M., Rosenberg, G., Valiante, E., Miyazawa, T., Tamura, H. & Katzgraber, H. G. Physics-inspired optimization for quadratic unconstrained problems using a digital annealer. *Front. Phys*. 00048 (2019).
- <span id="page-7-10"></span>16. Okuyama, T., Sonobe, T., Kawarabayashi, K. & Yamaoka, M. Binary optimization by momentum annealing. *Phys. Rev. E* **100**, 012111 (2019).
- <span id="page-7-11"></span>17. Goto, H., Tatsumura, K., & Dixon, A. R. Combinatorial optimization by simulating adiabatic bifurcations in nonlinear Hamiltonian systems. *Sci, Adv*. **5**, eaav2372 (2019).
- <span id="page-7-12"></span>18. Irie, H., Wongpaisarnsin, G., Terabe, M., Miki, A. & Taguchi, S. Quantum annealing of vehicle routing problem with time, state and capacity. arXiv: 1903.06322 (2019).
- <span id="page-7-13"></span>19. Ohzeki, M., Miki, A., Miyama, M. J. & Terabe, M. Control of automated guided vehicles without collision by quantum annealer and digital devices. *Front. Comput. Sci.* **19**, 00009 (2019).
- <span id="page-7-14"></span>20. Ikeda, K., Nakamura, Y. & Humble, T. S. Application of quantum annealing to nurse scheduling problem. *Sci. Rep*. **9**, 12837 (2019).
- <span id="page-7-15"></span>21. Alipour, E., Adolphs, C., Zaribafiyan, A. & Rounds, M. Quantum-Inspired Hierarchical Risk Parity. *1QBit white paper* Retrieved from: <https://1qbit.com/whitepaper/quantum-inspired-hierarchical-risk-parity/>(2016).
- <span id="page-7-16"></span>22. Kitai, K., Guo, J., Ju, S., Tanaka, S., Tsuda, K., Shiomi, J. & Tamura, R. Designing metamaterials with quantum annealing and factorization machines. *Phys. Rev. Res.* **2**, 013319 (2020).
- <span id="page-7-17"></span>23. Okamoto, Y. Finding a maximum common subgraph from molecular structural formulas through the maximum clique approach combined with the Ising model. *ACS Omega* **5**(22), 13064–13068 (2020).
- <span id="page-7-18"></span>24. Frazier, P. I. *A tutorial on Bayesian Optimization*. arXiv: 1807.02811 (2018).
- <span id="page-7-19"></span>25. Glover, F. Tabu search—Part I. *ORSA J. Comput.* **1**(3), 190–206 (1989).
- <span id="page-7-20"></span>26. Glover, F. Tabu search—Part II. *ORSA J. Comput.* **2**(1), 4–32 (1990).
- <span id="page-7-21"></span>27. Booth, M., Reinhardt, S. P. & Roy. A. Partitioning optimization problems for hybrid classical/quantum execution. [https://github.](https://github.com/dwavesystems/qbsolv/blob/master/qbsolv_techReport.pdf) [com/dwavesystems/qbsolv/blob/master/qbsolv\\_techReport.pdf](https://github.com/dwavesystems/qbsolv/blob/master/qbsolv_techReport.pdf) (2017).
- <span id="page-7-22"></span>28. The scikit-optimize.<https://github.com/scikit-optimize/scikit-optimize>(2016).
- <span id="page-7-23"></span>29. Rucho v. Common Cause, No. 18-422, 588 U.S. \_\_\_ (2019).
- <span id="page-7-24"></span>30. Tamura, N., Taga, A., Kitagawa, S. & Banbara, M. Compiling finite linear CSP into SAT. *Constraints* **14**, 254–272 (2009).

## **Acknowledgements**

I would like to thank Prof. Matsui for teaching me about the interpretation of Rucho v. Common Cause. This paper was (partly) based on the results obtained from a project, JPNP16007, commissioned by the New Energy and Industrial Technology Development Organization (NEDO), Japan.

## **Author contributions**

Y.O performed all experiments and analysis.

#### **Competing interests**

The author declares no competing interests.

## **Additional information**

**Supplementary Information** The online version contains supplementary material available at [https://doi.org/](https://doi.org/10.1038/s41598-021-03050-z) [10.1038/s41598-021-03050-z.](https://doi.org/10.1038/s41598-021-03050-z)

**Correspondence** and requests for materials should be addressed to Y.O.

**Reprints and permissions information** is available at [www.nature.com/reprints.](www.nature.com/reprints)

**Publisher's note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

**Open Access** This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit<http://creativecommons.org/licenses/by/4.0/>.

![](_page_7_Picture_14.jpeg)

© The Author(s) 2021