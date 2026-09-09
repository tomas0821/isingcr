import zipfile

import pytest

from isingcr.ingestion.tse_parser import load_tse_juntas_consolidado

_HEADER = ("eleccion,fuente,tipo_territorio,provincia_pais,canton_ciudad,distrito,junta,"
           "electores_inscritos,votos_validos,votos_nulos,votos_en_blanco,"
           "total_votos_recibidos,papeletas_sobrantes,partido,votos,porcentaje_validos")

_ROWS = [
    'PRESIDENCIALES,DEF,NACIONAL,SAN JOSE,CENTRAL,CARMEN,1,100,90,1,0,91,9,PARTIDO A,60,66.7',
    'PRESIDENCIALES,DEF,NACIONAL,SAN JOSE,CENTRAL,CARMEN,1,100,90,1,0,91,9,PARTIDO B,30,33.3',
    'PRESIDENCIALES,DEF,NACIONAL,SAN JOSE,CENTRAL,MERCED,2,80,70,0,0,70,10,PARTIDO A,20,28.6',
    'PRESIDENCIALES,DEF,NACIONAL,SAN JOSE,CENTRAL,MERCED,2,80,70,0,0,70,10,PARTIDO B,50,71.4',
    'PRESIDENCIALES,DEF,NACIONAL,ALAJUELA,CENTRAL,ALAJUELA,3,50,40,0,0,40,10,PARTIDO A,35,87.5',
    'PRESIDENCIALES,DEF,NACIONAL,ALAJUELA,CENTRAL,ALAJUELA,3,50,40,0,0,40,10,PARTIDO B,5,12.5',
    'PRESIDENCIALES,DEF,EXTRANJERO,ESTADOS UNIDOS,MIAMI,MIAMI,4,20,15,0,0,15,5,PARTIDO A,10,66.7',
    'PRESIDENCIALES,DEF,EXTRANJERO,ESTADOS UNIDOS,MIAMI,MIAMI,4,20,15,0,0,15,5,PARTIDO B,5,33.3',
]


def _make_zip(tmp_path, member="_consolidado_presidenciales.csv", extra_members=()):
    zip_path = tmp_path / "juntas.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(member, _HEADER + "\n" + "\n".join(_ROWS))
        for name in extra_members:
            zf.writestr(name, _HEADER + "\n" + _ROWS[0])
    return zip_path


def test_load_juntas_canton_level_aggregates_and_pivots(tmp_path):
    zip_path = _make_zip(tmp_path)
    out = load_tse_juntas_consolidado(zip_path, level="canton")

    assert set(out["name"]) == {"CENTRAL"}  # SJ-Central and Alajuela-Central both named "CENTRAL"
    assert len(out) == 2  # but SAN JOSE|CENTRAL and ALAJUELA|CENTRAL are distinct cantons
    sj_row = out[out["code"] == "SAN JOSE|CENTRAL"].iloc[0]
    assert sj_row["PARTIDO A"] == 80   # 60 (CARMEN) + 20 (MERCED)
    assert sj_row["PARTIDO B"] == 80   # 30 + 50


def test_load_juntas_distrito_level_keeps_districts_separate(tmp_path):
    zip_path = _make_zip(tmp_path)
    out = load_tse_juntas_consolidado(zip_path, level="distrito")

    assert len(out) == 3  # CARMEN, MERCED, ALAJUELA-central are distinct distritos
    carmen = out[out["code"] == "SAN JOSE|CENTRAL|CARMEN"].iloc[0]
    assert carmen["PARTIDO A"] == 60
    assert carmen["PARTIDO B"] == 30


def test_load_juntas_auto_detects_single_consolidado_member(tmp_path):
    zip_path = _make_zip(tmp_path, member="_consolidado_presidenciales.csv")
    out = load_tse_juntas_consolidado(zip_path, level="provincia")
    assert set(out["code"]) == {"SAN JOSE", "ALAJUELA"}


def test_load_juntas_requires_explicit_member_when_ambiguous(tmp_path):
    zip_path = _make_zip(tmp_path, member="_consolidado_presidenciales.csv",
                          extra_members=["_consolidado_diputaciones.csv"])
    with pytest.raises(ValueError, match="found"):
        load_tse_juntas_consolidado(zip_path, level="canton")

    out = load_tse_juntas_consolidado(zip_path, member="_consolidado_presidenciales.csv",
                                       level="canton")
    assert len(out) == 2


def test_load_juntas_filters_to_nacional_by_default(tmp_path):
    zip_path = _make_zip(tmp_path)
    out = load_tse_juntas_consolidado(zip_path, level="provincia")
    assert set(out["code"]) == {"SAN JOSE", "ALAJUELA"}  # ESTADOS UNIDOS/EXTRANJERO excluded


def test_load_juntas_territorio_none_keeps_everything(tmp_path):
    zip_path = _make_zip(tmp_path)
    out = load_tse_juntas_consolidado(zip_path, level="provincia", territorio=None)
    assert set(out["code"]) == {"SAN JOSE", "ALAJUELA", "ESTADOS UNIDOS"}


def test_load_juntas_renames_2018_distrito_electoral_column(tmp_path):
    header = _HEADER.replace("distrito,", "distrito_electoral,")
    zip_path = tmp_path / "juntas2018.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("ronda1/_consolidado_presidenciales.csv", header + "\n" + "\n".join(_ROWS))
    out = load_tse_juntas_consolidado(zip_path, level="distrito")
    assert "SAN JOSE|CENTRAL|CARMEN" in set(out["code"])


def test_load_juntas_strips_stray_whitespace_in_geography_fields(tmp_path):
    # A real 2026 TSE row has a leading space in its distrito field (" LEGUA") --
    # confirmed against data/raw/tse_juntas/DEFINITIVO_juntas_TSE_2026.zip.
    rows = [r.replace("SAN JOSE,CENTRAL,CARMEN", "SAN JOSE,CENTRAL, CARMEN") for r in _ROWS]
    zip_path = tmp_path / "juntas_whitespace.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("_consolidado_presidenciales.csv", _HEADER + "\n" + "\n".join(rows))
    out = load_tse_juntas_consolidado(zip_path, level="distrito")
    assert "SAN JOSE|CENTRAL|CARMEN" in set(out["code"])
