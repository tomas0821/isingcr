"""Reconcile canton naming between TSE results and third-party boundary files.

Two independent naming quirks otherwise break a plain province+canton join:

1. Costa Rica names each province's capital canton after the province itself
   (e.g. canton "San Jose" in province "San Jose"), but TSE's per-junta exports
   report that same canton as canton_ciudad="CENTRAL" -- one mismatch per
   province, 6 total.
2. TSE's exports strip acute accents (TILARAN, ASERRI) but keep "N" with
   tilde as a distinct letter (CANAS, i.e. "Cañas") rather than folding it to
   plain N -- unlike ordinary accent-stripping (e.g. Unicode NFKD + ASCII
   encode, which decomposes N-with-tilde into N same as it does A-with-acute),
   so a generic accent-stripper needs to special-case it to match TSE.
"""

from __future__ import annotations

import unicodedata

_NTILDE_PLACEHOLDER = "\x00"


def _strip_accents(s: str) -> str:
    # Protect N-with-tilde from NFKD decomposition (see module docstring point 2)
    s = s.replace("Ñ", _NTILDE_PLACEHOLDER).replace("ñ", _NTILDE_PLACEHOLDER)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.replace(_NTILDE_PLACEHOLDER, "Ñ")
    return s.upper().strip()


def normalize_canton_code(province: str, canton: str) -> str:
    """Build a "PROVINCE|CANTON" key matching `load_tse_juntas_consolidado`'s `code`.

    Strips accents/case and folds a province-capital canton (named after its
    province, e.g. shapefile canton "San Jose") to "CENTRAL" (TSE's name for
    the same canton), so TSE codes and third-party boundary-file codes agree.
    """
    province = _strip_accents(province)
    canton = _strip_accents(canton)
    if canton == province:
        canton = "CENTRAL"
    return f"{province}|{canton}"


def normalize_distrito_code(province: str, canton: str, distrito: str) -> str:
    """Build a "PROVINCE|CANTON|DISTRITO" key matching
    `load_tse_juntas_consolidado(..., level="distrito")`'s `code`.

    The province-capital-canton quirk `normalize_canton_code` handles recurs
    identically one level down: a boundary file's admin3 (distrito) layer
    names a canton's first distrito after the canton itself when TSE's export
    calls that same canton "CENTRAL" (e.g. shapefile canton "Alajuela" ->
    TSE canton_ciudad "CENTRAL", independent of the distrito's own name, which
    matches directly -- confirmed against the 2026 TSE distrito export: 430/492
    distritos match on a naive join, all 62 mismatches are this exact pattern
    on the canton component, none on the distrito name itself).
    """
    canton_code = normalize_canton_code(province, canton)
    distrito = _strip_accents(distrito)
    return f"{canton_code}|{distrito}"
