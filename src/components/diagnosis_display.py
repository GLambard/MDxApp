"""
HTML formatting and Streamlit display helpers for diagnosis results.
"""

import html as html_lib
from typing import Any, Dict, Optional

import streamlit as st

from ..core.ai_client import StructuredDiagnosisOutput

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
    "dx_fallback_notice": "Structured format unavailable; showing plain-text diagnosis.",
    "dx_icd10": "ICD-10",
    "dx_references": "References",
    "dx_evidence_disclaimer": "References are for education only; verify with a clinician.",
    "dx_imaging": "Imaging findings",
    "dx_drug_alerts": "Medication alerts",
    "dx_download_pdf": "Download PDF report",
}


def _label(translations: Dict[str, Any], key: str) -> str:
    return str(translations.get(key, _DEFAULT_LABELS.get(key, key)))


def _confidence_label(translations: Dict[str, Any], level: str) -> str:
    key = f"dx_confidence_{level.lower()}"
    return _label(translations, key)


def _esc(text: str) -> str:
    return html_lib.escape(text, quote=False)


def _confidence_badge_html(translations: Dict[str, Any], level: str) -> str:
    """Colored badge for confidence level (high / medium / low)."""
    lvl = level.lower()
    if lvl not in ("high", "medium", "low"):
        lvl = "medium"
    label = _esc(_confidence_label(translations, lvl))
    return (
        f'<span class="mdx-confidence-badge mdx-confidence-{lvl}">'
        f'{_esc(_label(translations, "dx_confidence"))}: {label}</span>'
    )


def format_structured_diagnosis_html(
    diagnosis: StructuredDiagnosisOutput,
    translations: Optional[Dict[str, Any]] = None,
) -> str:
    """Format structured diagnosis as HTML (export / session fallback)."""
    trans = translations or {}
    badge = _confidence_badge_html(trans, diagnosis.confidence_level)

    parts = [
        '<div style="font-size: 16px; line-height: 1.6;">',
        f'<h3 style="color: #1f77b4;">🔍 {_esc(_label(trans, "dx_primary"))}</h3>',
        f'<p style="font-size: 18px;"><strong>{_esc(diagnosis.primary_diagnosis)}</strong></p>',
        f"<p>{badge}</p>",
        f'<h3 style="color: #ff7f0e; margin-top: 20px;">🔬 {_esc(_label(trans, "dx_differential"))}</h3>',
        "<ul>",
    ]
    for diff_dx in diagnosis.differential_diagnoses:
        parts.append(f"<li>{_esc(diff_dx)}</li>")
    parts.extend(
        [
            "</ul>",
            f'<h3 style="color: #2ca02c; margin-top: 20px;">📋 {_esc(_label(trans, "dx_next_steps"))}</h3>',
            "<ol>",
        ]
    )
    for step in diagnosis.recommended_next_steps:
        parts.append(f"<li>{_esc(step)}</li>")
    parts.extend(
        [
            "</ol>",
            f'<h3 style="color: #d62728; margin-top: 20px;">⚠️ {_esc(_label(trans, "dx_considerations"))}</h3>',
            "<ul>",
        ]
    )
    for consideration in diagnosis.important_considerations:
        parts.append(f"<li>{_esc(consideration)}</li>")
    parts.extend(
        [
            "</ul>",
            f'<h3 style="color: #9467bd; margin-top: 20px;">💡 {_esc(_label(trans, "dx_reasoning"))}</h3>',
            f'<p class="mdx-clinical-reasoning" style="background-color: #f0f0f0; color: #262730; '
            f'padding: 15px; border-radius: 5px; border-left: 4px solid #9467bd;">'
            f"{_esc(diagnosis.reasoning)}</p>",
            "</div>",
        ]
    )
    return "\n".join(parts)


