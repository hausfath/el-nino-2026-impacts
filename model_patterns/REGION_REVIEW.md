# Region-by-region review: literature vs. September 2026 models vs. hindcasts

**Status: APPLIED in map v5 (23 Sep 2026).** Author decisions:
- Ohio Valley removed.
- S India hatched ("models disagree") rather than removed.
- Caribbean split, with "summer 2027" dropped. The wet region is labelled "Cuba & Bahamas" because the models don't support a wet Yucatán (z −0.44).
- S California, US Southwest and N Mexico merged at medium ⚠.
- All four new regions (#21–24) added.
- Other rows applied as recommended. The "cool" option for #11 was not applied.

Model columns come from `derived/region_table.csv`: sign agreement across 13 models (C3S + NMME) for SON/OND/DJF, and 6 NMME models for JFM/MAM. z is the multi-model mean divided by the observed interannual SD. "Robust" = FDR-significant, |z| ≥ 0.5 and ≥ 25% of cells robust. Literature tiers come from the dossier (`research/impacts-literature.md`) and the new searches (`research/lit_missing_americas.md`, `lit_missing_asiapacific.md`, `lit_africa_iod.md`). Every DOI in those files was re-verified against Crossref.

Rule applied: **fill colour = literature tier; shape = model-robust extent.** Where models and literature disagree, the recommendation leans toward the more conservative (smaller or lower-tier) option.

## Existing map regions

| # | Region (current label) | Lit tier | Models (season: agree, z) | Recommendation |
|---|---|---|---|---|
| 1 | Indonesia & Maritime Continent: drought + fire, Sep–Feb | high | SON 13/13, −1.05 robust; DJF 9/13, −0.38 weak | **Reshape** to model extent over the islands. **Relabel season "Sep–Dec"**, since the DJF signal fades. Keep high. |
| 2 | Southern Africa: drought, Dec–Feb | high | DJF 13/13, −0.59 robust; JFM 6/6 | **Reshape.** Keep high, with no flag: 1997–98 was a real failure, but 2023–24, with an IOD about as strong (SON DMI +0.89 vs +0.98), gave the worst drought on record. Add the 1997–98 note to NOTES. |
| 3 | Amazon: drought + fire, now–May | high | SON/DJF 13/13 (−1.6/−1.8); MAM 6/6 | **Reshape.** The model extent reaches into northern South America (see #21). |
| 4 | NE Brazil: drought, Mar–May 2027 | med-high | MAM 6/6, −1.15 robust (NMME only) | **Reshape.** Keep. |
| 5 | Central America & Caribbean: drought, Dec–Feb & summer 2027 | med-high | Dry Corridor DJF 13/13, −1.82; **Greater Antilles DJF 13/13, +2.57 (WET)** | **Split.** (a) "Central America & S Caribbean: drought, Dec–Feb", reshaped. (b) New "Greater Antilles & Yucatán: wet, Dec–Feb" (Giannini et al. 2000), med-high. **Unresolved:** the Americas search says the midsummer drought is a developing-year (2026) Jul–Aug feature and that the Caribbean early rainy season in 2027 tends *wet* (Chen & Taylor 2002). Dossier §A10 puts the strongest midsummer-drought signal in 2027. Proposal: drop "summer 2027" from the label until resolved. |
| 6 | W Pacific islands: drought, sea-level fall | med-high | SON 13/13, −1.28; DJF 13/13, −0.70 | **Reshape.** Keep. |
| 7 | E Australia ⚠: drought, fire risk, Sep–Feb | medium ⚠ | SON 10/13, −0.24 (not significant after FDR); OND 6/13; DJF 7/13 | **Relabel "Sep–Nov".** The literature (Cai et al. 2011) supports spring only. Keep medium + ⚠ and the hand-drawn shape, because no model support exists to reshape it. NOTES: this year's models show little signal. |
| 8 | Horn of Africa: floods, Oct–Dec (IOD-dependent) | medium | OND 13/13, +0.64 robust; DJF 13/13, +0.53 | **Reshape.** Keep medium. NOTES: models are known to have an IOD-related wet bias (Hirons & Turner 2018). |
| 9 | Peru / Ecuador coast ⚠: flooding, Dec–May | medium ⚠ | DJF 13/13, +2.27; MAM 6/6 | Keep the **hand-drawn** narrow strip. The sign is confirmed, but the 1° grid can't resolve the coastal plain. |
| 10 | SE South America: heavy rain, floods, Sep–Feb | high | SON 13/13, +0.63; DJF 13/13, +0.91 | **Reshape.** Keep. |
| 11 | US Gulf Coast & Southeast: wet, stormy, Dec–Feb | high | DJF 13/13, +1.08; JFM 6/6; temp DJF cool 11/11, −1.19 robust | **Reshape.** Option: add "cool" to the label (Ropelewski & Halpert 1986). |
| 12 | S India / Sri Lanka: heavy NE monsoon, Oct–Dec | medium | **OND 4/13, −0.28 (leans dry)** | Models contradict it. **Recommend removing** and noting it in NOTES. Alternative: keep with a new "models disagree" flag. |
| 13 | Yangtze basin ⚠: flood risk, summer 2027 | med-high ⚠ | beyond forecast range | No change (literature only). |
| 14 | Pacific NW: dry, warm, Dec–Feb | high | precip DJF 10/13, −0.21 weak; temp +0.89 trend-adjusted but +0.08 with land-mean removed | Models weak. **Recommend downgrading to medium-high** and keeping the hand-drawn shape. |
| 15 | Ohio Valley: dry, warm, Dec–Feb | high | **precip DJF 1/13 dry (z +0.34, leans wet); temp no signal (5/11)** | Models contradict both parts. **Recommend removing.** |
| 16 | N & Central India ⚠: weaker monsoon, Jun–Sep 2027 | medium ⚠ | beyond range | No change. |
| 17 | Central Pacific islands: wet, inundation, Sep–May | med-high | SON 13/13, +3.58; DJF 13/13, +1.94 | **Reshape.** Keep. |

## New regions

| # | Region | Lit tier (new searches) | Models | Hindcast / obs | Recommendation |
|---|---|---|---|---|---|
| 18 | Southern California: wet, Jan–Mar | med-high teleconnection, 2015–16 miss | DJF 13/13, +1.14; JFM 6/6, +1.07; NMME P(above) 50–56% | Obs 1950–2025: +24 pp/°C, r = 0.39; strong events median 148% (JFM), 6/8 above normal. Hindcast slope ratio 0.97 (not overstated). **2015–16: 9/10 models wet, observed 60–68% of normal.** | **Add at medium + ⚠** (decided). **Proposal: merge with #19** into "S. California, US Southwest & N Mexico: wet, Dec–Mar ⚠" at medium, since both share the 2015–16 failure. |
| 19 | N Mexico / US Southwest: wet, Dec–Mar | med-high (2015–16 AZ 66%) | DJF 10/13, +0.61 | station composites wet in 1982–83, 1997–98, 2023–24 | Merge with #18 (above). |
| 20 | Northern California | obs DJF r = 0.18 (not significant), JFM r = 0.27; strong events 7/8 wet (JFM) | DJF 13/13, +1.14; 2026 NMME 102–146% | NorCal 2015–16 was a hit | **Keep unshaded** (weak full-record relationship). NOTES and thread: models lean wet statewide. |
| 21 | Northern South America (Colombia, Venezuela): dry, Dec–Feb | med-high (DJF); SON not verified | SON 13/13, −2.15; DJF 13/13, −1.33 | not tested | **Add at med-high, "Dec–Feb"**, or merge into the Amazon polygon (#3). |
| 22 | Philippines: dry, Dec–Apr | med-high (DJF), medium (MAM) | DJF 13/13, −1.49; MAM 6/6; NMME P(below) 70–72% | not tested | **Add at med-high.** |
| 23 | Southern China: wet, Dec–May | med-high | DJF 12/13, +0.57; MAM 6/6, +0.76 | not tested | **Add at med-high.** |
| 24 | Hawaii: dry, Nov–Mar | med-high (EP events) | DJF 13/13, −1.34; P(below) 66–69% | no past-event check | **Add at med-high.** |
| 25 | Mekong (mainland SE Asia): dry, MAM | medium (narrow), low (basin-wide) | MAM 4/6, −0.69 (not significant) | — | **Don't add.** |
| 26 | Alaska / W Canada: warm | medium, coastal only; weakened under −PDO (now about −1.8) | DJF 9/11, +0.36 moderate | — | **Don't add.** |

## Latent issues found along the way (flagged, not yet fixed)

- **Dossier misattribution:** `impacts-literature.md` §A11 cites Jong et al. 2016 (ERL) for "2015–16 near-normal SoCal precipitation". The paper predates the outcome ("It will be interesting to see if the El Niño of 2015/16 impact... conformed to expectations"). Station data (NOAA nClimDiv, CA div. 6) give **60% (DJF) and 68% (JFM) of the 1991–2020 normal**: below normal, near the edge of the dry tercile. "Near-normal" is only defensible in tercile terms. Recommend correcting the dossier and `figures/NOTES.md`, citing the station data or Siler et al. 2017 (doi.org/10.1175/JCLI-D-17-0177.1, verified).
- **1991 IOD:** the Africa agent's HadISST calculation gives an SON DMI of about +0.04 °C for 1991 (neutral), in case any backing material calls it positive.
- **Climate Dashboard:** the NCAR-CESM1 NMME climatology period is undocumented on CPC, so its Niño3.4 baseline offset can't be quantified. The other NMME models it retains (CCSM4, GEOS) are on 1992–2019, a negligible offset.

## v5.1 follow-up (23 Sep 2026, applied)
Checked the remaining hand-drawn regions against the models (`figures/diag_handdrawn_check.png`, `figures/diag_north_america_djf.png`). Applied:
- **Pacific NW** → model-derived interior BC / N Rockies / inland Northwest, dry, low snowpack, medium.
- **Central Canada warm winter** added, medium, trimmed at ~79.5°W.
- **E Australia** → SE Australia (Sep–Nov, keeps ⚠).
- **S India / Sri Lanka** → Sri Lanka only, unhatched.
- **Peru strip** tightened to the coast.

Evidence and the selection-effect caveat are in `figures/NOTES.md`. Literature: `research/lit_canada_nw.md`.

## v5.2 (23 Sep 2026, applied)
S California / US Southwest / N Mexico upgraded from medium to medium-high, with ⚠ kept. The basis is observations: 6 of 8 strong El Niño winters since 1950 were in the upper tercile, P ≈ 0.02. Details are in figures/NOTES.md.

## v5.3 (23 Sep 2026, applied)
Peru/Ecuador coast changed from medium ⚠ to high, with no flag and Dec–Apr. Mid-September Niño 1+2 is +4.6 °C, and all six NMME models keep Jan–Mar at +1.9 °C or more, above the failed 2015–16 and 2023–24 values. Details are in figures/NOTES.md and derived/peru_nino12.csv.
