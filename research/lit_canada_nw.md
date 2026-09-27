# El Niño 2026–27 map: literature check for Canada / interior Northwest regions

Prepared 2026-09-23. Scope: two candidate map regions.
- **A.** Interior BC, northern Rockies & inland Northwest: dry, low snowpack, DJF.
- **B.** Central & eastern Canada: warm, DJF.

**How things were verified**
- Every DOI below was resolved through the Crossref API (`https://api.crossref.org/works/<DOI>`), and the returned title, authors, container and year were checked against the citation before it was used. Where full text was not reachable, I supplemented with the OpenAlex `abstract_inverted_index` (reconstructed) or the Crossref-deposited JATS abstract, both checked against the same DOI.
- Quote tags:
  - **[VERIFIED-PRIMARY: URL]**: read verbatim from the publisher/agency page.
  - **[ABSTRACT-ONLY: source]**: verbatim abstract text from Crossref or OpenAlex. Full text not read (most of the AMS/Taylor & Francis/ASCE papers below returned HTTP 403 to automated fetch; Unpaywall confirms no free full text exists for the WRR and ASCE papers).
  - **[SECONDARY/UNVERIFIED]**: paraphrase or a claim I could not check against a primary source.
- **Process caveat, stated plainly:** this session's web-search tool was already exhausted (shared budget across this project) before I started, so I could not run open-ended searches for agency snowpack/climate bulletins. I relied on the Crossref/OpenAlex/Unpaywall/Semantic Scholar APIs (which work over plain HTTP and are not "web search") for literature, and on direct URL guesses for agency bulletins, which succeeded for the ECCC winter 2023-24 bulletin but failed for 1997-98, 2015-16 and BC River Forecast Centre pages (404s). **Observed-event evidence below is thinner than the literature evidence, and that gap is real, not papered over.**
- I reused three citations already verified earlier in this project (`research/lit_missing_americas.md`): Bonsal, Shabbar & Higuchi (2001), Ropelewski & Halpert (1986), Cayan, Redmond & Riddle (1999), Gershunov & Barnett (1998). I re-ran the Crossref check on all four myself in this session rather than trusting the earlier file's tags.

---

## Summary table

| Region | Season | Sign | Tier | Key DOI |
|---|---|---|---|---|
| A. Interior BC / northern Rockies / inland NW | DJF | dry, low snowpack | **medium** | https://doi.org/10.1175/1520-0442(1997)010%3C3016:CPPAWT%3E2.0.CO;2 |
| B. Central Canada (west of Hudson Bay) core; weaker, NAO-conditional extension into Ontario/Quebec | DJF | warm | **medium** (medium-high for a "central Canada" footprint; medium-low if the label is stretched to mean "eastern Canada is the strongest region") | https://doi.org/10.1002/joc.590 |

**Headline finding that should change the map:** the literature does **not** consistently place the strongest El Niño warm anomaly in "central and eastern Canada." It places it in **western-to-central** Canada, with a documented anomaly center **just west of Hudson Bay** (i.e., northern Manitoba/Ontario border), and treats the further eastward extension into Ontario/Quebec/Labrador as real but **secondary and NAO-dependent**, not independently ENSO-driven. See Region B below — this is a "check the placement" flag, not a simple confirm/deny.

---

## A. Interior BC, northern Rockies & inland Northwest: dry, low snowpack, DJF

**Expected anomaly, season, mechanism (as stated in the task).** Dry DJF, driven by a northward/eastward-shifted, intensified subtropical jet and storm track that favours the US Southwest and leaves the interior Northwest and southern-interior BC under a drier, more zonal or ridged flow, while the immediate Pacific coast (Oregon/Washington, southern BC coast) stays wetter.

### Key papers

