"""Thermodynamic observables derived from MC time series."""

from __future__ import annotations

import numpy as np
from scipy import stats as _stats


def specific_heat(energies: np.ndarray, T: float, N: int) -> float:
    """C = Var(E) / (N * T^2)."""
    if T <= 0:
        return float("nan")
    return float(np.var(energies) / (N * T**2))


def susceptibility(magnetizations: np.ndarray, T: float, N: int) -> float:
    """chi = N * Var(m) / T, where m = M/N is the per-site magnetization."""
    if T <= 0:
        return float("nan")
    return float(N * np.var(magnetizations) / T)


def binder_cumulant(magnetizations: np.ndarray) -> float:
    """U4 = 1 - <m^4> / (3 <m^2>^2); crosses model-size-independent point at T_c."""
    m2 = np.mean(magnetizations**2)
    m4 = np.mean(magnetizations**4)
    if m2 == 0:
        return float("nan")
    return float(1.0 - m4 / (3.0 * m2**2))


def alignment_fraction(simulated_spins: np.ndarray, empirical_spins: np.ndarray) -> float:
    """Fraction of sites where simulated equilibrium spin matches empirical vote spin."""
    return float(np.mean(simulated_spins == empirical_spins))


def mcnemar_test(model_spins: np.ndarray, null_spins: np.ndarray,
                  empirical_spins: np.ndarray) -> dict:
    """Paired significance test: does `model_spins` classify sites significantly
    better than `null_spins` against the same ground truth?

    `null_spins` is typically a constant array (the majority-class prediction) --
    the same baseline used elsewhere in this project's scripts, now compared
    rigorously instead of by eyeballing whether accuracy clears it. This mirrors
    Korbel, Dahdoul & Thurner's own validation methodology for an Ising-type
    election model (PRL, arXiv:2510.00612 -- see NOVELTY_CHECK.md): they compare
    their fitted model against a null model via McNemar's test on the same kind
    of paired correct/incorrect classification table.

    Only the discordant pairs matter: n12 = model right & null wrong, n21 = model
    wrong & null right. Returns both the standard continuity-corrected chi-square
    approximation and the exact binomial form -- prefer `exact_pvalue` whenever
    n12 + n21 is small (a near-certainty at canton scale, N~84; Korbel et al. use
    the chi-square form because their n12+n21 is in the thousands).
    """
    model_correct = model_spins == empirical_spins
    null_correct = null_spins == empirical_spins
    n12 = int(np.sum(model_correct & ~null_correct))
    n21 = int(np.sum(~model_correct & null_correct))
    n_discordant = n12 + n21

    if n_discordant == 0:
        return {"n12": n12, "n21": n21, "n_discordant": 0,
                "chi2": 0.0, "chi2_pvalue": 1.0, "exact_pvalue": 1.0}

    chi2 = (abs(n12 - n21) - 1) ** 2 / n_discordant
    chi2_pvalue = float(_stats.chi2.sf(chi2, df=1))
    exact_pvalue = float(_stats.binomtest(min(n12, n21), n_discordant, 0.5).pvalue)
    return {"n12": n12, "n21": n21, "n_discordant": n_discordant,
            "chi2": float(chi2), "chi2_pvalue": chi2_pvalue, "exact_pvalue": exact_pvalue}


def mcnemar_seed_summary(final_spins_per_seed: list, empirical_spins: np.ndarray,
                          majority_label: int) -> dict:
    """Run `mcnemar_test` (model vs. constant majority-class null) once per seed's
    final configuration and summarize across seeds, rather than trusting any one
    seed -- this project's standing rule (see CLAUDE.md gotcha #7).

    Each seed's spins are sign-aligned to whichever orientation matches
    `empirical_spins` better before testing (see `symmetric_alignment_fraction`'s
    docstring on why a raw comparison can be spuriously bad for an exact mirror
    image when h is zero or weak).
    """
    null = np.full_like(empirical_spins, majority_label)
    results = []
    for s in final_spins_per_seed:
        s_aligned = s if alignment_fraction(s, empirical_spins) >= 0.5 else -s
        results.append(mcnemar_test(s_aligned, null, empirical_spins))

    exact_p = [r["exact_pvalue"] for r in results]
    return {
        "median_exact_pvalue": float(np.median(exact_p)),
        "fraction_significant_at_0.05": float(np.mean(np.array(exact_p) < 0.05)),
        "n_seeds": len(results),
        "per_seed": results,
    }


