"""Reduce multi-party vote tables to the binary spin states the Ising model needs."""

from __future__ import annotations

import numpy as np
import pandas as pd


def binarize_votes(df: pd.DataFrame, group_a: list[str], group_b: list[str],
                    code_col: str = "code") -> pd.DataFrame:
    """Assign spin +1/-1 per geographic unit by combined-vote majority between two macro-groups.

    Parameters
    ----------
    df : output of `load_tse_results` (one row per geographic unit, one column per party).
    group_a : party columns to sum as the +1 macro-state (e.g. traditional parties).
    group_b : party columns to sum as the -1 macro-state (e.g. emerging coalitions).
    code_col : geographic unit identifier column.

    Returns
    -------
    DataFrame with [code, spin, margin], where margin = (votes_a - votes_b) / (votes_a + votes_b)
    in [-1, 1] -- a natural candidate for deriving a local external field h_i.
    """
    votes_a = df[group_a].sum(axis=1)
    votes_b = df[group_b].sum(axis=1)
    total = votes_a + votes_b
    spin = np.where(votes_a >= votes_b, 1, -1).astype(np.int8)
    margin = np.divide(votes_a - votes_b, total, out=np.zeros_like(total, dtype=float), where=total > 0)
    return pd.DataFrame({code_col: df[code_col].values, "spin": spin, "margin": margin})
