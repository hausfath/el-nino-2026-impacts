#!/usr/bin/env python3.13
"""Oct 2026–Feb 2027 multi-model forecast maps, precipitation (% of normal) and temperature (°C vs 1991–2020)
side by side, for each impacts-map geography (same projections/extents as the regional close-ups).

Method (same as make_model_anomaly_maps.py):
- Oct–Feb anomaly per model = (3 × OND + 2 × JF) / 5 (month-weighted), from model_patterns/derived/seasonal_anoms.nc.
- Precip %: multi-model mean anomaly / GPCP 1991–2020 Oct–Feb climatology (same weighting); land cells with
  climatology < 0.5 mm/day are greyed out. 13 models (NMME + C3S).
- Temperature: each model shifted to a common 1991–2020 baseline via the ERA5 trend × (2006 − baseline midpoint);
  NOT trend-removed ("vs 1991–2020 normal"). CanESM5 and NCAR-CESM1 excluded (undocumented baselines) → 11 models.
- Dots: ≥80% of models share the sign of the multi-model mean.
- Outlines: the impact-map regions (make_impacts_map.py REGIONS + model_polygons.json).
Colour rules for the figure family: brown = dry, blue = wet, violet = cold, red = warm.
"""
import json
from pathlib import Path

import numpy as np
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from shapely.geometry import shape, Polygon, box
from shapely import affinity

HERE = Path(__file__).resolve().parent
D = HERE.parent / "model_patterns" / "derived"
a = xr.open_dataset(D / "seasonal_anoms.nc")
o = xr.open_dataset(D / "obs_ref.nc")
lon, lat = a.lon.values, a.lat.values
pc = ccrs.PlateCarree()
land = o.land.values.astype(bool)

NMME = ["CFSv2", "CanESM5", "GEM5.2_NEMO", "NASA_GEOS5v2", "NCAR_CCSM4", "NCAR_CESM1"]
C3S = ["ecmwf", "ukmo", "meteo_france", "dwd", "cmcc", "jma", "bom"]
BASE_MID = {"CFSv2": 2006.0, "NASA_GEOS5v2": 2006.0, "NCAR_CCSM4": 2006.0, "GEM5.2_NEMO": 1996.5,
            "CanESM5": None, "NCAR_CESM1": None, **{c: 2005.0 for c in C3S}}
REF_MID = 2006.0
W = {"OND": 3 / 5, "JF": 2 / 5}

# impact-map regions (outlines only)
src = (HERE / "make_impacts_map.py").read_text()
ns = {"Polygon": Polygon}
exec(src[src.index("REGIONS = ["):src.index("FOOTER =")], ns)
MODEL = {k: shape(v) for k, v in json.loads((D / "model_polygons.json").read_text()).items()}
BUF = {"peru": 0.8, "mekong": 0.8, "norcal": 0.3, "altiplano": 0.3, "cchile": 0.2}
OUTLINES = []
for key, kind, conf, flag, shp, *_ in ns["REGIONS"]:
    g = MODEL[key] if shp == "model" else Polygon(shp).buffer(BUF.get(key, 2.0), join_style=1).simplify(0.25)
    OUTLINES.append((g, flag == "busted"))


def oct_feb(var):
    out = []
    for m in NMME + C3S:
        if var == "t2m" and BASE_MID[m] is None:
            continue
        x = 0
        for s, w in W.items():
            f = a[var].sel(model=m, season=s).values
            if var == "t2m":
                f = f - o[f"t_trend_{s}"].values * (REF_MID - BASE_MID[m])
            x = x + w * f
        out.append(x)
    arr = np.array(out)
    mm = np.nanmean(arr, 0)
    agree = np.nanmean(np.sign(arr) == np.sign(mm), 0) >= 0.8 - 1e-9
    return mm, agree, arr.shape[0]


