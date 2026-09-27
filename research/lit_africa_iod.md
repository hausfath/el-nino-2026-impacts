# Literature check: Southern Africa drought and Horn of Africa short-rains confidence under 2026–27 El Niño + strong +IOD

Prepared 2026-09-23. Context: record, EP-leaning El Niño (peak Nov–Dec 2026) with a strong +IOD forecast for late 2026. Reviewer question: does the 1997–98 case (strong EP El Niño + strong +IOD → southern Africa drought "failure") mean the map's HIGH confidence on southern Africa drought needs a caveat, and what does the literature say about Horn of Africa short-rains skill/drivers.

All DOIs below were checked against `https://api.crossref.org/works/<DOI>` on 2026-09-23; title/author/year/journal were confirmed to match before inclusion. Where I could not get past a paywall to full text, quotes are pulled from the Crossref-hosted abstract (tagged ABSTRACT-ONLY) or from open-access full text (tagged VERIFIED-PRIMARY with URL). Anything from a news summary, gray-literature report, or web-search synthesis is tagged SECONDARY/UNVERIFIED and should not be treated as a peer-reviewed finding.

**Independent sanity check I ran**: I pulled the HadISST-based Dipole Mode Index monthly series direct from NOAA PSL (`https://psl.noaa.gov/data/timeseries/month/data/dmi.had.long.data`) and computed SON-mean DMI for the key comparison years myself, rather than trusting secondary "list of IOD years" text. Results (°C, SST-anomaly based, not normalized):

| Year | SON-mean DMI (°C) | ENSO state (SON) | SA outcome |
|---|---|---|---|
| 1982 | +0.45 | Strong/very strong EP El Niño | Severe drought |
| 1991 | +0.04 | Strong El Niño | Severe drought |
| 1994 | +0.51 | Weak El Niño | — |
| 1997 | **+0.98** | Extreme EP El Niño | Drought **failed to materialize** |
| 2006 | +0.50 | Weak/moderate El Niño | — |
| 2015 | +0.37 | Extreme El Niño (weak IOD) | Severe drought (worst in ~35 yr) |
| 2018 | +0.60 | Weak El Niño/neutral | — |
| 2019 | +0.90 | ENSO-neutral | (no SA El Niño drought test case) |
| 2023 | **+0.89** | Strong El Niño | Severe drought (worst on record) |

This is the single most important finding for the reviewer's question: **1991 was NOT a genuine positive-IOD year** (SON DMI ≈ 0.04°C, essentially neutral) despite appearing on some secondary "positive IOD years" lists I found in initial web searches — I am flagging that discrepancy rather than propagating it. And **2023, with a SON DMI (+0.89°C) almost as extreme as 1997's (+0.98°C)**, produced the worst southern African drought on record rather than a repeat of the 1997–98 failure. That is a direct, recent, strong-event counter-example to the idea that a strong +IOD reliably neutralizes the El Niño–southern Africa drought signal.

---

## Part A — Southern Africa drought under co-occurring El Niño + strong +IOD

### Key papers

