import pandas as pd

from isingcr.ingestion.tse_parser import aggregate_to_level, load_tse_results


def test_load_tse_results_autodetects_columns(tmp_path):
    csv_path = tmp_path / "results.csv"
    df = pd.DataFrame({
        "PROVINCIA": ["San Jose", "San Jose"],
        "COD_CANTON": ["101", "102"],
        "CANTON": ["San Jose", "Escazu"],
        "PLN": [1000, 500],
        "PUSC": [200, 100],
        "PPSD": [300, 900],
    })
    df.to_csv(csv_path, index=False, encoding="latin-1")

    out = load_tse_results(csv_path, level="canton")
    assert list(out["code"]) == ["101", "102"]
    assert list(out["name"]) == ["San Jose", "Escazu"]
    assert set(["PLN", "PUSC", "PPSD"]).issubset(out.columns)
    assert "PROVINCIA" not in out.columns


def test_aggregate_to_level_sums_finer_grain():
    df = pd.DataFrame({
        "COD_CANTON": ["101", "101", "102"],
        "PLN": [10, 20, 5],
        "PPSD": [1, 2, 3],
    })
    out = aggregate_to_level(df, group_cols=["COD_CANTON"], party_cols=["PLN", "PPSD"])
    row = out[out["COD_CANTON"] == "101"].iloc[0]
    assert row["PLN"] == 30
    assert row["PPSD"] == 3
