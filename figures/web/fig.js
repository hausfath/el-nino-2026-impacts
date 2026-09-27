/* Blog figures in the dashboard style. ?fig=<name>&theme=dark|light. Every number comes from
   /elnino_map/data (the live dashboard bundle) or figdata.json (export_figdata.py). */
'use strict';
(async () => {
  const FIGN = Q.get('fig'), E = Engine;
  const j = (u) => fetch(u).then((r) => { if (!r.ok) throw new Error(u); return r.json(); });
  const [geo, regs, meta, D] = await Promise.all([j('/elnino_map/data/geo.json'), j('/elnino_map/data/regions.json'), j('/elnino_map/data/meta.json'), j('figdata.json')]);
  await Promise.all(["700 20px 'Bricolage Grotesque'", "600 20px 'Bricolage Grotesque'", "400 14px 'IBM Plex Sans'", "600 14px 'IBM Plex Sans'", "500 12px 'IBM Plex Mono'", "600 12px 'IBM Plex Mono'"].map((f) => document.fonts.load(f)));
  E.setGeo(geo); E.setRegions(regs);
  const REG = E.REG, XREG = E.XREG, FIG = document.getElementById('fig');
  const css = (k) => getComputedStyle(document.documentElement).getPropertyValue(k).trim();
  const H = (s) => { const t = document.createElement('template'); t.innerHTML = s.trim(); return t.content.firstChild; };
  const add = (s) => FIG.appendChild(H(s));
  const px = (v) => `${Math.round(v)}px`;
  const S = D.stats, NEV = S.strong.length, NMOD = meta.seasons.OND.n;
  const pct = Math.round(100 * S.aggregate.hits / S.aggregate.n);
  const p27 = [S.p2027.ONI, S.p2027.RONI].map((v) => Math.round(100 * v)).sort((a, b) => a - b);
  const p27s = p27[0] === p27[1] ? `${p27[0]}%` : `${p27[0]}–${p27[1]}%`;
  const kindOfR = (R) => R.kind ?? 'dry';
  const mcls = (k) => ({ dry: 'md', wet: 'mw', warm: 'mt' }[k] ?? 'mx');

  function frame(w, h) { FIG.style.width = px(w); FIG.style.height = px(h); }
  function head(kicker, title, sub) {
    add(`<div class="f-head"><div class="f-kicker">${kicker}</div><div class="f-title">${title}</div><p class="f-sub">${sub}</p></div>`);
  }
  function credit(extra = '') {
    add(`<div class="f-credit">Z. Hausfather · The Climate Brink${extra} · interactive: dashboard.theclimatebrink.com/#impacts</div>`);
  }
  function mapCanvas(x, y, w, h, parent = FIG) {
    const c = document.createElement('canvas'); c.style.left = px(x); c.style.top = px(y); c.style.width = px(w); c.style.height = px(h);
    parent.appendChild(c); E.init(c); return c;
  }
  const fillA = () => (document.documentElement.dataset.theme === 'light' ? 0.82 : 0.78);
  function drawRegions(keys = null) {
    const list = Object.entries(REG).filter(([k]) => !keys || keys.includes(k)).map(([, R]) => ({ R, a: 1, fillA: fillA(), hi: 0, edgeA: 0.95, lw: 1.4 }));
    E.draw({ season: null, fieldA: 0, dotsA: 0, sstA: 0, regions: list });
  }
  // position of (lon, lat) inside the figure
  const at = (cv, lon, lat) => { const [x, y] = E.P(lon, lat); return [cv.offsetLeft + x, cv.offsetTop + y]; };
  // leader lines from map points to label boxes
  const svg = () => FIG.querySelector('#lead') ?? FIG.appendChild(H(`<svg id="lead" xmlns="http://www.w3.org/2000/svg"></svg>`));
  function leader(p, el, cls = '') {
    const r = el.getBoundingClientRect(), f = FIG.getBoundingClientRect();
    const L = r.left - f.left, T = r.top - f.top, R = L + r.width, B = T + r.height;
    const inside = p[0] > L && p[0] < R && p[1] > T && p[1] < B;
    const q = [clamp(p[0], L, R), clamp(p[1], T, B)];
    const s = svg();
    if (!inside && Math.hypot(q[0] - p[0], q[1] - p[1]) > 8) s.insertAdjacentHTML('beforeend', `<line class="${cls}" x1="${p[0]}" y1="${p[1]}" x2="${q[0]}" y2="${q[1]}"/>`);
    s.insertAdjacentHTML('beforeend', `<circle cx="${p[0]}" cy="${p[1]}" r="3.4"/>`);
  }
  // place an element with its left/right/centre edge at (x, y), vertically centred
  function place(el, x, y, al) {
    const w = el.offsetWidth, h = el.offsetHeight;
    el.style.left = px(al === 'l' ? x : al === 'r' ? x - w : x - w / 2); el.style.top = px(y - h / 2);
  }
  function models(k) {
    const m = D.models[k];
    if (!m) return null;
    return m;
  }
  const CK = '<svg class="ck" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 6.4l2.6 2.6L10 3.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  // push overlapping boxes apart (mostly vertically, so each label stays near its anchor), inside [x0, x1] × [y0, y1]
  function declutter(els, x0, y0, x1, y1, gap = 5) {
    const B = els.map((el) => ({ el, x: el.offsetLeft, y: el.offsetTop, w: el.offsetWidth, h: el.offsetHeight }));
    for (let it = 0; it < 400; it++) {
      let moved = false;
      for (let a = 0; a < B.length; a++) for (let b = a + 1; b < B.length; b++) {
        const p = B[a], q = B[b];
        const ox = Math.min(p.x + p.w, q.x + q.w) + gap - Math.max(p.x, q.x), oy = Math.min(p.y + p.h, q.y + q.h) + gap - Math.max(p.y, q.y);
        if (ox <= 0 || oy <= 0) continue;
        moved = true;
        if (oy <= ox * 1.6) { const d = oy / 2 + 0.5, s = p.y + p.h / 2 < q.y + q.h / 2 ? -1 : 1; p.y += s * d; q.y -= s * d; }
        else { const d = ox / 2 + 0.5, s = p.x + p.w / 2 < q.x + q.w / 2 ? -1 : 1; p.x += s * d; q.x -= s * d; }
      }
      for (const r of B) { r.x = clamp(r.x, x0, x1 - r.w); r.y = clamp(r.y, y0, y1 - r.h); }
      if (!moved) break;
    }
    for (const r of B) { r.el.style.left = px(r.x); r.el.style.top = px(r.y); }
  }
  function numsLine(k) {
    const R = REG[k], h = R.hits, m = models(k), kd = kindOfR(R);
    const mm = m ? `<span class="${mcls(kd)}">${m.agree}/${m.n}${m.dagger ? '†' : ''} models</span>` : '<span class="mx">no forecast yet</span>';
    return `<span class="h">${CK}${h.hits}/${h.n} past</span>${mm}`;
  }
  function legendRow(y, extra = []) {
    const sw = (k, c) => `<i class="sw" style="background:${TIER[k][c]}"></i>`;
    const items = [
      `<span class="lgp"><span class="lh">Drier</span>${sw('dry', 'high')}${sw('dry', 'medhigh')}${sw('dry', 'medium')}</span>`,
      `<span class="lgp"><span class="lh">Wetter</span>${sw('wet', 'high')}${sw('wet', 'medhigh')}${sw('wet', 'medium')}</span>`,
      `<span class="lgp">high → medium confidence</span>`,
      `<span class="lgp"><i class="dash"></i>underperformed in a recent strong event</span>`, ...extra];
    add(`<div class="f-legend" style="top:${px(y)}">${items.join('<span class="sep"></span>')}</div>`);
  }

  // ================================================================= global map
  function globalMap() {
    const W = 1600, Hh = 930; frame(W, Hh);
    head('El Niño 2026–27 · impacts outlook', 'Where the biggest impacts are expected',
      `Shading shows confidence from the teleconnection literature and the observed record. Each label gives how many of the <b>${NEV} strong El Niños since ${S.strong[0]}</b> went the expected way <span style="white-space:nowrap">(${CK}past)</span> and how many of this year's <b>${NMOD} seasonal forecast models</b> agree (NMME + Copernicus C3S, ${S.init} start).`);
    const MT = 150, MH = 610, cv = mapCanvas(0, MT, W, MH);
    Object.assign(E.CAM, { lon: 172, lat: 8, s: E.minS() }); E.constrain();
    drawRegions();
    const els = [], leads = [];
    // positions from make_impacts_map.py, except where these taller labels need room (Hawaii would cover its own region)
    const OVR = { hawaii: { lon: 184, lat: 21, align: 'r' } };
    for (const [k, L0] of Object.entries(D.labels)) {
      const R = REG[k]; if (!R) continue;
      const L = { ...L0, ...(OVR[k] ?? {}) };
      const kd = kindOfR(R);
      const el = add(`<div class="lbl al-${L.align}"><i class="rb" style="background:var(--${kd === 'warm' ? 'warm' : kd})"></i><div class="t">${L.title.replace(/\n/g, '<br>')}</div><div class="d">${L.detail.replace(/\n/g, '<br>')}</div><div class="n">${numsLine(k)}</div></div>`);
      el.style.paddingLeft = L.align === 'r' ? '8px' : '11px'; if (L.align === 'r') el.style.paddingRight = '11px';
      const [x, y] = at(cv, L.lon > 180 ? L.lon - 360 : L.lon, L.lat);
      place(el, x, y, L.align);
      const lp = L.lead ?? R.lp;
      els.push(el); leads.push([lp, el]);
    }
    declutter(els, 8, MT + 4, W - 8, MT + MH - 4);
    for (const [lp, el] of leads) leader(at(cv, lp[0], lp[1]), el);
    legendRow(778, [`<span class="lgp"><i class="sw" style="background:${TIER.warm.medium}"></i>warm winter</span>`,
      `<span class="lgp">† region drawn where this year's models agree, so its model count is high by construction</span>`]);
    add(`<div class="gstrip" style="top:812px">
      <div><b>${p27s}</b>chance 2027 is the warmest year on record</div>
      <div><b>CO₂</b>growth well above trend</div>
      <div><b>Coral reefs</b>widespread bleaching risk</div>
      <div><b>Crops</b>risk of crop failures in several breadbaskets at once</div></div>`);
    credit(' · basemap: Natural Earth');
  }

  // ================================================================= regional close-ups
  const CARD_DETAIL = { horn: 'heavy short rains, floods · Oct–Dec', safrica: 'drought · Dec–Feb · maize', amazon: 'drought + fire · now–May', sesa: 'heavy rain, floods · Sep–Feb' };
  // camera that fits bb exactly into a w × h canvas
  function fitCam(bb, w, h) {
    const lat = (bb[1] + bb[3]) / 2, cosf = Math.cos(clamp(lat, -50, 50) * 0.75 * DEG);
    return { lon: (bb[0] + bb[2]) / 2, lat, s: Math.min(w / ((bb[2] - bb[0]) * cosf), h / (bb[3] - bb[1])) };
  }
  function card(k, lon, lat, al, cv, noLead = false) {
    const R = REG[k], L = D.labels[k], kd = kindOfR(R), h = R.hits, m = models(k);
    const since = h.n === NEV ? 'past El Niños' : `El Niños since ${h.events.find((e) => e.pct_normal !== null).year}`;
    const mm = m ? `<div class="m"><b>${m.agree}</b><span>/${m.n}${m.dagger ? '†' : ''}</span><small>models agree</small></div>`
      : '<div class="m na"><b>—</b><small>beyond forecast range</small></div>';
    const det = (CARD_DETAIL[k] ?? L.detail).replace(/\n/g, ' · ');
    const el = add(`<div class="mc ${kd}${R.dashed ? ' dashed' : ''}"><div class="mc-k">${det}</div><div class="mc-t">${L.title.replace(/\n/g, ' ')}</div>
      <div class="mc-n"><div class="h"><b>${h.hits}</b><span>/${h.n}</span><small>${since}</small></div>${mm}</div></div>`);
    const [x, y] = at(cv, lon, lat); place(el, x, y, al);
    const lp = L.lead && !(k === 'inlandnw') ? L.lead : R.lp;
    el._lead = noLead ? null : at(cv, lp[0], lp[1]);
    return el;
  }
  function note(cv, pt, pos, text) {
    const el = add(`<div class="note">${text}</div>`);
    const [x, y] = at(cv, pos[0], pos[1]); place(el, x, y, 'c');
    el._lead = at(cv, pt[0], pt[1]);
    return el;
  }
  const RSUB = `Shading shows confidence from the literature and the observed record. Each card gives how many of the <b>${NEV} strong El Niños since ${S.strong[0]}</b> went the expected way and how many of this year's <b>${NMOD} seasonal forecast models</b> agree (NMME + Copernicus C3S, ${S.init} start; 6 NMME models for Mar–May).`;
  const REGIONAL = {
    indo_pacific: { w: 1500, h: 1000, title: 'Asia, Australia and the Pacific', bb: [66, -44, 232, 40], mapTop: 150, mapH: 690,
      cards: { maritime: [92, -24, 'c'], philippines: [150, 15, 'l'], mekong: [70, 19, 'l'], schina: [125, 28, 'l'], yangtze: [152, 37, 'l'],
        srilanka: [68, -4, 'l'], seaustralia: [118, -40, 'c'], wpacific: [178, -34, 'c'], cpacific: [212, -22, 'c'], hawaii: [205, 30, 'c'] },
      notes: [{ pt: [79, 28], pos: [74, 37.5], text: D.footers.india_note }], footer: D.footers.indo_pacific },
    africa: { w: 1100, h: 1080, title: 'Africa', bb: [-20, -37, 64, 26], mapTop: 150, mapH: 760,
      cards: { horn: [60, 18, 'l'], safrica: [38, -30, 'l'] },
      notes: [{ pt: [0, 14], pos: [-10, 2], text: D.footers.sahel_note }], footer: D.footers.africa },
    south_america: { w: 1200, h: 1140, title: 'South America', bb: [-96, -46, -30, 14], mapTop: 150, mapH: 820,
      cards: { nsam: [-52, 12, 'l'], amazon: [-92, 2, 'r'], nebrazil: [-32, -2, 'l'], peru: [-92, -12, 'r'], sesa: [-40, -34, 'l'], altiplano: [-92, -24, 'r'], cchile: [-92, -37, 'r'] },
      notes: [], footer: D.footers.south_america },
    north_america: { w: 1500, h: 1040, title: 'North and Central America', bb: [-164, 6, -54, 64], mapTop: 150, mapH: 730,
      cards: { hawaii: [-157, 33, 'c'], inlandnw: [-140, 55, 'r'], ccanada_warm: [-74, 58, 'l'], norcal: [-133, 41, 'r'], swus: [-128, 31, 'r'], gulf: [-66, 38, 'l'], antilles: [-66, 26, 'l'], drycorridor: [-104, 13, 'r'] },
      notes: [], footer: D.footers.north_america },
  };
  function regional(name) {
    const P = REGIONAL[name]; frame(P.w, P.h);
    head('El Niño 2026–27 · regional close-up', P.title, RSUB);
    P.mapTop = Math.max(P.mapTop, FIG.querySelector('.f-head').offsetTop + FIG.querySelector('.f-head').offsetHeight + 14);
    if (P.inset) {   // drawn first on its own canvas; the main map is drawn last so E.P refers to it
      const box = add(`<div class="inset" style="left:40px; top:${px(P.mapTop + P.mapH - 190)}; width:300px; height:170px"><div class="cap">Hawaii</div></div>`);
      const ic = mapCanvas(0, 0, 300, 170, box);
      Object.assign(E.CAM, E.camFor([-161.5, 18.5, -154.5, 22.5], { l: 0, r: 0, t: 0, b: 0 }, 60));
      drawRegions([P.inset]);
      box.dataset.cam = JSON.stringify(E.CAM);
    }
    const cv = mapCanvas(0, P.mapTop, P.w, P.mapH);
    Object.assign(E.CAM, fitCam(P.bb, P.w, P.mapH)); E.constrain();
    drawRegions();
    const cards = Object.entries(P.cards).map(([k, [lon, lat, al]]) => card(k, lon, lat, al, cv));
    const notes = P.notes.map((n) => note(cv, n.pt, n.pos, n.text));
    declutter([...cards, ...notes], 10, P.mapTop + 8, P.w - 10, P.mapTop + P.mapH - 8, 8);
    for (const el of [...cards, ...notes]) if (el._lead) leader(el._lead, el, el.classList.contains('note') ? 'note-line' : '');
    if (P.inset) {
      const box = FIG.querySelector('.inset'), el = card(P.inset, 0, 0, 'l', cv, true);
      el.style.left = px(box.offsetLeft + box.offsetWidth + 14); el.style.top = px(box.offsetTop + box.offsetHeight / 2 - el.offsetHeight / 2);
    }
    const dag = Object.keys(P.cards).some((k) => D.models[k]?.dagger);
    legendRow(P.mapTop + P.mapH + 14, dag ? [`<span class="lgp">† region drawn where this year's models agree, so its count is high by construction</span>`] : []);
    const lg = FIG.querySelector('.f-legend'), ft = add(`<div class="f-foot" style="top:${px(lg.offsetTop + lg.offsetHeight + 12)}">${P.footer}</div>`);
    credit(' · data: GPCC v2025, GHCN-D, GPCP, NMME, C3S');
    FIG.style.height = px(ft.offsetTop + ft.offsetHeight + 42);
  }

  // ================================================================= hit grid
  function hitGrid() {
    const light = document.documentElement.dataset.theme === 'light';
    const PR = ['#8C510A', '#D9A441', light ? '#E6E3DD' : 'rgba(232,234,242,0.13)', '#5FA8DA', '#0A5599'];
    const TC = ['#9E4AA0', '#D5A6D6', light ? '#E6E3DD' : 'rgba(232,234,242,0.13)', '#EA8466', '#B2182B'];
    FIG.style.width = '1300px';
    const wrap = add('<div class="hg"></div>');
    wrap.appendChild(H(`<div><div class="f-kicker">El Niño 2026–27 · track record</div><div class="f-title">How often have El Niño's impacts actually shown up?</div>
      <p class="f-sub">Each cell is one of the <b>${NEV} strong El Niños since ${S.strong[0]}</b> (Nov–Jan Oceanic Niño Index ≥ 1.5 °C), in the season on the impacts map, compared with ENSO-neutral years after removing long-term trends. Across the ${S.n_regions} map regions, <b>${pct}%</b> of region-events went the expected way (${S.aggregate.hits} of ${S.aggregate.n}).</p></div>`));
    let t = '<table><thead><tr><th class="l"></th><th class="l">Expected</th>' + S.strong.map((y) => `<th>${y}–<br>${String(y + 1).slice(2)}</th>`).join('') + '<th>Matched<br>expectation</th><th>Models agree<br>(Sep 2026)</th></tr></thead><tbody>';
    let prev = null;
    for (const r of D.grid) {
      if (r.group !== prev) { t += `<tr class="g${r.group === 'Not on the map' ? ' off' : ''}"><td colspan="12">${r.group}</td></tr>`; prev = r.group; }
      const cols = r.temp ? TC : PR;
      t += `<tr><td class="lab">${r.label}</td><td class="exp">${r.exp}</td>`;
      for (const c of r.cells) {
        if (c.bin === null) { t += '<td class="c na">n/a</td>'; continue; }
        const ink = c.bin === 0 || c.bin === 4 ? '#fff' : c.bin === 2 ? 'var(--text)' : '#1a1f2b';
        t += `<td class="c" style="background:${cols[c.bin]};color:${ink}">${c.hit ? CK : ''}</td>`;
      }
      t += `<td class="cnt">${r.hits}<small> of ${r.n}</small></td><td class="mod${r.agree === null ? ' na' : ''}">${r.models}</td></tr>`;
    }
    t += '</tbody></table>';
    wrap.appendChild(H(t));
    const sw = (c, s) => `<span><i style="background:${c}"></i>${s}</span>`;
    wrap.appendChild(H(`<div><div class="lg"><span class="lh">Rain &amp; snow</span>${['much drier', 'drier', 'near typical', 'wetter', 'much wetter'].map((s, i) => sw(PR[i], s)).join('')}</div>
      <div class="lg" style="margin-top:8px"><span class="lh">Temperature</span>${['much colder', 'colder', 'near typical', 'warmer', 'much warmer'].map((s, i) => sw(TC[i], s)).join('')}</div>
      <div class="fn">${CK} = on the expected side of the neutral-year median (counted as a match). Much drier/wetter = beyond the 15th/85th percentile of neutral years; near typical = 40th–60th.
      Central Pacific islands use satellite-era data only (5 events). ‡ The 1° grid cannot resolve Peru's coastal plain; see text. Model counts are for each original literature region or a box fixed in advance, over the region's full window up to ${S.horizon} (the last month all 13 systems cover; 6 NMME models for windows after that);
      † = shape drawn where this year's models agree, so the count is high by construction.<br>Z. Hausfather · The Climate Brink · GPCC v2025, Berkeley Earth, GHCN-D, GPCP, NMME, C3S · interactive: dashboard.theclimatebrink.com/#impacts</div></div>`));
    FIG.style.height = px(wrap.offsetHeight);
  }

  // ================================================================= Europe
  function europe() {
    const W = 1440, Hh = 1100; frame(W, Hh);
    const U = D.europe, npos = U.nao.filter((v) => v.djf > 0).length, nneg = U.nao.filter((v) => v.djf < 0).length;
    head('El Niño 2026–27 · Europe', 'El Niño and Europe this winter: no reliable signal',
      'A record El Niño strongly shapes weather around the Pacific rim, but its fingerprint on European winters is weak, inconsistent between events, and mostly not robust in this year\'s forecasts.');
    const light = document.documentElement.dataset.theme === 'light';
    const neutral = css('--bg');
    const CM = {
      pr: [[-1.5, '#5E3304'], [-1, '#A1601A'], [-0.5, '#D8B06A'], [0, neutral], [0.5, '#7CC5B6'], [1, '#26978A'], [1.5, '#0A5A50']],
      t: [[-1.5, '#173F7A'], [-1, '#3570B8'], [-0.5, '#98BFE3'], [0, neutral], [0.5, '#EFA288'], [1, '#D35A45'], [1.5, '#8E1B25']],
    };
    const rgb = (c) => { if (c.startsWith('#')) { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; } return c.match(/[\d.]+/g).slice(0, 3).map(Number); };
    const cmap = (stops, v) => {
      v = clamp(v, -1.5, 1.5);
      for (let i = 1; i < stops.length; i++) if (v <= stops[i][0]) { const a = rgb(stops[i - 1][1]), b = rgb(stops[i][1]), t = (v - stops[i - 1][0]) / (stops[i][0] - stops[i - 1][0]); return a.map((x, k) => Math.round(lerp(x, b[k], t))); }
      return rgb(stops[stops.length - 1][1]);
    };
    const pw = 440, ph = 360, top = 160, lon0 = -12, lon1 = 38, lat0 = 34, lat1 = 71, cosf = Math.cos(52.5 * DEG);
    const sc = Math.min(pw / ((lon1 - lon0) * cosf), ph / (lat1 - lat0)), lonc = (lon0 + lon1) / 2, latc = (lat0 + lat1) / 2;
    const X = (lo) => pw / 2 + (lo - lonc) * sc * cosf, Y = (la) => ph / 2 - (la - latc) * sc;
    U.panels.forEach((P, i) => {
      const x0 = 40 + i * (pw + 20);
      const box = add(`<div class="eu-p" style="left:${px(x0)}; top:${px(top)}; width:${px(pw)}"><h3>${P.title}</h3></div>`);
      const c = document.createElement('canvas'), dpr = 2; c.width = pw * dpr; c.height = ph * dpr; c.style.cssText = `position:static;width:${pw}px;height:${ph}px;border-radius:8px;border:1px solid ${css('--line-strong')}`;
      box.appendChild(c);
      const g = c.getContext('2d'); g.scale(dpr, dpr);
      const PCT = P.cmap === 'pct';
      g.fillStyle = PCT ? css('--map-ocean') : neutral; g.fillRect(0, 0, pw, ph);
      if (PCT) { g.fillStyle = css('--map-land'); for (const r of geo.land) { g.beginPath(); r.forEach(([lo, la], q) => (q ? g.lineTo(X(lo), Y(la)) : g.moveTo(X(lo), Y(la)))); g.closePath(); g.fill(); } }
      // field: one pixel per 1° cell, smoothed on scale-up
      const nx = U.lon.length, ny = U.lat.length, off = document.createElement('canvas'); off.width = nx; off.height = ny;
      const og = off.getContext('2d'), im = og.createImageData(nx, ny);
      const fa = +css('--map-field-a');
      P.z.forEach((row, jj) => row.forEach((v, ii) => {
        const o = (jj * nx + ii) * 4; if (v === null) return;
        const [r, gg, b] = PCT ? E.prColor(v) : cmap(CM[P.cmap], v);
        im.data[o] = r; im.data[o + 1] = gg; im.data[o + 2] = b; im.data[o + 3] = PCT ? 255 * E.prAlpha(v) * fa : 255;
      }));
      og.putImageData(im, 0, 0);
      g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
      const lw = U.lon[0] - 0.5, le = U.lon[nx - 1] + 0.5, ln = U.lat[0] + 0.5, ls = U.lat[ny - 1] - 0.5;   // lat descending
      g.drawImage(off, X(lw), Y(ln), X(le) - X(lw), Y(ls) - Y(ln));
      // coast + borders
      g.lineJoin = 'round'; g.strokeStyle = light ? 'rgba(30,36,50,0.55)' : 'rgba(225,232,245,0.55)'; g.lineWidth = 0.8;
      for (const r of geo.land) { g.beginPath(); r.forEach(([lo, la], q) => (q ? g.lineTo(X(lo), Y(la)) : g.moveTo(X(lo), Y(la)))); g.closePath(); g.stroke(); }
      g.strokeStyle = light ? 'rgba(30,36,50,0.22)' : 'rgba(225,232,245,0.22)'; g.lineWidth = 0.5;
      for (const r of geo.borders) { g.beginPath(); r.forEach(([lo, la], q) => (q ? g.lineTo(X(lo), Y(la)) : g.moveTo(X(lo), Y(la)))); g.stroke(); }
      // robust dots
      g.fillStyle = css('--text');
      P.robust.forEach((row, jj) => row.forEach((v, ii) => { if (!v) return; g.beginPath(); g.arc(X(U.lon[ii]), Y(U.lat[jj]), 1.6, 0, 7); g.fill(); }));
      // colour bar
      const cb = document.createElement('canvas'); cb.width = pw * 2; cb.height = 20; cb.style.cssText = `position:static;width:${pw}px;height:10px;border-radius:5px;display:block;margin-top:10px`;
      const cg = cb.getContext('2d');
      if (PCT) { cg.fillStyle = css('--map-land'); cg.fillRect(0, 0, pw * 2, 20); }
      for (let q = 0; q < pw * 2; q++) {
        if (PCT) { const v = -60 + 120 * q / (pw * 2), [r, gg, b] = E.prColor(v); cg.fillStyle = `rgba(${r | 0},${gg | 0},${b | 0},${E.prAlpha(v) * fa})`; }
        else { const [r, gg, b] = cmap(CM[P.cmap], -1.5 + 3 * q / (pw * 2)); cg.fillStyle = `rgb(${r},${gg},${b})`; }
        cg.fillRect(q, 0, 1, 20);
      }
      box.appendChild(cb);
      box.appendChild(H(PCT ? `<div class="cb-t"><span>−60%</span><span>−30%</span><span>0</span><span>+30%</span><span>+60%</span></div>`
        : `<div class="cb-t"><span>−1.5</span><span>−1</span><span>−0.5</span><span>0</span><span>+0.5</span><span>+1</span><span>+1.5</span></div>`));
      box.appendChild(H(`<div class="cb-l">${PCT ? '← drier · wetter →  (% of the 1991–2020 normal)' : '← colder · warmer →  (typical year-to-year swings)'}</div>`));
    });
    const R = U.robust_pct;
    add(`<p class="f-sub" style="position:absolute; left:40px; right:40px; top:${px(top + ph + 96)}; font-size:13px">Average of ${U.n_models} seasonal forecast models (NMME + Copernicus C3S, ${S.init} start). Rain: change as % of the 1991–2020 normal, the same scale as the impacts map. Temperature: in units of a typical year-to-year swing, trend removed. Dots: robust signal, where at least 80% of models agree and the average shift is at least half a typical year-to-year swing. Robust areas cover <b>${R.pr_OND}%</b> of European land for Oct–Dec rain (mostly western Ireland, Britain and France), <b>${R.pr_JF}%</b> for Jan–Feb rain and <b>${R.t_JF}%</b> for Jan–Feb temperature.</p>`);
    // NAO bars
    const cw = 640, ch = 320, y0 = 690, x0 = 40, pl = 46, pb = 60, ymin = -2, ymax = 1.75, sy = (ch - pb - 36) / (ymax - ymin), yv = (v) => 36 + (ymax - v) * sy;
    const bw = (cw - pl - 10) / U.nao.length;
    let s = `<svg class="nao" width="${cw}" height="${ch}" style="position:absolute;left:${px(x0)};top:${px(y0)}" xmlns="http://www.w3.org/2000/svg">`;
    s += `<text x="0" y="14" style="font:600 15px var(--display);fill:var(--text)">Every strong El Niño winter since 1950: the NAO split ${npos} positive, ${nneg} negative</text>`;
    for (const t of [-2, -1, 0, 1]) s += `<line class="${t === 0 ? 'zero' : 'ax'}" x1="${pl}" x2="${cw - 6}" y1="${yv(t)}" y2="${yv(t)}"/><text class="yl" x="${pl - 8}" y="${yv(t) + 4}" text-anchor="end">${t > 0 ? '+' : ''}${t}</text>`;
    U.nao.forEach((b, i) => {
      const cx = pl + bw * (i + 0.5), y1 = yv(Math.max(0, b.djf)), y2 = yv(Math.min(0, b.djf));
      s += `<rect class="${b.djf > 0 ? 'pos' : 'neg'}" x="${cx - bw * 0.3}" y="${y1}" width="${bw * 0.6}" height="${Math.max(1, y2 - y1)}" rx="3"/>`;
      s += `<text class="vl" x="${cx}" y="${b.djf > 0 ? y1 - 6 : y2 + 15}" text-anchor="middle">${b.djf > 0 ? '+' : '−'}${Math.abs(b.djf).toFixed(1)}</text>`;
      s += `<text class="xl" x="${cx}" y="${ch - pb + 22}" text-anchor="middle">${b.winter - 1}–${String(b.winter).slice(2)}</text>`;
    });
    s += `<text class="yl" transform="translate(12 ${36 + (ch - pb - 36) / 2}) rotate(-90)" text-anchor="middle">Winter (Dec–Feb) NAO index</text>`;
    s += `<text class="yl" x="${pl}" y="${ch - 20}" style="font-style:italic">Textbook El Niño expectation: negative NAO (cold north, wet south).</text><text class="yl" x="${pl}" y="${ch - 4}" style="font-style:italic">Positive NAO = mild, wet, stormy UK &amp; northern Europe.</text></svg>`;
    add(s);
    add(`<div class="eu-box" style="left:740px; top:${px(y0)}; width:660px"><h3>What this means</h3><ul>
      <li>Models lean wet for the UK and central Europe in Oct–Dec (<b>${U.uk_pos} of ${U.uk_n}</b> models) and colder for Scandinavia in Jan–Feb (<b>${U.sc_neg} of ${U.sc_n}</b>), but the shifts are small: about ${U.uk_pct === U.ce_pct ? `+${U.uk_pct}%` : `+${U.uk_pct}% and +${U.ce_pct}%`} rain for the UK and central Europe, and ${U.shift_hi} of a typical year-to-year swing for Scandinavian temperature.</li>
      <li>No European region passes the bar used for the global impacts map, and past strong El Niño winters split ${npos}–${nneg} on the NAO.</li>
      <li>The textbook late-winter pattern (cold north, wet south) mostly appears when a sudden stratospheric warming occurs, which can't be forecast months ahead (Ineson and Scaife 2009).</li>
      <li>The El Niño–Europe link may have weakened since the 1970s (Ivasić et al. 2021).</li></ul></div>`);
    credit(' · data: NMME, C3S, GPCP, ERA5, NOAA CPC NAO index');
  }

  ({ impacts_map: globalMap, hit_grid: hitGrid, europe_signal: europe }[FIGN] ?? (() => regional(FIGN)))();
  window.READY = true;
})().catch((e) => { document.body.insertAdjacentHTML('beforeend', `<pre style="color:red">${e.stack}</pre>`); window.READY = 'error: ' + e.message; });
