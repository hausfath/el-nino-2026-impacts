# El Niño 2026–27 map: literature check for candidate Americas regions

Prepared 2026-09-23. Scope: five candidate regions (A–E) where dynamical seasonal models are expected to show signals. A region is recommended for the map only if peer-reviewed literature supports the teleconnection.

**How things were verified**
- Every DOI below was resolved through the Crossref API (`https://api.crossref.org/works/<DOI>`), and the returned title, authors and year were checked against the citation. Where Crossref's `issued` year is the online-first year, both years are given.
- Quote tags:
  - **[VERIFIED-PRIMARY: URL]**: read verbatim from the publisher page or full-text PDF.
  - **[ABSTRACT-ONLY]**: verbatim abstract text taken from the publisher-deposited Crossref record, the OpenAlex record, or an OSTI mirror. Full text not read.
  - **[SECONDARY/UNVERIFIED]**: paraphrase, news, or a subagent read that I did not re-check myself.
- Region B and D observed outcomes were **computed** from NOAA NCEI Climate at a Glance DJF series, the CPC ONI (local file `oni_cpc_2026-09-15.txt`) and the NCEI ERSSTv5 PDO index. Script: `research/check_obs_composites_americas.py` (stdlib only; it re-downloads the data). "El Niño winters" means DJF ONI ≥ 1.0 over 1950–2025 (n = 10); "strong" means ONI ≥ 1.5 (n = 7: 1957-58, 1972-73, 1982-83, 1991-92, 1997-98, 2015-16, 2023-24).
- Process caveat: the session's web-search budget ran out partway through. Several agency event reports (especially for 1982-83 and 1997-98) could not be retrieved, and those gaps are flagged rather than filled.

> **Cross-cutting flag: the PDO is strongly negative.** The NCEI ERSSTv5 PDO was −1.72 (Jun), −2.14 (Jul) and −1.84 (Aug 2026). Several of the papers below (Gershunov & Barnett 1998; Bonsal et al. 2001; Papineau 2001; Pavia et al. 2006) find that North American El Niño teleconnections are weaker or less consistent when the North Pacific is in its cold phase. This matters most for Region D (see below).

---

## Summary table

| Region | Season | Sign | Tier | Key DOI |
|---|---|---|---|---|
| N South America (Colombian Caribbean/Andes, Guianas) | DJF (MAM weaker); SON low confidence | dry | medium-high (DJF); low (SON) | https://doi.org/10.1007/s00382-010-0931-y |
| N Mexico / US Southwest | DJF/JFM | wet | medium-high | https://doi.org/10.1175/1520-0442(1999)012%3C2881:EAHEIT%3E2.0.CO;2 |
| Hawaii | Nov–Mar core of the Oct–Apr wet season | dry | medium-high | https://doi.org/10.1175/JCLI-D-19-0985.1 |
| SE Alaska / Gulf coast + western Canada | DJF (to Mar) | warm | medium (low for interior/western Alaska) | https://doi.org/10.1002/joc.590 |
| NW Caribbean / Cuba (+ Yucatán, Honduras Caribbean coast) | DJF | wet | medium | https://doi.org/10.1175/1520-0442(2000)013%3C0297:IVOCRE%3E2.0.CO;2 |
| Southern Central America (Costa Rica) + N South America | DJF | dry | medium-high | https://doi.org/10.1175/1520-0442(2000)013%3C0297:IVOCRE%3E2.0.CO;2 |
| Central America Pacific slope (Dry Corridor) | Jul–Aug of the developing year (i.e. 2026, already past) | dry | medium-high (not for DJF 2026-27) | https://doi.org/10.5194/adgeo-42-35-2016 |
| Caribbean, strongest over Greater Antilles | mid-Apr–Jul 2027 (El Niño+1) | wet | medium-high | https://doi.org/10.1002/joc.711 |

---

## A. Northern South America (Colombia, Venezuela, Guianas)

**Expected anomaly, season, mechanism.** Dry, most robust in **DJF** (mature phase), weaker in MAM. During mature El Niño, the SLP seesaw between the eastern Pacific and the tropical Atlantic produces divergent low-level flow and subsidence over the southern Caribbean and northern South America (Giannini et al. 2000). Over Colombia this is compounded by a weakened Chocó jet and Walker-cell subsidence (Poveda et al. 2011).

