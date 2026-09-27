# Observed hit rates for the El Niño 2026–27 impacts map: methods

Purpose: one consistent, pre-registered number per impacts-map region (map v5.3): in how many past strong
El Niños was the labelled season wetter/drier (warmer) than a typical neutral year? It is shown next to the
literature confidence tier and the Sep-2026 13-model agreement count in a Climate Brink post.

Plan history: `PLAN.md` (first draft) was reviewed by a statistics reviewer and an ENSO-teleconnections
reviewer (both 24 Sep 2026) before anything was computed. Section 1 below is the revised, pre-registered
specification, written before any hit rate was computed. Results and any later deviations are in section 3,
and each deviation is labelled as such.

## 1. Pre-registered specification

### Events
- **Main set:** NDJ ONI ≥ 1.5 (CPC ONI v5, ERSSTv5; file `oni_cpc_2026-09-15.txt`). That gives 1957-58, 1965-66,
  1972-73, 1982-83, 1997-98, 2009-10, 2015-16 and 2023-24 (n = 8). This is the rule already used for the published
  SoCal (6/8) and Europe NAO (4–4) graphics.
- **Sensitivities:**
  - (a) NDJ RONI ≥ 1.5 (CPC `RONI.ascii.txt`, fetched 24 Sep 2026). This swaps 2023-24 (RONI 1.40) for 1991-92 (1.97), and n stays 8.
  - (b) Drop 2009-10, a central-Pacific event sitting exactly at the 1.50 threshold, giving n = 7.
  - (c) Leave-one-event-out.
  - (d) Moderate events, 1.0 ≤ NDJ ONI < 1.5, as a dose-response check.
- **Reference ("normal") years:** NDJ ONI between −0.5 and +0.5 (ENSO-neutral).
- **Year convention:** year 0 is the year of the NDJ peak. Seasons starting in Sep–Dec belong to year 0. Seasons wholly in Jan–Sep belong to year +1, i.e. the decay year.

### One primary season per region (the map-label window)
Sub-seasons are reported in the CSV only and are not quoted in the post.

| region | expected | primary season | data (main) | data (sensitivity) |
|---|---|---|---|---|
| maritime | dry | Sep–Dec yr0 | GPCC v2025 | PREC/L, GPCP |
| philippines | dry | Dec–Apr | GPCC | PREC/L, GPCP |
| safrica | dry | Dec–Feb | GPCC | PREC/L, GPCP |
| amazon | dry | Oct–May ("now–May") | GPCC | PREC/L, GPCP |
| nsam | dry | Dec–Feb | GPCC | PREC/L, GPCP |
| nebrazil | dry | Mar–May yr+1 | GPCC | PREC/L, GPCP |
| drycorridor | dry | Dec–Feb | GPCC, cells with DJF climatology ≥ 1 mm/day only | PREC/L |
| wpacific | dry | Sep–Feb | GHCN-D station composite | GPCP (ocean + land) |
| cpacific | wet | Sep–May | GPCP (n = 5, 1979–) | Canton Island station (n = 8) |
| hawaii | dry | Nov–Mar | GHCN-D station composite | GPCP, GPCC |
| seaustralia | dry | Sep–Nov | GPCC | PREC/L |
| inlandnw | dry | Dec–Feb | GPCC | PREC/L |
| ccanada_warm | warm | Dec–Feb (temperature) | Berkeley Earth land (Complete_TAVG 1°) | GHCN-CAMS |
| nindia | dry | Jun–Sep yr+1 | GPCC | PREC/L |
| horn | wet | Oct–Dec | GPCC | PREC/L, GPCP |
| peru | wet | Dec–Apr | GHCN-D north-coast airports (n = 5, 1973–) | GPCC (coarse) |
| sesa | wet | Sep–Feb | GPCC | PREC/L, GPCP |
| gulf | wet | Dec–Feb | GPCC | PREC/L |
| antilles | wet | Dec–Feb | GPCC | PREC/L, GPCP |
| swus | wet | Dec–Mar | GPCC | PREC/L; nClimDiv CA div 6 (validation) |
| srilanka | wet | Oct–Dec | GPCC | PREC/L |
| schina | wet | Dec–May | GPCC | PREC/L |
| yangtze | wet | Jun–Aug yr+1 | GPCC | PREC/L |

