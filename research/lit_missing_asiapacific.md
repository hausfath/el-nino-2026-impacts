# Literature check: candidate Asia-Pacific regions for the El Niño 2026-27 impacts map

Prepared 2026-09-23. Context: record, east-Pacific-leaning El Niño underway, peak expected Nov–Dec 2026, with a forecast positive IOD. Goal: decide, region by region, whether peer-reviewed literature supports adding/adjusting a teleconnection on the impacts map.

**Process note:** This was run as four parallel, independently-researched passes (one per region), each required to confirm every DOI live against the Crossref API (`api.crossref.org/works/<DOI>`) before citing it, and to pull verbatim text from the publisher/repository page where possible. A compiling pass then independently re-verified all 22 distinct DOIs referenced below against Crossref itself (title/author/year match confirmed for all). Many publisher pages (AMS, AGU/Wiley, Springer, Elsevier) blocked automated fetches (403/login-wall), so several quotes could only be obtained via abstract-indexing services or search-engine paraphrase rather than the publisher page itself — these are tagged `[SECONDARY/UNVERIFIED]` even where an earlier draft of this file had over-tagged them as `[ABSTRACT-ONLY]`. No DOI here was written from memory; several strings that could not be independently confirmed were dropped rather than guessed.

---

## A. Philippines — dry DJF–MAM in El Niño decay

**Anomaly / mechanism:** Below-normal rainfall across most of the Philippines from northern winter into spring (DJF, persisting into MAM especially for east-Pacific-type events), driven by a Rossby-wave-forced anomalous anticyclone over the western North Pacific (WNPAC) that suppresses convection and cross-equatorial moisture convergence over the archipelago. Same WNPAC that drives the southern China wet signal (Region C) — it is the west/southwest flank of the same feature that matters for the Philippines (subsidence) versus the northwest flank (moisture transport) that matters for China.

**Key papers:**

