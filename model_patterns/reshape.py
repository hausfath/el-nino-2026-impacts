#!/usr/bin/env python3.13
"""Model-derived polygon proposals for the impacts map.

For each region: cells where the multi-model signal is robust (>=80% sign agreement,
|z| >= 0.5; >=5/6 for NMME-only seasons) in the literature-expected direction, in any
of the seasons the map label covers, restricted to a search window around the
literature region (trim/extend only; contours never create a region). Land regions are
clipped to land (dilated 1 cell so coastlines aren't ragged). The mask is smoothed,
contoured, cleaned (small fragments dropped) and simplified.

Output: derived/model_polygons.json, figures/proposal_preview.png
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import shapely
from shapely.geometry import Polygon, Point, box, mapping
from scipy.ndimage import gaussian_filter, binary_dilation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ROOT = Path(__file__).parent
m = xr.open_dataset(ROOT / "derived" / "metrics.nc")
o = xr.open_dataset(ROOT / "derived" / "obs_ref.nc")
LAT, LON = m.lat.values, m.lon.values  # 0..359 (Pacific-contiguous)
LON2, LAT2 = np.meshgrid(LON, LAT)
land = binary_dilation(o.land.values.astype(bool), iterations=1)
land2 = binary_dilation(o.land.values.astype(bool), iterations=2)  # islands: keep near-shore seas

LITP = json.loads((ROOT / "lit_polygons_v4.json").read_text())  # literature polygons as of map v4
BUF = {"peru": 0.8, "camerica": 1.0, "safrica": 1.4}
to360 = lambda pts: [((x + 360) % 360, y) for x, y in pts]
LIT = {k: Polygon(to360(v["pts"])).buffer(BUF.get(k, 2.0), join_style=1) for k, v in LITP.items()}
CAND = {"socal": box(239, 32.5, 246, 35.5), "norcal": box(235.5, 38, 240, 42),
        "nmexico_sw": box(245, 25, 260, 33), "nsam": box(283, 0, 305, 12),
        "philippines": box(117, 5, 127, 19), "schina": box(105, 22, 122, 30),
        "hawaii": Point(202.5, 20.5).buffer(3.5), "antilles": box(268, 17.5, 288, 24),  # Greater Antilles + Yucatan (Giannini et al. 2000)
        "drycorridor": box(268, 10, 277, 16)}

# region: (window geometry, window buffer deg, seasons, sign, land-only)
SPEC = {
    "maritime": (LIT["maritime"], 4, ["SON", "OND"], -1, "islands"),
    "safrica": (LIT["safrica"], 5, ["DJF", "JFM"], -1, True),
    "amazon": (LIT["amazon"], 4, ["SON", "DJF", "MAM"], -1, True),
    "nebrazil": (LIT["nebrazil"], 3, ["MAM"], -1, True),
    "drycorridor": (CAND["drycorridor"].union(LIT["camerica"].intersection(box(260, 5, 290, 17))), 3, ["DJF"], -1, True),
    "antilles": (CAND["antilles"], 3, ["DJF"], +1, True),
    "wpacific": (LIT["wpacific"], 3, ["SON", "DJF"], -1, False),
    "horn": (LIT["horn"], 4, ["OND"], +1, True),
    "peru": (LIT["peru"], 2, ["DJF", "MAM"], +1, True),
    "sesa": (LIT["sesa"], 4, ["SON", "DJF"], +1, True),
    "gulf": (LIT["gulf"], 3, ["DJF", "JFM"], +1, True),
    "cpacific": (LIT["cpacific"], 4, ["SON", "DJF"], +1, False),
    "socal": (CAND["socal"], 2, ["DJF", "JFM"], +1, True),
    "norcal": (CAND["norcal"], 1, ["DJF", "JFM"], +1, True),
    "nsam": (CAND["nsam"], 3, ["SON", "DJF"], -1, True),
    "philippines": (CAND["philippines"], 2, ["DJF", "MAM"], -1, "islands"),
    "schina": (CAND["schina"], 2, ["DJF", "MAM"], +1, True),
    "hawaii": (CAND["hawaii"], 2, ["DJF", "JFM"], -1, False),
    "nmexico_sw": (CAND["nmexico_sw"], 2, ["DJF"], +1, True),
}


def mask_to_polys(msk, min_area=10.0):
    if not msk.any():
        return None
    sm = gaussian_filter(msk.astype(float), 0.8)
    fig, ax = plt.subplots()
    cs = ax.contour(LON, LAT, sm, levels=[0.45])
    polys = []
    for path in cs.get_paths():
        for ring in path.to_polygons():
            if len(ring) >= 4:
                p = Polygon(ring).buffer(0)
                if p.area >= min_area:
                    polys.append(p)
    plt.close(fig)
    if not polys:
        return None
    g = shapely.union_all(polys).buffer(0.8, join_style=1).buffer(-0.8, join_style=1).simplify(0.3)
    return g


out, stats = {}, {}
for reg, (win, wbuf, seasons, sign, landonly) in SPEC.items():
    wmask = shapely.contains_xy(win.buffer(wbuf), LON2, LAT2)
    rob = np.zeros_like(wmask)
    for s in seasons:
        rob |= (m[f"pr_robust_{s}"].values * sign) > 0
    clip = land2 if landonly == "islands" else land if landonly else True
    msk = rob & wmask & clip
    g = mask_to_polys(msk)
    lit_area = LIT[reg].area if reg in LIT else None
    if g is None:
        stats[reg] = "no robust cells"
        continue
    out[reg] = mapping(g)
    stats[reg] = f"area {g.area:.0f} deg²" + (f" (literature polygon {lit_area:.0f})" if lit_area else " (new)")
# ---- composite / de-overlapped regions for the v5 map (author decisions, 23 Sep 2026) ----
from shapely.geometry import shape as _shape
G = {k: _shape(v) for k, v in out.items()}
fin = {}
fin["swus"] = G["socal"].union(G["nmexico_sw"]).buffer(0.6, join_style=1).buffer(-0.6, join_style=1)
fin["amazon"] = G["amazon"].intersection(box(0, -90, 360, 2.0))
fin["nsam"] = G["nsam"].intersection(box(0, 0.5, 360, 90)).difference(fin["amazon"].buffer(0.3))
fin["philippines"] = G["philippines"]
fin["maritime"] = G["maritime"].difference(G["philippines"].buffer(0.3))
YANGTZE = Polygon(to360([(104, 28), (112, 30), (120, 32), (122, 30), (118, 27), (108, 26)])).buffer(2.0, join_style=1)
fin["schina"] = G["schina"].difference(YANGTZE.buffer(0.5))
for k in ["safrica", "nebrazil", "drycorridor", "antilles", "wpacific", "horn", "sesa", "gulf", "cpacific", "hawaii"]:
    fin[k] = G[k]
fin["wpacific"] = fin["wpacific"].difference(fin["maritime"].buffer(0.2)).difference(fin["cpacific"].buffer(0.2))
# priority: more specific / higher-tier region keeps shared cells
fin["amazon"] = fin["amazon"].difference(fin["nebrazil"].buffer(0.2))
fin["drycorridor"] = fin["drycorridor"].difference(fin["nsam"].buffer(0.2))
fin["antilles"] = fin["antilles"].difference(fin["gulf"].buffer(0.2))
fin["swus"] = fin["swus"].difference(fin["gulf"].buffer(0.2))
# ---- North America follow-up (23 Sep 2026): model-robust inland-NW dryness and E-Canada warmth ----
nw_win = shapely.contains_xy(box(226, 40, 262, 64), LON2, LAT2)
nw = (m["pr_robust_DJF"].values < 0) & nw_win & land
fin["inlandnw"] = mask_to_polys(nw)
t_all3 = ((m["t_robust_DJF"] > 0) & (m["t91_robust_DJF"] > 0) & (m["tlmr_robust_DJF"] > 0)).values
ec_win = shapely.contains_xy(box(248, 42, 305, 66), LON2, LAT2)
fin["ecanada_warm"] = mask_to_polys(t_all3 & ec_win & land)
fin["ecanada_warm"] = fin["ecanada_warm"].difference(fin["inlandnw"].buffer(0.5))
# author decision: central Canada only (literature core west of Hudson Bay; E Canada NAO-dominated)
fin["ccanada_warm"] = fin.pop("ecanada_warm").intersection(box(0, -90, 280.5, 90))
# ---- hand-drawn-region refinement (23 Sep 2026; sub-region boxes chosen after inspecting maps -> supporting only) ----
seau = (m["pr_robust_SON"].values < 0) & shapely.contains_xy(box(139, -45, 153, -33), LON2, LAT2) & land
fin["seaustralia"] = mask_to_polys(seau, min_area=4.0)
srl = (m["pr_robust_OND"].values > 0) & shapely.contains_xy(box(79, 5, 82.5, 10.5), LON2, LAT2) & land2
fin["srilanka"] = mask_to_polys(srl, min_area=2.0)
out_final = {}
for k, g in fin.items():
    # drop slivers created by the differences
    if g is None:
        continue
    parts = [p for p in getattr(g, "geoms", [g]) if p.area >= (2 if k in ("srilanka", "seaustralia") else 8)]
    out_final[k] = mapping(shapely.union_all(parts).simplify(0.2))
(ROOT / "derived" / "model_polygons.json").write_text(json.dumps(out_final))
(ROOT / "derived" / "model_polygons_raw.json").write_text(json.dumps(out))
print("final regions:", sorted(out_final))
for k, v in stats.items():
    print(f"{k:12s} {v}")

# ---------- preview ----------
from shapely.geometry import shape
fig = plt.figure(figsize=(15, 7.2))
ax = fig.add_axes([0.01, 0.06, 0.98, 0.84], projection=ccrs.Robinson(central_longitude=180))
ax.set_global()
ax.set_extent([0, 359.9, -47, 62], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="#ECEAE4")
ax.coastlines(lw=0.35, color="#AAAAAA")
pc = ccrs.PlateCarree()
for reg, g in LIT.items():
    ax.add_geometries([g], crs=pc, facecolor="none", edgecolor="#555555", lw=1.0, ls=(0, (3, 2)), zorder=4)
for reg, gj in out.items():
    sign = SPEC[reg][3]
    col = "#3F8FC5" if sign > 0 else "#C4791C"
    ax.add_geometries([shape(gj)], crs=pc, facecolor=col, alpha=0.6, edgecolor=col, lw=0.8, zorder=3)
    c = shape(gj).representative_point()
    ax.text(c.x, c.y, reg, transform=pc, fontsize=8, ha="center", zorder=6,
            bbox=dict(fc="white", ec="none", alpha=0.7, pad=0.5))
fig.text(0.02, 0.955, "Proposal: model-robust extents (filled) vs current hand-drawn polygons (dashed)",
         fontsize=15, fontweight="bold")
fig.text(0.02, 0.925, "Sep 2026 NMME + C3S; robust = ≥80% models agree & |z| ≥ 0.5 in the literature direction, any label season. "
         "Brown = dry, blue = wet. Regions without robust support keep their hand-drawn outline only.",
         fontsize=10, color="#444444")
fig.savefig(ROOT / "figures" / "proposal_preview.png", dpi=140)
print("wrote proposal_preview.png")
