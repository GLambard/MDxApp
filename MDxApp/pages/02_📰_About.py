import os
import sys
from pathlib import Path

import streamlit as st

path = os.path.dirname(__file__)
project_root = Path(path).parent.parent
sys.path.insert(0, str(project_root))

from src.components.localized_pages import render_about_page, render_page_sidebar
from src.config.settings import get_settings
from src.utils.styling import load_main_styles
from src.utils.translations_loader import load_app_translations

st.set_page_config(page_title="About", page_icon="📰", layout="wide")
load_main_styles(project_root)

transl = load_app_translations()

settings = get_settings()
lang = render_page_sidebar(transl, project_root)
render_about_page(transl, lang, settings)
