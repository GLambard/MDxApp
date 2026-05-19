"""
Patient form component for collecting patient information.
Provides reusable form fields with validation and state management.
"""

from typing import Any, Dict, Optional, Tuple

import streamlit as st
from pydantic import ValidationError

from ..models.patient import PatientData


def format_patient_validation_error(
    translations: Dict[str, Any], error: ValidationError
) -> str:
    """Map Pydantic validation errors to localized, user-friendly messages."""
    for err in error.errors():
        loc = err.get("loc", ())
        field = loc[-1] if loc else None
        err_type = err.get("type", "")
        if field == "symptoms" and err_type in ("string_too_short", "missing"):
            return translations.get(
                "submit_warning",
                "Please enter at least some symptoms before submission.",
            )
        if field == "age":
            return translations.get(
                "error_invalid_age",
                "Please enter a valid age between 0 and 150.",
            )
    return translations.get(
        "error_invalid_patient",
        "Please check the form and try again.",
    )


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

    # Canonical codes in session (language-independent); labels via format_func
    if "gender_code" not in st.session_state:
        st.session_state.gender_code = "male"
    if "pregnant_code" not in st.session_state:
        st.session_state.pregnant_code = "no"

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        gender_code = st.radio(
            f"**{trans['gender']}**",
            options=["male", "female"],
            format_func=lambda code: trans["male"] if code == "male" else trans["female"],
            key="gender_code",
            horizontal=True,
        )

    with col2:
        age = st.number_input(f"**{trans['age']}**", min_value=0, max_value=99, step=1, key="age")

    is_male = gender_code == "male"
    st.session_state.disabled = is_male
    if is_male:
        st.session_state.pregnant_code = "no"

    with col3:
        pregnancy_code = st.radio(
            f"**{trans['pregnant']}**",
            options=["no", "yes"],
            format_func=lambda code: trans["no"] if code == "no" else trans["yes"],
            key="pregnant_code",
            disabled=st.session_state.disabled,
            horizontal=True,
        )

    gender_label = trans["male"] if gender_code == "male" else trans["female"]
    pregnancy_label = trans["no"] if pregnancy_code == "no" else trans["yes"]
    return gender_label, age, pregnancy_label


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
        max_chars=2000,
        help=f":green[**{trans['hist_help']}**]",
    )

    # Symptoms (required)
    symptoms = st.text_input(
        f"**{trans['symptoms']}** *{trans['symp_example']}*",
        placeholder=trans["symp_ph"],
        key="symptoms",
        max_chars=2000,
        help=f":green[**{trans['symp_help']}**]",
    )

    # Examination findings
    exam = st.text_input(
        f"**{trans['exam']}** *{trans['exam_example']}*",
        placeholder=trans["exam_ph"],
        key="exam",
        max_chars=2000,
        help=f":green[**{trans['exam_help']}**]",
    )

    # Laboratory results
    lab_results = st.text_input(
        f"**{trans['lab']}** *{trans['lab_example']}*",
        placeholder=trans["lab_ph"],
        key="labresults",
        max_chars=2000,
        help=f":green[**{trans['lab_help']}**]",
    )

    # Medications (optional, Phase 2E)
    medications = st.text_input(
        f"**{trans.get('medications', 'Medications')}** *{trans.get('meds_example', '(optional)')}*",
        placeholder=trans.get("meds_ph", "none"),
        key="medications",
        max_chars=2000,
        help=f":green[**{trans.get('meds_help', 'List current medications')}**]",
    )

    return {
        "history": history,
        "symptoms": symptoms,
        "exam": exam,
        "lab_results": lab_results,
        "medications": medications,
    }


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
    medications = medical_data.get("medications") or None
    medications = medications if medications else None

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
            medications=medications,
            language=language,
        )
        return patient_data

    except ValidationError as e:
        st.warning(format_patient_validation_error(trans, e))
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
    symptoms = (
        patient_data.symptoms
        if patient_data.symptoms and patient_data.symptoms.strip()
        else none_text
    )
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


def build_patient_from_session(
    translations: Dict[str, Any], language: str = "English"
) -> Optional[PatientData]:
    """
    Build PatientData from current Streamlit session state (after form widgets rendered).

    Args:
        translations: Translation dictionary for current language
        language: Current language key

    Returns:
        PatientData if valid, None on validation error
    """
    trans = translations
    history = st.session_state.get("context") or None
    symptoms = st.session_state.get("symptoms") or ""
    exam = st.session_state.get("exam") or None
    lab_results = st.session_state.get("labresults") or None
    medications = st.session_state.get("medications") or None

    try:
        gender_code = st.session_state.get("gender_code", "male")
        pregnant_code = st.session_state.get("pregnant_code", "no")
        gender_label = trans["male"] if gender_code == "male" else trans["female"]
        pregnant_label = trans["no"] if pregnant_code == "no" else trans["yes"]
        return PatientData(
            gender=gender_label,
            age=int(st.session_state.get("age", 0)),
            is_pregnant=pregnant_label,
            history=history if history else None,
            symptoms=symptoms,
            exam_findings=exam if exam else None,
            lab_results=lab_results if lab_results else None,
            medications=medications if medications else None,
            language=language,
        )
    except ValidationError as e:
        st.warning(format_patient_validation_error(trans, e))
        return None


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
        st.warning(
            translations.get(
                "error_invalid_patient",
                "Please check the form and try again.",
            )
        )
        return False

    if not patient_data.has_minimum_data():
        st.warning(
            translations.get(
                "submit_warning",
                "Please enter at least some symptoms before submission.",
            )
        )
        return False

    return True
