from isingcr.ingestion.canton_names import normalize_canton_code, normalize_distrito_code


def test_normal_canton_unaffected():
    assert normalize_canton_code("Alajuela", "Atenas") == "ALAJUELA|ATENAS"


def test_accents_stripped():
    assert normalize_canton_code("San Jose", "Aserrí") == "SAN JOSE|ASERRI"
    assert normalize_canton_code("Heredia", "Belén") == "HEREDIA|BELEN"


def test_ntilde_preserved_not_folded_to_n():
    # TSE keeps enye as a distinct letter (unlike acute accents) -- see Cañas.
    assert normalize_canton_code("Guanacaste", "Cañas") == "GUANACASTE|CAÑAS"


def test_province_capital_canton_folds_to_central():
    assert normalize_canton_code("San Jose", "San Jose") == "SAN JOSE|CENTRAL"
    assert normalize_canton_code("Puntarenas", "Puntarenas") == "PUNTARENAS|CENTRAL"


def test_matches_tse_code_format_for_all_six_province_capitals():
    provinces = ["San Jose", "Alajuela", "Cartago", "Heredia", "Puntarenas", "Limon"]
    for p in provinces:
        assert normalize_canton_code(p, p) == f"{p.upper()}|CENTRAL"


def test_distrito_code_normal_case():
    assert normalize_distrito_code("Alajuela", "Atenas", "Atenas") == "ALAJUELA|ATENAS|ATENAS"


def test_distrito_code_folds_province_capital_canton():
    # Shapefile admin3 names a province-capital canton's distrito 1 after the
    # canton itself; TSE's canton_ciudad is "CENTRAL" regardless of distrito name.
    assert (normalize_distrito_code("Alajuela", "Alajuela", "Carrizal")
            == "ALAJUELA|CENTRAL|CARRIZAL")


def test_distrito_code_strips_accents_and_preserves_ntilde():
    assert (normalize_distrito_code("Guanacaste", "Cañas", "Bebedero")
            == "GUANACASTE|CAÑAS|BEBEDERO")
