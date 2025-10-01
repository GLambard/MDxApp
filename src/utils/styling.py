"""
Styling utilities for Streamlit applications.
Handles loading and applying CSS stylesheets.
"""

from pathlib import Path
from typing import Optional

import streamlit as st

from ..utils.logger import get_logger


def load_css(css_file: Path) -> None:
    """
    Load and apply CSS from an external file.

    Args:
        css_file: Path to the CSS file

    Raises:
        FileNotFoundError: If CSS file doesn't exist
    """
    logger = get_logger(__name__)

    if not css_file.exists():
        logger.error(f"CSS file not found: {css_file}")
        raise FileNotFoundError(f"CSS file not found: {css_file}")

    try:
        with open(css_file, encoding="utf-8") as f:
            css_content = f.read()

        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        logger.debug(f"Loaded CSS from: {css_file}")

    except Exception as e:
        logger.error(f"Error loading CSS file {css_file}: {e}")
        raise


def load_multiple_css(css_files: list[Path]) -> None:
    """
    Load multiple CSS files in order.

    Args:
        css_files: List of paths to CSS files
    """
    for css_file in css_files:
        load_css(css_file)


def apply_inline_css(css_content: str) -> None:
    """
    Apply inline CSS content.
    Useful for dynamic styling or page-specific styles.

    Args:
        css_content: CSS content as string
    """
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def get_styles_directory(base_path: Optional[Path] = None) -> Path:
    """
    Get the path to the styles directory.

    Args:
        base_path: Optional base path (defaults to MDxApp/pages/styles)

    Returns:
        Path: Path to styles directory
    """
    if base_path:
        return base_path / "pages" / "styles"

    # Default: relative to current file location
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    return project_root / "MDxApp" / "pages" / "styles"


def load_main_styles(base_path: Optional[Path] = None) -> None:
    """
    Load all main application stylesheets.

    Args:
        base_path: Optional base path to project root
    """
    styles_dir = get_styles_directory(base_path)

    # Load main CSS
    main_css = styles_dir / "main.css"
    if main_css.exists():
        load_css(main_css)


def apply_custom_theme() -> None:
    """
    Apply custom theme configuration using data attributes.
    This is more stable across Streamlit versions than class-based styling.
    """
    # Using data attributes for more stable styling
    theme_css = """
    /* Custom theme using data attributes */

    /* Text inputs with bold labels */
    [data-testid="stTextInput"] label {
        font-weight: 600;
    }

    /* Number inputs with bold labels */
    [data-testid="stNumberInput"] label {
        font-weight: 600;
    }

    /* Radio buttons with bold labels */
    [data-testid="stRadio"] label {
        font-weight: 600;
    }

    /* Selectbox with bold labels */
    [data-testid="stSelectbox"] label {
        font-weight: 600;
    }

    /* Buttons with custom styling */
    [data-testid="stButton"] button {
        font-weight: 600;
        border-radius: 4px;
    }
    """

    apply_inline_css(theme_css)


def hide_streamlit_elements() -> None:
    """
    Hide default Streamlit elements (hamburger menu, footer, etc.).
    Use with caution - may affect user experience.
    """
    hide_css = """
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    """

    apply_inline_css(hide_css)


def apply_mobile_responsive_styles() -> None:
    """
    Apply mobile-responsive CSS for better mobile experience.
    """
    mobile_css = """
    /* Mobile responsive styles */
    @media (max-width: 768px) {
        /* Reduce font sizes on mobile */
        [data-testid="stMarkdownContainer"] p {
            font-size: 14px !important;
        }

        /* Stack columns vertically */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }

        /* Full width elements */
        [data-testid="stButton"] button {
            width: 100% !important;
        }
    }
    """

    apply_inline_css(mobile_css)
