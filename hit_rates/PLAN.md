# Observed hit rates for the El Niño 2026–27 impacts map: analysis plan (pre-review)

Goal: for each region on the impacts map (v5.3), a single consistent, pre-registered number
"in X of N past strong El Niños, this region was wetter/drier (warmer) than normal in the labelled season",
for a Climate Brink post that walks region by region through likelihoods. Shown alongside the
literature tier and the Sep-2026 13-model agreement count.

## Event set (pre-registered)
- Main: NDJ ONI >= 1.5 (CPC ONI v5, ERSSTv5, file oni_cpc_2026-09-15.txt): 1957-58, 1965-66,
  1972-73, 1982-83, 1997-98, 2009-10, 2015-16, 2023-24 (n = 8). Same rule already used for the
  published SoCal (6/8) and Europe NAO (4-4) graphics.
- Sensitivity A: peak OND/NDJ/DJF ONI >= 1.5 (adds 1991-92, n = 9).
- Sensitivity B: CPC RONI peak >= 1.5 (relative index; expected to drop 2023-24 at 1.42 and possibly others).
- Year convention: "year 0" = year of the Nov peak. Seasons SON/OND/DJF refer to year 0 (DJF = Dec yr0–Feb yr1);
  MAM/JJA/JJAS refer to year +1.

## Data
- Precipitation: NOAA PREC/L 1° monthly land (Chen et al. 2002), 1948–Aug 2026, gauge-based (GHCN + CAMS).
  Known issue: gauge counts decline after ~2000 in parts of Africa/Asia.
- Sensitivity / ocean-island regions: GPCP v2.3 monthly 2.5° (1979–), already on disk — covers only
  1982, 1997, 2009, 2015, 2023 (n = 5). Used as the main source for ocean/small-island regions
  (W Pacific islands, Central Pacific islands, Hawaii) and as a cross-check for land regions.
- Temperature (Central Canada warm winter only): GHCN-CAMS 2 m temperature 0.5° (1948–) or Berkeley Earth 1°.

## Regions & seasons (from the map labels)
Polygon = the exact v5.3 map polygon (model-derived shapes from model_polygons.json; hand-drawn shapes buffered as
drawn). Sensitivity: the frozen pre-model literature polygons (lit_polygons_v4.json) where they exist, to address
the concern that shapes were chosen where 2026 models agree.

| key | sign | season | notes |
|---|---|---|---|
| maritime | dry | SON | |
| philippines | dry | DJF (label Dec–Apr; also test FMA/MAM yr+1) |
| safrica | dry | DJF | compare to Pomposi et al. 2018 ~80% below-normal for strong events |
| amazon | dry | SON and DJF (label "now–May") |
| nsam | dry | DJF |
| nebrazil | dry | MAM yr+1 |
| drycorridor | dry | DJF (climatological dry season; % anomalies noisy) |
| wpacific | dry | SON/DJF (GPCP, ocean) |
| cpacific | wet | SON/DJF (GPCP, ocean) |
| hawaii | dry | NDJFM (GPCP + PREC/L cells if any) |
| seaustralia | dry | SON |
| inlandnw | dry | DJF |
| ccanada_warm | warm | DJF (temperature) |
| nindia | dry | JJAS yr+1 |
| horn | wet | OND |
| peru | wet | DJFMA (coastal strip; 1° grid marginal) |
| sesa | wet | SON and DJF (label Sep–Feb) |
| gulf | wet | DJF |
| antilles | wet | DJF |
| swus | wet | DJFM |
| srilanka | wet | OND |
| schina | wet | DJF and MAM yr+1 |
| yangtze | wet | JJA yr+1 |
Plus "not on the map" contrasts: Europe (UK/central Europe OND wet; N Europe JF cold), Sahel JAS yr0 dry,
S India OND wet, Mekong (southern basin) MAM yr+1 dry, N California DJF wet, Ohio Valley DJF dry.

## Hit definition
- Area-weighted (cos lat) regional-mean seasonal total over land cells inside the polygon.
- Main: anomaly relative to a linear trend fitted over all years 1950–2025 (so base rate ≈ 50% and long-term drying/wetting
  trends don't count as hits). A "hit" = sign matches expected sign.
- Stricter secondary: in the expected tercile (upper/lower third of detrended 1950–2025 distribution; base rate 1/3).
- Report counts (X of N) and the median % of normal (vs 1991–2020 climatology) across the strong events.
- Report binomial P(>= X of N | p = 0.5) in the methods file only; the post shows counts, not significance stars
  (24+ regions, so multiple-testing: expect ~1 region at p<0.05 by chance under no signal).

## Validation (before trusting)
1. SoCal/SW US: compare PREC/L swus result for DJF/JFM against NOAA nClimDiv CA div 6 (6/8 above normal) and the
   NCEI statewide AZ/NM/CA DJF % of normal for 1982-83, 1997-98, 2015-16, 2023-24 (lit_missing_americas.md table).
2. Southern Africa: compare the strong-event below-normal fraction with Pomposi et al. 2018 (~80%).
3. Sanity-check PREC/L climatologies against known normals (e.g., Jakarta, Los Angeles, Nairobi seasonal totals).
4. Cross-check PREC/L vs GPCP sign agreement for 1982, 1997, 2009, 2015, 2023 in each land region.

## Outputs
- hit_rates/derived/hit_table.csv (region × event: anomaly, % normal, hit flag; per dataset/sensitivity)
- A figure: rows = regions (grouped by continent), columns = the 8 events, cell colour = drier/wetter than trend,
  marker for hit/miss; right-hand column with the 13-model count for 2026.
- hit_rates/METHODS.md with all parameter choices and sensitivity results.
