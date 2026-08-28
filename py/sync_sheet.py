#!/usr/bin/env python3
"""Fetch the HEP tracking Google Sheet (xlsx export) and publish:
  - data/hep-tracking.json   (rows, Explanation as HTML spans for bold/italic/color)
  - data/hep-tracking.xlsx   (viewable copy of the sheet)

Sheet is public, so no auth is needed. The xlsx format preserves rich text
(bold, italic, color), which the TSV/CSV exports strip.

Exit codes: 0 = files written, 1 = fetch/parse/validation failure.
"""

import json
import re
import sys
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

SPREADSHEET_ID = "1GLIgn546t5c6Vjk0Y3WE-4s9tjpSkjKQLkBZ9PyzLuw"
EXPECTED_HEADERS = ["Organization", "Date", "Sector", "Explanation"]

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_JSON = DATA / "hep-tracking.json"
OUT_XLSX = DATA / "hep-tracking.xlsx"

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def fetch_xlsx() -> bytes:
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        )
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except Exception as exc:
        print(f"ERROR: fetch failed: {exc}", file=sys.stderr)
        sys.exit(1)


def style_span(rpr) -> str:
    """Build a style string from a rich text run's rPr element, or None."""
    styles = []
    if rpr.find(f"{NS}b") is not None:
        styles.append("font-weight:bold")
    if rpr.find(f"{NS}i") is not None:
        styles.append("font-style:italic")
    if rpr.find(f"{NS}u") is not None:
        styles.append("text-decoration:underline")
    if rpr.find(f"{NS}strike") is not None:
        styles.append("text-decoration:line-through")
    color = rpr.find(f"{NS}color")
    if color is not None and color.get("rgb"):
        styles.append(f"color:#{color.get('rgb')[-6:]}")
    if not styles:
        return None
    return ";".join(styles)


def build_shared_strings(ss_xml: str) -> list:
    """Parse sharedStrings.xml. Rich-text runs become HTML span markup."""
    root = ET.fromstring(ss_xml)
    out = []
    for si in root.findall(f"{NS}si"):
        runs = si.findall(f"{NS}r")
        if not runs:
            t = si.find(f"{NS}t")
            out.append(t.text if t is not None and t.text else "")
            continue
        parts = []
        for r in runs:
            t = r.find(f"{NS}t")
            text = t.text if t is not None and t.text else ""
            rpr = r.find(f"{NS}rPr")
            style = style_span(rpr) if rpr is not None else None
            if style:
                parts.append(f"<span style='{style}'>{escape(text)}</span>")
            else:
                parts.append(escape(text))
        out.append("".join(parts))
    return out


def col_index(ref: str) -> int:
    """Cell ref like 'A2' -> 0-based column index."""
    letters = re.match(r"([A-Z]+)", ref).group(1)
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def parse_rows(sheet_xml: str, shared: list) -> list:
    root = ET.fromstring(sheet_xml)
    sheet_data = root.find(f"{NS}sheetData")
    rows = []
    for row in sheet_data.findall(f"{NS}row"):
        cells = {}
        for c in row.findall(f"{NS}c"):
            col = col_index(c.get("r"))
            t = c.get("t")
            v = c.find(f"{NS}v")
            if v is None or v.text is None:
                continue
            if t == "s":
                cells[col] = shared[int(v.text)]
            elif t == "inlineStr":
                is_el = c.find(f"{NS}is")
                t_el = is_el.find(f"{NS}t") if is_el is not None else None
                cells[col] = t_el.text if t_el is not None and t_el.text else ""
            else:
                cells[col] = v.text
        rows.append(cells)
    return rows


def canonical_xlsx(data: bytes) -> bytes:
    """Re-zip with fixed timestamps.

    Google stamps each xlsx export's zip entries with the current time, so
    byte-identical content produces different files every run. Rewriting the
    archive with a fixed timestamp makes the saved copy stable: it only
    changes when the sheet content actually changes.
    """
    src = zipfile.ZipFile(BytesIO(data))
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src.infolist():
            info.date_time = (1980, 1, 1, 0, 0, 0)
            out.writestr(info, src.read(info.filename))
    return buf.getvalue()


def main() -> None:
    data = fetch_xlsx()
    if data[:2] != b"PK":
        print("ERROR: response is not a valid xlsx", file=sys.stderr)
        sys.exit(1)

    DATA.mkdir(parents=True, exist_ok=True)
    OUT_XLSX.write_bytes(canonical_xlsx(data))  # viewable copy of the sheet in the repo

    with zipfile.ZipFile(BytesIO(data)) as z:
        shared = build_shared_strings(z.read("xl/sharedStrings.xml").decode("utf-8"))
        sheet = z.read("xl/worksheets/sheet1.xml").decode("utf-8")

    grid = parse_rows(sheet, shared)
    if not grid:
        print("ERROR: no rows found; refusing to write", file=sys.stderr)
        sys.exit(1)

    headers = [grid[0].get(i, "") for i in range(len(EXPECTED_HEADERS))]
    if headers != EXPECTED_HEADERS:
        print(
            f"ERROR: header mismatch. Expected {EXPECTED_HEADERS}, got {headers}",
            file=sys.stderr,
        )
        sys.exit(1)

    rows = []
    for r in grid[1:]:
        if not any((r.get(i) or "").strip() for i in range(len(EXPECTED_HEADERS))):
            continue  # skip trailing empty rows
        row = {}
        for i, h in enumerate(EXPECTED_HEADERS):
            val = r.get(i, "")
            if h == "Date":
                # xlsx exports numbers as "2016.0"; keep as plain string
                val = val[:-2] if val.endswith(".0") else val
            row[h] = val
        rows.append(row)

    if not rows:
        print("ERROR: no data rows found; refusing to write", file=sys.stderr)
        sys.exit(1)

    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} rows to {OUT_JSON}")
    print(f"Wrote viewable copy to {OUT_XLSX}")


if __name__ == "__main__":
    main()
