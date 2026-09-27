#!/usr/bin/env python3.13
"""Multi-model seasonal forecast maps (Sep 2026 start): precipitation (% of normal) and
2 m temperature (°C vs 1991-2020), with stippling where >=80% of models agree on sign.

Data: model_patterns/derived/seasonal_anoms.nc (per-model seasonal anomalies) and
obs_ref.nc (GPCP 1991-2020 climatology, ERA5 1979-2025 trend).
- Precip %: multi-model mean anomaly / GPCP 1991-2020 seasonal climatology x 100.
  Model anomalies are relative to each system's own hindcast climatology (1982-2019 range);
  LAND cells with climatology < 0.5 mm/day are masked grey (deserts/dry seasons); ocean is
  not masked, so the large (real) % increases over the cold-tongue Pacific remain visible.
- Temperature: each model's anomaly shifted to a common 1991-2020 baseline using the
  ERA5 trend x (2006.0 - model baseline midpoint). CanESM5 / NCAR-CESM1 excluded
  (undocumented baselines). NOT trend-removed: this is "vs 1991-2020 normal".
- Stippling: >=80% of models share the sign of the multi-model mean (sign only).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

HERE = Path(__file__).resolve().parent
D = HERE.parent / "model_patterns" / "derived"
a = xr.open_dataset(D / "seasonal_anoms.nc")
o = xr.open_dataset(D / "obs_ref.nc")
lon, lat = a.lon.values, a.lat.values
pc = ccrs.PlateCarree()

NMME = ["CFSv2", "CanESM5", "GEM5.2_NEMO", "NASA_GEOS5v2", "NCAR_CCSM4", "NCAR_CESM1"]
C3S = ["ecmwf", "ukmo", "meteo_france", "dwd", "cmcc", "jma", "bom"]
BASE_MID = {"CFSv2": 2006.0, "NASA_GEOS5v2": 2006.0, "NCAR_CCSM4": 2006.0, "GEM5.2_NEMO": 1996.5,
            "CanESM5": None, "NCAR_CESM1": None, **{c: 2005.0 for c in C3S}}
REF_MID = 2006.0  # 1991-2020
SEASONS = [("OND", "Oct–Dec 2026"), ("DJF", "Dec 2026–Feb 2027"), ("MAM", "Mar–May 2027")]


def members(var, s):
    out = []
    for mname in NMME + C3S:
        x = a[var].sel(model=mname, season=s).values
        if np.isnan(x).mean() > 0.01:
            continue
        if var == "t2m":
            if BASE_MID[mname] is None:
                continue
            x = x - o[f"t_trend_{s}"].values * (REF_MID - BASE_MID[mname])
        out.append(x)
    return np.array(out)


def agreement(arr):
    mm = np.nanmean(arr, 0)
    frac = np.nanmean(np.sign(arr) == np.sign(mm), 0)
    return mm, frac >= 0.8 - 1e-9


def figure(kind, pmax=60):
    fig = plt.figure(figsize=(12, 15.5), facecolor="white")
    land = o.land.values.astype(bool)
    floored = []  # % of mapped area where the mean anomaly exceeds observed climatology (< -100%)
    Wt = np.cos(np.deg2rad(lat))[:, None] * np.ones((1, lon.size)); band = (np.abs(lat) <= 58)[:, None]
    if kind == "pr":
        title = "Where forecast models expect a wetter or drier season"
        sub = ("Multi-model mean precipitation, % above or below normal. Dots: at least 80% of models agree on wetter vs\n"
               "drier. Grey: land in its normally very dry season (<0.5 mm/day), where percentages are not meaningful.")
        cmap, lev = "BrBG", np.arange(-pmax, pmax + 1, 10 if pmax <= 60 else 20)
        cblab = "Precipitation anomaly (% of 1991–2020 normal)"
    else:
        title = "Where forecast models expect a warmer or cooler season"
        sub = ("Multi-model mean 2 m temperature anomaly vs the 1991–2020 normal (°C), including long-term warming.\n"
               "Dots: at least 80% of models agree on warmer vs cooler.")
        cmap, lev = "RdBu_r", np.arange(-3, 3.01, 0.5)
        cblab = "Temperature anomaly (°C vs 1991–2020)"
    fig.text(0.04, 0.972, title, fontsize=20, fontweight="bold", color="#1A1A1A")
    fig.text(0.04, 0.962, sub, fontsize=11.5, color="#555555", va="top", linespacing=1.4)
    for i, (s, slab) in enumerate(SEASONS):
        proj = ccrs.Robinson(central_longitude=180)
        ax = fig.add_axes([0.03, 0.672 - i * 0.281, 0.94, 0.24], projection=proj)
        ax.set_global()
        x0, x1 = ax.get_xlim()
        ax.set_ylim(proj.transform_point(180, -58, pc)[1], proj.transform_point(180, 78, pc)[1])
        ax.set_xlim(x0, x1)
        arr = members("prate" if kind == "pr" else "t2m", s)
        mm, agree = agreement(arr)
        if kind == "pr":
            clim = o[f"pr_clim_{s}"].values
            field = 100 * mm / np.where(clim > 0, clim, np.nan)
            dry = (clim < 0.5) & land
            field = np.where(dry, np.nan, field)
            agree = agree & ~dry
            # model anomalies are vs each model's own (wetter-biased) climate but % uses GPCP, so a few
            # cells fall below the physical floor of -100%; display them at -100% and report the area
            bad = np.isfinite(field) & (field < -100) & band
            floored.append(100 * (Wt * bad).sum() / (Wt * (np.isfinite(field) & band)).sum())
            field = np.where(np.isfinite(field), np.maximum(field, -100), np.nan)
        else:
            field = mm
        f_c, lon_c = add_cyclic_point(field, coord=lon)
        ext = "max" if (kind == "pr" and pmax >= 100) else "both"  # precip cannot go below -100%
        cf = ax.contourf(lon_c, lat, f_c, levels=lev, cmap=cmap, extend=ext, transform=pc)
        if kind == "pr":
            ax.contourf(lon, lat, np.where(dry, 1.0, np.nan), levels=[0.5, 1.5], colors=["#D9D9D9"], transform=pc)
        yy, xx = np.meshgrid(lat, lon, indexing="ij")
        sel = agree & (yy % 3 == 0) & (xx % 3 == 0)
        ax.scatter(xx[sel], yy[sel], s=1.3, c="#222222", alpha=0.75, lw=0, transform=pc, zorder=4)
        ax.coastlines(lw=0.45, color="#333333")
        n = arr.shape[0]
        src = "NMME + C3S" if s != "MAM" else "NMME only; C3S forecasts end in Feb"
        ax.set_title(f"{slab}   ({n} models, {src})", fontsize=13, loc="left", color="#1A1A1A", pad=6)
    cax = fig.add_axes([0.2, 0.086, 0.6, 0.011])
    cb = fig.colorbar(cf, cax=cax, orientation="horizontal",
                      ticks=(lev if pmax >= 100 else lev[::2]) if kind == "pr" else lev)
    cb.set_label(cblab, fontsize=11)
    cb.ax.tick_params(labelsize=10)
    note = ("Seasonal forecasts initialized Sep 2026; shifts in the odds, not a forecast of any single storm or heatwave. "
            + ("Anomalies are relative to each model's\nhindcast climate; percentages use the GPCP 1991–2020 climatology. "
               f"Values below −100% (where a model's climate is wetter than observed;\n{min(floored):.1f}–{max(floored):.1f}% "
               "of the mapped area, mostly ocean) are shown as −100%."
               if kind == "pr" else "Models shifted to a common 1991–2020\nbaseline; 2 of 13 models omitted (undocumented baselines)."))
    fig.text(0.04, 0.008, note, fontsize=9, color="#666666", linespacing=1.35)
    fig.text(0.96, 0.057, "Z. Hausfather · NMME, C3S, GPCP, ERA5", fontsize=8.5, color="#999999", ha="right")
    out = HERE / (f"elnino_2026_model_precip_pct{'' if pmax == 60 else f'_{pmax}'}" if kind == "pr" else "elnino_2026_model_temperature")
    fig.savefig(str(out) + ".png", dpi=170)
    fig.savefig(str(out) + ".pdf")
    print("written", out.name, "| models per season:", [members("prate" if kind == "pr" else "t2m", s).shape[0] for s, _ in SEASONS])


if __name__ == "__main__":
    figure("pr")
    figure("pr", pmax=100)
    figure("t")
