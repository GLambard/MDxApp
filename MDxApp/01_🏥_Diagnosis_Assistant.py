"""
Medical Diagnosis Assistant — main Streamlit page.
Thin orchestrator: components + DiagnosisService (no inline OpenAI calls).
"""

import json
import os
import sys
from pathlib import Path

import streamlit as st

path = os.path.dirname(__file__)
project_root = Path(path).parent
sys.path.insert(0, str(project_root))

from src.components.diagnosis_display import render_diagnosis_result
from src.components.donation import (
    get_default_qr_path,
    render_inline_donation,
    render_sidebar_donation,
)
from src.components.language_selector import add_language_separator, render_language_selector
from src.components.patient_form import (
    build_patient_from_session,
    render_medical_history_fields,
    render_patient_demographics,
    render_patient_summary,
    validate_minimum_data,
)
from src.services.diagnosis_service import get_diagnosis_service
from src.utils.styling import load_main_styles

# Load translations
with open(path + "/../Assets/translations.json", encoding="utf-8") as f:
    transl = json.load(f)

# Preserve widget state across pages
for k, v in st.session_state.items():
    st.session_state[k] = v

st.set_page_config(page_title="Diagnosis_Assistant", page_icon="🏥", layout="wide")
load_main_styles(project_root)

lang = render_language_selector(transl, location="sidebar")
add_language_separator(location="sidebar")

with st.sidebar:
    render_sidebar_donation(
        username="geonosislaX",
        translations=transl,
        language=lang,
        qr_image_path=get_default_qr_path(project_root),
    )

logo_name = path + "/../Materials/MDxApp_logo_v2_256.png"
t1, t2 = st.columns([1, 3], gap="large")
with t1:
    st.image(logo_name, caption="", width=256)
with t2:
    st.header(f"**{transl[lang]['page1_header']}**")
    st.write(
        f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["page1_subheader"]}</p>',
        unsafe_allow_html=True,
    )

st.markdown("", unsafe_allow_html=True)
st.markdown("---")
st.write(
    f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["htu_0"]}</p>'
    f'<p style="font-size:18px;">1. {transl[lang]["htu_1"]}<br/>'
    f"2. {transl[lang]['htu_2']}<br/>"
    f"3. {transl[lang]['htu_3']}</p>",
    unsafe_allow_html=True,
)

st.subheader(f":black_nib: **{transl[lang]['report_header']}**")
render_patient_demographics(transl[lang], language=lang)
render_medical_history_fields(transl[lang], language=lang)

patient_data = build_patient_from_session(transl[lang], language=lang)

st.subheader(f":clipboard: **{transl[lang]['summary']}**")
if patient_data:
    st.write(
        render_patient_summary(patient_data, transl[lang], language=lang), unsafe_allow_html=True
    )

st.write("")
submit_button = st.button(
    f"**{transl[lang]['submit']}**",
    help=f":green[**{transl[lang]['submit_help']}**]",
)
st.write("")

st.subheader(f":computer: :speech_balloon: :pill: **{transl[lang]['diagnostic']}**")

if submit_button:
    if not validate_minimum_data(patient_data, transl[lang]):
        pass
    elif patient_data:
        with st.spinner(transl[lang]["submit_wait"]):
            try:
                service = get_diagnosis_service(translations=transl)
                result = service.run(patient_data, lang, translations=transl[lang])

                if result.success and result.html_content:
                    st.session_state.diagnostic = result.html_content
                    st.write("")
                    render_diagnosis_result(result.html_content)
                elif result.error_message:
                    st.error(f"OpenAI API Error: {result.error_message}")
                    st.write(
                        f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_response"]}</p>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.write(
                        f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_response"]}</p>',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"### :rotating_light: **{transl[lang]['caution']}** :rotating_light:\n"
                    f"{transl[lang]['caution_message']}",
                    unsafe_allow_html=True,
                )
                render_inline_donation(
                    username="geonosislaX",
                    translations=transl,
                    language=lang,
                    qr_image_path=get_default_qr_path(project_root),
                    show_separator=True,
                    invest_message=True,
                )
            except Exception as exc:
                st.error(f"OpenAI API Error: {exc}")
                st.write(
                    f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_response"]}</p>',
                    unsafe_allow_html=True,
                )
else:
    if "diagnostic" in st.session_state:
        render_diagnosis_result(st.session_state.diagnostic.replace("<|im_end|>", ""))
    else:
        st.write(
            f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_diagnostic"]}</p>',
            unsafe_allow_html=True,
        )