**Not-on-the-map contrasts** (same machinery, fixed now):

| region | expected | season |
|---|---|---|
| UK + central Europe (`c_uk_ceurope`) | wet | Oct–Dec |
| Scandinavia (`c_scandinavia`) | cold | Jan–Feb |
| Sahel (`c_sahel`) | dry | Jul–Sep yr0 |
| S India (`lit_sindia`) | wet | Oct–Dec |
| southern Mekong (`c_mekong_south`) | dry | Mar–May yr+1 |
| N California (`c_norcal`) | wet | Dec–Mar |
| Ohio Valley (`lit_ohio`) | dry | Dec–Feb |
| SE Alaska / N BC coast (`c_se_alaska`) | warm | Dec–Feb |

For N India, the developing-year monsoon (Jun–Sep yr0) is also reported as the canonical contrast.

### Hit definition
1. **Regional mean.** Seasonal regional-mean precipitation (mm/day), area-weighted by cos(lat) × the fraction of each cell inside the map polygon. At least 50% of the weight must have data. Station groups use the mean over stations of the seasonal total divided by that station's reference-year median (a "ratio index"), computed only from stations with a complete season.
2. **Detrending.**
   - Precipitation: a Theil–Sen linear trend fitted on reference (neutral) years only, over 1951–2024. It is removed from all years.
   - Temperature: a LOWESS fit on reference years (frac = 0.5) is removed from all years. This absorbs the post-2010 acceleration that a linear fit would leave in 2015-16 and 2023-24. It is the conservative choice, because it removes more warming.
3. **Percentile.** Each year's detrended value is expressed as a percentile of the reference-year distribution: the empirical CDF with a (rank − 0.5)/n plotting position, interpolated.
4. **Hit.** Primary: beyond the 50th percentile in the expected direction. Base rate = 50% by construction in neutral years. Secondary: beyond the expected tercile (base rate 1/3).
5. **Near-normal sensitivity.** Event-seasons between the 40th and 60th percentiles count as neither hit nor miss.
6. **Magnitude.** The median percentile across strong events is reported, plus % of the 1991–2020 mean for context. Percent of normal is not used for dry-season regions.
7. **Data quality.** GPCC `gauge` counts are summed over cells touching the region. An event-season with fewer than 5 gauges on average is flagged. For station groups, fewer than 2 reporting stations is flagged.

### Communication rules (fixed before seeing results)
- 8/8 or 7/8: "nearly every time" / "in all but one"
- 6/8: "usually"
- 5/8: "more often than not, but weakly"
- 4/8 or fewer: "no consistent pattern"
- For n = 5: only 5/5 is called consistent. 4/5 is "usually, small sample".
- Counts are never presented as probabilities. Under a coin flip, P(≥6/8) ≈ 14% and P(≥7/8) ≈ 3.5%.
- The hit counts are not independent confirmation of the literature tier. The canon was partly built on these same events (1982-83, 1997-98, 2015-16). The count restates the historical record the tier rests on in countable form.
- Map-level summary: total hits across all map regions vs. total expected at 50%. Regions are correlated within an event, so the effective n is closer to 8 than to 8 × 23.
- Per-event column totals (fraction of regions hit) are shown, to support the "every El Niño is different" message.

### Per-event context columns (used in the text, not for sub-hit-rates)
- SON DMI (HadISST, NOAA PSL): for Horn, SE Australia, Maritime and Sri Lanka.
- DJF PDO (NCEI ERSSTv5): for the North American regions and Hawaii.

## 2. Validation targets (before trusting results)
1. The swus Dec–Mar result vs NOAA nClimDiv CA division 6: 6/8 strong winters above normal (model_patterns/hindcast). Also the NCEI statewide AZ/NM DJF % of normal for 1982-83, 1997-98, 2015-16 and 2023-24 (research/lit_missing_americas.md).
2. Climatology sanity checks against known seasonal normals: Jakarta SON, Los Angeles DJF, Nairobi OND, Manila DJFMA.
3. GPCC vs PREC/L vs GPCP sign agreement per region and event, 1982 onward.
4. Southern Africa: Pomposi et al. (2018) state ~80% probability of below-normal rain in strong events. Their domain, season and event definition must be checked before this is used as a target.

