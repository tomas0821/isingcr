"""Phase-transition diagnostics: magnetization, specific heat, susceptibility vs T."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ..simulation.observables import alignment_fraction, specific_heat, susceptibility


def plot_phase_diagram(scan_results: list[dict], N: int, savepath: str | Path | None = None):
    """3-panel figure: |m|(T), specific heat C(T), susceptibility chi(T)."""
    import matplotlib.pyplot as plt

    T = np.array([r["T"] for r in scan_results])
    m = np.array([np.mean(np.abs(r["magnetization"])) for r in scan_results])
    C = np.array([specific_heat(r["energy"], r["T"], N) for r in scan_results])
    chi = np.array([susceptibility(r["magnetization"], r["T"], N) for r in scan_results])

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(T, m, "o-")
    axes[0].set_xlabel("Temperature T")
    axes[0].set_ylabel(r"$\langle |m| \rangle$")
    axes[0].set_title("Magnetization")

    axes[1].plot(T, C, "o-", color="tab:red")
    axes[1].set_xlabel("Temperature T")
    axes[1].set_ylabel("Specific heat C")
    axes[1].set_title("Specific heat")
    if len(T) and np.any(np.isfinite(C)):
        t_peak = T[np.nanargmax(C)]
        axes[1].axvline(t_peak, color="gray", linestyle="--", linewidth=1)

    axes[2].plot(T, chi, "o-", color="tab:green")
    axes[2].set_xlabel("Temperature T")
    axes[2].set_ylabel(r"Susceptibility $\chi$")
    axes[2].set_title("Magnetic susceptibility")
    if len(T) and np.any(np.isfinite(chi)):
        t_peak = T[np.nanargmax(chi)]
        axes[2].axvline(t_peak, color="gray", linestyle="--", linewidth=1)

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=150)
    return fig


def plot_alignment_curve(scan_results: list[dict], empirical_spins: np.ndarray,
                          savepath: str | Path | None = None):
    """Fraction of nodes where simulated equilibrium spin matches TSE ground truth, vs T.

    The peak of this curve is the "critical social temperature" from the spec:
    the point where the simulated network best reproduces the empirical map.
    """
    import matplotlib.pyplot as plt

    T = np.array([r["T"] for r in scan_results])
    accuracy = np.array([
        alignment_fraction(r["final_spins"], empirical_spins) for r in scan_results
    ])

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(T, accuracy, "o-", color="tab:purple")
    ax.axhline(0.5, color="gray", linestyle=":", linewidth=1, label="chance level")
    if len(T):
        t_best = T[np.argmax(accuracy)]
        ax.axvline(t_best, color="gray", linestyle="--", linewidth=1,
                    label=f"best match T={t_best:.3g}")
    ax.set_xlabel("Temperature T")
    ax.set_ylabel("Fraction matching empirical map")
    ax.set_title("Alignment with TSE ground truth vs. social temperature")
    ax.legend()
    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=150)
    return fig
