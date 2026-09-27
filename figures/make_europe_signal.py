#!/usr/bin/env python3.13
"""Europe explainer for the El Niño 2026-27 impacts work (for social sharing).

Why no Europe impacts map: no European region reaches the global map's bar in either
the literature (research/lit_europe.md: low / low-medium) or the Sep 2026 models
(model_patterns/derived/europe_table.csv: pre-registered tests, none robust).
All plotted numbers come from model_patterns/derived/, CPC's NAO index (1950-base monthly
normalized NAO) and CPC ONI, fetched live. NAO chart uses EVERY winter with NDJ ONI >= 1.5
since 1950 (an earlier draft showing only the 4 strongest post-1980 events overstated the
positive-NAO tendency: 3/4 vs 4/8).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shapely
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
MP = HERE.parent / "model_patterns" / "derived"
m = xr.open_dataset(MP / "metrics.nc")
tab = pd.read_csv(MP / "europe_table.csv")
lon = np.where(m.lon.values > 180, m.lon.values - 360, m.lon.values)
order = np.argsort(lon)
lon, lat = lon[order], m.lat.values
pc = ccrs.PlateCarree()

# CPC monthly NAO -> DJF means for winters after strong El Niños
txt = requests.get("https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii",
                   timeout=60).text
nao = {(int(a), int(b)): float(c) for a, b, c in (l.split() for l in txt.splitlines() if len(l.split()) == 3)}
# all El Niño winters with NDJ ONI >= 1.5 since 1950 (CPC ONI, ERSSTv5) -- no hand-picking
oni = {}
for l in requests.get("https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt", timeout=60).text.splitlines()[1:]:
    q = l.split()
    if len(q) == 4:
        oni[(q[0], int(q[1]))] = float(q[3])
winters = [y + 1 for y in range(1950, 2026)
           if oni.get(("NDJ", y), -9) >= 1.5 and (y, 12) in nao and (y + 1, 2) in nao]
djf = [np.mean([nao[(y - 1, 12)], nao[(y, 1)], nao[(y, 2)]]) for y in winters]
onis = [oni[("NDJ", y - 1)] for y in winters]
npos, nneg = sum(v > 0 for v in djf), sum(v < 0 for v in djf)


def z(name):
    return m[name].values[:, order]


def val(region, var, season, col):
    r = tab[(tab.region == region) & (tab["var"] == var) & (tab.season == season)].iloc[0]
    return r[col]


plt.rcParams["font.family"] = "DejaVu Sans"
INK, SUB = "#1A1A1A", "#4A4A4A"
fig = plt.figure(figsize=(13, 10), facecolor="white")
fig.text(0.035, 0.955, "El Niño and Europe this winter: no reliable signal", fontsize=22, fontweight="bold", color=INK)
fig.text(0.035, 0.93, "A record El Niño strongly shapes weather across the Pacific rim, but its fingerprint on European winters is weak,\n"
         "inconsistent between events, and largely not robust in this year's forecasts.",
         fontsize=12, color="#555555", linespacing=1.35, va="top")

trob = ((m.t_robust_JF > 0) & (m.t91_robust_JF > 0) & (m.tlmr_robust_JF > 0)) | \
       ((m.t_robust_JF < 0) & (m.t91_robust_JF < 0) & (m.tlmr_robust_JF < 0))
panels = [("Rain & snow, Oct–Dec", z("pr_z_OND"), z("pr_robust_OND") != 0, "BrBG"),
          ("Rain & snow, Jan–Feb", z("pr_z_JF"), z("pr_robust_JF") != 0, "BrBG"),
          ("Temperature, Jan–Feb (trend removed)", z("t_z_JF"), trob.values[:, order], "RdBu_r")]
proj = ccrs.LambertConformal(central_longitude=12, central_latitude=52, standard_parallels=(40, 62))
lev = np.arange(-1.5, 1.51, 0.25)
yy, xx = np.meshgrid(lat, lon, indexing="ij")
for i, (title, field, rob, cmap) in enumerate(panels):
    ax = fig.add_axes([0.03 + i * 0.32, 0.47, 0.30, 0.37], projection=proj)
    ax.set_extent([-12, 38, 35, 70], crs=pc)
    cf = ax.contourf(lon, lat, field, levels=lev, cmap=cmap, extend="both", transform=pc)
    ax.coastlines(lw=0.5, color="#444444")
    ax.add_feature(cfeature.BORDERS, lw=0.3, edgecolor="#666666")
    sel = rob & (np.abs(yy) < 72)
    ax.scatter(xx[sel], yy[sel], s=4, c="k", lw=0, transform=pc)
    ax.set_title(title, fontsize=12.5, loc="left", color=INK)
    cax = fig.add_axes([0.05 + i * 0.32, 0.445, 0.26, 0.012])
    cb = fig.colorbar(cf, cax=cax, orientation="horizontal", ticks=[-1.5, -1, -0.5, 0, 0.5, 1, 1.5])
    cb.ax.tick_params(labelsize=8.5)
    cb.set_label("← drier    wetter →" if cmap == "BrBG" else "← colder    warmer →", fontsize=9.5, color=SUB)
# robust fraction of European land, bound to the metrics file
o_ = xr.open_dataset(MP / "obs_ref.nc")
L2, A2 = np.meshgrid(np.where(m.lon > 180, m.lon - 360, m.lon), m.lat.values)
eu = shapely.contains_xy(box(-11, 35, 40, 71), L2, A2) & o_.land.values.astype(bool)
Wt = np.cos(np.deg2rad(A2))
frac = lambda x: 100 * float((Wt * (x & eu)).sum() / (Wt * eu).sum())
f_ond = frac(m.pr_robust_OND.values != 0)
f_jf = frac(m.pr_robust_JF.values != 0)
f_t = frac(((m.t_robust_JF != 0) & (np.sign(m.t_robust_JF) == np.sign(m.tlmr_robust_JF)) & (m.t91_robust_JF != 0)).values)
fig.text(0.035, 0.393, "Shading: average of 13 seasonal forecast models (NMME + C3S, Sep 2026 start), as a fraction of a typical "
         "year-to-year swing. Dots: robust signal (≥80% of models\nagree and ≥0.5 of a typical swing). "
         f"Robust areas cover {f_ond:.0f}% of European land for Oct–Dec rain (mostly western Ireland, Britain and France),\n"
         f"{f_jf:.0f}% for Jan–Feb rain, and {f_t:.0f}% for Jan–Feb temperature.",
         fontsize=9.5, color=SUB, va="top", linespacing=1.4)

# NAO bar chart
bx = fig.add_axes([0.075, 0.108, 0.36, 0.178])
cols = ["#B2182B" if v > 0 else "#2166AC" for v in djf]
bx.bar([f"{y-1}–\n{str(y)[2:]}" for y in winters], djf, color=cols, width=0.62)
bx.axhline(0, color="#333333", lw=0.8)
for k, v in enumerate(djf):
    bx.text(k, v + (0.06 if v > 0 else -0.06), f"{v:+.1f}", ha="center", va="bottom" if v > 0 else "top", fontsize=9)
bx.set_ylim(-2.0, 1.75)
bx.set_ylabel("Winter (Dec–Feb) NAO index", fontsize=10)
bx.set_title(f"Every strong El Niño winter since 1950 (Nov–Jan ONI ≥ 1.5):\nthe NAO split {npos} positive, {nneg} negative, a coin flip",
             fontsize=11, loc="left", color=INK)
bx.set_xlabel("Textbook El Niño expectation: negative NAO (cold north, wet south).\n"
              "Positive NAO = mild, wet, stormy UK & northern Europe.",
              fontsize=8.5, color="#444444", style="italic", linespacing=1.3, labelpad=6)
bx.spines[["top", "right"]].set_visible(False)
bx.tick_params(labelsize=8.5)

# takeaways (numbers bound to computed tables)
uk, ce = val("UK & Ireland", "pr", "OND", "mmm_z"), val("Central Europe", "pr", "OND", "mmm_z")
ukn = val("UK & Ireland", "pr", "OND", "models_pos")
sc = val("Scandinavia & Baltic", "t", "JF", "mmm_z")
scn = val("Scandinavia & Baltic", "t", "JF", "models_neg")
points = [
    f"Models lean wet for the UK & central Europe in Oct–Dec ({ukn} of 13\n"
    f"models) and colder for Scandinavia in Jan–Feb ({scn} of 11), but the\n"
    f"shifts are small: {min(uk, ce):.1f}–{abs(sc):.1f} of a typical year-to-year swing.",
    f"No European region passes the bar used for the global impacts map,\nand past strong El Niño winters split {npos}–{nneg} on the NAO.",
    "The textbook late-winter pattern (cold north, wet south) mostly\n"
    "appears when a sudden stratospheric warming occurs, which can't\n"
    "be forecast months ahead (Ineson & Scaife 2009).",
    "The El Niño–Europe link may have weakened since the 1970s\n(Ivasić et al. 2021).",
]
fig.text(0.53, 0.3, "What this means", fontsize=13, fontweight="bold", color=INK)
y = 0.268
for ptxt in points:
    fig.text(0.53, y, "•", fontsize=12, color=INK, va="top")
    fig.text(0.545, y, ptxt, fontsize=10.5, color="#333333", va="top", linespacing=1.35)
    y -= 0.01 + 0.02 * (ptxt.count("\n") + 1)

fig.text(0.965, 0.012, "Z. Hausfather · data: NMME, C3S, GPCP, ERA5, NOAA CPC NAO index",
         fontsize=8, color="#999999", ha="right")
out = HERE / "elnino_2026_europe_signal"
fig.savefig(str(out) + ".png", dpi=200)
fig.savefig(str(out) + ".pdf")
print("written", str(out) + ".png", "| winters:", winters, "NAO DJF:", [round(float(v), 2) for v in djf])
