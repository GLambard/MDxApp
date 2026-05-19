"""
Locale helpers: RTL languages, display order, and layout direction for Streamlit.
"""

from typing import Dict, List

import streamlit as st

# Right-to-left UI languages
RTL_LANGUAGES = frozenset({"العربية"})

# Preferred order in the language selector (remaining langs sorted alphabetically after)
LANGUAGE_DISPLAY_ORDER: List[str] = [
    "English",
    "Français",
    "Español",
    "Deutsch",
    "Italiano",
    "Português",
    "中文",
    "日本語",
    "한국어",
    "Русский",
    "العربية",
    "हिन्दी",
    "Türkçe",
    "Tiếng Việt",
    "Bahasa Indonesia",
]


def is_rtl(language: str) -> bool:
    """True when the active language needs right-to-left layout."""
    return language in RTL_LANGUAGES


def sort_languages(translations: Dict[str, dict]) -> List[str]:
    """Stable language list: preferred order first, then alphabetical."""
    available = set(translations.keys())
    ordered = [lang for lang in LANGUAGE_DISPLAY_ORDER if lang in available]
    remainder = sorted(lang for lang in available if lang not in ordered)
    return ordered + remainder


def apply_rtl_layout(language: str) -> None:
    """Apply RTL direction and alignment for Arabic (and future RTL locales)."""
    if not is_rtl(language):
        return

    st.markdown(
        """
        <style>
        /* App shell */
        [data-testid="stAppViewContainer"],
        [data-testid="stSidebar"],
        section.main {
            direction: rtl;
        }

        /* Main text blocks */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        .mdx-donation-text,
        .mdx-donation-title,
        .mdx-evidence-item {
            text-align: right;
        }

        /* Lists and expander labels */
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p {
            text-align: right;
            direction: rtl;
        }

        /* Form controls: keep inputs LTR for email/numbers */
        input, textarea {
            direction: rtl;
            text-align: right;
        }
        input[type="email"] {
            direction: ltr;
            text-align: left;
        }

        /* Columns: reverse visual order where helpful */
        [data-testid="stHorizontalBlock"] {
            direction: rtl;
        }

        /* Download / primary buttons */
        [data-testid="stButton"] {
            direction: rtl;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
