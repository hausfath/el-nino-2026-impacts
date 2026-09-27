#!/usr/bin/env python3.13
"""Data for the dashboard-style blog figures (figures/web/). Writes figures/web/figdata.json.

Nothing here is typed by hand. It reuses the logic of the matplotlib figure scripts it replaces:
  - hit grid rows, bins, checks and model counts: make_hit_grid.py (ROWS, bin5, model_txt)
  - global label positions / titles / details:    make_impacts_map.py (REGIONS)
  - regional footers:                              hit_rates/derived/*.csv, as make_regional_maps.py / _na.py
  - Europe fields, robust masks, NAO winters:      as make_europe_signal.py (metrics.nc, europe_table.csv, CPC)
The region polygons, observed record and per-model values come from the dashboard bundle
(Climate Dashboard/elnino_map/data/regions.json), so the figures match the live tab.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import shapely
import xarray as xr
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
FIG = HERE.parent
ROOT = FIG.parent
# the dashboard repo (github.com/hausfath/climate-dashboard): $CLIMATE_DASHBOARD, the local working copy, or a sibling clone
import os
DASH = next(p / "elnino_map" / "data" for p in [Path(os.environ["CLIMATE_DASHBOARD"])] * ("CLIMATE_DASHBOARD" in os.environ)
            + [ROOT.parents[1] / "Climate Dashboard", ROOT.parent / "climate-dashboard"] if (p / "elnino_map" / "data").exists())


def load_ns(script, upto, extra=None):
    src = (FIG / script).read_text()
    ns = {"__file__": str(FIG / script), **(extra or {})}
    exec(src[:src.index(upto)], ns)
    return ns


# ---------------------------------------------------------------- hit grid (make_hit_grid.py)
G = load_ns("make_hit_grid.py", "main = sm[sm.main]")
main = G["sm"][G["sm"].main].set_index("region")
ev = G["ev"]
STRONG = G["STRONG"]
grid = []
for g, key, lab, exp, spec in G["ROWS"]:
    r = main.loc[key]
    e = ev[(ev.region == key) & (ev.source == r.source) & (ev.year0.isin(STRONG))].set_index("year0")
    cells = []
    for yr in STRONG:
        p = e.pct.get(yr, np.nan)
        cells.append({"year": yr, "bin": None if not np.isfinite(p) else G["bin5"](p),
                      "hit": bool(e.hit.get(yr)) if np.isfinite(p) else None,
                      "pct_normal": None if not np.isfinite(e.pct_normal.get(yr, np.nan)) else round(float(e.pct_normal[yr]), 1)})
    mt, dag = G["model_txt"](key, spec)
    m = re.match(r"(\d+) of (\d+)", mt)
    grid.append({"group": g, "key": key, "label": lab, "exp": exp, "temp": key in G["TEMP"], "cells": cells,
                 "hits": int(r.hits), "n": int(r.n), "models": mt, "agree": int(m[1]) if m else None,
                 "mn": int(m[2]) if m else None, "dagger": dag or mt.endswith("†"), "lanina": r.get("lanina_same_dir")})
MODELS = {row["key"]: {"agree": row["agree"], "n": row["mn"], "dagger": row["dagger"]} for row in grid if row["agree"] is not None}

# ---------------------------------------------------------------- global labels (make_impacts_map.py)
src = (FIG / "make_impacts_map.py").read_text()
ns = {"Polygon": None, "HERE": FIG, "__file__": str(FIG / "make_impacts_map.py"), "pd": pd, "np": np, "json": json, "Path": Path}
exec(src[src.index("REGIONS = ["):src.index("FOOTER =")], ns)
labels = {k: {"lon": lxy[0], "lat": lxy[1], "title": t, "detail": d, "lead": ld, "align": al}
          for k, kind, conf, flag, shp, lxy, t, d, ld, al in ns["REGIONS"]}

# ---------------------------------------------------------------- footers (data-bound, as the regional scripts)
HS = pd.read_csv(ROOT / "hit_rates" / "derived" / "hit_summary.csv")
YJJ = HS[(HS.region == "yangtze") & (HS.source == "gpcc2025:yangtze@JJ1")].iloc[0]
HSm = HS[HS.main].set_index("region")
EV = pd.read_csv(ROOT / "hit_rates" / "derived" / "hit_events.csv")
hits = lambda k: f"{int(HSm.loc[k].hits)} of {int(HSm.loc[k].n)}"
PN = lambda k, y: f"{EV[(EV.region == k) & EV.main & (EV.year0 == y)].iloc[0].pct_normal:.0f}%"
misses = lambda k: [int(y) for y in EV[(EV.region == k) & EV.main & EV.year0.isin(STRONG) & (EV.hit == False)].year0]
ob = pd.read_csv(ROOT / "model_patterns" / "hindcast" / "data" / "obs_ca_winter_precip_enso.csv")
d6 = ob[(ob.region == "SoCal_d6") & (ob.decyear == 2015)].set_index("season").pct_normal_9120
hc = pd.read_csv(ROOT / "model_patterns" / "hindcast" / "data" / "nmme_event_table.csv")
hc = hc[hc.year == 2015]
assert misses("swus") == [2015]
sa_miss = misses("safrica")
footers = {
    "indo_pacific": f"Yangtze: wetter than a typical neutral summer in {hits('yangtze')} for Jun–Aug and {int(YJJ.hits)} of {int(YJJ.n)} for Jun–Jul "
                    f"(the Jun–Jul split was checked after the full-summer result). Central Pacific islands: satellite era only.",
    "india_note": f"India: a dry 2027 monsoon is not favoured (drier in {hits('nindia')} years after a strong El Niño)",
    "africa": f"Southern Africa's misses were {' and '.join(f'{y}–{str(y + 1)[2:]}' for y in sa_miss)}. 1997–98 came in at {PN('safrica', 1997)} "
              f"of the 1991–2020 average, and 2023–24, the driest of the eight, at {PN('safrica', 2023)}.",
    "sahel_note": f"Sahel: no reliable El Niño signal (drier in only {hits('c_sahel')} strong events)",
    "south_america": f"Peru / Ecuador coast: flooding rains in 1982–83 ({PN('peru', 1982)} of the 1991–2020 average) and 1997–98 ({PN('peru', 1997)}), "
                     "both with very warm coastal water, as in 2026. Other strong events ranged from somewhat below to somewhat above average.",
    "north_america": f"S California missed only in 2015–16: the coast got {d6['DJF']:.0f}–{d6['JFM']:.0f}% of its 1991–2020 average, though "
                     f"{int((hc.SoCal_d6_DJF_pct > 100).sum())} of {len(hc)} models rerun from Sep 2015 predicted a wet winter.",
}

# ---------------------------------------------------------------- Europe (make_europe_signal.py)
MP = ROOT / "model_patterns" / "derived"
m = xr.open_dataset(MP / "metrics.nc")
tab = pd.read_csv(MP / "europe_table.csv")
lon = np.where(m.lon.values > 180, m.lon.values - 360, m.lon.values)
order = np.argsort(lon)
lon, lat = lon[order], m.lat.values
z = lambda name: m[name].values[:, order]
trob = (((m.t_robust_JF > 0) & (m.t91_robust_JF > 0) & (m.tlmr_robust_JF > 0)) |
        ((m.t_robust_JF < 0) & (m.t91_robust_JF < 0) & (m.tlmr_robust_JF < 0))).values[:, order]
LO, LA = (lon >= -30) & (lon <= 60), (lat >= 28) & (lat <= 76)
cut = lambda f: np.round(np.where(np.isfinite(f), f, np.nan)[np.ix_(LA, LO)], 3)
panels = []
for title, f, rob, cmap in [("Rain & snow, Oct–Dec", z("pr_z_OND"), z("pr_robust_OND") != 0, "pr"),
                            ("Rain & snow, Jan–Feb", z("pr_z_JF"), z("pr_robust_JF") != 0, "pr"),
                            ("Temperature, Jan–Feb (trend removed)", z("t_z_JF"), trob, "t")]:
    v = cut(f)
    panels.append({"title": title, "cmap": cmap, "z": [[None if not np.isfinite(x) else float(x) for x in row] for row in v],
                   "robust": cut(rob.astype(float)).astype(int).tolist()})
o_ = xr.open_dataset(MP / "obs_ref.nc")
L2, A2 = np.meshgrid(np.where(m.lon > 180, m.lon - 360, m.lon), m.lat.values)
eu = shapely.contains_xy(box(-11, 35, 40, 71), L2, A2) & o_.land.values.astype(bool)
Wt = np.cos(np.deg2rad(A2))
frac = lambda x: 100 * float((Wt * (x & eu)).sum() / (Wt * eu).sum())
f_ond, f_jf = frac(m.pr_robust_OND.values != 0), frac(m.pr_robust_JF.values != 0)
f_t = frac(((m.t_robust_JF != 0) & (np.sign(m.t_robust_JF) == np.sign(m.tlmr_robust_JF)) & (m.t91_robust_JF != 0)).values)
val = lambda region, var, season, col: tab[(tab.region == region) & (tab["var"] == var) & (tab.season == season)].iloc[0][col]
txt = requests.get("https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii", timeout=60).text
nao = {(int(a), int(b)): float(c) for a, b, c in (l.split() for l in txt.splitlines() if len(l.split()) == 3)}
oni = {}
for l in requests.get("https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt", timeout=60).text.splitlines()[1:]:
    q = l.split()
    if len(q) == 4:
        oni[(q[0], int(q[1]))] = float(q[3])
winters = [y + 1 for y in range(1950, 2026) if oni.get(("NDJ", y), -9) >= 1.5 and (y, 12) in nao and (y + 1, 2) in nao]
djf = [round(float(np.mean([nao[(y - 1, 12)], nao[(y, 1)], nao[(y, 2)]])), 2) for y in winters]
assert [w - 1 for w in winters] == STRONG, (winters, STRONG)
europe = {
    "lon": lon[LO].tolist(), "lat": lat[LA].tolist(), "panels": panels,
    "robust_pct": {"pr_OND": round(f_ond), "pr_JF": round(f_jf), "t_JF": round(f_t)},
    "nao": [{"winter": w, "djf": v} for w, v in zip(winters, djf)],
    "uk_pos": int(val("UK & Ireland", "pr", "OND", "models_pos")),
    "uk_n": int(val("UK & Ireland", "pr", "OND", "models_pos") + val("UK & Ireland", "pr", "OND", "models_neg")),
    "sc_neg": int(val("Scandinavia & Baltic", "t", "JF", "models_neg")),
    "sc_n": int(val("Scandinavia & Baltic", "t", "JF", "models_pos") + val("Scandinavia & Baltic", "t", "JF", "models_neg")),
    "shift_lo": round(float(min(val("UK & Ireland", "pr", "OND", "mmm_z"), val("Central Europe", "pr", "OND", "mmm_z"))), 1),
    "shift_hi": round(float(abs(val("Scandinavia & Baltic", "t", "JF", "mmm_z"))), 1),
}

meta = json.loads((DASH / "meta.json").read_text())
import sys as _sys; _sys.path.insert(0, str(ROOT / "model_patterns")); import windows as WN   # noqa: E402
out = {"grid": grid, "models": MODELS, "labels": labels, "footers": footers, "europe": europe,
       "stats": {"aggregate": meta["aggregate"], "p2027": meta["p2027_warmest"], "strong": STRONG,
                 "oni": meta["oni_ndj_strong"], "init": meta["init"], "n_regions": meta["n_map_regions"],
                 "horizon": WN.label([WN.ALL_END]), "nmme_horizon": WN.label([WN.NMME_END])}}
(HERE / "figdata.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("figdata.json:", len(grid), "grid rows,", len(labels), "labels, NAO", djf, "| Europe robust %", europe["robust_pct"],
      "| UK", europe["uk_pos"], "/", europe["uk_n"], "Scand", europe["sc_neg"], "/", europe["sc_n"], europe["shift_lo"], europe["shift_hi"])
for k, v in footers.items():
    print(f"  {k}: {v}")