1. **Shabbar, A., Bonsal, B. & Khandekar, M. (1997).** Canadian Precipitation Patterns Associated with the Southern Oscillation. *J. Climate* 10, 3016–3027. https://doi.org/10.1175/1520-0442(1997)010%3C3016:CPPAWT%3E2.0.CO;2
   DOI confirmed via Crossref: title, authors (Shabbar, Bonsal, Khandekar) and *J. Climate* 1997 all match.
   > "Composite and correlation analyses indicate that precipitation over a large region of southern Canada extending from British Columbia, through the prairies, and into the Great Lakes region is significantly influenced by the SO phenomenon. The results show a distinct pattern of negative (positive) precipitation anomalies in this region during the first winter following the onset of El Niño (La Niña) events." **[ABSTRACT-ONLY: OpenAlex, reconstructed from `abstract_inverted_index`]**
   - This is the single best piece of direct support for a DJF dry signal spanning BC and Alberta/the Prairies. It does **not**, however, distinguish coast from interior within BC, or north from south — that granularity comes from the papers below.

2. **Clark, M.P., Serreze, M.C. & McCabe, G.J. (2001).** Historical effects of El Niño and La Niña events on the seasonal evolution of the montane snowpack in the Columbia and Colorado River Basins. *Water Resour. Res.* 37, 741–757. https://doi.org/10.1029/2000WR900305
   DOI confirmed via Crossref: title, authors, *WRR* 2001 all match.
   > "In the Columbia River Basin, there is a general tendency for decreased SWE during El Nino years and increased SWE in La Nina years. However, the SWE anomalies for El Nino years are much less pronounced. This occurs in part because midlatitude circulation anomalies in El Nino years are located 35° east of those in La Nina years. This eastward shift is most evident in midwinter, at which time, SWE anomalies associated with El Nino are actually positive in coastal regions of the Columbia River Basin." **[ABSTRACT-ONLY: Crossref-deposited JATS abstract; full text is paywalled (Unpaywall reports no OA copy exists)]**
   - This is the key **coast-vs-interior** paper for the proposed region. It directly supports "dry interior, not the coast" for DJF/midwinter specifically, and it directly supports the "dry" side of Region A. But it also flags that the El Niño *dry* signal is weaker and noisier than the La Niña *wet* signal — a real reason not to go above "medium" confidence.

3. **Fleming, S.W. & Whitfield, P.H. (2010).** Spatiotemporal mapping of ENSO and PDO surface meteorological signals in British Columbia, Yukon, and southeast Alaska. *Atmosphere-Ocean* 48, 122–131. https://doi.org/10.3137/ao1107.2010
   DOI confirmed via Crossref: title, authors (Fleming, Whitfield), *Atmosphere-Ocean* 2010 all match.
   > "temperature responses were relatively uniform, with higher (lower) temperatures during the warm (cool) phases of these circulation patterns... Overall spatiotemporal patterns in precipitation response were decoupled from those in temperature and were far more heterogeneous. Complexities in precipitation signals included north-south inverse teleconnectivity along the Pacific coast, with a zero-response hinge point in the approximate vicinity of northern Vancouver Island." **[ABSTRACT-ONLY: OpenAlex, reconstructed]**
   - **Caveat this raises for the map**: the coastal BC precipitation signal is not a simple uniform "wet," it is a **north-south dipole hinged near northern Vancouver Island**. That is a finer-grained coastal complexity than "OR/WA coast wet" captures, though it is consistent with treating the immediate south coast differently from the interior. I could not get full text (Tandfonline returned 403, and Semantic Scholar/Unpaywall list no other OA copy), so I don't have their explicit interior-BC number.

4. **Hamlet, A.F. & Lettenmaier, D.P. (1999).** Columbia River Streamflow Forecasting Based on ENSO and PDO Climate Signals. *J. Water Resour. Plann. Manage.* 125, 333–341. https://doi.org/10.1061/(ASCE)0733-9496(1999)125:6(333)
   DOI confirmed via Crossref: title, authors, journal and year all match.
   > "A streamflow forecast ensemble is created by resampling from the historical meteorological data according to six predefined PDO/ENSO categories." **[ABSTRACT-ONLY: Semantic Scholar/Crossref; full text closed, no OA location per Unpaywall]**
   - This is a methods paper, not a spatial-pattern paper. It is useful for the "effect on streamflow/hydropower" part of the task: it establishes that Columbia River hydropower planning treats El Niño+PDO phase as an operationally meaningful joint category, i.e., the agencies that run the system believe (and act on) this signal. It does not by itself give a magnitude or a coast/interior split, and it is silent on the current negative-PDO/El-Niño combination's expected direction beyond "one of six categories."

