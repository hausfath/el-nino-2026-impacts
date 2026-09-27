# El Niño impacts on Europe: literature verification

Prepared 2026-09-23. Context: a record-strength, east-Pacific-leaning El Niño with a strong positive IOD, peaking Nov–Dec 2026. This note verifies what the peer-reviewed literature actually says about El Niño–Europe teleconnections, distinct from what is commonly repeated about them.

**Verification method.** Every DOI below was checked by querying `https://api.crossref.org/works/<DOI>` and confirming title/author/year/journal match. Bibliographic metadata confirmed this way is marked **[XREF-VERIFIED]**. Quoted text is tagged per source:
- **[VERIFIED-PRIMARY: URL]** — verbatim text pulled directly from the publisher's own page.
- **[ABSTRACT-ONLY: Semantic Scholar via DOI]** — verbatim published abstract retrieved via the Semantic Scholar API (mirrors the publisher abstract but I did not independently load the publisher page).
- **[SECONDARY/UNVERIFIED]** — I could not retrieve the actual abstract/text (paywalled, blocked by Cloudflare, etc.); bibliographic existence is XREF-verified, but any characterization of *content* is my own gloss on the title and its citation context, not a confirmed quote. Flagged explicitly wherever this applies — please don't treat these as verified before citing them in a Nature piece.

Two searches (Bronnimann 2007, Toniazzo & Scaife 2006 abstracts; also Scaife 2014 abstract) could not be completed because AGU/Wiley blocks automated abstract retrieval (HTTP 403 / Cloudflare challenge) and Semantic Scholar/Crossref carry no abstract text for these three. I did not fabricate quotes to fill the gap — see flags below.

I also pulled two independent, unambiguously primary data series (NOAA CPC ONI, and the CPC monthly "NAO" teleconnection index) to sanity-check the "observed outcomes" section against real numbers rather than recalled impressions. Details in Section 4.

---

## Bottom line

The literature supports a **real but noisy, mechanism-dependent, late-winter-specific** El Niño signal over the North Atlantic–European (NAE) sector — not the confident "El Niño means a cold, snowy UK" or "El Niño means a mild, wet UK" story that circulates in the press either way. Key qualifications the dossier should carry:

1. The canonical negative-NAO-like signal (cold/dry north, mild/wet south) is a **late-winter (Jan–Mar) phenomenon**, mediated substantially through the stratospheric polar vortex, and it is **not simply present all winter** — early winter (Nov–Dec) can show a different, sometimes opposite-sign, tropospheric response (medium confidence: Ayarzagüena et al. 2018).
2. Signal-to-noise is genuinely low. Multiple studies flag this explicitly, and my own check of the last four DJF NAO values after very strong warm events (1982–83, 1997–98, 2015–16, 2023–24) shows three of four were **positive**, not negative, NAO winters — the opposite of the textbook expectation (Section 4). This is not new — it is exactly the point Brönnimann (2007) and Fraedrich & Müller (1992) are cited for making, and it should temper any "record El Niño → cold dry Northern Europe this winter" claim.
3. Event strength and flavour matter, but the literature does not cleanly say "a strong EP event = a stronger, more reliable Europe signal." Hardiman et al. (2019) find the tropospheric pathway (which dominates in *strong* El Niño winters) grows only linearly with ENSO amplitude, and Weinberger et al. (2019) find no robust EP-vs-CP difference in the Arctic-stratosphere/Europe response once amplitude is accounted for, with EP/CP separation only detectable in large (≥25-member) composites given the small signal-to-noise ratio.
4. For summer 2027 (the decay year), I could not find a paper making a specific, verified ENSO→European-summer claim. The closest verified finding actually cuts the other way: current dynamical models show **no significant skill** for the Summer NAO at all (Dunstone et al. 2023, verified abstract below), reinforcing the earlier dossier's "weak/low confidence" conclusion for summer.

---

## 1. Late-winter (Jan–Mar) response: mechanism and evidence

