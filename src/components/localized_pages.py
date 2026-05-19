"""
Localized About and Contact page content (driven by Assets/translations.json).
"""

from pathlib import Path
from typing import Any, Dict

import streamlit as st
from streamlit.components.v1 import html

from ..config.settings import Settings
from ..components.donation import get_default_qr_path, render_sidebar_donation
from ..components.language_selector import (
    add_language_separator,
    render_language_selector,
)
from ..utils.locale import apply_rtl_layout


def _t(trans: Dict[str, Any], key: str, **fmt: Any) -> str:
    """Translation with optional format placeholders."""
    text = str(trans.get(key, key))
    if fmt:
        try:
            return text.format(**fmt)
        except KeyError:
            return text
    return text


def render_page_sidebar(
    transl: Dict[str, Dict[str, Any]],
    project_root: Path,
) -> str:
    """Language selector + donation block; returns active language."""
    lang = render_language_selector(transl, location="sidebar")
    add_language_separator(location="sidebar")
    render_sidebar_donation(
        username="geonosislaX",
        translations=transl,
        language=lang,
        qr_image_path=get_default_qr_path(project_root),
    )
    apply_rtl_layout(lang)
    return lang


def render_about_page(
    transl: Dict[str, Dict[str, Any]],
    lang: str,
    settings: Settings,
) -> None:
    """Render localized About content."""
    trans = transl.get(lang, transl["English"])

    st.header(_t(trans, "page_about_title"))

    st.markdown(f"### {_t(trans, 'page_about_what_heading')}")
    st.markdown(_t(trans, "page_about_what_text", model=settings.openai_model))

    st.markdown(f"### {_t(trans, 'page_about_features_heading', version=settings.app_version)}")
    for key in (
        "page_about_feature_1",
        "page_about_feature_2",
        "page_about_feature_3",
        "page_about_feature_4",
        "page_about_feature_5",
        "page_about_feature_6",
    ):
        st.markdown(f"- {_t(trans, key)}")

    st.markdown(f"### {_t(trans, 'page_about_excluded_heading')}")
    for key in (
        "page_about_excluded_1",
        "page_about_excluded_2",
        "page_about_excluded_3",
    ):
        st.markdown(f"- {_t(trans, key)}")

    st.markdown(f"### {_t(trans, 'page_about_support_heading')}")
    st.markdown(_t(trans, "page_about_support_text"))

    st.markdown(f"### {_t(trans, 'page_about_versions_heading')}")
    st.markdown(_t(trans, "page_about_versions_table"), unsafe_allow_html=True)

    st.markdown(f"### {_t(trans, 'page_about_sources_heading')}")
    st.markdown(_t(trans, "page_about_sources_text"))

    st.markdown(
        f"### :rotating_light: {_t(trans, 'page_about_caution_heading')} :rotating_light:"
    )
    st.markdown(_t(trans, "caution_message"))

    st.markdown(f"### {_t(trans, 'page_about_dev_heading')}")
    st.markdown(_t(trans, "page_about_dev_message"))

    html(
        """
        <a class="github-button" href="https://github.com/GLambard/MDxApp" data-show-count="true"
           aria-label="Follow @GLambard on GitHub">Follow @GLambard</a>
        <script async defer src="https://buttons.github.io/buttons.js"></script>
        <a class="twitter-follow-button" href="https://twitter.com/gamlambard">Follow @gamlambard</a>
        <script async defer src="https://platform.twitter.com/widgets.js"></script>
        """
    )


def render_contact_page(
    transl: Dict[str, Dict[str, Any]],
    lang: str,
    email_address: str,
) -> None:
    """Render localized Contact form (FormSubmit.co)."""
    trans = transl.get(lang, transl["English"])

    st.header(_t(trans, "page_contact_title"))

    contact_form = f"""
    <form action="https://formsubmit.co/{email_address}" method="POST" dir="{'rtl' if lang == 'العربية' else 'ltr'}">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="{_t(trans, 'contact_form_name_ph')}" required>
         <input type="email" name="email" placeholder="{_t(trans, 'contact_form_email_ph')}" required>
         <textarea name="message" placeholder="{_t(trans, 'contact_form_message_ph')}"></textarea>
         <button type="submit">{_t(trans, 'contact_form_submit')}</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
