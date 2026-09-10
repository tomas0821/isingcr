#!/usr/bin/env python3
"""Round-10 referee item: the domain-wall contrast (boundary vs interior
error rate) was tested with per-unit tests (Mann-Whitney, Fisher) that assume
independent units, the assumption Section 3.4 rejects for this map. This
script (i) compares boundary and interior distritos WITHIN each canton that
contains both, and (ii) runs a canton-cluster bootstrap of the boundary minus
interior error difference on the consensus (time-averaged, seed-majority)
configuration of each field at T=1.008, from gam_timeavg_grid_2026.npz.
Writes data/processed/domain_wall_cluster_test_2026.npz.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_gam_true_field import build_true_field
P = Path(__file__).resolve().parent.parent / "data" / "processed"
N_BOOT = 20000


def main():
    z = np.load(P / "gam_timeavg_grid_2026.npz", allow_pickle=True)
    nodes, emp = z["nodes"], z["emp"]; N = len(emp)
    J, _, _, _, _ = build_true_field("any", verbose=False); Jc = J.tocsr()
    canton = np.array(["|".join(n.split("|")[:2]) for n in nodes]); cantons = np.unique(canton)
    members = {c: np.where(canton == c)[0] for c in cantons}
    rng = np.random.default_rng(2026); out = {}
    for tag, h in (("proxy_hi", z["h_proxy"]), ("any_hi", z["h_any"])):
        g = h > 0; b = np.zeros(N, bool)
        for i in range(N):
            nb = Jc.indices[Jc.indptr[i]:Jc.indptr[i + 1]]; b[i] = len(nb) > 0 and np.any(g[nb] != g[i])
        wrong = (z[f"{tag}_cons"] != emp).astype(float)
        obs = wrong[b].mean() - wrong[~b].mean()
        # within-canton comparison
        diffs = []
        for c in cantons:
            m = members[c]
            if b[m].any() and (~b[m]).any():
                diffs.append(wrong[m[b[m]]].mean() - wrong[m[~b[m]]].mean())
        diffs = np.array(diffs)
        strad = np.array([b[members[c]].any() for c in cantons]); cerr = np.array([wrong[members[c]].mean() for c in cantons])
        # canton-cluster bootstrap
        boots = []
        for _ in range(N_BOOT):
            pick = rng.choice(len(cantons), len(cantons), replace=True)
            idx = np.concatenate([members[cantons[k]] for k in pick]); bb = b[idx]; ww = wrong[idx]
            if bb.any() and (~bb).any():
                boots.append(ww[bb].mean() - ww[~bb].mean())
        boots = np.array(boots); p_two = 2 * min(np.mean(boots <= 0), np.mean(boots >= 0)); p_two = max(p_two, 1 / len(boots))
        print(f"== {tag} (T=1.008, seeds {int(z[f'{tag}_seed0'])}-{int(z[f'{tag}_seed0'])+15}, consensus map)")
        print(f"   boundary err {wrong[b].mean():.3f} (n={b.sum()}) vs interior {wrong[~b].mean():.3f} (n={(~b).sum()}), gap {obs:+.3f}")
        print(f"   within-canton ({len(diffs)} cantons with both): boundary worse {int((diffs>0).sum())}, better {int((diffs<0).sum())}, tied {int((diffs==0).sum())}, mean diff {diffs.mean():+.3f}")
        print(f"   cantons the line cuts (n={strad.sum()}) err {cerr[strad].mean():.3f} vs others (n={(~strad).sum()}) {cerr[~strad].mean():.3f}")
        print(f"   canton-cluster bootstrap ({N_BOOT}): 95% CI [{np.percentile(boots,2.5):+.3f}, {np.percentile(boots,97.5):+.3f}], two-sided p = {p_two:.4f}, x32 = {min(1,32*p_two):.3f}")
        out.update({f"{tag}_gap": obs, f"{tag}_within": diffs, f"{tag}_boot": boots, f"{tag}_p_two": p_two,
                    f"{tag}_strad_err": cerr[strad].mean(), f"{tag}_other_err": cerr[~strad].mean()})
    np.savez(P / "domain_wall_cluster_test_2026.npz", **out); print("written")


if __name__ == "__main__":
    main()
