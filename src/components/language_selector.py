"""
Language selector component for multi-language support.
Manages language selection and state across page navigation.
"""

from typing import Any, Dict, List

import streamlit as st

from ..utils.locale import sort_languages

# Persists across multipage navigation (widget keys are cleared when a page unmounts).
MDX_LANGUAGE_KEY = "mdx_language"
_LEGACY_WIDGET_KEY = "lang_select"


def initialize_language_state(default_language: str = "English") -> None:
    """Initialize canonical language in session (not tied to a widget key)."""
    if MDX_LANGUAGE_KEY not in st.session_state:
        # Migrate from old widget-only state if present
        if _LEGACY_WIDGET_KEY in st.session_state:
            st.session_state[MDX_LANGUAGE_KEY] = st.session_state[_LEGACY_WIDGET_KEY]
        else:
            st.session_state[MDX_LANGUAGE_KEY] = default_language

    if "lang_changed" not in st.session_state:
        st.session_state["lang_changed"] = False


def get_current_language() -> str:
    """Return the active UI language (same on every page)."""
    initialize_language_state()
    return str(st.session_state.get(MDX_LANGUAGE_KEY, "English"))


def _language_index(available_languages: List[str], current: str) -> int:
    try:
        return available_languages.index(current)
    except ValueError:
        return 0


def render_language_selector(
    translations: Dict[str, Dict[str, Any]], location: str = "sidebar", key: str = "lang_select"
) -> str:
    """
    Render language selection dropdown.

    Args:
        translations: Translation dictionary with all languages
        location: Where to render ("sidebar" or "main")
        key: Ignored (kept for API compatibility); language uses MDX_LANGUAGE_KEY

    Returns:
        str: Selected language
    """
    del key  # Canonical state is MDX_LANGUAGE_KEY, not a widget key
    initialize_language_state()

    available_languages = sort_languages(translations)
    current = get_current_language()
    if current not in translations:
        current = "English"
        st.session_state[MDX_LANGUAGE_KEY] = current

    label = translations[current].get("language_selection", "Select a language:")
    idx = _language_index(available_languages, current)

    # No widget key: index comes from MDX_LANGUAGE_KEY so language survives page changes
    if location == "sidebar":
        selected_lang = st.sidebar.selectbox(label, available_languages, index=idx)
    else:
        selected_lang = st.selectbox(label, available_languages, index=idx)

    if selected_lang != st.session_state.get(MDX_LANGUAGE_KEY):
        st.session_state[MDX_LANGUAGE_KEY] = selected_lang
        st.session_state["lang_changed"] = True
        handle_language_change()
        st.rerun()

    st.session_state["lang_changed"] = False
    return get_current_language()


def language_changed() -> bool:
    """Check if language was changed on the previous interaction."""
    return bool(st.session_state.get("lang_changed", False))


def clear_language_dependent_state() -> None:
    """Clear form widgets that depend on translated option labels."""
    for widget_key in ("gender", "pregnant", "gender_code", "pregnant_code"):
        if widget_key in st.session_state:
            del st.session_state[widget_key]


def handle_language_change() -> None:
    """Reset language-dependent widgets after a language change."""
    if language_changed():
        clear_language_dependent_state()


def render_language_selector_with_header(
    translations: Dict[str, Dict[str, Any]], show_header: bool = False, location: str = "sidebar"
) -> str:
    """Render language selector with optional header."""
    current_lang = get_current_language()

    if show_header:
        header_text = translations[current_lang].get("language_selection", "Select a language:")
        header_html = f'<p class="mdx-donation-title mdx-donation-center">{header_text}</p>'
        if location == "sidebar":
            st.sidebar.markdown(header_html, unsafe_allow_html=True)
        else:
            st.markdown(header_html, unsafe_allow_html=True)

    return render_language_selector(translations, location)


def add_language_separator(location: str = "sidebar") -> None:
    """Add a visual separator after language selection."""
    if location == "sidebar":
        st.sidebar.markdown("---")
    else:
        st.markdown("---")
