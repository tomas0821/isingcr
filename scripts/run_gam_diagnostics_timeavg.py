#!/usr/bin/env python3
"""Round-8 referee items: (1) score alignment and multistability on the per-site
time-averaged spin sign<s_i> over the measurement sweeps instead of the single
end-of-run snapshot, so that thermal flicker at T~1 is separated from a genuine
between-seed basin choice; (2) run the multistability, domain-wall and cascade
diagnostics on the OFFICIAL (inclusive, any-overlap) GAM field, not only on the
canton proxy, since the official area fractions put Tabarcia, Palmichal and
Monterrey outside the polygon.

For each field (proxy at T=1.008; official any-overlap at T=0.689, each at its
own best-of-grid T, unit weight) runs 16 seeds at the standard budget
(20000/20000 sweeps), saving final spins and site means, and reports:
  - alignment: snapshot vs sign<s_i>, median and mean+/-sd over seeds;
  - flicker: fraction of nodes with |<s_i>| < 0.5 (seed-averaged);
  - multistability: nodes whose sign<s_i> disagrees across seeds (minority
    count >= 3 of 16), compared with the snapshot-based count;
  - domain wall: boundary vs interior error rate of sign<s_i>, boundary
    defined by the field in use;
  - cascades for the 10 candidate distritos of run_gam_cascade_analysis.py
    (official field only): flip one node's field, rerun 16 seeds, count other
    nodes whose seed-majority sign<s_i> changes.

Writes data/processed/gam_diagnostics_timeavg_2026.npz.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.monte_carlo import temperature_scan
from run_gam_true_field import build_true_field
from run_gam_field import GAM_CANTONS, canton_of
from run_gam_cascade_analysis import CANDIDATES

N_EQUIL, N_SWEEPS, N_SEEDS, N_JOBS, SEED = 20000, 20000, 16, 12, 7
T_PROXY, T_ANY = 1.0080645161290325, 0.689
P = Path(__file__).resolve().parent.parent / "data" / "processed"


def run_field(J, h, T, emp):
    res = temperature_scan(J, h, [T] * N_SEEDS, n_equil=N_EQUIL, n_sweeps=N_SWEEPS,
                           dynamics="glauber", seed=SEED, n_jobs=N_JOBS, record_site_means=True)
    snaps, means = [], []
    for r in res:
        s, m = r["final_spins"].astype(np.int8), r["site_mean"]
        if np.mean(np.sign(m) == emp) < 0.5:  # Z2 sign resolution (never in doubt with h != 0)
            s, m = -s, -m
        snaps.append(s); means.append(m)
    return np.array(snaps), np.array(means)


def boundary_mask(J, is_gam):
    Jc = J.tocsr(); N = Jc.shape[0]; b = np.zeros(N, bool)
    for i in range(N):
        nb = Jc.indices[Jc.indptr[i]:Jc.indptr[i + 1]]
        b[i] = len(nb) > 0 and np.any(is_gam[nb] != is_gam[i])
    return b


def report(label, snaps, means, emp, J, h, nodes):
    N = len(emp)
    tsign = np.where(means >= 0, 1, -1).astype(np.int8)
    a_snap = (snaps == emp).mean(1); a_avg = (tsign == emp).mean(1)
    flicker = (np.abs(means) < 0.5).mean(1)
    print(f"\n=== {label} ===")
    print(f"alignment snapshot: median {np.median(a_snap):.4%}, mean {a_snap.mean():.4%} +/- {a_snap.std():.4%}")
    print(f"alignment sign<s_i>: median {np.median(a_avg):.4%}, mean {a_avg.mean():.4%} +/- {a_avg.std():.4%}")
    print(f"flicker |<s_i>|<0.5: mean fraction of nodes {flicker.mean():.4f} (per seed {np.round(flicker,4).tolist()})")
    # multistability: between-seed disagreement
    for name, S in (("snapshot", snaps), ("sign<s_i>", tsign)):
        minority = np.minimum((S == 1).sum(0), (S == -1).sum(0))
        locked = (minority == 0).mean()
        multi = np.where(minority >= 3)[0]
        print(f"multistability [{name}]: locked {locked:.3f}; nodes with minority>=3: {len(multi)}")
        for i in multi[np.argsort(-minority[multi])][:12]:
            print(f"    {nodes[i]:45s} minority {minority[i]:2d}/16  field {int(h[i]):+d} emp {int(emp[i]):+d}")
    for nm in ("SAN JOSE|MORA|TABARCIA", "SAN JOSE|ACOSTA|PALMICHAL", "SAN JOSE|ASERRI|MONTERREY", "CARTAGO|PARAISO|OROSI"):
        i = list(nodes).index(nm)
        ms = np.minimum((snaps[:, i] == 1).sum(), (snaps[:, i] == -1).sum())
        ma = np.minimum((tsign[:, i] == 1).sum(), (tsign[:, i] == -1).sum())
        print(f"  {nm:35s} field {int(h[i]):+d} emp {int(emp[i]):+d}  minority snapshot {ms}/16  sign<s> {ma}/16  mean<s_i> {means[:, i].mean():+.3f}  wrong(sign<s>) {(tsign[:, i] != emp[i]).sum()}/16")
    # domain wall
    is_gam = h > 0; b = boundary_mask(J, is_gam)
    err = (tsign != emp[None, :]).mean(0); err_s = (snaps != emp[None, :]).mean(0)
    u = mannwhitneyu(err[b], err[~b], alternative="greater")
    print(f"domain wall [sign<s_i>]: boundary n={b.sum()} err {err[b].mean():.3f} vs interior n={(~b).sum()} err {err[~b].mean():.3f}, MWU p={u.pvalue:.2e}")
    print(f"domain wall [snapshot]: boundary err {err_s[b].mean():.3f} vs interior {err_s[~b].mean():.3f}")
    return dict(a_snap=a_snap, a_avg=a_avg, flicker=flicker, err=err, err_snap=err_s, is_boundary=b)


def main():
    t0 = time.time()
    J, h_any, nodes, emp, frac = build_true_field("any", verbose=False)
    nodes = np.asarray(nodes); N = len(nodes)
    h_proxy = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
    out = {"nodes": nodes, "emp": emp, "h_proxy": h_proxy, "h_any": h_any, "T_proxy": T_PROXY, "T_any": T_ANY}

    sp_, mp_ = run_field(J, h_proxy, T_PROXY, emp)
    print(f"[proxy done {time.time()-t0:.0f}s]")
    rp = report("canton proxy, T=1.008", sp_, mp_, emp, J, h_proxy, nodes)
    out.update(snaps_proxy=sp_, means_proxy=mp_, **{f"proxy_{k}": v for k, v in rp.items()})

    sa, ma = run_field(J, h_any, T_ANY, emp)
    print(f"[official any done {time.time()-t0:.0f}s]")
    ra = report("official boundary (any overlap), T=0.689", sa, ma, emp, J, h_any, nodes)
    out.update(snaps_any=sa, means_any=ma, **{f"any_{k}": v for k, v in ra.items()})

    # cascades on the official field, scored on seed-majority sign<s_i>
    base = np.where(np.where(ma >= 0, 1, -1).sum(0) >= 0, 1, -1).astype(np.int8)
    idx = {n: i for i, n in enumerate(nodes)}
    targets, sizes, flipped = [], [], []
    print("\n=== cascades, official (any) field ===")
    for tgt, cat in CANDIDATES.items():
        if tgt not in idx:
            continue
        i = idx[tgt]; hp = h_any.copy(); hp[i] *= -1
        s2, m2 = run_field(J, hp, T_ANY, emp)
        pm = np.where(np.where(m2 >= 0, 1, -1).sum(0) >= 0, 1, -1).astype(np.int8)
        if np.mean(pm == base) < 0.5:
            pm = -pm
        d = pm != base; d[i] = False
        targets.append(tgt); sizes.append(int(d.sum())); flipped.append(list(nodes[d]))
        print(f"  {tgt:48s} field {int(h_any[i]):+d}: {int(d.sum()):3d} other nodes flipped {list(nodes[d])[:6]}  [{time.time()-t0:.0f}s]")
    out.update(cascade_targets=np.array(targets), cascade_sizes=np.array(sizes),
               cascade_flipped=np.array([";".join(f) for f in flipped]))
    np.savez(P / "gam_diagnostics_timeavg_2026.npz", **out)
    print(f"\nwritten ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
