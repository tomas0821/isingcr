#!/usr/bin/env python3
"""Why does a +/-1 GAM field beat the continuous IDS field as an Ising field
when both correlate with the 2026 outcome about equally? No MC -- everything
is computed from the fields and the empirical map on the N=488 network.

Reports: r(GAM, IDS) collinearity and overlap; each field's structural
ceiling (fraction of units on the side the field's sign predicts, best
global Z2 orientation); the best single IDS threshold (chosen on the
outcome, so a ceiling comparison, not a fair field); how much of the IDS
field's magnitude sits on the extreme quartile; how often each field
opposes a unit's own neighbor majority on the real map; and whether IDS
still discriminates within GAM.
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from run_3d_scan import build_distrito_graph_and_fields  # noqa: E402
from run_gam_field import build_graph_and_gam_field  # noqa: E402

J, h_pol, ids, nodes, emp = build_distrito_graph_and_fields()
_, gam, nodes2, _ = build_graph_and_gam_field("2026")
assert list(nodes) == list(nodes2)
is_gam = gam > 0
lead = 1 if np.mean(emp == 1) > 0.5 else -1


def ceiling(h):
    return max(np.mean(np.sign(h) == emp), np.mean(np.sign(h) == -emp))


print("== collinearity ==")
print(f"r(GAM, IDS z)            = {np.corrcoef(gam, ids)[0,1]:.3f}")
print(f"mean IDS z  GAM/periph   = {ids[is_gam].mean():+.2f} / {ids[~is_gam].mean():+.2f}")
q = np.quantile(ids, [0.25, 0.5, 0.75])
print(f"GAM above median IDS     = {np.mean(ids[is_gam] > q[1]):.0%};  GAM in bottom quartile = {np.mean(ids[is_gam] < q[0]):.0%}")
print(f"top-quartile IDS that are GAM = {np.mean(is_gam[ids > q[2]]):.0%}")
print(f"r(IDS, outcome) / r(GAM, outcome) = {np.corrcoef(ids, emp)[0,1]:+.3f} / {np.corrcoef(gam, emp)[0,1]:+.3f}")

print("== field shape ==")
print(f"structural ceiling  GAM = {ceiling(gam):.1%}   sign(IDS) = {ceiling(ids):.1%}")
best = max((max(np.mean((ids > c) == (emp == -1)), np.mean((ids > c) == (emp == 1))), c)
           for c in np.quantile(ids, np.linspace(0.02, 0.98, 97)))
print(f"best single IDS threshold ceiling = {best[0]:.1%} at z={best[1]:+.2f} (chosen on outcome)")
a = np.abs(ids)
print(f"share of |IDS field| on top-|z| quartile = {a[a > np.quantile(a, .75)].sum()/a.sum():.0%}  (GAM: 25% by construction)")
nb = J.tocsr().dot(emp)
for name, h in [("GAM", gam), ("IDS", np.sign(ids))]:
    s = h if np.mean(h == emp) >= 0.5 else -h
    print(f"{name} field opposes true neighbor majority on {np.mean(np.sign(nb) != s):.0%} of distritos")

print("== within GAM ==")
on = emp[is_gam] == lead
print(f"IDS z, GAM distritos on leading side / coalition side = {ids[is_gam][on].mean():+.2f} / {ids[is_gam][~on].mean():+.2f}")
