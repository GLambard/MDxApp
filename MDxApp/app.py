"""
MDxApp entry point — localized sidebar page names via st.navigation.
Run: streamlit run MDxApp/app.py
"""

import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(app_dir.parent))

from src.ui.streamlit_app import run_mdxapp

run_mdxapp(app_dir)
