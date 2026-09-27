#!/usr/bin/env python3.13
"""Station-based monthly precipitation for regions a 1° grid can't represent:
Hawaii, W Pacific islands, C Pacific islands, and the north coast of Peru.

Source: NOAA GHCN-Daily by-station CSVs (PRCP, QC-flagged values dropped). A month counts if
>= 80% of its days have valid data; its total is scaled up by ndays/nvalid.
Station selection (fixed before computing any hit rate):
  - hawaii: GHCN-D PRCP stations inside the map polygon (+1° buffer) with inventory coverage
    from <= 1957 to >= 2024.
  - wpacific: stations inside the map polygon buffered by 2° with coverage <= 1966 to >= 2016,
    Australian stations excluded (the polygon's bounding window touches Cape York).
  - cpacific: Canton Island (the only long record inside the polygon) + Tarawa/Funafuti (from 1973).
  - peru: Peru airport stations on the north coast (Tumbes, Talara, Piura, Chiclayo, Trujillo), 1973-.
Output: derived/stations_monthly.csv (station, group, time, prcp_mm)
"""
import gzip, io, json, subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from shapely.geometry import shape, Point

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "derived"
M = json.loads((HERE.parent / "model_patterns" / "derived" / "model_polygons.json").read_text())

inv = {}
for l in open(RAW / "ghcnd-inventory.txt"):
    p = l.split()
    if p[3] == "PRCP":
        inv[p[0]] = (int(p[4]), int(p[5]))
meta = {}
for l in open(RAW / "ghcnd-stations.txt"):
    meta[l[:11]] = (float(l[12:20]), float(l[21:30]), l[41:71].strip())

sel = {}
for sid, (lat, lon, name) in meta.items():
    if sid not in inv or sid.startswith("AS"):
        continue
    f, t = inv[sid]
    pt = Point(lon % 360, lat)
    if shape(M["hawaii"]).buffer(1.0).contains(pt) and f <= 1957 and t >= 2024:
        sel[sid] = "hawaii"
    elif shape(M["wpacific"]).buffer(2.0).contains(pt) and f <= 1966 and t >= 2016:
        sel[sid] = "wpacific"
for sid in ["KRW00060703", "KR000091610", "TV000091643"]:
    sel[sid] = "cpacific"
for sid in ["PEM00084370", "PEM00084390", "PEM00084401", "PEM00084452", "PEM00084501"]:
    sel[sid] = "peru"

rows = []
for sid, grp in sel.items():
    url = f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/{sid}.csv.gz"
    r = subprocess.run(["curl", "-sfL", url], capture_output=True)
    if r.returncode != 0:
        print("fail", sid)
        continue
    d = pd.read_csv(io.BytesIO(gzip.decompress(r.stdout)), header=None,
                    names=["id", "date", "el", "val", "m", "q", "s", "obs"], dtype={"q": str, "m": str})
    d = d[(d.el == "PRCP") & (d.q.isna())]
    d["date"] = pd.to_datetime(d.date.astype(str), format="%Y%m%d")
    d = d[d.date >= "1950-01-01"]
    g = d.set_index("date").val.resample("MS")
    tot, n = g.sum() / 10.0, g.count()   # tenths of mm -> mm
    ndays = tot.index.days_in_month
    ok = n >= 0.8 * ndays
    mon = (tot * ndays / n.where(n > 0)).where(ok)
    for t, v in mon.items():
        rows.append((sid, grp, meta[sid][2], t, v))
    print(sid, grp, meta[sid][2], int(ok.sum()), "good months", flush=True)

pd.DataFrame(rows, columns=["station", "group", "name", "time", "prcp_mm"]).to_csv(
    OUT / "stations_monthly.csv", index=False)
