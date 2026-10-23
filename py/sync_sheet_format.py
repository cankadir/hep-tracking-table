#!/usr/bin/env python3
"""Fetch the published HEP tracking sheet (TSV) and publish data/hep-tracking.json.

Two header rows: row 0 is a merged banner, row 1 holds the real column names.
Goal / Objective / Action columns are merged in the sheet, so they are only
filled on the first row of each group and get forward-filled before flattening.

Exit codes: 0 = file written, 1 = fetch/parse failure.
"""

import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd

PUBLISH_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTximK54RzevgtA54SwKnbA7P8o_d_nPcaqr0VG1jh7q3bbkOQSgesrUoeALTWujpycf-AtXO-eXFxU"
    "/pub?output=tsv"
)
COLUMNS = [
    "Goal",
    "Objective Code",
    "Objective Desc",
    "Subtitle",
    "Action Code",
    "Action Desc",
    "Activities-Deliverables",
    "Status",
    "Lead Implementers",
]
FILL_COLUMNS = COLUMNS[:6]

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "data" / "hep-tracking.json"


def fetch_tsv():
    req = urllib.request.Request(
        PUBLISH_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; hep-tracking-sync)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception as exc:
        sys.exit(f"ERROR: fetch failed: {exc}")


def read_rows(text):
    """Split the export into rows of fields.

    Not csv.reader: one cell holds a bare CR, which makes the csv module treat
    it as a line break and fail.
    """
    return [[field.replace("\r", "") for field in line.split("\t")] for line in text.split("\n")]


def build_frame(text):
    rows = read_rows(text)[1:]  # skip the banner row
    # object dtype keeps None as None; pandas 3's default str dtype turns it into NaN.
    df = pd.DataFrame(data=rows[1:], columns=rows[0], dtype=object)
    df = df.replace("", None)
    df = df[COLUMNS]
    for c in FILL_COLUMNS:
        df[c] = df[c].ffill().str.strip()
    return df


def main():
    df = build_frame(fetch_tsv())
    records = df.to_dict("records")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {OUT_JSON}")


if __name__ == "__main__":
    main()