| # | Citation | DOI / link |
|---|---|---|
| A1 | Lyon, B. & Mason, S.J. (2007). The 1997–98 Summer Rainfall Season in Southern Africa. Part I: Observations. *J. Climate* 20(20), 5134–5148. | [10.1175/JCLI4225.1](https://doi.org/10.1175/JCLI4225.1) |
| A2 | Lyon, B. & Mason, S.J. (2009). The 1997/98 Summer Rainfall Season in Southern Africa. Part II: Model Simulations and Coupled Model Forecasts. *J. Climate* 22(14), 3802–3818. | [10.1175/2009JCLI2600.1](https://doi.org/10.1175/2009JCLI2600.1) |
| A3 | Hoell, A., Funk, C., Zinke, J. & Harrison, L. (2017). Modulation of the Southern Africa precipitation response to the El Niño Southern Oscillation by the subtropical Indian Ocean Dipole. *Climate Dynamics*. | [10.1007/s00382-016-3220-6](https://doi.org/10.1007/s00382-016-3220-6) |
| A4 | Pomposi, C., Funk, C., Shukla, S., Harrison, L. & Magadzire, T. (2018). Distinguishing southern Africa precipitation response by strength of El Niño events and implications for decision-making. *Environ. Res. Lett.* 13, 074015. | [10.1088/1748-9326/aacc4c](https://doi.org/10.1088/1748-9326/aacc4c) |
| A5 | Wang, [initials], Geng, Cai & Lin (2026). Shallow Eastern Indian Ocean Thermocline Hinders ENSO Teleconnection to Southern Africa. *Geophysical Research Letters*. | [10.1029/2026GL122109](https://doi.org/10.1029/2026GL122109) |
| A6 | Liu, Yang, Zhao, Feng, Han & Wu (2017). Why Was the Indian Ocean Dipole Weak in the Context of the Extreme El Niño in 2015? *J. Climate*. | [10.1175/JCLI-D-16-0281.1](https://doi.org/10.1175/JCLI-D-16-0281.1) |
| A7 | Cai, W., Reason, C.J.C., Mohino, E., Rodríguez-Fonseca, B., Malherbe, J., Santoso, A., Li, T., Chikoore, H., Nnamchi, H. & McPhaden, M.J. (2025). Climate impacts of the El Niño–Southern Oscillation in Africa. *Nature Reviews Earth & Environment*. | [10.1038/s43017-025-00705-7](https://doi.org/10.1038/s43017-025-00705-7) |

Note on A5: Crossref returned author family names "Wang, Geng, Cai, Lin" but I could not confirm the full given-name spelling of the first author beyond the abstract page; title/journal/year/DOI all matched on Crossref.

### (i) The 1997–98 "failure" and its explanation

Lyon & Mason 2007 abstract (Crossref) [ABSTRACT-ONLY: https://doi.org/10.1175/JCLI4225.1]:

> "Following the onset of the strong El Niño of 1997–98 historical rainfall teleconnection patterns and dynamical model predictions both suggested an enhanced likelihood of drought for southern Africa, but widespread dry conditions failed to materialize... An unusually strong Angola low, exceptionally high sea surface temperatures (SSTs) in the western Indian and eastern tropical South Atlantic Oceans, and an enhanced northerly moisture flux from the continental interior and the western tropical Indian Ocean all appear to have contributed to more seasonal rainfall in 1997–98 over much of the southern Africa subcontinent than in past El Niño events."

Lyon & Mason 2009 (Part II) abstract [ABSTRACT-ONLY: https://doi.org/10.1175/2009JCLI2600.1]:

> "All three AGCMs generated widespread drought conditions across southern Africa, similar to those during past El Niño events, and did a generally poor job in generating the observed rainfall and atmospheric circulation anomaly patterns... In contrast, two of the three coupled models showed a higher probability of wetter conditions in JFM 1998 than for past El Niño events, with an enhanced moisture flux from the Indian Ocean, as was observed. However, neither the AGCMs nor the coupled models generated anomalous stationary wave patterns consistent with observations over the South Atlantic and Pacific. The failure of any of the models to reproduce an enhanced Angola low..."

This is important: even the coupled models that got closer to the right answer did so via the Indian Ocean moisture-flux pathway, not via correctly capturing the atmospheric circulation anomaly in full — i.e., 1997–98 was not a simple, mechanistically clean "IOD overrides ENSO" story even in hindsight simulation.

Cai et al. 2025 review, full text (I downloaded and text-extracted the open-access PDF) [VERIFIED-PRIMARY: https://repository.library.noaa.gov/view/noaa/71705/noaa_71705_DS1.pdf]:

> "Variability of the Angola Low modulates ENSO impact on Africa; for example, during the 1997/98 event, the Angola Low hardly weakened, and an expected drought did not occur in southern Africa."

> "The [Botswana] High during the 1997/98 strong El Niño event was less intense than the weaker 1986/1987 El Niño event, contributing to a condition against an expected severe dry season in 1997/98."

> "The strength of the [Botswana] high varies independently of ENSO; for example, large anomalies in the Botswana High are observed in a number of neutral ENSO summers when Southern Africa is unusually wet or dry."

**My read**: the peer-reviewed literature attributes the 1997–98 failure to a specific, somewhat idiosyncratic combination of regional circulation features (an unusually persistent/non-weakening Angola Low, an unusually weak Botswana High, a wet 7-day trough event in Jan 1998 contributing >40% of the season's rain per the Cai review) plus anomalously warm SW Indian Ocean/tropical Atlantic SSTs — not a generic, reproducible "+IOD cancels ENSO drying" mechanism. The Angola Low and Botswana High are both described as varying *independently* of ENSO, i.e., as wildcards that can go either way in any given El Niño year, extreme-IOD or not.

### (ii) Does +IOD / warm SW Indian Ocean SST systematically weaken the link?

Two distinct Indian Ocean modes get conflated in casual discussion and I want to flag this explicitly: the **tropical Indian Ocean Dipole (IOD)** (Sumatra–East Africa dipole, peaks SON) and the **subtropical Indian Ocean Dipole (SIOD)** (a mid-latitude mode, ~25–35°S). The reviewer's "warm SW Indian Ocean SST" phrasing is closer to the SIOD's southwest pole than to the tropical IOD.

Hoell et al. 2017 (Crossref metadata confirmed but no abstract text available; summarized from search-engine synthesis) [SECONDARY/UNVERIFIED — I could not retrieve verbatim journal text]:

> The SIOD can complement or disrupt the ENSO-forced response over southern Africa — when ENSO and SIOD are out of phase, the response is stronger than ENSO alone; when in phase, weaker.

Cai et al. 2025 review, full text [VERIFIED-PRIMARY, same PDF as above], on the *SIOD* specifically (not the tropical IOD):

> "El Niño-induced equatorward weakening of the subtropical highs drives a coherent negative phase of the Subtropical Indian Ocean Dipole... helping deliver El Niño impact to southern Africa. For example, the associated cold SST anomalies south of Madagascar decrease moist air from the subtropical South Indian Ocean towards southeastern Africa, favouring anomalously dry and hot summers... The impact becomes not statistically significant after ENSO influence is removed... suggesting that the Subtropical Indian Ocean Dipole is by and large a response to ENSO, facilitating ENSO impacts."

So per Cai et al. 2025, the SIOD's *typical, El-Niño-forced* phase (cold pole south of Madagascar) **reinforces** rather than weakens the drought signal, and is described as largely a response to ENSO rather than an independent modulator. That is the opposite direction from the reviewer's worry, but note it concerns the SIOD, and a genuinely anomalous, independent SIOD phase (as apparently occurred in 1997–98, given the "exceptionally high SSTs in the western Indian Ocean" in Lyon & Mason) can go the other way and buck the ENSO-forced tendency. Wang et al. 2026 (GRL) makes a related but distinct point about model structural bias [ABSTRACT-ONLY: https://doi.org/10.1029/2026GL122109]:

> "Climate models have struggled to simulate the ENSO impact pattern, with excessive southwestward contraction of El Niño-induced dry anomalies alongside wet anomalies extending too far into central southern Africa... an overly-shallow mean thermocline in the eastern Indian Ocean... distorts the ENSO teleconnection... leading to a spurious drying in northeast but wetting in southeast and central southern Africa."

This is a 2026 paper about a *model* bias (CMIP6-class models overstating a zonal IO dipole response and thereby distorting the simulated ENSO–southern Africa rainfall pattern), not a claim about the real atmosphere. It is relevant to the map only insofar as it's a reason to distrust dynamical-model-based confidence upgrades that lean on an amplified simulated IOD response.

**Bottom line on (ii)**: I do not find a peer-reviewed, event-tested claim that a strong tropical +IOD *systematically* weakens the El Niño–southern Africa drought teleconnection. The strongest empirical test of that hypothesis is exactly the 1997 vs. 2023 comparison in my DMI table above: both had SON DMI in the 0.9–1.0°C range (by far the two strongest Indian-Ocean-basin analogs available), both co-occurred with strong-to-extreme EP-leaning El Niño, and they produced opposite southern African outcomes (near-normal rain in 1997–98 vs. worst-on-record drought in 2023–24). That strongly suggests +IOD strength alone is not the operative variable, and that the 1997–98 case reflects sampling from the "independently varying" Angola Low / Botswana High degrees of freedom that Cai et al. 2025 explicitly describe, not a repeatable IOD-driven override.

### (iii) 1982–83, 1991–92, 2015–16, 2023–24 outcomes

- **1982–83**: SON DMI +0.45°C (moderate, not extreme). Strong/very strong EP El Niño. Outcome: severe drought — one of the strong-El-Niño droughts Pomposi et al. 2018 group together (their finding, ERL abstract-level, is that strong El Niño events carry an ~80% chance of below-climatological SA rainfall vs. ~60% for moderate/weak events) [SECONDARY/UNVERIFIED for the specific 1982–83 outcome narrative, sourced from search-engine synthesis of Cai et al. 2025 and UN/SADC gray literature; the ~80%/60% statistic is drawn from the Pomposi et al. abstract summary and I was not able to retrieve the full abstract text verbatim from Crossref].
- **1991–92**: SON DMI +0.04°C — essentially **IOD-neutral**, not positive as some secondary sources state. Strong El Niño. Outcome: one of the worst droughts in South African history (halved cereal production per gray-literature reports) [SECONDARY/UNVERIFIED]. Because the IOD was neutral this year, it is not actually a useful test of the +IOD-weakens-drought hypothesis, despite appearing in some lists alongside 1982 and 1997 as a "positive IOD" year — I'd flag that as an error if it appears anywhere in the map's supporting materials.
- **2015–16**: SON DMI +0.37°C (weak). Extreme El Niño (among the strongest on record, comparable to 1997–98 in Pacific SST). Outcome: worst SA drought in ~35 years, 28+ million food insecure [SECONDARY/UNVERIFIED, SADC/OCHA reporting]. Liu et al. 2017 (J. Climate) is directly about why the IOD stayed weak that year despite the extreme El Niño [ABSTRACT-ONLY: https://doi.org/10.1175/JCLI-D-16-0281.1]: "The Indian Ocean witnessed a weak positive Indian Ocean dipole (IOD) event from the boreal summer to autumn in 2015, while an extreme El Niño occurred over the tropical Pacific. This was different from the case in 1997/98, when an extreme El Niño and the strongest IOD took place simultaneously... a combination of the classic El Niño... and the recently identified central Pacific El Niño... had opposite remote influences on the tropical Indian Ocean." This paper itself frames 2015 as evidence that ENSO amplitude and IOD amplitude are not tightly coupled — reinforcing that IOD strength is close to an independent draw, not a deterministic function of El Niño strength/flavor.
- **2023–24**: SON DMI +0.89°C — the second most extreme IOD in my table, comparable to 2019. Strong El Niño. Outcome: worst SA drought on record, 6 countries declared states of emergency, driest three-month period on record in parts of the region [SECONDARY/UNVERIFIED, SADC/OCHA/ReliefWeb reporting — I was not able to find a peer-reviewed attribution paper specifically quantifying this in time for this memo; a World Weather Attribution rapid study exists on El Niño as a driver of the 2024 drought but I have not verified its DOI or pulled quotes from it here].

### Confidence conclusion for Part A

I think **HIGH confidence remains defensible**, but I would add an explicit caveat/footnote rather than leave it silent, for three reasons:
1. The 1997–98 case is real, peer-reviewed, and directly on point (strong EP El Niño + extreme +IOD → drought failure) — it should not be memory-holed.
2. But it is a single case, and the best available literature (Cai et al. 2025; Lyon & Mason 2007/2009) attributes it to circulation features (Angola Low, Botswana High) that the same literature explicitly says vary *independently* of ENSO/IOD strength — i.e., not something the map can conditionally forecast on IOD strength alone.
3. The most comparable recent analog by IOD strength, 2023–24, went the opposite way (worst drought on record with almost as strong a +IOD), which is direct evidence against a robust "+IOD strength → weakened SA drought" dose-response relationship.

**Suggested caveat language for the map**: "Southern Africa drought — HIGH confidence for the core Dec–Feb dry signal. Note: in the one prior case combining an extreme EP El Niño with an extreme +IOD (1997–98), the expected drought failed to materialize (Lyon & Mason 2007, 2009), attributed to an anomalously persistent Angola Low and weak Botswana High rather than the IOD itself. The comparably strong +IOD event of 2023–24 did not repeat this pattern (worst SA drought on record). Confidence should not be downgraded on IOD grounds alone, but users should be aware the 1997–98 outcome exists as a documented low-probability failure mode."

---

## Part B — Horn of Africa / East Africa short rains (OND)

### Key papers

| # | Citation | DOI / link |
|---|---|---|
| B1 | Black, E., Slingo, J. & Sperber, K.R. (2003). An Observational Study of the Relationship between Excessively Strong Short Rains in Coastal East Africa and Indian Ocean SST. *Monthly Weather Review* 131(1), 74–94. | [10.1175/1520-0493(2003)131<0074:AOSOTR>2.0.CO;2](https://doi.org/10.1175/1520-0493(2003)131%3C0074:AOSOTR%3E2.0.CO;2) |
| B2 | Behera, S.K., Luo, J.-J., Masson, S., Delecluse, P., Gualdi, S., Navarra, A. & Yamagata, T. (2005). Paramount Impact of the Indian Ocean Dipole on the East African Short Rains: A CGCM Study. *J. Climate* 18(21), 4514–4530. | [10.1175/JCLI3541.1](https://doi.org/10.1175/JCLI3541.1) |
| B3 | Liu et al. 2017 (as above, A6) | [10.1175/JCLI-D-16-0281.1](https://doi.org/10.1175/JCLI-D-16-0281.1) |
| B4 | Lu, B. & Ren, H.-L. (2020). What Caused the Extreme Indian Ocean Dipole Event in 2019? *GRL*. | [10.1029/2020GL087768](https://doi.org/10.1029/2020GL087768) |
| B5 | Wainwright, C.M., Finney, D.L., Kilavi, M., Black, E. & Marsham, J.H. (2021). Extreme rainfall in East Africa, October 2019–January 2020 and context under future climate change. *Weather* 76(1). | [10.1002/wea.3824](https://doi.org/10.1002/wea.3824) |
| B6 | Hirons, L. & Turner, A. (2018). The Impact of Indian Ocean Mean-State Biases in Climate Models on the Representation of the East African Short Rains. *J. Climate* 31(16), 6611–6631. | [10.1175/JCLI-D-17-0804.1](https://doi.org/10.1175/JCLI-D-17-0804.1) |
| B7 | Igler(?), M., Turner, A.G., Hirons, L.C., Wainwright, C.M. & Marzin, C. (2025). Systematic biases over the equatorial Indian Ocean and their influence on seasonal forecasts of the IOD. *Climate Dynamics* 63, art. 328. | [10.1007/s00382-025-07794-6](https://doi.org/10.1007/s00382-025-07794-6) |
| B8 | Tefera, Liguori, Cabos & Navarra (2025). Seasonal forecasting of East African short rains. *Scientific Reports*. | [10.1038/s41598-025-86564-0](https://doi.org/10.1038/s41598-025-86564-0) |

Note on B7: Crossref lists the first author as "Gler, M." — I believe this is a truncation/OCR artifact for "Igler" based on institutional (Reading/NCAS) search hits, but I could not fully confirm the correct spelling; DOI, title, journal, year all check out.
Note on B8: I could not get past the Nature.com login redirect to pull verbatim text; the DOI/title/journal/year are Crossref-confirmed, but I have no verified quotes from this paper — treat any characterization of its findings as SECONDARY/UNVERIFIED.

### IOD vs ENSO as dominant driver

Behera et al. 2005 abstract [ABSTRACT-ONLY: https://doi.org/10.1175/JCLI3541.1]:

> "Most of the variability in the model short rains is linked to the basinwide large-scale coupled mode, that is, the Indian Ocean dipole (IOD) in the tropical Indian Ocean. The analysis of observed data and model results reveals that the influence of the IOD on short rains is overwhelming as compared to that of the El Niño–Southern Oscillation (ENSO); the correlation between ENSO and short rains is insignificant when the IOD influence is excluded."

This is a strong, direct, peer-reviewed statement that IOD dominates over ENSO for the short rains, consistent with the map's framing of Horn-of-Africa impact size being "set by IOD." Black, Slingo & Sperber 2003 (title alone, DOI-confirmed, but I could not pull Crossref abstract text — MWR pre-abstract era) is the foundational observational paper establishing the Indian-Ocean-SST link to excessively strong short rains; I am not able to give a verbatim quote from it here [tag: DOI VERIFIED, content SECONDARY/UNVERIFIED pending full-text access].

Cai et al. 2025 review [VERIFIED-PRIMARY, same PDF], consistent with Behera:

> "The weakened Walker circulation, the anomalous equatorial easterlies associated with a concurrent pIOD event, and the anomalously strong ITCZ over the western Indian Ocean promote low-level warm moist convergence toward the equatorial east coast of Africa. As a result, anomalously high rainfall occurs during the short-rain season... For example, during the 1997 El Niño event, devastating floods in Somalia, Ethiopia, Kenya, Sudan and Uganda caused several thousand deaths."

> "In the east Africa region, short-rain wet anomaly during EP El Niño is greater than that during CP El Niño, +0.90 mm day⁻¹ and +0.22 mm day⁻¹, respectively... in part because a pIOD induced by EP El Niño is greater than an nIOD induced by CP La Niña."

So the mechanistic picture in the current review literature is that El Niño (especially EP-flavor) contributes to short-rains wetness partly *by* forcing a pIOD — the two are not fully independent, but the IOD is described as carrying the larger direct loading on rainfall variance.

### Forecast skill from September starts

I found several relevant statements from web-search synthesis but could not obtain verbatim primary-source quotes in the time available; flagging accordingly [SECONDARY/UNVERIFIED unless noted]:
- Models initialized in September generally show skill for OND precipitation anomalies across much of East Africa, with skill notably better than August initializations for extreme SON events over equatorial Africa (source: NHESS 2026 paper on ECMWF SEAS5.1 skill, not independently verified here).
- Nicholson 2017 (*Reviews of Geophysics*) [DOI verified: 10.1002/2016RG000544] devotes a section to seasonal forecasting skill for eastern Africa; I was not able to pull verbatim text in the time available, but the review's scope (per its own framing, confirmed via search synthesis) explicitly covers "seasonal forecasting" as one of six major topics — this is the single best entry point for a fuller skill assessment if the map needs one, and I'd recommend reading it directly rather than relying on my secondary summary.

### Known model tendency to overdo IOD amplitude

Hirons & Turner 2018 abstract [ABSTRACT-ONLY: https://doi.org/10.1175/JCLI-D-17-0804.1]:

> "In observations, a wet short-rainy season is associated with the positive phase of the IOD and anomalous easterly low-level flow across the equatorial Indian Ocean. A model's ability to capture the teleconnection to the positive IOD is closely related to its representation of the mean state... those models that exhibit mean-state low-level equatorial easterlies in the Indian Ocean, rather than the observed westerlies, are unable to capture the latitudinal structure of moisture advection into East Africa during a positive IOD... This positive Bjerknes coupled feedback is stronger in easterly mean-state models, resulting in a wetter East African short-rain precipitation bias in those models."

Igler et al. 2025 (Climate Dynamics) abstract [ABSTRACT-ONLY: https://doi.org/10.1007/s00382-025-07794-6]:

> "GloSea6 exhibits a pronounced cold bias in the [eastern equatorial Indian Ocean] that rapidly develops after the monsoon onset in boreal summer... and persists into autumn... This cold bias is linked to erroneous easterlies and a shallow thermocline, likely associated with the monsoon circulation."

This is directly relevant and confirms the reviewer's premise: there is a real, peer-reviewed, model-diagnostics literature (not just impressionistic forecaster experience) documenting that a widely used operational seasonal system (Met Office GloSea6) carries a structural cold/easterly bias in the eastern equatorial Indian Ocean that would tend to inflate simulated IOD-driven short-rains anomalies — i.e., a documented tendency to overdo IOD amplitude/impact in dynamical seasonal forecasts, mechanistically consistent with (though not identical to) the CMIP6-mean-state bias described in Hirons & Turner 2018 and the Wang et al. 2026 southern-Africa thermocline-bias paper (A5 above). This is a cross-cutting model bias that shows up on both sides of the continent.

### 1997, 2019, 2023 outcomes

- **1997**: extreme +IOD (SON DMI 0.98°C, my calc) + extreme EP El Niño → per Cai et al. 2025 [VERIFIED-PRIMARY], "devastating floods in Somalia, Ethiopia, Kenya, Sudan and Uganda caused several thousand deaths and displaced hundreds of thousands of people."
- **2019**: extreme +IOD (SON DMI 0.90°C) with ENSO-neutral background — Lu & Ren 2020 abstract [ABSTRACT-ONLY: https://doi.org/10.1029/2020GL087768]: "An extreme positive Indian Ocean Dipole (IOD) event occurred in 2019 boreal autumn, which has induced severe climate impacts around the Indian Ocean basin." Wainwright et al. 2021 (title/DOI confirmed, could not pull abstract text) covers the resulting East Africa floods and future-climate context [DOI VERIFIED; content SECONDARY/UNVERIFIED pending full-text access]. Gray literature (FEWS NET) reports the 2019 short rains as among the wettest on record, 200–400% of average in places. This case demonstrates the IOD can drive an extreme short-rains wet season with essentially no help from ENSO — consistent with Behera et al.'s "IOD dominant" conclusion.
- **2023**: strong +IOD (SON DMI 0.89°C) + strong El Niño → per gray-literature/search synthesis, initial OND forecasts (both El Niño and +IOD favoring wet) verified in direction but the resulting floods were severe enough (compared explicitly to 1997 in some reporting) to cause major humanitarian impact after a preceding multi-year drought — I was not able to locate a peer-reviewed post-event verification paper for 2023 in the time available; treat the outcome narrative as SECONDARY/UNVERIFIED (FEWS NET, ICPAC, and general news reporting).

### Confidence conclusion for Part B

MEDIUM confidence for "Horn of Africa floods, Oct–Dec, size set by IOD" looks well supported and, if anything, slightly conservative relative to the mechanistic literature (Behera et al. 2005's "overwhelming" IOD influence is about as strong a peer-reviewed statement as you'll find in this literature). I would keep it at MEDIUM rather than raise it, specifically because of the documented, peer-reviewed model tendency to overdo IOD amplitude/impact (Hirons & Turner 2018; Igler et al. 2025) — a real physical driver with a real forecast-amplification bias layered on top is exactly a MEDIUM-not-HIGH situation, since the map presumably draws partly on dynamical model guidance for magnitude. I'd add a short note flagging the bias explicitly, since it cuts toward the outlook being too wet, not too dry, in ensemble mean forecasts.

---

## Part C — Robust El Niño DJF signal elsewhere in Africa

I could verify this fully via the Cai et al. 2025 Nature Reviews Earth & Environment review, which I downloaded and text-extracted directly (open access via NOAA repository mirror) [VERIFIED-PRIMARY: https://repository.library.noaa.gov/view/noaa/71705/noaa_71705_DS1.pdf].

**Guinea coast dry, DJF, EP-El-Niño-specific:**

> "Towards the Guinea coast, EP El Niño shows a drying in DJF, owing to an associated increase in subsidence over the equatorial eastern Atlantic arising from increased convection over the western Indian Ocean; such dry anomalies are not seen during CP El Niño."

This is exactly the reviewer's claim, and it is explicitly flavor-dependent: it is a documented feature of EP El Niño composites specifically (relevant to the 2026–27 event, which is described as EP-leaning), and the review states it does *not* show up in CP El Niño composites. I have not independently verified the underlying composite dataset or replicated the calculation — this is one review's synthesis, referencing underlying primary sources (Ropelewski & Halpert 1987, DOI 10.1175/1520-0493(1987)115<1606:garspp>2.0.co;2, confirmed; and others I have not individually chased down).

**Equatorial/off-equatorial East Africa wet, extending into DJF:**

> "By contrast, over off-equatorial East Africa, above-average rainfall occurs because the seasonal southward excursion of the [South Indian Convergence Zone] and cloud band events are impeded and shift northeastward to the off-equatorial regions... In MAM, as the El Niño-induced [Indian Ocean Basin] warming continues, the dry and warm condition persists in southern Africa... El Niño-induced negative phase of the Subtropical Indian Ocean Dipole... reinforcing the anomalously dry and hot conditions over southern east Africa and anomalously wet and cold conditions over east Africa."

So yes — there is a documented, quantified (in the review's Fig. 2 composites, which I did not reproduce myself) DJF and MAM extension of the wet-north/dry-south dipole, i.e., the equatorial/off-equatorial East Africa wet anomaly is not confined to the OND short rains but is described as persisting into DJF and MAM in the ENSO composite framework used by this review.

**Caveat**: this entire section rests on one (very recent, comprehensive, and to my reading credible) review paper's composite analysis. I was not able to independently verify the underlying station data or locate a second independent paper making the identical DJF/Guinea-coast claim in the time available. I would call this MEDIUM-to-HIGH confidence as a documented pattern in dynamical/composite analyses, but flag that I have single-sourced it to one 2025 review, which is a genuine limitation given how specific the EP-vs-CP flavor-dependence claim is.

---

## Summary table

| Map claim | Current tier | Literature support | Recommended tier | Flag needed? |
|---|---|---|---|---|
| Southern Africa drought, Dec–Feb | HIGH | Strong for the core signal; one well-documented failure case (1997–98) attributed to independently-varying regional circulation (Angola Low/Botswana High), not to +IOD per se; 2023–24 (comparable +IOD strength) did not repeat the failure | **Keep HIGH**, add caveat footnote citing 1997–98 as a known low-probability failure mode | Yes — "signal underperformed once (1997–98); did not underperform in the most comparable recent strong-+IOD analog (2023–24)" |
| Horn of Africa floods, Oct–Dec, size set by IOD | MEDIUM | IOD dominance over ENSO well supported (Behera et al. 2005); documented, peer-reviewed model bias toward overestimating IOD amplitude/impact (Hirons & Turner 2018; Igler et al. 2025) | **Keep MEDIUM** | Yes — flag that ensemble/dynamical guidance for magnitude likely skews wet-biased |
| (New, Part C) Guinea coast dry DJF (EP El Niño only) | not currently on map | Documented in one 2025 review composite analysis, EP-flavor-specific | Could add as LOW-MEDIUM, single-sourced | Flag single-source status |
| (New, Part C) Equatorial/off-equatorial East Africa wet extending into DJF/MAM | not currently on map | Same review, same caveat | LOW-MEDIUM, single-sourced | Flag single-source status |

## Honesty notes on this memo

- I verified every DOI cited above against Crossref and confirmed title/author/year/journal match before including it. Where I could not get past a paywall, I used the Crossref-hosted abstract text (tagged ABSTRACT-ONLY) rather than fabricate full-text quotes.
- Several claims in this memo — the specific 1982–83/1991–92/2023–24 outcome narratives, the September-initialization forecast-skill claim, the Black/Slingo/Sperber and Wainwright et al. content, and the Tefera et al. 2025 content — are DOI-verified as real papers but I was not able to pull verbatim primary-source text for them in the time available. These are explicitly tagged SECONDARY/UNVERIFIED and should be checked against full text before being used in the final piece if precise wording matters.
- The DMI table is the one piece of genuinely new, self-computed analysis in this memo (not from any single source) — I'd treat it as reasonably solid (it's a standard, widely used index computed directly from NOAA's published monthly HadISST-based series) but note it uses raw °C anomalies from one particular DMI product (HadISST-based); other IOD indices (e.g., OISST-based, as used in some of the news reporting on 2019/2023 "second-strongest on record" claims) use different base periods and can give somewhat different absolute magnitudes, though the relative ranking of these years should be robust.