pr_mm, pr_agree, n_pr = oct_feb("prate")
clim = W["OND"] * o.pr_clim_OND.values + W["JF"] * o.pr_clim_JF.values
dry = (clim < 0.5) & land
PR = np.where(dry, np.nan, 100 * pr_mm / np.where(clim > 0, clim, np.nan))
PR = np.where(np.isfinite(PR), np.maximum(PR, -100), np.nan)
pr_agree = pr_agree & ~dry
T, t_agree, n_t = oct_feb("t2m")

PR_CMAP = LinearSegmentedColormap.from_list("drywet", ["#6B3D08", "#8C510A", "#D9A441", "#F3E6C8", "#F7F6F2",
                                                       "#D3E6F2", "#5FA8DA", "#0A5599", "#073F73"])
T_CMAP = LinearSegmentedColormap.from_list("coldwarm", ["#5A1466", "#9E4AA0", "#D5A6D6", "#F7F4F1",
                                                        "#F6BFA8", "#E0694B", "#B2182B", "#7A0C1E"])
PR_LEV = np.arange(-60, 61, 10)
T_LEV = np.arange(-3, 3.01, 0.5)
INK, SUB = "#1A1A1A", "#555555"
plt.rcParams["font.family"] = "DejaVu Sans"


def panel(fig, rect, proj, extent, field, agree, cmap, lev, cblab, ptitle, stride, show_dry, outlines=True):
    ax = fig.add_axes(rect, projection=proj)
    ax.set_extent(extent, crs=pc)
    # re-centre longitudes on the map's central meridian and contour in projected space (avoids dateline artefacts)
    c0 = getattr(proj, "proj4_params", {}).get("lon_0", 0.0)
    lon_r = ((lon - c0 + 180) % 360) - 180 + c0
    order = np.argsort(lon_r)
    L, F = lon_r[order], field[:, order]
    f_c, lon_c = add_cyclic_point(F, coord=L)
    # keep only the map window (+12°): contouring far-side points in an azimuthal projection creates streaks
    w, e, s_, n = extent
    xs = (lon_c >= w - 35) & (lon_c <= e + 35)
    ys = (lat >= s_ - 20) & (lat <= n + 20)
    f_c, lon_c, lat_c = f_c[np.ix_(ys, xs)], lon_c[xs], lat[ys]
    LON2, LAT2 = np.meshgrid(lon_c, lat_c)
    norm = BoundaryNorm(lev, cmap.N, extend="both")
    cf = ax.contourf(LON2, LAT2, f_c, levels=lev, cmap=cmap, norm=norm, extend="both", transform=pc,
                     transform_first=True, zorder=1)
    if show_dry:
        ax.set_facecolor("#D9D9D9")   # hides thin anti-aliasing rims around the dry-season mask
        dd, _ = add_cyclic_point(np.where(dry, 1.0, np.nan)[:, order], coord=L)
        dd = dd[np.ix_(ys, xs)]
        ax.contourf(LON2, LAT2, dd, levels=[0.5, 1.5], colors=["#D9D9D9"], transform=pc, transform_first=True, zorder=1.5)
    yy, xx = np.meshgrid(lat, lon, indexing="ij")
    sel = agree & (yy % stride == 0) & (xx % stride == 0)
    ax.scatter(xx[sel], yy[sel], s=2.2 if stride > 1 else 1.4, c="#222222", alpha=0.7, lw=0, transform=pc, zorder=3)
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.9, edgecolor="#222222", zorder=4)
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.6, edgecolor="#4A4A4A", zorder=4)
    w, e, s_, n = extent
    for g, busted in (OUTLINES if outlines else []):   # clip to the map window (+5°) so far-side polygons don't break azimuthal projections
        for shift in (0, -360, 360):
            gg = affinity.translate(g, xoff=shift).intersection(box(w - 5, s_ - 5, e + 5, n + 5))
            if not gg.is_empty:
                ax.add_geometries([gg], crs=pc, facecolor="none", edgecolor="#111111", linewidth=1.1,
                                  linestyle=(0, (4, 2)) if busted else "solid", zorder=5)
    ax.spines["geo"].set_edgecolor("#BBBBBB")
    ax.set_title(ptitle, fontsize=13.5, fontweight="bold", loc="left", color=INK, pad=7)
    bb = ax.get_position()
    cax = fig.add_axes([bb.x0 + 0.08 * bb.width, bb.y0 - 0.075, 0.84 * bb.width, 0.018])
    cb = fig.colorbar(cf, cax=cax, orientation="horizontal", ticks=lev[::2])
    cb.set_label(cblab, fontsize=10.5, color=SUB)
    cb.ax.tick_params(labelsize=9.5)
    cb.outline.set_edgecolor("#BBBBBB")
    return ax


