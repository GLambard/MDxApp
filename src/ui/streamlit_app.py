"""
MDxApp Streamlit entry bootstrap (shared by app.py and legacy main script).
"""

from pathlib import Path

import streamlit as st

from ..components.app_shell import build_navigation_pages, render_app_sidebar
from ..components.language_selector import initialize_language_state
from ..config.settings import log_openai_model_config
from ..utils.styling import load_main_styles
from ..utils.translations_loader import load_app_translations


def run_mdxapp(app_dir: Path) -> None:
    """Configure app shell, localized sidebar nav labels, and run the active page."""
    project_root = app_dir.parent
    transl = load_app_translations()

    st.set_page_config(page_title="MDxApp", page_icon="🏥", layout="wide")
    log_openai_model_config()
    load_main_styles(project_root)
    initialize_language_state()

    with st.sidebar:
        lang = render_app_sidebar(transl, project_root)

    pg = st.navigation(build_navigation_pages(transl, lang, app_dir))
    pg.run()
