"""Contact page (navigation labels set in app.py)."""

import sys
from pathlib import Path

import streamlit as st

app_dir = Path(__file__).resolve().parent.parent
project_root = app_dir.parent
sys.path.insert(0, str(project_root))

from src.components.app_shell import current_language
from src.components.localized_pages import render_contact_page
from src.utils.translations_loader import load_app_translations


def _local_css(file_name: str) -> None:
    css_path = Path(__file__).parent / file_name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


transl = load_app_translations()
lang = current_language(transl)
render_contact_page(transl, lang, st.secrets["email_address"])
_local_css("styles/email_form.css")
