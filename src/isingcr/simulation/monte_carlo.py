"""Monte Carlo driver: sweeps, equilibration + measurement runs, and temperature scans.

The temperature scan is embarrassingly parallel (each T is independent), which is
the natural seam for later HPC/array-job parallelization -- swap the local
ProcessPoolExecutor here for an MPI or job-array dispatcher without touching
ising_model.py or dynamics.py.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from typing import Sequence

import numpy as np
import scipy.sparse as sp

from .dynamics import DYNAMICS
from .ising_model import IsingModel


def run_sweep(model: IsingModel, T: float, dynamics: str = "glauber",
              rng: np.random.Generator | None = None) -> int:
    """One sweep = N randomly-ordered single-spin update attempts. Returns #flips."""
    rng = rng if rng is not None else model.rng
    step_fn = DYNAMICS[dynamics]
    order = rng.permutation(model.N)
    n_flips = 0
    for i in order:
        if step_fn(model, int(i), T, rng):
            n_flips += 1
    return n_flips


def run_mc(model: IsingModel, T: float, n_equil: int = 200, n_sweeps: int = 200,
           dynamics: str = "glauber", measure_every: int = 1,
           rng: np.random.Generator | None = None,
           record_site_means: bool = False,
           record_spins_every: int | None = None) -> dict:
    """Equilibrate for n_equil sweeps, then measure every `measure_every` sweeps.

    Returns a dict with energy/magnetization time series and the final spin config.
    With record_site_means=True it also returns "site_mean", the per-site
    time-averaged spin <s_i> over the measured sweeps, so that alignment and
    multistability can be scored on sign<s_i> rather than on the single
    end-of-run snapshot (which cannot separate thermal flicker at T~1 from a
    genuine between-seed basin choice). With record_spins_every=k it also
    returns "spin_series", the full configuration every k measurement
    sweeps (int8, n_records x N), for stationarity checks along the run.
    """
    rng = rng if rng is not None else model.rng
    for _ in range(n_equil):
        run_sweep(model, T, dynamics, rng)

    energies, magnetizations = [], []
    site_sum = np.zeros(model.N, dtype=np.float64) if record_site_means else None
    n_measured = 0
    series = [] if record_spins_every else None
    for step in range(n_sweeps):
        run_sweep(model, T, dynamics, rng)
        if step % measure_every == 0:
            energies.append(model.energy())
            magnetizations.append(model.magnetization())
            if record_site_means:
                site_sum += model.spins
            n_measured += 1
        if record_spins_every and step % record_spins_every == 0:
            series.append(model.spins.astype(np.int8).copy())

    out = {
        "T": T,
        "energy": np.array(energies),
        "magnetization": np.array(magnetizations),
        "final_spins": model.spins.copy(),
    }
    if record_site_means:
        out["site_mean"] = site_sum / max(n_measured, 1)
    if record_spins_every:
        out["spin_series"] = np.array(series, dtype=np.int8)
    return out


def _run_single_temperature(J_data, J_indices, J_indptr, J_shape, h, T, n_equil,
                             n_sweeps, dynamics, measure_every, seed,
                             record_site_means=False, record_spins_every=None):
    """Picklable worker: rebuilds a model from raw arrays and runs run_mc at one T."""
    J = sp.csr_matrix((J_data, J_indices, J_indptr), shape=J_shape)
    rng = np.random.default_rng(seed)
    spins0 = rng.choice(np.array([-1, 1], dtype=np.int8), size=J_shape[0])
    model = IsingModel(J, h, spins=spins0, rng=rng)
    return run_mc(model, T, n_equil, n_sweeps, dynamics, measure_every, rng,
                  record_site_means=record_site_means,
                  record_spins_every=record_spins_every)


def temperature_scan(J: sp.spmatrix, h: np.ndarray, temperatures: Sequence[float],
                      n_equil: int = 200, n_sweeps: int = 200, dynamics: str = "glauber",
                      measure_every: int = 1, seed: int | None = None,
                      n_jobs: int = 1, record_site_means: bool = False,
                      record_spins_every: int | None = None) -> list[dict]:
    """Run an independent MC simulation at each temperature.

    Each temperature starts from a fresh random configuration (standard for
    estimating equilibrium observables / phase diagrams, as opposed to annealing).
    Set n_jobs > 1 to parallelize across temperatures with local processes; the
    same worker signature maps directly onto an HPC job array (one T per task).
    """
    J = J.tocsr()
    h = np.asarray(h, dtype=np.float64)
    seeds = [None if seed is None else seed + i for i in range(len(temperatures))]

    if n_jobs == 1:
        results = []
        for T, s in zip(temperatures, seeds):
            results.append(_run_single_temperature(
                J.data, J.indices, J.indptr, J.shape, h, T,
                n_equil, n_sweeps, dynamics, measure_every, s, record_site_means,
                record_spins_every))
        return results

    with ProcessPoolExecutor(max_workers=n_jobs) as pool:
        futures = [
            pool.submit(_run_single_temperature, J.data, J.indices, J.indptr, J.shape,
                        h, T, n_equil, n_sweeps, dynamics, measure_every, s, record_site_means,
                        record_spins_every)
            for T, s in zip(temperatures, seeds)
        ]
        return [f.result() for f in futures]


def pooled_temperature_scan(J: sp.spmatrix, h: np.ndarray, temperatures: Sequence[float],
                             n_seeds: int, n_equil: int = 200, n_sweeps: int = 200,
                             dynamics: str = "glauber", measure_every: int = 1,
                             seed: int | None = None, n_jobs: int = 1,
                             seed_stride: int = 10_000) -> list[dict]:
    """Run n_seeds independent temperature_scan replicates and pool them per-T.

    A single seed's energy/magnetization series at one T is already noisy with
    only a few hundred measurement sweeps -- especially for derived variances
    like specific heat/susceptibility, which need more samples than a plain
    mean to converge. Pooling energies/magnetizations across n_seeds
    independent chains before computing those observables is equivalent to
    n_seeds times as many (decorrelated-across-chains) samples, which is what
    actually reduces the noise; rerunning one chain longer only helps up to
    its own autocorrelation time.

    Caveat this pooling can expose that a single seed hides: at low T,
    independent chains can each freeze into a *different* metastable domain
    configuration rather than all finding the same one within n_sweeps.
    Pooling then mixes genuine thermal fluctuation with between-chain
    disagreement, and susceptibility/specific heat both divide by T -- so as
    T -> 0 that disagreement can get amplified into a spurious divergence at
    the low-T edge of the scan rather than a real thermodynamic peak. A real
    critical point is an interior bump in the pooled curve, not a monotonic
    blow-up toward T=0.

    Returns one dict per temperature: {"T", "energy" (concatenated across
    seeds), "magnetization" (concatenated across seeds), "final_spins_per_seed"
    (list of n_seeds arrays, e.g. for averaging an empirical-alignment score
    across seeds rather than pooling it -- it's one score per configuration,
    not a per-sweep series)}.
    """
    replicates = [
        temperature_scan(J, h, temperatures, n_equil=n_equil, n_sweeps=n_sweeps,
                          dynamics=dynamics, measure_every=measure_every,
                          seed=None if seed is None else seed + k * seed_stride,
                          n_jobs=n_jobs)
        for k in range(n_seeds)
    ]
    pooled = []
    for i, T in enumerate(temperatures):
        pooled.append({
            "T": T,
            "energy": np.concatenate([r[i]["energy"] for r in replicates]),
            "magnetization": np.concatenate([r[i]["magnetization"] for r in replicates]),
            "final_spins_per_seed": [r[i]["final_spins"] for r in replicates],
        })
    return pooled
