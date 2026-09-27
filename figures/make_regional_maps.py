#!/usr/bin/env python3.13
"""Regional close-ups of the El Niño 2026-27 impacts map (v6): Indo-Pacific, Africa, South America.

Tiers, flags and shapes are read from make_impacts_map.py (REGIONS) and model_polygons.json, like
make_impacts_map_na.py, so the close-ups cannot drift from the global map. Footer numbers are read from
hit_rates/derived/hit_summary.csv (observed strong-El-Niño hit counts, METHODS.md) at render time.
"""
import json
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnnotationBbox, TextArea, VPacker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import shape, Polygon

HERE = Path(__file__).resolve().parent
src = (HERE / "make_impacts_map.py").read_text()
ns = {"Polygon": Polygon}
exec(src[src.index("# confidence -> fill"):src.index("LAT_S, LAT_N")], ns)
exec(src[src.index("REGIONS = ["):src.index("FOOTER =")], ns)
DRY, WET, WARM, EDGE = ns["DRY"], ns["WET"], ns["WARM"], ns["EDGE"]
GLOBAL = {r[0]: r for r in ns["REGIONS"]}
MODEL = {k: shape(v) for k, v in json.loads(
    (HERE.parent / "model_patterns" / "derived" / "model_polygons.json").read_text()).items()}
HS = pd.read_csv(HERE.parent / "hit_rates" / "derived" / "hit_summary.csv")
YJJ = HS[(HS.region == "yangtze") & (HS.source == "gpcc2025:yangtze@JJ1")].iloc[0]
HS = HS[HS.main].set_index("region")
INK, SUB = "#1A1A1A", "#4A4A4A"
plt.rcParams["font.family"] = "DejaVu Sans"
pc = ccrs.PlateCarree()


EV = pd.read_csv(HERE.parent / "hit_rates" / "derived" / "hit_events.csv")


def PN(k, y):   # % of the 1991-2020 average, main source, event year y (counts use the typical neutral year instead)
    r = EV[(EV.region == k) & (EV.main) & (EV.year0 == y)].iloc[0]
    return f"{r.pct_normal:.0f}%"


def hits(k):
    r = HS.loc[k]
    return f"{int(r.hits)} of {int(r.n)}"


def poly_for(key):
    _, kind, conf, flag, shp, *_ = GLOBAL[key]
    if shp == "model":
        return MODEL[key]
    return Polygon(shp).buffer({"peru": 0.8, "mekong": 0.8, "norcal": 0.3, "altiplano": 0.3, "cchile": 0.2}.get(key, 2.0), join_style=1).simplify(0.25)


