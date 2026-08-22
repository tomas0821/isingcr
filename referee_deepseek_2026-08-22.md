[0m
> build · deepseek-reasoner
[0m
[0m→ [0mRead manuscript/main.tex
[0m→ [0mRead manuscript/main.tex[90m [offset=863][0m
[0m→ [0mRead manuscript/main.tex[90m [offset=1687][0m
Now let me examine the references and the novelty check document to assess prior-art claims.
[0m
[0m$ [0mls manuscript/
README.md
figures
main.aux
main.bbl
main.blg
main.log
main.out
main.pdf
main.spl
main.tex
references.bib
[0m
[0m✱ [0mGlob "manuscript/references.bib"[90m 0 matches[0m
[0m→ [0mRead manuscript/references.bib
Let me check the novelty check document and the project README for consistency context.
[0m→ [0mRead NOVELTY_CHECK.md
Let me verify a few technical claims against the codebase and check the questionable references.
[0m
[0m$ [0mrg -n "J_|border_length|border len|normaliz|weight" isingcr/utils/graph_arrays.py | head -50
/bin/bash: line 1: rg: command not found
[0m
[0m✱ [0mGrep "def build_electoral_graph|def _build_adjacency|border"[90m 43 matches[0m
[0m→ [0mRead src/isingcr/ingestion/shapefile_adjacency.py
[0m
[0m$ [0mgrep -rn "def binarize_votes" src/ ; grep -rn "margin" src/isingcr/ingestion/*.py | head
src/isingcr/ingestion/binarize.py:9:def binarize_votes(df: pd.DataFrame, group_a: list[str], group_b: list[str],
src/isingcr/ingestion/binarize.py:22:    DataFrame with [code, spin, margin], where margin = (votes_a - votes_b) / (votes_a + votes_b)
src/isingcr/ingestion/binarize.py:29:    margin = np.divide(votes_a - votes_b, total, out=np.zeros_like(total, dtype=float), where=total > 0)
src/isingcr/ingestion/binarize.py:30:    return pd.DataFrame({code_col: df[code_col].values, "spin": spin, "margin": margin})
src/isingcr/ingestion/graph_builder.py:28:        (e.g. a rescaled incumbency/margin score). Falls back to `default_h`.
src/isingcr/ingestion/mideplan_ids.py:109:    (unlike the vote-margin field, which is already centered by construction)
[0m
[0m$ [0mgrep -rn "def pooled_temperature_scan\|def temperature_scan\|def mcnemar\|def spatial_block" src/ | head
src/isingcr/simulation/observables.py:37:def mcnemar_test(model_spins: np.ndarray, null_spins: np.ndarray,
src/isingcr/simulation/observables.py:73:def mcnemar_seed_summary(final_spins_per_seed: list, empirical_spins: np.ndarray,
src/isingcr/simulation/observables.py:99:def spatial_block_permutation_test(model_spins: np.ndarray, empirical_spins: np.ndarray,
src/isingcr/simulation/observables.py:133:def spatial_block_permutation_test_paired(spins_a: np.ndarray, spins_b: np.ndarray,
src/isingcr/simulation/monte_carlo.py:70:def temperature_scan(J: sp.spmatrix, h: np.ndarray, temperatures: Sequence[float],
src/isingcr/simulation/monte_carlo.py:102:def pooled_temperature_scan(J: sp.spmatrix, h: np.ndarray, temperatures: Sequence[float],
[0m
[0m→ [0mRead src/isingcr/simulation/observables.py
[0m
[0m$ [0mgrep -n "n_permutations\|spatial_block\|0.0005\|median_p\|paired" scripts/run_gam*.py scripts/run_3d_scan.py scripts/run_direct_paired_test.py 2>/dev/null | head -40
scripts/run_gam_cascade_analysis.py:84:        # Same pattern as run_direct_paired_test.py's best_t_final_spins_aligned.
scripts/run_gam_domain_wall_analysis.py:15:Reuses the exact spin configurations each year's GAM paired significance
scripts/run_gam_domain_wall_analysis.py:39:from run_direct_paired_test import best_t_final_spins_aligned
scripts/run_gam_field.py:108:        "accuracy_by_T": per_t_accuracy, "mcnemar_median_p": mc["median_exact_pvalue"],
scripts/run_gam_field.py:157:          f"best accuracy={r['best_accuracy']:.3%}, McNemar median p={r['mcnemar_median_p']:.4f} "
scripts/run_gam_polarization_trend.py:18:accuracy, and (3) the direct paired significance test between them
scripts/run_gam_polarization_trend.py:19:(spatial_block_permutation_test_paired, PROVINCE-blocked -- matches
scripts/run_gam_polarization_trend.py:20:run_direct_paired_test.py's canton-level convention exactly, since canton-
scripts/run_gam_polarization_trend.py:45:from run_direct_paired_test import best_t_final_spins_aligned, paired_test, province_blocks
scripts/run_gam_polarization_trend.py:102:            "mcnemar_median_p": mc["median_exact_pvalue"]}
scripts/run_gam_polarization_trend.py:130:              f"(p={r_geo['mcnemar_median_p']:.4f})")
scripts/run_gam_polarization_trend.py:132:              f"(p={r_gam['mcnemar_median_p']:.4f})")
scripts/run_gam_polarization_trend.py:139:        paired = paired_test(f"{label}: geography-only vs. GAM", spins_a, spins_b, empirical,
scripts/run_gam_polarization_trend.py:142:        results[label] = {"gap_pp": gap, "geo": r_geo, "gam": r_gam, "paired": paired}
scripts/run_gam_polarization_trend.py:149:        sig = int(round(r["paired"]["frac_sig"] * N_SEEDS))
scripts/run_gam_polarization_trend.py:151:              f"{r['gam']['best_accuracy']:>10.2%}{gain:>+8.2%}{r['paired']['median_p']:>10.4f}"
scripts/run_gam_polarization_trend.py:158:             **{f"{label}_paired_p": r["paired"]["median_p"] for label, r in results.items()})
scripts/run_3d_scan.py:146:        "accuracy_by_T": per_t_accuracy, "mcnemar_median_p": mc["median_exact_pvalue"],
scripts/run_3d_scan.py:258:              f"McNemar median p={r['mcnemar_median_p']:.4f}")
scripts/run_direct_paired_test.py:2:"""Direct paired test: does adding h (geography+margin, arm B) actually
scripts/run_direct_paired_test.py:9:Uses `spatial_block_permutation_test_paired` (isingcr.simulation.observables),
scripts/run_direct_paired_test.py:19:For each of the paired seeds (seed i of arm A vs. seed i of arm B), computes
scripts/run_direct_paired_test.py:20:one paired test; reports the median p-value and the fraction of seed-pairs
scripts/run_direct_paired_test.py:47:    spatial_block_permutation_test_paired,
scripts/run_direct_paired_test.py:76:def paired_test(label, spins_a_list, spins_b_list, empirical, blocks, n_seeds):
scripts/run_direct_paired_test.py:77:    ps = [spatial_block_permutation_test_paired(sa, sb, empirical, blocks,
scripts/run_direct_paired_test.py:78:                                                 n_permutations=N_PERMUTATIONS,
scripts/run_direct_paired_test.py:81:    median_p = float(np.median(ps))
scripts/run_direct_paired_test.py:84:    print(f"  median p={median_p:.4f}  significant in {int(round(frac_sig*n_seeds))}/{n_seeds} seed-pairs")
scripts/run_direct_paired_test.py:85:    return {"ps": np.array(ps), "median_p": median_p, "frac_sig": frac_sig}
scripts/run_direct_paired_test.py:89:    print("=== Canton-level: direct paired test, arm A (h=0, T=2.60) vs. "
scripts/run_direct_paired_test.py:110:    return paired_test("canton (province blocks)", spins_a, spins_b, empirical, blocks, N_SEEDS)
scripts/run_direct_paired_test.py:114:    print("\n=== Distrito-level: direct paired test, arm A (h=0, T=2.83) vs. "
scripts/run_direct_paired_test.py:137:    return paired_test("distrito (canton blocks)", spins_a, spins_b, empirical, blocks, N_SEEDS)
scripts/run_direct_paired_test.py:144:    np.savez(RESULTS_DIR / "direct_paired_test.npz",
scripts/run_direct_paired_test.py:145:             canton_ps=canton["ps"], canton_median_p=canton["median_p"], canton_frac_sig=canton["frac_sig"],
scripts/run_direct_paired_test.py:146:             distrito_ps=distrito["ps"], distrito_median_p=distrito["median_p"],
scripts/run_direct_paired_test.py:148:    print(f"\nRaw results written to {RESULTS_DIR / 'direct_paired_test.npz'}")
[0m
[0m$ [0mgrep -n "N_PERMUTATIONS" scripts/run_direct_paired_test.py scripts/run_gam_polarization_trend.py scripts/run_mideplan*.py scripts/run_gam_field.py 2>/dev/null
scripts/run_direct_paired_test.py:58:N_PERMUTATIONS = 999
scripts/run_direct_paired_test.py:78:                                                 n_permutations=N_PERMUTATIONS,
scripts/run_gam_polarization_trend.py:65:N_PERMUTATIONS = 999
[0m
[0m$ [0mls results/ 2>/dev/null | head -40; grep -rn "0.0005\|p=0.0005" results/ 2>/dev/null | head
(no output)
[0m
[0m$ [0mls -d */ 2>/dev/null; find . -name "*.npz" -not -path "*/node_modules/*" 2>/dev/null | head; find . -type d -name "results*" 2>/dev/null | head
data/
docs/
figures/
manuscript/
papers_md/
processed_networks/
scripts/
src/
tests/
./.venv/lib/python3.12/site-packages/scipy/interpolate/tests/data/bug-1310.npz
./.venv/lib/python3.12/site-packages/scipy/interpolate/tests/data/gcvspl.npz
./.venv/lib/python3.12/site-packages/scipy/fftpack/tests/fftw_double_ref.npz
./.venv/lib/python3.12/site-packages/scipy/fftpack/tests/fftw_single_ref.npz
./.venv/lib/python3.12/site-packages/scipy/fftpack/tests/fftw_longdouble_ref.npz
./.venv/lib/python3.12/site-packages/scipy/fftpack/tests/test.npz
./.venv/lib/python3.12/site-packages/scipy/spatial/tests/data/degenerate_pointset.npz
./.venv/lib/python3.12/site-packages/scipy/sparse/linalg/tests/propack_test_data.npz
./.venv/lib/python3.12/site-packages/scipy/special/tests/data/local.npz
./.venv/lib/python3.12/site-packages/scipy/special/tests/data/gsl.npz
[0m
[0m$ [0mgrep -n "paired\|0.0005\|15/16\|N_PERM\|999" scripts/run_gam_field.py scripts/run_gam_cascade_analysis.py scripts/run_gam_domain_wall_analysis.py 2>/dev/null | head -30
scripts/run_gam_cascade_analysis.py:84:        # Same pattern as run_direct_paired_test.py's best_t_final_spins_aligned.
scripts/run_gam_domain_wall_analysis.py:15:Reuses the exact spin configurations each year's GAM paired significance
scripts/run_gam_domain_wall_analysis.py:39:from run_direct_paired_test import best_t_final_spins_aligned
[0m
[0m$ [0mgrep -n "def best_t_final_spins_aligned\|def paired_test\|N_PERMUTATIONS" scripts/run_direct_paired_test.py | head; sed -n '30,60p' scripts/run_direct_paired_test.py
58:N_PERMUTATIONS = 999
69:def best_t_final_spins_aligned(J, h, T, empirical, n_equil, n_sweeps, n_seeds, n_jobs, seed):
76:def paired_test(label, spins_a_list, spins_b_list, empirical, blocks, n_seeds):
78:                                                 n_permutations=N_PERMUTATIONS,
import networkx as nx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.ingestion import (
    binarize_votes,
    build_adjacency_graph,
    build_electoral_graph,
    load_shapefile,
    load_tse_juntas_consolidado,
    normalize_canton_code,
    normalize_distrito_code,
)
from isingcr.simulation.monte_carlo import temperature_scan
from isingcr.simulation.observables import (
    alignment_fraction,
    spatial_block_permutation_test_paired,
)
from isingcr.utils.graph_arrays import graph_to_arrays

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TSE_RESULTS_ZIP = DATA_RAW / "tse_juntas" / "DEFINITIVO_juntas_TSE_2026.zip"
TSE_MEMBER = "_consolidado_presidenciales.csv"
LEADING_PARTY = ["PUEBLO SOBERANO"]
COALITION_PARTIES = ["LIBERACION NACIONAL", "COALICION AGENDA CIUDADANA", "FRENTE AMPLIO"]
N_PERMUTATIONS = 999
[0m
Now let me verify the two suspicious references via DOI resolution.
[0m$ [0mcurl -s "https://api.crossref.org/works/10.35242/rde_2019_28_11" --max-time 30 2>/dev/null | head -c 1200
{"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2026,6,15]],"date-time":"2026-06-15T14:54:45Z","timestamp":1781535285755,"version":"3.54.5"},"reference-count":0,"publisher":"Tribunal Supremo de Elecciones","content-domain":{"domain":[],"crossmark-restriction":false},"short-container-title":["RDE"],"published-print":{"date-parts":[[2006]]},"DOI":"10.35242\/rde_2019_28_11","type":"journal-article","created":{"date-parts":[[2019,8,1]],"date-time":"2019-08-01T15:15:21Z","timestamp":1564672521000},"page":"195-216","source":"Crossref","is-referenced-by-count":0,"title":["El sistema de partidos en los cantones: an\u00e1lisis de la distribuci\u00f3n territorial de los apoyos (1953-2016)"],"prefix":"10.35242","author":[{"given":"Mar\u00eda Jos\u00e9","family":"Cascante Matamoros","sequence":"first","affiliation":[],"role":[{"vocabulary":"crossref","role":"author"}]},{"given":"Sharon","family":"Camacho S\u00e1nchez","sequence":"additional","affiliation":[],"role":[{"vocabulary":"crossref","role":"author"}]}],"member":"19855","container-title":["Revista de Derecho Electoral"],"original-title":["The party system in cantons:  analysis of the t
[0m
[0m$ [0mcurl -sI -o /dev/null -w "%{http_code} %{url_effective}\n" -L "https://doi.org/10.1103/9gjj-1df6" --max-time 30 2>&1; echo "---"; curl -s -o /dev/null -w "%{http_code}\n" "https://api.crossref.org/works/10.1103/9gjj-1df6" --max-time 30 2>&1
403 https://link.aps.org/doi/10.1103/9gjj-1df6
---
200
[0m
[0m$ [0mcurl -s "https://api.crossref.org/works/10.1103/9gjj-1df6" --max-time 30 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin)['message']; print('title:', d.get('title')); print('journal:', d.get('container-title')); print('volume:', d.get('volume'), 'issue:', d.get('issue'), 'page:', d.get('page')); print('issued:', d.get('issued')); print('authors:', [a.get('family') for a in d.get('author',[])]); print('type:', d.get('type'))"
title: ['Empirical Validation of the Polarization Transition in a Double-Random Field Model of Elections']
journal: ['Physical Review Letters']
volume: 136 issue: 12 page: None
issued: {'date-parts': [[2026, 3, 27]]}
authors: ['Korbel', 'Dahdoul', 'Thurner']
type: journal-article
[0m
[0m$ [0mcurl -s "https://api.crossref.org/works/10.35242/rde_2019_28_11" --max-time 30 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin)['message']; print('title:', d.get('title')); print('journal:', d.get('container-title')); print('volume:', d.get('volume'), 'issue:', d.get('issue')); print('issued:', d.get('issued')); print('published:', d.get('published')); print('published-print:', d.get('published-print')); print('created:', d.get('created'))"
title: ['El sistema de partidos en los cantones: análisis de la distribución territorial de los apoyos (1953-2016)']
journal: ['Revista de Derecho Electoral']
volume: None issue: None
issued: {'date-parts': [[2006]]}
published: {'date-parts': [[2006]]}
published-print: {'date-parts': [[2006]]}
created: {'date-parts': [[2019, 8, 1]], 'date-time': '2019-08-01T15:15:21Z', 'timestamp': 1564672521000}
[0m
Let me read the Korbel paper summary to check the positioning claims.
[0m$ [0mls papers_md/ 2>/dev/null; ls papers_md/korbel* 2>/dev/null
CONVERSION_NOTES.md
braha2017
camachosanchez2025
cardoso2022
cardoso2023
cascantematamoros2006
chavarriamora2022
dibenedetto2023
galam2021
godoylorite2020
jordan2020
korbel2026
massoli2026
mitra2026
mullick2025
okamoto2021
raducha2025
siegenfeld2020
tiwari2021
_page_14_Figure_1.jpeg
_page_15_Figure_1.jpeg
_page_16_Figure_1.jpeg
_page_2_Figure_1.jpeg
_page_3_Figure_1.jpeg
_page_7_Diagram_2.jpeg
_page_7_Figure_3.jpeg
_page_7_Figure_5.jpeg
_page_8_Figure_1.jpeg
_page_8_Figure_3.jpeg
korbel2026.md
korbel2026_meta.json
[0m
[0m$ [0mwc -l papers_md/korbel2026/korbel2026.md; grep -n -i "monte carlo\|mean.field\|self.consisten\|configuration.model\|campaign spend\|bimodal\|social temperature\|US House\|1980\|spatial\|geograph" papers_md/korbel2026/korbel2026.md | head -50
352 papers_md/korbel2026/korbel2026.md
13:We model bipartisan elections where voters are exposed to two forces: local homophilic interactions and external influence from two political campaigns. The model is mathematically equivalent to the random field Ising model with a bimodal field. When both parties exceed a critical campaign spending, the system undergoes a phase transition to a highly polarized state where homophilic influence becomes negligible, and election outcomes mirror the proportion of voters aligned with each campaign, independent of total spending. The model predicts a hysteresis region, where the election results are not determined by campaign spending but by incumbency. Calibrating the model with historical data from US House elections between 1980 and 2020, we find the critical campaign spending to be ∼ 1.8 million USD. Campaigns exceeding critical expenditures increased in 2018 and 2020, suggesting a boost in political polarization.
21:A central challenge in complex adaptive systems such as societies is the variety of time-dependent interactions, co-evolution, herding, and anticipation of others' actions [\[39\]](#page-5-30). While some aspects are easy to model, calibration and validation remain difficult, requiring great care to ensure testable models. Here, we address opinion formation with multiple interaction types, as in political elections. Voters exchange views within social networks of family, friends, and colleagues, while also following political campaigns—typically only those of their preferred party. We model these two processes through Ising interactions for homophily and a bimodal random field for campaign influence. Together, they form a Random Field Ising Model (RFIM), extending spin-spin interactions with site-dependent random external fields. An equivalent mean-field description can be derived from a master-equation of stochastic opinion switching with preference and adaptation terms, as originally introduced in the context of sociodynamics [\[40,](#page-5-31) [41\]](#page-5-32).
23:Despite its simplicity, the RFIM captures rich behavior such as quenched disorder and complex phase diagrams [\[42–](#page-5-33)[44\]](#page-5-34). Variants with bimodal random fields, where the field takes two values [\[45–](#page-5-35)[47\]](#page-5-36), exhibit tri-critical points marking the transition from second- to first-order phase changes [\[48,](#page-6-0) [49\]](#page-6-1). In the context of an election campaign, the RFIM represents a bipartisan electorate where each voter holds a binary preference. Voters occupy a social (friendship) network and are randomly assigned one of two field values: the sign encodes campaign affiliation, while the magnitude reflects campaign strength, with spending serving as a proxy. A schematic illustration is shown in End Matter, Fig. [3.](#page-7-0) RFIM approaches have long been used in sociophysics [\[50,](#page-6-2) [51\]](#page-6-3), specifically to illustrate qualitative campaign effects [\[38\]](#page-5-29), but have never been calibrated to an Ising-type model with data on campaign spending. The model employs concepts such as temperature and external fields, which should be understood as effective parameters that summarize complex
29:The aim of this paper is to understand how the interplay between homophily and campaign-following leads to the emergence of campaign polarization in ways that can be calibrated to data. Campaign polarization is defined as the normalized difference between the average opinions of voters exposed to each campaign. Low polarization indicates that both groups vote similarly, with decisions mainly shaped by homophily, whereas high polarization means that groups align with campaigns and are less influenced by neighbors. We compute the phase diagram as a function of the "temperature," representing susceptibility to opinion change, and the campaign spending of the two parties.
31:We focus on the effects of increasing campaign intensity. At low spending, opinions are shaped mainly by homophily, but as campaign influence grows, voter preferences are increasingly influenced by campaign messaging. Key questions are: when does campaign alignment outweigh homophilic similarity, how does polarization evolve at this point, and how does this transition affect social tension and election outcomes? A strength of our model is that it can be calibrated and tested on empirical data; we use the US House elections between 1980 and 2020, particularly. Calibration allows us to infer the "temperature" and the critical spending threshold above which campaign polarization rises sharply, and to track how many races exceeded this threshold over four decades. To our knowledge, this is the first time that thermodynamic parameters and a critical spending threshold are directly extracted from historical election data and used to predict levels of polarization in society.
33:Election model as an RFIM with a bimodal field. — We consider N voters with binary opinions s<sup>i</sup> ∈ ±1, representing preference for one of two parties in a bipartisan election. Voters form a social network encoded in the adjacency matrix Aij and interact through homophily, tending to align with neighbors. Each voter also follows one of the two campaigns, modeled by an external field h<sup>i</sup> drawn from a bimodal distribution,
41:To solve the model, we apply two approximations: the configuration model and a mean-field approximation (see Supplemental Material). Denoting the average magnetization by m = ⟨si⟩, we arrive at the meanfield Hamiltonian HMF (s1, . . . , s<sup>N</sup> ) = − P i (Jm˜ + hi)s<sup>i</sup> , where J˜ = J⟨k⟩ and ⟨k⟩ is the average node degree. The equilibrium distribution is therefore p(s|h <sup>±</sup>) = exp h −β(Jm˜ ± h <sup>±</sup>)s i /Z<sup>±</sup>, where β = (kT) −1 is the inverse temperature (for the rest of the paper, we set k = 1), and Z <sup>±</sup> = 2 cosh h β(Jm˜ ± h ±) i is the partition function. Here, the temperature T represents social volatility—the willingness of individuals to adopt new opinions, even if this increases social stress.
55:3 We extend this result to the non-symmetric case using Eq. [\(4\)](#page-1-1), which links h <sup>+</sup> and h <sup>−</sup>, and by expanding the self-consistency equation [\(3\)](#page-1-0) around m = 0. Unlike the symmetric case, the quadratic term does not vanish, yielding the critical curves
63:Phase diagram. — In the (h <sup>+</sup>, h<sup>−</sup>) plane, we solve Eq. [\(3\)](#page-1-0) numerically to obtain the phase diagrams shown in Fig. [1.](#page-2-0) For T ≥ 1, the system has a single stable solution: the candidate with higher campaign spending wins, with the boundary given by Eq. [\(4\)](#page-1-1). For T < 1 and low fields, a hysteresis region appears around the curve given by Eq. [\(4\)](#page-1-1) until reaching the critical values of
73:Calibration to US House election data. — To test the model against real data, we analyze all US House campaigns in 435 districts across 21 elections (presidential and midterms) from 1980–2020. Campaign spending and results are publicly available via the Federal Election Commission (FEC) [\[59\]](#page-6-10) and in machine-readable form at [\[60\]](#page-6-11). We focus on House races because congressional districts have relatively uniform populations, enabling meaningful spending comparisons. To ensure bipartisan competition, we restrict to races contested solely between Democratic and Republican candidates, excluding those with significant third-party or independent contenders. This yields 6357 races from 9135 in the period. All campaign expenditures are inflation-adjusted to 2020 USD using the Consumer Price Index (CPI). For each race, the campaign share parameter p is set by the previous election result in the same district. For the first election in our dataset (1980), p is taken from the 1978 publicly available results.
81:FIG. 2: Estimation of model parameters for US House of Representatives. We compare campaign spending and election results for 6357 of 9135 races between 1980–2020, focusing on close races (p = 0.5 ± 0.05). (a) For T ≥ 1, the classification model (see Supplemental Material) predicts the higher-spending candidate wins. (b) For T < 1, it predicts an incumbency region (yellow) where incumbents win despite lower spending. (c) Optimal parameters T and h<sup>c</sup> are estimated by maximizing classification accuracy across all 6357 races, yielding T <sup>∗</sup> = 0.922 and h<sup>c</sup> = \$1.83M. Cases where incumbents win with lower spending are highlighted, with additional black borders for points in the hysteresis region. The spending diagram is truncated to show the incumbency region (yellow). (d) Accuracy across T is shown, with the maximum marked by a red star. The inset shows a McNemar contingency table comparing the optimal model (T = T ∗ ) to the null model (T = 1). The McNemar test gives p < 0.0001, indicating significantly better performance of the optimal model.
95:Discussion. — We introduced a simple election model combining two mechanisms influencing voter decisions: homophily, i.e., interactions with family, friends, and close contacts, and political campaign influence. Despite its simplicity, the model can be calibrated with real-world data (US House elections) and reproduces rich behavior absent in earlier work. The fact that voters typically follow only one campaign leads to a phase transition: campaign polarization rises sharply once both parties exceed a critical spending threshold. In this regime, most outcomes are 50:50 when p ≈ 0.5 (swing states), regardless of the detailed spending. For biased states (p ̸≈ 0.5), the model allows us to estimate the challenger's minimum spending above which 50:50 outcomes become possible.
103:Despite its simplicity, the model predicts complex game-theoretic behavior. Strategic aspects of campaigns have been studied from this perspective [\[68,](#page-6-19) [69\]](#page-6-20), and our results deepen this understanding. The model suggests that candidates may rationally raise spending to induce polarization; once reached, it is difficult for opponents to reverse, locking in an advantage. This is especially effective in partisan districts, where dominant candidates benefit from driving the electorate into a polarized phase. Yet this strategy carries social costs: polarization erodes ties across divides and exacerbates fragmentation. A key implication of the model is that regulatory interventions, such as caps on campaign spending, may be needed to prevent undesirable outcomes. While spending limits are under renewed discussion [\[70\]](#page-6-21), our results add a novel perspective by emphasizing the broader societal costs of unbounded campaign intensity.
124:  - A. Nowak, F. Saracco, P. Holme, and M. de Domenico, [The physics of news, rumors, and opinions](https://arxiv.org/abs/2510.15053) (2025), [arXiv:2510.15053 \[physics.soc-ph\].](https://arxiv.org/abs/2510.15053) [36] S. Fortunato and C. Castellano, Scaling and universality in proportional elections, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.99.138701) 99, 138701 [\(2007\).](https://doi.org/10.1103/PhysRevLett.99.138701) [37] R. Pal, A. Kumar, and M. S. Santhanam, Universal statistics of competition in democratic elections, [Phys.](https://doi.org/10.1103/PhysRevLett.134.017401) Rev. Lett. 134[, 017401 \(2025\).](https://doi.org/10.1103/PhysRevLett.134.017401) [38] M. Tiwari, X. Yang, and S. Sen, Modeling the nonlinear effects of opinion kinematics in elections: A simple Ising model with random field-based study, [Physica A](https://doi.org/https://doi.org/10.1016/j.physa.2021.126287) 582, [126287 \(2021\).](https://doi.org/https://doi.org/10.1016/j.physa.2021.126287) [39] S. Thurner, R. Hanel, and P. Klimek, Introduction to the Theory of Complex Systems (Oxford University Press, 2018). [40] W. Weidlich, Physics and social science—the approach of synergetics, [Phys. Rep.](https://doi.org/10.1016/0370-1573(91)90024-G) 204, 1 (1991). [41] W. Weidlich and G. Haag, Concepts and models of a quantitative sociology: The dynamics of interacting populations, Vol. 14 (Springer Science & Business Media, 2012). [42] Y. Imry and S.-k. Ma, Random-field instability of the ordered state of continuous symmetry, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.35.1399) 35[, 1399 \(1975\).](https://doi.org/10.1103/PhysRevLett.35.1399) [43] J. Bricmont and A. Kupiainen, Lower critical dimension for the random-field Ising model, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.59.1829) 59, [1829 \(1987\).](https://doi.org/10.1103/PhysRevLett.59.1829) [44] N. G. Fytas, V. Mart´ın-Mayor, M. Picco, and N. Sourlas, Review of recent developments in the random-field Ising model, [J. Stat. Phys.](https://doi.org/10.1007/s10955-018-1955-7) 172, 665 (2018). [45] A. K. Hartmann and U. Nowak, Universality in three dimensional random-field ground states, [Eur. Phys. J. B](https://doi.org/10.1007/s100510050593) 7[, 105 \(1999\).](https://doi.org/10.1007/s100510050593) [46] J. Sinova and G. Canright, Nature and number of distinct phases in the random-field Ising model, [Phys. Rev. B](https://doi.org/10.1103/PhysRevB.64.094402) 64, [094402 \(2001\).](https://doi.org/10.1103/PhysRevB.64.094402) [47] N. G. Fytas and A. Malakis, Phase diagram of the 3d bimodal random-field Ising model, [Eur. Phys. J. B](https://doi.org/10.1140/epjb/e2008-00039-7) 61,
126:- [111 \(2008\).](https://doi.org/10.1140/epjb/e2008-00039-7) [48] A. Aharony, Tricritical points in systems with random fields, Phys. Rev. B 18[, 3318 \(1978\).](https://doi.org/10.1103/PhysRevB.18.3318) [49] I. Hadjiagapiou, The random-field Ising model with asymmetric bimodal probability distribution, [Physica A](https://doi.org/https://doi.org/10.1016/j.physa.2010.05.033) 389[, 3945 \(2010\).](https://doi.org/https://doi.org/10.1016/j.physa.2010.05.033) [50] S. Galam, Rational group decision making: A random field ising model at t = 0, Physica A 238[, 66 \(1997\).](https://doi.org/https://doi.org/10.1016/S0378-4371(96)00456-6) [51] J.-P. Bouchaud, Crises and collective socio-economic phenomena: Simple models and challenges, [J. Stat. Phys.](https://doi.org/10.1007/s10955-012-0687-3) 151[, 567 \(2013\).](https://doi.org/10.1007/s10955-012-0687-3) [52] S. P. Anderson and G. Glomm, Incumbency effects in political campaigns, [Public Choice](https://doi.org/10.1007/BF00140768) 74, 207 (1992). [53] A. Fowler, A Bayesian explanation for the effect of incumbency, [Elect. Stud.](https://doi.org/https://doi.org/10.1016/j.electstud.2018.03.005) 53, 66 (2018). [54] J. N. Druckman, M. J. Kifer, and M. Parkin, Campaign rhetoric and the incumbency advantage, [Am. Politics](https://doi.org/10.1177/1532673X18822314) Res. 48[, 22 \(2020\).](https://doi.org/10.1177/1532673X18822314) [55] A. V. Hirsch, Polarization and campaign spending in elections, J. Politics 85[, 240 \(2023\).](https://doi.org/10.1086/722045) [56] S. Iyengar, G. Sood, and Y. Lelkes, Affect, not ideology: A social identity perspective on polarization, [Public](https://doi.org/10.1093/poq/nfs038) Opin. Q. 76[, 405 \(2012\).](https://doi.org/10.1093/poq/nfs038) [57] Y. Lelkes, Mass polarization: Manifestations and measurements, [Public Opin. Q.](https://doi.org/10.1093/poq/nfw005) 80, 392 (2016). [58] S. Iyengar, Y. Lelkes, M. Levendusky, N. Malhotra, and
127:- <span id="page-6-12"></span><span id="page-6-11"></span><span id="page-6-10"></span><span id="page-6-9"></span><span id="page-6-8"></span><span id="page-6-7"></span><span id="page-6-6"></span>S. J. Westwood, The origins and consequences of affective polarization in the united states, [Annu. Rev. Poltical Sci.](https://doi.org/10.1146/annurev-polisci-051117-073034) 22[, 129 \(2019\).](https://doi.org/10.1146/annurev-polisci-051117-073034) [59] [https://www.fec.gov/.](https://www.fec.gov/) [60] A. Bonica, Database on ideology, money in politics, and elections (dime), <https://data.stanford.edu/dime> (2024), Stanford, CA. [61] A. Fouirnaies and A. B. Hall, The financial incumbency advantage: Causes and consequences, [J. Politics](https://doi.org/10.1017/S0022381614000139) 76, 711 [\(2014\).](https://doi.org/10.1017/S0022381614000139) [62] Pew Research Center, [The partisan divide on political](https://www.pewresearch.org/politics/2017/10/05/the-partisan-divide-on-political-values-grows-even-wider/) [values grows even wider](https://www.pewresearch.org/politics/2017/10/05/the-partisan-divide-on-political-values-grows-even-wider/) (2017). [63] G. C. Jacobson, It's nothing personal: The decline of the incumbency advantage in us house elections, [J. Politics](https://doi.org/10.1086/681670) 77[, 861 \(2015\).](https://doi.org/10.1086/681670) [64] W. J. Stone, S. A. Fulton, C. D. Maestas, and L. S. Maisel, Incumbency reconsidered: Prospects, strategic retirement, and incumbent quality in u.s. house elections,
128:- <span id="page-6-22"></span><span id="page-6-21"></span><span id="page-6-20"></span><span id="page-6-19"></span><span id="page-6-18"></span><span id="page-6-17"></span><span id="page-6-16"></span><span id="page-6-15"></span><span id="page-6-14"></span><span id="page-6-13"></span>J. Politics 72[, 178 \(2010\).](https://doi.org/10.1017/S0022381609990557) [65] D. Blankschtein, Y. Shapir, and A. Aharony, Potts models in random fields, Phys. Rev. B 29[, 1263 \(1984\).](https://doi.org/10.1103/PhysRevB.29.1263) [66] G. C. Jacobson, The effects of campaign spending in congressional elections, [Am. Political Sci. Rev.](https://doi.org/10.2307/1954105) 72, 469–491 [\(1978\).](https://doi.org/10.2307/1954105) [67] G. C. Jacobson, The effects of campaign spending in house elections: New evidence for old arguments, [Am.](http://www.jstor.org/stable/2111450)
129:- <span id="page-6-25"></span><span id="page-6-24"></span><span id="page-6-23"></span><span id="page-6-5"></span><span id="page-6-4"></span><span id="page-6-3"></span><span id="page-6-2"></span><span id="page-6-1"></span><span id="page-6-0"></span>[J. Political Sci.](http://www.jstor.org/stable/2111450) 34, 334 (1990). [68] R. S. Erikson and T. R. Palfrey, Equilibria in campaign spending games: Theory and data, [Am. Political Sci.](https://doi.org/10.2307/2585833) Rev. 94[, 595–609 \(2000\).](https://doi.org/10.2307/2585833) [69] K. E. Schnakenberg and I. R. Turner, Helping friends or influencing foes: Electoral and policy effects of campaign finance contributions, [Am. J. Political Sci.](https://doi.org/https://doi.org/10.1111/ajps.12534) 65, 88 (2021). [70] E. Avis, C. Ferraz, F. Finan, and C. Varj˜ao, Money and politics: The effects of campaign spending limits on political entry and competition, [Am. Econ. J. Appl. Econ.](https://doi.org/10.1257/app.20200296) 14[, 167–99 \(2022\).](https://doi.org/10.1257/app.20200296) [71] X. Lu, J. Gao, and B. K. Szymanski, The evolution of polarization in the legislative branch of government, [J.](https://doi.org/10.1098/rsif.2019.0010)
142:FIG. 4: Emergence of campaign polarization in the US House of Representatives elections. We compare campaign spending and election results for races from 1980–2020, focusing on close contests with p = 0.5 ± 0.05. (a) Phase diagram as in Fig. [2,](#page-3-0) now covering the full range of spending, including the polarized region; the gray area marks races with close spending. (b) Election outcomes near h DEM ≈ h REP , where |h DEM − h REP | < \$100, 000. The x-axis shows average spending <sup>1</sup> 2 (h DEM + h REP ). Below hc, outcomes are mostly decisive, with only 39% close races (|m| < 0.1) and stronger incumbency effects. Above hc, over 70% of outcomes are near 50:50, consistent with RFIM predictions. (c) Percentage of close races where both campaigns exceed hc, i.e., within the polarized region π. This share rises sharply in 2018 and 2020.
146:FIG. 5: Estimation of model parameters for US House of Representatives for Republican-leaning races (p = 0.6 ± 0.05). Similarly to [2](#page-3-0) in the main text, we use the classification model for p = 0.6 to estimate the parameters of the model. (a) Classification model for T = 1 without hysteresis. (b) Classification model for T < 1 with incumbent region. (c) The plot of the election results with the campaign spending, with the incumbent region predicted by the optimal model. (d) The accuracy of the classification model in a range of temperatures; the star denotes the model with the best accuracy, corresponding to T <sup>⋆</sup> = 0.845.
150:FIG. 6: Estimation of model parameters for US House of Representatives for Democrat-leaning races (p = 0.4 ± 0.05). We use the classification model for p = 0.4 to estimate the parameters of the model. (a) Classification model for T = 1 without hysteresis. (b) Classification model for T < 1 with incumbent region. (c) The plot of the election results with the campaign spending, with the incumbent region predicted by the optimal model. (d) The accuracy of the classification model in a range of temperatures; the star denotes the model with the best accuracy, corresponding to T <sup>⋆</sup> = 0.865.
154:### Detailed derivation of the self-consistency equation
160:In order to decouple the Hamiltonian into the Hamiltonian for a single individual, we use the two approximations. The first one is the configuration model approximation, where we assume that the adjacency matrix of a random network can be approximated as Aij ≈ kik<sup>j</sup> N⟨k⟩ , where k<sup>i</sup> is the degree (i.e., connectivity) of the node i and ⟨k⟩ is the average degree. The second approximation we use is the mean-field approximation. Expressing the spin in terms of its average value as s<sup>i</sup> = ⟨si⟩ + δs<sup>i</sup> enables us to omit the term quadratic in fluctuations. By denoting the average magnetization as m = ⟨si⟩, we can rewrite the Hamiltonian as
164:The first term can be omitted from the Hamiltonian, as it is an additive constant of the energy and will be canceled when the equilibrium distribution is calculated. Thus, the mean-field Hamiltonian can be expressed as
190:Let us now focus on the symmetric case, i.e., when p = 1 2 and h <sup>+</sup> = h <sup>−</sup> ≡ h. We investigate how the phase diagram depends on the strength of the field and the temperature. Without loss of generality, we consider that J˜ = 1. To this end, we expand the right-hand side of the self-consistency equation around m = 0 and get
202:Finally, by plugging the critical curve into the self-consistency equation, we can determine the order of the phase transition from the sign of the third-order coefficient. The coefficient is along the critical curve equal to <sup>2</sup>−3<sup>T</sup> <sup>3</sup><sup>T</sup> <sup>2</sup> so the critical point where the phase transition changes its order is
212:and expand the self-consistency equation
220:By denoting ξ <sup>±</sup> = tanh(h <sup>±</sup>/T), one can rewrite the self-consistency equation as
250:#### Alternative derivation of the self-consistency equation from the Weidlich master-equation model
252:In this section, we show that the mean-field description used in the main text can alternatively be obtained from a master-equation approach to opinion dynamics, following the sociodynamics framework introduced by Weidlich and Haag. This demonstrates that the polarization transition does not rely on the Hamiltonian formulation with spatial interactions, but emerges generically from stochastic opinion switching driven by individual preferences and social adaptation.
260:Second, individuals exhibit an adaptive response to the prevailing opinion, whereby the propensity to adopt a given opinion increases with its share of the population, reflecting conformity or social pressure. This mechanism is somewhat similar to the homophily, although it does not necessarily require the assumption on the spatial distribution of interactions. These preference and adaptation tendencies act simultaneously at the individual level and may have independent strengths. The particular choice that is widely used in sociodynamics literature is
288:which is exactly the self-consistency equation from the main text.
309:<span id="page-13-0"></span>The McNemar test is used to demonstrate whether one of the two classification models used on a given data set is better than the other. For each observation, a classification model gives a predicted classification, which is compared with the actual classification. For example, in the election races, the classification model predicts the winner of the election based on the campaign spending and incumbency (see the second above), which is then compared with the actual election result. For two classification models M1,M2, the contingency table between correctly and incorrectly classified observations can be written as shown in Tab. [II.](#page-13-0)
319:# Calibration to US House election data for Republican-leaning races (p = 0.6 ± 0.05)
323:### Comparison of calibration of US House election data for different time periods
327:# Comparison of calibration of US House election data with a support vector machine model
333:<span id="page-14-1"></span>FIG. 7: Comparison of fitted parameters for US House elections in four decades.
347:FIG. 8: Comparison of fitted parameters for US House elections in four decades corresponding to the previous plots, focused on incumbency regions.
[0m
[0m$ [0mls papers_md/godoylorite2020/; grep -n -i "ising\|social temperature\|temperature\|ferro\|spin\|EU Referendum\|London\|monte carlo\|network\|inferred\|infer" papers_md/godoylorite2020/*.md 2>/dev/null | head -40
_page_14_Figure_0.jpeg
_page_15_Figure_0.jpeg
_page_16_Figure_0.jpeg
_page_17_Figure_0.jpeg
_page_18_Figure_3.jpeg
_page_19_Figure_0.jpeg
_page_1_Figure_1.jpeg
_page_20_Diagram_0.jpeg
_page_21_Figure_3.jpeg
_page_2_Figure_1.jpeg
_page_4_Figure_1.jpeg
_page_5_Diagram_1.jpeg
_page_5_Figure_2.jpeg
_page_6_Figure_1.jpeg
_page_8_Figure_1.jpeg
_page_9_Figure_1.jpeg
godoylorite2020.md
godoylorite2020_meta.json
1:### Inference and Influence of Large-Scale Social Networks Using Snapshot Population Behaviour without Network Data
7:*Imperial College London, London SW7 2AZ, United Kingdom*
9:<sup>2</sup>*Centre for Advanced Spatial Analysis. University College London,*
11:*First floor, 90 Tottenham Court Road, London, United Kingdom* <sup>3</sup>*Department of Mathematics, Imperial College London, London SW7 2AZ, UK*
15:Population behaviours, such as voting and vaccination, depend on social networks. Social networks can differ depending on behaviour type and are typically hidden. However, we do often have large-scale behavioural data, albeit only snapshots taken at one timepoint. We present a method that jointly infers large-scale network structure and a networked model of human behaviour using only snapshot population behavioural data. This exploits the simplicity of a few parameter, geometric socio-demographic network model and a spin based model of behaviour. We illustrate, for the EU Referendum and two London Mayoral elections, how the model offers both prediction and the interpretation of our homophilic inclinations. Beyond offering the extraction of behaviour specific network structure from large-scale behavioural datasets, our approach yields a crude calculus linking inequalities and social preferences to behavioural outcomes. We give examples of potential network sensitive policies: how changes to income inequality, a social temperature and homophilic preferences might have reduced polarisation in a recent election.
19:Human behaviour, from voting preferences to vaccine sentiments, can depend on social networks [1]. While we have huge, high-quality, social-scientific datasets linking the behaviour of individuals to their individual circumstances (from censuses through health surveys to voting outcomes) it is extremely costly, or even impossible, to have direct access to the social networks on which this behaviour is articulated. The need to understand social network structure and how it shapes behaviour appears acute: there are concerns about both the role of social networks in health from vaccine refusal to obesity [2–4], and the recurring notion that our societies are becoming excessively polarised [5]. By accessing social-networks and the behavioural dynamics they support, we could also improve our perturbative understanding: clarifying how changes in social inequalities might change health and social polarisation.
21:Given the need for social-network data, it follows that there has been immense scientific excitement about data from large networking platforms from Twitter to Mobile Phones [6, 7]. It is, however, widely acknowledged that technology-platform data has numerous practical issues. A leading concern is whether technology-dependent network datasets give a true indication of the social networks on which society-relevant behaviours, like smoking or voting, depend; it is likely, instead, that different behaviours are spread on different aspects of our social networks [8]. Technology-dependent network datasets are commercially sensitive and so are hard to access and share, are often available for limited time-spans or spatial extents, and, indeed, specific platforms themselves are unlikely to exist indefinitely: this creates concerns for reproducibility and generalizability. The most substantial issue, however, which must limit all such efforts in the future, is the immense privacy implication of large-scale social-network data: social network data is hard to anonymize [9, 10]. An alternative route to using data from technology platforms is to use conventional surveys-surveys though, beyond issues with scalability, it is often a challenge to identify whether the inferred networks are the network on which a particular behaviour is articulated [11–13]. A third established route is to attempt to infer network models through e.g. time-series data [14–17]. These approaches typically assume repeated observations of individual-level data; unfortunately human behaviour, such as voting or smoking, is often sampled at a single point in time.
23:While it might thus seem challenging to access behaviourspecific social network structure there is one distinctive feature of social data which assists network inference: unlike many networked systems, censuses provide socially-relevant coordinate information for individual nodes. Peter Blau postulated an intuitive and powerful theory for social structure such that each individual in a society can be considered as being a point in a high-dimensional space (with dimensions like age, gender and income) where the rates of connection between individuals are driven by homophily and depend on their relative separation in the space [18–20]. This homophily suggests that we can consider individuals to form social network links conditional on their separation in social space: typically modelled by a soft random geometric graph [13, 20, 21]. Beyond information about the coordinates of individuals, large-scale health and voting datasets give us snap-shot information about the behaviour of nodes. There is well developed theory to capture discrete choices [22] which in turn has links to finitetemperature linear threshold models of influence [23, 24] and Ising models [25–27]. This paper exploits a merger between Blau's geometric view of social structure and Ising models of behaviour to infer kernels for soft-geometric random graph models of social networks; we name this a kernel-Blau-Ising (KBI) model.
29:Figure 1. Outline of the kernel-Blau-Ising methodology. Input data consist of: aggregated behavioural data at for different geographical areas and socio-demographic variables (age, income, education, etc.) associated to those areas (from census data). (a) Heatmap of (hypothetical) behavioural data in Greater London, in this case electoral outcomes, where red represents 100% votes to Labour and blue represents 100% votes to Conservatives. (b) Probability distribution of behavioural outcomes in (a). (c) Blau space representation of the behavioural outcomes spanned by socio-demographic characteristics (e.g. age, income). (d) Blau space representation of Kernel-Blau-Ising approach using input data in (1), and learning parameters: the External Fields, which account for the general trends, e.g. older people are more likely to vote Conservatives than younger people; and the Social Network that connects population according to their distances in the Blau space and their homophilic preferences. Once the model parameters are learnt, we can further estimate how changes and interventions affect behavioural outcomes. Examples of potential network-sensitive intervention strategies: how changes to income distribution (e) and homophilic preferences (f) can reduce behavioural polarisation.
31:network. We illustrate this conceptualisation in Fig. 1. It takes as input a set of individuals in a social-space and invokes both a Ising model for behaviour and a simple (soft random geometric graph) model for how distances in a social space affect the chance of connections (friends, confidants, etc.). The simplicity of our model means we can use it to infer network parameter values for simulated data which carries no network information but only a snapshot of system behavioural state and node coordinate information. We illustrate our results for the EU Referendum and two London Mayoral elections, using only census data and voting outcomes, where we infer network parameter values consistent with the literature and we are able to predict missing/suppressed voting data. Finally our model allows us to quantify, model-dependently, the potentially depolarising effects of shifts in social connectivity preferences (e.g. eliminating income or age homophily) and social coordinates (e.g. reducing income inequality).
33:#### II. AN INTERPRETABLE GENERATIVE MODEL FOR BOTH POPULATION BEHAVIOUR AND SOCIAL NETWORKS IN BLAU SPACE
35:We deploy a generative model for population behaviour where the behaviour of individuals is partly determined by their social coordinates (as would be standard in logistic regression from survey data, e.g. regressing vaccine refusal on age and income); and partly determined by the behaviour of their neighbours on a social network as would be standard in socio-physics models [26, 28]. Regarding the social network, we also deploy a generative model for social networks where the chance that individuals have a social connection depends on their proximity in social space. In our model we consider binary social outcomes (for example voting Conservative/Labour or being smoker/non-smoker), but it is possible to extend the model to a discrete set of possible outcomes by using a Potts instead of an Ising model (we will keep to binary outcomes for simplicity). We use an Ising-like model (or Binary Markov Random Field) to model population social outcomes, but instead of locating spins in a regular grid, in our approach spins will be embedded in a multidimensional Blau space (where dimensions are socio-demographic variables and geographical coordinates) and social links between individuals occur with a probability depending on their separation in the Blau space.
37:*Social network model:* We have N individuals each embedded in a K-dimensional Blau space, where vector <sup>z</sup><sup>i</sup> ∈ R K encodes the ith individual's coordinates in the Blau space representing her age, income, residential coordinates, etc. (see Fig. 2A showing random coordinates of nodes in a 2D Blau space). We connect individuals through a soft random geometric graph (SRGG) [29] according to a connectivity kernel function which depends on distances in the Blau space and the kernel parameters (see Fig. 2B for an example of a SRGG). This model makes it easy to simulate realistic networks with clustering [30], although it does not explicitly build in other real social networks properties such as heavy-tailed degree distributions. Nonetheless, it is a well-established model for generating social networks that provides interpretable results [21, 30, 31].
39:We coded connections between spins in an adjacency matrix where Aij = 1 if i and j are connected and 0 otherwise,
43: 0.4 0.2 0.4 0.2 *Behavioural model:* Our Ising model to generate spin configurations is as follows. Each individual i in the population has a spin associated <sup>σ</sup><sup>i</sup> <sup>=</sup> {−1, <sup>1</sup>} encoding her binary social outcome, so that a spin configuration is <sup>σ</sup> ∈ {−1, <sup>1</sup>} N . The spin orientation depends on the external fields (EFs) and the other spins they are connected to in the network. As is common for conventional social statistics (logistic regression with linear dependence on the covariates), we model the EFs as linear fields in each dimension of the Blau space, where the linear coefficient in each dimension of the Blau space k is hk, so that the individual spin interaction with the EFs is the scalar product <sup>h</sup> · <sup>z</sup><sup>i</sup> <sup>=</sup> P k hkzik. The spins interact with the external fields depending only on their coordinates so that they tend to align with the EFs (see Fig. 2C).
45:Figure 2. Generative process for spin configurations balances social/spatial fields and social network effects. Panel (a) shows the coordinates of nodes in a two dimensional Blau space (e.g. x, y is age vs income). In (b) we show a realisation of a Soft Random Geometric Graph (SRGG) from the connectivity kernel parameters θ<sup>x</sup> = θ<sup>y</sup> = 10 (θ<sup>0</sup> = 0). Panel (c) shows a spin configuration for a linear External Field (EFs) in the y-axis and low thermal noise (β = 100), where the spins are aligned with the local EFs. Finally, in (d) we show the spin configuration under the same External Fields as in (c), also with low thermal noise (β = 100), but now the spins are connected according to the SRGG in (b). We see how spins that in (c) aligned with the EFs have now changed their orientation to align more with their neighbours.
51:We choose our connectivity kernel to be a logistic sigmoid function as they have been successfully used for the inference of connectivity kernels on ego networks [13] and in latentspace inference [21, 30, 31].
57:The energy of a spin configuration σ is given by the Hamiltonian function,
61:where h<sup>k</sup> is the EFs linear coefficient in dimension k of the Blau space, J is the connection strength and Aij is the adjacency matrix. We can add an homogeneous field h<sup>0</sup> which is felt by the whole population regardless of their coordinates. However, in the cases we consider in the following it is reasonable to set h<sup>0</sup> to zero. The configuration probability is given by the Boltzmann distribution with inverse temperature <sup>β</sup> = 1/T, β ≥ <sup>0</sup>:
69:is the partition function, where the sum is over all possible spin configurations, Ω, which for and Ising model are 2 N terms. The configuration probabilities <sup>p</sup>(σ|β, <sup>h</sup>, J, A(θ)) represent the probability that, in equilibrium, the system is in a state with configuration σ. Fig. 2D gives an example of a spin-assignment which has been generated conditional on a particular network structure –in our case a SRGG from a particular connectivity kernel. Vitally, the spins of the nodes are not exclusively determined by either the external fields or network structure.
71:### III. INFERENCE METHOD FOR MODEL PARAMETERS
73:Given a record of a social outcome <sup>σ</sup> ∈ {−1, <sup>1</sup>} <sup>N</sup> together with the population Blau space coordinates <sup>z</sup> ∈ R <sup>N</sup>×K, our goal is to find the most plausible model parameters Θ = {β, <sup>h</sup>, J, <sup>θ</sup>}. For the Ising model the partition function <sup>Z</sup> cannot be computed even for small systems, since it requires the computation of 2 <sup>N</sup> terms. A further challenge is that Z itself depends on the model parameters and would need to be recomputed for each possible parameter set. In this case the inference is called doubly-intractable [32] and Markov chain Monte Carlo is challenging.
75:As an alternative likelihood-free method (that nonetheless avoids mean-field approximation) we use approximate Bayesian computation (ABC), which has been applied to a wide spectrum of problems with intractable likelihoods [33, 34]. In Algorithm III we show our rejection-based ABC inference method for the model parameters. We suppose we have priors, π(Θ), on possible parameter values. Importantly, on *lines 4,5* the generation of a spin configuration requires two steps: (i) the generation of a soft random geometric graph (SRGG) from the connectivity kernel Eq.(2) given the node coordinates; (ii) the generation of the spin configuration conditional on the graph generated in (i) and for the parameters of the Hamiltonian in Eq.(3).
79:We use Glauber dynamics to generate spin configurations σ 0 for any combination of the model parameters Θ0 from Boltzmann distribution. Importantly, in order to improve the efficiency of the ABC rejection algorithm, we define a set of lower-dimensional summary statistics. We summarise spins that share the same coordinates z by the fraction of spins down (or up) S<sup>z</sup> = n<sup>z</sup> P <sup>i</sup>|<sup>z</sup>i∈<sup>z</sup> δ(σ<sup>i</sup> , −1), where <sup>n</sup><sup>z</sup> is the number of individual spins at coordinate z of Blau Space. If there are C different Blau space coordinates populated with spins, the summary statistic would be such that <sup>S</sup>(σ) ∈ [0, 1]<sup>C</sup> , with ideally <sup>C</sup> <sup>N</sup>. Therefore, We approximate our posteriors by <sup>p</sup>(σ|(kη(S(<sup>σ</sup> 0 ), S(σ))k < )), where <sup>η</sup>(S(<sup>σ</sup> 0 ), S(σ)) measures the discrepancy between σ 0 and σ after they are summarised with function S(σ 0 ). We define the distance between S(σ) (summary statistics of the original social outcomes data) and S(σ 0 ) (observational data of the spins configuration generated from Θ0 ) as,
83:where |<sup>S</sup><sup>z</sup> − <sup>S</sup> 0 z | is the absolute difference between the fraction of spins down in the observed spin data and the generated spins, so that the distance is zero only if S<sup>z</sup> = S 0 <sup>z</sup> ∀z. The distance η(S 0 , S) can also be considered as a weighted mean absolute error (WMAE). Significantly, our observational data itself will be aggregated in the form of fractions of spin-up nodes in different small spatial regions (e.g. proportions of smokers or voters in different small spatial patches – as in Section IV B). Since we are precisely attempting to simulate our observational data, and given that all spins with the same coordinates are statistically indistinguishable (Eq.3), vitally, S(σ) are sufficient statistics and the ABC posteriors tend to exact Bayesian posteriors in the limit of → <sup>0</sup>. For largescale data applications (as in our voting illustration), population size can be rescaled through rescaling the connectivity kernel bias term θ<sup>0</sup> in Eq.2 (see SM Section S2). Since the ABC approximate posteriors of the model parameters are obtained through independent samples, it is straightforward to parallelise the algorithm so that the samples are obtained concurrently. For a more efficient sampling procedure sequential sampling schemes for ABC can also be used [35].
87:#### A. ABC Inference can estimate model parameters from synthetic data
89:We tested the ability of our ABC inference method to recover the known parameters, of both the network and behavioural processes, for synthetic snapshot data. We note that, in a manner distinct from other inverse-Ising or network inference approaches [36, 37], we are not seeking to recover unique network links, do not observe each node state (only coarsened observations) and we will not use time-series data. As it is reasonable for social data, we suppose that we are given access to information about the social coordinates of nodes/individuals. Our simple, but justified, model structure allows us to extract information from very limited datasets composed of snapshot behavioural data and census information. Given that survey and census demographic-variables are typically ordinal or categorical, we use ordinal data in our experiments with synthetic data. We performed the ABC rejection method for two different combinations of connection strengths at a temperature below the corresponding critical temperature β > β<sup>c</sup> (see Fig. S3). We found that for a given temperature β there is a value of Jaligned where every pair of nodes that are connected are aligned (Jaligned changes for the different β values). Therefore, any J > Jaligned has the same distribution over spin configurations where connected spins are aligned. We test our inference method in two different synthetic data scenarios, one with strong connection strength J<sup>s</sup> > Jaligned, and another with weak connection strength J<sup>w</sup> < Jaligned.
91:In Fig. 3 we show the ABC posteriors for the different scenarios, with J = 5 (weak) and J = 25 (strong). Importantly, we have set two model parameters in the inference: the x axis external field h<sup>x</sup> (h<sup>x</sup> = 1) and the connectivity bias term θ0. Regarding hx, from Eq.4 we see that the inverse temperature parameter β multiplies the linear external fields h, thus there is one degree of freedom that we choose to reduce by setting h<sup>x</sup> = 1 without violating any constraint. Regarding the connectivity bias term θ<sup>0</sup> in Eq.2, there is a coupling between the connection strength J and the bias term θ<sup>0</sup> in the Hamiltonian Eq. 3. This implies that, in some regimes, the same spin configurations can be generated by different combinations of these two factors, i.e, a spin configuration could be a result of a certain combination of low connectivity density (large θ0)
95:Figure 3. Inference allows the recovery of model parameters for synthetic snapshot data. On the top left, synthetic data with a weak connectivity strength spin configuration (J=5), and on the bottom right a strong connectivity strength spin configuration (J=25); both for β = 0.3 (see Fig. S3) and kernel parameters θ<sup>0</sup> = 9, θ<sup>x</sup> = 2 and θ<sup>y</sup> = 0.5. There are a total of N = 10, 000 spins, with 100 spins on each of the discrete coordinates on the grid where x, y <sup>=</sup> {0, <sup>1</sup>, .., <sup>9</sup>} (for visualisation purposes links are aggregated at the coordinate level). To avoid coupling between certain model parameters we choose to set h<sup>x</sup> = 1 and θ<sup>0</sup> = 9 for the ABC inference (see main text). We use uniform priors for <sup>β</sup> ∈ [0, 2], <sup>h</sup><sup>y</sup> ∈ [−1.5, <sup>0</sup>.5], <sup>θ</sup><sup>x</sup> ∈ [−0.5, <sup>4</sup>.5], <sup>θ</sup><sup>y</sup> ∈ [−2.5, <sup>2</sup>.5], and <sup>J</sup> ∈ [0, 10] in the <sup>J</sup> = 5 scenario and <sup>J</sup> ∈ [0, 40] in the <sup>J</sup> = 25 scenario. We show the ABC marginal posterior distributions for 500 samples with the lowest distance η(S 0 , S) in Eq.6. The samples are visualised using histograms in grey and Gaussian kernel density estimates as solid lines, and the vertical lines correspond to the real values used to generate the synthetic spin configuration. On the right, for J = 25, it shows that the ABC inference is not able to distinguish between configurations above a given values of J > Jaligned since all spins that are connected are already aligned. The ABC inference algorithm accurately estimate the connectivity kernel parameters without using network data for synthetic systems.
97:and strong connection strength J and vice-versa, high connectivity density (small θ0) and weak connection strength —-this trade-off does not hold when the link density is very low, with almost no links, or when it is very high, such that it become almost a complete network, see SM Fig S2. Therefore, we set the connectivity bias term θ<sup>0</sup> = 9 in the inference (such that the average degree is <sup>κ</sup> ∼ <sup>2</sup>, a parameter choice discussed in the next section). For the ABC inference in Fig. 3, we show the ABC marginal posteriors for the best 500 samples according to the datasets distance η(S 0 , S) Eq.6. The distances corresponding to the spins configuration in Fig. 3 are = 0.036, which can be also be seen as a weighed mean absolute percent error (WMAPE) lower than 3.6%. Results show that all inferred parameters are consistent with the original values both for weak and strong connection scenarios. As expected, the posterior of the connection strength for J = 25 accepts all values for J > Jaligned. Considering the connectivity kernel parameters, we show we can recover posteriors consistent with θ<sup>x</sup> and θ<sup>y</sup> from one single observation of a spin configuration without using network data.
99:#### B. Inferred parameters for Mayoral Elections and EU Referendum are consonant with homophilic tendencies and voting preferences.
101:To demonstrate our model and inference approach beyond synthetic data, we apply it to three electoral datasets in Greater London: 2012 London Mayoral Election, 2016 London Mayoral Election and EU (Brexit) Referendum in 2016. Our kernel-Blau-Ising model allows us to compare the different electoral outcomes using readily interpretable parameters, to visualise and compare the social connectivity structures and to further estimate interventions. We stress that our objective is illustrative and note, of course, that much more refined social models, e.g. allowing connections between the external fields, could be deployed.
103:The electoral results are given as aggregated outcomes, where we know the total outcome for a specific area but we do not know the votes of individuals. The smallest areas in spatial resolution that we can get for electoral outcomes are the electoral wards – 630 electoral wards in Greater London from which, due to data mismatches, we can only use 608 wards outcomes; for the EU referendum ward level data is missing for 18 Boroughs, so we use a combination of 280 ward level outcomes and 18 Borough electoral outcomes data (see SM Section S1). While census microdata is available at the wardlevel, we define the Blau space coordinates of each electoral ward as the average value from census data in each Blau space dimension, which are: education, age, gender, wards centroid spatial coordinates and income (see SM Section S1 for details). This coarsening overestimates proximity within wards (and could conceal heterogeneities) –favouring more homogeneous behaviour– however we note that although we lose information about individuals' connectivity by using aggregated data instead of individual's micro-data coordinates, we see that average coordinates at the ward level are heterogeneous (in SM Fig. S4 we show evidence of heterogeneous distribution of average wards' coordinates by bootstrapping census micro-data for each ward). We finally note that census data is from 2011, and London is a fast changing city, nonetheless we consider this 1-5 year gap adequate for our illustrative aim.
105:We now define distances in the Blau space and how we can return reasonable posteriors for real data. We define distance between two wards in the Blau space (Eq. 2) as the absolute difference of their coordinate values for education, age, gender and income dimensions, and as the distance between centroid coordinates for the spatial distance (see SM Section S1). Before passing the distances to the inference algorithm, we standardise them by subtracting the mean distance and then dividing by twice their standard deviation for each Blau di-
111:Figure 4. ABC marginal posteriors for London Mayoral Elections 2012 and 2016 and EU (Brexit) Referendum are consistent with known homophilic and political preferences. We show ABC marginal posteriors for London Mayoral Elections 2012 and 2016 for 608 electoral wards (See ABC marginal posteriors for Mayoral Elections 2012 and 2016 for 280 electoral wards and 18 Boroughs Fig. S7). We show estimates for parameters: inverse temperature β in red, the connectivity strength J in yellow, the external field for age, gender and income, <sup>h</sup>i; <sup>i</sup> <sup>=</sup> {age, gender, income}, and the connectivity kernel parameters <sup>θ</sup>i; <sup>i</sup> <sup>=</sup> {education, age, gender, distance, income}. <sup>h</sup>education and <sup>θ</sup><sup>0</sup> as fixed (see main text). We use uniform priors for <sup>β</sup> ∈ [0, 4], <sup>J</sup> ∈ [0, 4], <sup>h</sup>age ∈ [−3, <sup>0</sup>.15], <sup>h</sup>gender ∈ [−0.3, 3], <sup>h</sup>income ∈ [−1.6, <sup>0</sup>.7], <sup>θ</sup>education ∈ [−7, 12], <sup>θ</sup>age ∈ [−5, 12], <sup>θ</sup>gender ∈ [−6, 12], <sup>θ</sup>distance ∈ [−7, 11] and <sup>θ</sup>income ∈ [−5, 12]. The ABC marginal posterior distributions are shown for 500 samples with the lowest distance η(S 0 , S) (Eq.6). We show the histograms of the ABC marginal posteriors in grey, as a solid line the Gaussian kernel density estimates, and the vertical lines correspond to 0 value. The parameter estimates show that the connectivity kernel parameters of the two Mayoral Elections are similar but considerably different from EU Referendum connectivity kernel. Unlike the Mayoral Elections, the EU referendum does not show homophilic signal for age, gender and income but only for distance and education, even though the EU referendum took place a month after Mayoral Election 2016.
113:mension [38]. The standardisation allows us to compare homophily kernel parameters among them and makes interpretation easier. Finally, for the ABC rejection algorithm we simulate a representative sample of spins in each electoral ward instead of simulating the whole population. Specifically, we keep the relative size of the wards population according to the census data (from a population of <sup>N</sup> ∼ <sup>8</sup>, <sup>800</sup>, <sup>000</sup> individuals in Greater London we rescale the system to N = 60, 683 with a average of 100 spins per ward). The population rescaling inevitably affects the bias term θ<sup>0</sup> in Eq.2 but for sufficiently large samples can provide an adequate approximation for the homophily kernel parameters (see SM Section S2). Given the coupling between the connection strength J and the connectivity bias term θ0, we set θ<sup>0</sup> = 14 – which corresponds to a social network with an average degree of <sup>κ</sup> ≈ <sup>2</sup>, comparable with real data on the estimated number of ego-confidants [39], see also Fig. S2 where we show evidence of insensitivity of dimension-specific kernel parameters to changes in the degree of the network. As per the synthetic data, we fixed one of the external fields hedu to remove the degree of freedom in the Hamiltonian (Eq. 4) between the inverse temperature and the External Fields. We choose to set hedu = 0.45 based on the results for a simple multilinear regression (see SM Section S5), where we find that the education linear coefficient has the least variability when comparing values among the three election. In Fig. 4 we show the ABC marginal posteriors for 500 samples with the lowest data distances η(S 0S), with distances (or WMAE) η(S 0 , S) < 0.088 for 2012 and 2016 Mayoral Elections and η(S 0 , S) < 0.050 for the EU Referendum. The EU Referendum ward outcome distribution is less polarised than the MEs outcome distribution (see SM Section S8), and less polarised outcomes are better captured by linear External Fields (see SM Section S6 for the inference only with EFs), hence, overall KBI performance is better for the EU referendum than for MEs.
115:Figure 4 shows that the marginal posteriors for the two London Mayoral Elections are qualitatively similar (except possibly the level of noise, indicated by β) with the Conservative party winning the 2012 MEs while the Labour party won the 2016 MEs (see Fig. S8 for the detailed distribution of outcomes for the three elections). However, the EU Referendum ABC marginal posteriors present some differences. In terms of the parameters of the model, the temperatures are sub-critical for the the three elections, meaning that spins are in the ordered phase (see in SM Fig. S3). Regarding the connection strength J, for the three elections the value of J is large enough that all spins connected are aligned and the inference can not distinguish J values larger than Jaligned as
119:Figure 5. KBI accurately reproduces electoral outcomes while inferred connectivity networks highlight differences between Mayoral Elections and EU referendum. The *left* column show the real electoral outcomes and next to it the *middle* column show inferred outcomes generated from the ABC posteriors with lowest data distance, for the three election in Greater London. For London Mayoral elections, the colour range goes from red for S<sup>w</sup> = 1 ward's fraction of Labour vote, and blue for S<sup>w</sup> = 0 or all ward's votes for Conservatives. For EU Referendum, in order to keep colour consistency, we represent in red Sw/B = 1 fraction of ward/Borough votes for remain, and blue Sw/B = 0 for wards/Boroughs voting for leave. On the *right* column, we show the connectivity networks from Fig. 4 ABC marginal posteriors of the kernel parameters aggregated at the Borough level for visualisation purposes (ward level social networks with 184, 528 links are hard to visualise). The colour map in the background is the real electoral outcomes at the Borough level. For the connectivity kernel we coloured in a linear range (white to black) the strength of the nodes and the weight of the links, also the size of nodes and links is linear with their strength and weight respectively. We have not visualised intra-Borough links but we have take them into account for the nodes strengths. We see that MEs connectivity networks are similar among them but different from the EU Referendum connectivity network. All the networks show pronounced spatial homophily leading to strong links between neighbouring Boroughs.
121:in the strong connection scenario in Fig. 3 (our choice of θ<sup>0</sup> is partly determining our inferred J). For the EFs, the three elections show the same sign for the linear coefficients in the different dimensions, with the difference that EU referendum EFs are closer to zero than for the two MEs. Notice that heducation is set to 0.45 so that more educated people tend to vote Labour/Remain (see SM Section S5). The observed EFs are in agreement with traditional two-party partisan voting socio-demographic tendencies in the UK: hage is negative, meaning that older voters prefer Conservative/leave, hgender is positive, meaning that men vote more Conservative/leave than women, and hincome is negative meaning that the richer the more Conservative they vote; although for the EU referendum income EF is peaked around zero.
123:Regarding the connectivity kernel parameters, the resulting connectivity kernels are non-negative for the three electoral datasets, which is in agreement with the homophilous tendency of social relations [19, 40, 41]. Importantly, the connectivity kernel parameters for the two MEs are similar, but differ from EU referendum kernel parameters. Regarding the similarities, distance homophily is persistently the strongest homophily signal in the three electoral outcomes, consistent with other work [13, 20]. Apart from spatial distance homophily, MEs' kernels show positive signal (homophily) for age and income dimensions; while for the EU Referendum age and income ABC marginal posteriors are peaked around zero, but the education kernel parameter shows a positive signal that is not present in the MEs' kernels. Notably the 2016 Mayoral Election was held on the 5 th of May 2016, only 49 days before the EU Referendum on the 23rd of June. Therefore, the changes in the social kernels we infer, if true, are not due to temporary evolution of the social connectivity structure, but rather indicate that different social ties were at play for the EU Referendum compared to Mayoral Elections.
[0m
[0m✱ [0mGrep "weakly significant|weakly confirm|significant in its own"[90m 0 matches[0m
Let me search for a few specific phrases to pin down exact quotes and check consistency.
[0m✱ [0mGrep "0.0005|p=0.0005|999|low-\$T\$ tail|low-temperature tail"[90m 0 matches[0m
[0m
[0m$ [0mgrep -n "weakly significant\|0.0005\|999\|low-\$T\$ tail" manuscript/main.tex
46:$+13.4$ points, $p=0.0005$ for 2026, though not significant for 2022 or at
457:of the low-$T$ tail the wider grid samples.
507:\citep{moran1950}, using a 999-permutation test for significance.
530:999 Monte Carlo sign-flip draws (matching the Moran's $I$ test's
531:999-permutation budget above), not exact enumeration even where the block
533:$\sqrt{p(1-p)/999} \approx 0.005$--$0.015$ over the range of $p$ values
1059:percentage points; at the extension's low-$T$ tail ($\lambda_{pol}=8$,
1201:$p=0.0005$, significant in 15 of 16 seed-pairs -- the most decisive result of
1403:($p=0.0005$, Section~\ref{sec:gam}) but not at canton level here, the same
1588:$p=0.0005$) has enough headroom that this plausibly does not threaten it: the
1667:percentage points at distrito resolution with direct paired $p=0.0005$
[0m
[0m→ [0mRead manuscript/main.tex[90m [offset=862, limit=30][0m
[0m→ [0mRead manuscript/main.tex[90m [limit=28, offset=443][0m
[0m
[0m$ [0mls scripts/ | grep -i "gam\|paired\|mideplan\|3d_scan"; echo ---; grep -rn "N_PERMUTATIONS\|n_permutations\|1999\|n_perm" scripts/run_gam_field.py scripts/run_3d_scan.py scripts/run_3d_scan_2022.py 2>/dev/null
analyze_3d_scan.py
parse_mideplan_ids.py
run_3d_scan.py
run_3d_scan_2022.py
run_axis_paired_test.py
run_direct_paired_test.py
run_gam_cascade_analysis.py
run_gam_counterfactual_sweep.py
run_gam_domain_wall_analysis.py
run_gam_field.py
run_gam_polarization_trend.py
run_gam_susceptibility_scan.py
run_mideplan_axis_screen.py
run_soc_paired_test.py
submit_3d_scan.slurm
submit_3d_scan_polext_2026.slurm
submit_gam_counterfactual_sweep.slurm
submit_gam_field.slurm
submit_gam_susceptibility_scan.slurm
submit_mideplan_axis_screen.slurm
---
[0m
[0m$ [0mgrep -n "paired_test\|N_PERMUTATIONS\|median_p\|0.0005\|spatial" scripts/run_gam_susceptibility_scan.py scripts/run_soc_paired_test.py scripts/run_axis_paired_test.py 2>/dev/null | head -30
scripts/run_soc_paired_test.py:6:run_direct_paired_test.py; reuses its spatial_block_permutation_test_paired
scripts/run_soc_paired_test.py:26:from isingcr.simulation.observables import spatial_block_permutation_test_paired
scripts/run_soc_paired_test.py:27:from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks, paired_test
scripts/run_soc_paired_test.py:40:    return paired_test(label, spins_a, spins_b, empirical, blocks, N_SEEDS)
scripts/run_soc_paired_test.py:50:    out = Path(__file__).resolve().parent.parent / "data" / "processed" / "soc_paired_test.npz"
scripts/run_soc_paired_test.py:52:             p2026_ps=r2026["ps"], p2026_median_p=r2026["median_p"], p2026_frac_sig=r2026["frac_sig"],
scripts/run_soc_paired_test.py:53:             p2022_ps=r2022["ps"], p2022_median_p=r2022["median_p"], p2022_frac_sig=r2022["frac_sig"])
scripts/run_axis_paired_test.py:5:rationale and machinery as run_soc_paired_test.py (which did this for the
scripts/run_axis_paired_test.py:37:from run_direct_paired_test import best_t_final_spins_aligned, canton_blocks, paired_test
scripts/run_axis_paired_test.py:78:        result = paired_test(label, spins_a, spins_b, empirical, blocks, N_SEEDS)
scripts/run_axis_paired_test.py:79:        sig_bonf = result["median_p"] < BONFERRONI_ALPHA
scripts/run_axis_paired_test.py:93:            flag = "***" if r["sig_bonferroni"] else ("*" if r["median_p"] < 0.05 else "")
scripts/run_axis_paired_test.py:95:                  f"median_p={r['median_p']:.4f}  sig_pairs={int(round(r['frac_sig'] * N_SEEDS))}/{N_SEEDS}  {flag}")
scripts/run_axis_paired_test.py:97:    out = RESULTS_DIR / "axis_paired_test.npz"
[0m
[0m$ [0mgrep -n "paired\|permut\|999\|median" scripts/run_gam_susceptibility_scan.py | head; echo ===; grep -rn "0.0005" scripts/ | head
===
[0m
[0m$ [0mgrep -n "def \|paired_test\|spatial_block" scripts/run_gam_susceptibility_scan.py | head -20; echo ===; grep -rn "0.0005\|0.001" scripts/run_gam_field.py scripts/run_soc_paired_test.py 2>/dev/null | head
51:def run_scan(J, h, empirical, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs):
65:def estimate_resources(n_temperatures, n_seeds, n_equil, n_sweeps):
75:def main():
===
[0m
[0m→ [0mRead manuscript/main.tex[90m [limit=45, offset=1180][0m
[0m→ [0mRead manuscript/main.tex[90m [limit=22, offset=1065][0m
I've read the full manuscript (`manuscript/main.tex`, 1709 lines), the bibliography, the novelty check, the actual simulation code (`src/isingcr/simulation/observables.py`, `src/isingcr/ingestion/shapefile_adjacency.py`, the `run_*` scripts), and resolved the questionable DOIs. Here is the review.

---

## 1. Methods / reproducibility

**severity: MAJOR**
**location:** §3.4 (Observables) vs. §4.9 (GAM), also Abstract and Conclusion
**quote:** "Every spatial-block $p$-value below is estimated from 999 Monte Carlo sign-flip draws (matching the Moran's $I$ test's 999-permutation budget above), not exact enumeration even where the block count would make that feasible" and "The direct paired test against geography-only gives median $p=0.0005$, significant in 15 of 16 seed-pairs"
**problem:** The implemented/described test computes `p = mean(|null_stat| >= |observed|)` over 999 sign-flip draws, so attainable p-values are multiples of 1/999 ≈ 0.001 (or exactly 0); a median of 0.0005 cannot be produced by the stated procedure, yet it is the paper's headline second-contribution number, repeated in the Abstract and Conclusion.
**fix:** State the true permutation budget for that specific test (≥1999 draws) or report the value as p ≈ 0.001 / p < 0.001, consistent with the method as described.

**severity: MAJOR**
**location:** §4.6 (distrito-level ablation), first paragraph
**quote:** "the geography-only model achieves $66.2\% \pm 6.4\%$ best-fit alignment -- statistically indistinguishable from, and nominally \emph{below}, the baseline, and weakly significant in its own right (McNemar median $p=0.180$, only 4 of 16 seeds individually significant)"
**problem:** Median p = 0.180 with 4/16 seeds significant is not significant by any threshold, so "weakly significant in its own right" is false — and it directly contradicts the same sentence's claim that the model is "statistically indistinguishable from" that same baseline.
**fix:** Reword to "nominally below the baseline and not significant against it (McNemar median p=0.180; 4/16 seeds)".

**severity: MAJOR**
**location:** §3.2 (Formal definition); §2.2 (Geographic adjacency network)
**quote:** "where $J_{ij} > 0$ is the coupling between geographically adjacent units $i$ and $j$ (set by shared border length; zero for non-adjacent pairs)"
**problem:** The manuscript never states the normalization of the border-length weights — the code divides each shared border length by the mean over edges (mean weight 1.0) — so the coupling matrix, the temperature scale, and the "1.13 energy units per canton" are not reproducible from the text; raw meter lengths would shift every best-fit $T$ by orders of magnitude.
**fix:** State the normalization explicitly (e.g., "$J_{ij}=l_{ij}/\bar l$, shared border length normalized to mean weight 1.0") and give the resulting scale of $J$ relative to $h$.

**severity: MAJOR**
**location:** §4.9 (GAM) vs. §4.7 (MIDEPLAN); Abstract
**quote:** "by a wide margin, the strongest field tested in this paper beyond the own-margin field itself, for 2026" alongside "scanning $\lambda_{soc} \in [0,2]$" (peak at λ=1.5) and "this field in the $h^{soc}$ slot at $\lambda_{soc}=1$ ($h_i=+1$ if GAM else $-1$)"
**problem:** MIDEPLAN's +6.78pp is quoted at its λ-optimized peak while GAM is evaluated at a single arbitrary λ=1 with no λ-scan, so the "GAM is strongest" ranking is confounded by weighting policy (and by each field's intrinsic scale), not a controlled head-to-head.
**fix:** Scan λ for every candidate field (or justify a single common weighting) and compare each field's peak gain with its uncertainty.

**severity: MAJOR**
**location:** §4.9 (GAM); Abstract
**quote:** "testing three non-circular candidates against real distrito-level 2026/2022 data" and "the most decisive result of any field tested in this paper, including the own-margin field"
**problem:** GAM was selected as the strongest of three tested fields (and the political field itself was pre-selected as the better of two candidate sources), yet p=0.0005 is reported with no correction for field selection, and the best-of-32-T grid selection is also uncorrected in that number — classic winner's-curse multiple testing.
**fix:** Apply a selection-aware correction (best-of-fields max-statistic null, or a Bonferroni factor equal to the number of candidate fields and grid points), or explicitly flag the value as a post-selection maximum.

**severity: MAJOR**
**location:** §3.3 (Monte Carlo dynamics) vs. §§4.7–4.12
**quote:** "We report a simple, conservative Bonferroni correction alongside every raw $p$-value below (raw $p$ times the number of grid points scanned, 24 or 32 depending on the analysis, capped at 1)" vs. "rises to a peak of 74.42\% at $\lambda_{soc}=1.5$ ($+6.78$ percentage points, McNemar $p=0.015$)"
**problem:** The stated "alongside every raw p-value" convention is not honored in the MIDEPLAN/GAM/axes/polarization sections: MIDEPLAN's headline p=0.015 becomes 0.48 after the stated ×32 correction (not significant) and is presented without it, and the axes table's Bonferroni α=0.01 (×5) is inconsistent with the ×32 T-grid correction applied elsewhere.
**fix:** Apply the stated correction uniformly (including ×32 on top of ×5 for the axes) and report corrected values wherever raw p-values appear.

**severity: MINOR**
**location:** §3.3 (Monte Carlo dynamics), grid paragraph
**quote:** "differing only in how much of the low-$T$ tail the wider grid samples."
**problem:** The "wider grid" is [0.05, 5.0] vs. [0.05, 3.5]; both share the same low-T endpoint, so the difference is the high-T upper bound (and sampling density), not the low-T tail — the sentence's explanation is backwards.
**fix:** Reword to "differing only in how far the wider grid extends into the high-T range (and in low-T sampling density)".

**severity: MINOR**
**location:** References (cascantematamoros2006)
**quote:** "year = {2006}" for the entry with DOI "10.35242/rde_2019_28_11"
**problem:** The DOI suffix (2019), issue number (28), and the article's own title range "(1953-2016)" all indicate a ~2019 publication, so the year field is unreliable for locating the source.
**fix:** Verify against RDE issue 28 and correct year/volume/issue.

**severity: MINOR**
**location:** "Data and code availability"; §§2.1–2.3
**quote:** "Official electoral results are publicly available from the Tribunal Supremo de Elecciones de Costa Rica; canton and distrito boundary geometry are publicly available from UN OCHA's Humanitarian Data Exchange."
**problem:** No download URLs, release versions, or access dates are given for the TSE escrutinio ZIPs, the HDX COD-AB release, or the MIDEPLAN IDS 2023 tables, and the two Costa Rican news sources underpinning the chavismo field are cited inline with no bibliography entries.
**fix:** Add full provenance (URLs, versions, access dates) and bibliography entries for the two news reports.

## 2. Novelty vs. prior art

**severity: MAJOR**
**location:** Introduction, first paragraph
**quote:** "What is comparatively rare -- absent from all of the above -- is a model whose coupling network is not an assumption -- a lattice, a mean-field all-to-all approximation, or a configuration model -- but the literal geographic adjacency structure of a real country, fit against that country's own official results and simulated rather than solved analytically"
**problem:** Godoy-Lorite & Jones (arXiv:2003.07146, 2020) fit a Blau-space Ising model with Glauber dynamics and external fields to official UK election outcomes (EU Referendum, London Mayoral), explicitly invoke "social temperature," and decompose network vs. external-field influence — the very decomposition claimed "absent from all of the above" — and the paper's own NOVELTY_CHECK.md flags it as referee-visible.
**fix:** Cite and explicitly differentiate against Godoy-Lorite & Jones (inferred Blau-space network vs. literal geographic adjacency), and narrow "absent from all of the above" to the literal-adjacency corner actually defended.

**severity: MAJOR**
**location:** Discussion / Conclusion
**quote:** "suggesting that spatial resolution is worth checking explicitly, rather than assumed immaterial, in sociophysical election models more broadly, a question this single case study cannot itself settle."
**problem:** The paper's central lesson — the geography-vs-predisposition decomposition reverses under aggregation — is a textbook modifiable-areal-unit/ecological-inference effect, extensively documented in political geography (e.g., Russo & Beauguitte 2014, which the project's own novelty check identified as a positioning reference), and omitting it overstates the general novelty of the scale-dependence finding.
**fix:** Cite the aggregation-level/MAUP literature and reposition the novelty: scale-sensitivity is expected from political geography; the contribution is the physics framing and the real-network implementation.

**severity: MINOR**
**location:** §4.6 (distrito ablation) and Introduction
**quote:** "Costa Rica's own political-science literature has documented real geographic heterogeneity in party support at exactly this finer scale"
**problem:** All three cited works are canton-level studies ("mirada cantonal", "en los cantones"), so they do not document heterogeneity at the distrito scale claimed here.
**fix:** Either cite distrito-level evidence or rephrase to "at finer granularity than the national level".

## 3. Results / figures internal consistency

**severity: MAJOR**
**location:** Abstract and Conclusion vs. §5 (Limitations)
**quote:** Abstract: "though two flagship cases cannot be fully separated from a GAM-proxy labeling artifact" vs. Limitations: "and the cascade test's single largest propagating case (Section~\ref{sec:cascade}, Orosi, in another such canton)"
**problem:** The Abstract and Conclusion say two flagship cases are artifact-exposed, but the Limitations explicitly names three (the two multistability flagships Tabarcia/Monterrey plus the cascade flagship Orosi), so the summary undercounts the exposure.
**fix:** Say "three flagship cases" or explicitly separate the two multistability flagships from Orosi in the Abstract/Conclusion.

**severity: MINOR**
**location:** Figure 4 (historical maps) caption
**quote:** "Gray cantons have no matching result row for that election (see Section~\ref{sec:data}) and are excluded from that election's $N$ in Table~\ref{tab:historical}."
**problem:** Section 2 nowhere explains why 3 cantons (2018, N=81) and 2 cantons (2022, N=82) are missing result rows; the caption points to a section that does not contain the explanation.
**fix:** Add a sentence to §2.1 accounting for the missing canton rows.

**severity: MINOR**
**location:** Table 4.9 vs. §§4.7/4.9
**quote:** Table 4.9: "A: geography only ($h=0$) & $66.2\% \pm 6.4\%$ & 2.83" vs. §4.7: "best-fit temperature drifts sharply downward (from $T=2.605$ to $T=0.369$)"
**problem:** The text reconciles the 66.2% vs. 67.64% best-alignment difference between the two grids but not the parallel best-T difference (2.83 vs. 2.605) for the identical geography-only quantity.
**fix:** Note explicitly that best-T is grid-dependent too, or report both from a single grid.

**severity: MINOR**
**location:** §4.9 (GAM)
**quote:** "2022 does not replicate this: 67.16\% at the same $T$ (a $+4.7$pp gain over its 62.46\% baseline), paired median $p=0.239$, only 4 of 16 seed-pairs significant"
**problem:** The 2026 result is quoted at 2026's best-T (T=1.008) while the 2022 comparison is evaluated at that same fixed T rather than 2022's own best-T, making the across-year significance comparison asymmetric.
**fix:** Report 2022 at its own best-T (as the canton-level polarization table does) or justify the fixed-T choice.

**severity: MINOR**
**location:** §4.9 (GAM) vs. §4.7 (MIDEPLAN, ceiling argument)
**quote:** "a stronger, better-aligned field lets the fitted system settle at lower effective noise" and "the field's own 99.8\% sign-agreement ceiling"
**problem:** From the paper's own figures (31.7% of GAM and 88.7% of periphery distritos on the leading side), the GAM field's sign-agreement with the 2026 label is ~67%, no better than the geography-only baseline — yet it yields +13.4pp and is described as "better-aligned," while the ceiling logic applied to the own-margin field is never applied to GAM.
**fix:** Compute and report GAM's sign-agreement ceiling and explain why a spatially coherent field can exceed it (network-mediated organization) rather than implying field-dominance.

## 4. Journal fit / clarity

**severity: MINOR**
**location:** Abstract, final sentence
**quote:** "Four diagnostics converge on a robustly determined equilibrium, uncertainty confined to a small set of fault-line distritos, though two flagship cases cannot be fully separated from a GAM-proxy labeling artifact."
**problem:** The domain-wall diagnostic is later conceded to be "corroborative rather than exclusive," and the fault-line flagship cases are partly artifact-contaminated, so "four ... converge" overstates the independence and weight of the evidence.
**fix:** Soften to "three dynamical diagnostics, with a corroborative boundary analysis, converge..." or equivalent.

**severity: MINOR**
**location:** Throughout (esp. §4.6, Discussion)
**quote:** "The answer looks like yes: $+8.7$ to $+11.6$ percentage points, consistently, across a resolution-matched subsample and an entirely different binarization. Is the effect formally \emph{confirmed} at conventional significance, independent of which reasonable methodological choice is made? The answer is no:"
**problem:** The manuscript is long and nearly every claim is delivered as a self-interrogating yes/no pair; the density of hedging makes it read like a working report, and the two defensible positives (the scale-dependence reversal and the GAM field) are diluted by exhaustive caveats that would fit better in a supplement.
**fix:** Tighten the presentation, move exhaustive robustness exposition to supplementary material, and give the headline results one consistent, pre-declared significance treatment.

---

**Overall assessment:** This is an unusually honest and methodologically self-aware manuscript: the best-of-grid selection, the single-seed pooling failure history, the low-T χ/C artifact, the McNemar independence violation, the spatial-block-granularity instability, and the GAM-proxy caveats are all disclosed with exceptional candor, and the multi-election, multi-resolution real-network design is a genuine and defensible niche for Physica A's sociophysics program. The abstract/body/tables/conclusion numbers are, impressively, mutually consistent (I could not find a single arithmetic mismatch across the four headline findings). However, the review surfaces one significant prior-art omission (Godoy-Lorite & Jones 2020, which the project's own novelty file flags as referee-visible), a headline p-value (0.0005) that cannot be produced by the stated 999-draw method, a direct statistical self-contradiction ("weakly significant" with median p=0.180), an uncorrected winner's-curse problem on the central GAM claim, an unequal-λ confound in the "strongest field" ranking, and an unstated coupling normalization that breaks textual reproducibility. None of these appear fatal to the underlying science, but several touch the paper's two headline claims and all are fixable with reporting and a re-run or two.

**Recommendation: major revisions.**
