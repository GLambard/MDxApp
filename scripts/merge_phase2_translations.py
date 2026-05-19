#!/usr/bin/env python3
"""Merge Phase 2 translation keys and add new languages. Run from repo root."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANS_PATH = ROOT / "Assets" / "translations.json"

# New keys to merge into every existing language (English defaults)
PHASE2_KEYS = {
    "dx_download_pdf": "Download PDF report",
    "pdf_title": "MDxApp Medical Diagnosis Report",
    "pdf_patient_summary": "Patient Summary",
    "pdf_generated": "Generated",
    "dx_icd10": "ICD-10",
    "dx_references": "References",
    "dx_evidence_disclaimer": "References are for education only; verify with a clinician.",
    "dx_imaging": "Imaging findings",
    "dx_drug_alerts": "Medication alerts",
    "medications": "Medications",
    "meds_example": "(Example: metformin, lisinopril)",
    "meds_ph": "none",
    "meds_help": "List current medications, one per line or comma-separated",
    "imaging_header": "Medical image (optional)",
    "imaging_consent": "Images are not stored. For educational use only — not a radiologist report.",
    "imaging_type_label": "Image type",
    "imaging_type_skin": "Skin / rash",
    "imaging_type_xray": "X-ray",
    "imaging_type_ecg": "ECG trace",
    "imaging_type_lab": "Lab report photo",
    "imaging_type_other": "Other",
    "imaging_upload_label": "Upload image (JPG/PNG, max 5 MB)",
    "imaging_too_large": "Image exceeds 5 MB limit.",
    "imaging_type_warning": "Use JPG or PNG format.",
}

# Full new language blocks (abbreviated keys use English structure from file)
NEW_LANGS = {
    "中文": {},  # filled from English + overrides below
    "Português": {},
    "हिन्दी": {},
    "العربية": {},
    "Русский": {},
}

LANG_OVERRIDES = {
    "Français": {
        "dx_download_pdf": "Télécharger le rapport PDF",
        "pdf_title": "Rapport de diagnostic MDxApp",
        "medications": "Médicaments",
        "dx_icd10": "CIM-10",
        "dx_references": "Références",
    },
    "日本語": {
        "dx_download_pdf": "PDFレポートをダウンロード",
        "medications": "薬剤",
        "dx_icd10": "ICD-10",
    },
    "Español": {
        "dx_download_pdf": "Descargar informe PDF",
        "medications": "Medicamentos",
        "dx_icd10": "CIE-10",
    },
    "Deutsch": {
        "dx_download_pdf": "PDF-Bericht herunterladen",
        "medications": "Medikamente",
        "dx_icd10": "ICD-10",
    },
    "中文": {
        "page1_header": "医疗诊断助手",
        "language_selection": "选择语言：",
        "dx_download_pdf": "下载 PDF 报告",
        "medications": "药物",
        "dx_primary": "主要诊断",
        "submit": "提交",
    },
    "Português": {
        "page1_header": "Assistente de Diagnóstico Médico",
        "language_selection": "Selecione um idioma:",
        "dx_download_pdf": "Baixar relatório PDF",
        "medications": "Medicamentos",
        "submit": "ENVIAR",
    },
    "हिन्दी": {
        "page1_header": "चिकित्सा निदान सहायक",
        "language_selection": "भाषा चुनें:",
        "dx_download_pdf": "PDF रिपोर्ट डाउनलोड करें",
        "medications": "दवाइयाँ",
        "submit": "जमा करें",
    },
    "العربية": {
        "page1_header": "مساعد التشخيص الطبي",
        "language_selection": "اختر اللغة:",
        "dx_download_pdf": "تنزيل تقرير PDF",
        "medications": "الأدوية",
        "submit": "إرسال",
    },
    "Русский": {
        "page1_header": "Медицинский диагностический помощник",
        "language_selection": "Выберите язык:",
        "dx_download_pdf": "Скачать PDF-отчёт",
        "medications": "Лекарства",
        "submit": "ОТПРАВИТЬ",
    },
}


def main() -> None:
    data = json.loads(TRANS_PATH.read_text(encoding="utf-8"))
    english = data["English"]

    for lang, block in data.items():
        for key, val in PHASE2_KEYS.items():
            block.setdefault(key, val)
        if lang in LANG_OVERRIDES:
            block.update(LANG_OVERRIDES[lang])

    for lang in NEW_LANGS:
        if lang not in data:
            block = dict(english)
            block.update(PHASE2_KEYS)
            if lang in LANG_OVERRIDES:
                block.update(LANG_OVERRIDES[lang])
            data[lang] = block

    TRANS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
    print(f"Updated {TRANS_PATH} — {len(data)} languages")


if __name__ == "__main__":
    main()
