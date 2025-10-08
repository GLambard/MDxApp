"""
Language selector component for multi-language support.
Manages language selection and state across page navigation.
"""

from typing import Any, Dict

import streamlit as st


def initialize_language_state(default_language: str = "English") -> None:
    """
    Initialize language-related session state variables.

    Args:
        default_language: Default language to use
    """
    if "lang_tmp" not in st.session_state:
        st.session_state["lang_tmp"] = default_language

    if "lang_changed" not in st.session_state:
        st.session_state["lang_changed"] = False

    if "lang_select" not in st.session_state:
        st.session_state["lang_select"] = default_language


def render_language_selector(
    translations: Dict[str, Dict[str, Any]], location: str = "sidebar", key: str = "lang_select"
) -> str:
    """
    Render language selection dropdown.

    Args:
        translations: Translation dictionary with all languages
        location: Where to render ("sidebar" or "main")
        key: Session state key for the selectbox

    Returns:
        str: Selected language
    """
    # Initialize state if needed
    initialize_language_state()

    # Get available languages
    available_languages = list(translations.keys())

    # Get current language for label
    current_lang = st.session_state.get(key, "English")
    if current_lang not in translations:
        current_lang = "English"

    # Get translated label
    label_key = "language_selection"
    label = translations[current_lang].get(label_key, "Select a language:")

    # Render selectbox in appropriate location
    if location == "sidebar":
        selected_lang = st.sidebar.selectbox(label, options=available_languages, key=key)
    else:
        selected_lang = st.selectbox(label, options=available_languages, key=key)

    # Track language changes
    if selected_lang != st.session_state.get("lang_tmp", "English"):
        st.session_state["lang_tmp"] = selected_lang
        st.session_state["lang_changed"] = True
    else:
        st.session_state["lang_changed"] = False

    return selected_lang


def get_current_language() -> str:
    """
    Get the currently selected language.

    Returns:
        str: Current language name
    """
    lang = st.session_state.get("lang_select", "English")
    return str(lang)


def language_changed() -> bool:
    """
    Check if language was changed in this session.

    Returns:
        bool: True if language was just changed
    """
    changed = st.session_state.get("lang_changed", False)
    return bool(changed)


def clear_language_dependent_state() -> None:
    """
    Clear session state variables that depend on language.
    Useful when language changes to reset form values.
    """
    # List of keys to clear when language changes
    language_dependent_keys = ["gender", "pregnant"]

    for key in language_dependent_keys:
        if key in st.session_state:
            del st.session_state[key]


def handle_language_change() -> None:
    """
    Handle language change event.
    Clears language-dependent state if language was changed.
    """
    if language_changed():
        clear_language_dependent_state()


def render_language_selector_with_header(
    translations: Dict[str, Dict[str, Any]], show_header: bool = False, location: str = "sidebar"
) -> str:
    """
    Render language selector with optional header.

    Args:
        translations: Translation dictionary
        show_header: Whether to show header above selector
        location: Where to render ("sidebar" or "main")

    Returns:
        str: Selected language
    """
    current_lang = get_current_language()

    # Optional header
    if show_header:
        header_text = translations[current_lang].get("language_selection", "Select a language:")
        if location == "sidebar":
            st.sidebar.markdown(
                f"<h3 style='text-align: center; color: black;'>{header_text}</h3>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<h3 style='text-align: center; color: black;'>{header_text}</h3>",
                unsafe_allow_html=True,
            )

    # Render selector
    return render_language_selector(translations, location)


def add_language_separator(location: str = "sidebar") -> None:
    """
    Add a visual separator after language selection.

    Args:
        location: Where to add separator ("sidebar" or "main")
    """
    if location == "sidebar":
        st.sidebar.markdown("---")
    else:
        st.markdown("---")
