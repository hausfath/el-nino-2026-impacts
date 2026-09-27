#!/usr/bin/env python3.13
"""Stream-process GPCC Precipitation Analysis Monthly Version 2025 (1°) into regional-mean series.

Downloads one 5-year file at a time from DWD open data, extracts area-weighted regional means of
`precip` (gauge-only analysis, mm/month) and the mean number of gauges per region (`gauge`),
then deletes the raw file. Regions and weights are identical to extract.py.
Output: derived/gpcc_regional_monthly.csv
"""
import gzip, shutil, subprocess
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import os
from extract import SHAPES, frac_weights, OUT, RAW
ONLY = [x for x in os.environ.get("ONLY", "").split(",") if x]
if ONLY:
    SHAPES = {k: v for k, v in SHAPES.items() if k in ONLY}
SUFFIX = os.environ.get("SUFFIX", "")

BASE = ("https://opendata.dwd.de/climate_environment/GPCC/GPCC_Precipitation_Analysis_Monthly/"
        "Version_2025/100_degree/")
CHUNKS = [f"{y}_{y+4}" for y in range(1951, 2021, 5)] + ["2021_2024"]
D = RAW / "gpcc"
D.mkdir(exist_ok=True)

W = None
rows = []
for c in CHUNKS:
    nc = D / f"gpcc_precipitation_analysis_monthly_{c}_v2025_100.nc"
    if not nc.exists():
        gz = nc.with_suffix(".nc.gz")
        subprocess.run(["curl", "-sfL", "-o", str(gz), BASE + gz.name], check=True)
        with gzip.open(gz, "rb") as fi, open(nc, "wb") as fo:
            shutil.copyfileobj(fi, fo)
        gz.unlink()
    ds = xr.open_dataset(nc).sortby("lat")
    ds = ds.assign_coords(lon=np.mod(ds.lon, 360)).sortby("lon")
    if W is None:
        W = {r: frac_weights(g, ds.lat.values, ds.lon.values) for r, g in SHAPES.items()}
    P = ds.precip.values
    G = ds.gauge.values
    days = ds.time.dt.days_in_month.values
    for r, w in W.items():
        if w.sum() == 0:
            continue
        ok = np.isfinite(P)
        num = np.nansum(P * w, axis=(1, 2))
        den = np.sum(ok * w, axis=(1, 2))
        v = np.where(den > 0.5 * den.max(), num / np.where(den > 0, den, 1), np.nan) / days  # mm/day; >=50% of max land weight
        gauges = np.nansum(np.where(w > 0, G, 0), axis=(1, 2))   # gauges in cells touching the region
        for t, vv, gg in zip(ds.time.values, v, gauges):
            rows.append((t, r, vv, gg))
    ds.close()
    nc.unlink()   # keep disk use to one chunk
    print(c, "done", flush=True)

pd.DataFrame(rows, columns=["time", "region", "value", "ngauges"]).assign(dataset="gpcc2025").to_csv(
    OUT / f"gpcc_regional_monthly{SUFFIX}.csv", index=False)
