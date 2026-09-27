#!/usr/bin/env python3.13
"""Pre-registered Europe tests (written 23 Sep 2026 BEFORE inspecting any European model
output). Expected signs follow the canonical literature picture: an early-winter
(Nov-Dec) +NAO-like response and a late-winter (Jan-Feb/Mar) -NAO-like response
(cold/dry north, wet south). Reported two-sided: we also count models with the
opposite sign, since a clear signal of either sign is informative.

Output: derived/europe_table.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import shapely
from shapely.geometry import box
from scipy.stats import binom

ROOT = Path(__file__).parent
a = xr.open_dataset(ROOT / "derived" / "seasonal_anoms.nc")
m = xr.open_dataset(ROOT / "derived" / "metrics.nc")
o = xr.open_dataset(ROOT / "derived" / "obs_ref.nc")
LAT, LON = a.lat.values, a.lon.values
LON2, LAT2 = np.meshgrid(np.where(LON > 180, LON - 360, LON), LAT)
W = np.cos(np.deg2rad(LAT2))
land = o.land.values.astype(bool)
ENS = ["CFSv2", "CanESM5", "GEM5.2_NEMO", "NASA_GEOS5v2", "NCAR_CCSM4", "NCAR_CESM1",
       "ecmwf", "ukmo", "meteo_france", "dwd", "cmcc", "jma", "bom"]

REG = {
    "Scandinavia & Baltic": box(5, 55, 30, 70),
    "UK & Ireland": box(-10.5, 50, 2, 59),
    "Central Europe": box(2, 45, 20, 55),
    "Iberia": box(-10, 36, 3.5, 44),
    "Italy & Balkans": box(8, 37, 28, 46),
    "Eastern Europe": box(20, 45, 40, 58),
}
# (region, var, season, expected sign) -- expected from the literature, fixed a priori
TESTS = []
for r in REG:
    north = r in ("Scandinavia & Baltic", "UK & Ireland", "Central Europe", "Eastern Europe")
    TESTS += [(r, "pr", "OND", +1 if north else -1),   # early winter +NAO-like: wet north, dry south
              (r, "pr", "JF", -1 if north else +1),    # late winter -NAO-like: dry north, wet south
              (r, "t", "OND", +1),                     # early winter mild
              (r, "t", "JF", -1 if north else 0)]      # late winter cold north; south: no expectation
TESTS += [(r, "pr", "DJF", 0) for r in REG] + [(r, "t", "DJF", 0) for r in REG]  # exploratory


def rmean(f, msk):
    ok = msk & np.isfinite(f)
    return float(np.sum(f[ok] * W[ok]) / np.sum(W[ok]))


rows = []
for reg, var, s, exp in TESTS:
    msk = shapely.contains_xy(REG[reg], LON2, LAT2) & land
    if var == "pr":
        sd = o[f"pr_sd_{s}"].clip(min=0.05).values
        per = np.array([rmean(a.prate.sel(model=x, season=s).values / sd, msk) for x in ENS])
        rob = m[f"pr_robust_{s}"].values
        lmr = None
    else:
        sd = o[f"t_sd_{s}"].clip(min=0.1).values
        per = np.array([rmean(a.t2m_adj.sel(model=x, season=s).values / sd, msk) for x in ENS])
        per = per[np.isfinite(per)]
        lmr = np.mean([rmean(a.t2m_lmr.sel(model=x, season=s).values / sd, msk) for x in ENS])
        rob = np.where((np.sign(m[f"t_robust_{s}"]) == np.sign(m[f"tlmr_robust_{s}"])) &
                       (m[f"t_robust_{s}"] != 0) & (m[f"t91_robust_{s}"] != 0), m[f"t_robust_{s}"], 0)
    n = len(per)
    kpos, kneg = int((per > 0).sum()), int((per < 0).sum())
    k = max(kpos, kneg)
    p2 = min(1.0, 2 * binom.sf(k - 1, n, 0.5))  # two-sided sign test
    mz = float(per.mean())
    robfrac = float(np.sum((rob != 0) & (np.sign(rob) == np.sign(mz)) & msk) / msk.sum())
    rows.append(dict(region=reg, var=var, season=s,
                     lit_expect={1: "+", -1: "−", 0: "none"}[exp], mmm_z=round(mz, 2),
                     models_pos=kpos, models_neg=kneg, p_two_sided=p2,
                     robust_frac_same_sign=round(robfrac, 2),
                     lmr_z=None if lmr is None else round(float(lmr), 2)))
df = pd.DataFrame(rows)
p = df.p_two_sided.values
o_ = np.argsort(p)
q = np.empty_like(p)
q[o_] = np.minimum.accumulate((p[o_] * len(p) / (np.arange(len(p)) + 1))[::-1])[::-1].clip(max=1)
df["q_BH"] = q.round(4)
df["p_two_sided"] = df.p_two_sided.round(4)


def verdict(r):
    agree_lit = r.lit_expect != "none" and ((r.mmm_z > 0) == (r.lit_expect == "+"))
    if r.q_BH <= 0.10 and abs(r.mmm_z) >= 0.5 and r.robust_frac_same_sign >= 0.25:
        return "ROBUST " + ("(matches lit)" if agree_lit else "(no lit expectation)" if r.lit_expect == "none" else "(OPPOSITE to lit)")
    if r.q_BH <= 0.10 and abs(r.mmm_z) >= 0.25:
        return "moderate " + ("(matches lit)" if agree_lit else "(no lit expectation)" if r.lit_expect == "none" else "(opposite to lit)")
    return "no reliable signal"


df["verdict"] = df.apply(verdict, axis=1)
df.to_csv(ROOT / "derived" / "europe_table.csv", index=False)
pd.set_option("display.width", 220, "display.max_rows", 100)
print(df.to_string(index=False))
