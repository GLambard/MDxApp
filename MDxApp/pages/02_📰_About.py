import os
import sys
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html

path = os.path.dirname(__file__)
project_root = Path(path).parent.parent
sys.path.insert(0, str(project_root))

from src.components.donation import get_default_qr_path, render_sidebar_donation
from src.config.settings import get_settings
from src.utils.styling import load_main_styles

st.set_page_config(page_title="About", page_icon="📰", layout="wide")
load_main_styles(project_root)

settings = get_settings()

translations_en = {
    "English": {
        "bmc_0": "Let's keep MDxApp free!",
        "bmc_1": "By clicking here:",
        "bmc_2": "Or use this QR code:",
    }
}

with st.sidebar:
    render_sidebar_donation(
        username="geonosislaX",
        translations=translations_en,
        language="English",
        qr_image_path=get_default_qr_path(project_root),
    )

st.header("About MDxApp")

st.markdown(
    f"""
### What is MDxApp?

MDxApp is a **free medical diagnosis assistant** that helps clinicians, students, and patients
organize symptoms and receive an **AI-assisted preliminary assessment**. It runs on
[OpenAI](https://openai.com/) **{settings.openai_model}** with structured outputs for clear,
actionable results.

### Current features (v{settings.app_version})

- **Structured diagnosis** — primary diagnosis, differentials, next steps, considerations, confidence, clinical reasoning
- **PDF report download** — shareable summary after each assessment
- **Educational references** — optional literature links when the model provides verifiable PMIDs or URLs
- **Medication safety notes** — interaction warnings when medications are listed (OpenFDA + AI)
- **10 languages** — English, Français, 日本語, Español, Deutsch, 中文, Português, हिन्दी, العربية, Русский
- **Privacy-first** — no patient data stored on our servers; each session is ephemeral

### Not included (by design)

- **Medical imaging upload** — disabled while we validate safety and accuracy (can be enabled later via configuration)
- **Regional billing codes (ICD-10, etc.)** — hidden because coding systems differ by country
- **Final diagnosis** — always requires a licensed clinician; this tool is educational and assistive only

### Support the project

The app uses the OpenAI API, which has a real cost per request. Donations via **Buy Me a Coffee**
(see the sidebar) help keep MDxApp free for everyone. Thank you for your support.

### Version history

| Version | Date | Highlights |
|---------|------|------------|
| **2.5.0** | 2026 | Phase 2: PDF export, references, 10 languages, drug checks, GPT-5 Mini, modular `src/` architecture |
| **2.0.0** | 2025 | Modernized codebase, structured outputs, tests, external CSS |
| **1.12x** | 2023 | Multilingual UI expansion, ChatGPT integration |
| **1.0** | 2023 | Initial public release |

### Sources

- Source code: [github.com/GLambard/MDxApp](https://github.com/GLambard/MDxApp)
- Example cases on the main page are adapted from public teaching material (e.g. [@BrownJHM](https://twitter.com/BrownJHM)).

### :rotating_light: Caution :rotating_light:

This app supports medical decision-making; it does **not** replace evaluation by a licensed
professional. Seek urgent care for emergencies. Verify all suggestions before treatment decisions.

### Message from the developer

> Dear community,
>
> Thank you for using MDxApp. This project is built in spare time to make diagnostic thinking
> more accessible worldwide. Your feedback and coffee support keep it running.
>
> — **Guillaume Lambard**  
> AI solutions designer and developer
"""
)

html(
    """
    <a class="github-button" href="https://github.com/GLambard/MDxApp" data-show-count="true"
       aria-label="Follow @GLambard on GitHub">Follow @GLambard</a>
    <script async defer src="https://buttons.github.io/buttons.js"></script>
    <a class="twitter-follow-button" href="https://twitter.com/gamlambard">Follow @gamlambard</a>
    <script async defer src="https://platform.twitter.com/widgets.js"></script>
    """
)
