"""About page (navigation labels set in app.py)."""

import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
project_root = app_dir.parent
sys.path.insert(0, str(project_root))

from src.components.app_shell import current_language
from src.components.localized_pages import render_about_page
from src.config.settings import get_settings
from src.utils.translations_loader import load_app_translations

transl = load_app_translations()
lang = current_language(transl)
render_about_page(transl, lang, get_settings())
