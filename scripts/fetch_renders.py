#!/usr/bin/env python3
"""ينزّل مخرجات Higgsfield المكتوبة في higgsfield/renders.json إلى higgsfield/renders/."""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDERS = ROOT / "higgsfield" / "renders"


def main():
    manifest = json.loads((ROOT / "higgsfield" / "renders.json").read_text(encoding="utf-8"))
    RENDERS.mkdir(parents=True, exist_ok=True)
    failed = 0
    for name, item in manifest.items():
        if name.startswith("_"):
            continue
        dest = RENDERS / name
        if dest.exists():
            print(f"  موجود: {name}")
            continue
        try:
            with urllib.request.urlopen(item["url"], timeout=60) as res:
                dest.write_bytes(res.read())
            print(f"  نزل: {name}")
        except OSError as e:
            failed += 1
            print(f"  فشل: {name}: {e}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
