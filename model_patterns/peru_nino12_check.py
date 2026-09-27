#!/usr/bin/env python3.13
"""Niño 1+2 check behind the v5.3 Peru/Ecuador upgrade (23 Sep 2026).
Observed: CPC weekly OISST Niño 1+2 anomalies (1991-2020 base), wksst9120.for.
Forecast: NMME Sep 2026 per-model ensemble-mean tmpsfc anomalies, 0-10S, 90-80W
(raw/nmme_202609_sst/, from realtime_anom/ENSMEAN). Output: derived/peru_nino12.csv
"""
import re, datetime as dt
from pathlib import Path
import numpy as np, pandas as pd, requests, xarray as xr

ROOT = Path(__file__).parent
rows = []
for l in requests.get("https://www.cpc.ncep.noaa.gov/data/indices/wksst9120.for", timeout=60).text.splitlines():
    mm = re.match(r"\s*(\d{2}[A-Z]{3}\d{4})\s+(\d+\.\d)\s*([-+]?\d+\.\d)", l)  # fixed-width: anomaly can abut SST
    if mm:
        rows.append((dt.datetime.strptime(mm.group(1), "%d%b%Y"), float(mm.group(3))))
def near(y, m, d):
    return min(rows, key=lambda r: abs((r[0] - dt.datetime(y, m, d)).days))[1]
def mean(y0, m0, y1, m1):
    return float(np.mean([a for (t, a) in rows if dt.datetime(y0, m0, 1) <= t < dt.datetime(y1, m1, 1)]))
out = []
for y in [1997, 2015, 2023, 2026]:
    r = dict(event=f"{y}-{str(y+1)[2:]}", obs_midSep=near(y, 9, 16))
    if y < 2026:
        r.update(obs_Dec=mean(y, 12, y + 1, 1), obs_JFM=mean(y + 1, 1, y + 1, 4), obs_FMA=mean(y + 1, 2, y + 1, 5))
    out.append(r)
fc = {}
for m in ["CFSv2", "CanESM5", "GEM5.2_NEMO", "NASA_GEOS5v2", "NCAR_CCSM4", "NCAR_CESM1"]:
    f = xr.open_dataset(ROOT / "raw" / "nmme_202609_sst" / f"{m}.tmpsfc.anom.nc", decode_times=False).fcst
    f = f.sel(lat=slice(0, -10), lon=slice(270, 280))
    fc[m] = f.weighted(np.cos(np.deg2rad(f.lat))).mean(("lat", "lon")).values  # Sep..May
arr = np.array(list(fc.values()))
out[-1].update(nmme_Dec=float(arr[:, 3].mean()), nmme_JFM=float(arr[:, 4:7].mean()), nmme_FMA=float(arr[:, 5:8].mean()),
               nmme_JFM_min=float(arr[:, 4:7].mean(1).min()), nmme_JFM_max=float(arr[:, 4:7].mean(1).max()),
               nmme_FMA_min=float(arr[:, 5:8].mean(1).min()), nmme_FMA_max=float(arr[:, 5:8].mean(1).max()))
df = pd.DataFrame(out).round(2)
df.to_csv(ROOT / "derived" / "peru_nino12.csv", index=False)
print(df.to_string(index=False))