5. **Mote, P.W. (2006).** Climate-Driven Variability and Trends in Mountain Snowpack in Western North America. *J. Climate* 19, 6209–6220. https://doi.org/10.1175/JCLI3971.1
   DOI confirmed via Crossref: title, author (Mote), *J. Climate* 2006 all match.
   > "These results emphasize the sensitivity to warming of the mountains of northern California and the Cascades of Oregon and Washington. In addition, the contribution of modes of Pacific climate variability is examined and found to be responsible for about 10%–60% of the trends in SWE, depending on the period of record and climate index." **[ABSTRACT-ONLY: Crossref-deposited JATS abstract]**
   - **This paper is weaker support than it looks and I want to flag that clearly.** It is a long-term *trend*-attribution paper (SWE decline 1950s–2000s), not a single-winter ENSO composite study, so it doesn't directly quantify a DJF 2026-27 El Niño snowpack anomaly. Its one genuinely load-bearing point for this map is a **caveat, not a confirmation**: the Cascades and northern California mountains are unusually *temperature*-sensitive (they sit near 0 °C much of the winter), so even where NMME/C3S show the OR/WA coast/Cascades as wet in precipitation, a warm DJF there (which is the typical El Niño temperature response) could still suppress SWE via more rain-not-snow. I did not find a paper in this search that quantifies this specifically for El Niño winters — it is my inference from Mote's general finding, and I am flagging it as such, not as a verified result.

### Does a negative PDO weaken the dry signal? (directly asked in the task)

I did not find a Canada/BC-specific paper that tests this. The closest verified evidence is from the adjacent US Southwest/Northwest literature already checked in `lit_missing_americas.md` (re-verified here):

- **Gershunov, A. & Barnett, T.P. (1998).** Interdecadal Modulation of ENSO Teleconnections. *BAMS* 79, 2715–2725. https://doi.org/10.1175/1520-0477(1998)079%3C2715:IMOET%3E2.0.CO;2. DOI confirmed via Crossref.
  > "Typical El Niño patterns (e.g., low pressure over the northeastern Pacific, dry northwest, and wet southwest, etc.) are strong and consistent only during the high phase of the NPO, which is associated with an anomalously cold northwestern Pacific." **[ABSTRACT-ONLY: OpenAlex]**
  - Their "high NPO" phase is the PDO-*cold* phase — i.e., **the same phase we are in now**. Read literally this says the classic dry-Northwest pattern should be *more* consistent under a cold/negative PDO, not less. That is the **opposite** of the direction the Bonsal et al. (2001) temperature paper implies for Region B (see below), and it is a genuine, unresolved tension I am flagging rather than smoothing over: PDO modulation of the *precipitation* dipole and PDO modulation of the *temperature* pattern do not obviously point the same way in the papers I could check.
- **Cayan, D.R., Redmond, K.T. & Riddle, L.G. (1999).** ENSO and Hydrologic Extremes in the Western United States. *J. Climate* 12, 2881–2893. https://doi.org/10.1175/1520-0442(1999)012%3C2881:EAHEIT%3E2.0.CO;2. DOI confirmed via Crossref.
  > "In years with negative SOI values (El Niño), days with high daily precipitation and stream flow are more frequent than average over the Southwest and less frequent over the Northwest." **[ABSTRACT-ONLY: OpenAlex]**
  - Supports a Northwest-wide (not BC-specific) dry/low-streamflow signal, without a PDO breakdown.

