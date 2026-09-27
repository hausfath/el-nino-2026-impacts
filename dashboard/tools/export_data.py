#!/usr/bin/env python3.13
"""Export everything the video draws from the El Niño impacts analysis into small files under data/.

Outputs
  data/geo.json        Natural Earth 50m land rings + country borders (lon/lat, simplified)
  data/regions.json    impact-map regions exactly as figures/make_impacts_map.py builds them
                       (shape, tier, fill colour, dashed flag, labels) + observed hit record
                       (hit_rates/derived/hit_events.csv, main source) + this year's model values
  data/fields.json     robust-agreement dots per season (lon/lat of cells where >=80% of models
                       share the sign of the multi-model mean), extents of the raster PNGs
  src/img/pr_<S>.png   multi-model mean precipitation, % of GPCP 1991–2020 normal, RGBA (alpha ~ |anomaly|)
  src/img/sst_DJF.png  NMME mean surface-temperature anomaly Dec–Feb over ocean (3 models on a
                       1992–2019 baseline), for the intro
  data/stats.json      numbers the narration quotes, computed here (tools/check_numbers.mjs asserts them)

Model-count method is identical to hit_rates/model_counts.py (cell centres inside the polygon, land only
except island/ocean regions, cos-lat weights) and is asserted against hit_rates/derived/model_counts.csv.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import shapely
from shapely.geometry import Polygon, shape, mapping
from shapely import affinity
from scipy.ndimage import zoom, gaussian_filter
import cartopy.io.shapereader as shpreader
from PIL import Image
import sys

VID = Path(__file__).resolve().parent.parent
ROOT = VID.parent
sys.path.insert(0, str(ROOT / "hit_rates"))
from extract import SHAPES, OCEAN_OK  # noqa: E402  (same shapes the hit rates were computed on)

DATA = VID / "data"
IMG = VID / "src" / "img" if (VID / "src").exists() else VID / "img"   # video project vs public repo (dashboard/)
DATA.mkdir(exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- map regions (published map v6.4)
src = (ROOT / "figures" / "make_impacts_map.py").read_text()
ns = {"Polygon": Polygon}
exec(src[src.index("DRY = {"):src.index("LAT_S")], ns)
exec(src[src.index("REGIONS = ["):src.index("FOOTER =")], ns)
DRY, WET, WARM, EDGE = ns["DRY"], ns["WET"], ns["WARM"], ns["EDGE"]
MODEL = {k: shape(v) for k, v in json.loads((ROOT / "model_patterns" / "derived" / "model_polygons.json").read_text()).items()}
BUF = {"peru": 0.8, "mekong": 0.8, "norcal": 0.3, "altiplano": 0.3, "cchile": 0.2}


def to180(g):
    """Shift a polygon so its centroid lies in [-180, 180) (keeps vertices continuous across the dateline)."""
    c = g.centroid.x
    return affinity.translate(g, -360) if c >= 180 else g


def rings(g):
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys]


# ---------------------------------------------------------------- model fields
a = xr.open_dataset(ROOT / "model_patterns" / "derived" / "seasonal_anoms.nc")
o = xr.open_dataset(ROOT / "model_patterns" / "derived" / "obs_ref.nc")
lat, lon = a.lat.values, a.lon.values
LON2, LAT2 = np.meshgrid(lon, lat)
Wt = np.cos(np.deg2rad(LAT2))
land = o.land.values.astype(bool)
NMME = ["CFSv2", "CanESM5", "GEM5.2_NEMO", "NASA_GEOS5v2", "NCAR_CCSM4", "NCAR_CESM1"]
C3S = ["ecmwf", "ukmo", "meteo_france", "dwd", "cmcc", "jma", "bom"]
LABEL = {"CFSv2": "NOAA CFSv2", "CanESM5": "Canada CanESM5", "GEM5.2_NEMO": "Canada GEM5.2", "NASA_GEOS5v2": "NASA GEOS",
         "NCAR_CCSM4": "NCAR CCSM4", "NCAR_CESM1": "NCAR CESM1", "ecmwf": "ECMWF", "ukmo": "UK Met Office",
         "meteo_france": "Météo-France", "dwd": "DWD Germany", "cmcc": "CMCC Italy", "jma": "JMA Japan", "bom": "BoM Australia"}


def ens(season):
    return NMME + C3S if season in ("SON", "OND", "DJF", "JF") else NMME


def clim(season):
    return o[f"pr_clim_{season}"].values


# per-region model values, same method as hit_rates/model_counts.py
REG = {  # region: (sign, model season)   (precipitation only; temperature regions not featured)
    "maritime": (-1, "SON"), "philippines": (-1, "DJF"), "safrica": (-1, "DJF"), "amazon": (-1, "DJF"),
    "nsam": (-1, "DJF"), "nebrazil": (-1, "MAM"), "drycorridor": (-1, "DJF"), "wpacific": (-1, "SON"),
    "cpacific": (1, "SON"), "hawaii": (-1, "DJF"), "seaustralia": (-1, "SON"), "inlandnw": (-1, "DJF"),
    "horn": (1, "OND"), "peru": (1, "DJF"), "sesa": (1, "DJF"), "gulf": (1, "DJF"), "antilles": (1, "DJF"),
    "swus": (1, "DJF"), "srilanka": (1, "OND"), "schina": (1, "DJF"), "mekong": (-1, "MAM"),
    "norcal": (1, "DJF"), "altiplano": (-1, "DJF"), "cchile": (1, "OND"),
    "lit_sindia": (1, "OND"), "lit_ohio": (-1, "DJF"), "c_uk_ceurope": (1, "OND"),
}
mc = pd.read_csv(ROOT / "hit_rates" / "derived" / "model_counts.csv").set_index("region")
models = {}
for r, (sign, s) in REG.items():
    g = SHAPES[r]
    msk = shapely.contains_xy(g, LON2, LAT2)
    if r not in OCEAN_OK:
        msk &= land
    if msk.sum() == 0:
        msk = shapely.contains_xy(g.buffer(0.75), LON2, LAT2) & (land | (r in OCEAN_OK))
    cl = clim(s)
    rows = []
    for m in ens(s):
        f = a.prate.sel(model=m, season=s).values
        ok = msk & np.isfinite(f)
        an = np.sum(f[ok] * Wt[ok]) / np.sum(Wt[ok])
        c = np.sum(cl[ok] * Wt[ok]) / np.sum(Wt[ok])
        rows.append({"model": m, "label": LABEL[m], "anom": round(float(an), 3), "pct": round(float(100 * an / c), 1),
                     "agree": bool(np.sign(an) == sign)})
    agree = sum(x["agree"] for x in rows)
    assert agree == mc.loc[r, "agree"] and len(rows) == mc.loc[r, "n"], (r, agree, mc.loc[r].to_dict())
    models[r] = {"season": s, "sign": sign, "n": len(rows), "agree": agree, "members": rows,
                 "mmm_pct": round(float(np.mean([x["pct"] for x in rows])), 1)}
print("model counts match hit_rates/derived/model_counts.csv for", len(models), "regions")

# ---------------------------------------------------------------- observed hit record
STRONG = [1957, 1965, 1972, 1982, 1997, 2009, 2015, 2023]
TEMP_REGIONS = {"ccanada_warm", "c_scandinavia", "c_se_alaska"}   # pct_normal/pct_typical are °C anomalies there
ev = pd.read_csv(ROOT / "hit_rates" / "derived" / "hit_events.csv")
ev = ev[ev.main & ev.year0.isin(STRONG)]
summ = pd.read_csv(ROOT / "hit_rates" / "derived" / "hit_summary.csv")
summ = summ[summ.main == True].set_index("region")  # noqa: E712
# Bars are % of the 1991–2020 mean (pct_normal, the numbers the post quotes). Each event also carries the
# *typical neutral year* on that same scale (typ_level = pct_normal / pct_typical × 100), i.e. the reference the hit
# test uses (hit_rates/analyze.py pct_typical, added 25 Sep 2026). A check <=> the bar ends beyond the marker.
hits = {}
for r, grp in ev.groupby("region"):
    grp = grp.sort_values("year0")
    hits[r] = {
        "source": grp.source.iloc[0], "season": summ.loc[r, "season"], "sign": int(summ.loc[r, "sign"]),
        "hits": int(summ.loc[r, "hits"]), "n": int(summ.loc[r, "n"]),
        "median_pct_normal": round(float(summ.loc[r, "median_pct_normal_strong"]), 1),
        "median_pct_typ": round(float(summ.loc[r, "median_pct_typical_strong"]), 1),
        "lanina_same_dir": summ.loc[r, "lanina_same_dir"],
        "events": [{"year": int(y), "pct_normal": None if not np.isfinite(p) else round(float(p), 1),
                    "percentile": None if not np.isfinite(q) else round(float(q), 3),
                    "hit": None if pd.isna(h) else bool(h),
                    "pct_typ": None if pd.isna(pt) or pd.isna(h) else round(float(pt), 1),
                    "typ_level": None if pd.isna(pt) or pd.isna(h) or r in TEMP_REGIONS else round(float(100 * p / pt), 1)}
                   for y, p, q, h, pt in zip(grp.year0, grp.pct_normal, grp.pct, grp.hit, grp.pct_typical)],
    }
    for e in hits[r]["events"]:   # bar vs marker must match the check
        if e["hit"] is not None and e["typ_level"] is not None:
            assert (e["pct_normal"] > e["typ_level"]) == ((hits[r]["sign"] > 0) == e["hit"]), (r, e)
    assert sum(bool(e["hit"]) for e in hits[r]["events"]) == hits[r]["hits"], r
    assert sum(e["hit"] is not None for e in hits[r]["events"]) == hits[r]["n"], r

# ---------------------------------------------------------------- region records
regions = {}
for key, kind, conf, flag, shp, lxy, title, detail, leader, align in ns["REGIONS"]:
    g = MODEL[key] if shp == "model" else Polygon(shp).buffer(BUF.get(key, 2.0), join_style=1).simplify(0.25)
    g = to180(g)
    fill = {"dry": DRY, "wet": WET, "warm": WARM}[kind][conf]
    regions[key] = {"kind": kind, "conf": conf, "dashed": flag == "busted", "fill": fill, "edge": EDGE[kind],
                    "title": title, "detail": detail, "rings": rings(g),
                    "centroid": [round(g.representative_point().x, 2), round(g.representative_point().y, 2)],
                    "bounds": [round(v, 2) for v in g.bounds],
                    "hits": hits.get(key), "models": models.get(key)}
# removed / not-mapped regions used in the "myths" beat
EXTRA = {"nindia": "N & central India monsoon (Jun–Sep 2027)", "nindia_yr0": "N & central India monsoon, developing year (Jun–Sep)", "lit_ohio": "Ohio Valley (Dec–Feb)",
         "c_uk_ceurope": "UK & central Europe (Oct–Dec)", "c_scandinavia": "Scandinavia cold (Jan–Feb)"}
extras = {}
for k, name in EXTRA.items():
    g = to180(SHAPES.get(k.replace("_yr0", ""), SHAPES.get("lit_" + k.replace("lit_", "").replace("_yr0", ""))))
    extras[k] = {"title": name, "rings": rings(g.simplify(0.25)), "hits": hits.get(k), "models": models.get(k)}

# aggregate over the regions on the map
on_map = [k for k in regions if regions[k]["hits"]]
agg_hits = sum(regions[k]["hits"]["hits"] for k in on_map)
agg_n = sum(regions[k]["hits"]["n"] for k in on_map)
by_event = {y: [0, 0] for y in STRONG}
for k in on_map:
    for e in regions[k]["hits"]["events"]:
        if e["hit"] is not None:
            by_event[e["year"]][0] += e["hit"]; by_event[e["year"]][1] += 1
def frac(col):
    h = n = 0
    for k in on_map:
        v = summ.loc[k, col]
        if isinstance(v, str) and "/" in v:
            a_, b_ = map(int, v.split("/")); h += a_; n += b_
    return h, n
lanina_h, lanina_n = frac("lanina_same_dir")
mod_h, mod_n = frac("moderate")
print(f"La Niña years on the El Niño side: {lanina_h}/{lanina_n}; moderate El Niños: {mod_h}/{mod_n}")
print(f"aggregate: {agg_hits}/{agg_n} over {len(on_map)} regions = {100*agg_hits/agg_n:.1f}%")
print("by event:", {y: f"{h}/{n}" for y, (h, n) in by_event.items()})

# ---------------------------------------------------------------- rasters
FLD_RES = 8        # pixels per degree
EXT = [-180, 180, -90, 90]


def roll180(f):
    """0..359 grid -> -180..179 grid."""
    return np.roll(f, 180, axis=-1)


def upsample(f, fill=0.0):
    f = np.where(np.isfinite(f), f, fill)
    f = np.concatenate([f, f[:, :1]], axis=1)       # wrap column so -180 and +180 match
    z = zoom(f, FLD_RES, order=3)
    return z[:180 * FLD_RES, :360 * FLD_RES]


def cmap(stops):
    xs = np.array([s[0] for s in stops]); cs = np.array([[int(s[1][i:i + 2], 16) for i in (1, 3, 5)] for s in stops])
    return lambda v: np.stack([np.interp(v, xs, cs[:, k]) for k in range(3)], -1)


PR_STOPS = cmap([(-100, "#7A3E06"), (-60, "#B4651A"), (-30, "#E3A24A"), (-10, "#D8A057"), (0, "#F5EEDC"),
                 (10, "#7FB6E3"), (30, "#6FB4E6"), (60, "#2F86D6"), (100, "#1D5FB8")])
dots, meta = {}, {}
for s in ["SON", "OND", "DJF", "MAM"]:
    arr = np.array([a.prate.sel(model=m, season=s).values for m in ens(s)])
    mm = arr.mean(0)
    cl = clim(s)
    dry = (cl < 0.5) & land
    pct = np.where(dry, np.nan, 100 * mm / np.where(cl > 0, cl, np.nan))
    pct = np.clip(pct, -100, 150)
    agree = (np.mean(np.sign(arr) == np.sign(mm), 0) >= 0.8 - 1e-9) & ~dry & np.isfinite(pct)
    # dots only where the signal is also non-trivial (|anomaly| >= 10% of normal), as a visual threshold
    sel = agree & (np.abs(pct) >= 10)
    jj, ii = np.where(sel)
    dots[s] = [[int(((lon[i] + 180) % 360) - 180), int(lat[j])] for j, i in zip(jj, ii)]
    P = upsample(roll180(pct), 0.0)
    V = np.clip(zoom(np.concatenate([gaussian_filter(roll180(np.isfinite(pct).astype(float)), 0.7, mode="wrap")] * 1, 1), FLD_RES, order=1), 0, 1)[:180 * FLD_RES, :360 * FLD_RES]
    V = np.clip((V - 0.35) / 0.3, 0, 1)
    rgb = PR_STOPS(np.clip(P, -100, 100))
    alpha = np.clip((np.abs(P) - 5) / 40, 0, 1) ** 0.85 * 235 * V
    img = np.dstack([rgb, alpha]).astype(np.uint8)
    Image.fromarray(img, "RGBA").save(IMG / f"pr_{s}.png", optimize=True)
    meta[s] = {"n": len(ens(s)), "extent": EXT, "robust_cells": int(sel.sum())}
    print(f"pr_{s}.png  {img.shape[1]}x{img.shape[0]}  dots {len(dots[s])}")

# SST DJF (3 NMME models sharing the 1992–2019 baseline); target 803 = DJF start month Dec
sst = []
for m in ["CFSv2", "NASA_GEOS5v2", "NCAR_CCSM4"]:
    d = xr.open_dataset(ROOT / "model_patterns" / "raw" / "nmme_202609_sst" / f"{m}.tmpsfc.anom.nc", decode_times=False)
    f = d.fcst.sel(target=[803.0, 804.0, 805.0]).mean("target").values  # Dec, Jan, Feb
    sst.append(f)
sst = np.mean(sst, 0)
sst = np.where(land, np.nan, sst)
# display only: taper outside the tropics (30°S–30°N shown); the hook is about the tropical Pacific
sst_disp = sst * np.clip((32 - np.abs(LAT2)) / 10, 0, 1)
nino34 = float(np.nanmean(sst[(LAT2 >= -5) & (LAT2 <= 5) & (LON2 >= 190) & (LON2 <= 240)]))
S = upsample(roll180(gaussian_filter(np.where(np.isfinite(sst_disp), sst_disp, 0), 0.6)), 0.0)
V = upsample(roll180(np.isfinite(sst).astype(float)), 0.0)
SST_STOPS = cmap([(-3, "#3B6FD9"), (-1, "#6F95E0"), (0, "#1a1a1a"), (0.8, "#7A2E14"), (1.6, "#D2542C"), (2.6, "#EF3B3F"), (3.6, "#FF7A4D"), (4.6, "#FFE29A")])
rgb = SST_STOPS(np.clip(S, -3, 5))
alpha = np.where(S > 0, np.clip((S - 0.7) / 1.6, 0, 1), np.clip((-S - 0.4) / 1.2, 0, 1)) ** 0.9 * 240 * np.clip(V, 0, 1)
Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA").save(IMG / "sst_DJF.png", optimize=True)
print(f"sst_DJF.png  Niño 3.4 box mean of the 3-model DJF SST anomaly: {nino34:.2f} °C (vs 1992–2019)")

# ---------------------------------------------------------------- geography
def ne(name, cat="physical"):
    return shpreader.Reader(shpreader.natural_earth(resolution="50m", category=cat, name=name)).geometries()


land_rings = []
for g in ne("land"):
    for p in ([g] if g.geom_type == "Polygon" else g.geoms):
        p = p.simplify(0.04, preserve_topology=True)
        if p.area < 0.08:
            continue
        land_rings.append([[round(x, 2), round(y, 2)] for x, y in p.exterior.coords])
borders = []
for g in ne("admin_0_boundary_lines_land", "cultural"):
    for ls in ([g] if g.geom_type == "LineString" else g.geoms):
        ls = ls.simplify(0.05)
        borders.append([[round(x, 2), round(y, 2)] for x, y in ls.coords])
states = []
for rec in shpreader.Reader(shpreader.natural_earth(resolution="50m", category="cultural", name="admin_1_states_provinces_lakes")).records():
    if rec.attributes.get("admin") not in ("United States of America",):
        continue
    g = rec.geometry
    for p in ([g] if g.geom_type == "Polygon" else g.geoms):
        p = p.simplify(0.05)
        states.append([[round(x, 2), round(y, 2)] for x, y in p.exterior.coords])

# ---------------------------------------------------------------- hindcast (California) + Peru
hc = pd.read_csv(ROOT / "model_patterns" / "hindcast" / "data" / "nmme_event_table.csv")
obs = pd.read_csv(ROOT / "model_patterns" / "hindcast" / "data" / "obs_ca_winter_precip_enso.csv")
cal = {}
for y in [1982, 1997, 2015]:
    h = hc[hc.year == y]
    o_ = obs[(obs.decyear == y) & (obs.season == "DJF") & (obs.region == "SoCal_d6")].pct_normal_9120.iloc[0]
    cal[y] = {"obs_pct": round(float(o_), 1),
              "models": [{"model": m, "pct": float(p)} for m, p in zip(h.model, h.SoCal_d6_DJF_pct)],
              "n": int(len(h)), "n_wet": int((h.SoCal_d6_DJF_pct > 100).sum())}
mem = pd.read_csv(ROOT / "model_patterns" / "hindcast" / "data" / "summary_member_strong_events.csv")
mem = mem[(mem.region == "SoCal_d6") & (mem.season == "DJF")].iloc[0]
HD = ROOT / "model_patterns" / "hindcast" / "data"
Mm = pd.read_csv(HD / "nmme_member_pct_normal.csv").merge(
    pd.read_csv(HD / "nmme_sepinit_regional_series.csv")[["model", "year", "nino34_NDJ_model"]].drop_duplicates(), on=["model", "year"])
g = Mm[(Mm.nino34_NDJ_model >= 2.0) & (Mm.year <= 2025) & (Mm.region == "SoCal_d6") & (Mm.season == "DJF")]
obs15 = cal[2015]["obs_pct"]
cal_members = {"n_members": int(len(g)), "n_models": int(g.model.nunique()),
               "frac_below_normal": round(float((g.pct_normal < 100).mean()), 3),
               "frac_below70": round(float((g.pct_normal < 70).mean()), 3),
               "frac_at_or_below_2015": round(float((g.pct_normal <= obs15).mean()), 3), "obs_2015": obs15,
               "members_pct": sorted(round(float(v), 1) for v in g.pct_normal)}
assert cal_members["n_members"] == int(mem.n_members) and abs(cal_members["frac_below70"] - mem.frac_below70_pooled) < 1e-3
peru = pd.read_csv(ROOT / "model_patterns" / "derived" / "peru_nino12.csv").set_index("event")

# 2027 record odds from Zeke's operational GMST forecast (a separate workflow; 6-dataset blend, 14-model ENSO plume,
# 1850-1900 baseline): P(2027 ranks warmest on record), ONI and RONI conventions
# The forecast lives in a separate private workflow; when it is present, refresh the small extract in data/ that the
# public repo carries (the four numbers used here), otherwise read that extract.
_lp = ROOT / "local_paths.json"      # local-only (git-ignored): where the forecast run lives on this machine
FC = Path(json.loads(_lp.read_text())["forecast_dir"]) if _lp.exists() else ROOT / "no_local_forecast"
EXTRACT = ROOT / "data" / "forecast_2027_extract.json"
if (FC / "rank_probabilities_wide.csv").exists():
    rk = pd.read_csv(FC / "rank_probabilities_wide.csv").set_index(["approach", "year"])
    p2027 = {a: round(float(rk.loc[(a, 2027), "P(rank=1)"]), 3) for a in ["ONI", "RONI"]}
    fc_meta = json.loads((FC / "forecast_2026_2027_results.json").read_text())
    EXTRACT.parent.mkdir(exist_ok=True)
    EXTRACT.write_text(json.dumps({"p2027_rank1": p2027, "n_models": fc_meta["n_models"], "n_members": fc_meta["n_members"],
                                   "source": "Z. Hausfather operational global temperature forecast, Sep 2026 run (6-dataset blend, "
                                             "multi-model ENSO plume, 1850-1900 baseline): P(2027 ranks warmest on record), ONI and RONI conventions"}, indent=1))
else:
    _x = json.loads(EXTRACT.read_text())
    p2027, fc_meta = _x["p2027_rank1"], {"n_models": _x["n_models"], "n_members": _x["n_members"]}
oni = {}
for l in (ROOT / "oni_cpc_2026-09-15.txt").read_text().splitlines()[1:]:
    q = l.split()
    if q[0] == "NDJ" and int(q[1]) in STRONG:
        oni[int(q[1])] = float(q[3])
assert len(oni) == 8 and min(oni.values()) >= 1.5

stats = {
    "p2027_warmest": p2027, "forecast_models": fc_meta["n_models"], "forecast_members": fc_meta["n_members"],
    "oni_ndj_strong": oni,
    "aggregate_hits": agg_hits, "lanina_same": [lanina_h, lanina_n], "moderate_hits": [mod_h, mod_n],
    "nindia_yr0": [int(summ.loc["nindia_yr0", "hits"]), int(summ.loc["nindia_yr0", "n"])],
    "yangtze_jj_posthoc": [int(r.hits), int(r.n)] if (r := pd.read_csv(ROOT / "hit_rates" / "derived" / "hit_summary.csv").query("region == 'yangtze' and source == 'gpcc2025:yangtze@JJ1'").iloc[0]) is not None else None, "aggregate_n": agg_n, "n_map_regions": len(regions), "by_event": by_event,
    "cal_hindcast": cal, "cal_members_djf": cal_members, "sst_nino34_djf_3model": round(nino34, 2),
    "peru_nino12_midSep": {e: float(peru.loc[e, "obs_midSep"]) for e in peru.index},
    "peru_nmme_jfm_min": float(peru.loc["2026-27", "nmme_JFM_min"]),
    "peru_nino12": {e: {c: (None if pd.isna(v) else float(v)) for c, v in peru.loc[e].items()} for e in peru.index},
    "strong_events": STRONG,
}

json.dump({"land": land_rings, "borders": borders, "states": states}, open(DATA / "geo.json", "w"), separators=(",", ":"))
json.dump({"regions": regions, "extras": extras}, open(DATA / "regions.json", "w"), separators=(",", ":"), ensure_ascii=False)
json.dump({"dots": dots, "meta": meta}, open(DATA / "fields.json", "w"), separators=(",", ":"))
json.dump(stats, open(DATA / "stats.json", "w"), indent=1)
for f in ["geo.json", "regions.json", "fields.json", "stats.json"]:
    print(f, f"{(DATA / f).stat().st_size / 1e3:.0f} kB")
print("California SoCal DJF hindcast:", {y: f"{v['n_wet']}/{v['n']} wet, obs {v['obs_pct']}%" for y, v in cal.items()})