## 3. Results and deviations (computed 24 Sep 2026)

### Deviations from §1 (each decided after data coverage was known, before interpreting results unless noted)
1. **Peru main source changed to GPCC** (`peru` map polygon). The GHCN-D north-coast airport series have usable
   Dec–Apr seasons only through ~2005 (1982-83 and 1997-98 only). Stations kept as a sensitivity (n = 2).
   GPCC at 1° cannot resolve the coastal plain; the Peru count is therefore not quoted as a headline (see caveats).
2. **Central Pacific station sensitivity unusable.** Canton Island (1950–67) covers 1957 and 1965 only
   (Sep–May totals 1,851 and 1,780 mm vs a neutral-year median of 280 mm, both hits); Tarawa and Funafuti have
   too few complete Sep–May seasons. GPCP (n = 5) remains the main source as planned.
3. **Minimum reference seasons per station lowered from 10 to 6** (needed for Canton).
4. **Latent bug fixed:** the ≥50%-coverage rule in `extract.py`/`gpcc_extract.py` compared against total polygon
   weight including ocean, which returned all-NaN series for 8 mostly-ocean shapes (hawaii, box_hawaii, wpacific,
   cpacific, lit_sindia, lit_camerica, lit_wpacific, lit_cpacific) in PREC/L and GPCC. No main-source result was
   affected (those regions' main sources are stations/GPCP); the S India contrast and gridded Hawaii/W Pacific
   sensitivities were recovered after the fix (coverage now relative to the maximum land weight observed).
5. **Map v6 changes made on the basis of these results (author decisions, 24 Sep 2026):** N & Central India removed
   (1/8); Yangtze downgraded med-high → medium ⚠ and relabelled Jun–Jul; southern Mekong added at medium with a
   hand-drawn polygon, whose hit rate was then recomputed on the drawn shape (7/8, same as the pre-registered box).
   **Post-hoc:** the Yangtze Jun–Jul check (6/8) was run after seeing the pre-registered Jun–Aug result (4/8) and
   is reported as such.

6. **Map v6.1 (author decision, 24 Sep 2026): N California added at medium.** The shape is the pre-registered
   model-test box (124.5–120°W, 38–42°N; region_table 13/13 DJF, robust fraction 1.0) clipped to California and
   buffered 0.3°. Hit rate recomputed on the drawn shape: 6/8 (same as the box). Weak ENSO specificity
   (La Niña same side 7/12; moderate events 2/6) is stated in the post. Map-level summary becomes 164 of 189
   region-events (87%) across 24 regions; per-event: 1957-58 74%, 1965-66 65%, 1972-73 91%, 1982-83 100%,
   1997-98 100%, 2009-10 83%, 2015-16 92%, 2023-24 88%.

7. **Map v6.4 (author decision, 24 Sep 2026): Chile/Altiplano, after a suggestion from a Chilean colleague.** Literature: research/lit_chile_altiplano.md. Boxes were fixed from the colleague's sketch before any results, then narrowed per the literature and fixed again before results.
   - *Altiplano, dry Dec–Mar (added at medium):* 6/8 on the box (71–66°W, 22–14°S); **5/8 on the drawn outline**, which excludes the Titicaca basin. Models 13/13 DJF, z −3.0, 93% of cells robust.
   - *Central Chile 35–38°S, wet Oct–Nov yr0 (added at medium):* 7/8 (median 170%); 6/6 moderate events; La Niña 3/12. Models SON 11/13, OND 13/13, 100% of cells robust. The 30–40°S box gives 7/8 for Sep–Nov.
   - *Not mapped:* central Chile Mar–Sep yr+1 (2/8, median 89%); S-central Chile 38–42°S Jan–Mar (obs 7/8, but models JFM 2/6 and DJF 7/13, no robust cells); W Patagonia 40–52°S DJF (obs 6/8, La Niña 6/12; models 13/13, but literature low south of 42°S); Atacama (gauge-sparse and zero-heavy, so percentiles are unreliable; the literature signal is in the yr0 winter, now past).
   - Map-level summary with 26 regions: 176/205 (86%). Per event: 1957-58 68%, 1965-66 68%, 1972-73 88%, 1982-83 100%, 1997-98 100%, 2009-10 81%, 2015-16 92%, 2023-24 88%.

### Validation
- GPCC v2025 statewide DJF % of 1991–2020 normal vs NOAA NCEI (research/lit_missing_americas.md), for 1982-83,
  1997-98, 2015-16, 2023-24: CA 149/179/93/116 vs 147/179/103/121; AZ 153/162/68/104 vs 147/157/66/115;
  NM 170/138/72/119 vs 168/133/88/120. Mean absolute difference ~5 pp (max 16 pp, NM 2015-16); above/below-100% sign
  agrees in 11 of 12 (CA 2015-16: 93 vs 103).
- Southern Africa 6/8 (75%) is consistent with Pomposi et al. (2018) ~80% below-normal for strong events
  (their domain/definition differ; not a like-for-like check).
- Climatologies plausible: Maritime Sep–Dec 6.5 mm/day; SW US Dec–Mar 1.0 mm/day; N India Jun–Sep 6.5 mm/day
  (~790 mm/season; all-India long-period average ~870 mm).

### Main results (strong events, NDJ ONI ≥ 1.5, n = 8 unless noted)
Columns: hits = on the expected side of the neutral-year median; terc = in the expected tercile; RONI = event set
with 1991-92 replacing 2023-24; LOO = leave-one-out range; mod = moderate events (1.0–1.5); LN = La Niña years
(NDJ ≤ −1.0) on the *El Niño* side (should be low if the signal is ENSO-specific); med% = median strong-event
percentile of neutral years; %N = median % of 1991–2020 normal (°C anomaly for temperature).

| region | season | source | hits | terc | RONI | mod | LN | med% | %N |
|---|---|---|---|---|---|---|---|---|---|
| Maritime Continent | Sep–Dec | GPCC | 8/8 | 8 | 8/8 | 6/6 | 1/12 | 0 | 73 |
| Philippines | Dec–Apr | GPCC | 8/8 | 8 | 8/8 | 6/6 | 1/12 | 4 | 58 |
| Southern Mekong | Mar–May +1 | GPCC | 7/8 | 7 | 7/8 | 2/6 | 1/12 | 5 | 71 |
| Southern China | Dec–May | GPCC | 5/8 | 5 | 5/8 | 3/6 | 2/12 | 80 | 127 |
| Yangtze | Jun–Aug +1 | GPCC | 4/8 | 3 | 4/8 | 0/6 | 4/12 | 53 | 99 |
| Sri Lanka | Oct–Dec | GPCC | 8/8 | 8 | 8/8 | 5/6 | 8/12 | 91 | 126 |
| SE Australia | Sep–Nov | GPCC | 7/8 | 6 | 7/8 | 5/6 | 6/12 | 19 | 81 |
| W Pacific islands | Sep–Feb | stations | 8/8 | 8 | 8/8 | 6/6 | 2/12 | 0 | 82 |
| Central Pacific islands | Sep–May | GPCP | 5/5 | 5 | 5/5 | 5/5 | 0/8 | 100 | 207 |
| Southern Africa | Dec–Feb | GPCC | 6/8 | 5 | 6/8 | 5/6 | 2/12 | 14 | 87 |
| Horn of Africa | Oct–Dec | GPCC | 8/8 | 8 | 7/8 | 4/6 | 4/12 | 91 | 131 |
| Amazon | Oct–May | GPCC | 7/8 | 7 | 7/8 | 4/6 | 6/12 | 0 | 92 |
| N South America | Dec–Feb | GPCC | 8/8 | 8 | 8/8 | 6/6 | 1/12 | 0 | 71 |
| NE Brazil | Mar–May +1 | GPCC | 6/8 | 4 | 7/8 | 2/6 | 3/12 | 26 | 79 |
| Peru/Ecuador coast | Dec–Apr | GPCC (coarse) | 7/8 | 7 | 7/8 | 4/6 | 8/12 | 79 | 103 |
| SE South America | Sep–Feb | GPCC | 7/8 | 7 | 8/8 | 5/6 | 3/12 | 100 | 115 |
| Central America & S Caribbean | Dec–Feb | GPCC, ≥1 mm/day cells | 5/8 | 5 | 5/8 | 5/6 | 0/12 | 23 | 93 |
| Cuba & Bahamas | Dec–Feb | GPCC | 8/8 | 8 | 8/8 | 5/6 | 3/12 | 100 | 163 |
| US Gulf Coast & Southeast | Dec–Feb | GPCC | 8/8 | 7 | 8/8 | 5/6 | 1/12 | 91 | 125 |
| S California, SW US & N Mexico | Dec–Mar | GPCC | 7/8 | 7 | 7/8 | 4/6 | 3/12 | 90 | 137 |
| Hawaii | Nov–Mar | stations | 6/8 | 6 | 6/8 | 5/6 | 6/12 | 5 | 69 |
| Interior BC & inland NW | Dec–Feb | GPCC | 7/8 | 7 | 6/8 | 4/6 | 4/12 | 29 | 95 |
| Central Canada (temp) | Dec–Feb | Berkeley Earth | 8/8 | 5 | 8/8 | 5/6 | 7/12 | 86 | +0.7 °C |
| *not on map:* N & Central India | Jun–Sep +1 | GPCC | 1/8 | 1 | 2/8 | 2/6 | 2/12 | 82 | 108 |
| N & Central India (developing yr) | Jun–Sep yr0 | GPCC | 8/8 | 6 | 8/8 | 6/6 | 4/12 | 5 | 89 |
| Sahel | Jul–Sep yr0 | GPCC | 3/8 | 3 | 4/8 | 5/6 | 3/12 | 68 | 98 |
| Southern India | Oct–Dec | GPCC | 7/8 | 6 | 7/8 | 4/6 | 7/12 | 95 | 120 |
| UK & central Europe | Oct–Dec | GPCC | 5/8 | 4 | 4/8 | 4/6 | 4/12 | 77 | 108 |
| Scandinavia (cold) | Jan–Feb +1 | Berkeley Earth | 5/8 | 5 | 4/8 | 3/6 | 6/12 | 16 | −0.7 °C |
| N California | Dec–Mar | GPCC | 6/8 | 6 | 5/8 | 2/6 | 7/12 | 73 | 116 |
| Ohio Valley (dry) | Dec–Feb | GPCC | 4/8 | 1 | 5/8 | 3/6 | 5/12 | 46 | 97 |
| SE Alaska & N BC coast (warm) | Dec–Feb | Berkeley Earth | 6/8 | 5 | 6/8 | 5/6 | 4/12 | 73 | +0.6 °C |

Full table incl. drop-2009-10, excluding-near-normal and leave-one-out columns: `derived/hit_summary.csv`.

### Sensitivities (main count → alternatives)
- Dataset: PREC/L agrees within ±1 hit for most regions; larger drops for southern Africa (6 → 5), inland NW (7 → 5).
  GPCP (n = 5) gives 5/5 for every tested land region except Horn RONI (4/5).
- **Shape selection:** inland NW falls from 7/8 (model-shaped polygon) to **3/8** with a simple box fixed from the
  label (125–110°W, 45–56°N). The inland-NW signal is shape-dependent and should be described as such.
  SE Australia (7 → 7), Sri Lanka (8 → 8), Cuba & Bahamas (8 → 8), Central Canada (8 → 8), Hawaii (6 → 7 GPCC box)
  are robust to the box test. Literature-polygon versions: Horn 8, SE S America 8, Gulf 8, Yangtze 4, Peru 6, N India 1.
- **Temperature trend dependence (Central Canada):** all 8 strong winters above the neutral-year median after LOWESS
  detrending, but only 5 in the upper tercile, and 7 of 12 La Niña winters are also above the median. The El Niño
  specificity of this signal is weak in the observed record; the four post-1982 events are clearly warm (+1.9 to
  +4.9 °C vs 1991–2020).
- **Low La Niña discrimination** (LN ≥ 6/12) also for Sri Lanka, Amazon, SE Australia, Hawaii and Peru: the
  El Niño-side count is high but the same side also occurs in many La Niña years, so these counts overstate
  El Niño specificity. Reported in the post for Peru; others noted in NOT-FOR-PUBLICATION notes.
- **Map-level summary:** 158 of 181 region-events (87%) on the expected side (23 map regions; 50% expected by chance;
  regions are correlated within events, so this is not 181 independent trials). By event: 1982-83 and 1997-98 100%
  of regions, 2015-16 91%, 1972-73 91%, 2009-10 87%, 2023-24 87%, 1957-58 73%, 1965-66 68%. The two earliest
  events have the sparsest gauge networks; the pattern is also consistent with the canon having been built on 1982-83
  and 1997-98 (circularity caveat, §1).
- Data quality: only one main-source strong-event season below 5 gauges (Cuba & Bahamas 2023-24, 3.7 gauges).

### Caveats
- n = 8. Under a coin flip P(≥7/8) ≈ 3.5% and P(8/8) ≈ 0.4% for a single region, but ~30 regions were examined.
- The event record contains no event of 2026's forecast size; hit rates are for "strong", not "record" events.
- Coarse-grid regions (Peru coast, Sri Lanka, SE Australia) and PREC/L relaxation to climatology where gauges are
  sparse (hence GPCC as main).

## Two benchmarks: counts vs percentages (added 25 Sep 2026)

- **Counts** (`hit`, `hits`): the event is on the expected side of a *typical neutral year*, the neutral-year Theil-Sen trend plus the median neutral residual.
- **Percentages quoted in the post** (`pct_normal`, `median_pct_normal_strong`): % of the raw 1991–2020 mean.
- **New columns:** `pct_typical` in `hit_events.csv` and `median_pct_typical_strong` in `hit_summary.csv`. They express each season relative to the typical neutral year: % for precipitation, °C anomaly for temperature. A hit ⇔ `pct_typical` on the expected side of 100% (or 0 °C). This holds for every event, except neutral years sitting exactly on the median.
- **Rerun check:** all pre-existing columns were verified byte-identical after the rerun.
- **Why the two can disagree:** in skewed climates a few extreme years pull the 1991–2020 mean away from a typical year. In 24 of 309 strong-event region-rows, the % of the 1991–2020 mean sits on the other side of 100% from the hit. Examples: Horn 1957 at 97.5% (typical neutral year ≈ 81% of the mean), Peru 2009/2015/2023, Sri Lanka 1982/2009, SE Australia 2009, Yangtze 1972/2023, Altiplano 2023, Central America 2015, SE South America 2023.
- **Decision (Zeke, 25 Sep 2026):** keep magnitudes as % of the 1991–2020 mean everywhere. Word counts as "than a typical neutral year". Show the typical-neutral-year level alongside where both appear (video strips).
- **Why the magnitude alternative was rejected:** % of a typical neutral year inflates magnitudes in dry, skewed regions. For example, coastal SoCal (nClimDiv div. 6) DJF 2015–16 becomes 103% instead of 60%, Peru 2023 becomes 114% instead of 90%, and the Cuba median becomes 208% instead of 163%.

## Bars rebased on the typical neutral year (27 Sep 2026)

- **Bars.** The dashboard's and the video's per-event bars now show each event as a % of the typical neutral year (`pct_typical`), the same reference as the x/8 checks. A bar above or below 100% therefore always matches its check. The 1991–2020 average is drawn as the marker line (`10000 / typ_level`).
- **Unchanged.** Forecast shading, the model tiles and counts, and the percentages quoted in the post stay relative to the 1991–2020 average.
- **Why the forecasts weren't rebased.** Before deciding, Zeke previewed a full rebase (`export_dashboard.py` with `BASELINE=typical`, `model_patterns/windows.window_typical`). That version used a per-cell GPCP typical neutral year: the Theil-Sen trend through the neutral years, extended to 2026, plus the median residual. It reproduces analyze.py's GPCP values to 2e-16. It was rejected for four reasons:
  - With a forecast of exactly normal rainfall, 61% of the map would still be shaded by 10% or more. The map would mostly show the baseline rather than the forecast.
  - GPCP has only 13 neutral years (1979–2023) for Sep–Feb seasons and 14 for Mar–May, so the per-cell trend is noisy.
  - GPCC and GPCP typical levels differ by 10 points or more in about a third of regions.
  - Model anomalies are ensemble-mean departures from each model's own hindcast average. Rebasing them is a rescaling of the same numbers, and it compares a mean with a median.