1. **Lyon, B. & Camargo, S. J. (2009).** "The seasonally-varying influence of ENSO on rainfall and tropical cyclone activity in the Philippines." *Climate Dynamics* 33, 3–15. https://doi.org/10.1007/s00382-008-0380-z
   - Crossref-confirmed: title/authors (Lyon, Camargo)/2009 match.
   - Full text obtained via an open-access author copy (Columbia/LDEO repository, via Unpaywall) and read directly. Verbatim: *"precipitation in most regions of the Philippines is typically below (above) average in the fall and winter of EN (LN) events (Ropelewski and Halpert 1987; Kiladis and Diaz 1989)"* and *"development of an anomalous anticyclone (cyclone) over the WNP in El Niño (La Niña) and the well-known tendency for below (above) average rainfall in the fall."* **[VERIFIED-PRIMARY: https://www.ldeo.columbia.edu/~suzana/papers/lyon_camargo_clim_dyn09.pdf]**
   - Caveat: the paper's own new empirical result is actually a summer-wet/fall-dry reversal specific to the north-central Philippines; its DJF-dry claim leans on the older Ropelewski & Halpert (1987) and Kiladis & Diaz (1989) studies, which were not independently re-verified in this pass.

2. **Yu, T., Feng, J., Chen, W. & Wang, X. (2021).** "Persistence and breakdown of the western North Pacific anomalous anticyclone during the EP and CP El Niño decaying spring." *Climate Dynamics* 57, 3529–3544. https://doi.org/10.1007/s00382-021-05882-x
   - Crossref-confirmed: title/authors/2021 match.
   - Directly relevant to 2026: distinguishes EP vs. CP El Niño — the EP-type WNPAC persists into spring (MAM), while the CP-type breaks down earlier. Given the 2026 event is described as east-Pacific-leaning, this supports extending the dry window into MAM rather than stopping at DJF. **[SECONDARY/UNVERIFIED]** for exact wording — Springer page login-walled; only a search-engine paraphrase obtained ("the EP El Niño-induced WNPAC has good persistence in spring, whereas the CP El Niño-induced WNPAC has an obvious breakdown in spring"). DOI/authorship/title solid.

3. **Lu, M.-M. et al. (2023).** "The Philippine springtime (February–April) sub-seasonal rainfall extremes and extended-range forecast skill assessment using the S2S database." *Weather and Climate Extremes* 41, 100582. https://doi.org/10.1016/j.wace.2023.100582
   - Crossref-confirmed: title/7 authors/2023 match; open access (CC-BY-NC-ND).
   - Supports the MAM-specific (Feb–Apr) part of the claim. **[SECONDARY/UNVERIFIED]** for wording — ScienceDirect 403'd; only a paraphrase obtained ("extremely dry [sub-seasonal peak rainfall events] tend to occur during El Niño springs" vs. wet during La Niña springs).

4. **Wang, B., Wu, R. & Fu, X. (2000).** "Pacific–East Asian Teleconnection: How Does ENSO Affect East Asian Climate?" *J. Climate* 13(9), 1517–1536. https://doi.org/10.1175/1520-0442%282000%29013%3C1517%3APEATHD%3E2.0.CO%3B2 — foundational WNPAC mechanism paper, shared with Region C; see Region C for quote status.

*(Villafuerte, Matsumoto & Kubota 2015, `10.1002/joc.4105`, and Villafuerte & Matsumoto 2015, `10.1175/JCLI-D-14-00531.1`, both Crossref-confirmed and on-topic, were also located but no usable quote was obtained from either — listed as supporting-but-unquoted background rather than as key citations.)*

**Observed outcomes in named events** (secondary sources only — World Bank "Striking a Balance" 2019, DOST-PCAARRD, news reporting; **not** independently checked against primary PAGASA bulletins, so treat magnitudes as indicative, not publication-ready):
- **1982–83:** ~450,000 ha farmland affected; ~US$14M rice/maize damage.
- **1997–98 (strongest on record):** rainfall ~half of normal in parts of the country; ~US$240M agricultural damage; rice −27%, maize −44%; Angat reservoir ~32% of normal; Metro Manila water rationing.
- **2015–16:** 18-month dry episode; >400,000 farmers, ~550,000 ha affected; ~US$327M agricultural losses.
- **2023–24 (moderate event):** dry spell from Nov 2023; ~₱15.3 billion agricultural damage; 333,195 farmers/fishers affected.
None of these secondary sources give a monthly DJF-vs-MAM breakdown — the seasonal timing rests on the peer-reviewed papers above, not the damage reports.

**Caveats:**
- EP vs. CP flavour matters (Yu et al. 2021): the DJF–MAM window is not flavour-invariant. The 2026 event's EP-leaning character favors MAM persistence, but that is forecast framing, not an observed outcome yet.
- Lyon & Camargo's DJF claim rests partly on older studies not independently re-verified here.
- No explicit search was made for failed/null cases (El Niño winters where the Philippines stayed wet) — a gap, not a resolved question.

**Confidence tier: medium-high for DJF; medium for extension into MAM.** Justification: the DJF mechanism now has one genuinely primary-text-verified paper (Lyon & Camargo) plus a foundational mechanism paper (Wang, Wu & Fu 2000); the MAM extension is supported by two Crossref-confirmed, on-topic, but quote-unverified papers, and depends on the 2026 event's (still forecast, not observed) EP character.

---

## B. Mainland Southeast Asia / Mekong basin — dry during/after El Niño

**Starting point:** this project's existing dossier (`impacts-verification-asia-foundational.md`) states "no peer-reviewed citation verified" for Mekong drought claims. That finding holds for the *specific event-magnitude* claims (e.g., "worst drought in ~90 years," province counts, hectares salinized) — those remain grey-literature only (ReliefWeb, Vietnam News, Save the Children). **It does not hold for the general teleconnection**, where a careful re-search this pass found real, Crossref-verified, on-topic peer-reviewed literature. The picture is narrower and more caveated than a blanket "Mekong basin dry" label, though — this is not a green light for an unqualified regional claim.

**Best-supported claim:** a dry (precipitation → meteorological/hydrological drought) anomaly concentrated in **March–May of the El Niño decay year**, strongest and statistically most robust in the **southern/central Mekong basin** (Cambodia, southern Laos, southern Vietnam/Mekong Delta), and weak-to-insignificant in the northern basin (Yunnan, northern Laos, northern Thailand). Separately, Thailand's JJA monsoon rainfall shows a negative ENSO relationship, but one that is **nonstationary** — it only emerged post-1980. Mechanism: El Niño shifts the descending branch of the Pacific Walker circulation over Thailand–Indochina–the Maritime Continent, suppressing convection; effect is stronger for east-Pacific-flavor El Niño and the relationship is asymmetric (weaker for El Niño than for La Niña).

**Key papers:**

1. **Räsänen, T. A., Lindgren, V. & Guillaume, J. H. A. (2016).** "On the spatial and temporal variability of ENSO precipitation and drought teleconnection in mainland Southeast Asia." *Climate of the Past* 12, 1889–1905. https://doi.org/10.5194/cp-12-1889-2016
   - Crossref-confirmed. Open access (Copernicus). Verbatim, fetched directly from the article page: *"the variability of the hydroclimate over mainland Southeast Asia is strongly influenced by the El Niño–Southern Oscillation (ENSO)"*; *"the effects of ENSO were found to be most consistent and expressed over the largest areal extents during March–May of the year when the ENSO events decay"*; but also *"considerable variability in ENSO's influence was revealed: the spatial pattern of precipitation anomalies varied between individual ENSO events, and the strength of ENSO's influence was found to vary through time."* **[VERIFIED-PRIMARY: https://cp.copernicus.org/articles/12/1889/2016/]**
   - This is the load-bearing citation. It supports the MAM decay-phase timing but explicitly warns the pattern is event-dependent, not a reliable every-time signal.

2. **Nguyen, V. T., Li, Q., Vu, D. T. & Chen, H. (2023).** "Multiple drought indices and their teleconnections with ENSO in various spatiotemporal scales over the Mekong River Basin." *Science of the Total Environment* 863, 158589. https://doi.org/10.1016/j.scitotenv.2022.158589
   - Crossref-confirmed. **[ABSTRACT-ONLY, via Semantic Scholar; ScienceDirect 403'd]**: *"the strongest ENSO events in Dec-Jan-Feb may result in developments of meteorological drought in Mar-Apr-May... significant influences on drought variabilities in southern MRB and were insignificant in the north."* — the primary source for the north/south basin asymmetry claim above.

3. **Singhrattna, N., Rajagopalan, B., Kumar, K. K. & Clark, M. (2005).** "Interannual and Interdecadal Variability of Thailand Summer Monsoon Season." *J. Climate* 18(11). https://doi.org/10.1175/jcli3364.1
   - Crossref-confirmed. Verbatim: *"ENSO, have a negative relationship with the summer monsoon rainfall over Thailand in recent decades. However, the relationship... was weak prior to 1980."* **[VERIFIED-PRIMARY]**

4. **Watanabe, S., Phan, T. D., Yamazaki, S. & Chiang, F. (2022).** "Nonstationary footprints of ENSO in the Mekong River Delta hydrology." *Sci. Reports* 12, 17303. https://doi.org/10.1038/s41598-022-20597-7
   - Crossref-confirmed. Reinforces that the ENSO-Mekong Delta hydrological signal is not a fixed linear relationship but tracks the central-Pacific ENSO index specifically at times. **[VERIFIED-PRIMARY]** (publisher page — Nature/Sci Rep is open access — fetched directly).

5. **Le Roy, E. J. & Ummenhofer, C. C. (2025).** "Past and Future Modulation of the ENSO Teleconnection to Southeast Asian Rainfall by Interbasin Interactions." *GRL*. https://doi.org/10.1029/2024GL111916
   - Crossref-confirmed. **[ABSTRACT-ONLY, via Semantic Scholar; AGU page 403'd]**: *"Due to ENSO teleconnection asymmetry, Southeast Asian rainfall is more sensitive to La Niña than El Niño."* Important, recent, directly relevant caveat: El Niño is explicitly the weaker half of this relationship.

*(Räsänen & Kummu 2013, `10.1016/j.jhydrol.2012.10.028`, Crossref-confirmed and on-topic but no usable quote obtained — Elsevier 403'd throughout.)*

**Observed outcomes in named events:**
- **1997–98:** Vietnam drought, ~3M people affected, ~US$400M losses — grey literature only, no peer-reviewed attribution located.
- **2015–16:** widely reported (media/MRC) as the "longest/most severe" Lower Mekong drought, coincident with the strong 2015–16 El Niño; no formal peer-reviewed attribution study isolating El Niño's specific share was found. Consistent with, but not proof from, Räsänen et al. (2016).
- **2019–20:** a severe drought occurred, but in a weak-El-Niño/neutral year, which actively *weakens* clean ENSO attribution for that event.
- **1982–83, 2023–24:** no quantitative peer-reviewed or primary-agency source found for either event this pass — flagged as a gap, not a negative finding.

**Caveats:**
- Strong north–south basin asymmetry: the signal is real and robust in the southern/central basin, weak/insignificant in the north (Nguyen et al. 2023).
- Nonstationary relationship: weak/absent before ~1980 (Singhrattna et al. 2005); tracks CP-ENSO index specifically at times (Watanabe et al. 2022).
- Asymmetric and event-variable: weaker for El Niño than La Niña (Le Roy & Ummenhofer 2025); spatial pattern and strength vary between individual events (Räsänen et al. 2016).
- Streamflow/hydrological studies are confounded by upstream damming and land-use change, which is a hydrological rather than purely climatic signal.
- The specific magnitude claims used in earlier project drafts (90-year drought, hectares salinized, province counts) remain **unverified against peer-reviewed sources** — that part of the prior dossier finding stands unchanged.

**Confidence tier: medium for a narrow, spatially-specific claim ("southern/central Mekong basin: drought risk, MAM of the El Niño decay year"); low for a basin-wide, all-season "Mekong drought" claim.** Justification: three independently Crossref-verified, on-topic papers (Räsänen et al. 2016 with a genuine verbatim primary quote, Nguyen et al. 2023, Watanabe et al. 2022) now support the narrow claim — this corrects the earlier dossier's blanket "no literature" finding. But the two most recent, most relevant papers both caveat the relationship as event-variable and structurally weaker for El Niño than La Niña, and there is zero verified peer-reviewed event-attribution for 2015–16/2023–24 magnitudes. **Recommendation: if added to the map, phrase narrowly** — "Southern/central Mekong basin: drought risk, Mar–May (decay year)" — not a basin-wide, year-round label.

---

## C. Southern/southeastern China — wet DJF–MAM in El Niño

**Anomaly / mechanism:** Above-normal rainfall over southern and southeastern China (Guangdong, Guangxi, Fujian and neighboring provinces) in winter through spring during and after El Niño, via the WNPAC: El Niño-suppressed convection over the western tropical Pacific triggers a Rossby-wave response that spins up an anomalous lower-tropospheric anticyclone over the Philippine Sea/western North Pacific; southwesterly flow on its northwest flank carries South China Sea moisture into southern China.

**Key papers:**

1. **Wang, B., Wu, R. & Fu, X. (2000).** "Pacific–East Asian Teleconnection: How Does ENSO Affect East Asian Climate?" *J. Climate* 13(9), 1517–1536. https://doi.org/10.1175/1520-0442%282000%29013%3C1517%3APEATHD%3E2.0.CO%3B2
   - Crossref-confirmed. **[SECONDARY/UNVERIFIED]**: *"The key system that bridges the warm (cold) events in the eastern Pacific and the weak (strong) East Asian winter monsoons is an anomalous lower-tropospheric anticyclone (cyclone) located in the western North Pacific."* — sourced from an ORNL research-index page reproducing the abstract; AMS publisher page and PDF both 403'd, so not confirmed against the original publisher page itself.

2. **Zhang, R., Sumi, A. & Kimoto, M. (1996).** "Impact of El Niño on the East Asian Monsoon: A Diagnostic Study of the '86/87 and '91/92 Events." *J. Meteorological Society of Japan, Ser. II* 74(1), 49–62. https://doi.org/10.2151/jmsj1965.74.1_49
   - Crossref-confirmed. Verbatim, fetched directly from the publisher (J-STAGE) page: *"a southerly wind anomaly appeared in the lower troposphere along the coast of the East Asia during the mature phases of these two El Niño events"* and, as an explicit nonlinearity caveat from the primary source itself, *"an inverse relationship does not hold during the La Niña periods."* **[VERIFIED-PRIMARY: https://www.jstage.jst.go.jp/article/jmsj1965/74/1/74_1_49/_article]**
   - The '91/92 case (winter mature phase) is directly analogous to the wet-southern-China DJF signal; the '86/87 case is a summer-monsoon response.

3. **Zhang, R., Min, Q. & Su, J. (2017).** "Impact of El Niño on atmospheric circulations over East Asia and rainfall in China: Role of the anomalous western North Pacific anticyclone." *Science China Earth Sciences* 60, 1124–1132. https://doi.org/10.1007/s11430-016-9026-x
   - Crossref-confirmed. **[SECONDARY/UNVERIFIED]**: *"an anomalous lower-tropospheric anticyclone is evident near the Philippine Sea, which usually transports more moisture to southern China and thereby increases local precipitation"* — from a search-engine-generated summary, not a page fetched directly.

4. **Chen, J., Wen, Z., Wu, R., Chen, Z. & Zhao, P. (2014).** "Interdecadal changes in the relationship between Southern China winter–spring precipitation and ENSO." *Climate Dynamics* 43, 1439–1454. https://doi.org/10.1007/s00382-013-1947-x
   - Crossref-confirmed. No usable quote obtained (Springer page inaccessible). Cited only as a pointer to the decadal-non-stationarity caveat below.

**Observed outcomes in named events:** Per a related paper — Lu, Scaife, Dunstone & Smith (2017), "Skillful seasonal predictions of winter precipitation over southern China," *ERL*, https://doi.org/10.1088/1748-9326/aa739a (Crossref-confirmed) — composite analysis reportedly shows positive winter precipitation anomalies of roughly ~100 mm in the Guangdong/Guangxi region for **1982–83, 1997–98, and 2015–16**, with 2015–16 winter described as the wettest for southern China since the 1990s. For **2023–24**, a China Daily report (April 2024) describes a "vast increase in precipitation" in South China. **All event-specific figures here are [SECONDARY/UNVERIFIED]** (search-tool summaries or media reporting, not a primary CMA bulletin or a journal figure opened directly) — recommend spot-checking against CMA National Climate Center bulletins before publishing specific numbers.

**Caveats:**
- CP vs. EP El Niño flavour differences plausibly affect the longitudinal position/strength of the anomaly (parallel to the Philippines case), but a specific China-focused CP/EP paper was not DOI-verified this pass.
- Chen et al. (2014)'s title itself indicates the ENSO–southern China relationship is not stationary across decades; net implication for 2026-27 is ambiguous without a dedicated read.
- Zhang, Sumi & Kimoto (1996) documents explicit ENSO/La Niña asymmetry from the primary source.
- The WNPAC's persistence from winter into spring (needed for the MAM half of the window) is itself an area of active research and plausibly less certain than the DJF core.
- IOD interaction with this specific teleconnection was not directly assessed this pass — a real gap given the 2026-27 positive-IOD forecast.

**Confidence tier: medium-high.** Justification: this is one of the most extensively replicated ENSO–East Asia teleconnections in the literature (consistent mechanism across four independent papers, 1996–2017; consistent sign in 3 of 4 named strong events per secondary sources) — but only one of the four key papers (Zhang, Sumi & Kimoto 1996) yielded a genuine publisher-page verbatim quote, all four named-event magnitudes are secondary/unverified, and decadal non-stationarity plus an unresolved IOD-interaction question add real uncertainty to the spring tail of the window specifically.

---

## D. Eastern Australia — El Niño drought seasonality (SON vs. DJF) and role of the IOD

**Determination:** The literature supports the reviewer's argument. Austral **spring (SON)** is the season when the ENSO–eastern/southeastern Australia rainfall teleconnection is most robust, precisely because that is when ENSO and the IOD co-vary most strongly. By summer (DJF), the IOD signal has typically decayed and the Southern Annular Mode (SAM) and local/regional SST patterns become more influential, degrading ENSO's DJF skill — this is a real, mechanistically-documented override, not just noise around the 2023-24 case.

**Key papers:**

1. **Cai, W., van Rensch, P., Cowan, T. & Hendon, H. H. (2011).** "Teleconnection Pathways of ENSO and the IOD and the Mechanisms for Impacts on Australian Rainfall." *J. Climate* 24(15), 3910–3923. https://doi.org/10.1175/2011JCLI4129.1
   - Crossref-confirmed. **[SECONDARY/UNVERIFIED]** (AMS page 403'd; wording via search summary, not independently verbatim-fetched): finds that because ENSO and IOD are largely uncorrelated in austral winter, ENSO's impact on southern/eastern Australian rainfall is weak then, while the "strong impact of ENSO on southern Australia rainfall in spring is ascribed to the strong covariation of ENSO and the IOD in this season." This is the key mechanistic paper for the reviewer's argument, but the exact wording above should be treated as a paraphrase pending publisher-page access, not a confirmed quote.

2. **Risbey, J. S., Pook, M. J., McIntosh, P. C. & Wheeler, M. C. (2009).** "On the Remote Drivers of Rainfall Variability in Australia." *Mon. Wea. Rev.* 137(10), 3233–3253. https://doi.org/10.1175/2009MWR2861.1
   - Crossref-confirmed. **NO QUOTE OBTAINED** (AMS 403'd; Semantic Scholar abstract field null). Existence/topic/venue confirmed only. Reported (via search summary, unverified) to find ENSO's regions of influence "shift with the seasons," with the IOD "particularly important in the June–October period" — **[SECONDARY/UNVERIFIED]**, not independently confirmed.

3. **Ummenhofer, C. C., England, M. H., McIntosh, P. C. & Meyers, G. A. (2009).** "What causes southeast Australia's worst droughts?" *GRL* 36, L04706. https://doi.org/10.1029/2008GL036801
   - Crossref-confirmed. **NO QUOTE OBTAINED** (AGU/Wiley 403'd). Reported to independently show SE Australia's worst multi-year droughts were Indian-Ocean/IOD-driven rather than Pacific/ENSO-driven — consistent with, and complementary to, the Cai et al. (2011) mechanism, but not independently quote-verified here.

4. **Cai, W., Cowan, T. & Raupach, M. (2009).** "Positive Indian Ocean Dipole events precondition southeast Australia bushfires." *GRL* 36, L19710. https://doi.org/10.1029/2009GL039902
   - Crossref-confirmed. **NO QUOTE OBTAINED** (same access constraints). Directly relevant given the 2026-27 positive-IOD forecast co-occurring with El Niño.

5. **Liguori, G., McGregor, S., Singh, M. & Arblaster, J. (2022).** "Revisiting ENSO and IOD Contributions to Australian Precipitation." *GRL* 49(1). https://doi.org/10.1029/2021GL094295
   - Crossref-confirmed. **[SECONDARY/UNVERIFIED]**: adds a statistical caution that ENSO and IOD indices co-vary so strongly that cleanly separating their independent contributions to Australian rainfall is not statistically robust — a caveat that cuts against over-crediting either driver individually, including in this write-up.

6. **van Rensch, P., Arblaster, J., Gallant, A. J. E. & Cai, W. (2019).** "Mechanisms causing east Australian spring rainfall differences between three strong El Niño events." *Climate Dynamics* 53, 3641–3659. https://doi.org/10.1007/s00382-019-04732-1
   - Crossref-confirmed (title/authors match), but abstract text itself was not retrievable (paywalled PDF) — **[SECONDARY/UNVERIFIED]**. Directly explains why the three strong El Niño events (1982-83, 1997-98, 2015-16) produced *different* eastern-Australia spring rainfall outcomes — the key primary-literature basis for the nonlinearity caveat below, though the specific mechanisms per event could not be quoted verbatim here.

**Observed outcomes in named events:**
- **1982–83:** severe, broad SON–DJF rainfall deficit; associated with the Ash Wednesday fires.
- **1997–98:** impacts reportedly "confined to coastal southeastern Australia and Tasmania" — markedly weaker than 1982-83 and 2015-16 despite comparable El Niño strength, illustrating the event-to-event nonlinearity that van Rensch et al. (2019) set out to explain.
- **2015–16:** severe eastern rainfall deficits comparable to 1982-83.
- **2023–24:** documented DJF exception — wet, +18.9% anomaly, despite a moderate-strong El Niño and positive IOD. Per a BoM account relayed via a secondary source (Climate Council; a direct bom.gov.au fetch returned 403, so this is **[SECONDARY]**, not primary-verified), El Niño's atmospheric influence "typically weakens" by summer; SAM and anomalously warm coastal SSTs favored wet conditions; "the different phases of ENSO do not appear to influence the likelihood of thunderstorms"; and four tropical cyclones added rain that summer. This is a real, mechanistically-explained override of the ENSO dry signal by DJF, not statistical noise — it should be treated as a documented failure mode of the DJF window, not dismissed as an anomaly. **Recommend independently re-verifying this BoM account directly at bom.gov.au before publication**, since automated access was blocked this pass.

**Caveats:**
- CP vs. EP El Niño flavour differences plausibly matter for this teleconnection too (as for East Asia and the Philippines) but were not specifically confirmed for Australia in this pass.
- Liguori et al. (2022): ENSO and IOD are statistically difficult to cleanly separate, so attributing the SON signal cleanly to "IOD reinforcement of ENSO" rather than a joint/confounded signal is a simplification worth flagging.
- Every citation in this section beyond Wang/Zhang-type mechanism papers relies on search-summary paraphrase or Crossref metadata only — no publisher page in this region yielded a page I read myself; this is the weakest quote-verification coverage of the four regions and should be prioritized for a follow-up pass with authenticated journal access.

**Recommendation for the map:** Change the eastern Australia window from **"Sep–Feb"** to **"SON" (spring), or at most "SON–early DJF, declining confidence into summer."** The current "Sep–Feb" framing overstates DJF skill and is directly contradicted by the documented, mechanistically-explained 2023-24 wet DJF anomaly.

**Confidence tier: medium-high for the SON dry signal** (multiple mechanistic papers converge on the same physical picture, and the 2026 forecast configuration — El Niño plus positive IOD — is exactly the combination that maximizes this signal per Cai et al. 2011, though the exact wording of that finding is unverified paraphrase and event-to-event scatter per van Rensch et al. 2019 keeps this below "high"). **Confidence tier: low for extending the dry signal through DJF** (SAM, SST, and cyclone/thunderstorm activity are documented, mechanistically-explained overrides by summer — 2023-24 is a real documented failure case for the DJF claim, not an anomaly to explain away).

---

## Summary table

| Region | Season | Sign | Confidence tier | Key DOI |
|---|---|---|---|---|
| A. Philippines | DJF (core) extending into MAM for EP-flavor events | Dry | Medium-high (DJF) / Medium (MAM extension) | [10.1007/s00382-008-0380-z](https://doi.org/10.1007/s00382-008-0380-z) (Lyon & Camargo 2009) |
| B. Mainland SE Asia / Mekong | MAM of El Niño decay year, southern/central basin only | Dry, event-variable, weaker than La Niña side | Medium (narrow, spatially-specific claim) / Low (basin-wide, all-season claim) | [10.5194/cp-12-1889-2016](https://doi.org/10.5194/cp-12-1889-2016) (Räsänen, Lindgren & Guillaume 2016) |
| C. Southern/SE China | DJF core, MAM tail less certain | Wet | Medium-high | [10.2151/jmsj1965.74.1_49](https://doi.org/10.2151/jmsj1965.74.1_49) (Zhang, Sumi & Kimoto 1996) |
| D. Eastern Australia | SON (spring); DJF should be dropped or heavily hedged | Dry (SON), IOD-reinforced | Medium-high (SON) / Low (DJF extension) | [10.1175/2011JCLI4129.1](https://doi.org/10.1175/2011JCLI4129.1) (Cai, van Rensch, Cowan & Hendon 2011) |

---

## Overall honesty notes for the record

- All 22 distinct DOIs cited across the four regions were checked against the live Crossref API by the researching pass **and independently re-checked by the compiling pass**; title/author/year matched in every case. None were taken from memory without that check, and candidate DOIs that could not be confirmed were dropped rather than guessed.
- Genuine `[VERIFIED-PRIMARY]` (publisher/repository page fetched and read directly) status was obtained for only 4 of the ~18 key citations: Lyon & Camargo (2009, Philippines), Räsänen, Lindgren & Guillaume (2016, Mekong), Singhrattna et al. (2005, Thailand), Watanabe et al. (2022, Mekong Delta), and Zhang, Sumi & Kimoto (1996, China). Everything else is `[ABSTRACT-ONLY]`/`[SECONDARY/UNVERIFIED]` or, where no usable text was found at all, marked `NO QUOTE OBTAINED` — flagged explicitly rather than filled with a memory-based or fabricated quote. One earlier internal draft of this file had mis-tagged several search-summary paraphrases as `[ABSTRACT-ONLY]`; those have been corrected to `[SECONDARY/UNVERIFIED]` here since the researching passes reported they came from search-engine summaries, not a fetched abstract field.
- **Region B is the one place this exercise materially overturns a prior project finding.** The earlier dossier's "no peer-reviewed citation verified" conclusion was correct for the specific *event-magnitude* claims (still unverified), but this pass found real, Crossref-confirmed, on-topic peer-reviewed literature on the *general* ENSO–mainland SE Asia teleconnection. That literature itself reports the relationship as spatially uneven (southern/central basin only), nonstationary (weak pre-1980), and asymmetrically weaker for El Niño than La Niña — so the net recommendation is still to keep confidence low for any basin-wide claim, but for a more precise, literature-grounded reason than "no literature exists." If the map adds a Mekong region at all, it should be scoped narrowly (southern/central basin, MAM, decay year).
- **Region D is where the reviewer's critique is best supported.** SON is the literature-favored window; the current "Sep–Feb" label overstates DJF skill, and the 2023-24 wet DJF anomaly is a real, mechanistically-explained (SAM, warm coastal SSTs, tropical cyclone activity) counter-example, not noise.
- Weakest quote-verification coverage is Region D (Australia) — no publisher page there yielded text read directly; all supporting quotes are paraphrase-level. This should be the top priority for a follow-up pass with authenticated journal access.
- No primary-agency source (PAGASA, BoM, CMA, Mekong River Commission) was directly and successfully fetched in this pass for any of the four regions' named-event outcomes; all such figures are tagged secondary/unverified and should be spot-checked before any specific number is published.