def render_structured_diagnosis(
    diagnosis: StructuredDiagnosisOutput,
    translations: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Render structured diagnosis with native Streamlit widgets (expanders, badges).
    """
    trans = translations or {}

    st.markdown(
        f"#### 🔍 {_esc(_label(trans, 'dx_primary'))}",
        unsafe_allow_html=True,
    )
    st.markdown(f"**{diagnosis.primary_diagnosis}**")
    st.markdown(_confidence_badge_html(trans, diagnosis.confidence_level), unsafe_allow_html=True)

    if diagnosis.icd10_primary:
        st.markdown(f"**{_label(trans, 'dx_icd10')}:** {diagnosis.icd10_primary}")
        for code in diagnosis.icd10_differentials:
            st.markdown(f"- {_esc(code)}")

    diff_label = f"🔬 {_label(trans, 'dx_differential')}"
    with st.expander(diff_label, expanded=True):
        for diff_dx in diagnosis.differential_diagnoses:
            st.markdown(f"- {diff_dx}")

    st.markdown(
        f"#### 📋 {_esc(_label(trans, 'dx_next_steps'))}",
        unsafe_allow_html=True,
    )
    for i, step in enumerate(diagnosis.recommended_next_steps, start=1):
        st.markdown(f"{i}. {step}")

    st.markdown(
        f'#### ⚠️ {_esc(_label(trans, "dx_considerations"))}',
        unsafe_allow_html=True,
    )
    for consideration in diagnosis.important_considerations:
        st.markdown(
            f'<p class="mdx-consideration-item">• {_esc(consideration)}</p>',
            unsafe_allow_html=True,
        )

    if diagnosis.imaging_findings:
        st.markdown(
            f"#### 🔬 {_esc(_label(trans, 'dx_imaging'))}",
            unsafe_allow_html=True,
        )
        st.markdown(diagnosis.imaging_findings)

    if diagnosis.drug_interactions:
        st.markdown(
            f"#### ⚠️ {_esc(_label(trans, 'dx_drug_alerts'))}",
            unsafe_allow_html=True,
        )
        for alert in diagnosis.drug_interactions:
            st.markdown(
                f'<p class="mdx-drug-alert">• {_esc(alert)}</p>',
                unsafe_allow_html=True,
            )
        if diagnosis.medication_notes:
            st.caption(diagnosis.medication_notes)

    if diagnosis.evidence_items:
        ref_label = f"📚 {_label(trans, 'dx_references')}"
        with st.expander(ref_label, expanded=False):
            st.caption(_label(trans, "dx_evidence_disclaimer"))
            for ev in diagnosis.evidence_items:
                if ev.pmid:
                    url = f"https://pubmed.ncbi.nlm.nih.gov/{ev.pmid}/"
                    st.markdown(f"- [{ev.title}]({url}) — {ev.source}")
                elif ev.url:
                    st.markdown(f"- [{ev.title}]({ev.url}) — {ev.source}")
                else:
                    st.markdown(f"- {ev.title} ({ev.source})")

    reasoning_label = f"💡 {_label(trans, 'dx_reasoning')}"
    with st.expander(reasoning_label, expanded=False):
        st.markdown(
            f'<p class="mdx-clinical-reasoning" style="background-color: #f0f0f0; color: #262730; '
            f'padding: 15px; border-radius: 5px; border-left: 4px solid #9467bd;">'
            f"{_esc(diagnosis.reasoning)}</p>",
            unsafe_allow_html=True,
        )


def normalize_diagnosis_html(html_content: str) -> str:
    """Strip blank lines and patch legacy reasoning styles for readability."""
    lines = [line for line in html_content.splitlines() if line.strip()]
    html = "\n".join(lines)
    legacy = 'style="background-color: #f0f0f0; padding: 15px; border-radius: 5px;"'
    if legacy in html:
        html = html.replace(
            legacy,
            'class="mdx-clinical-reasoning" style="background-color: #f0f0f0; color: #262730; '
            'padding: 15px; border-radius: 5px; border-left: 4px solid #9467bd;"',
        )
    return html


def render_diagnosis_result(
    html_content: Optional[str] = None,
    structured: Optional[StructuredDiagnosisOutput] = None,
    translations: Optional[Dict[str, Any]] = None,
    used_plain_fallback: bool = False,
) -> None:
    """
    Render diagnosis: structured UI when data is available, else HTML/plain text.
    """
    trans = translations or {}

    if used_plain_fallback:
        st.info(_label(trans, "dx_fallback_notice"))

    if structured is not None:
        render_structured_diagnosis(structured, trans)
        return

    if html_content:
        st.markdown(normalize_diagnosis_html(html_content), unsafe_allow_html=True)


def render_pdf_download_button(
    patient: Any,
    translations: Dict[str, Any],
    structured: Optional[StructuredDiagnosisOutput] = None,
    plain_html: Optional[str] = None,
    logo_path: Optional[Any] = None,
    enabled: bool = True,
) -> None:
    """Render PDF download button when export is enabled and diagnosis exists."""
    if not enabled:
        return
    if structured is None and not plain_html:
        return

    from ..config.settings import get_settings
    from ..services.pdf_export_service import build_pdf_bytes, build_pdf_filename

    if not get_settings().enable_pdf_export:
        return

    try:
        pdf_bytes = build_pdf_bytes(
            patient=patient,
            translations=translations,
            structured=structured,
            plain_html=plain_html,
            logo_path=logo_path,
        )
        st.download_button(
            label=_label(translations, "dx_download_pdf"),
            data=pdf_bytes,
            file_name=build_pdf_filename(),
            mime="application/pdf",
            key="mdx_pdf_download",
        )
    except Exception as exc:
        st.warning(f"PDF export failed: {exc}")


def structured_from_session(data: Optional[Dict[str, Any]]) -> Optional[StructuredDiagnosisOutput]:
    """Rebuild StructuredDiagnosisOutput from session_state dict."""
    if not data:
        return None
    try:
        return StructuredDiagnosisOutput.model_validate(data)
    except Exception:
        return None
