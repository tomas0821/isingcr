"""Parse Tribunal Supremo de Elecciones (TSE, Costa Rica) results files.

TSE publishes results as CSV/XLSX at https://www.tse.go.cr (e.g. the vr2026
results portal, or the historical "elecciones en cifras" compendia). Exact
column names shift release to release, so this loader auto-detects the common
geographic-code/name columns and treats everything else numeric as a party
vote column; pass the *_col arguments explicitly when auto-detection is wrong
for a given file.

Expected shape after loading: one row per geographic unit (canton or distrito)
with a code column, a name column, and one numeric column per party/list.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pandas as pd

# Geography columns used by TSE's per-junta "consolidado" exports (2018/2022/2026
# "juntas" ZIPs), keyed by aggregation level. 2018 files use "distrito_electoral"
# instead of "distrito" -- load_tse_juntas_consolidado renames it on load.
_JUNTAS_GEO_COLS = {
    "provincia": ["provincia_pais"],
    "canton": ["provincia_pais", "canton_ciudad"],
    "distrito": ["provincia_pais", "canton_ciudad", "distrito"],
}

# Column name fragments (lowercased) TSE files commonly use for geography.
_CODE_HINTS = ("cod_canton", "cod_distrito", "codigo", "cod_")
_NAME_HINTS = {"canton": ("canton",), "distrito": ("distrito",)}
_NON_PARTY_HINTS = ("provincia", "canton", "distrito", "codigo", "cod_", "total", "padron",
                    "votos_recibidos", "junta", "mesa")


def _read_any(path: str | Path, encoding: str = "latin-1") -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path)
    for enc in (encoding, "utf-8", "cp1252"):
        try:
            return pd.read_csv(path, encoding=enc, sep=None, engine="python")
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Could not decode {path} with any of the tried encodings")


def _detect_column(columns: list[str], hints: tuple[str, ...],
                    exclude: tuple[str, ...] = ()) -> str | None:
    lower = {c: c.lower() for c in columns if c not in exclude}
    for col, low in lower.items():
        if any(hint in low for hint in hints):
            return col
    return None


def load_tse_results(path: str | Path, level: str = "canton", code_col: str | None = None,
                      name_col: str | None = None, party_cols: list[str] | None = None,
                      encoding: str = "latin-1") -> pd.DataFrame:
    """Load a raw TSE results file and identify geography/party columns.

    Parameters
    ----------
    path : path to a TSE .csv/.xlsx results file.
    level : "canton" or "distrito" -- used only for auto-detecting the name column.
    code_col, name_col, party_cols : override auto-detection when the file's
        headers don't match the common TSE naming patterns.

    Returns
    -------
    DataFrame with columns [code, name, <party columns...>].
    """
    df = _read_any(path, encoding=encoding)
    columns = list(df.columns)

    code_col = code_col or _detect_column(columns, _CODE_HINTS)
    name_col = name_col or _detect_column(
        columns, _NAME_HINTS.get(level, ("canton",)),
        exclude=(code_col,) if code_col else (),
    )
    if code_col is None or name_col is None:
        raise ValueError(
            f"Could not auto-detect geography columns in {path}. "
            f"Found columns: {columns}. Pass code_col/name_col explicitly."
        )

    if party_cols is None:
        non_party = {code_col.lower(), name_col.lower()}
        party_cols = [
            c for c in columns
            if c.lower() not in non_party
            and not any(hint in c.lower() for hint in _NON_PARTY_HINTS)
            and pd.api.types.is_numeric_dtype(df[c])
        ]
        if not party_cols:
            raise ValueError(
                f"Could not auto-detect party vote columns in {path}. "
                f"Found columns: {columns}. Pass party_cols explicitly."
            )

    out = df[[code_col, name_col, *party_cols]].rename(
        columns={code_col: "code", name_col: "name"}
    )
    out["code"] = out["code"].astype(str).str.strip()
    for c in party_cols:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)
    return out


def aggregate_to_level(df: pd.DataFrame, group_cols: list[str], party_cols: list[str]) -> pd.DataFrame:
    """Sum finer-grained results (e.g. per polling station) up to canton/distrito level."""
    return df.groupby(group_cols, as_index=False)[party_cols].sum()


def load_tse_juntas_consolidado(zip_path: str | Path, member: str | None = None,
                                 level: str = "canton", encoding: str = "utf-8",
                                 territorio: str | None = "NACIONAL") -> pd.DataFrame:
    """Load a TSE per-junta ("juntas receptoras de votos") results ZIP export.

    These are the official TSE "resultados por junta" exports (2018, 2022, 2026
    presidential elections), one CSV row per (junta, partido) with columns
    including provincia_pais/canton_ciudad/distrito/partido/votos. Each ZIP also
    bundles a pre-aggregated `_consolidado_*.csv` member covering every junta in
    one file (thousands of per-junta CSVs otherwise) -- this loads that member and
    aggregates it up to the requested geographic level, pivoting parties into columns.

    Parameters
    ----------
    zip_path : path to the TSE "juntas" ZIP file.
    member : name of the consolidado CSV inside the zip (e.g.
        "_consolidado_presidenciales.csv", or "ronda1/_consolidado_presidenciales.csv"
        for the 2018 ZIP, which nests results under ronda1/ronda2). Auto-detected
        when the zip contains exactly one file matching "_consolidado*"; several
        TSE ZIPs bundle more than one (e.g. presidenciales + diputaciones, or
        provisional + definitivo) and require picking one explicitly.
    level : "provincia", "canton", or "distrito" -- level to aggregate juntas up to.
        Note 2018 files use that year's "distrito electoral" (finer-grained, TSE's
        own reporting unit that year) rather than the administrative distrito used
        in 2022/2026 -- see that ZIP's LEEME.txt.
    territorio : filter to this "tipo_territorio" value before aggregating (default
        "NACIONAL", which is what leaves exactly the 84 real cantons -- juntas
        abroad are reported under tipo_territorio="EXTRANJERO" with foreign city
        names in canton_ciudad, which have no geographic adjacency and would
        corrupt the coupling graph if left in). Pass None to keep every row.

    Returns
    -------
    DataFrame with columns [code, name, <geography columns>, <party columns...>].
    `code` is a "|"-joined compound key (province|canton[|distrito]) since e.g.
    distrito names like "CENTRAL" repeat across many cantons and aren't unique
    on their own.
    """
    if level not in _JUNTAS_GEO_COLS:
        raise ValueError(f"level must be one of {list(_JUNTAS_GEO_COLS)}, got {level!r}")
    group_cols = _JUNTAS_GEO_COLS[level]

    with zipfile.ZipFile(zip_path) as zf:
        if member is None:
            candidates = [n for n in zf.namelist() if Path(n).name.startswith("_consolidado")]
            if len(candidates) != 1:
                raise ValueError(
                    f"Expected exactly one '_consolidado*' member in {zip_path}, "
                    f"found {candidates or 'none'}. Pass member= explicitly."
                )
            member = candidates[0]
        with zf.open(member) as f:
            df = pd.read_csv(io.TextIOWrapper(f, encoding=encoding))

    df = df.rename(columns={"distrito_electoral": "distrito"})
    for c in ("provincia_pais", "canton_ciudad", "distrito"):
        if c in df.columns:
            df[c] = df[c].str.strip()  # at least one real TSE row has a stray leading space
    missing = [c for c in (*group_cols, "partido", "votos") if c not in df.columns]
    if missing:
        raise ValueError(
            f"{zip_path}::{member} is missing expected column(s) {missing}. "
            f"Found: {list(df.columns)}"
        )

    if territorio is not None:
        if "tipo_territorio" not in df.columns:
            raise ValueError(
                f"{zip_path}::{member} has no 'tipo_territorio' column to filter on. "
                f"Pass territorio=None to skip filtering."
            )
        df = df[df["tipo_territorio"] == territorio]
        if df.empty:
            raise ValueError(
                f"No rows with tipo_territorio={territorio!r} in {zip_path}::{member}."
            )

    agg = df.groupby([*group_cols, "partido"], as_index=False)["votos"].sum()
    wide = agg.pivot_table(index=group_cols, columns="partido", values="votos",
                            fill_value=0, aggfunc="sum").reset_index()
    wide.columns.name = None

    wide["code"] = wide[group_cols].astype(str).agg("|".join, axis=1)
    wide["name"] = wide[group_cols[-1]]
    party_cols = [c for c in wide.columns if c not in (*group_cols, "code", "name")]
    return wide[["code", "name", *group_cols, *party_cols]]
