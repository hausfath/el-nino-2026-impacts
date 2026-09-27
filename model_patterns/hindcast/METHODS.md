# California winter precipitation and ENSO: observed teleconnection vs NMME September-start hindcasts

Analysis date 2026-09-23. Purpose: decide how far to trust dynamical-model agreement on a wet 2026–27 Southern California winter, and check Northern California. All numbers below come from the scripts in `scripts/` and the output files in `data/`. Precipitation is expressed as % of the 1991–2020 normal (observations) or % of each model's own 1991–2020 normal (models), unless stated otherwise.

## Pipeline
1. `scripts/obs_analysis.py` parses nClimDiv, builds DJF and JFM totals, and computes % of normal and z-scores. Output: `data/obs_ca_winter_precip_enso.csv`.
2. `scripts/obs_stats.py` runs the regressions, strong-event composites and nonlinearity diagnostics. Output: `data/obs_regression_stats.csv`, `data/obs_strong_events_*.csv`, `data/obs_nonlinearity_diagnostics.csv`.
3. `scripts/fetch_nmme.py` pulls NMME data from the IRI Data Library over OPeNDAP. Output: `data/nmme_raw/*.nc` (20 MB).
4. `scripts/make_weights.py` computes grid-cell weights for the model regions. Output: `data/model_region_weights.csv`.
5. `scripts/model_analysis.py [--split]` computes model anomalies, regressions against observations, the event table and the 2026 forecasts. Output: `data/nmme_*.csv`.
6. `scripts/summary_stats.py [_splitclim]` produces the summary tables. Output: `data/summary_*.csv` and `data/summary_output*.txt`.
7. `scripts/make_figure.py` draws `fig_ca_precip_vs_nino34_nmme.png`.

## Data sources
- **Observed precipitation.** NOAA NCEI nClimDiv divisional monthly precipitation, `climdiv-pcpndv-v1.0.0-20260904` (latest in the directory on 2026-09-23), from https://www.ncei.noaa.gov/pub/data/cirs/climdiv/ (redirects to https://www.ncei.noaa.gov/monitoring-content/data/us/climdiv/monthly/current/). Record format and state code 04 = California come from `divisional-readme.txt`. Division numbers and names were verified from the NCEI `CONUS_CLIMATE_DIVISIONS.shp.zip` attribute table:
  - div 2 = SACRAMENTO DRNG.
  - div 6 = SOUTH COAST DRNG. (32.5–35.3°N, 120.7–116.3°W)
  - div 7 = SOUTHEAST DESERT BASIN (32.6–38.0°N; includes the Mojave and Owens Valley)
  - Areas (EPSG:5070): div 2 = 70,766 km², div 6 = 37,536 km², div 7 = 118,191 km².
- **Region definitions.**
  - "SoCal" = div 6 (primary). Div 6+7 area-weighted is a sensitivity test. Div 7 alone is not used as a primary region because it is mostly desert.
  - "NorCal" = div 2.
- **ENSO indices.** CPC ONI (https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt; ERSSTv5, centred 30-yr base periods updated every 5 years) and CPC RONI (https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt). Both use the NDJ value. The "NDJ 1997" row sits between OND 1997 and DJF 1998, so it means Nov 1997–Jan 1998.
- **Models.** NMME monthly `prec` and `sst` from https://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/. The HTML catalogue now requires login, but OPeNDAP (`.../dods`) access works without it. Only September starts were used. Lead convention: L = 0.5 is the start month, so for S = Sep, NDJ = L 2.5–4.5, DJF = L 3.5–5.5 and JFM = L 4.5–6.5. This was verified from the S/L grids, where S is in months since 1960-01, 360-day calendar, and S = 800 is Sep 2026.

| Model (stream) | Sep starts used | Members | Sep 2026? |
|---|---|---|---|
| CanSIPS-IC4 (HINDCAST+FORECAST) | 1990–2026 | 40 | yes |
| NCEP-CFSv2 (HINDCAST; FORECAST/EARLY_MONTH_SAMPLES) | 1982–2026 | 24 hindcast / 32 forecast slots, only 9–10 filled for Sep 2026 | yes |
| NASA-GEOSS2S (HINDCAST+FORECAST) | 1981–2026 | 4 hindcast / 10 forecast | yes |
| COLA-RSMAS-CCSM4 (MONTHLY) | 1982–2026 | 10 | yes |
| COLA-RSMAS-CESM1 (MONTHLY) | 1982–2026 | 10 | yes |
| GFDL-SPEAR (HINDCAST+FORECAST) | 1991–2023 for Niño-3.4 (prec to 2025) | 15 / 30 | **no** (latest prec start on the DL is Jul 2026; SST forecast only to Mar 2024) |
| CanSIPS-IC3 | 1980–2023 | 20 | no (retired) |
| CanSIPSv2 | 1981–2021 | 20 | no (retired) |
| CMC1-CanCM3, CMC2-CanCM4 | 1981–2018 | 10 | no (retired) |
| NCAR-CESM1 | 1980–2010, plus 2016 | 10 | no (retired) |

