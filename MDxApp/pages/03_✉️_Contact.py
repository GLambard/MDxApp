import os
import sys
from pathlib import Path

import streamlit as st

path_dir = os.path.dirname(__file__)
project_root = Path(path_dir).parent.parent
sys.path.insert(0, str(project_root))

from src.components.localized_pages import render_contact_page, render_page_sidebar
from src.utils.styling import load_main_styles
from src.utils.translations_loader import load_app_translations


def local_css(file_name: str) -> None:
    css_path = Path(path_dir) / file_name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


st.set_page_config(page_title="Contact", page_icon="✉️")
load_main_styles(project_root)

transl = load_app_translations()

lang = render_page_sidebar(transl, project_root)
render_contact_page(transl, lang, st.secrets["email_address"])
local_css("styles/email_form.css")
