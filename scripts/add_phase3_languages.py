#!/usr/bin/env python3
"""Add 5 languages (15+ total), About/Contact page keys. Run from repo root."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANS_PATH = ROOT / "Assets" / "translations.json"

PAGE_KEYS_EN = {
    "page_about_title": "About MDxApp",
    "page_about_what_heading": "What is MDxApp?",
    "page_about_what_text": (
        "MDxApp is a **free medical diagnosis assistant** for clinicians, students, and patients. "
        "It organizes symptoms and returns an **AI-assisted preliminary assessment** using "
        "[OpenAI](https://openai.com/) **{model}** with structured, actionable output."
    ),
    "page_about_features_heading": "Current features (v{version})",
    "page_about_feature_1": "**Structured diagnosis** — primary diagnosis, differentials, next steps, considerations, confidence, clinical reasoning",
    "page_about_feature_2": "**PDF report download** — shareable summary after each assessment",
    "page_about_feature_3": "**Educational references** — literature links when verifiable PMIDs or URLs are provided",
    "page_about_feature_4": "**Medication safety notes** — interaction warnings when medications are listed (OpenFDA + AI)",
    "page_about_feature_5": "**15+ languages** — global UI including RTL support for Arabic",
    "page_about_feature_6": "**Privacy-first** — no patient data stored on our servers; each session is ephemeral",
    "page_about_excluded_heading": "Not included (by design)",
    "page_about_excluded_1": "**Medical imaging upload** — disabled while we validate safety and accuracy",
    "page_about_excluded_2": "**Regional billing codes (ICD-10, etc.)** — hidden because coding systems differ by country",
    "page_about_excluded_3": "**Final diagnosis** — always requires a licensed clinician",
    "page_about_support_heading": "Support the project",
    "page_about_support_text": (
        "The app uses the OpenAI API, which has a real cost per request. Donations via **Buy Me a Coffee** "
        "(sidebar) help keep MDxApp free. Thank you for your support."
    ),
    "page_about_versions_heading": "Version history",
    "page_about_versions_table": (
        "| Version | Date | Highlights |\n"
        "|---------|------|------------|\n"
        "| **2.5.1** | 2026 | Default model **gpt-5.4-nano**, localized About/Contact, 15 languages, Arabic RTL |\n"
        "| **2.5.0** | 2026 | Phase 2: PDF export, references, drug checks, structured diagnosis UI |\n"
        "| **2.0.0** | 2025 | Modular architecture, structured outputs, automated tests |\n"
        "| **1.12x** | 2023 | Multilingual UI, ChatGPT integration |\n"
        "| **1.0** | 2023 | Initial public release |"
    ),
    "page_about_sources_heading": "Sources",
    "page_about_sources_text": (
        "- Source code: [github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)\n"
        "- Example cases adapted from public teaching material (e.g. [@BrownJHM](https://twitter.com/BrownJHM))."
    ),
    "page_about_caution_heading": "Caution",
    "page_about_dev_heading": "Message from the developer",
    "page_about_dev_message": (
        "> Thank you for using MDxApp. This project is built in spare time to make diagnostic thinking "
        "more accessible worldwide. Your feedback and coffee support keep it running.\n>\n"
        "> — **Guillaume Lambard**, AI solutions designer and developer"
    ),
    "page_contact_title": "Contact",
    "contact_form_name_ph": "Your name",
    "contact_form_email_ph": "Your email",
    "contact_form_message_ph": "Your message here",
    "contact_form_submit": "Send",
    "dx_evidence_none": "No verifiable references were provided for this case.",
}

NEW_LANGUAGES = ["Italiano", "한국어", "Türkçe", "Tiếng Việt", "Bahasa Indonesia"]

# Per-language overrides (UI + pages); missing keys fall back to English
LANG_OVERRIDES: dict[str, dict[str, str]] = {
    "Français": {
        "page_about_title": "À propos de MDxApp",
        "page_about_what_heading": "Qu'est-ce que MDxApp ?",
        "page_about_features_heading": "Fonctionnalités actuelles (v{version})",
        "page_about_feature_5": "**15+ langues** — interface mondiale avec prise en charge RTL pour l'arabe",
        "page_contact_title": "Contact",
        "contact_form_name_ph": "Votre nom",
        "contact_form_email_ph": "Votre e-mail",
        "contact_form_message_ph": "Votre message",
        "contact_form_submit": "Envoyer",
        "page1_header": "Assistant Diagnostic Médical",
        "language_selection": "Sélectionnez une langue :",
        "submit": "SOUMETTRE",
    },
    "Español": {
        "page_about_title": "Acerca de MDxApp",
        "page_about_what_heading": "¿Qué es MDxApp?",
        "page_about_feature_5": "**Más de 15 idiomas** — interfaz global con soporte RTL para árabe",
        "page_contact_title": "Contacto",
        "contact_form_name_ph": "Su nombre",
        "contact_form_email_ph": "Su correo electrónico",
        "contact_form_message_ph": "Su mensaje",
        "contact_form_submit": "Enviar",
        "language_selection": "Seleccione un idioma:",
        "submit": "ENVIAR",
    },
    "Deutsch": {
        "page_about_title": "Über MDxApp",
        "page_about_what_heading": "Was ist MDxApp?",
        "page_about_feature_5": "**15+ Sprachen** — globale Oberfläche mit RTL für Arabisch",
        "page_contact_title": "Kontakt",
        "contact_form_name_ph": "Ihr Name",
        "contact_form_email_ph": "Ihre E-Mail",
        "contact_form_message_ph": "Ihre Nachricht",
        "contact_form_submit": "Senden",
        "language_selection": "Sprache wählen:",
        "submit": "SENDEN",
    },
    "Italiano": {
        "page1_header": "Assistente Diagnostico Medico",
        "page1_subheader": "Il futuro della diagnostica con ChatGPT.",
        "language_selection": "Seleziona una lingua:",
        "submit": "INVIA",
        "page_about_title": "Informazioni su MDxApp",
        "page_about_what_heading": "Cos'è MDxApp?",
        "page_about_feature_5": "**Oltre 15 lingue** — interfaccia globale con RTL per l'arabo",
        "page_contact_title": "Contatto",
        "contact_form_name_ph": "Il tuo nome",
        "contact_form_email_ph": "La tua email",
        "contact_form_message_ph": "Il tuo messaggio",
        "contact_form_submit": "Invia",
        "dx_download_pdf": "Scarica report PDF",
        "medications": "Farmaci",
    },
    "한국어": {
        "page1_header": "의료 진단 도우미",
        "language_selection": "언어 선택:",
        "submit": "제출",
        "page_about_title": "MDxApp 소개",
        "page_about_what_heading": "MDxApp이란?",
        "page_about_feature_5": "**15개 이상의 언어** — 아랍어 RTL 지원",
        "page_contact_title": "문의",
        "contact_form_name_ph": "이름",
        "contact_form_email_ph": "이메일",
        "contact_form_message_ph": "메시지",
        "contact_form_submit": "보내기",
        "dx_download_pdf": "PDF 보고서 다운로드",
        "medications": "약물",
    },
    "Türkçe": {
        "page1_header": "Tıbbi Tanı Asistanı",
        "language_selection": "Dil seçin:",
        "submit": "GÖNDER",
        "page_about_title": "MDxApp Hakkında",
        "page_about_what_heading": "MDxApp nedir?",
        "page_about_feature_5": "**15+ dil** — Arapça için RTL desteği",
        "page_contact_title": "İletişim",
        "contact_form_name_ph": "Adınız",
        "contact_form_email_ph": "E-posta",
        "contact_form_message_ph": "Mesajınız",
        "contact_form_submit": "Gönder",
        "dx_download_pdf": "PDF raporu indir",
        "medications": "İlaçlar",
    },
    "Tiếng Việt": {
        "page1_header": "Trợ lý chẩn đoán y khoa",
        "language_selection": "Chọn ngôn ngữ:",
        "submit": "GỬI",
        "page_about_title": "Giới thiệu MDxApp",
        "page_about_what_heading": "MDxApp là gì?",
        "page_about_feature_5": "**Hơn 15 ngôn ngữ** — hỗ trợ RTL cho tiếng Ả Rập",
        "page_contact_title": "Liên hệ",
        "contact_form_name_ph": "Tên của bạn",
        "contact_form_email_ph": "Email",
        "contact_form_message_ph": "Tin nhắn",
        "contact_form_submit": "Gửi",
        "dx_download_pdf": "Tải báo cáo PDF",
        "medications": "Thuốc",
    },
    "Bahasa Indonesia": {
        "page1_header": "Asisten Diagnosis Medis",
        "language_selection": "Pilih bahasa:",
        "submit": "KIRIM",
        "page_about_title": "Tentang MDxApp",
        "page_about_what_heading": "Apa itu MDxApp?",
        "page_about_feature_5": "**15+ bahasa** — dukungan RTL untuk Arab",
        "page_contact_title": "Kontak",
        "contact_form_name_ph": "Nama Anda",
        "contact_form_email_ph": "Email",
        "contact_form_message_ph": "Pesan Anda",
        "contact_form_submit": "Kirim",
        "dx_download_pdf": "Unduh laporan PDF",
        "medications": "Obat",
    },
    "中文": {
        "page_about_title": "关于 MDxApp",
        "page_about_what_heading": "什么是 MDxApp？",
        "page_about_feature_5": "**15+ 种语言** — 支持阿拉伯语 RTL",
        "page_contact_title": "联系",
        "contact_form_name_ph": "您的姓名",
        "contact_form_email_ph": "您的邮箱",
        "contact_form_message_ph": "您的留言",
        "contact_form_submit": "发送",
    },
    "Português": {
        "page_about_title": "Sobre o MDxApp",
        "page_about_feature_5": "**Mais de 15 idiomas** — suporte RTL para árabe",
        "page_contact_title": "Contato",
        "contact_form_name_ph": "Seu nome",
        "contact_form_email_ph": "Seu e-mail",
        "contact_form_message_ph": "Sua mensagem",
        "contact_form_submit": "Enviar",
    },
    "日本語": {
        "page_about_title": "MDxAppについて",
        "page_about_feature_5": "**15以上の言語** — アラビア語RTL対応",
        "page_contact_title": "お問い合わせ",
        "contact_form_name_ph": "お名前",
        "contact_form_email_ph": "メールアドレス",
        "contact_form_message_ph": "メッセージ",
        "contact_form_submit": "送信",
    },
    "Русский": {
        "page_about_title": "О MDxApp",
        "page_about_feature_5": "**Более 15 языков** — поддержка RTL для арабского",
        "page_contact_title": "Контакты",
        "contact_form_name_ph": "Ваше имя",
        "contact_form_email_ph": "Электронная почта",
        "contact_form_message_ph": "Сообщение",
        "contact_form_submit": "Отправить",
    },
    "हिन्दी": {
        "page_about_title": "MDxApp के बारे में",
        "page_about_feature_5": "**15+ भाषाएँ** — अरबी के लिए RTL समर्थन",
        "page_contact_title": "संपर्क",
        "contact_form_name_ph": "आपका नाम",
        "contact_form_email_ph": "ईमेल",
        "contact_form_message_ph": "संदेश",
        "contact_form_submit": "भेजें",
    },
    "العربية": {
        "page_about_title": "حول MDxApp",
        "page_about_what_heading": "ما هو MDxApp؟",
        "page_about_what_text": (
            "MDxApp هو **مساعد تشخيص طبي مجاني** للأطباء والطلاب والمرضى. "
            "يجمع الأعراض ويقدم **تقييماً أولياً بمساعدة الذكاء الاصطناعي** عبر "
            "[OpenAI](https://openai.com/) **{model}** بنتائج منظمة وواضحة."
        ),
        "page_about_features_heading": "الميزات الحالية (الإصدار {version})",
        "page_about_feature_1": "**تشخيص منظم** — تشخيص أولي، تشخيصات تفريقية، خطوات تالية، اعتبارات، ثقة، تعليل سريري",
        "page_about_feature_2": "**تنزيل تقرير PDF** — ملخص قابل للمشاركة بعد كل تقييم",
        "page_about_feature_3": "**مراجع تعليمية** — روابط literature عند توفر معرف PubMed أو URL",
        "page_about_feature_4": "**تنبيهات الأدوية** — تفاعلات دوائية عند إدراج الأدوية",
        "page_about_feature_5": "**أكثر من 15 لغة** — واجهة عالمية مع دعم RTL للعربية",
        "page_about_feature_6": "**الخصوصية أولاً** — لا نخزن بيانات المرضى على الخوادم",
        "page_about_excluded_heading": "غير متضمن (بقصد)",
        "page_about_excluded_1": "**رفع الصور الطبية** — معطل أثناء التحقق من السلامة",
        "page_about_excluded_2": "**رموز الفوترة الإقليمية (ICD-10)** — مخفية لاختلاف الأنظمة",
        "page_about_excluded_3": "**التشخيص النهائي** — يتطلب دائماً مختصاً مرخصاً",
        "page_about_support_heading": "ادعم المشروع",
        "page_about_support_text": "التطبيق يستخدم واجهة OpenAI بتكلفة حقيقية. التبرعات عبر **Buy Me a Coffee** (الشريط الجانبي) تبقي MDxApp مجانياً.",
        "page_about_versions_heading": "سجل الإصدارات",
        "page_about_sources_heading": "المصادر",
        "page_about_caution_heading": "تحذير",
        "page_about_dev_heading": "رسالة من المطور",
        "page_contact_title": "اتصل بنا",
        "contact_form_name_ph": "اسمك",
        "contact_form_email_ph": "بريدك الإلكتروني",
        "contact_form_message_ph": "رسالتك",
        "contact_form_submit": "إرسال",
        "page1_header": "مساعد التشخيص الطبي",
        "language_selection": "اختر اللغة:",
        "submit": "إرسال",
        "caution_message": "يرجى العلم أن هذا التطبيق يدعم اتخاذ القرار الطبي ولا يغني عن التشخيص من قبل مختص مرخص. ننصح بمراجعات إضافية قبل أي قرار علاجي.",
    },
}


def main() -> None:
    data = json.loads(TRANS_PATH.read_text(encoding="utf-8"))
    english = data["English"]

    # Merge page keys into English and all languages
    for key, val in PAGE_KEYS_EN.items():
        english.setdefault(key, val)

    for lang, block in data.items():
        for key, val in PAGE_KEYS_EN.items():
            block.setdefault(key, val)
        if lang in LANG_OVERRIDES:
            block.update(LANG_OVERRIDES[lang])

    # Add new languages
    for lang in NEW_LANGUAGES:
        if lang not in data:
            block = dict(english)
            block.update(LANG_OVERRIDES.get(lang, {}))
            data[lang] = block
        elif lang in LANG_OVERRIDES:
            data[lang].update(LANG_OVERRIDES[lang])

    # Update English feature line if old text
    data["English"]["page_about_feature_5"] = PAGE_KEYS_EN["page_about_feature_5"]

    TRANS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {TRANS_PATH} — {len(data)} languages")


if __name__ == "__main__":
    main()
