#!/usr/bin/env python3
"""One-off builder for scripts/i18n_locale_packs.py — run from repo root."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANS_PATH = ROOT / "Assets" / "translations.json"
OUT_PATH = ROOT / "scripts" / "i18n_locale_packs.py"

# ---------------------------------------------------------------------------
# Shared About-page fragments (placeholders {model}, {version} preserved)
# ---------------------------------------------------------------------------

def _versions_table(
    ver_hdr: str,
    date_hdr: str,
    hi_hdr: str,
    r251: str,
    r250: str,
    r200: str,
    r112: str,
    r100: str,
) -> str:
    return (
        f"| {ver_hdr} | {date_hdr} | {hi_hdr} |\n"
        f"|---------|------|------------|\n"
        f"| **2.5.1** | 2026 | {r251} |\n"
        f"| **2.5.0** | 2026 | {r250} |\n"
        f"| **2.0.0** | 2025 | {r200} |\n"
        f"| **1.12x** | 2023 | {r112} |\n"
        f"| **1.0** | 2023 | {r100} |"
    )


# Phase-2 / dx / imaging / meds keys shared across gap-fills
def _phase2_block(
    pdf_title: str,
    pdf_patient: str,
    pdf_gen: str,
    dx_icd10: str,
    dx_refs: str,
    dx_evidence_disc: str,
    dx_imaging: str,
    dx_drug: str,
    meds_ex: str,
    meds_ph: str,
    meds_help: str,
    img_hdr: str,
    img_consent: str,
    img_lbl: str,
    img_skin: str,
    img_xray: str,
    img_ecg: str,
    img_lab: str,
    img_other: str,
    img_upload: str,
    img_large: str,
    img_warn: str,
    dx_ev_none: str,
) -> dict[str, str]:
    return {
        "pdf_title": pdf_title,
        "pdf_patient_summary": pdf_patient,
        "pdf_generated": pdf_gen,
        "dx_icd10": dx_icd10,
        "dx_references": dx_refs,
        "dx_evidence_disclaimer": dx_evidence_disc,
        "dx_imaging": dx_imaging,
        "dx_drug_alerts": dx_drug,
        "meds_example": meds_ex,
        "meds_ph": meds_ph,
        "meds_help": meds_help,
        "imaging_header": img_hdr,
        "imaging_consent": img_consent,
        "imaging_type_label": img_lbl,
        "imaging_type_skin": img_skin,
        "imaging_type_xray": img_xray,
        "imaging_type_ecg": img_ecg,
        "imaging_type_lab": img_lab,
        "imaging_type_other": img_other,
        "imaging_upload_label": img_upload,
        "imaging_too_large": img_large,
        "imaging_type_warning": img_warn,
        "dx_evidence_none": dx_ev_none,
    }


def _about_block(
    what_text: str,
    feat_hdr: str,
    f1: str,
    f2: str,
    f3: str,
    f4: str,
    f6: str,
    excl_hdr: str,
    excl1: str,
    excl2: str,
    excl3: str,
    sup_hdr: str,
    sup_txt: str,
    ver_hdr: str,
    ver_tbl: str,
    src_hdr: str,
    src_txt: str,
    caut_hdr: str,
    dev_hdr: str,
    dev_msg: str,
    contact_title: str | None = None,
) -> dict[str, str]:
    out = {
        "page_about_what_text": what_text,
        "page_about_features_heading": feat_hdr,
        "page_about_feature_1": f1,
        "page_about_feature_2": f2,
        "page_about_feature_3": f3,
        "page_about_feature_4": f4,
        "page_about_feature_6": f6,
        "page_about_excluded_heading": excl_hdr,
        "page_about_excluded_1": excl1,
        "page_about_excluded_2": excl2,
        "page_about_excluded_3": excl3,
        "page_about_support_heading": sup_hdr,
        "page_about_support_text": sup_txt,
        "page_about_versions_heading": ver_hdr,
        "page_about_versions_table": ver_tbl,
        "page_about_sources_heading": src_hdr,
        "page_about_sources_text": src_txt,
        "page_about_caution_heading": caut_hdr,
        "page_about_dev_heading": dev_hdr,
        "page_about_dev_message": dev_msg,
    }
    if contact_title:
        out["page_contact_title"] = contact_title
    out["page_about_sources_heading"] = src_hdr  # ensure localized (may match EN cognate)
    return out


# Gap overrides for languages with strong existing UI in translations.json
GAPS: dict[str, dict[str, str]] = {}

# --- Français gaps ---
GAPS["Français"] = {
    "diagnostic": "Résultat diagnostique",
    "vissum_patient": "Patient : ",
    **_phase2_block(
        pdf_title="Rapport de diagnostic médical MDxApp",
        pdf_patient="Résumé du patient",
        pdf_gen="Généré le",
        dx_icd10="CIM-10",
        dx_refs="Références",
        dx_evidence_disc="Les références sont fournies à titre éducatif uniquement ; vérifiez-les avec un clinicien.",
        dx_imaging="Résultats d'imagerie",
        dx_drug="Alertes médicamenteuses",
        meds_ex="(Exemple : metformine, lisinopril)",
        meds_ph="aucun",
        meds_help="Liste des médicaments actuels, un par ligne ou séparés par des virgules",
        img_hdr="Image médicale (facultatif)",
        img_consent="Les images ne sont pas stockées. Usage éducatif uniquement — ce n'est pas un compte rendu de radiologie.",
        img_lbl="Type d'image",
        img_skin="Peau / éruption",
        img_xray="Radiographie",
        img_ecg="Tracé ECG",
        img_lab="Photo de compte rendu de laboratoire",
        img_other="Autre",
        img_upload="Téléverser une image (JPG/PNG, max. 5 Mo)",
        img_large="L'image dépasse la limite de 5 Mo.",
        img_warn="Utilisez le format JPG ou PNG.",
        dx_ev_none="Aucune référence vérifiable n'a été fournie pour ce cas.",
    ),
    **_about_block(
        what_text=(
            "MDxApp est un **assistant de diagnostic médical gratuit** pour les cliniciens, les étudiants et les patients. "
            "Il organise les symptômes et fournit une **évaluation préliminaire assistée par l'IA** via "
            "[OpenAI](https://openai.com/) **{model}**, avec des résultats structurés et exploitables."
        ),
        feat_hdr="Fonctionnalités actuelles (v{version})",
        f1="**Diagnostic structuré** — diagnostic principal, diagnostics différentiels, prochaines étapes, considérations, confiance, raisonnement clinique",
        f2="**Téléchargement du rapport PDF** — résumé partageable après chaque évaluation",
        f3="**Références éducatives** — liens vers la littérature lorsque des PMIDs ou URL vérifiables sont fournis (PubMed)",
        f4="**Notes de sécurité médicamenteuse** — alertes d'interaction lorsque des médicaments sont listés (OpenFDA + IA)",
        f6="**Confidentialité d'abord** — aucune donnée patient stockée sur nos serveurs ; chaque session est éphémère",
        excl_hdr="Non inclus (volontairement)",
        excl1="**Téléversement d'imagerie médicale** — désactivé pendant la validation de la sécurité et de la précision",
        excl2="**Codes de facturation régionaux (ICD-10, etc.)** — masqués car les systèmes de codage varient selon les pays",
        excl3="**Diagnostic final** — nécessite toujours un clinicien agréé",
        sup_hdr="Soutenir le projet",
        sup_txt=(
            "L'application utilise l'API OpenAI, qui a un coût réel par requête. Les dons via **Buy Me a Coffee** "
            "(barre latérale) aident à garder MDxApp gratuit. Merci pour votre soutien."
        ),
        ver_hdr="Historique des versions",
        ver_tbl=_versions_table(
            "Version", "Date", "Points clés",
            "Modèle par défaut **gpt-5.4-nano**, pages À propos/Contact localisées, 15 langues, RTL arabe",
            "Phase 2 : export PDF, références, contrôles médicamenteux, interface de diagnostic structuré",
            "Architecture modulaire, sorties structurées, tests automatisés",
            "Interface multilingue, intégration ChatGPT",
            "Première version publique",
        ),
        src_hdr="Sources et références",
        src_txt=(
            "- Code source : [github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)\n"
            "- Cas d'exemple adaptés de matériel pédagogique public (p. ex. [@BrownJHM](https://twitter.com/BrownJHM))."
        ),
        caut_hdr="Mise en garde",
        dev_hdr="Message du développeur",
        contact_title="Nous contacter",
        dev_msg=(
            "> Merci d'utiliser MDxApp. Ce projet est développé sur mon temps libre pour rendre la réflexion diagnostique "
            "plus accessible dans le monde entier. Vos retours et votre soutien via Buy Me a Coffee le font vivre.\n>\n"
            "> — **Guillaume Lambard**, concepteur et développeur de solutions IA"
        ),
    ),
}

# --- Español gaps ---
GAPS["Español"] = {
    **_phase2_block(
        pdf_title="Informe de diagnóstico médico MDxApp",
        pdf_patient="Resumen del paciente",
        pdf_gen="Generado",
        dx_icd10="CIE-10",
        dx_refs="Referencias",
        dx_evidence_disc="Las referencias son solo educativas; verifíquelas con un clínico.",
        dx_imaging="Hallazgos de imagen",
        dx_drug="Alertas de medicación",
        meds_ex="(Ejemplo: metformina, lisinopril)",
        meds_ph="ninguno",
        meds_help="Liste los medicamentos actuales, uno por línea o separados por comas",
        img_hdr="Imagen médica (opcional)",
        img_consent="Las imágenes no se almacenan. Solo uso educativo — no es un informe radiológico.",
        img_lbl="Tipo de imagen",
        img_skin="Piel / erupción",
        img_xray="Radiografía",
        img_ecg="Trazado de ECG",
        img_lab="Foto de informe de laboratorio",
        img_other="Otro",
        img_upload="Subir imagen (JPG/PNG, máx. 5 MB)",
        img_large="La imagen supera el límite de 5 MB.",
        img_warn="Use formato JPG o PNG.",
        dx_ev_none="No se proporcionaron referencias verificables para este caso.",
    ),
    **_about_block(
        what_text=(
            "MDxApp es un **asistente de diagnóstico médico gratuito** para clínicos, estudiantes y pacientes. "
            "Organiza los síntomas y devuelve una **evaluación preliminar asistida por IA** mediante "
            "[OpenAI](https://openai.com/) **{model}**, con resultados estructurados y accionables."
        ),
        feat_hdr="Funciones actuales (v{version})",
        f1="**Diagnóstico estructurado** — diagnóstico principal, diferenciales, próximos pasos, consideraciones, confianza, razonamiento clínico",
        f2="**Descarga de informe PDF** — resumen compartible tras cada evaluación",
        f3="**Referencias educativas** — enlaces bibliográficos cuando se proporcionan PMIDs o URL verificables (PubMed)",
        f4="**Notas de seguridad de medicamentos** — alertas de interacción cuando se listan medicamentos (OpenFDA + IA)",
        f6="**Privacidad primero** — no se almacenan datos de pacientes en nuestros servidores; cada sesión es efímera",
        excl_hdr="No incluido (por diseño)",
        excl1="**Carga de imágenes médicas** — desactivada mientras validamos seguridad y precisión",
        excl2="**Códigos de facturación regionales (ICD-10, etc.)** — ocultos porque los sistemas de codificación varían por país",
        excl3="**Diagnóstico final** — siempre requiere un clínico autorizado",
        sup_hdr="Apoyar el proyecto",
        sup_txt=(
            "La aplicación usa la API de OpenAI, que tiene un coste real por solicitud. Las donaciones mediante "
            "**Buy Me a Coffee** (barra lateral) ayudan a mantener MDxApp gratuito. Gracias por su apoyo."
        ),
        ver_hdr="Historial de versiones",
        ver_tbl=_versions_table(
            "Versión", "Fecha", "Aspectos destacados",
            "Modelo predeterminado **gpt-5.4-nano**, Acerca de/Contacto localizados, 15 idiomas, RTL árabe",
            "Fase 2: exportación PDF, referencias, comprobaciones de fármacos, UI de diagnóstico estructurado",
            "Arquitectura modular, salidas estructuradas, pruebas automatizadas",
            "Interfaz multilingüe, integración ChatGPT",
            "Lanzamiento público inicial",
        ),
        src_hdr="Fuentes",
        src_txt=(
            "- Código fuente: [github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)\n"
            "- Casos de ejemplo adaptados de material docente público (p. ej. [@BrownJHM](https://twitter.com/BrownJHM))."
        ),
        caut_hdr="Precaución",
        dev_hdr="Mensaje del desarrollador",
        dev_msg=(
            "> Gracias por usar MDxApp. Este proyecto se construye en tiempo libre para hacer el pensamiento "
            "diagnóstico más accesible en todo el mundo. Sus comentarios y el apoyo con café lo mantienen en marcha.\n>\n"
            "> — **Guillaume Lambard**, diseñador y desarrollador de soluciones de IA"
        ),
    ),
}

# --- Deutsch gaps ---
GAPS["Deutsch"] = {
    "vissum_patient": "Patient/in: ",
    **_phase2_block(
        pdf_title="MDxApp Medizinischer Diagnosebericht",
        pdf_patient="Patientenzusammenfassung",
        pdf_gen="Erstellt",
        dx_icd10="ICD-10",
        dx_refs="Referenzen",
        dx_evidence_disc="Referenzen dienen nur der Ausbildung; bitte mit einem Kliniker abgleichen.",
        dx_imaging="Bildgebungsbefunde",
        dx_drug="Medikamentenwarnungen",
        meds_ex="(Beispiel: Metformin, Lisinopril)",
        meds_ph="keine",
        meds_help="Aktuelle Medikamente auflisten, je Zeile oder durch Kommas getrennt",
        img_hdr="Medizinisches Bild (optional)",
        img_consent="Bilder werden nicht gespeichert. Nur zu Bildungszwecken — kein radiologischer Befund.",
        img_lbl="Bildtyp",
        img_skin="Haut / Ausschlag",
        img_xray="Röntgen",
        img_ecg="EKG-Kurve",
        img_lab="Foto eines Laborberichts",
        img_other="Sonstiges",
        img_upload="Bild hochladen (JPG/PNG, max. 5 MB)",
        img_large="Das Bild überschreitet das Limit von 5 MB.",
        img_warn="Verwenden Sie das Format JPG oder PNG.",
        dx_ev_none="Für diesen Fall wurden keine überprüfbaren Referenzen angegeben.",
    ),
    **_about_block(
        what_text=(
            "MDxApp ist ein **kostenloser medizinischer Diagnoseassistent** für Kliniker, Studierende und Patienten. "
            "Er ordnet Symptome und liefert eine **KI-gestützte Vorabbeurteilung** mit "
            "[OpenAI](https://openai.com/) **{model}** in strukturierter, umsetzbarer Form."
        ),
        feat_hdr="Aktuelle Funktionen (v{version})",
        f1="**Strukturierte Diagnose** — Hauptdiagnose, Differentialdiagnosen, nächste Schritte, Überlegungen, Konfidenz, klinische Begründung",
        f2="**PDF-Bericht herunterladen** — teilbare Zusammenfassung nach jeder Beurteilung",
        f3="**Bildungsreferenzen** — Literaturlinks bei verifizierbaren PMIDs oder URLs (PubMed)",
        f4="**Medikamentensicherheitshinweise** — Interaktionswarnungen bei gelisteten Medikamenten (OpenFDA + KI)",
        f6="**Datenschutz zuerst** — keine Patientendaten auf unseren Servern; jede Sitzung ist flüchtig",
        excl_hdr="Nicht enthalten (absichtlich)",
        excl1="**Upload medizinischer Bilder** — deaktiviert während wir Sicherheit und Genauigkeit prüfen",
        excl2="**Regionale Abrechnungscodes (ICD-10 usw.)** — ausgeblendet, da Kodierungssysteme je Land variieren",
        excl3="**Endgültige Diagnose** — erfordert stets einen zugelassenen Kliniker",
        sup_hdr="Projekt unterstützen",
        sup_txt=(
            "Die App nutzt die OpenAI-API mit echten Kosten pro Anfrage. Spenden über **Buy Me a Coffee** "
            "(Seitenleiste) helfen, MDxApp kostenlos zu halten. Vielen Dank für Ihre Unterstützung."
        ),
        ver_hdr="Versionsverlauf",
        ver_tbl=_versions_table(
            "Version", "Datum", "Highlights",
            "Standardmodell **gpt-5.4-nano**, lokalisierte Über/Uns/Kontakt-Seiten, 15 Sprachen, Arabisch RTL",
            "Phase 2: PDF-Export, Referenzen, Arzneimittelprüfungen, strukturierte Diagnose-UI",
            "Modulare Architektur, strukturierte Ausgaben, automatisierte Tests",
            "Mehrsprachige Oberfläche, ChatGPT-Integration",
            "Erste öffentliche Version",
        ),
        src_hdr="Quellen",
        src_txt=(
            "- Quellcode: [github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)\n"
            "- Beispielfälle aus öffentlichem Lehrmaterial (z. B. [@BrownJHM](https://twitter.com/BrownJHM))."
        ),
        caut_hdr="Vorsicht",
        dev_hdr="Nachricht des Entwicklers",
        dev_msg=(
            "> Danke, dass Sie MDxApp nutzen. Dieses Projekt entsteht in der Freizeit, um diagnostisches Denken "
            "weltweit zugänglicher zu machen. Ihr Feedback und Kaffee-Support halten es am Laufen.\n>\n"
            "> — **Guillaume Lambard**, KI-Lösungsdesigner und Entwickler"
        ),
    ),
}

# --- 日本語 gaps ---
GAPS["日本語"] = {
    "page_about_what_heading": "MDxAppとは？",
    **_phase2_block(
        pdf_title="MDxApp 医療診断レポート",
        pdf_patient="患者サマリー",
        pdf_gen="作成日時",
        dx_icd10="ICD-10",
        dx_refs="参考文献",
        dx_evidence_disc="参考文献は教育目的のみです。臨床医と確認してください。",
        dx_imaging="画像所見",
        dx_drug="薬剤アラート",
        meds_ex="（例：メトホルミン、リシノプリル）",
        meds_ph="なし",
        meds_help="現在の薬剤を1行ずつ、またはカンマ区切りで入力",
        img_hdr="医療画像（任意）",
        img_consent="画像は保存されません。教育目的のみ — 放射線科医の報告書ではありません。",
        img_lbl="画像の種類",
        img_skin="皮膚 / 発疹",
        img_xray="X線",
        img_ecg="心電図",
        img_lab="検査報告書の写真",
        img_other="その他",
        img_upload="画像をアップロード（JPG/PNG、最大5MB）",
        img_large="画像が5MBの上限を超えています。",
        img_warn="JPGまたはPNG形式を使用してください。",
        dx_ev_none="この症例では検証可能な参考文献は提供されませんでした。",
    ),
    **_about_block(
        what_text=(
            "MDxAppは、臨床医・学生・患者向けの**無料の医療診断アシスタント**です。"
            "症状を整理し、[OpenAI](https://openai.com/) **{model}** による**AI支援の予備評価**を"
            "構造化された実用的な形式で返します。"
        ),
        feat_hdr="現在の機能（v{version}）",
        f1="**構造化診断** — 主診断、鑑別診断、次のステップ、考慮事項、信頼度、臨床的理由",
        f2="**PDFレポートのダウンロード** — 各評価後に共有可能なサマリー",
        f3="**教育用参考文献** — 検証可能なPMIDまたはURLがある場合の文献リンク（PubMed）",
        f4="**薬剤安全メモ** — 薬剤が記載されている場合の相互作用警告（OpenFDA + AI）",
        f6="**プライバシー優先** — 患者データはサーバーに保存されません。各セッションは一時的です",
        excl_hdr="含まれないもの（意図的）",
        excl1="**医療画像のアップロード** — 安全性と精度の検証中は無効",
        excl2="**地域の請求コード（ICD-10など）** — 国ごとにコード体系が異なるため非表示",
        excl3="**最終診断** — 常に資格を持つ臨床医が必要",
        sup_hdr="プロジェクトを支援",
        sup_txt=(
            "本アプリはOpenAI APIを使用しており、リクエストごとに実コストがかかります。"
            "**Buy Me a Coffee**（サイドバー）への寄付がMDxAppを無料で維持する助けになります。ご支援ありがとうございます。"
        ),
        ver_hdr="バージョン履歴",
        ver_tbl=_versions_table(
            "バージョン", "日付", "ハイライト",
            "デフォルトモデル **gpt-5.4-nano**、About/Contactのローカライズ、15言語、アラビア語RTL",
            "フェーズ2：PDFエクスポート、参考文献、薬剤チェック、構造化診断UI",
            "モジュール構成、構造化出力、自動テスト",
            "多言語UI、ChatGPT統合",
            "初回公開リリース",
        ),
        src_hdr="ソース",
        src_txt=(
            "- ソースコード：[github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)\n"
            "- 公開教材からの例症例（例：[@BrownJHM](https://twitter.com/BrownJHM)）。"
        ),
        caut_hdr="注意",
        dev_hdr="開発者からのメッセージ",
        dev_msg=(
            "> MDxAppをご利用いただきありがとうございます。このプロジェクトは診断的思考を世界中にもっと"
            "身近にするために趣味で作られています。フィードバックとコーヒー支援が運営を支えています。\n>\n"
            "> — **Guillaume Lambard**、AIソリューション設計者・開発者"
        ),
    ),
}

