"""Diagnosis Assistant page (navigation labels set in app.py)."""

import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
project_root = app_dir.parent
sys.path.insert(0, str(project_root))

import streamlit as st

from src.components.app_shell import current_language
from src.ui.diagnosis_page import render_diagnosis_page
from src.utils.translations_loader import load_app_translations

transl = load_app_translations()
lang = current_language(transl)
render_diagnosis_page(project_root, transl, lang)