def make(name, region_title, proj, extent, figsize, rects, stride, title_y=0.955, outlines=True):
    fig = plt.figure(figsize=figsize, facecolor="white")
    fig.text(0.03, title_y, f"El Niño 2026–27 forecast: {region_title}, Oct 2026–Feb 2027",
             fontsize=19, fontweight="bold", color=INK)
    fig.text(0.03, title_y - 0.028,
             ("Average of seasonal forecast models (NMME + Copernicus C3S, Sep 2026 start). Dots: at least 80% of models "
              "agree on the sign.\nOutlines: regions on the El Niño impacts map (dashed = underperformed in a recent strong event); "
              "some peak outside Oct–Feb." if outlines else
              "Average of seasonal forecast models started in September 2026 as a strong El Niño develops (NMME + Copernicus C3S).\n"
              "Dots: at least 80% of models agree on wetter vs drier (left) or warmer vs cooler (right)."),
             fontsize=11, color=SUB, va="top", linespacing=1.4)
    panel(fig, rects[0], proj, extent, PR, pr_agree, PR_CMAP, PR_LEV, "Precipitation (% above or below 1991–2020 normal)",
          f"Rain & snow  ({n_pr} models)", stride, True, outlines)
    panel(fig, rects[1], proj, extent, T, t_agree, T_CMAP, T_LEV, "Temperature (°C vs 1991–2020 normal, incl. long-term warming)",
          f"Temperature  ({n_t} models)", stride, False, outlines)
    fig.text(0.03, 0.012, "Shifts in the odds for the season as a whole, not a forecast of any single storm or heatwave. "
             "Grey: land in its normally very dry season (<0.5 mm/day).", fontsize=9, color="#777777")
    fig.text(0.97, 0.012, "Z. Hausfather · NMME, C3S, GPCP, ERA5", fontsize=8.5, color="#999999", ha="right")
    out = HERE / f"elnino_2026_forecast_octfeb_{name}{'' if outlines else '_clean'}"
    fig.savefig(str(out) + ".png", dpi=200)
    fig.savefig(str(out) + ".pdf")
    plt.close(fig)
    print("written", out.name)


for OUTL in (True, False):
    make("indo_pacific", "Asia, Australia and the Pacific", ccrs.PlateCarree(central_longitude=148), [62, 234, -46, 42],
         (17, 7.6), [[0.02, 0.2, 0.47, 0.6], [0.51, 0.2, 0.47, 0.6]], 2, title_y=0.94, outlines=OUTL)
    make("africa", "Africa", ccrs.LambertAzimuthalEqualArea(central_longitude=20, central_latitude=0), [-20, 58, -37, 24],
         (15, 9.6), [[0.03, 0.17, 0.45, 0.66], [0.52, 0.17, 0.45, 0.66]], 1, outlines=OUTL)
    make("south_america", "South America", ccrs.LambertAzimuthalEqualArea(central_longitude=-62, central_latitude=-15),
         [-92, -30, -45, 14], (14, 10.2), [[0.03, 0.16, 0.45, 0.68], [0.52, 0.16, 0.45, 0.68]], 1, outlines=OUTL)
    make("north_america", "North America",
         ccrs.LambertConformal(central_longitude=-98, central_latitude=40, standard_parallels=(25, 55)),
         [-138, -58, 8, 64], (16, 8.6), [[0.02, 0.18, 0.47, 0.64], [0.51, 0.18, 0.47, 0.64]], 1, outlines=OUTL)
print(f"models: precip {n_pr}, temperature {n_t}")
