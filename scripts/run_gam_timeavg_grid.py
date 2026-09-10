#!/usr/bin/env python3
"""Round-9 referee items on the time-averaged diagnostics: (1) the missing
temperature x field cells (proxy at T=0.689, official inclusive at T=1.008)
so that block-level basin choice can be attributed to T or to the field;
(2) an independent seed set for the official field (the round-8 reruns
shared seeds 7-22 with the proxy, so the same two atypical starts appeared
under both fields); (3) per-chain configuration series every 100 sweeps to
show whether a chain is stationary over the measurement window
(first-half vs second-half agreement of sign<s_i>) and to expose the decay
of a metastable periphery domain; (4) the 2022 proxy system at T=1.008 with
time averages, so both years are scored under one rule.

Cells (16 chains each, 20000/20000 sweeps):
  proxy 2026 @1.008 seeds 7-22 (repeat of the round-8 run, now with series)
  proxy 2026 @0.689 seeds 7-22
  official-any 2026 @1.008 seeds 107-122
  official-any 2026 @0.689 seeds 107-122
  proxy 2022 @1.008 seeds 7-22
Writes data/processed/gam_timeavg_grid_2026.npz.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isingcr.simulation.monte_carlo import temperature_scan
from run_gam_true_field import build_true_field
from run_gam_field import GAM_CANTONS, canton_of, build_graph_and_gam_field

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, EVERY = 20000, 20000, 16, 12, 100
T_HI, T_LO = 1.0080645161290325, 0.689
P = Path(__file__).resolve().parent.parent / "data" / "processed"


def run_cell(J, h, T, emp, seed):
    res = temperature_scan(J, h, [T] * N_SEEDS, n_equil=N_EQUIL, n_sweeps=N_SWEEPS, dynamics="glauber",
                           seed=seed, n_jobs=N_JOBS, record_site_means=True, record_spins_every=EVERY)
    snaps, means, series = [], [], []
    for r in res:
        s, m, ser = r["final_spins"].astype(np.int8), r["site_mean"], r["spin_series"]
        if np.mean(np.sign(m) == emp) < 0.5:  # global orientation resolved against the map (one bit)
            s, m, ser = -s, -m, -ser
        snaps.append(s); means.append(m); series.append(ser)
    return np.array(snaps), np.array(means), np.array(series)


def summarize(label, snaps, means, series, emp, h, nodes):
    ts = np.where(means >= 0, 1, -1); cons = np.where(ts.sum(0) >= 0, 1, -1)
    a = (ts == emp).mean(1); a_snap = (snaps == emp).mean(1)
    n = series.shape[1]; h1 = series[:, : n // 2].mean(1); h2 = series[:, n // 2 :].mean(1)
    stat = (np.sign(h1) == np.sign(h2)).mean(1)  # first-half vs second-half sign agreement
    align_series = (series == emp[None, None, :]).mean(2)  # chains x records
    mino = np.minimum((ts == 1).sum(0), (ts == -1).sum(0))
    print(f"\n=== {label} ===")
    print(f"align sign<s>: median {np.median(a):.4%} mean {a.mean():.4%}+/-{a.std():.4%}; snapshot median {np.median(a_snap):.4%}")
    print(f"per-chain align {np.round(100*a,1).tolist()}")
    print(f"stationarity (half agreement) {np.round(stat,3).tolist()}")
    print(f"nodes differing from consensus per chain {(ts != cons).sum(1).tolist()}")
    print(f"locked {(mino==0).mean():.3f}; >=3 minority: {int((mino>=3).sum())} -> {[ (str(nodes[i]), int(mino[i])) for i in np.where(mino>=3)[0]][:16]}")
    for nm in ("PUNTARENAS|OSA|BAHIA DRAKE", "PUNTARENAS|GOLFITO|GOLFITO", "CARTAGO|PARAISO|OROSI", "CARTAGO|CENTRAL|CORRALILLO",
               "SAN JOSE|MORA|TABARCIA", "SAN JOSE|ACOSTA|PALMICHAL", "SAN JOSE|ASERRI|MONTERREY", "HEREDIA|CENTRAL|VARABLANCA"):
        if nm in list(nodes):
            i = list(nodes).index(nm); print(f"  {nm:42s} <s> mean {means[:,i].mean():+.2f} sd {means[:,i].std():.2f} minority {int(mino[i])}/16")
    return dict(a=a, a_snap=a_snap, stat=stat, align_series=align_series, mino=mino, cons=cons)


def main():
    t0 = time.time(); out = {}
    J, h_any, nodes, emp, _ = build_true_field("any", verbose=False); nodes = np.asarray(nodes)
    h_proxy = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
    out.update(nodes=nodes, emp=emp, h_proxy=h_proxy, h_any=h_any)
    for tag, h, T, seed in (("proxy_hi", h_proxy, T_HI, 7), ("proxy_lo", h_proxy, T_LO, 7),
                            ("any_hi", h_any, T_HI, 107), ("any_lo", h_any, T_LO, 107)):
        sn, mn, ser = run_cell(J, h, T, emp, seed)
        r = summarize(f"{tag} T={T:.3f} seeds {seed}-{seed+15}", sn, mn, ser, emp, h, nodes)
        out.update({f"{tag}_snaps": sn, f"{tag}_means": mn, f"{tag}_T": T, f"{tag}_seed0": seed,
                    **{f"{tag}_{k}": v for k, v in r.items()}})
        print(f"[{tag} done {time.time()-t0:.0f}s]")
    # 2022 proxy system
    J22, h22, nodes22, emp22 = build_graph_and_gam_field("2022"); nodes22 = np.asarray(nodes22)
    sn, mn, ser = run_cell(J22, h22, T_HI, emp22, 7)
    r = summarize("proxy 2022 T=1.008 seeds 7-22", sn, mn, ser, emp22, h22, nodes22)
    out.update(nodes22=nodes22, emp22=emp22, h22=h22, p22_snaps=sn, p22_means=mn, **{f"p22_{k}": v for k, v in r.items()})
    np.savez(P / "gam_timeavg_grid_2026.npz", **out)
    print(f"\nwritten ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
