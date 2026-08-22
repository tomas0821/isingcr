#!/usr/bin/env python3
"""Parse MIDEPLAN's IDS 2023 regional CSV exports into the flat
data/raw/mideplan_ids_2023.csv that isingcr.ingestion.mideplan_ids.
load_mideplan_ids auto-detects.

Source: MIDEPLAN's official IDS 2023 workbook (see
https://www.mideplan.go.cr/indice-desarrollo-social), specifically the six
regional per-canton-per-distrito tables (Tabla 15-20, one per Costa Rican
planning region: Central, Pacifico Central, Chorotega, Brunca, Huetar
Caribe, Huetar Norte), fetched 2026-08-20 as CSV exports and archived
verbatim under data/raw/mideplan_source/tabla{15..20}.csv.

Row format quirk (an Excel merged-cell layout surviving the CSV export):
the FIRST canton in each regional table has its name embedded in the
header cell ("...DISTRITO <canton>") rather than its own row; every
subsequent canton instead gets a row with only its name (all data columns
blank), followed by that canton's distrito rows (name + data columns
filled). Handled below by tracking "current canton" and reassigning it
whenever a data-column-empty row is seen.

Province isn't given directly -- MIDEPLAN groups these six tables by
planning region, which spans multiple provinces (e.g. Tabla 15 alone
covers cantons from San Jose, Alajuela, Cartago, and Heredia provinces) --
so province is looked up from this project's own already-verified
canton/province shapefile data (cri_admin2.shp) rather than hand-typed.

Result (2026-08-20): 490 distrito rows, 84 unique cantons, 0 missing
province/ids values -- matches MIDEPLAN's own stated coverage exactly
(490 districts, 84 cantons). Joined against the real N=488 distrito
electoral graph: 486/488 matched (2 missing -- SAN JOSE|PEREZ ZELEDON|LA
AMISTAD and HEREDIA|BARVA|PUENTE SALAS, apparently distritos created after
the IDS 2023 publication; ids_zscore_by_code assigns them a neutral h_soc=0
rather than dropping them).

Extended 2026-08-21 to also emit the five published sub-dimensions IDS is
composed of (SALUD, PARTICIPA, SEGURIDAD, EDUCACION, ECONOMICO) -- present
in these same source tables under identical headers across all six
regional files, just never extracted before. Purely additive: existing
consumers of mideplan_ids_2023.csv read the `ids` column by name.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from isingcr.ingestion import load_shapefile

DATA_RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
SOURCE_DIR = DATA_RAW / "mideplan_source"
CANTON_SHAPEFILE = DATA_RAW / "boundaries" / "extracted" / "cri_admin2.shp"
OUT_CSV = DATA_RAW / "mideplan_ids_2023.csv"
TABLE_NUMBERS = [15, 16, 17, 18, 19, 20]


def canton_province_map() -> dict[str, str]:
    gdf = load_shapefile(CANTON_SHAPEFILE, id_col="adm2_name")
    return {c: p for p, c in zip(gdf["adm1_name"], gdf["adm2_name"])}


AXIS_HEADERS = {
    "salud": "DIMENSIÓN SALUD",
    "participa": "PARTICIPA",
    "seguridad": "SEGURIDAD",
    "educacion": "EDUCACION",
    "economico": "ECONOMICO",
}


def parse_table(path: Path) -> list[tuple]:
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    m = re.search(r"DISTRITO\s+(.+)$", header[0].strip())
    if not m:
        raise ValueError(f"Could not find first-canton marker in {path.name}: {header[0]!r}")
    current_canton = m.group(1).strip()
    ids_col = next(i for i, h in enumerate(header) if h.strip() == "IDS 2023")
    axis_cols = {key: next(i for i, h in enumerate(header) if h.strip() == label)
                 for key, label in AXIS_HEADERS.items()}

    out = []
    for row in rows[1:]:
        name = row[0].strip().strip('"')
        if not name:
            continue
        ids_val = row[ids_col].strip() if ids_col < len(row) else ""
        if not ids_val:
            current_canton = name  # canton-header row, no data on this row
            continue
        axis_vals = [float(row[axis_cols[key]].strip().replace(",", "."))
                     for key in AXIS_HEADERS]
        out.append((current_canton, name, float(ids_val.replace(",", ".")), *axis_vals))
    return out


def main() -> None:
    prov_map = canton_province_map()
    all_rows: list[tuple] = []
    for n in TABLE_NUMBERS:
        table_rows = parse_table(SOURCE_DIR / f"tabla{n}.csv")
        print(f"Tabla {n}: {len(table_rows)} distrito rows, "
              f"{len(set(row[0] for row in table_rows))} cantons")
        all_rows.extend(table_rows)
    print(f"\nTotal distrito rows parsed: {len(all_rows)} "
          f"({len(set(row[0] for row in all_rows))} unique cantons)")

    unmatched = sorted(set(row[0] for row in all_rows if row[0] not in prov_map))
    if unmatched:
        print(f"WARNING: {len(unmatched)} canton name(s) not found in shapefile "
              f"province map: {unmatched}")

    OUT_CSV.parent.mkdir(exist_ok=True, parents=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["provincia", "canton", "distrito", "ids", *AXIS_HEADERS.keys()])
        for canton, distrito, ids, *axis_vals in all_rows:
            writer.writerow([prov_map.get(canton, ""), canton, distrito, ids, *axis_vals])
    print(f"Written to {OUT_CSV}")


if __name__ == "__main__":
    main()