**Also checked and found to complicate, not support, the region:** Ropelewski & Halpert (1986), DOI https://doi.org/10.1175/1520-0493(1986)114%3C2352:NAPATP%3E2.0.CO;2 (confirmed via Crossref), the foundational hemispheric ENSO composite study, states explicitly:
> "No high latitude precipitation signals were indicated by this analysis." **[ABSTRACT-ONLY: OpenAlex]**
This is the classic, most-cited paper in this literature, and it found **no** coherent high-latitude (i.e., BC/interior-Canada-latitude) precipitation signal by their coherence criterion. That does not overturn the more targeted, more recent studies above (Shabbar/Bonsal/Khandekar 1997; Clark/Serreze/McCabe 2001), but it means the "dry interior BC/Rockies" signal is not universally recovered across methods, and a reader who goes to the most classic paper in the field will not find it there. Worth a footnote if the map cites primary literature.

### Observed strong-event outcomes (1982-83, 1997-98, 2015-16, 2023-24)

I could not verify these independently for BC/interior NW this session — every direct URL guess at the BC River Forecast Centre and at NOAA/NWS PNW snowpack summaries returned 404 or non-substantive pages, and the web-search tool needed to locate the right archived bulletins was unavailable (budget exhausted). This is a real gap, not a "no signal" finding. **[flagged as unverified; do not cite specific winter outcomes for this region without further work]**

### Tier and recommendation

**Tier: medium.** Two solid, independently verified sources (Shabbar/Bonsal/Khandekar 1997 for the BC-through-Great Lakes DJF dry swath; Clark/Serreze/McCabe 2001 for the coast/interior contrast within the Columbia Basin specifically) support the mechanism and the coast-vs-interior spatial logic the map proposes. Downgraded from "medium-high" because: (a) the foundational Ropelewski & Halpert (1986) composite does not recover a high-latitude precipitation signal at all; (b) Clark et al. themselves say the El Niño dry anomaly is "much less pronounced" than the La Niña wet one; (c) Fleming & Whitfield (2010) show the coastal precipitation signal is a north-south dipole, not simply "wet," which complicates the map's coast/interior boundary; (d) I could not verify any of the four named strong events against observations this session, so there is no "it verified/didn't verify" check to report — flag this explicitly on the map or in a footnote. **A "signal not verified against recent strong events" flag is warranted** — not because it failed, but because I could not check it.

---

## B. Central & eastern Canada: warm, DJF

**Expected anomaly, season, mechanism (as stated in the task).** Warm DJF winter temperatures over Hudson Bay, northern and southern Ontario, and Quebec, described as robust even after detrending, with western-Canada warmth described as weaker once the trend is removed.

### Key papers

1. **Shabbar, A. & Khandekar, M. (1996).** The impact of El Niño-Southern Oscillation on the temperature field over Canada: Research Note. *Atmosphere-Ocean* 34, 401–416. https://doi.org/10.1080/07055900.1996.9649570
   DOI confirmed via Crossref: title, authors (Shabbar, Khandekar), *Atmosphere-Ocean* 1996 all match.
   > "Using a composite analysis, the present study conclusively demonstrates that significant positive surface temperature anomalies spread eastward from the west coast of Canada to the Labrador coast from the late fall to early spring (November through May) following the onset of El Niño episodes... while western Canadian surface temperatures are influenced during both phases of ENSO, eastern Canadian surface temperature effects are found during the El Niño phase only... The largest positive (negative) anomalies are found to be centred over two separate regions, one over the Yukon and the other just west of Hudson Bay in the El Niño (La Niña) years." **[ABSTRACT-ONLY: OpenAlex, reconstructed]**
   - **This is the single most important paper for Region B, and it is genuinely supportive but not exactly of the label as written.** It documents a real, specifically El-Niño-only (not La Niña) warm signal that spreads east to Labrador. But its **strongest anomaly centers** are the **Yukon (west)** and the area **just west of Hudson Bay** — i.e., northern Manitoba/the Manitoba–Ontario–Nunavut border area — which is "central Canada," not classically "eastern Canada" (Quebec/Maritimes). The eastward spread to Labrador is described but not identified as a second peak.

