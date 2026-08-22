#!/usr/bin/env python3
"""GAM (Gran Area Metropolitana) membership as a static, non-circular
predisposition field -- geography + capital-region membership predicting
the real 2026/2022 outcome.

Motivation: the historical-comparison section already notes the same
qualitative pattern in every election modeled so far (2018/2022/2026) --
the winner's opposition/minority concentrates in and around San Jose while
the winner sweeps the periphery. GAM membership is the natural quantitative
version of that pattern. Unlike MIDEPLAN IDS (a 2023-only snapshot) or the
prior-election political field (2022-only, and diluted by real allegiance
shifts -- see those runs), GAM is a STATIC administrative boundary, so the
exact same field applies unchanged to every election year -- no
comparability caveat needed.

GAM definition: 31 cantons across San Jose (13), Alajuela (3: Alajuela,
Atenas, Poas), Cartago (6), Heredia (9), per Plan GAM 2013-2030 (Decreto
Ejecutivo 38145-PLAN-MINAE-MIVAH-MOPT-S-MAG, La Gaceta No 82, 30 abril
2014). This is a CANTON-LEVEL proxy, not the precise distrito-level
boundary -- the real GAM cuts through some cantons at the distrito level
("184 distritos, en algunos casos fracciones de distritos" per the
official description), and the distrito-level annex/shapefile could not be
retrieved (MIVAH's site blocks automated access, a GeoNode GIS layer
refused the connection, an academic atlas PDF is now login-gated). So this
slightly over-includes a handful of large, mostly-rural cantons that only
partially qualify (e.g. Atenas, Aserri, Paraiso) -- a known, documented
imprecision, not a silent one. Free correlation check (2026-08-21, no MC)
found this still gives the strongest correlation of any field tried this
session: r=-0.589 with the 2026 outcome (r=-0.277 for 2022) -- see
00_Master_Notebook.md.

Field: h_gam = +1 if the distrito's canton is in the GAM list, else -1
(symmetric, not raw 0/1 -- matches every other margin-like field in this
project, which are all naturally centered at 0). Single field, no lambda
weighting, matches run_distrito_ablation.py's Run B / run_prior_margin_field.py.

Modes match run_prior_margin_field.py: --validate, --estimate, default
(full budget). --year selects 2026 or 2022.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from isingcr.simulation.monte_carlo import pooled_temperature_scan
from isingcr.simulation.observables import mcnemar_seed_summary, symmetric_alignment_fraction
from run_3d_scan import (
    FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED, FULL_T_RANGE,
    MAX_CORES_PER_TASK, MS_PER_SWEEP_DISTRITO,
    VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED, VALIDATE_TEMPERATURES,
)
from run_3d_scan import build_distrito_graph_and_fields as build_2026
from run_3d_scan_2022 import build_distrito_graph_and_fields as build_2022

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

GAM_CANTONS = {
    "SAN JOSE|CENTRAL", "SAN JOSE|ESCAZU", "SAN JOSE|DESAMPARADOS", "SAN JOSE|ASERRI",
    "SAN JOSE|MORA", "SAN JOSE|GOICOECHEA", "SAN JOSE|SANTA ANA", "SAN JOSE|ALAJUELITA",
    "SAN JOSE|VAZQUEZ DE CORONADO", "SAN JOSE|TIBAS", "SAN JOSE|MORAVIA",
    "SAN JOSE|MONTES DE OCA", "SAN JOSE|CURRIDABAT",
    "ALAJUELA|CENTRAL", "ALAJUELA|ATENAS", "ALAJUELA|POAS",
    "CARTAGO|CENTRAL", "CARTAGO|PARAISO", "CARTAGO|LA UNION", "CARTAGO|OREAMUNO",
    "CARTAGO|ALVARADO", "CARTAGO|EL GUARCO",
    "HEREDIA|CENTRAL", "HEREDIA|BARVA", "HEREDIA|SANTO DOMINGO", "HEREDIA|SANTA BARBARA",
    "HEREDIA|SAN RAFAEL", "HEREDIA|SAN ISIDRO", "HEREDIA|BELEN", "HEREDIA|FLORES",
    "HEREDIA|SAN PABLO",
}
assert len(GAM_CANTONS) == 31

BUILDERS = {"2026": build_2026, "2022": build_2022}


def canton_of(node_code: str) -> str:
    parts = node_code.split("|")
    return parts[0] + "|" + parts[1]


def build_graph_and_gam_field(year: str):
    build_fn = BUILDERS[year]
    J, _h_pol_own, _h_soc, nodes, empirical = build_fn()
    gam = np.array([1.0 if canton_of(n) in GAM_CANTONS else -1.0 for n in nodes])
    n_gam = int((gam > 0).sum())
    print(f"  GAM distritos (canton-level proxy): {n_gam}/{len(nodes)}")
    return J, gam, nodes, empirical


def scan(J, h, empirical, majority_label, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs):
    pooled = pooled_temperature_scan(J, h, temperatures, n_seeds=n_seeds,
                                      n_equil=n_equil, n_sweeps=n_sweeps,
                                      dynamics="glauber", seed=seed, n_jobs=n_jobs)
    per_t_accuracy = [
        float(np.mean([symmetric_alignment_fraction(s, empirical) for s in p["final_spins_per_seed"]]))
        for p in pooled
    ]
    best_idx = int(np.argmax(per_t_accuracy))
    mc = mcnemar_seed_summary(pooled[best_idx]["final_spins_per_seed"], empirical, majority_label)
    return {
        "best_T": float(temperatures[best_idx]), "best_accuracy": per_t_accuracy[best_idx],
        "accuracy_by_T": per_t_accuracy, "mcnemar_median_p": mc["median_exact_pvalue"],
    }


def estimate_resources(n_temperatures, n_seeds, n_equil, n_sweeps):
    cores_per_task = min(MAX_CORES_PER_TASK, n_temperatures)
    t_batches = -(-n_temperatures // cores_per_task)
    wall_seconds = n_seeds * t_batches * (n_equil + n_sweeps) * MS_PER_SWEEP_DISTRITO / 1000.0
    print("=== Resource estimate (grounded in 2026-08-16 cluster benchmark) ===")
    print(f"  1 field x {n_temperatures} T x {n_seeds} seeds")
    print(f"  Cores per task: {cores_per_task}")
    print(f"  Estimated wall time: {wall_seconds:.1f}s ({wall_seconds / 60:.1f} min)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", choices=["2026", "2022"], default="2026")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--n-temperatures", type=int, default=32)
    args = parser.parse_args()

    if args.estimate and not args.validate:
        estimate_resources(args.n_temperatures, FULL_N_SEEDS, FULL_N_EQUIL, FULL_N_SWEEPS)
        return

    RESULTS_DIR.mkdir(exist_ok=True, parents=True)
    print(f"Building real {args.year} distrito network + GAM field...")
    t0 = time.time()
    J, h_gam, nodes, empirical = build_graph_and_gam_field(args.year)
    N = J.shape[0]
    majority_label = 1 if np.mean(empirical == 1) > 0.5 else -1
    print(f"  N={N} distritos, {J.nnz // 2} edges, built in {time.time() - t0:.1f}s")

    if args.validate:
        n_equil, n_sweeps, n_seeds, seed = VALIDATE_N_EQUIL, VALIDATE_N_SWEEPS, VALIDATE_N_SEEDS, VALIDATE_SEED
        temperatures = VALIDATE_TEMPERATURES
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        print(f"\n--validate mode: {len(temperatures)} T, {n_equil}+{n_sweeps} sweeps, {n_seeds} seed.")
    else:
        temperatures = np.linspace(*FULL_T_RANGE, args.n_temperatures)
        n_equil, n_sweeps, n_seeds, seed = FULL_N_EQUIL, FULL_N_SWEEPS, FULL_N_SEEDS, FULL_SEED
        n_jobs = min(MAX_CORES_PER_TASK, len(temperatures))
        estimate_resources(args.n_temperatures, n_seeds, n_equil, n_sweeps)

    t_start = time.time()
    r = scan(J, h_gam, empirical, majority_label, temperatures, n_equil, n_sweeps, n_seeds, seed, n_jobs)
    elapsed = time.time() - t_start
    print(f"\ngam_field year={args.year} -> best T={r['best_T']:.3f}, "
          f"best accuracy={r['best_accuracy']:.3%}, McNemar median p={r['mcnemar_median_p']:.4f} "
          f"({elapsed:.1f}s)")

    if not args.validate:
        out_path = RESULTS_DIR / f"gam_field_{args.year}.npz"
        np.savez(out_path, result=r, temperatures=temperatures, N=N,
                 n_equil=n_equil, n_sweeps=n_sweeps, n_seeds=n_seeds)
        print(f"Raw results written to {out_path}")


if __name__ == "__main__":
    main()
