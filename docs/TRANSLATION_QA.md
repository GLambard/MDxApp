# Translation QA Checklist

## Languages (15)

English, Français, Español, Deutsch, Italiano, Português, 中文, 日本語, 한국어, Русский, العربية, हिन्दी, Türkçe, Tiếng Việt, Bahasa Indonesia

## Per-language review

- [ ] All UI keys present (compare key count to English)
- [ ] Medical tone appropriate
- [ ] `dx_*` diagnosis section labels correct
- [ ] PDF / imaging / medication strings reviewed
- [ ] Arabic: RTL layout on Diagnosis, About, and Contact pages
- [ ] About / Contact pages match selected sidebar language
- [ ] Submit flow and caution disclaimer clear

## Regenerate packs

After editing locale data:

```bash
python3 scripts/merge_locale_packs.py
```

## Smoke test

1. Select language in sidebar (page should refresh; labels update)
2. Verify form labels (gender, symptoms, submit) are translated
3. Open About and Contact — content matches selected language
4. Submit sample case on Diagnosis page
5. Verify structured sections and PDF button label
