#!/usr/bin/env python3
"""
Pipeline:
- Read mirrulations-fetch docket folder
- Extract FR doc numbers from documents/*.json
- Call ingest_federal_registry_document.py for each FR JSON

Usage:
  python db/ingest_docket_federal_register.py \
    --docket-dir data/CMS_2026 \
    --fr-dir db/data/CMS_2026/federal_register
"""

import argparse
import json
import subprocess
from pathlib import Path
from typing import Set


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


# ─── Run ingest script ────────────────────────────────────────────────────────

def run_ingest(frdocnum: str, fr_dir: Path):
    json_path = fr_dir / f"{frdocnum}.json"

    if not json_path.exists():
        print(f"⚠️  Missing FR JSON: {json_path}")
        return

    cmd = [
        "python3",
        "db/ingest_federal_registry_document.py",
        "--json",
        str(json_path),
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Ingested {frdocnum}")
    except subprocess.CalledProcessError:
        print(f"Failed ingest: {frdocnum}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--docket-dir",
        required=True,
        help="Path to mirrulations-fetch docket folder (contains /documents)",
    )
    ap.add_argument(
        "--fr-dir",
        required=True,
        help="Directory containing Federal Register JSON files",
    )

    args = ap.parse_args()

    docket_dir = Path(args.docket_dir)
    fr_dir = Path(args.fr_dir)

    if not docket_dir.exists():
        raise SystemExit(f"Docket folder not found: {docket_dir}")

    if not fr_dir.exists():
        raise SystemExit(f"FR directory not found: {fr_dir}")

    print("Collecting FR document numbers...")
    frdocnums = collect_frdocnums(docket_dir)

    print(f"Found {len(frdocnums)} unique FR documents")

    for frdocnum in sorted(frdocnums):
        run_ingest(frdocnum, fr_dir)


if __name__ == "__main__":
    main()