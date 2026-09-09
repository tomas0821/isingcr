#!/usr/bin/env python3
"""Residualized GAM field: regress the +/-1 GAM membership field on the
MIDEPLAN IDS composite (z-scored) and log registered-voter count, take the
OLS residual, z-score it, and use it as h_soc in Eq. (3) at lambda_pol=0.
If this field still reproduces the 2026 map, GAM membership is not merely a
proxy for development or population. Same budget/grid/seeds as
run_gam_lambda_scan.py; LAMBDA_GRID = [1, 1.5, 2] (one SLURM task each).
--diagnose prints the field's construction statistics without any MC.
"""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_3d_scan import (FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, FULL_T_RANGE, MAX_CORES_PER_TASK,
                         VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED, VALIDATE_TEMPERATURES,
                         build_distrito_graph_and_fields)
from run_gam_field import GAM_CANTONS, canton_of
from run_gam_lambda_scan import scan_point
from registered_voters import registered_voters

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
LAMBDA_GRID = [1.0, 1.5, 2.0]


def build_residual_field(verbose=True):
    J, _h_pol, ids, nodes, empirical = build_distrito_graph_and_fields()
    gam = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
    pop = registered_voters(nodes, "2026")
    assert not np.isnan(pop).any()
    lp = np.log(pop); lpz = (lp - lp.mean()) / lp.std()
    X = np.column_stack([np.ones(len(nodes)), ids, lpz])
    beta, *_ = np.linalg.lstsq(X, gam, rcond=None)
    resid = gam - X @ beta
    h = (resid - resid.mean()) / resid.std()
    if verbose:
        r = lambda a, b: np.corrcoef(a, b)[0, 1]
        ceil = lambda f: max(np.mean(np.sign(f) == empirical), np.mean(np.sign(f) == -empirical))
        print(f"  OLS gam ~ 1 + ids + logpop: beta={beta.round(3)}, R^2={1-resid.var()/gam.var():.3f}")
        print(f"  r(resid, ids)={r(h, ids):+.3f}  r(resid, logpop)={r(h, lpz):+.3f}  r(resid, gam)={r(h, gam):+.3f}  r(resid, outcome)={r(h, empirical):+.3f}")
        print(f"  r(gam, outcome)={r(gam, empirical):+.3f}  r(ids, outcome)={r(ids, empirical):+.3f}  r(logpop, outcome)={r(lpz, empirical):+.3f}")
        print(f"  sign-agreement ceiling: resid {ceil(h):.1%}  gam {ceil(gam):.1%}  ids {ceil(ids):.1%}")
        print(f"  resid field: sign(resid)==sign(gam) on {np.mean(np.sign(h)==gam):.1%} of nodes; std {h.std():.3f}")
    return J, h, nodes, empirical, dict(beta=beta, gam=gam, ids=ids, lpz=lpz)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--diagnose", action="store_true"); ap.add_argument("--validate", action="store_true")
    ap.add_argument("--estimate", action="store_true"); ap.add_argument("--lambda-index", type=int, default=None)
    ap.add_argument("--n-temperatures", type=int, default=32)
    a = ap.parse_args()
    if a.estimate:
        print("3 lambda points x 32 T x 16 seeds; same cost as one run_gam_lambda_scan.py task each (~30 min on shared)"); return
    J, h, nodes, empirical, meta = build_residual_field()
    if a.diagnose: return
    N = J.shape[0]; majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    if a.validate:
        temperatures, lambdas = VALIDATE_TEMPERATURES, [1.0]
        n_equil, n_sweeps, n_seeds, seed = VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED
    else:
        temperatures = np.linspace(*FULL_T_RANGE, a.n_temperatures)
        lambdas = [LAMBDA_GRID[a.lambda_index]] if a.lambda_index is not None else LAMBDA_GRID
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
    n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
    results = []
    for lam in lambdas:
        t0 = time.time()
        r = scan_point(J, h, lam, empirical, majority_label, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs)
        results.append(r)
        print(f"  lambda_soc={lam:.2f} -> best T={r['best_T']:.3f}, best accuracy={r['best_accuracy']:.3%} +/- {r['best_accuracy_std']:.3%}, McNemar median p={r['mcnemar_median_p']:.4g}  ({time.time()-t0:.0f}s)")
    if not a.validate:
        suffix = f"_lam{a.lambda_index}" if a.lambda_index is not None else ""
        out = RESULTS_DIR / f"gam_residual_field_2026{suffix}.npz"
        np.savez(out, results=np.array(results, dtype=object), lambda_grid=np.array(LAMBDA_GRID), temperatures=temperatures,
                 nodes=np.array(nodes), empirical=empirical, h_resid=h, beta=meta["beta"], N=N, n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print("written", out)


if __name__ == "__main__":
    main()
