#!/usr/bin/env python3.13
"""Berkeley Earth land (Complete_TAVG, 1°) regional-mean monthly temperature anomalies (vs 1951-1980)
for the temperature regions. Cells are weighted by cos(lat) × polygon fraction × Berkeley Earth's land_mask,
so Hudson Bay (open water/ice) is excluded. Output: derived/be_regional_monthly.csv"""
import numpy as np, pandas as pd, xarray as xr
from extract import SHAPES, frac_weights, OUT, RAW
REG = ["ccanada_warm", "box_ccanada", "c_se_alaska", "c_scandinavia", "inlandnw"]
d = xr.open_dataset(RAW / "be_complete_tavg_1deg.nc", decode_times=False)
t = d.time.values
sel = (t >= 1950) & (t < 2025)
T = d.temperature.isel(time=np.where(sel)[0]).rename(latitude="lat", longitude="lon")
T = T.assign_coords(lon=np.mod(T.lon, 360)).sortby("lon").sortby("lat")
lm = d.land_mask.rename(latitude="lat", longitude="lon")
lm = lm.assign_coords(lon=np.mod(lm.lon, 360)).sortby("lon").sortby("lat").values
yrs = np.floor(t[sel]).astype(int); mons = np.round((t[sel] - yrs) * 12 + 0.5).astype(int)
times = pd.to_datetime([f"{y}-{m:02d}-01" for y, m in zip(yrs, mons)])
V = T.values
rows = []
for r in REG:
    w = frac_weights(SHAPES[r], T.lat.values, T.lon.values) * lm
    ok = np.isfinite(V)
    s = np.nansum(V * w, axis=(1, 2)) / np.sum(ok * w, axis=(1, 2))
    rows += [(tt, r, v) for tt, v in zip(times, s)]
pd.DataFrame(rows, columns=["time", "region", "value"]).assign(dataset="berkeley").to_csv(
    OUT / "be_regional_monthly.csv", index=False)
print("ok", times[0], times[-1])
