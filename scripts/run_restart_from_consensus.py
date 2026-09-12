#!/usr/bin/env python3
"""Cold-read referee item: are the periphery domains metastable equilibria or
finite-budget trapping from random starts? For each (field, T) cell of
gam_timeavg_grid_2026.npz, run 16 chains started FROM THE CONSENSUS
configuration and 16 started FROM THE SEED-20 DOMAIN configuration, each for
5x the standard budget (100,000 sweeps, no separate equilibration), recording
the configuration every 500 sweeps. If chains started at the consensus never
enter a domain and chains started in the domain decay to the consensus, the
domains are trapping, not equilibria. Writes
data/processed/restart_from_consensus_2026.npz.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np
import scipy.sparse as sp
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.ising_model import IsingModel
from isingcr.simulation.monte_carlo import run_mc
from run_gam_true_field import build_true_field
from run_gam_field import GAM_CANTONS, canton_of

N_SWEEPS, N_CHAINS, N_JOBS, EVERY = 100_000, 16, 12, 500
P = Path(__file__).resolve().parent.parent / "data" / "processed"


def _worker(J_data, J_indices, J_indptr, J_shape, h, T, spins0, seed):
    J = sp.csr_matrix((J_data, J_indices, J_indptr), shape=J_shape)
    rng = np.random.default_rng(seed)
    model = IsingModel(J, h, spins=spins0.copy(), rng=rng)
    r = run_mc(model, T, n_equil=0, n_sweeps=N_SWEEPS, dynamics="glauber", rng=rng,
               record_site_means=True, record_spins_every=EVERY)
    return r["site_mean"], r["spin_series"]


def run_cell(J, h, T, start, seed0):
    Jc = J.tocsr(); args = [(Jc.data, Jc.indices, Jc.indptr, Jc.shape, h, T, start, seed0 + k) for k in range(N_CHAINS)]
    with ProcessPoolExecutor(max_workers=N_JOBS) as pool:
        res = list(pool.map(_worker, *zip(*args)))
    means = np.array([r[0] for r in res]); series = np.array([r[1] for r in res], dtype=np.int8)
    return means, series


def main():
    t0 = time.time()
    z = np.load(P / "gam_timeavg_grid_2026.npz", allow_pickle=True)
    J, h_any, nodes, emp, _ = build_true_field("any", verbose=False); nodes = np.asarray(nodes)
    h_proxy = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
    # the fields as simulated are oriented opposite to the stored (resolved) configurations;
    # start configurations are therefore flipped back into the simulation frame
    out = {"nodes": nodes, "emp": emp}
    for tag, h, T in (("proxy_hi", h_proxy, 1.0080645161290325), ("proxy_lo", h_proxy, 0.689),
                      ("any_hi", h_any, 1.0080645161290325), ("any_lo", h_any, 0.689)):
        cons = z[f"{tag}_cons"].astype(np.int8)
        dom_src = "proxy_hi" if tag.startswith("proxy") else "any_hi"
        m = z[f"proxy_hi_means"]; ts = np.where(m >= 0, 1, -1).astype(np.int8)
        dom = ts[13]  # seed-20 chain of the proxy run: the frozen 72-site periphery domain
        for start_name, start in (("consensus", cons), ("domain", dom)):
            sim_start = (-start).astype(np.int8)  # into the simulation frame (h=+1 on GAM)
            means, series = run_cell(J, h, T, sim_start, 1000 + 100 * ["proxy_hi","proxy_lo","any_hi","any_lo"].index(tag) + (0 if start_name == "consensus" else 50))
            # resolve orientation as elsewhere: flip so that sign<s> agrees with the map
            flip = np.array([np.mean(np.sign(mm) == emp) < 0.5 for mm in means])
            means[flip] *= -1; series[flip] *= -1
            tsign = np.where(means >= 0, 1, -1)
            align = (series == emp[None, None, :]).mean(2)  # chains x records
            off = (tsign != cons[None, :]).sum(1)
            print(f"{tag} from {start_name} T={T:.3f}: final align per chain {np.round(100*align[:,-1],1).tolist()}")
            print(f"   sites off consensus (time-avg sign) {off.tolist()}; align first/last record mean {100*align[:,0].mean():.1f} -> {100*align[:,-1].mean():.1f}  [{time.time()-t0:.0f}s]")
            out.update({f"{tag}_{start_name}_means": means, f"{tag}_{start_name}_align": align, f"{tag}_{start_name}_off": off})
    np.savez(P / "restart_from_consensus_2026.npz", **out); print("written")


if __name__ == "__main__":
    main()
