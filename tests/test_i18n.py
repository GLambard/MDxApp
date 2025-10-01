"""
Unit tests for internationalization utilities.
Tests translation loading and retrieval.
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.utils.i18n import I18n, load_translations


class TestI18n:
    """Test cases for I18n class."""

    @pytest.fixture
    def sample_translations_file(self):
        """Create a temporary translations file for testing."""
        translations = {
            "English": {
                "greeting": "Hello",
                "farewell": "Goodbye",
                "none": "none"
            },
            "Français": {
                "greeting": "Bonjour",
                "farewell": "Au revoir",
                "none": "aucun"
            },
            "Español": {
                "greeting": "Hola",
                "farewell": "Adiós"
                # Intentionally missing "none" to test fallback
            }
        }

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump(translations, f)
            temp_path = Path(f.name)

        yield temp_path

        # Cleanup
        temp_path.unlink()

    def test_load_translations(self, sample_translations_file):
        """Test loading translations from file."""
        i18n = I18n(sample_translations_file)

        assert len(i18n.translations) == 3
        assert "English" in i18n.translations
        assert "Français" in i18n.translations
        assert "Español" in i18n.translations

    def test_get_translation(self, sample_translations_file):
        """Test retrieving a translation."""
        i18n = I18n(sample_translations_file)

        greeting = i18n.get("English", "greeting")
        assert greeting == "Hello"

        greeting_fr = i18n.get("Français", "greeting")
        assert greeting_fr == "Bonjour"

    def test_get_translation_with_fallback(self, sample_translations_file):
        """Test fallback to default language when translation missing."""
        i18n = I18n(sample_translations_file)

        # "none" is missing in Español, should fallback to English
        none_text = i18n.get("Español", "none")
        assert none_text == "none"  # English fallback

    def test_get_translation_with_default(self, sample_translations_file):
        """Test using default value when translation not found."""
        i18n = I18n(sample_translations_file)

        result = i18n.get("English", "nonexistent_key", default="N/A")
        assert result == "N/A"

    def test_get_available_languages(self, sample_translations_file):
        """Test getting list of available languages."""
        i18n = I18n(sample_translations_file)

        languages = i18n.get_available_languages()
        assert len(languages) == 3
        assert "English" in languages
        assert "Français" in languages
        assert "Español" in languages

    def test_language_exists(self, sample_translations_file):
        """Test checking if a language exists."""
        i18n = I18n(sample_translations_file)

        assert i18n.language_exists("English") is True
        assert i18n.language_exists("Français") is True
        assert i18n.language_exists("Deutsch") is False

    def test_get_all_translations(self, sample_translations_file):
        """Test getting all translations for a language."""
        i18n = I18n(sample_translations_file)

        english_translations = i18n.get_all("English")
        assert english_translations["greeting"] == "Hello"
        assert english_translations["farewell"] == "Goodbye"

    def test_add_translation(self, sample_translations_file):
        """Test adding a new translation at runtime."""
        i18n = I18n(sample_translations_file)

        i18n.add_translation("English", "new_key", "New Value")

        result = i18n.get("English", "new_key")
        assert result == "New Value"


def test_load_translations_function(tmp_path):
    """Test the standalone load_translations function."""
    translations = {
        "English": {"test": "value"}
    }

    # Create temporary file
    trans_file = tmp_path / "test_translations.json"
    with open(trans_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f)

    loaded = load_translations(trans_file)

    assert loaded == translations
    assert loaded["English"]["test"] == "value"

