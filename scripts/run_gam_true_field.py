#!/usr/bin/env python3
"""GAM field from the OFFICIAL distrito-level boundary (MIVAH GeoExplora
polygon 'Limite_GAM', Plan GAM 2013-2030) instead of the 31-canton proxy.

Two pre-specified definitions of membership from each distrito's area
fraction inside the polygon:
  majority : h=+1 if fraction >= 0.5   (162 distritos)
  any      : h=+1 if fraction >  0.01  (175 distritos; includes split units)
The canton proxy has 186. Same MC budget/grid/seeds as run_gam_lambda_scan.py;
LAMBDA_GRID = [1.0, 1.5]; SLURM array index = variant*2 + lambda index.
--diagnose prints the membership comparison without MC.
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

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "data" / "processed"
LAMBDA_GRID = [1.0, 1.5]
VARIANTS = ["majority", "any"]


def gam_fractions(nodes):
    import geopandas as gpd
    from isingcr.ingestion import load_shapefile
    from isingcr.ingestion.canton_names import normalize_distrito_code
    gam = gpd.read_file(ROOT / "data" / "raw" / "gam" / "gam_limite" / "GAM_LIMITE_1.shp").to_crs(5367)
    poly = gam.geometry.union_all() if hasattr(gam.geometry, "union_all") else gam.geometry.unary_union
    d = load_shapefile(ROOT / "data" / "raw" / "boundaries" / "extracted" / "cri_admin3.shp", id_col="adm3_name").to_crs(5367)
    d["code"] = [normalize_distrito_code(p, c, x) for p, c, x in zip(d["adm1_name"], d["adm2_name"], d["adm3_name"])]
    frac = dict(zip(d["code"], d.geometry.intersection(poly).area / d.geometry.area))
    f = np.array([frac[n] for n in nodes])
    return f


def build_true_field(variant, verbose=True):
    J, _hp, _ids, nodes, empirical = build_distrito_graph_and_fields()
    f = gam_fractions(nodes)
    member = f >= 0.5 if variant == "majority" else f > 0.01
    h = np.where(member, 1.0, -1.0)
    if verbose:
        proxy = np.array([canton_of(n) in GAM_CANTONS for n in nodes])
        ceil = lambda hh: max(np.mean(np.sign(hh) == empirical), np.mean(np.sign(hh) == -empirical))
        print(f"  variant={variant}: GAM distritos {int(member.sum())} (proxy {int(proxy.sum())}); "
              f"proxy-only {int((proxy & ~member).sum())}, new {int((member & ~proxy).sum())}; ceiling {ceil(h):.2%} (proxy {ceil(np.where(proxy,1.,-1.)):.2%})")
    return J, h, nodes, empirical, f


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--diagnose", action="store_true"); ap.add_argument("--validate", action="store_true")
    ap.add_argument("--estimate", action="store_true"); ap.add_argument("--task-index", type=int, default=None)
    ap.add_argument("--variant", choices=VARIANTS, default="majority"); ap.add_argument("--n-temperatures", type=int, default=32)
    a = ap.parse_args()
    if a.estimate:
        print("4 tasks (2 variants x 2 lambdas) x 32 T x 16 seeds; ~30 min each on shared"); return
    if a.task_index is not None:
        variant = VARIANTS[a.task_index // len(LAMBDA_GRID)]; lambdas = [LAMBDA_GRID[a.task_index % len(LAMBDA_GRID)]]
    else:
        variant = a.variant; lambdas = LAMBDA_GRID
    J, h, nodes, empirical, frac = build_true_field(variant)
    if a.diagnose: return
    N = J.shape[0]; majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    if a.validate:
        temperatures, lambdas = VALIDATE_TEMPERATURES, [1.0]
        n_equil, n_sweeps, n_seeds, seed = VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED
    else:
        temperatures = np.linspace(*FULL_T_RANGE, a.n_temperatures)
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
    n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
    results = []
    for lam in lambdas:
        t0 = time.time()
        r = scan_point(J, h, lam, empirical, majority_label, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs)
        results.append(r)
        print(f"  variant={variant} lambda_soc={lam:.2f} -> best T={r['best_T']:.3f}, best accuracy={r['best_accuracy']:.3%} +/- {r['best_accuracy_std']:.3%}, McNemar median p={r['mcnemar_median_p']:.4g}  ({time.time()-t0:.0f}s)")
    if not a.validate:
        suffix = f"_task{a.task_index}" if a.task_index is not None else ""
        out = RESULTS_DIR / f"gam_true_field_2026_{variant}{suffix}.npz"
        np.savez(out, results=np.array(results, dtype=object), lambda_grid=np.array(LAMBDA_GRID), temperatures=temperatures,
                 nodes=np.array(nodes), empirical=empirical, h=h, frac=frac, variant=variant, N=N, n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print("written", out)


if __name__ == "__main__":
    main()
