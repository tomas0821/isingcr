#!/usr/bin/env python3
"""Regression baselines for the 2026 distrito map (N=488), to answer "why an
Ising model rather than a regression on the same covariates":
  (a) logistic: outcome ~ GAM                       (non-spatial)
  (b) logistic: outcome ~ GAM + IDS + log pop       (non-spatial)
  (c) spatial-lag logistic: (b) + J-weighted mean of neighbors' GAM field
  (d) autologistic: (b) + J-weighted mean of neighbors' OBSERVED outcome
(d) uses the true labels of neighbors as a covariate, so its in-sample
accuracy is not comparable to a model that must generate the whole map;
it is the standard autologistic baseline and is reported as such. Each is
scored in-sample and leave-one-province-out (fit on six provinces, predict
the seventh; for (d) the held-out province's own observed neighbor labels
are used, which is generous to the regression).
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_3d_scan import build_distrito_graph_and_fields
from run_gam_field import GAM_CANTONS, canton_of
from registered_voters import registered_voters

J, _hp, ids, nodes, emp = build_distrito_graph_and_fields()
Jc = J.tocsr(); deg = np.asarray(Jc.sum(axis=1)).ravel()
gam = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
lp = np.log(registered_voters(nodes)); lpz = (lp - lp.mean()) / lp.std()
y = (emp == 1).astype(float)
lag_gam = (Jc @ gam) / deg
lag_y = (Jc @ emp) / deg
prov = np.array([n.split("|")[0] for n in nodes])


def fit_logit(X, y, l2=1e-3):
    Xb = np.column_stack([np.ones(len(y)), X])
    def nll(w):
        z = Xb @ w; return np.sum(np.logaddexp(0, -z) * y + np.logaddexp(0, z) * (1 - y)) + l2 * np.sum(w[1:] ** 2)
    def grad(w):
        p = 1 / (1 + np.exp(-(Xb @ w))); g = Xb.T @ (p - y); g[1:] += 2 * l2 * w[1:]; return g
    return minimize(nll, np.zeros(Xb.shape[1]), jac=grad, method="L-BFGS-B").x


def predict(w, X):
    return (np.column_stack([np.ones(len(X)), X]) @ w > 0).astype(float)


models = {"(a) GAM": np.column_stack([gam]),
          "(b) GAM+IDS+logpop": np.column_stack([gam, ids, lpz]),
          "(c) (b)+lag(GAM)": np.column_stack([gam, ids, lpz, lag_gam]),
          "(d) autologistic (b)+lag(y)": np.column_stack([gam, ids, lpz, lag_y]),
          "(e) autologistic lag(y) only": np.column_stack([lag_y])}
baseline = max(y.mean(), 1 - y.mean())
print(f"N={len(y)}  majority baseline={baseline:.2%}")
for name, X in models.items():
    w = fit_logit(X, y); ins = np.mean(predict(w, X) == y)
    lopo = np.zeros(len(y))
    for p in np.unique(prov):
        m = prov == p; wp = fit_logit(X[~m], y[~m]); lopo[m] = predict(wp, X[m])
    lo = np.mean(lopo == y)
    per = {p: np.mean(lopo[prov == p] == y[prov == p]) for p in np.unique(prov)}
    print(f"{name:32s} in-sample {ins:.2%}   LOPO {lo:.2%}   per-province LOPO: " + " ".join(f"{k[:3]}={v:.0%}" for k, v in per.items()))