**SON:** I found no verified support for a robust SON dry signal over the Caribbean coast or the Guianas. Giannini et al. (2000) do report drier conditions in the rainy season *preceding* the mature phase basin-wide, which argues for some autumn drying. However, Poveda et al. (2011) put the Colombian peak in DJF, and the 2023 case included heavy Nov–Dec rain in Cesar. **Treat SON as low confidence.**

**Key papers**
1. Poveda, G., Álvarez, D.M. & Rueda, Ó.A. (2011; online 2010). Hydro-climatic variability over the Andes of Colombia associated with ENSO: a review… *Climate Dynamics* 36, 2233–2249. https://doi.org/10.1007/s00382-010-0931-y
   > "During El Nino (La Nina), the region experiences negative (positive) anomalies in rainfall, river discharges (average and extremes), soil moisture, and NDVI. ENSO's effects are phase-locked to the seasonal cycle, being stronger during December-February, and weaker during March-May." **[ABSTRACT-ONLY: https://www.osti.gov/etdeweb/biblio/21472059, raw text checked]**
2. Giannini, A., Kushnir, Y. & Cane, M.A. (2000). Interannual variability of Caribbean rainfall, ENSO, and the Atlantic Ocean. *J. Climate* 13, 297–311. https://doi.org/10.1175/1520-0442(2000)013%3C0297:IVOCRE%3E2.0.CO;2
   > "The dry season that coincides with the mature phase of ENSO is wetter than average over the northwestern section of the basin, that is, Yucatan, the Caribbean coast of Honduras, and Cuba, and drier than average over the rest of the basin, that is, Costa Rica and northern South America." **[ABSTRACT-ONLY via OpenAlex; a research subagent also read the full-text PDF (https://rainbow.ldeo.columbia.edu/papers/interannual.pdf) and reported identical wording]**
   - **Correction:** the Region A subagent's draft misquoted this sentence as "drier… over the northwestern section… Cuba". The actual text says **wetter**. This matters for Region E.
3. Salas, H.D., Builes-Jaramillo, A., Boers, N., Poveda, G., Mesa, Ó.J. & Kurths, J. (2024). Precipitation over northern South America and the far-eastern Pacific during ENSO: Phase synchronization at inter-annual time scales. *Int. J. Climatol.* https://doi.org/10.1002/joc.8443
   > "the Guianas (northeastern Amazon) and the Caribbean constitute two regions with negative (positive) rainfall anomalies during El Niño (La Niña), separated by a zone of non-significant anomalies along the Orinoco Low-level Jet corridor." **[ABSTRACT-ONLY via OpenAlex]**
4. Poveda, G., Jaramillo, A., Gil, M.M., Quiceno, N. & Mantilla, R.I. (2001). Seasonality in ENSO-related precipitation, river discharges, soil moisture, and vegetation index in Colombia. *Water Resour. Res.* 37, 2169–2178. https://doi.org/10.1029/2000WR900395. DOI verified (the Crossref title contains a typo, "Seasonally"). No quote obtained.

**Observed outcomes**
- 1982-83, 1997-98: not independently documented here. They are among the events underlying the composites above.
- 2015-16: IDEAM statements on worsening drought through early 2016, relayed by media (colombiareports.com). **[SECONDARY/UNVERIFIED]**
- 2023-24: ACAPS (24 Jan 2024), citing IDEAM, reported "below-average precipitation resulting from El Niño has affected Colombia's Caribbean and Andean regions" since Aug 2023, with projected Jan–Mar deficits of 10–60%. It also noted Nov–Dec flooding in Cesar. **[SECONDARY/UNVERIFIED: read by subagent, not re-checked]**

**Caveats.** The region is spatially heterogeneous: Salas et al. (2024) find no significant signal along the Orinoco corridor, so interior Venezuela should not be shaded with the same confidence. Salas et al. also state that their anomalies "differ from those previously reported in the literature." The tropical Atlantic modulates the signal: a warm TNA after the ENSO peak favours convection (Giannini et al. 2000), which can shorten the dry anomaly into MAM. Venezuela-specific literature was not found or verified.

**Tier: medium-high** for DJF dry over Colombia's Caribbean/Andean regions and the Guianas. Two independent peer-reviewed analyses plus a basin-scale study agree, and 2023-24 behaved as expected. **Low** for SON, and **medium** for interior Venezuela/Orinoco.

---

## B. Northern Mexico / US Southwest

**Expected anomaly, season, mechanism.** Wet, DJF/JFM. An eastward-extended, strengthened Pacific subtropical jet and a southward-shifted storm track steer more winter storms into the southern tier.

**Key papers**
1. Cayan, D.R., Redmond, K.T. & Riddle, L.G. (1999). ENSO and hydrologic extremes in the western United States. *J. Climate* 12, 2881–2893. https://doi.org/10.1175/1520-0442(1999)012%3C2881:EAHEIT%3E2.0.CO;2
   > "In years with negative SOI values (El Niño), days with high daily precipitation and stream flow are more frequent than average over the Southwest and less frequent over the Northwest." **[ABSTRACT-ONLY via OpenAlex]**
2. Ropelewski, C.F. & Halpert, M.S. (1986). North American precipitation and temperature patterns associated with the El Niño/Southern Oscillation (ENSO). *Mon. Wea. Rev.* 114, 2352–2362. https://doi.org/10.1175/1520-0493(1986)114%3C2352:NAPATP%3E2.0.CO;2
   > "above normal precipitation was associated with ENSO in 18 out of 22 cases (81%) in the 'season' starting with October of the ENSO year to March of the following year for an area of North America that includes parts of the southeastern United States and northern Mexico." **[ABSTRACT-ONLY via OpenAlex]**
   - Note that their coherent region is the Gulf coast plus **northern Mexico**, not the interior US Southwest.
3. Pavia, E.G., Graef, F. & Reyes, J. (2006). PDO–ENSO effects in the climate of Mexico. *J. Climate* 19, 6433–6438. https://doi.org/10.1175/JCLI4045.1
   > "For precipitation, El Niño favors wet conditions during summers of LoPDO and during winters of HiPDO." **[ABSTRACT-ONLY via Crossref]**
4. Gershunov, A. & Barnett, T.P. (1998). Interdecadal modulation of ENSO teleconnections. *BAMS* 79, 2715–2725. https://doi.org/10.1175/1520-0477(1998)079%3C2715:IMOET%3E2.0.CO;2
   > "Typical El Niño patterns (e.g., low pressure over the northeastern Pacific, dry northwest, and wet southwest, etc.) are strong and consistent only during the high phase of the NPO, which is associated with an anomalously cold northwestern Pacific." **[ABSTRACT-ONLY via OpenAlex]**
   - Their "NPO" index is effectively PDO-like.

**Supporting papers on the 2015-16 failure**
- Siler, N., Kosaka, Y., Xie, S.-P. & Li, X. (2017). Tropical Ocean contributions to California's surprisingly dry El Niño of 2015/16. *J. Climate*. https://doi.org/10.1175/JCLI-D-17-0177.1
  > "these ensemble-mean differences were likely related to a pattern of tropical SST variability with a strong signal in the Indian Ocean and western Pacific and a weaker signal in the eastern equatorial Pacific" **[ABSTRACT-ONLY via Crossref]**
- Cash, B.A. & Burls, N.J. (2019). Predictable and unpredictable aspects of U.S. West Coast rainfall and El Niño: understanding the 2015/16 event. *J. Climate*. https://doi.org/10.1175/JCLI-D-18-0181.1
  > "while there is a statistically significant positive correlation between El Niño events and the SOCAL and PNW rainfall anomalies, this relationship explains at most one-third of the observed variance." **[ABSTRACT-ONLY via Crossref]**
- Yu, J.-Y. & Zou, Y. (2013). The enhanced drying effect of Central-Pacific El Niño on US winter. *ERL* 8, 014019. https://doi.org/10.1088/1748-9326/8/1/014019
  > "the Central-Pacific El Niño enhances the drying effect, but weakens the wetting effect, typically produced by traditional Eastern-Pacific El Niño events on the US winter precipitation." **[ABSTRACT-ONLY via OpenAlex]**
  - This paper's drying emphasis is on the Ohio–Mississippi Valley, PNW and Southeast, not specifically the Southwest.

**Observed outcomes (computed; NCEI statewide DJF precipitation, % of the 1991–2020 mean)**

| Winter | Arizona | New Mexico | California |
|---|---|---|---|
| 1982-83 | 147% | 168% | 147% |
| 1997-98 | 157% | 133% | 179% |
| 2015-16 | **66%** | 88% | 103% |
| 2023-24 | 115% | 120% | 121% |

- Hit rates for DJF above the 1950–2025 median across the 10 El Niño winters: AZ 8/10, NM 9/10, CA 7/10. For the 7 strong winters: AZ 5/7, NM 6/7, CA 6/7.
- 2023-24 was wet despite a DJF PDO of −1.52, so the PDO dependence that Gershunov & Barnett and Pavia et al. describe is not obvious in this small US sample.
- Northern Mexico was **not computed**, and no Mexican agency outcome reports were retrieved.

**Caveats.** 2015-16 is a documented failure over southern California and Arizona. Siler et al. tie it partly to Indian Ocean and western Pacific SSTs. Whether a +IOD in 2026 is analogous is **my speculation, not an established finding**. ENSO explains ≤ ~1/3 of West Coast winter rainfall variance (Cash & Burls). Atmospheric-river luck matters. For Mexico, the only verified PDO-conditioned study says winter wetness is favoured under a *high* PDO.

**Tier: medium-high.** The mechanism is well established and the observed hit rate is about 80%. Not "high" because of the 2015-16 failure, the modest variance explained, and thin verified evidence for northern Mexico specifically under a negative PDO.

---

## C. Hawaii

**Expected anomaly, season, mechanism.** Dry during the wet season, core Nov/Dec–Mar. In East-Pacific El Niño winters, an enhanced local Hadley cell and an eastward-extended subtropical jet produce subsidence, moisture-flux divergence and weaker trades near Hawaii.

**Key papers**
1. Lu, B.-Y., Chu, P.-S., Kim, S.-H. & Karamperidou, C. (2020). Hawaiian regional climate variability during two types of El Niño. *J. Climate* 33, 9929–. https://doi.org/10.1175/JCLI-D-19-0985.1
   > "As a result of this robust signal, dry conditions prevail in Hawaii and the standard deviation of rainfall during EP winters is smaller than the climatology… Without strong external forcing, rainfall in the Hawaiian Islands during CP winters is close to the long-term mean." **[ABSTRACT-ONLY via OpenAlex; the subagent also read it on the AMS page]**
2. Chu, P.-S. (1989). Hawaiian drought and the Southern Oscillation. *Int. J. Climatol.* 9, 619–631. https://doi.org/10.1002/joc.3370090606. DOI verified. No quote: the paper is paywalled. Its findings are known here only via Lu et al.'s introduction ("During an El Niño winter and the following spring, droughts tend to occur more often in the Hawaiian Islands (Chu 1989, 1995; Chu and Chen 2005)"). **[SECONDARY/UNVERIFIED: read by subagent]**
3. Frazier, A.G., Elison Timm, O., Giambelluca, T.W. & Diaz, H.F. (2018; online 2017). The influence of ENSO, PDO and PNA on secular rainfall variations in Hawai'i. *Clim. Dyn.* 51, 2127–2140. https://doi.org/10.1007/s00382-017-4003-4
   > "PNA is the dominant mode of wet season (November–April) variability, while ENSO is most significant in the dry season (May–October)." **[VERIFIED-PRIMARY: https://www.fs.usda.gov/psw/publications/frazier/psw_2018_frazier001.pdf, text extracted from the PDF myself]**
4. Elison Timm, O. et al. (2011). *JGR* https://doi.org/10.1029/2010JD014923. DOI verified. No quote obtained; supporting only.

**Observed outcomes**
- 2015-16: the NWS Honolulu Jan 2016 newsletter *forecast* "significant below average rainfall this winter through April 2016," tied to El Niño. **[SECONDARY/UNVERIFIED: read by subagent]** This is a forecast, not a verified outcome. I did **not** confirm observed 2015-16 wet-season totals.
- 2023-24: news reports of drought were coincident with El Niño (Governing.com). **[SECONDARY/UNVERIFIED]**
- 1982-83, 1997-98: commonly cited as drought winters in the literature, but not verified here.
- Hawaii rainfall was not computed (NCEI Climate at a Glance has no Hawaii series).

**Caveats.**
- The signal depends on event flavour: it is robust for EP events and near zero with large spread for CP events (Lu et al. 2020). The current event is described as EP-leaning, which helps.
- Frazier et al. find the leading wet-season mode tracks the PNA more than ENSO. The PNA and ENSO are correlated, so this is not a contradiction, but it means non-ENSO PNA variability can override the signal.
- Chu's reported asymmetry (El Niño reliably dry, La Niña not reliably wet) does not affect this case.

**Tier: medium-high.** The mechanism is specific to EP events and verified, and it matches the current event's flavour. Downgraded from high because event outcomes were not verified here and wet-season variance is PNA-dominated.

---

## D. Alaska / western Canada

**Expected anomaly, season, mechanism.** Warm DJF–Mar via the PNA response to tropical heating. A deeper, east-shifted Aleutian Low with a downstream ridge advects maritime air into southern Alaska and British Columbia.

**Key papers**
1. Papineau, J.M. (2001). Wintertime temperature anomalies in Alaska correlated with ENSO and PDO. *Int. J. Climatol.* 21, 1577–1592. https://doi.org/10.1002/joc.686
   > "During El Niño winters, temperatures are near normal in western Alaska but significantly warmer than normal for the eastern two‐thirds of the state… Temperature patterns produced during El Niño, La Niña, and neutral winters are modified by the concurrent state of the North Pacific sea‐surface temperature anomalies, as indicated by the Pacific Decadal Oscillation index." **[ABSTRACT-ONLY via Crossref]**
2. Bonsal, B.R., Shabbar, A. & Higuchi, K. (2001). Impacts of low frequency variability modes on Canadian winter temperature. *Int. J. Climatol.* 21, 95–108. https://doi.org/10.1002/joc.590
   > "Impacts are stronger and more spatially coherent during El Niño episodes when positive PDO winters are associated with strong positive temperature anomalies over most of Canada, neutral PDO with weaker anomalies (positive in the west and negative in the east), and negative PDO with strong negative anomalies over western Canada." **[ABSTRACT-ONLY via Crossref]**
3. Ropelewski & Halpert (1986), DOI above.
   > "Areas of Alaska and western Canada experienced positive temperature anomalies in 17 out of 21 ENSO episodes (81%) during the 'season' defined by December of the ENSO year through the following March." **[ABSTRACT-ONLY via OpenAlex]**
4. Wallace, J.M. & Gutzler, D.S. (1981). Teleconnections in the geopotential height field during the Northern Hemisphere winter. *Mon. Wea. Rev.* 109, 784–812. https://doi.org/10.1175/1520-0493(1981)109%3C0784:TITGHF%3E2.0.CO;2. This paper defines the PNA pattern but does not analyse ENSO. A subagent read the PDF. **[SECONDARY/UNVERIFIED for quote]**
5. Also verified: Rodionov, Overland & Bond (2005), *J. Climate*, https://doi.org/10.1175/JCLI3253.1. For the Bering Sea, the Aleutian Low's *position* matters more than its depth. **[ABSTRACT-ONLY]**

**Observed outcomes (computed; NCEI DJF Tavg, °C)**
- **Alaska statewide, vs 1991–2020:** 1982-83 −0.6, 1997-98 −0.9, 2015-16 +4.3 (2nd warmest; matches USGS "second warmest on record"), 2023-24 +0.1.
- **Alaska statewide, detrended 1950–2025:** the strong-El-Niño composite is only +0.2 °C, with 3/7 winters positive.
- **By climate division (detrended, 7 strong winters):**
  - NE Gulf and the three Panhandle divisions: +1.0 to +1.5 °C, 5–6 of 7 positive. Robust.
  - North Slope, West Coast, Bristol Bay and Aleutians: no signal (−0.5 to −0.2 °C).
  - Interior: weak (+0.2 to +0.4 °C).
  - This is consistent with Papineau's east–west contrast and puts the robust signal in **SE Alaska/Gulf coast**.
- **SE Alaska split by DJF PDO (10 El Niño winters):**
  - PDO ≥ 0: warm in all 6 (+1.8 to +3.1 °C).
  - PDO < 0: 1965-66 −1.5, 1972-73 −1.4, 2009-10 +0.9 (PDO ≈ −0.1), 2023-24 +0.1 (PDO −1.5).
  - n is small, but the split agrees with Bonsal et al.
- 2015-16 is confounded by the North Pacific marine heatwave. USGS: "El Niño was at most a modest contributor." **[VERIFIED-PRIMARY: https://www.usgs.gov/programs/climate-adaptation-science-centers/regional-super-el-nino-impacts-alaska, quote confirmed via fetch]**
- Western Canada outcomes were **not computed**. The Canada-wide 2023-24 winter should be checked against ECCC's Climate Trends and Variations Bulletin before citing.

**Caveats.** The PNA is also internally generated. **The PDO is currently about −1.8, and the literature (Bonsal; Papineau) plus this composite say El Niño warmth over western Canada and SE Alaska weakens or reverses under a negative PDO.** A record El Niño may push the PDO up by winter through the atmospheric bridge, but that is not guaranteed: in 2023-24 it stayed strongly negative. Statewide Alaska shows no robust El Niño warmth after detrending.

**Tier: medium** for SE Alaska/Gulf coast + BC. **Low** for interior, western and northern Alaska. If you keep this region, restrict the footprint to the Gulf of Alaska coast/Panhandle and BC/Yukon, and consider a "weaker if PDO stays negative" qualifier. This is the region where I would lean most on whether the dynamical models actually show it.

---

## E. Caribbean & Central America: reshaping the current "drought, Dec–Feb & summer 2027" region

**Bottom line.** The reviewer is essentially right, and the literature supports **three** changes:
1. DJF 2026-27 is **wet in the NW Caribbean** (Cuba, Yucatán, the Caribbean coast of Honduras) and **dry in the south** (Costa Rica, northern South America).
2. The documented Central America Dry Corridor drought signal is a **Jul–Aug midsummer-drought signal in the developing year**, i.e. summer 2026, which is already past. DJF is the climatological dry season on the Pacific slope anyway, so a DJF "drought" label there says little.
3. **Summer 2027 should not be labelled drought for the Caribbean.** The verified literature points to a **wet early rainy season (mid-Apr–Jul) in the El Niño+1 year**, strongest over the Greater Antilles.

**Key papers**
1. **Giannini, Kushnir & Cane (2000)**, *J. Climate* 13, 297–311. https://doi.org/10.1175/1520-0442(2000)013%3C0297:IVOCRE%3E2.0.CO;2 **[ABSTRACT-ONLY via OpenAlex; full text read by subagent with identical wording]** This single abstract covers the full seasonal sequence:
   > "The tendency is for drier-than-average conditions when the divergent atmospheric flow dominates, during the rainy season preceding the mature phase of a warm ENSO event. The dry season that coincides with the mature phase of ENSO is wetter than average over the northwestern section of the basin, that is, Yucatan, the Caribbean coast of Honduras, and Cuba, and drier than average over the rest of the basin, that is, Costa Rica and northern South America. The following spring… The positive precipitation anomaly spreads southeastward, from the northwest to the entire basin. At the start of a new rainy season, it is especially strong over the Greater Antilles."
2. **Chen, A.A. & Taylor, M.A. (2002).** Investigating the link between early season Caribbean rainfall and the El Niño + 1 year. *Int. J. Climatol.* 22, 87–106. https://doi.org/10.1002/joc.711
   > "Whereas traditionally ENSO events have been identified with dry conditions during the later Caribbean rainfall season, recent research suggests a second signal that manifests itself as a wet early rainfall season of the year of ENSO decline (the El Niño + 1 year)… Strong correlations are shown to exist between the first mode and wintertime equatorial Pacific anomalies." **[ABSTRACT-ONLY via Crossref]**
   - Their early season is defined as **mid-April to July**. The proposed mechanism is warm spring north tropical Atlantic SSTs.
   - **Chen & Taylor do not make the DJF spatial-split claim.** Cite them only for the wet early rainy season in 2027. The subagent's draft had spliced a Giannini sentence into this quote; that has been removed.
3. **Jury, M., Malmgren, B.A. & Winter, A. (2007).** Subregional precipitation climate of the Caribbean and relationships with ENSO and NAO. *JGR* 112, D16107. https://doi.org/10.1029/2006JD007541
   > "The ENSO relationship, represented by Niño 3.4 sea surface temperatures (SST), is positive and stable at all lags, but tends to reverse over the SE Caribbean (C4) in late summer… Early summer rainfall in the northwest Caribbean (C1) increases under El Niño conditions." **[ABSTRACT-ONLY via Crossref]**
   - Their C1 region is western Cuba plus the NW Bahamas. The analysis uses 35 island stations over 1951–1981.
4. **Maldonado, T., Rutgersson, A., Alfaro, E., Amador, J. & Claremar, B. (2016).** Interannual variability of the midsummer drought in Central America and the connection with sea surface temperatures. *Adv. Geosci.* 42, 35–50. https://doi.org/10.5194/adgeo-42-35-2016
   > "It is shown that the MSD extends along the Pacific coast… The MSD intensity and magnitude show a negative relationship with Niño 3.4 and a positive relationship with the Caribbean low-level jet (CLLJ) index, however for the Caribbean stations the results were not statistically significant" **[ABSTRACT-ONLY via Crossref]**
   - "Intensity" is defined as the minimum rainfall during the MSD, so the negative relationship means a drier MSD under El Niño.
5. Supporting: **Anderson, K. et al. (2023).** How exceptional was the 2015–2019 Central American drought? *GRL*. https://doi.org/10.1029/2023GL105391
   > "the severity of this drought was driven primarily by rainfall deficits in July–August." **[ABSTRACT-ONLY via Crossref]**
   - The abstract does **not** attribute the drought to El Niño; it links it to a stronger CLLJ. Use it for seasonality only.
   - Hidalgo et al. (2019), *Clim. Dyn.*, https://doi.org/10.1007/s00382-019-04638-y: title verified, content not read.

**Observed outcomes**
- 2015 Dry Corridor drought and food insecurity: widely reported, with UN figures relayed by Reuters and Scientific American. **[SECONDARY/UNVERIFIED]** Pull an FAO/WFP/FEWS NET primary report before citing numbers.
- No NOAA CPC or INSMET (Cuba) confirmation of wet DJF in the Antilles for 1982-83, 1997-98, 2015-16 or 2023-24 was retrieved. **This is a gap.** The wet-DJF claim rests on the climatological papers above.

**Recommended reshaping**
1. **NW Caribbean (Cuba, Bahamas, Yucatán, Caribbean coast of Honduras): "wetter, Dec–Feb."** Tier **medium**. Giannini and Jury agree, but Jamaica, Hispaniola and Puerto Rico are less clearly covered in DJF, and no case-year verification was obtained.
2. **Southern Central America (Costa Rica, Panama) + Caribbean coast of Colombia/Venezuela: "drier, Dec–Feb."** Tier **medium-high**. This merges naturally with Region A.
3. **Caribbean basin, strongest over the Greater Antilles: "wetter early rainy season, Apr–Jul 2027."** Tier **medium-high**. Two independent verified papers plus a physically clear TNA-warming mechanism support it. It is not "high" because of the record-warm Atlantic background and the lack of case-year verification.
4. **Drop "summer 2027 drought."** The Dry Corridor Jul–Aug signal belongs to summer 2026, the developing year (medium-high). No verified literature was found on Central America Pacific-slope rainfall in El Niño+1 summers, so leave it unshaded.

**Where the subagent tiers were revised down.** The subagent rated the May–Jul wet signal "high" and the midsummer drought "high". I lowered both to medium-high: the Anderson et al. paper does not tie the drought to ENSO, the Maldonado signal is correlational over a limited station set, and no case years were verified.
