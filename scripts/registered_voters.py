"""Per-distrito registered-voter counts (electores_inscritos) from the TSE
consolidado ZIP, joined onto this project's distrito node codes."""
from __future__ import annotations
import io, zipfile
from pathlib import Path
import numpy as np, pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from isingcr.ingestion.canton_names import normalize_distrito_code

ZIPS = {"2026": "DEFINITIVO_juntas_TSE_2026.zip", "2022": "juntas_TSE_2022_ronda2_provisional_y_definitivo.zip"}


def registered_voters(nodes, year="2026"):
    z = zipfile.ZipFile(Path(__file__).resolve().parent.parent / "data" / "raw" / "tse_juntas" / ZIPS[year])
    name = [n for n in z.namelist() if n.endswith("consolidado_presidenciales.csv")][0]
    df = pd.read_csv(io.BytesIO(z.read(name)))
    df = df[df["tipo_territorio"].str.upper() == "NACIONAL"]
    df = df.drop_duplicates(subset=["provincia_pais", "canton_ciudad", "distrito", "junta"])
    df["code"] = [normalize_distrito_code(p, c, d) for p, c, d in zip(df["provincia_pais"], df["canton_ciudad"], df["distrito"])]
    pop = df.groupby("code")["electores_inscritos"].sum()
    out = np.array([float(pop.get(n, np.nan)) for n in nodes])
    return out
