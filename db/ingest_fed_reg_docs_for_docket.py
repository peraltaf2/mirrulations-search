#!/usr/bin/env python3
"""
Pipeline:
- Read mirrulations-fetch docket folder
- Extract FR doc numbers from documents/*.json
- Fetch each FR document from the Federal Register API
- Call ingest_federal_registry_document.py for each

Usage:
  python db/ingest_fed_reg_docs_for_docket.py \
    --docket-dir data/CMS_2026
"""

import argparse
import json
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Set

FR_API_URL = "https://www.federalregister.gov/api/v1/documents/{}.json"


# ─── Extract FR doc numbers ───────────────────────────────────────────────────

def extract_frdocnums(doc_path: Path) -> Set[str]:
    try:
        raw = json.loads(doc_path.read_text(encoding="utf-8"))
    except Exception:
        return set()

    fr_nums = set()

    # Navigate to attributes safely
    attrs = (
        raw.get("data", {})
           .get("attributes", {})
    )

    if not isinstance(attrs, dict):
        return fr_nums

    val = attrs.get("frDocNum")

    if isinstance(val, str) and val.strip():
        fr_nums.add(val.strip())

    return fr_nums


def collect_frdocnums(docket_dir: Path) -> Set[str]:
    docs_dir = docket_dir / "documents"

    if not docs_dir.exists():
        raise SystemExit(f"documents folder not found: {docs_dir}")

    all_nums = set()

    for file in docs_dir.glob("*.json"):
        nums = extract_frdocnums(file)
        all_nums.update(nums)

    return all_nums


# ─── Fetch from Federal Register API ─────────────────────────────────────────

def fetch_fr_document(frdocnum: str) -> dict:
    url = FR_API_URL.format(frdocnum)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Not found in Federal Register API: {frdocnum}")
        else:
            print(f"HTTP {e.code} fetching {frdocnum}: {e.reason}")
        return {}
    except urllib.error.URLError as e:
        print(f"Network error fetching {frdocnum}: {e.reason}")
        return {}


# ─── Run ingest script ────────────────────────────────────────────────────────

def run_ingest(frdocnum: str):
    doc = fetch_fr_document(frdocnum)
    if not doc:
        return

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(doc, tmp)
        tmp_path = tmp.name

    cmd = [
        "python3",
        "db/ingest_federal_registry_document.py",
        "--json",
        tmp_path,
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Ingested {frdocnum}")
    except subprocess.CalledProcessError:
        print(f"Failed ingest: {frdocnum}")
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--docket-dir",
        required=True,
        help="Path to mirrulations-fetch docket folder (contains /documents)",
    )
    args = ap.parse_args()

    docket_dir = Path(args.docket_dir)

    if not docket_dir.exists():
        raise SystemExit(f"Docket folder not found: {docket_dir}")

    print("Collecting FR document numbers...")
    frdocnums = collect_frdocnums(docket_dir)

    print(f"Found {len(frdocnums)} unique FR documents")

    for frdocnum in sorted(frdocnums):
        run_ingest(frdocnum)


if __name__ == "__main__":
    main()