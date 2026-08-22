"""Loader for MIDEPLAN's Indice de Desarrollo Social (IDS), distrito level.

Not yet wired to a real MIDEPLAN export -- as of 2026-08-20 no IDS CSV exists
under `data/raw/` (this project's raw-data conventions keep such files out of
version control; see `data/raw/.gitkeep`). This loader is written against
MIDEPLAN's published IDS schema (province/canton/distrito name columns plus a
0-100 score column) so that dropping the real 2023 file in place needs no
code changes, following `load_tse_results`'s auto-detect-but-never-silently-
guess convention (CLAUDE.md gotcha #4): a column that can't be found raises,
it is never assumed.
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from .canton_names import normalize_distrito_code

_PROVINCE_CANDIDATES = ["provincia", "province"]
_CANTON_CANDIDATES = ["canton", "cantón", "cod_canton_nombre"]
_DISTRITO_CANDIDATES = ["distrito", "district"]
_IDS_CANDIDATES = ["ids", "indice", "índice", "indice_desarrollo_social",
                   "indice de desarrollo social", "score"]


def _find_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand in lower:
            return lower[cand]
    return None


def load_mideplan_ids(path, province_col: str | None = None, canton_col: str | None = None,
                       distrito_col: str | None = None, ids_col: str | None = None) -> pd.DataFrame:
    """Load a MIDEPLAN IDS CSV and attach a normalized distrito `code`.

    Parameters
    ----------
    path : str or Path, relative to the caller (never hardcode an absolute
        path here -- callers pass e.g. `DATA_RAW / "mideplan_ids_2023.csv"`
        built from `Path(__file__)`, matching every other loader in this
        package).
    province_col, canton_col, distrito_col, ids_col : optional explicit
        column names. If omitted, auto-detected from common MIDEPLAN header
        variants; raises ValueError (not a silent guess) if a required
        column can't be found either way.

    Returns
    -------
    DataFrame with columns ["code", "ids_raw"], `code` in the same
    "PROVINCE|CANTON|DISTRITO" form `normalize_distrito_code` produces for
    the electoral graph, so it can be joined directly against that graph's
    node order.
    """
    df = pd.read_csv(path)

    province_col = province_col or _find_col(df, _PROVINCE_CANDIDATES)
    canton_col = canton_col or _find_col(df, _CANTON_CANDIDATES)
    distrito_col = distrito_col or _find_col(df, _DISTRITO_CANDIDATES)
    ids_col = ids_col or _find_col(df, _IDS_CANDIDATES)

    missing = [name for name, col in
               [("province", province_col), ("canton", canton_col),
                ("distrito", distrito_col), ("ids", ids_col)] if col is None]
    if missing:
        raise ValueError(
            f"Could not auto-detect MIDEPLAN IDS column(s) {missing} in {list(df.columns)}. "
            "Pass the explicit column name(s) rather than guessing.")

    out = pd.DataFrame({
        "code": [normalize_distrito_code(p, c, d)
                 for p, c, d in zip(df[province_col], df[canton_col], df[distrito_col])],
        "ids_raw": df[ids_col].astype(float),
    })
    return out


_AXIS_COLUMNS = ["salud", "participa", "seguridad", "educacion", "economico"]


def load_mideplan_ids_axes(path) -> pd.DataFrame:
    """Load MIDEPLAN's five IDS sub-dimensions (the composite's own inputs).

    Unlike `load_mideplan_ids`, no auto-detection: `path` is this project's
    own generated `mideplan_ids_2023.csv` (see scripts/parse_mideplan_ids.py),
    so the column names are fixed and known. Returns `code` (normalized
    "PROVINCE|CANTON|DISTRITO", joinable against the electoral graph exactly
    like `load_mideplan_ids`'s output) plus one `<axis>_raw` column per
    dimension, so `ids_zscore_by_code(df, nodes, ids_col="<axis>_raw")`
    works unchanged.
    """
    df = pd.read_csv(path)
    out = pd.DataFrame({
        "code": [normalize_distrito_code(p, c, d)
                 for p, c, d in zip(df["provincia"], df["canton"], df["distrito"])],
    })
    for axis in _AXIS_COLUMNS:
        out[f"{axis}_raw"] = df[axis].astype(float)
    return out


def ids_zscore_by_code(ids_df: pd.DataFrame, node_codes: list[str],
                        ids_col: str = "ids_raw") -> tuple[np.ndarray, int]:
    """Center+scale IDS scores into `h^soc`, aligned to `node_codes` order.

    A distrito's IDS score is a static 0-100 value with no natural zero, so
    (unlike the vote-margin field, which is already centered by construction)
    it needs explicit centering before it can act as a symmetric external
    field: h^soc = (ids - mean(ids)) / std(ids).

    Nodes in `node_codes` missing from `ids_df` get h^soc = 0 (a neutral
    field) rather than being dropped -- the caller's node ordering comes from
    the already-built adjacency graph and must stay fixed, or J/h_pol/h_soc
    would desync. Returns (h_soc, n_missing) so the caller can judge whether
    n_missing is small enough to trust, the same "don't silently drop nodes"
    posture as `build_electoral_graph`'s unmatched-node warning.
    """
    lookup = dict(zip(ids_df["code"], ids_df[ids_col]))
    raw = np.array([lookup.get(c, np.nan) for c in node_codes], dtype=np.float64)
    n_missing = int(np.isnan(raw).sum())

    mean = np.nanmean(raw)
    std = np.nanstd(raw)
    z = (raw - mean) / std if std > 0 else np.zeros_like(raw)
    z = np.nan_to_num(z, nan=0.0)
    return z, n_missing