"Active" set = CanSIPS-IC4, CFSv2, GEOS-S2S, COLA-CCSM4, COLA-CESM1 and SPEAR. The Canadian systems (IC4, IC3, v2, CanCM3, CanCM4) share components and are not independent.

## Methods choices
- **Seasons.** DJF and JFM totals are labelled by the December year (the ENSO year). For example, "1997" means DJF 1997–98 or JFM 1998.
- **Observed normal.** The sum of 1991–2020 monthly means, which is the NCEI convention.
- **Observed z-score.** Uses the interannual SD of winters Dec 1990 to Mar 2020.
- **Model regional means.** Each 1° cell is weighted by its area of overlap with the division polygon (`make_weights.py`). The SoCal weights sum to 37,536 km² and the NorCal weights to 70,766 km², matching the division areas exactly.
  - Sensitivity test: the task boxes intersected with California land. SoCal box = 32.5–35°N, 121–114.5°W. NorCal box = 38–41.5°N, 123–120°W.
- **Model Niño-3.4.** 5°S–5°N, 190–240°E, averaged server-side with Ingrid `[X Y]average`. A client-side cos-lat check on the CFSv2 forecast agreed to 0.002 °C.
- **Model climatology.** Each model's own mean over Sep starts 1990–2019, which covers target Jan–Mar of 1991–2020. SPEAR uses 1991–2019 because its hindcast starts in 1991. NCAR-CESM1 and the CMC models use whatever falls inside that window (≥ 20 years in every case). Where a year appears in both streams, the hindcast is used. Periods are listed in `data/nmme_climatology_periods.csv`.
- **Model % of normal and z-scores.** % of normal = ensemble-mean seasonal rate ÷ climatological rate. z = (ensemble mean − climatology) ÷ SD of single-member anomalies, so the model z-scale matches the observed one.
- **Slope comparison.** Model slope = OLS of ensemble-mean % of normal on the model's own ensemble-mean NDJ Niño-3.4. It is compared with the observed OLS slope of % of normal on ONI over the **same years** (primary), and with 1950–2025. Using % of normal per °C avoids the variance deflation that comes with ensemble averaging.
- **Sensitivity (`--split`).** CFSv2 and the two COLA models are initialised from CFSR, which has a known ~1999 discontinuity in the tropical Pacific. Their Niño-3.4 minus ONI offset is −0.63 to −0.81 °C before 1999 and about 0 afterwards. They were re-run with separate 1982–1998 and 1999–2019 climatologies. Results are in the `*_splitclim` files.

