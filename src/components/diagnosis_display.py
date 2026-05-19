"""
HTML formatting and Streamlit display helpers for diagnosis results.
"""

from typing import Any, Dict, Optional

import streamlit as st

from ..core.ai_client import StructuredDiagnosisOutput

# Default English labels when translation keys are missing
_DEFAULT_LABELS = {
    "dx_primary": "Primary Diagnosis",
    "dx_confidence": "Confidence",
    "dx_differential": "Differential Diagnoses",
    "dx_next_steps": "Recommended Next Steps",
    "dx_considerations": "Important Considerations",
    "dx_reasoning": "Clinical Reasoning",
    "dx_confidence_high": "HIGH",
    "dx_confidence_medium": "MEDIUM",
    "dx_confidence_low": "LOW",
}


def _label(translations: Dict[str, Any], key: str) -> str:
    return str(translations.get(key, _DEFAULT_LABELS.get(key, key)))


def _confidence_label(translations: Dict[str, Any], level: str) -> str:
    key = f"dx_confidence_{level.lower()}"
    return _label(translations, key)


def format_structured_diagnosis_html(
    diagnosis: StructuredDiagnosisOutput,
    translations: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Format structured diagnosis as HTML using translated section titles.

    Args:
        diagnosis: Parsed structured output from OpenAI
        translations: Language-specific strings from translations.json

    Returns:
        HTML string for st.write(..., unsafe_allow_html=True)
    """
    trans = translations or {}
    conf = _confidence_label(trans, diagnosis.confidence_level)

    html_output = f"""
<div style="font-size: 16px; line-height: 1.6;">
    <h3 style="color: #1f77b4;">🔍 {_label(trans, "dx_primary")}</h3>
    <p style="font-size: 18px;"><strong>{diagnosis.primary_diagnosis}</strong></p>
    <p style="font-size: 14px; color: #666;">{_label(trans, "dx_confidence")}: {conf}</p>

    <h3 style="color: #ff7f0e; margin-top: 20px;">🔬 {_label(trans, "dx_differential")}</h3>
    <ul>
"""
    for diff_dx in diagnosis.differential_diagnoses:
        html_output += f"        <li>{diff_dx}</li>\n"

    html_output += f"""    </ul>

    <h3 style="color: #2ca02c; margin-top: 20px;">📋 {_label(trans, "dx_next_steps")}</h3>
    <ol>
"""
    for step in diagnosis.recommended_next_steps:
        html_output += f"        <li>{step}</li>\n"

    html_output += f"""    </ol>

    <h3 style="color: #d62728; margin-top: 20px;">⚠️ {_label(trans, "dx_considerations")}</h3>
    <ul>
"""
    for consideration in diagnosis.important_considerations:
        html_output += f"        <li>{consideration}</li>\n"

    html_output += f"""    </ul>

    <h3 style="color: #9467bd; margin-top: 20px;">💡 {_label(trans, "dx_reasoning")}</h3>
    <p style="background-color: #f0f0f0; padding: 15px; border-radius: 5px;">
        {diagnosis.reasoning}
    </p>
</div>
"""
    return html_output


def render_diagnosis_result(html_content: str, use_expanders: bool = False) -> None:
    """
    Render diagnosis HTML in Streamlit.

    Args:
        html_content: HTML string to display
        use_expanders: If True, wrap long sections in expanders (plain text only)
    """
    st.write(html_content, unsafe_allow_html=True)
