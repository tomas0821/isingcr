#!/usr/bin/env python3
"""Four topological checks against the GAM domain-wall per-node error rate
(data/processed/gam_domain_wall_analysis_2026.csv), all using only J_ij (no
vote data) as the predictor: does a node's position in the real geographic
coupling network -- not just its GAM-boundary status -- independently
predict where the fitted model is unreliable?

Reuses the exact N=488 electoral distrito network (build_distrito_graph_and_fields,
run_3d_scan.py) that produced the per-node error rates in the first place, so
predictor and outcome are computed on the identical node set.

1. Near-tripoint: does touching at least one edge with J_ij<0.1 raise error
   rate? Binary comparison (Mann-Whitney U) plus, for robustness, a Spearman
   correlation against the continuous minimum-incident-edge-weight.
2. Total coupling strength: does a node's summed J_ij over all neighbors
   (weighted degree) predict error rate? Spearman correlation.
3. Betweenness centrality: does a node's position on the most shortest
   weighted paths (distance = 1/J_ij, so strong coupling = short path)
   predict error rate? Spearman correlation, overall and within the
   interior (non-GAM-boundary) subset.
4. Community-boundary: does sitting adjacent to a distrito in a different
   Louvain-detected community (seed=42, resolution=1.0, same as
   plot_community_detection_distrito.py) predict error rate, independent
   of GAM-boundary status?

A Bonferroni correction (raw p times 4, capped at 1) is applied across
these four checks against the single per-node error-rate outcome.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats

from run_3d_scan import build_distrito_graph_and_fields

RESULTS_DIR = ROOT / "data" / "processed"
N_TESTS = 4


def bonferroni(p):
    return min(1.0, p * N_TESTS)


def main():
    J, h_pol, h_soc, nodes, empirical = build_distrito_graph_and_fields()
    node_idx = {n: i for i, n in enumerate(nodes)}
    N = len(nodes)

    df = pd.read_csv(RESULTS_DIR / "gam_domain_wall_analysis_2026.csv")
    df["idx"] = df["node"].map(node_idx)
    missing = df["idx"].isna().sum()
    if missing:
        print(f"WARNING: {missing} nodes in the domain-wall CSV not found in the model network")
    df = df.dropna(subset=["idx"])
    df["idx"] = df["idx"].astype(int)

    J_csr = J.tocsr()
    weighted_degree = np.array(J_csr.sum(axis=1)).flatten()
    min_incident_edge = np.full(N, np.nan)
    for i in range(N):
        start, end = J_csr.indptr[i], J_csr.indptr[i + 1]
        if end > start:
            min_incident_edge[i] = J_csr.data[start:end].min()

    df["weighted_degree"] = df["idx"].map(lambda i: weighted_degree[i])
    df["min_incident_edge"] = df["idx"].map(lambda i: min_incident_edge[i])
    df["has_weak_edge"] = df["min_incident_edge"] < 0.1

    # --- Check 1: near-tripoint ---
    a = df[df["has_weak_edge"]]["error_rate"]
    b = df[~df["has_weak_edge"]]["error_rate"]
    u, p_mw = stats.mannwhitneyu(a, b, alternative="two-sided")
    rho_cont, p_cont = stats.spearmanr(df["min_incident_edge"], df["error_rate"])
    print("=== Check 1: near-tripoint (J_ij < 0.1) ===")
    print(f"  has_weak_edge=True: n={len(a)}, mean={a.mean():.4f}")
    print(f"  has_weak_edge=False: n={len(b)}, mean={b.mean():.4f}")
    print(f"  Mann-Whitney U={u}, raw p={p_mw:.4f}, Bonferroni-corrected p={bonferroni(p_mw):.4f}")
    print(f"  Spearman(min_incident_edge continuous, error_rate) = {rho_cont:.4f}, "
          f"raw p={p_cont:.4f}, Bonferroni-corrected p={bonferroni(p_cont):.4f}")

    # --- Check 2: total coupling strength ---
    rho_wdeg, p_wdeg = stats.spearmanr(df["weighted_degree"], df["error_rate"])
    print("\n=== Check 2: total coupling strength (weighted degree) ===")
    print(f"  Spearman rho={rho_wdeg:.4f}, raw p={p_wdeg:.4f}, "
          f"Bonferroni-corrected p={bonferroni(p_wdeg):.4f}")

    # --- Check 3: betweenness centrality ---
    G = nx.from_scipy_sparse_array(J)
    G = nx.relabel_nodes(G, {i: n for i, n in enumerate(nodes)})
    for u_, v_, d in G.edges(data=True):
        d["distance"] = 1.0 / d["weight"]
    bc = nx.betweenness_centrality(G, weight="distance", normalized=True)
    df["betweenness"] = df["node"].map(bc)
    rho_bc, p_bc = stats.spearmanr(df["betweenness"], df["error_rate"])
    print("\n=== Check 3: betweenness centrality (distance = 1/J_ij) ===")
    print(f"  Spearman rho={rho_bc:.4f}, raw p={p_bc:.4f}, "
          f"Bonferroni-corrected p={bonferroni(p_bc):.4f}")
    thresh = df["betweenness"].quantile(0.9)
    hi = df[df["betweenness"] >= thresh]
    lo = df[df["betweenness"] < thresh]
    print(f"  Top decile (n={len(hi)}): mean error_rate={hi['error_rate'].mean():.4f}")
    print(f"  Rest (n={len(lo)}): mean error_rate={lo['error_rate'].mean():.4f}")
    interior = df[df["is_boundary"] == False]
    rho_int, p_int = stats.spearmanr(interior["betweenness"], interior["error_rate"])
    print(f"  Interior subset only (n={len(interior)}): rho={rho_int:.4f}, p={p_int:.4f} (not Bonferroni-corrected, secondary check)")
    rho_wdeg_bc, p_wdeg_bc = stats.spearmanr(df["weighted_degree"], df["betweenness"])
    print(f"  Spearman(weighted_degree, betweenness) = {rho_wdeg_bc:.4f}, p={p_wdeg_bc:.4g}")

    # --- Check 4: community-boundary ---
    comms = nx.algorithms.community.louvain_communities(G, weight="weight", seed=42, resolution=1.0)
    comm_of = {n: i for i, c in enumerate(comms) for n in c}
    is_comm_boundary = {n: any(comm_of[nbr] != comm_of[n] for nbr in G.neighbors(n)) for n in G.nodes}
    df["comm_boundary"] = df["node"].map(is_comm_boundary)
    print(f"\n=== Check 4: community-boundary ({len(comms)} Louvain communities) ===")
    cb = df[df["comm_boundary"]]["error_rate"]
    ci = df[~df["comm_boundary"]]["error_rate"]
    print(f"  comm_boundary=True: n={len(cb)}, mean={cb.mean():.4f}")
    print(f"  comm_boundary=False: n={len(ci)}, mean={ci.mean():.4f}")
    rho_cb, p_cb = stats.spearmanr(df["comm_boundary"].astype(int), df["error_rate"])
    print(f"  Spearman rho={rho_cb:.4f}, raw p={p_cb:.4f}, Bonferroni-corrected p={bonferroni(p_cb):.4f}")
    for gam_b in [True, False]:
        sub = df[df["is_boundary"] == gam_b]
        for flag in [True, False]:
            s = sub[sub["comm_boundary"] == flag]
            if len(s):
                print(f"  GAM-boundary={gam_b}, comm_boundary={flag}: n={len(s)}, mean={s['error_rate'].mean():.4f}")

    out = RESULTS_DIR / "domain_wall_topology_checks_2026.csv"
    df.drop(columns=["idx"]).to_csv(out, index=False)
    print(f"\nPer-node results written to {out}")


if __name__ == "__main__":
    main()
