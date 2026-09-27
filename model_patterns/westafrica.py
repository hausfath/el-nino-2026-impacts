#!/usr/bin/env python3.13
"""West Africa tests (23 Sep 2026). Expected signs fixed from the literature before
running: Guinea Coast dry (Cai et al. 2025, EP El Niño, DJF; also tested in the
Oct-Dec second rains and the Mar-May 2027 first rains), Sahel dry (JAS canon; only the
Sep tail falls in SON), West African land warm (tropical tropospheric warming).
NOT blind: global diagnostic maps covering Africa had already been viewed.
Two-sided sign tests, BH FDR within this family. Output: derived/westafrica_table.csv
"""
from pathlib import Path
import numpy as np, pandas as pd, xarray as xr, shapely
from shapely.geometry import box
from scipy.stats import binom

ROOT = Path(__file__).parent
a = xr.open_dataset(ROOT / "derived" / "seasonal_anoms.nc")
m = xr.open_dataset(ROOT / "derived" / "metrics.nc")
o = xr.open_dataset(ROOT / "derived" / "obs_ref.nc")
L2, A2 = np.meshgrid(np.where(a.lon > 180, a.lon - 360, a.lon), a.lat.values)
W = np.cos(np.deg2rad(A2)); land = o.land.values.astype(bool)
ENS = ["CFSv2", "CanESM5", "GEM5.2_NEMO", "NASA_GEOS5v2", "NCAR_CCSM4", "NCAR_CESM1",
       "ecmwf", "ukmo", "meteo_france", "dwd", "cmcc", "jma", "bom"]
REG = {"Guinea Coast": box(-10, 4, 10, 9), "Sahel": box(-17, 11, 20, 18),
       "Nigeria/Cameroon": box(3, 4, 15, 12), "West Africa (all)": box(-17, 4, 15, 18)}
TESTS = [("Guinea Coast", "pr", s, -1) for s in ["SON", "OND", "DJF", "MAM"]] + \
        [("Nigeria/Cameroon", "pr", s, -1) for s in ["OND", "MAM"]] + \
        [("Sahel", "pr", "SON", -1)] + \
        [(r, "t", s, +1) for r in ["West Africa (all)", "Guinea Coast", "Sahel"] for s in ["SON", "DJF", "JF"]]

def rmean(f, msk):
    ok = msk & np.isfinite(f); return float(np.sum(f[ok] * W[ok]) / np.sum(W[ok]))

rows = []
for reg, var, s, exp in TESTS:
    msk = shapely.contains_xy(REG[reg], L2, A2) & land
    ens = [x for x in ENS if np.isfinite(a.prate.sel(model=x, season=s).values).any()]
    if var == "pr":
        sd = o[f"pr_sd_{s}"].clip(min=0.05).values
        per = np.array([rmean(a.prate.sel(model=x, season=s).values / sd, msk) for x in ens])
        clim = rmean(o[f"pr_clim_{s}"].values, msk); lmr = np.nan
        rob = m[f"pr_robust_{s}"].values
    else:
        sd = o[f"t_sd_{s}"].clip(min=0.1).values
        per = np.array([rmean(a.t2m_adj.sel(model=x, season=s).values / sd, msk) for x in ens]); per = per[np.isfinite(per)]
        lmr = np.mean([rmean(a.t2m_lmr.sel(model=x, season=s).values / sd, msk) for x in ens]); clim = np.nan
        rob = np.where((m[f"t_robust_{s}"] != 0) & (m[f"t91_robust_{s}"] != 0) &
                       (np.sign(m[f"t_robust_{s}"]) == np.sign(m[f"tlmr_robust_{s}"])), m[f"t_robust_{s}"], 0)
    n = len(per); kp, kn = int((per > 0).sum()), int((per < 0).sum())
    mz = float(per.mean())
    rows.append(dict(region=reg, var=var, season=s, lit_expect="+" if exp > 0 else "−", clim_mm_day=round(clim, 2),
                     mmm_z=round(mz, 2), lmr_z=round(float(lmr), 2) if np.isfinite(lmr) else None,
                     pos=kp, neg=kn, p2=min(1, 2 * binom.sf(max(kp, kn) - 1, n, 0.5)),
                     robust_frac=round(float(((rob != 0) & (np.sign(rob) == np.sign(mz)) & msk).sum() / msk.sum()), 2)))
df = pd.DataFrame(rows); p = df.p2.values; o_ = np.argsort(p)
q = np.empty_like(p); q[o_] = np.minimum.accumulate((p[o_] * len(p) / (np.arange(len(p)) + 1))[::-1])[::-1].clip(max=1)
df["q_BH"] = q.round(4); df["p2"] = df.p2.round(4)
def verdict(r):
    if r.var == "pr" and r.clim_mm_day < 0.5: return "dry season (uninformative)"
    match = (r.mmm_z > 0) == (r.lit_expect == "+")
    tag = "matches lit" if match else "OPPOSITE to lit"
    if r.q_BH <= 0.10 and abs(r.mmm_z) >= 0.5 and r.robust_frac >= 0.25: return f"ROBUST ({tag})"
    if r.q_BH <= 0.10 and abs(r.mmm_z) >= 0.25: return f"moderate ({tag})"
    return "no reliable signal"
df["verdict"] = df.apply(verdict, axis=1)
df.to_csv(ROOT / "derived" / "westafrica_table.csv", index=False)
pd.set_option("display.width", 220); print(df.to_string(index=False))
