#!/usr/bin/env python3.13
"""Australia close-up of the multi-model seasonal forecasts (Sep 2026 start).
Uses members()/agreement() from make_model_anomaly_maps.py so methods are identical:
precip % of GPCP 1991-2020 climatology (floored at -100%, dry land masked), temperature
vs a common 1991-2020 baseline (2 models with undocumented baselines omitted),
dots where >=80% of models agree on sign. Scales are narrower than the global maps
(±50%, ±2 °C) to resolve Australian anomalies.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import make_model_anomaly_maps as M

HERE = Path(__file__).resolve().parent
lon, lat, o, pc = M.lon, M.lat, M.o, M.pc
land = o.land.values.astype(bool)
SEAS = [("SON", "Sep–Nov (spring)"), ("DJF", "Dec–Feb (summer)"), ("MAM", "Mar–May 2027 (autumn)")]
EXT = [110, 157, -45, -9]
DRY_MM = 1.0  # mm/day; stricter than the global maps (0.5) because arid-interior % values mislead
yy, xx = np.meshgrid(lat, lon, indexing="ij")

fig = plt.figure(figsize=(15, 10.2), facecolor="white")
fig.text(0.03, 0.955, "Australia: what seasonal forecast models expect from El Niño 2026–27",
         fontsize=19, fontweight="bold", color="#1A1A1A")
fig.text(0.03, 0.935, "Multi-model mean from 13 models (NMME + C3S; Mar–May: NMME only). Dots: at least 80% of models agree on the "
         "direction of the change.", fontsize=11.5, color="#555555", va="top")

rows = [("pr", "Rain", "BrBG", np.arange(-50, 51, 10), "Precipitation (% of 1991–2020 normal)"),
        ("t", "Temperature", "RdBu_r", np.arange(-2, 2.01, 0.25), "Temperature anomaly (°C vs 1991–2020)")]
for r, (kind, rowname, cmap, lev, cblab) in enumerate(rows):
    for c, (s, slab) in enumerate(SEAS):
        ax = fig.add_axes([0.03 + c * 0.305, 0.5 - r * 0.42, 0.29, 0.36], projection=pc)
        ax.set_extent(EXT, crs=pc)
        arr = M.members("prate" if kind == "pr" else "t2m", s)
        mm, agree = M.agreement(arr)
        if kind == "pr":
            clim = o[f"pr_clim_{s}"].values
            dry = (clim < DRY_MM) & land
            field = 100 * mm / np.where(clim > 0, clim, np.nan)
            field = np.maximum(field, -100)  # dry cells covered by the grey mask below (no NaN holes -> no halos)
            agree = agree & ~dry
        else:
            field = mm
        cf = ax.contourf(lon, lat, field, levels=lev, cmap=cmap, extend="both", transform=pc)
        if kind == "pr":
            ax.pcolormesh(np.append(lon - 0.5, lon[-1] + 0.5), np.append(lat + 0.5, lat[-1] - 0.5),
                          np.where(dry, 1.0, np.nan), cmap=matplotlib.colors.ListedColormap(["#D9D9D9"]),
                          transform=pc, zorder=3)
        sel = agree & (xx >= EXT[0] - 1) & (xx <= EXT[1] + 1) & (yy >= EXT[2] - 1) & (yy <= EXT[3] + 1)
        ax.scatter(xx[sel], yy[sel], s=5, c="#222222", alpha=0.8, lw=0, transform=pc, zorder=4)
        ax.coastlines(lw=0.7, color="#333333", resolution="50m")
        ax.add_feature(cfeature.STATES.with_scale("50m"), lw=0.35, edgecolor="#666666")
        ax.set_title(f"{rowname} · {slab} · {arr.shape[0]} models", fontsize=11.5, loc="left", color="#1A1A1A")
    cax = fig.add_axes([0.93, 0.53 - r * 0.42, 0.012, 0.3])
    cb = fig.colorbar(cf, cax=cax, ticks=lev if kind == "pr" else lev[::2])
    cb.set_label(cblab, fontsize=10)
    cb.ax.tick_params(labelsize=9)

fig.text(0.03, 0.012, "Seasonal forecasts initialized Sep 2026; shifts in the odds, not a forecast of any single storm or heatwave. "
         "Rain: anomalies relative to each model's hindcast climate, as % of the GPCP 1991–2020 climatology;\n"
         f"grey = land normally receiving <{DRY_MM:g} mm/day in that season, where percentages mislead.\nTemperature: models shifted to a common 1991–2020 baseline, "
         "long-term warming included; 2 of 13 models omitted (undocumented baselines).",
         fontsize=9, color="#666666", linespacing=1.4)
fig.text(0.97, 0.955, "Z. Hausfather · NMME, C3S, GPCP, ERA5", fontsize=8.5, color="#999999", ha="right")
out = HERE / "elnino_2026_australia_models"
fig.savefig(str(out) + ".png", dpi=170)
fig.savefig(str(out) + ".pdf")
print("written", out.name)
