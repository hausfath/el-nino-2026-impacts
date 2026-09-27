#!/usr/bin/env python3.13
"""Diagnostic maps of multi-model standardized anomalies with robust-agreement stippling."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point

ROOT = Path(__file__).parent
m = xr.open_dataset(ROOT / "derived" / "metrics.nc")
o = xr.open_dataset(ROOT / "derived" / "obs_ref.nc")
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
lon, lat = m.lon.values, m.lat.values
pc = ccrs.PlateCarree()


def panel(ax, z, robust, title, cmap, levels, dry=None):
    zc, lonc = add_cyclic_point(z, coord=lon)
    cf = ax.contourf(lonc, lat, zc, levels=levels, cmap=cmap, extend="both", transform=pc)
    if dry is not None:
        ax.contourf(lon, lat, np.where(dry, 1, np.nan), levels=[0.5, 1.5], colors=["#DDDDDD"], transform=pc)
    yy, xx = np.meshgrid(lat, lon, indexing="ij")
    sel = (robust != 0) & (yy % 3 == 0) & (xx % 3 == 0)
    ax.scatter(xx[sel], yy[sel], s=1.2, c="k", lw=0, transform=pc)
    ax.coastlines(lw=0.4, color="#444444")
    ax.set_global()
    ax.set_title(title, fontsize=12, loc="left")
    return cf


def figure(kind, seasons, fname, sup):
    n = len(seasons)
    rows = (n + 1) // 2
    H = 4.1 * rows + 2.2
    fig, axs = plt.subplots(rows, 2, figsize=(15, H),
                            subplot_kw=dict(projection=ccrs.Robinson(central_longitude=180)))
    axs = np.atleast_1d(axs).ravel()
    for ax, s in zip(axs, seasons):
        if kind == "pr":
            dry = o[f"pr_clim_{s}"].values < 0.5
            cf = panel(ax, m[f"pr_z_{s}"].values, m[f"pr_robust_{s}"].values,
                       f"Precipitation {s}  (n={int(m[f'pr_n_{s}'])} models)", "BrBG",
                       np.arange(-1.5, 1.51, 0.25), dry)
            lab = "Multi-model mean anomaly / observed interannual SD (GPCP 1991–2020, detrended)"
        else:
            rob = ((m[f"t_robust_{s}"] > 0) & (m[f"t91_robust_{s}"] > 0) & (m[f"tlmr_robust_{s}"] > 0)) | \
                  ((m[f"t_robust_{s}"] < 0) & (m[f"t91_robust_{s}"] < 0) & (m[f"tlmr_robust_{s}"] < 0))
            cf = panel(ax, m[f"t_z_{s}"].values, rob.values,
                       f"2 m temperature {s}, trend-adjusted  (n={int(m[f't_n_{s}'])})", "RdBu_r",
                       np.arange(-2, 2.01, 0.25))
            lab = "Trend-adjusted multi-model mean / ERA5 interannual SD (1991–2020, detrended)"
    for ax in axs[n:]:
        ax.set_visible(False)
    fig.subplots_adjust(left=0.02, right=0.98, top=1 - 1.1 / H, bottom=1.1 / H, wspace=0.04, hspace=0.12)
    cax = fig.add_axes([0.25, 0.55 / H, 0.5, 0.18 / H])
    fig.colorbar(cf, cax=cax, orientation="horizontal").set_label(lab, fontsize=10)
    fig.suptitle(sup, fontsize=15, fontweight="bold", x=0.02, ha="left", y=1 - 0.2 / H)
    fig.text(0.02, 1 - 0.62 / H, "Sep 2026 initializations: NMME (6 models) + C3S (7 independent centres; SON & DJF only). "
             "Dots: ≥80% of models agree on sign and |mean| ≥ 0.5 SD" +
             (" under all three trend treatments" if kind == "t" else ". Grey: dry-season mask (<0.5 mm/day)") + ".",
             fontsize=10, color="#444444")
    fig.savefig(FIG / fname, dpi=130)
    print("wrote", fname)


figure("pr", ["SON", "OND", "DJF", "JFM", "MAM"], "diag_precip_z.png", "Multi-model precipitation signal, El Niño 2026–27")
figure("t", ["SON", "DJF"], "diag_t2m_z.png", "Multi-model temperature signal (trend-adjusted), El Niño 2026–27")
