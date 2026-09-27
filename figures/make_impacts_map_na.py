#!/usr/bin/env python3.13
"""North America close-up of the El Niño 2026-27 impacts map (for social sharing).

Region tiers, flags and shapes are read from make_impacts_map.py (REGIONS block) and
model_patterns/derived/model_polygons.json, so this map cannot drift from the global one.
Only labels/layout are defined here. Numbers in the footer come from
model_patterns/hindcast/ (see figures/NOTES.md).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import shape, Polygon
from shapely import affinity

HERE = Path(__file__).resolve().parent
src = (HERE / "make_impacts_map.py").read_text()
ns = {}
exec(src[src.index("# confidence -> fill"):src.index("LAT_S, LAT_N")], ns)   # palettes
exec(src[src.index("REGIONS = ["):src.index("FOOTER =")], ns)
DRY, WET, WARM, EDGE = ns["DRY"], ns["WET"], ns["WARM"], ns["EDGE"]
GLOBAL = {r[0]: r for r in ns["REGIONS"]}
MODEL = {k: shape(v) for k, v in json.loads(
    (HERE.parent / "model_patterns" / "derived" / "model_polygons.json").read_text()).items()}

# key: (label lon/lat, title override or None, detail override or None, align)
NA = {
    "inlandnw": ((-146, 56), "Interior BC, N Rockies\n& inland Northwest", None, "c"),
    "ccanada_warm": ((-73, 62.5), None, None, "l"),
    "swus": ((-131, 27), "S California, US Southwest\n& N Mexico", "wet · Dec–Mar", "c"),
    "norcal": ((-137, 41), "N California", "wet · Dec–Mar", "c"),
    "gulf": ((-68, 36), None, None, "l"),
    "antilles": ((-66, 26.5), None, None, "l"),
    "drycorridor": ((-97, 10.5), None, None, "r"),
}

INK, SUB = "#1A1A1A", "#4A4A4A"
plt.rcParams["font.family"] = "DejaVu Sans"
pc = ccrs.PlateCarree()
proj = ccrs.LambertConformal(central_longitude=-98, central_latitude=40, standard_parallels=(25, 55))

fig = plt.figure(figsize=(12, 10), facecolor="white")
ax = fig.add_axes([0.02, 0.15, 0.96, 0.70], projection=proj)
ax.set_extent([-138, -58, 8, 64], crs=pc)
ax.add_feature(cfeature.LAND, facecolor="#E9E7E1", edgecolor="none")
ax.add_feature(cfeature.LAKES, facecolor="white", edgecolor="#B7B3AA", linewidth=0.3)
ax.add_feature(cfeature.COASTLINE, linewidth=0.4, edgecolor="#B7B3AA")
ax.add_feature(cfeature.BORDERS, linewidth=0.4, edgecolor="#C9C5BC")
ax.add_feature(cfeature.STATES, linewidth=0.2, edgecolor="#D5D1C8")
ax.spines["geo"].set_edgecolor("#CCC9C2")


def xy(a, lon, lat):
    return a.projection.transform_point(lon, lat, pc)


def draw(a, key, lxy=None, title=None, detail=None, align="c", fs=(11, 10)):
    _, kind, conf, flag, shp, _, gtitle, gdetail, leader, _ = GLOBAL[key]
    poly = MODEL[key] if shp == "model" else Polygon(shp).buffer({"norcal": 0.3}.get(key, 2.0), join_style=1)
    if a is not ax and poly.bounds[0] > 180:  # inset uses -180..180 longitudes
        poly = affinity.translate(poly, xoff=-360)
    fill = {"dry": DRY, "wet": WET, "warm": WARM}[kind][conf]
    a.add_geometries([poly], crs=pc, facecolor=fill, alpha=0.88, edgecolor=EDGE[kind],
                     linewidth=1.5 if flag == "busted" else 0.8,
                     linestyle=(0, (4, 2)) if flag == "busted" else "solid", zorder=3)
    if lxy is None:
        return
    rp = poly.representative_point()
    lead = leader or (rp.x, rp.y)
    a.plot(*xy(a, *lead), marker="o", ms=3.6, color="#333333", mec="white", mew=0.6, zorder=6)
    ta = {"l": "left", "r": "right", "c": "center"}[align]
    box = VPacker(children=[
        TextArea(title or gtitle, textprops=dict(fontsize=fs[0], fontweight="bold", color=INK, ha=ta)),
        TextArea(detail or gdetail, textprops=dict(fontsize=fs[1], color=SUB, linespacing=1.2, ha=ta)),
    ], align={"l": "left", "r": "right", "c": "center"}[align], pad=0, sep=1.5)
    a.add_artist(AnnotationBbox(
        box, xy(a, *lead), xybox=xy(a, *lxy), xycoords="data", boxcoords="data",
        box_alignment={"l": (0, 0.5), "r": (1, 0.5), "c": (0.5, 0.5)}[align], pad=0.4, zorder=7,
        bboxprops=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#D0CCC4", linewidth=0.6, alpha=0.95),
        arrowprops=dict(arrowstyle="-", color="#6E6E6E", linewidth=0.8, shrinkA=0, shrinkB=2.5)))


for key, (lxy, t, d, al) in NA.items():
    draw(ax, key, lxy, t, d, al)

# Hawaii inset
hax = fig.add_axes([0.092, 0.162, 0.2, 0.115], projection=ccrs.PlateCarree())
hax.set_extent([-164.8, -154.4, 18.4, 23.2], crs=pc)
# the model-robust Hawaii area covers the whole inset, so shade the islands themselves
_hi = [g for g in cfeature.NaturalEarthFeature("physical", "land", "10m").intersecting_geometries(
    [-164.8, -154.4, 18.4, 23.2])]
_k = GLOBAL["hawaii"]
hax.add_geometries(_hi, crs=pc, facecolor={"dry": DRY, "wet": WET}[_k[1]][_k[2]],
                   edgecolor=EDGE[_k[1]], linewidth=0.6)
hax.spines["geo"].set_edgecolor("#999999")
hax.text(0.04, 0.92, "Hawaii", transform=hax.transAxes, fontsize=10.5, fontweight="bold", color=INK, va="top")
hax.text(0.04, 0.72, "drought · Nov–Mar", transform=hax.transAxes, fontsize=9.5, color=SUB, va="top")

fig.text(0.03, 0.955, "El Niño 2026–27: what to expect this winter in North America",
         fontsize=20, fontweight="bold", color=INK)
fig.text(0.03, 0.932, "Shading = scientific confidence from the literature and past strong events. Shapes show where ≥80% of\n"
         "13 seasonal forecast models agree (NMME + C3S, Sep 2026 start). Impacts are shifts in odds, not certainties.",
         fontsize=11.5, color="#555555", linespacing=1.35, va="top")

# legend
lx, ly, sw, sh, gx = 0.035, 0.085, 0.022, 0.022, 0.075
cx0 = lx + 0.13
for j, lab in enumerate(["High", "Med-high", "Medium"]):
    fig.text(cx0 + j * gx, ly + 2.0 * sh, lab, fontsize=9.5, color="#555555", ha="center")
for i, (ramp, rowlab) in enumerate([(DRY, "Drought / dry"), (WET, "Flood / wet")]):
    y = ly + (1 - i) * sh
    fig.text(lx, y + 0.008, rowlab, fontsize=10, color="#222222", ha="left", va="center")
    for j, conf in enumerate(["high", "medhigh", "medium"]):
        fig.patches.append(mpatches.FancyBboxPatch((cx0 + j * gx - sw / 2, y), sw, sh * 0.72,
                           boxstyle="round,pad=0.001,rounding_size=0.004", facecolor=ramp[conf],
                           edgecolor="none", transform=fig.transFigure))
fx = cx0 + 2.7 * gx
fig.patches.append(mpatches.Rectangle((fx, ly + 1.1 * sh), sw * 1.1, sh * 0.72, facecolor=WET["medhigh"],
                   edgecolor=EDGE["wet"], linewidth=1.3, linestyle=(0, (3, 1.6)), transform=fig.transFigure))
fig.text(fx + sw * 1.1 + 0.01, ly + 1.45 * sh, "dashed outline = signal underperformed in a recent strong event (2015–16)",
         fontsize=9.5, color="#555555", va="center")
fig.patches.append(mpatches.FancyBboxPatch((fx, ly + 0.0 * sh), sw * 1.1, sh * 0.72,
                   boxstyle="round,pad=0.001,rounding_size=0.004", facecolor=WARM["medium"],
                   edgecolor="none", transform=fig.transFigure))
fig.text(fx + sw * 1.1 + 0.01, ly + 0.35 * sh, "warm winter (medium confidence)", fontsize=9.5, color="#555555", va="center")

# footer numbers are read from the hit-rate and hindcast files, not typed
import pandas as _pd
_ROOT = HERE.parent
_hs = _pd.read_csv(_ROOT / "hit_rates" / "derived" / "hit_summary.csv"); _hs = _hs[_hs.main].set_index("region").loc["swus"]
_ev = _pd.read_csv(_ROOT / "hit_rates" / "derived" / "hit_events.csv"); _ev15 = _ev[(_ev.region == "swus") & _ev.main & (_ev.year0 == 2015)].iloc[0]
assert not _ev15.hit
_ob = _pd.read_csv(_ROOT / "model_patterns" / "hindcast" / "data" / "obs_ca_winter_precip_enso.csv")
_d6 = _ob[(_ob.region == "SoCal_d6") & (_ob.decyear == 2015)].set_index("season").pct_normal_9120
_hc = _pd.read_csv(_ROOT / "model_patterns" / "hindcast" / "data" / "nmme_event_table.csv"); _hc = _hc[_hc.year == 2015]
_wet, _nm = int((_hc.SoCal_d6_DJF_pct > 100).sum()), len(_hc)
FOOT = (f"S California, Southwest & N Mexico: wetter than a typical neutral winter in {int(_hs.hits)} of {int(_hs.n)} strong El Niños since 1957, but not 2015–16.\n"
        f"Coastal S California got {_d6['DJF']:.0f}–{_d6['JFM']:.0f}% of its 1991–2020 average that winter, though {_wet} of {_nm} models rerun from Sep 2015 predict wet.\n"
        "Every Sep 2026 forecast is beyond the strongest El Niño on record.")
print(FOOT)
fig.text(0.5, 0.018, FOOT, fontsize=10, color="#333333", ha="center", linespacing=1.4,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#F4F2EC", edgecolor="#DDD9D0"))
fig.text(0.975, 0.073, "Z. Hausfather · data: NMME, C3S, NOAA nClimDiv",
         fontsize=8, color="#999999", ha="right")

out = HERE / "elnino_2026_impacts_map_north_america"
fig.savefig(str(out) + ".png", dpi=200)
fig.savefig(str(out) + ".pdf")
print("written", str(out) + ".png")
