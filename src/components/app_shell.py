"""
Shared Streamlit shell: sidebar (language, donation) and localized navigation labels.
"""

from pathlib import Path
from typing import Any, Dict, List

import streamlit as st

from ..components.donation import get_default_qr_path, render_sidebar_donation
from ..components.language_selector import (
    add_language_separator,
    get_current_language,
    render_language_selector,
)
from ..config.settings import get_settings
from ..utils.locale import apply_rtl_layout


def _nav_label(trans: Dict[str, Any], key: str, fallback: str) -> str:
    """Sidebar page title from translations (existing keys)."""
    return str(trans.get(key, fallback))


def build_navigation_pages(
    transl: Dict[str, Dict[str, Any]],
    lang: str,
    app_dir: Path,
) -> List[st.Page]:
    """Build st.Page list with titles in the active language (updates on language change)."""
    trans = transl.get(lang, transl.get("English", {}))
    pages_dir = app_dir / "pages"
    return [
        st.Page(
            pages_dir / "diagnosis.py",
            title=_nav_label(trans, "nav_diagnosis", trans.get("page1_title", "Diagnosis")),
            icon="🏥",
            default=True,
        ),
        st.Page(
            pages_dir / "about.py",
            title=_nav_label(trans, "nav_about", trans.get("page_about_title", "About")),
            icon="📰",
        ),
        st.Page(
            pages_dir / "contact.py",
            title=_nav_label(trans, "nav_contact", trans.get("page_contact_title", "Contact")),
            icon="✉️",
        ),
    ]


def render_app_sidebar(
    transl: Dict[str, Dict[str, Any]],
    project_root: Path,
) -> str:
    """Language selector, donation block, optional API usage; returns active language."""
    lang = render_language_selector(transl, location="sidebar")
    add_language_separator(location="sidebar")
    render_sidebar_donation(
        username="geonosislaX",
        translations=transl,
        language=lang,
        qr_image_path=get_default_qr_path(project_root),
    )
    _render_api_usage_sidebar()
    apply_rtl_layout(lang)
    return lang


def _render_api_usage_sidebar() -> None:
    """Optional token usage caption (development / ops)."""
    settings = get_settings()
    if not settings.show_usage_in_ui:
        return
    usage = st.session_state.get("last_api_usage")
    if not usage:
        return
    total = usage.get("total_tokens", "?")
    reasoning = usage.get("reasoning_tokens")
    line = f"API usage (last run): {total} tokens"
    if reasoning is not None:
        line += f" ({reasoning} reasoning)"
    st.sidebar.caption(line)


def current_language(transl: Dict[str, Dict[str, Any]]) -> str:
    """Active UI language (sidebar is rendered in the entry script before pg.run())."""
    lang = get_current_language()
    if lang in transl:
        return lang
    return "English" if "English" in transl else next(iter(transl))
