"""Reusable UI components for MDxApp."""

from .diagnosis_display import (
    format_structured_diagnosis_html,
    render_diagnosis_result,
    render_structured_diagnosis,
    structured_from_session,
)
from .donation import (
    get_default_qr_path,
    render_donation_button,
    render_donation_qr,
    render_inline_donation,
    render_sidebar_donation,
)
from .language_selector import (
    add_language_separator,
    get_current_language,
    handle_language_change,
    initialize_language_state,
    language_changed,
    render_language_selector,
    render_language_selector_with_header,
)
from .patient_form import (
    build_patient_from_session,
    collect_patient_data,
    render_medical_history_fields,
    render_patient_demographics,
    render_patient_summary,
    validate_minimum_data,
)

__all__ = [
    # Donation components
    "render_donation_button",
    "render_donation_qr",
    "render_sidebar_donation",
    "render_inline_donation",
    "get_default_qr_path",
    # Language selector components
    "initialize_language_state",
    "render_language_selector",
    "get_current_language",
    "language_changed",
    "handle_language_change",
    "render_language_selector_with_header",
    "add_language_separator",
    # Patient form components
    "render_patient_demographics",
    "render_medical_history_fields",
    "collect_patient_data",
    "build_patient_from_session",
    "render_patient_summary",
    "validate_minimum_data",
    # Diagnosis display
    "format_structured_diagnosis_html",
    "render_diagnosis_result",
    "render_structured_diagnosis",
    "structured_from_session",
]
