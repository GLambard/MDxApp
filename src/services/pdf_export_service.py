"""
Generate PDF diagnosis reports in memory (ReportLab).
"""

import re
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer

from ..core.ai_client import StructuredDiagnosisOutput
from ..models.patient import PatientData

_DEFAULT_LABELS = {
    "dx_primary": "Primary Diagnosis",
    "dx_confidence": "Confidence",
    "dx_differential": "Differential Diagnoses",
    "dx_next_steps": "Recommended Next Steps",
    "dx_considerations": "Important Considerations",
    "dx_reasoning": "Clinical Reasoning",
    "pdf_title": "MDxApp Medical Diagnosis Report",
    "pdf_patient_summary": "Patient Summary",
    "pdf_generated": "Generated",
    "caution": "Caution",
    "caution_message": "This is a preliminary AI-assisted assessment, not a final medical diagnosis.",
}


def _label(translations: Dict[str, Any], key: str) -> str:
    return str(translations.get(key, _DEFAULT_LABELS.get(key, key)))


def _safe_text(text: str) -> str:
    """Escape text for ReportLab Paragraph XML."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def _strip_html(html: str) -> str:
    """Plain text from HTML for fallback PDF."""
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


def build_pdf_filename() -> str:
    return f"MDxApp_diagnosis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"


def build_pdf_bytes(
    patient: PatientData,
    translations: Dict[str, Any],
    structured: Optional[StructuredDiagnosisOutput] = None,
    plain_html: Optional[str] = None,
    logo_path: Optional[Path] = None,
) -> bytes:
    """
    Build PDF report bytes from structured diagnosis or plain HTML fallback.

    Args:
        patient: Patient data for summary section
        translations: Language-specific labels
        structured: Structured diagnosis (preferred)
        plain_html: Fallback HTML/text diagnosis
        logo_path: Optional path to logo PNG

    Returns:
        PDF file content as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "MDxTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "MDxHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1f77b4"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "MDxBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
    )
    caution_style = ParagraphStyle(
        "MDxCaution",
        parent=body_style,
        fontSize=9,
        textColor=colors.HexColor("#721c24"),
        backColor=colors.HexColor("#f8d7da"),
        borderPadding=6,
    )

    story: list = []

    if logo_path and logo_path.is_file():
        img = Image(str(logo_path), width=1.2 * inch, height=1.2 * inch)
        story.append(img)
        story.append(Spacer(1, 8))

    story.append(Paragraph(_safe_text(_label(translations, "pdf_title")), title_style))
    story.append(
        Paragraph(
            f"{_label(translations, 'pdf_generated')}: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            body_style,
        )
    )
    story.append(Spacer(1, 12))

    # Patient summary
    story.append(Paragraph(_safe_text(_label(translations, "pdf_patient_summary")), heading_style))
    none_t = translations.get("none", "none")
    story.append(
        Paragraph(
            _safe_text(
                f"{patient.gender}, {patient.age} | "
                f"{translations.get('vissum_pregnancy', 'Pregnancy')}: {patient.is_pregnant}<br/>"
                f"{translations.get('vissum_history', 'History')}: {patient.history or none_t}<br/>"
                f"{translations.get('vissum_symp', 'Symptoms')}: {patient.symptoms}<br/>"
                f"{translations.get('vissum_exam', 'Exam')}: {patient.exam_findings or none_t}<br/>"
                f"{translations.get('vissum_lab', 'Lab')}: {patient.lab_results or none_t}"
            ),
            body_style,
        )
    )
    story.append(Spacer(1, 12))

    if structured:
        _append_structured_sections(story, structured, translations, heading_style, body_style)
    elif plain_html:
        story.append(Paragraph(_safe_text(_label(translations, "diagnostic")), heading_style))
        story.append(Paragraph(_safe_text(_strip_html(plain_html)), body_style))
    else:
        story.append(Paragraph(_safe_text("No diagnosis content available."), body_style))

    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            f"<b>{_safe_text(_label(translations, 'caution'))}</b>: "
            f"{_safe_text(_label(translations, 'caution_message'))}",
            caution_style,
        )
    )

    doc.build(story)
    return buffer.getvalue()


def _append_structured_sections(
    story: list,
    diagnosis: StructuredDiagnosisOutput,
    translations: Dict[str, Any],
    heading_style: ParagraphStyle,
    body_style: ParagraphStyle,
) -> None:
    """Add structured diagnosis sections to PDF story."""
    conf_key = f"dx_confidence_{diagnosis.confidence_level.lower()}"
    conf_label = translations.get(conf_key, diagnosis.confidence_level.upper())

    story.append(Paragraph(_safe_text(_label(translations, "dx_primary")), heading_style))
    story.append(Paragraph(_safe_text(diagnosis.primary_diagnosis), body_style))
    story.append(
        Paragraph(
            _safe_text(f"{_label(translations, 'dx_confidence')}: {conf_label}"),
            body_style,
        )
    )

    if diagnosis.icd10_primary:
        story.append(
            Paragraph(
                _safe_text(f"{_label(translations, 'dx_icd10')}: {diagnosis.icd10_primary}"),
                body_style,
            )
        )

    story.append(Paragraph(_safe_text(_label(translations, "dx_differential")), heading_style))
    for item in diagnosis.differential_diagnoses:
        story.append(Paragraph(_safe_text(f"• {item}"), body_style))

    story.append(Paragraph(_safe_text(_label(translations, "dx_next_steps")), heading_style))
    for i, step in enumerate(diagnosis.recommended_next_steps, start=1):
        story.append(Paragraph(_safe_text(f"{i}. {step}"), body_style))

    story.append(Paragraph(_safe_text(_label(translations, "dx_considerations")), heading_style))
    for item in diagnosis.important_considerations:
        story.append(Paragraph(_safe_text(f"• {item}"), body_style))

    if diagnosis.imaging_findings:
        story.append(Paragraph(_safe_text(_label(translations, "dx_imaging")), heading_style))
        story.append(Paragraph(_safe_text(diagnosis.imaging_findings), body_style))

    if diagnosis.drug_interactions:
        story.append(Paragraph(_safe_text(_label(translations, "dx_drug_alerts")), heading_style))
        for alert in diagnosis.drug_interactions:
            story.append(Paragraph(_safe_text(f"• {alert}"), body_style))

    if diagnosis.evidence_items:
        story.append(Paragraph(_safe_text(_label(translations, "dx_references")), heading_style))
        for ev in diagnosis.evidence_items:
            line = f"{ev.title} ({ev.source})"
            if ev.pmid:
                line += f" — https://pubmed.ncbi.nlm.nih.gov/{ev.pmid}/"
            elif ev.url:
                line += f" — {ev.url}"
            story.append(Paragraph(_safe_text(line), body_style))
        story.append(
            Paragraph(_safe_text(_label(translations, "dx_evidence_disclaimer")), body_style)
        )

    story.append(Paragraph(_safe_text(_label(translations, "dx_reasoning")), heading_style))
    story.append(Paragraph(_safe_text(diagnosis.reasoning), body_style))
