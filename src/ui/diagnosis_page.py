"""
Diagnosis Assistant page body (sidebar and navigation handled by app entry).
"""

from pathlib import Path

import streamlit as st

from ..components.diagnosis_display import (
    render_diagnosis_result,
    render_pdf_download_button,
    structured_from_session,
)
from ..components.donation import get_default_qr_path, render_inline_donation
from ..components.image_upload import render_image_upload
from ..components.patient_form import (
    build_patient_from_session,
    render_medical_history_fields,
    render_patient_demographics,
    render_patient_summary,
    validate_minimum_data,
)
from ..config.settings import get_settings
from ..services.diagnosis_service import get_diagnosis_service


def _persist_diagnosis_result(result) -> None:
    """Store diagnosis in session and reset PDF cache for a fresh download widget."""
    st.session_state.diagnostic = result.html_content
    st.session_state.diagnostic_structured = (
        result.structured.model_dump() if result.structured else None
    )
    st.session_state.diagnostic_fallback = result.used_plain_fallback
    if result.metadata and result.metadata.get("usage"):
        st.session_state.last_api_usage = result.metadata["usage"]
    for _pdf_key in ("mdx_pdf_download", "mdx_pdf_bytes", "mdx_pdf_cache_meta"):
        st.session_state.pop(_pdf_key, None)


def _render_diagnosis_footer(lang: str, transl: dict, project_root: Path) -> None:
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


def _render_stored_diagnosis(
    patient_data,
    lang: str,
    transl: dict,
    project_root: Path,
) -> bool:
    if "diagnostic" not in st.session_state:
        return False

    structured = structured_from_session(st.session_state.get("diagnostic_structured"))
    html = st.session_state.diagnostic.replace("<|im_end|>", "")
    st.write("")
    render_diagnosis_result(
        html_content=html,
        structured=structured,
        translations=transl[lang],
        used_plain_fallback=st.session_state.get("diagnostic_fallback", False),
    )
    if patient_data:
        render_pdf_download_button(
            patient=patient_data,
            translations=transl[lang],
            structured=structured,
            plain_html=html,
            logo_path=project_root / "Materials" / "MDxApp_logo_v2_256.png",
        )
    _render_diagnosis_footer(lang, transl, project_root)
    return True


def render_diagnosis_page(
    project_root: Path,
    transl: dict,
    lang: str,
) -> None:
    """Main diagnosis form and results."""
    logo_path = project_root / "Materials" / "MDxApp_logo_v2_256.png"
    t1, t2 = st.columns([1, 3], gap="large")
    with t1:
        st.image(str(logo_path), caption="", width=256)
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

    settings = get_settings()
    image_bytes, image_mime = None, None
    if settings.enable_medical_imaging:
        image_bytes, image_mime, _ = render_image_upload(transl[lang])

    patient_data = build_patient_from_session(transl[lang], language=lang)

    st.subheader(f":clipboard: **{transl[lang]['summary']}**")
    if patient_data:
        st.write(
            render_patient_summary(patient_data, transl[lang], language=lang),
            unsafe_allow_html=True,
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
                    result = service.run(
                        patient_data,
                        lang,
                        translations=transl[lang],
                        image_bytes=image_bytes,
                        image_mime_type=image_mime,
                    )

                    if result.success and result.html_content:
                        _persist_diagnosis_result(result)
                    elif result.error_message:
                        st.error(f"{transl[lang]['error_openai_prefix']}: {result.error_message}")
                        st.write(
                            f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_response"]}</p>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.write(
                            f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_response"]}</p>',
                            unsafe_allow_html=True,
                        )
                except Exception as exc:
                    st.error(f"{transl[lang]['error_openai_prefix']}: {exc}")
                    st.write(
                        f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_response"]}</p>',
                        unsafe_allow_html=True,
                    )

            if not _render_stored_diagnosis(patient_data, lang, transl, project_root):
                _render_diagnosis_footer(lang, transl, project_root)
    elif not _render_stored_diagnosis(patient_data, lang, transl, project_root):
        st.write(
            f'<p style="font-weight: bold; font-size:18px;">{transl[lang]["no_diagnostic"]}</p>',
            unsafe_allow_html=True,
        )
