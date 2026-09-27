# Blog figures, dashboard style

These scripts redraw the seven figures in `cb_el_nino_impacts_draft.md` with the Climate Dashboard's El Niño tab engine, card components, fonts and data. Each figure is rendered in both themes: `figures/<name>_light.png` for the post and `figures/<name>_dark.png` for social.

```bash
python3.13 figures/web/export_figdata.py   # data -> figures/web/figdata.json (fetches CPC NAO + ONI)
node figures/web/render.mjs                # all figures, or name some: impacts_map hit_grid indo_pacific africa south_america north_america europe_signal
```

Every number comes from computed data. Region polygons, the observed record and per-model values are read from `Climate Dashboard/elnino_map/data`, the same files as the live tab. Everything else comes from `export_figdata.py`, which reuses the matplotlib scripts' own logic:
- hit-grid rows, bins and model counts from `make_hit_grid.py`;
- global label positions from `make_impacts_map.py`;
- footers from `hit_rates/derived`;
- the Europe fields and NAO winters from `make_europe_signal.py`.

The model counts on the figures follow the hit grid's convention: the model test on each original literature region, or on a box fixed in advance. † marks shapes drawn where this year's models agree. The dashboard tab uses the same convention, so southern China reads 12/13 in both (the final drawn polygon would give 11/13).

- `fig.html` / `fig.js` / `fig.css`: one page, `?fig=<name>&theme=light|dark`.
- `render.mjs` serves the dashboard's `/elnino_map` and `/assets` next to this folder and screenshots `#fig` at 2x.
- Labels and cards start at hand-picked anchors and are pushed apart automatically, so they never overlap.
