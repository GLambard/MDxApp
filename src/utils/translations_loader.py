"""Load translations.json once per Streamlit session."""

from functools import lru_cache
from pathlib import Path
from typing import Dict

import streamlit as st

from .i18n import load_translations


def translations_path() -> Path:
    """Resolve Assets/translations.json from project root."""
    return Path(__file__).resolve().parents[2] / "Assets" / "translations.json"


@lru_cache
def load_app_translations() -> Dict[str, Dict[str, str]]:
    """Cached load of all language packs (cleared on process restart)."""
    return load_translations(translations_path())


def get_lang_pack(language: str) -> Dict[str, str]:
    """Translation dict for a language with English fallback."""
    transl = load_app_translations()
    if language in transl:
        return transl[language]
    return transl["English"]
