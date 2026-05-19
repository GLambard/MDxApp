#!/usr/bin/env python3
"""Merge scripts/i18n_locale_packs.py into Assets/translations.json."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.i18n_locale_packs import merge_into  # noqa: E402

TRANS_PATH = ROOT / "Assets" / "translations.json"


def main() -> None:
    base = json.loads(TRANS_PATH.read_text(encoding="utf-8"))
    merge_into(base)
    TRANS_PATH.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {TRANS_PATH} ({len(base)} languages)")


if __name__ == "__main__":
    main()