2. **Bonsal, B.R., Shabbar, A. & Higuchi, K. (2001).** Impacts of low frequency variability modes on Canadian winter temperature. *Int. J. Climatol.* 21, 95–108. https://doi.org/10.1002/joc.590
   DOI confirmed via Crossref: title, authors, *IJC* 2001 all match. (Full abstract re-read in this session, not just the earlier file's excerpt.)
   > "Results show the NAO as the dominant low frequency variability mode affecting winter temperature, however, the effects are mainly confined to north-eastern regions of the country. **The ENSO and PDO influences are somewhat weaker and occur over western and central Canada.**... Over eastern regions of Canada, El Niño (La Niña) events modulate the typical positive (negative) NAO temperature responses by generally making them warmer (colder)." **[ABSTRACT-ONLY: Crossref-deposited JATS abstract]**
   - **This is the clearest statement in the literature I could check, and it argues against putting the primary warm shading in "central and eastern Canada" as a single undifferentiated region.** ENSO's own (PDO-independent) footprint is western-and-central Canada. Eastern Canada's temperature is dominated by the NAO; ENSO only modulates (amplifies or dampens) whatever the NAO is already doing there. If the NAO happens to be positive this winter, El Niño would indeed add extra warmth over Ontario/Quebec/Labrador — but that is a **conditional, NAO-dependent** effect, not an independent, robust ENSO signal of the kind claimed for the model composites. **This is a real and specific place where the literature does not simply confirm the proposed region as labeled** — it supports a "central Canada, west of Hudson Bay" core with a weaker, conditional eastern extension, not "central and eastern Canada" as two co-equal robust zones.

3. **Ropelewski, C.F. & Halpert, M.S. (1986).** North American Precipitation and Temperature Patterns Associated with the El Niño/Southern Oscillation (ENSO). *Mon. Wea. Rev.* 114, 2352–2362. https://doi.org/10.1175/1520-0493(1986)114%3C2352:NAPATP%3E2.0.CO;2. DOI confirmed via Crossref (re-checked this session).
   > "Areas of Alaska and western Canada experienced positive temperature anomalies in 17 out of 21 ENSO episodes (81%) during the 'season' defined by December of the ENSO year through the following March." **[ABSTRACT-ONLY: OpenAlex, reconstructed]**
   - This, the most classic and most widely cited paper in the field, identifies the coherent, high-confidence ENSO warm region as **Alaska and western Canada** — full stop. It does not identify central or eastern Canada as a coherent ENSO-temperature region at all. Combined with Bonsal et al. (2001), the balance of the peer-reviewed literature leans toward "western/central" as the historically robust core, with "eastern" as a secondary, NAO-gated effect — the opposite emphasis from what the map's Region B label implies.

### Observed strong-event outcomes

- **2023-24 (ONI classified as a strong/near-record El Niño winter): [VERIFIED-PRIMARY]** ECCC, *Climate Trends and Variations Bulletin — Winter 2023/2024*: https://www.canada.ca/en/environment-climate-change/services/climate-change/science-research-data/climate-trends-variability/trends-variations/winter-2024-bulletin.html
  > "the warmest winter [on] nationwide record since 1948[,] and 1.1°C higher than the previous warmest winter[, which] occurred in 2009/2010." The bulletin further reports temperature departures of "at least 6.5°C" above baseline over "northern Ontario, central Manitoba... and the southern border between Ontario and Manitoba," with the Great Lakes/St. Lawrence and Northeastern Forest regions also setting records, while the Prairies ranked only "5th warmest" and British Columbia's anomaly was a comparatively modest 1.5–2.8°C above baseline. **The bulletin does not mention El Niño anywhere as a driver.**
  - Read plainly, this observed event is a **good match to the "west of Hudson Bay + extension into Ontario/Quebec" pattern** the literature describes (strongest anomaly on the Manitoba/Ontario border, record warmth also reaching the Great Lakes/St. Lawrence corridor and the Northeast, weaker signal on the Prairies and in BC — consistent with Bonsal et al.'s "PDO negative → weaker/negative anomalies over western Canada" and with the Shabbar/Khandekar "west of Hudson Bay" center extending east). **But this cannot be cleanly credited to El Niño**: it is also, and possibly primarily, the warmest winter on record amid the long-term warming trend, and the agency's own bulletin does not attribute it to El Niño. Treat this as consistent-with, not proof-of, the ENSO mechanism. I could not find a detrended, ENSO-composite equivalent for Canada (analogous to the Alaska divisional analysis already done for Region D in `lit_missing_americas.md`) — that would be the right next step before trusting this event as confirmation.
- **1997-98 and 2015-16:** I was not able to retrieve the corresponding ECCC winter bulletins (URL pattern guesses for `winter-1998-bulletin.html` / `winter-2016-bulletin.html` both 404'd, and the archive index page did not resolve). **[gap, flagged rather than filled]**

### Any dependence on EP vs CP flavour, or on the PDO?

I did not find a paper in this search that directly tests EP-vs-CP flavour dependence for the Canadian temperature pattern specifically (the EP/CP distinction in the Region-C Hawaii analysis in `lit_missing_americas.md` used Lu et al. 2020, which does not cover Canada). On the PDO: Bonsal et al. (2001) is explicit and is the answer to this part of the task —
> "positive PDO winters are associated with strong positive temperature anomalies over most of Canada, neutral PDO with weaker anomalies (positive in the west and negative in the east), and negative PDO with strong negative anomalies over western Canada." **[ABSTRACT-ONLY, quoted above]**
With the PDO currently at roughly −1.8, this predicts a **weakened or reversed warm signal specifically over western Canada**, consistent with the modest 2023-24 Prairie/BC anomalies above, while eastern Canada's response depends on the NAO rather than the PDO in their framework, so the negative PDO does not by itself argue against warmth reaching Ontario/Quebec.

### Tier and recommendation

**Tier: medium overall; medium-high if the region is redrawn as "central Canada, west of Hudson Bay (Manitoba/northern Ontario), extending more weakly and conditionally into southern Ontario and Quebec"; medium-low if the map keeps "central and eastern Canada" as two equally robust zones.** The mechanism is real and multiply documented (Shabbar & Khandekar 1996; Bonsal, Shabbar & Higuchi 2001), and the most recent strong event (2023-24) is qualitatively consistent with a Manitoba/Ontario-border-centered anomaly extending into the Great Lakes/St. Lawrence corridor. But two of the three papers checked (Bonsal et al. 2001; Ropelewski & Halpert 1986) put the *independent*, PDO/ENSO-driven core in **western-to-central**, not central-to-eastern, Canada, and describe the eastward extension into Ontario/Quebec as **NAO-modulated rather than robustly ENSO-driven on its own**. **I recommend flagging this on the map or in a caveat**: label the core "central Canada / west of Hudson Bay" with a note that the signal weakens and becomes NAO-dependent further east into Ontario and Quebec, rather than presenting "central and eastern Canada" as a single, equally robust warm region. This is the clearest place in this whole review where the literature pushes back on the proposed region as currently framed. A "signal not independently verified against 1997-98/2015-16" flag is also warranted given the retrieval gap above.

---

## Bottom line for the two regions

- **Region A (interior BC/inland NW dry):** supported at **medium** confidence by two solid, independently verified papers, with real complications (R&H 1986 finds no high-latitude precip signal at all; the coastal signal is a north-south dipole, not simply wet; event verification is an open gap).
- **Region B (central & eastern Canada warm):** the mechanism is real, but the literature's own spatial center of mass is **western-to-central Canada**, with the eastern (Ontario/Quebec) extension being **secondary and NAO-conditional** rather than an independently robust ENSO signal. **The map's placement/label should probably shift toward "central Canada" with a softer eastern extension, rather than treating central and eastern Canada as equally strong.** This is a substantive literature-based objection to the region as titled, not just a confidence-tier nuance.
