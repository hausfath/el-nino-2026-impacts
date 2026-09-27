// Render the dashboard-style blog figures to PNG (2x) in dark and light.
// usage: node figures/web/render.mjs [fig ...]   (default: all)
// Serves /elnino_map and /assets from the Climate Dashboard repo so the figures use the live tab's engine,
// cards, fonts and data, and this folder for fig.html / fig.js / figdata.json.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const FIGDIR = path.resolve(HERE, '..');
// the dashboard repo (github.com/hausfath/climate-dashboard): $CLIMATE_DASHBOARD, the local working copy, or a sibling clone
const DASH = [process.env.CLIMATE_DASHBOARD, path.resolve(HERE, '../../../../Climate Dashboard'), path.resolve(HERE, '../../../climate-dashboard')]
  .find((p) => p && fs.existsSync(path.join(p, 'elnino_map')));
if (!DASH) { console.error('set CLIMATE_DASHBOARD to a clone of github.com/hausfath/climate-dashboard'); process.exit(1); }
// playwright-core: this folder's own install (npm install), else the video project's
const pkg = [path.resolve(HERE, 'package.json'), path.resolve(HERE, '../../video/package.json')].find((p) => fs.existsSync(p.replace('package.json', 'node_modules/playwright-core')));
const require = createRequire(pkg ?? path.resolve(HERE, 'package.json'));
const { chromium } = require('playwright-core');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.bin': 'application/octet-stream', '.png': 'image/png', '.ttf': 'font/ttf' };
const srv = http.createServer((req, res) => {
  const u = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const f = u.startsWith('/elnino_map/') || u.startsWith('/assets/') ? path.join(DASH, u) : path.join(HERE, u);
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] ?? 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
}).listen(0);
const port = srv.address().port;
const ALL = ['impacts_map', 'hit_grid', 'indo_pacific', 'africa', 'south_america', 'north_america', 'europe_signal'];
const figs = process.argv.slice(2).length ? process.argv.slice(2) : ALL;
const b = await chromium.launch({ channel: 'chrome' });
for (const fig of figs) for (const theme of ['light', 'dark']) {
  const p = await b.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
  await p.goto(`http://127.0.0.1:${port}/fig.html?fig=${fig}&theme=${theme}`);
  await p.waitForFunction(() => window.READY, null, { timeout: 30000 });
  const ok = await p.evaluate(() => window.READY);
  if (ok !== true) { console.log('FAIL', fig, theme, ok, errs.join(' | '), await p.evaluate(() => document.querySelector('pre')?.textContent?.slice(0, 600))); await p.close(); continue; }
  const name = { impacts_map: 'elnino_2026_impacts_map', hit_grid: 'elnino_2026_hit_grid', europe_signal: 'elnino_2026_europe_signal' }[fig] ?? `elnino_2026_impacts_map_${fig}`;
  const out = path.join(FIGDIR, `${name}_${theme}.png`);
  await p.locator('#fig').screenshot({ path: out });
  console.log(ok === true ? 'ok ' : `FAIL ${ok} `, path.basename(out), errs.length ? errs.join(' | ') : '');
  await p.close();
}
await b.close(); srv.close();