## Validation checks
- **ONI.** NDJ 1997 = 2.37 and NDJ 2015 = 2.59 in the current CPC file. These round to the published ONI table values of 2.4 and 2.6. **Pass.**
- **nClimDiv normals.** My 1991–2020 monthly means reproduce the NCEI `climdiv-norm-pcpndv` rows ending in `0010` exactly to 0.01 in. Div 6: Jan 3.81, Feb 4.24, Mar 2.77, Dec 2.73. Div 2: 6.33, 5.92, 5.19, 6.61. **Pass.** The row code 0010 = 1991–2020 is inferred from this match; the readme does not document it.
- **Jong et al. 2016** (ERL 11:054021, https://doi.org/10.1088/1748-9326/11/5/054021) was checked against the IOP page, read through a web-fetch summariser, so the quotes need a final human read.
  - The paper uses data from 1901–2010 and states that "The El Niño influence on California precipitation strengthens from early to late winter and is stronger in the south than the north". It reports that "Eight of ten moderate-to-strong El Niños in the late winter put southern California in the wettest tercile".
  - It was published in May 2016 and **does not report the 2015–16 outcome**. It says "It will be interesting to see if the El Niño of 2015/16 impact on California precipitation conformed to expectations". So the dossier's use of this paper as the source for "2015–16 gave near-normal SoCal precipitation" is a misattribution.
  - The 2015–16 outcome itself is confirmed here from nClimDiv: div 6 DJF 60% and JFM 68% of the 1991–2020 normal. Both sit at or just above the lower-tercile bound, since the 1991–2020 terciles are 59% and 111% for DJF and 61% and 107% for JFM. "Near-normal" is defensible in tercile terms; "below normal" is accurate in % of mean terms.
- **Model data.** A bug was found and fixed in my own code before any results were used. Absent forecast members (NaN) were being summed as 0 in the regional mean. This had depressed the CFSv2 2023 and 2026 forecasts to about 30–38% of normal. The fix uses `skipna=False`, and no reported numbers are affected. A second bug was also caught: division areas were misassigned in the div 6+7 sensitivity test and have been corrected.

## Key results
Values are % of the 1991–2020 normal; slopes are percentage points (pp) per °C of NDJ index.

### Observed, 1950–2025 (n = 76 winters), ONI

| Region / season | Slope (pp per °C) | 95% CI | r | p |
|---|---|---|---|---|
| SoCal JFM | +23.8 | 10.9 to 36.8 | 0.39 | < 0.001 |
| SoCal DJF | +17.1 | 5.2 to 29.0 | 0.32 | 0.005 |
| NorCal JFM | +10.9 | 2.0 to 19.9 | 0.27 | 0.02 |
| NorCal DJF | +6.9 | −1.8 to 15.6 | 0.18 | 0.12 |

- RONI slopes are within about 1 pp per °C of the ONI values (SoCal JFM +24.5, r = 0.41).
- The 1982–2025 slopes are similar (SoCal JFM +21.8, r = 0.39).
- SoCal div 6+7: JFM +26.0, r = 0.42.

### Strong events (NDJ ONI ≥ 1.5; n = 8)
The events are 1957, 1965, 1972, 1982, 1997, 2009, 2015 and 2023.

| Region | DJF, median of events | JFM, median of events | Above normal in DJF | Above normal in JFM |
|---|---|---|---|---|
| SoCal | 131% | 148% | 6/8 | 6/8 |
| NorCal | 116% | 128% | 6/8 | 7/8 |

For comparison, the base rate of winters above 100% of normal is 32–36% for SoCal and 39–42% for NorCal. With RONI ≥ 1.5, 1991 enters and 2023 drops out, and the results are almost the same.

### Nonlinearity
There is no significant nonlinearity: the t-statistic of the quadratic term is 0.55–1.24 for SoCal. Fitting El Niño years only (ONI ≥ 0.5) gives a SoCal JFM slope of 13.5 ± 26.4 pp per °C over 1950–2025, which is not steeper than the fit to all years. The four events with ONI ≥ ~2 gave the following SoCal JFM values:

| Event | ONI NDJ (°C) | SoCal JFM |
|---|---|---|
| 1982–83 | 2.1 | 204% |
| 1997–98 | 2.4 | 227% |
| 2015–16 | 2.6 | 68% |
| 2023–24 | 2.0 | 161% |

The 2015–16 residual from the linear fit is −87 pp, or −1.46 residual SDs. That is unusual but not extraordinary.

### Models vs observed slope (same years, ONI; see `summary_slope_ratios.csv`)

| Region / season | Median ratio, all 11 models | Median ratio, active 6 | Range, active 6 |
|---|---|---|---|
| SoCal JFM | 0.97 | 0.96 | 0.74–1.25 |
| SoCal DJF | 1.36 | 1.08 | 0.76–1.65 |
| NorCal JFM | 0.59 | 0.89 | 0.17–1.15 |
| NorCal DJF | 0.80 | 0.97 | 0.45–1.34 |

- CanCM3 has almost no California teleconnection: its ratio is 0.15–0.22 for SoCal.
- With the split climatology, the active-set SoCal JFM median ratio is 1.00.
- The observed-slope 95% CI is ±54% of the estimate, so these ratios cannot distinguish "models slightly overstate" from "models slightly understate".
- The ensemble-mean precipitation skill against observations is modest: median r = 0.34 for SoCal JFM and 0.18 for NorCal JFM.

### Hindcasts of key events
"Wet call" means an ensemble mean above 100% of the model's own normal.

| Event | Observed | Wet calls | Model range | Model median | Verdict |
|---|---|---|---|---|---|
| 1997–98 SoCal JFM | 227% | 11/11 | 109–243% | 178% | Hit |
| 2015–16 SoCal JFM | 68% | 9/10 | 94–205% | 160% | Broad miss |
| 2015–16 SoCal DJF | 60% | 9/10 | 99–197% | 149% | Broad miss |
| 2015–16 NorCal JFM | 126% | 9/10 | — | 123% | Hit |
| 2023–24 SoCal JFM | 161% | 5/7 | 87–166% | — | Mixed |

In 2015–16 the only non-wet model was CanCM3, which has no teleconnection. Across all hindcast years in which a model's ensemble-mean NDJ Niño-3.4 was ≥ 2.0 °C, 23% of the 448 pooled individual members had SoCal JFM below normal and 9% below 70%. The model's own noise therefore makes a 2015–16-type outcome plausible, at roughly 1 in 10 for ≤ 70%.

### Sep 2026 real-time forecasts (ensemble mean)
Each model's NDJ Niño-3.4 is relative to its own 1991–2020 climatology.

| Model | NDJ Niño-3.4 | SoCal DJF | SoCal JFM | NorCal DJF | NorCal JFM | Members above normal, SoCal JFM |
|---|---|---|---|---|---|---|
| CanSIPS-IC4 | +3.84 °C | 201% | 198% | 147% | 146% | 78% |
| COLA-CESM1 | +4.10 °C | 209% | 198% | 116% | 124% | 100% |
| COLA-CCSM4 | +3.00 °C | 161% | 170% | 121% | 132% | 90% |
| GEOS-S2S | +4.59 °C | 119% | 133% | 115% | 122% | 80% |
| CFSv2 (9–10 members only) | +3.51 °C | 123% | 112% | 112% | 102% | 70% |

- 5-model median: SoCal DJF 161% and JFM 170%; NorCal DJF 116% and JFM 124%.
- Linear extrapolation of the observed 1950–2025 fit to ONI 3.3 and 3.9 °C gives 172% and 186% for SoCal JFM, and 132% and 138% for NorCal JFM. **This is extrapolation beyond the largest observed NDJ ONI, 2.59.**
- GEOS-S2S and CFSv2 sit well below their own hindcast regression lines for 2026. Their SoCal response is weaker than their Niño-3.4 amplitude would imply, and I have not diagnosed why.

## Caveats
- **Amplitude cannot be validated.** Every 2026 model Niño-3.4 (+3.0 to +4.6 °C) lies beyond the strongest observed event (NDJ ONI 2.59 in 2015). The hindcasts test the sign and slope of the response only up to about 2.6 °C, and the observations show no evidence that the response steepens or saturates at the top of that range.
- **Sample size.** There are only 8 events with ONI ≥ 1.5 and 3 with ONI ≥ 2.0. Composites and hit rates carry large sampling uncertainty.
- **Subseasonal noise.** California's seasonal totals are dominated by a handful of atmospheric-river events, so even a correctly forecast mean shift leaves a wide spread. Ensemble-mean skill is r ≈ 0.3–0.45 in SoCal and ≈ 0.1–0.35 in NorCal.
- **Resolution.** Models run at about 1° (roughly 100 km). Div 6 is covered by 13 partial cells, several of them coastal. Orographic enhancement in the Transverse and Peninsular Ranges and the Sierra is not resolved, which is why % of the model's own normal is used rather than absolute amounts.
- **Index conventions.**
  - Observed ONI uses rolling 30-yr bases, while models use a fixed 1991–2020 base. Over 1982–2025 the mean model-minus-ONI offset is +0.1 to −0.8 °C before 1999 and about 0 afterwards; the large offsets are the CFSR discontinuity described under Methods.
  - RONI (relative) is about 0.6 °C lower than ONI for the 2026 forecasts, per the task brief. Re-expressing model Niño-3.4 in relative terms would shift the 2026 markers left, but they would stay beyond the observed range.
- **Missing and truncated data.**
  - GFDL-SPEAR has no Sep 2026 forecast on the IRI DL as of 2026-09-23. The CFSv2 Sep 2026 EARLY_MONTH_SAMPLES stream had only 9–10 members.
  - C3S models were not analysed here.
- **Choices made in this analysis.** The 1991–2020 normal for observations is the NCEI monthly-sum convention. Model % of normal is relative to each model's own climatology. Using ensemble means of different sizes across streams (for example, GEOS with 4 hindcast and 10 forecast members) changes the noise level from year to year but not the expected mean.
