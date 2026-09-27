# El Niño 2026–27: where the biggest impacts are likely

Code and data behind the Climate Brink post "Where this El Niño is most likely to hit, region by region" and the interactive **El Niño Impacts** tab on the [Climate Dashboard](https://dashboard.theclimatebrink.com/#impacts).

For each region on the impacts map, the analysis combines three lines of evidence:

1. **The literature.** Teleconnection studies, assessed with IPCC-style confidence levels. The regional reviews are in `research/`.
2. **The observed record.** How often the region's season was drier or wetter (or warmer) than a *typical ENSO-neutral year* in each of the 8 strong El Niños since 1957 (Nov–Jan Oceanic Niño Index ≥ 1.5 °C). Code is in `hit_rates/`.
3. **This year's forecasts.** Agreement among 13 dynamical seasonal forecast systems (6 NMME + 7 Copernicus C3S, September 2026 start) over the region's season. Code is in `model_patterns/`.

The full methods, pre-registered specifications, sensitivity tests and every deviation from the plan are in the METHODS files:

| File | What it covers |
|---|---|
| [`hit_rates/METHODS.md`](hit_rates/METHODS.md) | Observed hit rates: event and neutral-year definitions, detrending, datasets per region, sensitivities (RONI events, dropping 2009–10, leave-one-out, moderate events, La Niña specificity), the two benchmarks (typical neutral year vs the 1991–2020 average) |
| [`model_patterns/METHODS.md`](model_patterns/METHODS.md) | Seasonal forecast processing: sources and baselines, deduplication, temperature trend adjustment, robustness tests, polygon reshaping, full-window model checks |
| [`model_patterns/hindcast/METHODS.md`](model_patterns/hindcast/METHODS.md) | NMME hindcasts of strong El Niño winters for California (the 2015–16 miss) |
| [`figures/NOTES.md`](figures/NOTES.md) | Map versions and the changes between them |

## Pipeline

```
raw downloads (not in this repo, see below)
  │
  ├─ hit_rates/        gpcc_extract.py, extract.py, be_extract.py, stations.py  →  derived/*_regional_monthly.csv
  │                    analyze.py      →  derived/hit_events.csv, hit_summary.csv       (the x/8 counts)
  │                    model_counts.py →  derived/model_counts.csv                     (3-month model counts, kept for reference)
  │
  ├─ model_patterns/   fetch_cds.py (C3S, ERA5) + NMME via CPC  →  process.py  →  derived/seasonal_anoms.nc, obs_ref.nc, metrics.nc
  │                    regions.py, europe.py, westafrica.py     →  derived/region_table.csv, europe_table.csv, ...
  │                    reshape.py                               →  derived/model_polygons.json   (map shapes)
  │                    windows.py, window_tests.py              →  derived/monthly_anoms.nc, window_tests.csv  (the y/13 counts)
  │                    hindcast/scripts/                        →  hindcast/data/                (California hindcasts)
  │
  ├─ figures/          make_*.py (matplotlib versions), web/ (the dashboard-style blog figures; see web/README.md)
  │
  └─ dashboard/        tools/export_data.py      →  data/regions.json, stats.json, geo.json, img/
                       tools/export_dashboard.py →  the Climate Dashboard's elnino_map/ bundle
                       tools/check_region_lit.py, check_lit_numbers.py  →  checks on data/region_lit.json (the tab's literature text)
```

**What this repo includes:**
- All derived files, so every count, table and figure can be regenerated without re-downloading.
- The raw downloads are left out (about 400 MB). The scripts above fetch or read them, and each METHODS file lists its sources.

**Running it:**
- Python 3.13 with the packages in `requirements.txt`.
- The figure renderer in `figures/web/` also needs Node 20+, Chrome, and `npm install` in that folder.
- It reads the dashboard's El Niño tab from a clone of [hausfath/climate-dashboard](https://github.com/hausfath/climate-dashboard). Put it next to this repo as `climate-dashboard/`, or set `CLIMATE_DASHBOARD`.

**Two reference points.** The observed counts and the per-event bars on the dashboard compare each event with a typical ENSO-neutral year: the Theil-Sen trend through the neutral years, plus the median neutral residual. Forecast magnitudes and the percentages quoted in the post are relative to the 1991–2020 average. `hit_rates/METHODS.md` explains why both are used, and why rebasing the forecasts on a typical neutral year was tested and rejected.

**The 2027 record odds.** `data/forecast_2027_extract.json` holds the four numbers the map and dashboard use from a separate global temperature forecast: P(2027 is the warmest year) on the ONI and RONI conventions, plus the model and member counts.

## Data sources

| Data | Provider | Used for |
|---|---|---|
| GPCC Full Data Monthly v2025, 1° | DWD / GPCC | observed rainfall, main source |
| GPCP v2.3 monthly | NOAA PSL | islands and ocean regions; forecast climatology and year-to-year variability |
| NOAA PREC/L | NOAA PSL | sensitivity |
| GHCN-Daily | NOAA NCEI | island and coastal station composites |
| Berkeley Earth Complete_TAVG, 1° | Berkeley Earth | temperature regions |
| NOAA nClimDiv | NOAA NCEI | California climate divisions |
| ONI, RONI | NOAA CPC | event selection (`oni_cpc_2026-09-15.txt`) |
| NMME real-time forecasts and hindcasts | NOAA CPC, IRI Data Library | forecasts, California hindcasts |
| C3S seasonal forecasts (`seasonal-postprocessed-single-levels`) | Copernicus Climate Change Service | forecasts |
| ERA5 monthly | Copernicus Climate Change Service | temperature trends |
| Natural Earth | naturalearthdata.com | coastlines, borders |

Derived data from each source remain under that provider's terms. Check them before redistributing. The Copernicus-derived files contain modified Copernicus Climate Change Service information (2026); neither the European Commission nor ECMWF is responsible for any use of it.

## License

Code: MIT (see `LICENSE`). Derived data: see the data sources above.

Zeke Hausfather · [The Climate Brink](https://www.theclimatebrink.com)
