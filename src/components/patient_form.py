"""
Patient form component for collecting patient information.
Provides reusable form fields with validation and state management.
"""

from typing import Any, Dict, Optional, Tuple

import streamlit as st
from pydantic import ValidationError

from ..models.patient import PatientData


def render_patient_demographics(
    translations: Dict[str, Any], language: str = "English"
) -> Tuple[str, int, str]:
    """
    Render patient demographics section (gender, age, pregnancy).

    Args:
        translations: Translation dictionary for current language
        language: Current language

    Returns:
        Tuple of (gender, age, pregnancy_status)
    """
    trans = translations

    # Initialize session state for disabled field
    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    # Create gender and pregnancy option lists
    genders_list = [trans["male"], trans["female"]]
    pregnant_list = [trans["no"], trans["yes"]]

    # Create three columns
    col1, col2, col3 = st.columns(3, gap="large")

    # Gender selector
    with col1:
        # Handle language change by resetting gender if needed
        if "lang_changed" in st.session_state and st.session_state["lang_changed"]:
            if "gender" in st.session_state:
                del st.session_state["gender"]

        if "gender" not in st.session_state:
            st.session_state["gender"] = genders_list[0]

        gender = st.radio(f"**{trans['gender']}**", genders_list, key="gender")

    # Age selector
    with col2:
        age = st.number_input(f"**{trans['age']}**", min_value=0, max_value=99, step=1, key="age")

    # Pregnancy selector (disabled for males)
    # Check if male and disable pregnancy field
    if st.session_state.gender == trans["male"]:
        st.session_state.disabled = True
        if "pregnant" in st.session_state:
            st.session_state["pregnant"] = trans["no"]
    else:
        st.session_state.disabled = False

    with col3:
        # Handle language change
        if "lang_changed" in st.session_state and st.session_state["lang_changed"]:
            if "pregnant" in st.session_state:
                del st.session_state["pregnant"]

        if "pregnant" not in st.session_state:
            st.session_state["pregnant"] = pregnant_list[0]

        pregnancy = st.radio(
            f"**{trans['pregnant']}**",
            pregnant_list,
            disabled=st.session_state.disabled,
            key="pregnant",
        )

    return gender, age, pregnancy


def render_medical_history_fields(
    translations: Dict[str, Any], language: str = "English"
) -> Dict[str, str]:
    """
    Render medical history input fields.

    Args:
        translations: Translation dictionary for current language
        language: Current language

    Returns:
        Dictionary with history, symptoms, exam, lab_results
    """
    trans = translations

    # History/Context
    history = st.text_input(
        f"**{trans['history']}** *{trans['hist_example']}*",
        placeholder=trans["hist_ph"],
        key="context",
        max_chars=250,
        help=f":green[**{trans['hist_help']}**]",
    )

    # Symptoms (required)
    symptoms = st.text_input(
        f"**{trans['symptoms']}** *{trans['symp_example']}*",
        placeholder=trans["symp_ph"],
        key="symptoms",
        max_chars=250,
        help=f":green[**{trans['symp_help']}**]",
    )

    # Examination findings
    exam = st.text_input(
        f"**{trans['exam']}** *{trans['exam_example']}*",
        placeholder=trans["exam_ph"],
        key="exam",
        max_chars=250,
        help=f":green[**{trans['exam_help']}**]",
    )

    # Laboratory results
    lab_results = st.text_input(
        f"**{trans['lab']}** *{trans['lab_example']}*",
        placeholder=trans["lab_ph"],
        key="labresults",
        max_chars=250,
        help=f":green[**{trans['lab_help']}**]",
    )

    return {"history": history, "symptoms": symptoms, "exam": exam, "lab_results": lab_results}


def collect_patient_data(
    translations: Dict[str, Any], language: str = "English"
) -> Optional[PatientData]:
    """
    Collect and validate patient data from form.

    Args:
        translations: Translation dictionary
        language: Current language

    Returns:
        PatientData: Validated patient data, or None if validation fails
    """
    trans = translations

    # Get demographics
    gender, age, pregnancy = render_patient_demographics(trans, language)

    # Get medical history
    medical_data = render_medical_history_fields(trans, language)

    # Convert empty strings to None
    history = medical_data["history"] if medical_data["history"] else None
    symptoms = medical_data["symptoms"] if medical_data["symptoms"] else ""
    exam = medical_data["exam"] if medical_data["exam"] else None
    lab_results = medical_data["lab_results"] if medical_data["lab_results"] else None

    # Create PatientData with validation
    try:
        patient_data = PatientData(
            gender=gender,
            age=age,
            is_pregnant=pregnancy,
            history=history,
            symptoms=symptoms,
            exam_findings=exam,
            lab_results=lab_results,
            language=language,
        )
        return patient_data

    except ValidationError as e:
        st.error(f"Validation error: {e}")
        return None


def render_patient_summary(
    patient_data: PatientData, translations: Dict[str, Any], language: str = "English"
) -> str:
    """
    Render HTML summary of patient data for display.

    Args:
        patient_data: Patient data to summarize
        translations: Translation dictionary
        language: Current language

    Returns:
        str: HTML formatted summary
    """
    trans = translations
    none_text = trans.get("none", "none")

    # Get display values
    history = patient_data.history if patient_data.history else none_text
    symptoms = patient_data.symptoms
    exam = patient_data.exam_findings if patient_data.exam_findings else none_text
    lab = patient_data.lab_results if patient_data.lab_results else none_text

    # Build HTML summary
    summary = (
        '<p style="font-size:18px;">'
        f'<b>{trans["vissum_patient"]}</b>'
        f'{patient_data.gender}, {patient_data.age}{trans["vissum_yrsold"]}<br/>'
        f'<b>{trans["vissum_pregnancy"]}</b>{patient_data.is_pregnant}<br/>'
        f'<b>{trans["vissum_history"]}</b>{history}<br/>'
        f'<b>{trans["vissum_symp"]}</b>{symptoms}<br/>'
        f'<b>{trans["vissum_exam"]}</b>{exam}<br/>'
        f'<b>{trans["vissum_lab"]}</b>{lab}<br/>'
        "</p>"
    )

    return summary


def validate_minimum_data(
    patient_data: Optional[PatientData], translations: Dict[str, Any]
) -> bool:
    """
    Validate that patient has minimum required data.

    Args:
        patient_data: Patient data to validate
        translations: Translation dictionary for error messages

    Returns:
        bool: True if valid, False otherwise (displays error)
    """
    if patient_data is None:
        st.error("Patient data is invalid")
        return False

    if not patient_data.has_minimum_data():
        none_text = translations.get("none", "none")
        if patient_data.symptoms == none_text or not patient_data.symptoms.strip():
            st.write(
                f'<p style="font-weight: bold; font-size:18px;">'
                f"{translations['submit_warning']}</p>",
                unsafe_allow_html=True,
            )
            return False

    return True
