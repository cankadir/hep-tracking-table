# History

## 2026-10-28 (status bar)

- Added `web-app/src/lib/components/StatusBar.svelte`: counts activities per status from `$lib/status.js`, maps counts to percent widths with `scaleLinear`, writes the stacked bar as plain SVG markup (no d3 DOM code).
- `Accordion.svelte` gained an `extra` snippet rendered left of the `+` icon (10rem, hidden under 40rem); the page passes a bar for each objective, so 19 bars exist in the page. `extra` sits in the header button, so bars survive the closed/unmounted body.
- Page now uses `$lib/status.js` for both label and class; `.status.none` became `.status.na`. JSON still carries `null`.
- **Svelte drops a whitespace-only text node inside `<title>` in SVG**, so `<title>{count} {name}</title>` SSR'd as "9Completed". Fixed by interpolating the whole string: `{`${count} ${name}`}`. Watch for this in any svg tooltip.
- Verified without a build: autofixer clean, 0 warnings client+server compile, SSR with every accordion forced open gives 36 `<rect>` / 19 `aria-label="Status mix: …"` / 81 `NA` badges / badges 2·24·12·1·81; per-objective widths chain with no gaps and sum to 100.
- Note: with all accordions closed on first paint, no h3 renders, so no bars are visible until a goal is expanded.

## 2026-10-28 (later)

- Replaced the one-off card styling with the client's existing accordion pattern. The user guessed `LegendAccordion.svelte`; that file is a legend/metadata panel with no toggle. The real pattern lives in `SectorSidebar.svelte` (plus icon rotating to ×, `transition:slide`, `#d6d6ce` open state), so that is what was ported.
- Added `web-app/src/lib/components/Accordion.svelte` and copied `accordion-open.svg` from the other project. Goals and objectives are accordions; actions stay as headings over their per-action table. Status badges and the table styling were kept by request.
- First goal and first objective open on load.
- Verified: autofixer clean on both files, zero compiler warnings, SSR shows 5 h2 / 4 h3 / 4 h4 / 4 tables on first paint and the full 5/19/41/120 when forced open, status mix unchanged.
- Tradeoff flagged: closed accordions unmount, so Ctrl+F only finds open rows.

## 2026-10-28

- Client asked for a hierarchical view instead of a flat 9-column table. Added `web-app/src/lib/group.js` (`groupRows`) that folds the flat JSON into `Goal > Objective > Action > activities`. No dependency added; nested `Map` grouping is about 20 lines and preserves sheet order.
- Grouping keys are composites (code + desc + subtitle for objectives, code + desc for actions), so repeated codes like `A` across the 5 goals never merge.
- Rewrote `web-app/src/routes/+page.svelte`, which still expected the old `Organization / Date / Sector / Explanation` schema. Now renders nested sections with a per-action activities table and status badges; all sizing in rem.
- Removed the unused `rows` writable from `$lib/store.js`; the page uses `$derived(groupRows(data.rows))`.
- Verified: `groupRows` gives 5 / 19 / 41 / 120, matching the flat counts; autofixer clean; `npm run build` passes; live dev render shows 5 h2, 19 h3, 41 h4/tables, 120 activity rows.
- No filtering, no schema change to the JSON: the GitHub Action output is untouched, so other consumers of the flat file are unaffected.

## 2026-10-23

- Replaced the xlsx/rich-text sync path with the published TSV transform from `py/data_transform.ipynb`: two header rows, 9 selected columns, forward-fill of the 6 group columns, JSON records.
- Implemented in `py/sync_sheet_format.py`; added `py/requirements.txt` (pandas 3.0.3) and pip caching + install step to `.github/workflows/sync.yml`.
- Verified: 120 records, 0 nulls in group columns, valid JSON, `null` for empty `Status` (81) and `Lead Implementers` (96).
- First pass added row filtering and schema validation that were not in the notebook; removed on request. Script now mirrors the notebook: no filtering, no extra cleaning.
- Found: `csv.reader` and `pd.read_csv` both fail on this export (bare CR inside one cell), so manual line splitting is used deliberately.
- Dropped `data/hep-tracking.xlsx` writing and the `canonical_xlsx` helper.
