import numpy as np

from isingcr.simulation.observables import (
    alignment_fraction,
    mcnemar_test,
    spatial_block_permutation_test,
    specific_heat,
    susceptibility,
    symmetric_alignment_fraction,
)


def test_specific_heat_zero_variance_is_zero():
    energies = np.full(50, -10.0)
    assert specific_heat(energies, T=1.0, N=10) == 0.0


def test_susceptibility_scales_with_variance():
    rng = np.random.default_rng(0)
    m = rng.normal(0, 0.1, size=1000)
    chi = susceptibility(m, T=1.0, N=100)
    assert chi > 0


def test_alignment_fraction():
    sim = np.array([1, 1, -1, -1])
    emp = np.array([1, -1, -1, -1])
    assert alignment_fraction(sim, emp) == 0.75


def test_symmetric_alignment_fraction_rescues_mirrored_run():
    sim = np.array([1, 1, -1, -1])
    emp = -sim  # exact mirror image: raw alignment is 0%, shape is perfectly right
    assert alignment_fraction(sim, emp) == 0.0
    assert symmetric_alignment_fraction(sim, emp) == 1.0


def test_symmetric_alignment_fraction_matches_raw_when_already_high():
    sim = np.array([1, 1, -1, -1])
    emp = np.array([1, -1, -1, -1])
    assert symmetric_alignment_fraction(sim, emp) == alignment_fraction(sim, emp)


def test_mcnemar_no_discordant_pairs_gives_pvalue_one():
    empirical = np.array([1, 1, -1, -1])
    model = empirical.copy()
    null = empirical.copy()
    result = mcnemar_test(model, null, empirical)
    assert result["n12"] == 0
    assert result["n21"] == 0
    assert result["exact_pvalue"] == 1.0
    assert result["chi2_pvalue"] == 1.0


def test_mcnemar_model_strictly_better_than_null():
    # 7 majority (+1), 3 minority (-1); null always predicts majority.
    empirical = np.array([1, 1, 1, 1, 1, 1, 1, -1, -1, -1])
    null = np.ones(10, dtype=int)  # always predicts majority class
    model = empirical.copy()  # perfect classifier

    result = mcnemar_test(model, null, empirical)
    assert result["n12"] == 3  # model right, null wrong, on the 3 minority sites
    assert result["n21"] == 0  # model is never wrong where null is right
    assert result["n_discordant"] == 3
    assert result["exact_pvalue"] < 1.0


def test_mcnemar_identical_error_rates_gives_high_pvalue():
    empirical = np.array([1, 1, 1, -1, -1, -1])
    model = np.array([1, 1, -1, -1, -1, 1])   # wrong on indices 2, 5
    null = np.array([1, -1, 1, -1, 1, -1])    # wrong on indices 1, 4
    result = mcnemar_test(model, null, empirical)
    assert result["n12"] == result["n21"] == 2
    assert result["exact_pvalue"] == 1.0


def test_spatial_block_permutation_no_difference_gives_pvalue_one():
    empirical = np.array([1, 1, -1, -1])
    model = np.array([1, 1, 1, 1])  # same predictions as the majority-class null
    blocks = np.array([0, 1, 2, 3])  # singleton blocks
    rng = np.random.default_rng(0)
    result = spatial_block_permutation_test(model, empirical, majority_label=1,
                                             blocks=blocks, n_permutations=200, rng=rng)
    assert result["observed_statistic"] == 0.0
    assert result["p_value"] == 1.0
    assert result["n_blocks"] == 4


def test_spatial_block_permutation_singleton_blocks_detects_strong_effect():
    # Large, spatially spread-out advantage (own block per unit) should be
    # detectable, much like mcnemar_test would find on the same data.
    n = 40
    empirical = np.array([1] * 30 + [-1] * 10)
    null_always_majority = np.ones(n, dtype=int)
    model = empirical.copy()  # perfect on the 10 minority sites null gets wrong
    blocks = np.arange(n)  # every unit its own block -- no spatial pooling needed
    rng = np.random.default_rng(1)
    result = spatial_block_permutation_test(model, empirical, majority_label=1,
                                             blocks=blocks, n_permutations=999, rng=rng)
    mc = mcnemar_test(model, null_always_majority, empirical)
    assert result["observed_statistic"] == mc["n12"] - mc["n21"]
    assert result["p_value"] < 0.05


def test_spatial_block_permutation_penalizes_clustered_discordance():
    # Same total discordant-pair count and direction as the singleton-block
    # case above, but every discordant unit is crammed into a single spatial
    # block -- exactly the scenario mcnemar_test's independence assumption
    # mishandles. The block test should be far less confident than mcnemar's
    # naive per-unit p-value on the same data.
    n = 40
    empirical = np.array([1] * 30 + [-1] * 10)
    null_always_majority = np.ones(n, dtype=int)
    model = empirical.copy()
    blocks = np.array([0] * 10 + list(range(1, 31)))  # all 10 minority sites: one block
    rng = np.random.default_rng(2)
    result = spatial_block_permutation_test(model, empirical, majority_label=1,
                                             blocks=blocks, n_permutations=999, rng=rng)
    mc = mcnemar_test(model, null_always_majority, empirical)
    assert result["n_blocks"] == 31
    assert mc["exact_pvalue"] < 0.05
    assert result["p_value"] > mc["exact_pvalue"]