def make(name, title, subtitle, proj, extent, labels, notes, footer, figsize=(12, 9.6), axrect=(0.02, 0.16, 0.96, 0.70), ly=0.085):
    fig = plt.figure(figsize=figsize, facecolor="white")
    ax = fig.add_axes(list(axrect), projection=proj)
    ax.set_extent(extent, crs=pc)
    ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor="#E9E7E1", edgecolor="none")
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.4, edgecolor="#B7B3AA")
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.4, edgecolor="#C9C5BC")
    ax.spines["geo"].set_edgecolor("#CCC9C2")

    def xy(lon, lat):
        return proj.transform_point(lon, lat, pc)

    for key, (lxy, t, d, al, lead) in labels.items():
        _, kind, conf, flag, shp, _, gtitle, gdetail, gleader, _ = GLOBAL[key]
        poly = poly_for(key)
        fill = {"dry": DRY, "wet": WET, "warm": WARM}[kind][conf]
        ax.add_geometries([poly], crs=pc, facecolor=fill, alpha=0.88, edgecolor=EDGE[kind],
                          linewidth=1.5 if flag == "busted" else 0.8,
                          linestyle=(0, (4, 2)) if flag == "busted" else "solid", zorder=3)
        rp = poly.representative_point()
        lead = lead or gleader or (rp.x, rp.y)
        ax.plot(*xy(*lead), marker="o", ms=3.6, color="#333333", mec="white", mew=0.6, zorder=6)
        ta = {"l": "left", "r": "right", "c": "center"}[al]
        box = VPacker(children=[
            TextArea(t or gtitle.replace("\n", " "), textprops=dict(fontsize=11, fontweight="bold", color=INK, ha=ta)),
            TextArea(d or gdetail, textprops=dict(fontsize=9.5, color=SUB, linespacing=1.25, ha=ta)),
        ], align={"l": "left", "r": "right", "c": "center"}[al], pad=0, sep=1.5)
        ax.add_artist(AnnotationBbox(
            box, xy(*lead), xybox=xy(*lxy), xycoords="data", boxcoords="data",
            box_alignment={"l": (0, 0.5), "r": (1, 0.5), "c": (0.5, 0.5)}[al], pad=0.4, zorder=7,
            bboxprops=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#D0CCC4", linewidth=0.6, alpha=0.95),
            arrowprops=dict(arrowstyle="-", color="#6E6E6E", linewidth=0.8, shrinkA=0, shrinkB=2.5)))

    for (pt, txt, txy) in notes:   # unshaded italic notes (regions deliberately left off)
        ax.plot(*xy(*pt), marker="o", ms=3.6, color="#777777", mec="white", mew=0.6, zorder=6)
        ax.annotate(txt, xy=xy(*pt), xytext=xy(*txy), textcoords="data", fontsize=9.5, color="#555555",
                    style="italic", ha="center", va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#D0CCC4", linewidth=0.6, alpha=0.95),
                    arrowprops=dict(arrowstyle="-", color="#9A9A9A", linewidth=0.8, linestyle=(0, (2, 2)),
                                    shrinkA=0, shrinkB=2.5))

    fig.text(0.03, 0.955, title, fontsize=20, fontweight="bold", color=INK)
    fig.text(0.03, 0.928, subtitle, fontsize=11.5, color="#555555", linespacing=1.35, va="top")

    lx, sw, sh, gx = 0.035, 0.022, 0.022, 0.075
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
    fig.patches.append(mpatches.Rectangle((fx, ly + 1.1 * sh), sw * 1.1, sh * 0.72, facecolor=DRY["medium"],
                       edgecolor=EDGE["dry"], linewidth=1.3, linestyle=(0, (3, 1.6)), transform=fig.transFigure))
    fig.text(fx + sw * 1.1 + 0.01, ly + 1.45 * sh, "dashed outline = signal underperformed in a recent strong event",
             fontsize=9.5, color="#555555", va="center")
    fig.text(fx, ly + 0.35 * sh, "All impacts are shifts in probability, not certainties", fontsize=9.5,
             color="#555555", va="center")
    fig.text(0.5, 0.018, footer, fontsize=10, color="#333333", ha="center", linespacing=1.4,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#F4F2EC", edgecolor="#DDD9D0"))
    fig.text(0.975, ly - 0.012, "Z. Hausfather · data: NMME, C3S, GPCC, GHCN-D, GPCP", fontsize=8, color="#999999", ha="right")
    out = HERE / f"elnino_2026_impacts_map_{name}"
    fig.savefig(str(out) + ".png", dpi=200)
    fig.savefig(str(out) + ".pdf")
    plt.close(fig)
    print("written", out.name)


SUBT = ("Shading = scientific confidence from the literature and how often each signal appeared in the 8 strong\n"
        "El Niños since 1957. Shapes show where ≥80% of 13 seasonal forecast models agree (NMME + C3S, Sep 2026 start).")

# ---------------------------------------------------------------- Indo-Pacific
make("indo_pacific", "El Niño 2026–27: Asia, Australia and the Pacific", SUBT,
     ccrs.PlateCarree(central_longitude=148), [62, 234, -46, 42],
     {
         "maritime": ((96, -24), None, None, "c", None),
         "philippines": ((150, 21), None, None, "l", None),
         "mekong": ((86, 12), None, None, "c", None),
         "schina": ((92, 25), None, None, "c", None),
         "yangtze": ((134, 35), None, None, "c", None),
         "srilanka": ((72, -8), None, None, "c", None),
         "seaustralia": ((122, -42), None, None, "c", None),
         "wpacific": ((178, -36), None, None, "c", None),
         "cpacific": ((208, -14), None, None, "c", None),
         "hawaii": ((212, 30), None, None, "c", None),
     },
     [((78, 22), "India: the 2027 monsoon is not favoured dry\n(dry in 1 of 8 years after a strong El Niño)", (76, 37))],
     f"Observed record vs a typical neutral year, strong El Niños since 1957: Maritime Continent drier in {hits('maritime')}, Philippines {hits('philippines')},\n"
     f"W Pacific islands {hits('wpacific')}, southern Mekong {hits('mekong')}, SE Australia {hits('seaustralia')}; "
     f"Sri Lanka wetter in {hits('srilanka')}; Yangtze wetter in {hits('yangtze')} for Jun–Aug, "
     f"{int(YJJ.hits)} of {int(YJJ.n)} for Jun–Jul.",
     figsize=(13, 8.6), axrect=(0.02, 0.17, 0.96, 0.68))

# ---------------------------------------------------------------- Africa
make("africa", "El Niño 2026–27: Africa", SUBT,
     ccrs.LambertAzimuthalEqualArea(central_longitude=20, central_latitude=0), [-20, 58, -37, 24],
     {
         "horn": ((24, 16), None, "floods, heavy short rains · Oct–Dec\n(size set by Indian Ocean Dipole)", "c", None),
         "safrica": ((42, -30), None, None, "l", None),
     },
     [((0, 14), f"Sahel: no reliable El Niño signal\n(drier in only {hits('c_sahel')} strong events)", (-8, 4))],
     f"Observed record vs a typical neutral year, strong El Niños since 1957: southern Africa drier in {hits('safrica')} (Dec–Feb); "
     f"Horn of Africa wetter in {hits('horn')} (Oct–Dec).\n"
     f"Southern Africa's misses were 1957–58 and 1965–66. 1997–98 came in at {PN('safrica', 1997)} of the 1991–2020 average, "
     f"and 2023–24, the driest of the eight, at {PN('safrica', 2023)}.",
     figsize=(11, 10.4), axrect=(0.02, 0.15, 0.96, 0.72))

# ---------------------------------------------------------------- South America
make("south_america", "El Niño 2026–27: South America", SUBT,
     ccrs.LambertAzimuthalEqualArea(central_longitude=-62, central_latitude=-15), [-92, -30, -45, 14],
     {
         "nsam": ((-50, 11), None, None, "l", None),
         "amazon": ((-88, 2), None, None, "r", None),
         "nebrazil": ((-33, -2), None, None, "l", None),
         "peru": ((-88, -16), None, None, "r", None),
         "sesa": ((-36, -35), None, None, "l", None),
         "altiplano": ((-88, -27), None, None, "r", None),
         "cchile": ((-88, -38.5), None, None, "r", None),
     },
     [],
     f"Observed record vs a typical neutral year, strong El Niños since 1957: Amazon drier in {hits('amazon')}, northern South America {hits('nsam')}, "
     f"NE Brazil {hits('nebrazil')},\nAltiplano {hits('altiplano')}; SE South America wetter in {hits('sesa')}, "
     f"central Chile (Oct–Nov) {hits('cchile')}.\nPeru/Ecuador coast: flooding rains in 1982–83 "
     f"({PN('peru', 1982)} of the 1991–2020 average) and 1997–98 ({PN('peru', 1997)}), both with very warm coastal waters,\nas in 2026; "
     "other strong events ranged from somewhat below to somewhat above the 1991–2020 average.",
     figsize=(11, 11.6), axrect=(0.02, 0.19, 0.96, 0.69), ly=0.115)