def spatial_block_permutation_test(model_spins: np.ndarray, empirical_spins: np.ndarray,
                                    majority_label: int, blocks: np.ndarray,
                                    n_permutations: int = 999,
                                    rng: np.random.Generator | None = None) -> dict:
    """Sign-flip block-permutation test: a spatially-aware alternative to
    `mcnemar_test` for the same model-vs-majority-baseline comparison.

    `mcnemar_test` assumes each unit's discordant/concordant outcome is an
    independent draw, which is false whenever nearby units are spatially
    autocorrelated (as this project's own Moran's I results confirm they
    are, see `investigate_2018_anomaly.py`/the manuscript's Observables
    section) -- that inflates significance (p-values too small). This test
    instead only randomizes at the level of spatial blocks (e.g. each
    distrito's parent canton, or each canton's parent province), which
    respects local spatial structure: units within one block move together
    under the null rather than independently.

    Parameters
    ----------
    blocks : array-like of length N, one group label per unit (same order as
        model_spins/empirical_spins), e.g. derived from a "PROVINCE|CANTON"
        or "PROVINCE|CANTON|DISTRITO" node code's leading components.

    Returns a dict with the observed signed discordant-pair statistic
    (n12 - n21, matching `mcnemar_test`'s n12/n21 convention), the number of
    blocks (sets the coarsest achievable p-value resolution, 2/2^n_blocks),
    and a two-sided permutation p-value.
    """
    null_pred = np.full_like(empirical_spins, majority_label)
    return _spatial_block_permutation(plus_spins=model_spins, minus_spins=null_pred,
                                       empirical_spins=empirical_spins, blocks=blocks,
                                       n_permutations=n_permutations, rng=rng)


def spatial_block_permutation_test_paired(spins_a: np.ndarray, spins_b: np.ndarray,
                                           empirical_spins: np.ndarray, blocks: np.ndarray,
                                           n_permutations: int = 999,
                                           rng: np.random.Generator | None = None) -> dict:
    """Like `spatial_block_permutation_test`, but compares two fitted models'
    predictions directly against each other instead of one model against a
    constant majority-class baseline.

    Every significance test elsewhere in this project (McNemar or
    spatial-block) compares a single model's predictions to the trivial
    majority baseline; none directly tests whether two models (e.g. h=0 vs.
    h=margin) differ from *each other*. This is that direct paired test:
    positive `observed_statistic` means `spins_b` matches the empirical map
    on more units than `spins_a` does, among the units where exactly one of
    the two is right.
    """
    return _spatial_block_permutation(plus_spins=spins_b, minus_spins=spins_a,
                                       empirical_spins=empirical_spins, blocks=blocks,
                                       n_permutations=n_permutations, rng=rng)


def _spatial_block_permutation(plus_spins, minus_spins, empirical_spins, blocks,
                                n_permutations, rng):
    """observed_statistic > 0 means plus_spins matches empirical_spins more
    often than minus_spins does, among the units where exactly one is right."""
    rng = rng if rng is not None else np.random.default_rng()
    signed = (plus_spins == empirical_spins).astype(int) - (minus_spins == empirical_spins).astype(int)

    blocks = np.asarray(blocks)
    unique_blocks = np.unique(blocks)
    n_blocks = len(unique_blocks)
    block_sums = np.array([signed[blocks == b].sum() for b in unique_blocks])
    observed = float(block_sums.sum())

    flips = rng.choice(np.array([-1, 1]), size=(n_permutations, n_blocks))
    null_stats = flips @ block_sums
    p_value = float(np.mean(np.abs(null_stats) >= abs(observed)))

    return {
        "n_blocks": n_blocks, "observed_statistic": observed,
        "p_value": p_value, "n_permutations": n_permutations,
    }


def symmetric_alignment_fraction(simulated_spins: np.ndarray, empirical_spins: np.ndarray) -> float:
    """Z2-safe alignment: max(match fraction, 1 - match fraction).

    With h=0 (or h weak relative to J) the model's up/down symmetry makes the
    sign of a low-T ordered run arbitrary -- it may land on the empirical
    map's exact mirror image and score near 0% on `alignment_fraction` despite
    getting the *shape* of the clustering right. Use this instead whenever
    comparing runs where h is zero or negligible (e.g. a pure-geography
    ablation); it's a no-op difference from `alignment_fraction` whenever h is
    strong enough to reliably break the symmetry in the correct direction.
    """
    match = alignment_fraction(simulated_spins, empirical_spins)
    return max(match, 1.0 - match)
