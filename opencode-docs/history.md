# History

## 2026-10-23

- Replaced the xlsx/rich-text sync path with the published TSV transform from `py/data_transform.ipynb`: two header rows, 9 selected columns, forward-fill of the 6 group columns, JSON records.
- Implemented in `py/sync_sheet_format.py`; added `py/requirements.txt` (pandas 3.0.3) and pip caching + install step to `.github/workflows/sync.yml`.
- Verified: 120 records, 0 nulls in group columns, valid JSON, `null` for empty `Status` (81) and `Lead Implementers` (96).
- First pass added row filtering and schema validation that were not in the notebook; removed on request. Script now mirrors the notebook: no filtering, no extra cleaning.
- Found: `csv.reader` and `pd.read_csv` both fail on this export (bare CR inside one cell), so manual line splitting is used deliberately.
- Dropped `data/hep-tracking.xlsx` writing and the `canonical_xlsx` helper.
