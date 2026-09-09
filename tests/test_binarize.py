import pandas as pd

from isingcr.ingestion.binarize import binarize_votes


def test_binarize_majority_and_margin():
    df = pd.DataFrame({
        "code": ["001", "002", "003"],
        "PLN": [100, 20, 50],
        "PUSC": [50, 10, 50],
        "PPSD": [30, 80, 30],
        "NR": [10, 40, 20],
    })
    out = binarize_votes(df, group_a=["PLN", "PUSC"], group_b=["PPSD", "NR"])

    assert list(out["code"]) == ["001", "002", "003"]
    assert out.loc[0, "spin"] == 1     # 150 vs 40 -> traditional wins
    assert out.loc[1, "spin"] == -1    # 30 vs 120 -> emerging wins
    assert out.loc[2, "spin"] == 1     # 100 vs 50 -> tie-break goes to group_a (>=)
    assert abs(out.loc[0, "margin"] - (150 - 40) / 190) < 1e-9


def test_binarize_handles_zero_total():
    df = pd.DataFrame({"code": ["x"], "A": [0], "B": [0]})
    out = binarize_votes(df, group_a=["A"], group_b=["B"])
    assert out.loc[0, "margin"] == 0.0