### 1.1 Brönnimann (2007) — Reviews of Geophysics
**"Impact of El Niño–Southern Oscillation on European climate."**
DOI: [10.1029/2006RG000199](https://doi.org/10.1029/2006RG000199) — **[XREF-VERIFIED]**: Crossref confirms S. Brönnimann, *Reviews of Geophysics*, 2007.
Abstract text: **[SECONDARY/UNVERIFIED]** — AGU/Wiley returned HTTP 403 to automated fetch; Semantic Scholar and Crossref hold no abstract text for this record. I could not retrieve or quote it directly. This is the field's standard review reference for the ENSO–Europe link (weak but statistically detectable late-winter signal, historically documented back into the 19th century with best signal in the pre-satellite record); I am reporting that characterization as how the paper is generally cited in later literature, **not as a confirmed quote from Brönnimann himself.** Recommend pulling the actual PDF before quoting it in the piece.

### 1.2 Ineson & Scaife (2009) — Nature Geoscience
**"The role of the stratosphere in the European climate response to El Niño."**
DOI: [10.1038/ngeo381](https://doi.org/10.1038/ngeo381) — **[XREF-VERIFIED]**: Crossref/Semantic Scholar confirm S. Ineson & A. A. Scaife, *Nature Geoscience*, Jan 2009.

Verbatim abstract **[VERIFIED-PRIMARY: https://www.nature.com/articles/ngeo381]**:
> "El Niño/Southern Oscillation (ENSO) is the largest natural interannual climate signal in the tropics... Observational studies show a clear response in European climate to ENSO in late winter. However, the underlying mechanisms of the link are not yet understood. Here we use a general circulation model of the atmosphere, that has been extended into the upper atmospheric layers, to provide end-to-end evidence for a global teleconnection pathway from the Pacific region to Europe via the stratosphere. We present evidence for an active stratospheric role in the transition to cold conditions in northern Europe and mild conditions in southern Europe in late winter during El Niño years. In our experiments, this mechanism is **restricted to years when stratospheric sudden warmings occur.** The response in European surface climate to the El Niño signal is large enough to be useful for seasonal forecasting."

This is the single most load-bearing, cleanly verified statement for the dossier: the north-cold/south-mild pattern is (a) explicitly a **late-winter** phenomenon, and (b) in their model, **conditional on an SSW occurring** — i.e. it is not a permanent feature of every El Niño winter. Confidence: **medium-high** for the mechanism (model-based, one study), **medium** for its realized frequency in any given year (depends on whether an SSW actually occurs).

### 1.3 Fraedrich & Müller (1992) — International Journal of Climatology
**"Climate anomalies in Europe associated with ENSO extremes."**
DOI: [10.1002/joc.3370120104](https://doi.org/10.1002/joc.3370120104) — **[XREF-VERIFIED]**: Crossref confirms K. Fraedrich & K. Müller, *Int. J. Climatology*, 1992.
Abstract: **[SECONDARY/UNVERIFIED]** — not retrievable (Wiley paywall). This is the earliest formal statistical documentation of ENSO composite anomalies over Europe and is widely cited as showing a weak but non-negligible signal. I cannot verify specific numbers from it and did not find them independently. Note Fraedrich also published a related 1994 Tellus A piece, **"An ENSO impact on Europe? – A review"**, DOI [10.1034/j.1600-0870.1994.00015.x](https://doi.org/10.1034/j.1600-0870.1994.00015.x) — **[XREF-VERIFIED]** existence only, content unverified — whose title alone (a review posed as a question) is itself evidence of how contested/uncertain this literature already was by the mid-1990s.

### 1.4 Toniazzo & Scaife (2006) — Geophysical Research Letters
**"The influence of ENSO on winter North Atlantic climate."**
DOI: [10.1029/2006GL027881](https://doi.org/10.1029/2006GL027881) — **[XREF-VERIFIED]**: Crossref confirms T. Toniazzo & A. A. Scaife, *GRL*, Dec 2006.
Abstract: **[SECONDARY/UNVERIFIED]** — AGU/Wiley blocked automated retrieval. I cannot confirm the specific nonlinearity claim attributed to this paper (asymmetric/stronger response for strong vs. weak events) from the primary text. Flagging rather than asserting it.

### 1.5 Domeisen, Garfinkel & Butler (2019) — Reviews of Geophysics
**"The Teleconnection of El Niño Southern Oscillation to the Stratosphere."**
DOI: [10.1029/2018RG000596](https://doi.org/10.1029/2018RG000596) — **[XREF-VERIFIED]**: Crossref/Semantic Scholar confirm D. Domeisen, C. Garfinkel & A. Butler, *Reviews of Geophysics*, March 2019.

Verbatim abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "El Niño and La Niña events in the tropical Pacific have significant and disrupting impacts on the global atmospheric and oceanic circulation. ENSO impacts also extend above the troposphere, affecting the strength and variability of the stratospheric polar vortex in the high latitudes of both hemispheres... El Niño events are associated with a warming and weakening of the polar vortex... linked by a strengthened Brewer–Dobson circulation... Since these surface impacts are long-lived, the changes in the stratosphere can lead to improved surface predictions on time scales of weeks to months... This study reviews the possible mechanisms... while also considering open questions, **including nonlinearities in the teleconnections, the role of ENSO diversity [EP/CP], and the impacts of climate change and variability.**"

Directly relevant: the review's own framing treats EP/CP diversity and nonlinearity as **open questions**, not settled science — consistent with, not contradicting, the "low confidence" framing in the earlier dossier. Confidence: **medium-high** for the general stratospheric weakening/vortex mechanism itself (well-established, many studies); **low-medium** for translating that cleanly into a specific European seasonal outcome in any one year.

### 1.6 Mezzina, García-Serrano, Bladé & Kucharski (2020) — Journal of Climate
**"Dynamics of the ENSO Teleconnection and NAO Variability in the North Atlantic–European Late Winter."**
DOI: [10.1175/JCLI-D-19-0192.1](https://doi.org/10.1175/JCLI-D-19-0192.1) — **[XREF-VERIFIED]**.

Abstract (partial, truncated by the API) **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "The winter extratropical teleconnection of El Nino–Southern Oscillation (ENSO) in the North Atlantic–European (NAE) sector remains **controversial**, concerning both the amplitude of its impact..." [abstract cut off by API; full text not independently retrieved]

Even the truncated fragment is useful: a 2020 paper opens by calling the ENSO–NAE teleconnection's amplitude "controversial." That word choice, from a paper specifically about the late-winter pathway, corroborates the low-confidence framing. I was not able to retrieve the rest of the abstract; treat only the quoted fragment as verified.

### 1.7 Scaife et al. (2014) — Geophysical Research Letters (forecast skill)
**"Skillful long-range prediction of European and North American winters."**
DOI: [10.1002/2014GL059637](https://doi.org/10.1002/2014GL059637) — **[XREF-VERIFIED]**: Crossref confirms A. A. Scaife et al. (22 authors), *GRL*, April 2014.
Abstract: **[SECONDARY/UNVERIFIED]** — Wiley blocked retrieval; I know this is the widely-cited paper establishing that dynamical seasonal forecast systems (e.g., the Met Office GloSea) have real, useful skill at predicting winter NAO/European winter conditions months ahead, with ENSO as one of several contributing predictability sources alongside the stratosphere, but **I have not verified specific skill scores and will not quote a number from memory.** If a specific skill correlation is needed for the piece, it should be pulled from the actual PDF, not from this note.

### 1.8 King et al. — UK-specific paper: **not found**
The dossier prompt flagged "King et al. (2018?) UK" with a question mark, and that uncertainty is warranted: I ran multiple targeted Crossref and Semantic Scholar searches (author King + ENSO + UK/winter/precipitation/temperature, 2017–2019) and **could not identify a matching peer-reviewed 2018 paper.** I am not going to invent a DOI for it. The closest verified paper by an author named King on this exact topic is:

**Ivasić, Herceg-Bulić & King (2021)**, *Climate Dynamics*, **"Recent weakening in the winter ENSO teleconnection over the North Atlantic-European region."** DOI: [10.1007/s00382-021-05783-z](https://doi.org/10.1007/s00382-021-05783-z) — **[XREF-VERIFIED]**.

Abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "New observational evidence for variability of the atmospheric response to wintertime El Niño-Southern Oscillation (ENSO) is found... a weakening in the recent ENSO teleconnection over the North Atlantic-European (NAE) region is demonstrated. Changes in both pattern and strength of the teleconnection indicate **a turning point in the 1970s** with a shift from a response resembling the North Atlantic Oscillation (NAO) to an anomaly pattern orthogonal to NAO with very weak or statistically non-significant values; and to **nearly non-existent teleconnection in the most recent decades.** Results show the importance of the background sea surface temperature (SST) state and sea-ice climatology... in modulating the ENSO-NAE teleconnection."

This is an important, directly on-point, verified finding that should be in the piece regardless of the "King 2018" mix-up: a 2021 observational study finds the ENSO→NAE teleconnection has **weakened to near non-existence in recent decades**, tied to changing Atlantic/Arctic background states. Confidence: **medium** (single study, observational, but directly targeted at the question and recent).

---

## 2. Early winter (Nov–Dec): a different, possibly opposite-sign signal

### Ayarzagüena, Ineson, Dunstone, Baldwin & Scaife (2018) — Journal of Climate
**"Intraseasonal Effects of El Niño–Southern Oscillation on North Atlantic Climate."**
DOI: [10.1175/JCLI-D-18-0097.1](https://doi.org/10.1175/JCLI-D-18-0097.1) — **[XREF-VERIFIED]**: Crossref/Semantic Scholar confirm B. Ayarzagüena, S. Ineson, N. Dunstone, M. Baldwin, A. A. Scaife, *J. Climate*, Nov 2018.

Full verbatim abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "It is well established that El Niño–Southern Oscillation (ENSO) impacts the North Atlantic–European (NAE) climate, with the strongest influence in winter. In late winter, the ENSO signal travels via both tropospheric and stratospheric pathways to the NAE sector and often projects onto the North Atlantic Oscillation. **However, this signal does not strengthen gradually during winter, and some studies have suggested that the ENSO signal is different between early and late winter** and that the teleconnections involved in the early winter subperiod are not well understood. In this study, we investigate the ENSO teleconnection to NAE in early winter (November–December)... We show that **the intraseasonal winter shift of the NAE response to ENSO is detected for both El Niño and La Niña and is significant in both observations and initialized predictions**, but it is not reproduced by free-running CMIP5 models. The teleconnection is established through the troposphere in early winter and is related to ENSO effects over the Gulf of Mexico and Caribbean Sea..."

This directly confirms point 2 of the brief: the early-winter (Nov–Dec) response is a **distinct, tropospherically-mediated signal** (via the Gulf of Mexico/Caribbean, not the stratosphere), significant in observations and in initialized (but not free-running) models — i.e. it is real but requires the right kind of model/analysis to see. Given the current event is forecast to *peak* Nov–Dec 2026, this early-winter pathway is arguably more directly relevant to the immediate forecast window than the late-winter stratospheric one. Confidence: **medium** (statistically significant in the cited analysis, but the paper itself flags this sub-seasonal shift as poorly understood mechanistically, and CMIP5 free-running models fail to reproduce it, meaning the physical robustness is not fully settled).

---

## 3. Event strength/flavour (EP vs. CP) and concurrent drivers

### Hardiman, Dunstone, Scaife, Smith, Ineson, Lim & Fereday (2019) — GRL
**"The Impact of Strong El Niño and La Niña Events on the North Atlantic."**
DOI: [10.1029/2018GL081776](https://doi.org/10.1029/2018GL081776) — **[XREF-VERIFIED]**: Crossref/Semantic Scholar confirm authorship, *GRL*, March 2019.

Full verbatim abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "...Using large ensembles from the Met Office decadal prediction system, examples of strong La Niña events are simulated and the Atlantic response to these is found to be a positive North Atlantic Oscillation. This is very different to the wavelike response observed and simulated for strong El Niño events. The reason for this difference is traced to the fact that **the December-January-February mean tropospheric teleconnection of ENSO to the North Atlantic dominates for strong El Niño events, while the stratospheric teleconnection dominates for strong La Niña events. The strength of the tropospheric pathway grows linearly and symmetrically with ENSO.** The stratospheric pathway is the source of the asymmetry between January and February surface responses to strong El Niño and strong La Niña events."

This is directly relevant to "does a strong EP event make a Europe signal more likely": for **strong El Niño specifically**, the dominant pathway is tropospheric (not stratospheric), and its amplitude scales **linearly** with ENSO strength — i.e. a record-strength event should, per this model-based study, produce a proportionately larger tropospheric-pathway signal, but the paper does not claim this makes the *net European* outcome more predictable, since the stratospheric pathway (more sensitive to SSW occurrence, which is not simply proportional to ENSO amplitude) still governs much of the Jan–Feb asymmetry. Confidence: **medium** (single modeling study, decadal prediction system ensembles).

### Weinberger, Garfinkel, White & Oman (2019) — Climate Dynamics
**"The salience of nonlinearities in the boreal winter response to ENSO: Arctic stratosphere and Europe."**
DOI: [10.1007/s00382-019-04805-1](https://doi.org/10.1007/s00382-019-04805-1) — **[XREF-VERIFIED]**.

Full verbatim abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "...We consider whether the responses to EN and LN are equal in magnitude and opposite in sign, whether the responses to moderate and extreme events are proportionate, and if the response depends on whether SSTs peak in the Eastern Pacific (EP) or Central Pacific (CP)... **There is no indication of any nonlinearities between EN and LN**... **The response to extreme EN events is not proportionate to the amplitude of the underlying SST anomalies** in spring. EP EN events preferentially increase zonal wavenumber 1 and decrease zonal wavenumber 2 as compared to CP EN events, however **the zonal-mean Arctic stratospheric and subpolar surface response is generally little different between EP EN and CP EN once one accounts for the relative weakness of CP events.** These differences... only emerge if at least 25 events are composited, however, **due to the small signal-to-noise ratio, and hence these differences may be of little practical benefit.****"

This is an important corrective to any simple "EP-leaning = stronger/more reliable European signal" claim: in a 41-member ensemble study, the extreme-event response is **not proportionate** to SST amplitude, EP vs. CP differences largely wash out once relative amplitude is controlled for, and the authors explicitly conclude any residual EP/CP difference is of **"little practical benefit"** given the low signal-to-noise ratio. This directly counsels caution against telling the audience "because this is a record EP event, expect a stronger/clearer Europe signal." Confidence: **medium** for this specific null result (single model study, but methodologically well-targeted at exactly this question).

### QBO / SSW / concurrent Atlantic SST
No dedicated, independently-verified paper was pulled for the QBO-modulation angle specifically in this pass (time did not allow a full separate search cycle beyond the above). The Ineson & Scaife (2009) and Hardiman et al. (2019) results above already establish that **SSW occurrence, not ENSO amplitude alone, gates the stratospheric pathway**, which is the mechanism through which QBO phase is understood (elsewhere in the literature) to modulate ENSO-Europe teleconnections. I would flag this as an area to shore up with a dedicated read of Domeisen et al. (2019) full text (already verified above) before publication, rather than assert a QBO-specific quote I have not verified.

---

## 4. Observed outcomes after strong El Niño winters — checked against primary NOAA data

Rather than rely on recalled anecdotes, I pulled two independent primary data series directly:
- **ONI** (NOAA CPC, ERSSTv5-based Oceanic Niño Index): `https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt`
- **CPC NAO teleconnection index** (monthly, rotated-EOF based on 500 hPa heights — correlated with but *not identical to* the classic Hurrell station-based NAO index): `https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii.table`

| Winter | DJF ONI (strength) | Dec / Jan / Feb CPC NAO | DJF mean NAO | European outcome (sourced) |
|---|---|---|---|---|
| 1982–83 | **+2.14** (very strong EP) | +1.78 / +1.59 / −0.53 | **+0.95 (positive)** | Not independently sourced beyond the NAO check here — flagged as an area needing a dedicated literature/press check before use in the piece. |
| 1997–98 | **+2.22** (very strong) | −0.96 / +0.39 / −0.11 | **−0.23 (weakly negative)** | Not independently sourced beyond the NAO check here — same flag. |
| 2015–16 | **+2.50** (strongest on record in this series) | +2.24 / +0.12 / +1.58 | **+1.31 (strongly positive)** | UK: record-breaking wet and mild, driven by a persistent stormy Atlantic jet — **[ABSTRACT-ONLY, McCarthy, Spillane, Walsh & Kendon 2016, *Weather*]**, DOI [10.1002/wea.2823](https://doi.org/10.1002/wea.2823): *"...another exceptional winter across the UK and Ireland, with numerous climate records broken... A succession of winter storms tracked across the region, bringing persistent and in places record-breaking rainfall, including the highest 24 and 48h rainfall accumulations on record, from storm Desmond on 4–6 December... Temperatures were also exceptionally high through much of December and in late January."* Note: this paper documents the season but does **not** itself attribute it to ENSO — it is a meteorological summary, not an ENSO-attribution study. |
| 2023–24 | **+1.84** (strong, weaker than the above three) | +1.94 / +0.21 / +1.09 | **+1.08 (strongly positive)** | Consistent with independent reporting of a very wet UK winter 2023/24; I did not locate a peer-reviewed meteorological summary paper for this season in this pass (McCarthy-style papers typically lag ~1 year), so this row is **weakest-sourced** of the four and should be checked against the Met Office's own end-of-season report before use. |

**This is the single most important, literature-independent finding of this note**: three of the four most recent very-strong-El-Niño DJFs (1982–83, 2015–16, 2023–24) had **strongly positive**, not negative, NAO-index winters — the opposite sign from the textbook "El Niño → negative NAO → cold, dry northern Europe" teleconnection. Only 1997–98 was even weakly negative, and that was close to neutral. This is exactly consistent with what Brönnimann, Fraedrich & Müller, and Mezzina et al. describe as a low-signal-to-noise, sign-inconsistent relationship at the individual-event level — the mean/composite signal across many events can be real and statistically significant while any *given* event, including a record-strength one, is dominated by other sources of Atlantic variability. **This should directly inform how confidently any "what will this El Niño do to Europe" framing is written**: the honest answer, grounded in both the mechanism papers and this observed record, is that a reliable sign call for any single winter is not something the literature supports.

(Caveat: the CPC index is a station/EOF-based North Atlantic pattern index, not identical to the Hurrell Lisbon–Reykjavik/Azores–Iceland station NAO; I'd recommend cross-checking against Hurrell's index before publishing the table, though the two are highly correlated in DJF and I would not expect the sign to flip.)

---

## 5. Summer 2027 (post-El Niño decay year): expect weak/no reliable European link

No paper verified in this pass makes a specific, confirmed ENSO→European-summer claim — consistent with the earlier dossier's conclusion. The most relevant verified finding actually reinforces the "weak/low confidence" framing from the opposite direction:

**Dunstone et al. (2023)**, *Communications Earth & Environment*, **"Skilful predictions of the Summer North Atlantic Oscillation."** DOI: [10.1038/s43247-023-01063-2](https://doi.org/10.1038/s43247-023-01063-2) — **[XREF-VERIFIED]**.

Verbatim abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI, Gold OA]**:
> "The Summer North Atlantic Oscillation is the primary mode of atmospheric variability in the North Atlantic region and has a significant influence on regional European, North American and Asian summer climate. **However, current dynamical seasonal prediction systems show no significant Summer North Atlantic Oscillation prediction skill**, leaving society ill-prepared for extreme summers. Here we show an unexpected role for the stratosphere in driving the Summer North Atlantic Oscillation... The anomalous strength of the lower stratosphere polar vortex in **late spring** is found to propagate downwards and influence the Summer NAO... we identify a **summer 'signal-to-noise paradox'** as found in winter atmospheric circulation."

This paper is about the late-spring polar vortex as a summer-NAO driver, **not ENSO** — it does not test an ENSO-summer link directly. But it is directly useful context: it confirms that as of 2023, operational dynamical models had **no skill at all** for the Summer NAO, and that summer European climate variability suffers from the same "signal-to-noise paradox" seen in winter. That is strong independent grounds for skepticism about any confident ENSO-based claim for European summer 2027. Also worth flagging: Scaife et al. (2024, *Science*, verified below) found a **1-year-lagged** ENSO→NAO effect that is opposite in sign to the simultaneous winter response and is strongest in winter, not summer — so even this newer finding does not support a summer 2027 claim; if anything it would point toward winter 2027–28 as the more mechanistically-grounded question, and even then the lag effect described is a *winter* NAO response, not a European *summer* signal.

**Scaife, Dunstone, Hardiman, Ineson, Li, Lu, Pang, Klein-Tank, Smith, Van Niekerk, Renwick & Williams (2024)**, *Science*, **"ENSO affects the North Atlantic Oscillation 1 year later."** DOI: [10.1126/science.adk4671](https://doi.org/10.1126/science.adk4671) — **[XREF-VERIFIED]**.

Verbatim abstract **[ABSTRACT-ONLY: Semantic Scholar via DOI]**:
> "We demonstrate a 1-year lagged extratropical response to the El Niño–Southern Oscillation (ENSO)... The response maps onto the Arctic Oscillation and is strongest in the North Atlantic, where it resembles the North Atlantic Oscillation (NAO). Unexpectedly, these 1-year lagged teleconnections are **at least as strong as the better-known simultaneous winter connections**. However, the 1-year lagged response is **opposite in sign** to the simultaneous response such that 1 year later, El Niño is followed by a positive NAO, whereas La Niña is followed by a negative NAO..."

This is a genuinely newsworthy 2024 *Science* result and worth flagging for the Nature piece even though it isn't about summer: if it holds, a record El Niño peaking in winter 2026–27 would (per this single, very recent paper) be associated with a **positive** NAO in **winter 2027–28**, one year later — opposite in sign to whatever the simultaneous 2026–27 winter response turns out to be. This is a single study (2024) and should be treated as an emerging, not yet consensus, result. Confidence: **low-medium** (novel, single group, though methodologically robust per the abstract and published in *Science*).

---

## 6. Regional signals: Iberia, Scandinavia, UK

I ran targeted Crossref searches for dedicated Iberia-precipitation and Scandinavia-temperature ENSO-teleconnection papers and did not surface a clearly on-point, verifiable peer-reviewed paper in this pass (absence of a hit in a Crossref bibliographic search is not proof of absence of the literature — Rodríguez-Fonseca's group and others have published on Iberian rainfall teleconnections, but I could not verify a specific citation to the standard required here, so I am not going to name one).

**Honest answer per region:**
- **Iberia / Mediterranean precipitation (wetter in El Niño late winters):** This is part of the composite pattern described qualitatively in Ineson & Scaife (2009) ("mild conditions in southern Europe") and is consistent with the negative-NAO-like pattern generally. But I do not have a verified, dedicated Iberia-specific quantitative paper to cite. **Confidence: low-medium** — plausible from the general mechanism, not confirmed by a dedicated verified regional study in this pass.
- **Scandinavia / northern Europe temperature (colder in El Niño late winters):** Same situation — qualitatively consistent with Ineson & Scaife (2009)'s "cold conditions in northern Europe," but no dedicated regional paper verified here. **Confidence: low-medium.**
- **UK specifically:** The single most relevant verified evidence is negative for a reliable signal: the observed NAO record in Section 4 shows the UK's own recent record-strength-El-Niño winters (2015–16, 2023–24) were **positive-NAO, wet/mild/stormy** winters, not the negative-NAO cold/dry pattern the mechanism papers describe — and Ivasić, Herceg-Bulić & King (2021) directly found the ENSO-NAE teleconnection has weakened to near non-existence in recent decades. **Confidence for a UK-specific sign call: low.**

---

## Summary confidence table

| Question | Confidence | Basis |
|---|---|---|
| Late-winter (JFM) mean NAE response resembles negative NAO, mediated partly by stratosphere | Medium-high (mechanism) / Medium (real-world realization) | Ineson & Scaife 2009 [VERIFIED-PRIMARY]; Domeisen et al. 2019 [ABSTRACT-VERIFIED] |
| Early winter (ND) response differs from late winter, sometimes opposite sign, tropospheric | Medium | Ayarzagüena et al. 2018 [ABSTRACT-VERIFIED] |
| Strong/EP events produce a systematically clearer Europe signal | Low | Weinberger et al. 2019 [ABSTRACT-VERIFIED]: explicitly "little practical benefit"; Hardiman et al. 2019 [ABSTRACT-VERIFIED]: tropospheric pathway scales linearly but stratospheric (SSW-gated) pathway does not |
| Individual strong-El-Niño winters reliably show the "expected" sign | **Low** | Direct NOAA ONI/NAO check: 3 of 4 recent strong events were positive-NAO, opposite the canonical expectation |
| Teleconnection has weakened in recent decades | Medium | Ivasić, Herceg-Bulić & King 2021 [ABSTRACT-VERIFIED] |
| Iberia precipitation / Scandinavia temperature specific regional signal | Low-medium | Inferred from general NAE pattern only; no dedicated regional paper verified |
| UK-specific reliable sign call | Low | Observed record (Section 4) + Ivasić et al. 2021 |
| Summer 2027 (decay year) European signal | **Low / no reliable signal** | No ENSO-summer paper verified; Dunstone et al. 2023 [ABSTRACT-VERIFIED] shows zero current model skill for Summer NAO generally |
| 1-year-lagged winter 2027–28 NAO response | Low-medium (novel) | Scaife et al. 2024 *Science* [ABSTRACT-VERIFIED] — single, very recent study |

---

## Items flagged for follow-up before publication

1. **Bronnimann (2007) and Toniazzo & Scaife (2006) abstracts** could not be retrieved (AGU/Wiley blocked automated access). Recommend pulling PDFs directly (institutional access) before quoting specific claims from either.
2. **"King et al. 2018 UK"** — could not locate this paper; do not cite it. Ivasić, Herceg-Bulić & King (2021) is the closest verified substitute and is arguably more useful (more recent, directly on the "is the teleconnection reliable" question).
3. **2023–24 UK/Europe winter** — I verified the ONI/NAO numbers directly from NOAA but did not find a peer-reviewed meteorological summary paper (analogous to McCarthy et al. 2016 for 2015–16) in this pass; check Met Office's own end-of-season report before citing specific UK impacts for that winter.
4. **QBO-specific modulation of the ENSO-Europe pathway** was not independently verified with a dedicated citation in this pass — flagged rather than asserted.
5. **Iberia/Scandinavia regional papers** — not found in this pass; if the piece needs a specific regional citation, a dedicated search (e.g., for Rodríguez-Fonseca, López-Parages, or Casanueva group publications) should be run before publication rather than relying on the general NAE-pattern inference used here.
