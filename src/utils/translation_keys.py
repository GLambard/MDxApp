"""Shared translation key constants and helpers."""

# Keys that may stay identical across languages (brands, placeholders)
UNTRANSLATED_OK = frozenset(
    {
        "none",
        "dx_icd10",
        "pdf_title",
    }
)
