"""
Donation component for Buy Me a Coffee integration.
Provides reusable donation button and QR code display.
"""

from pathlib import Path
from typing import Optional

import streamlit as st
from streamlit.components.v1 import html


def render_donation_button(
    username: str = "geonosislaX", text: str = "Buy me a coffee", color: str = "#FFDD00"
) -> None:
    """
    Render Buy Me a Coffee button using HTML/JavaScript.

    Args:
        username: Buy Me a Coffee username
        text: Button text
        color: Button background color (hex)
    """
    button_html = f"""
    <script type="text/javascript"
            src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js"
            data-name="bmc-button"
            data-slug="{username}"
            data-color="{color}"
            data-emoji=""
            data-font="Cookie"
            data-text="{text}"
            data-outline-color="#000000"
            data-font-color="#000000"
            data-coffee-color="#ffffff">
    </script>
    """

    html(button_html, height=70, width=220)


def render_donation_qr(qr_image_path: Path, caption: str = "", width: int = 220) -> None:
    """
    Render QR code image for donations.

    Args:
        qr_image_path: Path to QR code image
        caption: Optional image caption
        width: Image width in pixels
    """
    if qr_image_path.exists():
        st.image(str(qr_image_path), caption=caption, width=width)
    else:
        st.warning(f"QR code image not found: {qr_image_path}")


def render_sidebar_donation(
    username: str = "geonosislaX",
    translations: dict = None,
    language: str = "English",
    qr_image_path: Optional[Path] = None,
) -> None:
    """
    Render complete donation section in sidebar.
    Includes header, button, and QR code.

    Args:
        username: Buy Me a Coffee username
        translations: Translation dictionary
        language: Current language
        qr_image_path: Optional path to QR code image
    """
    # Use default translations if not provided
    if translations is None:
        translations = {
            language: {
                "bmc_0": "Let's keep MDxApp free!",
                "bmc_1": "By clicking here:",
                "bmc_2": "Or use this QR code:",
            }
        }

    trans = translations.get(language, translations.get("English", {}))

    # Header
    st.markdown(
        f"<h3 style='text-align: center; color: black;'>{trans.get('bmc_0', 'Support MDxApp')}</h3>",
        unsafe_allow_html=True,
    )

    # Button text
    st.markdown(
        f"<h4 style='text-align: left; color: black;'>{trans.get('bmc_1', 'By clicking here:')}</h4>",
        unsafe_allow_html=True,
    )

    # Button
    render_donation_button(username=username)

    # QR code section
    st.markdown(
        f"<h4 style='text-align: left; color: black;'>{trans.get('bmc_2', 'Or use this QR code:')}</h4>",
        unsafe_allow_html=True,
    )

    # QR code image
    if qr_image_path:
        render_donation_qr(qr_image_path)


def render_inline_donation(
    username: str = "geonosislaX",
    translations: dict = None,
    language: str = "English",
    qr_image_path: Optional[Path] = None,
    show_separator: bool = True,
    invest_message: bool = True,
) -> None:
    """
    Render donation section inline (in main content area).
    Typically shown after diagnosis results.

    Args:
        username: Buy Me a Coffee username
        translations: Translation dictionary
        language: Current language
        qr_image_path: Optional path to QR code image
        show_separator: Show horizontal separator before donation section
        invest_message: Show investment/support message
    """
    # Use default translations if not provided
    if translations is None:
        translations = {
            language: {
                "invest": "Invest in your health, and support our mission!",
                "bmc_1": "By clicking here:",
                "bmc_2": "Or use this QR code:",
            }
        }

    trans = translations.get(language, translations.get("English", {}))

    # Separator
    if show_separator:
        st.markdown("---")

    # Investment message
    if invest_message:
        st.markdown(
            f"<h4 style='text-align: left; color: black;'>{trans.get('invest', 'Support MDxApp!')}</h4>",
            unsafe_allow_html=True,
        )

    # Button section
    st.markdown(
        f"<h5 style='text-align: left; color: black;'>{trans.get('bmc_1', 'By clicking here:')}</h5>",
        unsafe_allow_html=True,
    )

    render_donation_button(username=username)

    # QR code section
    st.markdown(
        f"<h5 style='text-align: left; color: black;'>{trans.get('bmc_2', 'Or use this QR code:')}</h5>",
        unsafe_allow_html=True,
    )

    if qr_image_path:
        render_donation_qr(qr_image_path)


# Convenience function for getting QR path
def get_default_qr_path(base_path: Optional[Path] = None) -> Path:
    """
    Get default path to QR code image.

    Args:
        base_path: Optional base path to project root

    Returns:
        Path: Path to QR code image
    """
    if base_path:
        return base_path / "Materials" / "bmc_qr.png"

    # Default: relative to current file
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    return project_root / "Materials" / "bmc_qr.png"
