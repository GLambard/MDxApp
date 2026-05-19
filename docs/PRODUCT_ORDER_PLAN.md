# MDxApp Product Roadmap — Implementation Plan

**Status:** v2.5.1 — Phase 2 complete; default model **gpt-5.4-nano**  
**Stack:** Streamlit + `src/` services + OpenAI GPT-5 family (`openai_api_model` in secrets)

---

## Completed

### Phase 0–1
- Modular `DiagnosisService`, structured outputs, i18n diagnosis UI
- Confidence badges, expanders, plain-text fallback, GPT-5 Mini parameters, tests

### Phase 2A–2E
| Phase | Feature | Status |
|-------|---------|--------|
| 2A | PDF export (ReportLab) | ✅ |
| 2B | Evidence references | ✅ (ICD-10 display off by default — regional variance) |
| 2C | Medical imaging | ✅ code; **disabled** in secrets (`enable_medical_imaging = false`) |
| 2D | 15 languages + RTL (Arabic) + localized About/Contact | ✅ |
| 2E | Drug interactions (OpenFDA + LLM) | ✅ |

### Recent polish (2026)
- Default model **`gpt-5.4-nano`** (`openai_api_model` in `.streamlit/secrets.toml`)
- **15 languages**, Arabic RTL, localized About/Contact (shared sidebar language selector)
- About page updated for v2.5
- Evidence sanitization (PubMed URLs, dedupe, no fabricated links in prompt)
- OpenAI token usage logging + optional sidebar display
- GPT-5 completion token floor (8000+) and length-limit retry
- PDF / session-state / dark-mode donation fixes

---

## Feature flags (`.streamlit/secrets.toml`)

| Key | Default | Purpose |
|-----|---------|---------|
| `enable_pdf_export` | `true` | PDF download button |
| `enable_evidence_fields` | `true` | References expander |
| `enable_icd10_codes` | `false` | Regional coding (off) |
| `enable_medical_imaging` | `false` | Vision upload (off until validated) |
| `enable_drug_interactions` | `true` | Medication warnings |
| `openai_api_maxtok` | `8000` | GPT-5 structured output budget |
| `log_openai_usage` | `true` | Log tokens to console |
| `show_usage_in_ui` | `false` | Sidebar token caption (`true` in development) |

---

## Next actions (recommended order)

1. **Deploy** — Streamlit Cloud secrets aligned with `secrets.toml.example`
2. **Translation QA** — [`TRANSLATION_QA.md`](TRANSLATION_QA.md) for 中文, Português, हिन्दी, العربية, Русский
3. **Medical imaging pilot** — enable flag locally only after clinical review
4. **Phase 3** (pick one track):
   - Trust: red-flag highlighting, stronger disclaimers
   - Reach: more languages, RTL polish
   - Sustainability: usage limits, optional support tiers

---

## Cross-cutting

- Tests: `pytest tests/`
- Docs: keep `EXECUTIVE_SUMMARY.md` in sync with releases
- Do not edit Cursor plan files in `.cursor/plans/`
