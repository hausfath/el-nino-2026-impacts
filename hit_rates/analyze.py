#!/usr/bin/env python3.13
"""Observed hit rates for the El Niño 2026-27 impacts-map regions (spec: METHODS.md §1, fixed before results).

Reads the regional monthly series in derived/ and writes:
  derived/hit_events.csv   one row per (config, region, event year): value, percentile, hit flags
  derived/hit_summary.csv  one row per (config, region): counts, median percentile, base-rate checks
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import theilslopes
from statsmodels.nonparametric.smoothers_lowess import lowess

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
ROOT = HERE.parent

# ---------------------------------------------------------------- ENSO classification (NDJ, year 0)
def ndj(path, col):
    t = pd.read_csv(path, sep=r"\s+")
    t = t[t.SEAS == "NDJ"]
    return pd.Series(t[col].values, index=t.YR.values)

ONI = ndj(ROOT / "oni_cpc_2026-09-15.txt", "ANOM")
RONI = ndj(HERE / "raw" / "roni.ascii.txt", "ANOM")
YEARS = np.arange(1951, 2024)          # year 0 from 1951; decay-year seasons need data through 2024
STRONG = [y for y in YEARS if ONI.get(y, np.nan) >= 1.5]
STRONG_RONI = [y for y in YEARS if RONI.get(y, np.nan) >= 1.5]
MODERATE = [y for y in YEARS if 1.0 <= ONI.get(y, np.nan) < 1.5]
NEUTRAL = [y for y in YEARS if abs(ONI.get(y, np.nan)) < 0.5]
LANINA = [y for y in YEARS if ONI.get(y, np.nan) <= -1.0]
assert STRONG == [1957, 1965, 1972, 1982, 1997, 2009, 2015, 2023], STRONG

# ---------------------------------------------------------------- seasons: (month, year offset)
def mons(a, b, off_first=0):
    """months a..b inclusive, wrapping the year; months after the wrap get offset +1."""
    out, m, off = [], a, off_first
    while True:
        out.append((m, off))
        if m == b:
            return out
        m += 1
        if m == 13:
            m, off = 1, off + 1

SEASON = {
    "SOND": mons(9, 12), "DJFMA": mons(12, 4), "DJF": mons(12, 2), "ONDJFMAM": mons(10, 5),
    "MAM1": mons(3, 5, 1), "SONDJF": mons(9, 2), "SONDJFMAM": mons(9, 5), "NDJFM": mons(11, 3),
    "SON": mons(9, 11), "JJAS1": mons(6, 9, 1), "JJAS0": mons(6, 9), "OND": mons(10, 12),
    "DJFMA_p": mons(12, 4), "DJFM": mons(12, 3), "DJFMAM": mons(12, 5), "JJA1": mons(6, 8, 1),
    "JAS0": mons(7, 9), "JF1": mons(1, 2, 1), "JJ1": mons(6, 7, 1),
    "JJA0": mons(6, 8), "JJASON0": mons(6, 11), "MAMJJAS0": mons(3, 9), "MAMJJAS1": mons(3, 9, 1), "ON0": mons(10, 11), "JFM1": mons(1, 3, 1),
}

# region: (expected sign, season, main source, [sensitivity sources], variable)
P, T = "pr", "t"
SPEC = {
    "maritime": (-1, "SOND", "gpcc2025", ["precl", "gpcp"], P),
    "philippines": (-1, "DJFMA", "gpcc2025", ["precl", "gpcp"], P),
    "safrica": (-1, "DJF", "gpcc2025", ["precl", "gpcp"], P),
    "amazon": (-1, "ONDJFMAM", "gpcc2025", ["precl", "gpcp"], P),
    "nsam": (-1, "DJF", "gpcc2025", ["precl", "gpcp"], P),
    "nebrazil": (-1, "MAM1", "gpcc2025", ["precl", "gpcp"], P),
    "drycorridor": (-1, "DJF", "gpcc2025:drycorridor_wet", ["gpcc2025", "precl"], P),
    "wpacific": (-1, "SONDJF", "stations", ["gpcp"], P),
    "cpacific": (+1, "SONDJFMAM", "gpcp", ["stations"], P),
    "hawaii": (-1, "NDJFM", "stations", ["gpcp", "gpcc2025", "gpcc2025:box_hawaii"], P),
    "seaustralia": (-1, "SON", "gpcc2025", ["precl", "gpcc2025:box_seaustralia"], P),
    "inlandnw": (-1, "DJF", "gpcc2025", ["precl", "gpcc2025:box_inlandnw"], P),
    "ccanada_warm": (+1, "DJF", "berkeley", ["ghcncams", "berkeley:box_ccanada"], T),
    "nindia": (-1, "JJAS1", "gpcc2025", ["precl", "gpcc2025:lit_nindia"], P),  # removed from map v6
    "horn": (+1, "OND", "gpcc2025", ["precl", "gpcp", "gpcc2025:lit_horn"], P),
    "peru": (+1, "DJFMA", "gpcc2025", ["stations", "gpcc2025:lit_peru", "precl"], P),  # deviation: stations end ~2005
    "sesa": (+1, "SONDJF", "gpcc2025", ["precl", "gpcp", "gpcc2025:lit_sesa"], P),
    "gulf": (+1, "DJF", "gpcc2025", ["precl", "gpcc2025:lit_gulf"], P),
    "antilles": (+1, "DJF", "gpcc2025", ["precl", "gpcp", "gpcc2025:box_antilles"], P),
    "swus": (+1, "DJFM", "gpcc2025", ["precl"], P),
    "srilanka": (+1, "OND", "gpcc2025", ["precl", "gpcc2025:box_srilanka"], P),
    "schina": (+1, "DJFMAM", "gpcc2025", ["precl"], P),
    "yangtze": (+1, "JJA1", "gpcc2025", ["precl", "gpcc2025:lit_yangtze", "gpcc2025:yangtze@JJ1"], P),
    "mekong": (-1, "MAM1", "gpcc2025", ["gpcc2025:c_mekong_south", "precl:c_mekong_south"], P),  # added map v6
    "norcal": (+1, "DJFM", "gpcc2025", ["gpcc2025:c_norcal", "precl:c_norcal"], P),  # added map v6.1
    # Chile proposals (24 Sep 2026): seasons still ahead are primary; developing-year winter shown for context
    "cl_altiplano": (-1, "DJFM", "gpcc2025", ["precl:cl_altiplano"], P),
    "cl_atacama": (+1, "SON", "gpcc2025", ["gpcc2025:cl_atacama@JJA0", "gpcc2025:cl_atacama@JJASON0"], P),
    "cl_central": (+1, "SON", "gpcc2025", ["gpcc2025:cl_central@MAMJJAS1", "gpcc2025:cl_central@MAMJJAS0",
                                           "gpcc2025:cl_central@JJA0", "gpcc2025:cl_central@OND"], P),
    "cl_south": (-1, "DJF", "gpcc2025", ["precl:cl_south"], P),
    "cl_central_n": (+1, "ON0", "gpcc2025", ["gpcc2025:cl_central_n@SON", "gpcc2025:cl_central_n@MAMJJAS1"], P),
    "cl_south_n": (-1, "JFM1", "gpcc2025", ["gpcc2025:cl_south_n@DJF"], P),
    "altiplano": (-1, "DJFM", "gpcc2025", ["gpcc2025:cl_altiplano"], P),  # map v6.4
    "cchile": (+1, "ON0", "gpcc2025", ["gpcc2025:cl_central_n", "gpcc2025:cchile@SON"], P),  # map v6.4
    # not on the map (contrasts)
    "c_uk_ceurope": (+1, "OND", "gpcc2025", ["precl"], P),
    "c_scandinavia": (-1, "JF1", "berkeley", ["ghcncams"], T),
    "c_sahel": (-1, "JAS0", "gpcc2025", ["precl"], P),
    "lit_sindia": (+1, "OND", "gpcc2025", ["precl"], P),
    "c_mekong_south": (-1, "MAM1", "gpcc2025", ["precl"], P),
    "c_norcal": (+1, "DJFM", "gpcc2025", ["precl"], P),
    "lit_ohio": (-1, "DJF", "gpcc2025", ["precl"], P),
    "c_se_alaska": (+1, "DJF", "berkeley", ["ghcncams"], T),
    "nindia_yr0": (-1, "JJAS0", "gpcc2025:nindia", ["precl:nindia"], P),
}
CONTRASTS = [k for k in SPEC if k.startswith(("c_", "lit_")) or k in ("nindia_yr0", "nindia")]

# ---------------------------------------------------------------- load monthly series
def load():
    frames = []
    g = pd.read_csv(D / "gpcc_regional_monthly.csv", parse_dates=["time"])
    for extra in sorted(D.glob("gpcc_regional_monthly_*.csv")):
        g = pd.concat([g, pd.read_csv(extra, parse_dates=["time"])])
    frames.append(g[["dataset", "region", "time", "value", "ngauges"]])
    r = pd.read_csv(D / "regional_monthly.csv", parse_dates=["time"])
    frames.append(r[["dataset", "region", "time", "value"]])
    b = pd.read_csv(D / "be_regional_monthly.csv", parse_dates=["time"])
    frames.append(b[["dataset", "region", "time", "value"]])
    out = pd.concat(frames, ignore_index=True)
    # later re-extractions (e.g. *_coastfix) supersede empty rows for the same dataset/region/month
    out = out.sort_values("value", na_position="first").drop_duplicates(["dataset", "region", "time"], keep="last")
    return out

MON = load()
STA = pd.read_csv(D / "stations_monthly.csv", parse_dates=["time"])


def season_values(ts, season, how="mean"):
    """ts: monthly Series indexed by Timestamp. Returns Series indexed by year 0 (NaN unless complete)."""
    out = {}
    idx = {(t.year, t.month): v for t, v in ts.items()}
    for y in YEARS:
        vals = [idx.get((y + off, m), np.nan) for m, off in SEASON[season]]
        out[y] = np.nan if np.any(~np.isfinite(vals)) else (np.mean(vals) if how == "mean" else np.sum(vals))
    return pd.Series(out)


def station_index(group, season):
    """Mean over stations of (seasonal total / station neutral-year median); also count of stations."""
    ratios, counts = {}, {}
    sub = STA[STA.group == group]
    per = []
    for sid, s in sub.groupby("station"):
        sv = season_values(s.set_index("time").prcp_mm, season, how="sum")
        ref = sv.reindex(NEUTRAL).dropna()
        if len(ref) < 6:
            continue
        per.append(sv / ref.median())
    if not per:
        return None, None
    M = pd.concat(per, axis=1)
    return M.mean(axis=1, skipna=True), M.notna().sum(axis=1)


def series_for(source, region, season, var):
    """Returns (seasonal Series by year0, gauges/stations Series or None)."""
    ds, _, reg = source.partition(":")
    reg = reg or region
    if region == "nindia_yr0":
        reg = reg if reg != "nindia_yr0" else "nindia"
    if ds == "stations":
        return station_index(region, season)
    m = MON[(MON.dataset == ds) & (MON.region == reg)].set_index("time").sort_index()
    if m.empty:
        return None, None
    sv = season_values(m.value, season)
    gv = season_values(m.ngauges, season) if "ngauges" in m and m.ngauges.notna().any() else None
    return sv, gv


def percentiles(sv, var):
    """Detrend on neutral years (Theil-Sen for precip, LOWESS for temperature); percentile vs neutral residuals."""
    yrs = np.array([y for y in NEUTRAL if np.isfinite(sv.get(y, np.nan))])
    ref = sv.reindex(yrs).values
    if var == T:
        fit = lowess(ref, yrs, frac=0.5, return_sorted=True)
        trend = np.interp(sv.index.values, fit[:, 0], fit[:, 1])
    else:
        sl, ic, *_ = theilslopes(ref, yrs)
        trend = ic + sl * sv.index.values
    res = sv.values - trend
    rref = np.sort(res[np.isin(sv.index.values, yrs)])
    n = len(rref)
    pos = (np.arange(1, n + 1) - 0.5) / n
    pct = np.interp(res, rref, pos, left=0.0, right=1.0)
    pct[~np.isfinite(res)] = np.nan
    return pd.Series(pct, index=sv.index), pd.Series(res, index=sv.index), n


def pct_normal(sv, var):
    base = sv.reindex(range(1991, 2021)).mean()
    return (sv - base) if var == T else 100 * sv / base


def pct_typical(sv, res, var):
    """Relative to a *typical neutral year*: the neutral-year trend line plus the median neutral residual, i.e. the
    exact reference the hit test uses (a hit <=> pct_typical on the expected side of 100%, or of 0 °C).
    Precipitation: % of that reference. Temperature: anomaly (°C) from it. Added 25 Sep 2026 so published
    magnitudes use the same baseline as the hit counts."""
    ref_res = res.reindex([y for y in NEUTRAL if np.isfinite(res.get(y, np.nan))])
    typical = sv - res + float(np.median(ref_res.values))
    return (sv - typical) if var == T else 100 * sv / typical


# ---------------------------------------------------------------- run
events, summary = [], []
for region, (sign, season, main, sens, var) in SPEC.items():
    for cfg_src in [main] + sens:
        src_, _, season_o = cfg_src.partition("@")
        sv, qual = series_for(src_, region, season_o or season, var)
        if sv is None or sv.notna().sum() < 20:
            continue
        pct, res, nref = percentiles(sv, var)
        pn = pct_normal(sv, var)
        pt = pct_typical(sv, res, var)
        hit = (pct < 0.5) if sign < 0 else (pct > 0.5)
        terc = (pct < 1 / 3) if sign < 0 else (pct > 2 / 3)
        near = (pct >= 0.4) & (pct <= 0.6)
        for y in YEARS:
            events.append(dict(region=region, source=cfg_src, main=cfg_src == main, year0=y,
                               oni=ONI.get(y), roni=RONI.get(y), value=sv.get(y), pct=pct.get(y),
                               pct_normal=pn.get(y), pct_typical=pt.get(y) if np.isfinite(pct.get(y)) else None, hit=bool(hit.get(y)) if np.isfinite(pct.get(y)) else None,
                               tercile_hit=bool(terc.get(y)) if np.isfinite(pct.get(y)) else None,
                               near_normal=bool(near.get(y)), quality=None if qual is None else qual.get(y)))

        def rate(ys, h=hit, excl_near=False):
            ys = [y for y in ys if np.isfinite(pct.get(y, np.nan)) and not (excl_near and near.get(y))]
            return int(h.reindex(ys).sum()), len(ys)

        s_hit, s_n = rate(STRONG)
        loo = [rate([e for e in STRONG if e != x])[0] for x in STRONG]
        summary.append(dict(
            region=region, source=cfg_src, main=cfg_src == main, sign=sign, season=season, n_ref=nref,
            hits=s_hit, n=s_n, tercile_hits=rate(STRONG, terc)[0],
            hits_excl_near=f"{rate(STRONG, excl_near=True)[0]}/{rate(STRONG, excl_near=True)[1]}",
            hits_roni=f"{rate(STRONG_RONI)[0]}/{rate(STRONG_RONI)[1]}",
            hits_no2009=f"{rate([e for e in STRONG if e != 2009])[0]}/{rate([e for e in STRONG if e != 2009])[1]}",
            loo_range=f"{min(loo)}-{max(loo)}",
            moderate=f"{rate(MODERATE)[0]}/{rate(MODERATE)[1]}",
            lanina_same_dir=f"{rate(LANINA)[0]}/{rate(LANINA)[1]}",
            median_pct_strong=float(np.nanmedian(pct.reindex(STRONG))),
            median_pct_normal_strong=float(np.nanmedian(pn.reindex(STRONG))),
            median_pct_typical_strong=float(np.nanmedian(pt.reindex([y for y in STRONG if np.isfinite(pct.get(y, np.nan))]))),
            events_hit=" ".join(str(y)[2:] for y in STRONG if hit.get(y) is True or hit.get(y) == True),
        ))

ev = pd.DataFrame(events)
sm = pd.DataFrame(summary)
ev.to_csv(D / "hit_events.csv", index=False)
sm.to_csv(D / "hit_summary.csv", index=False)
pd.set_option("display.width", 250, "display.max_columns", 30, "display.max_rows", 200)
print(sm[sm.main][["region", "season", "source", "hits", "n", "tercile_hits", "hits_excl_near", "hits_roni",
                   "hits_no2009", "loo_range", "moderate", "lanina_same_dir", "median_pct_strong",
                   "median_pct_normal_strong", "median_pct_typical_strong", "events_hit"]].to_string(index=False))
