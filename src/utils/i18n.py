"""
Internationalization (i18n) utilities for MDxApp.
Handles translation loading, retrieval, and language management.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.logger import get_logger


class I18n:
    """
    Internationalization helper for managing translations.
    Provides easy access to translations with fallback support.
    """

    def __init__(self, translations_path: Path):
        """
        Initialize i18n with translations from file.

        Args:
            translations_path: Path to translations JSON file
        """
        self.logger = get_logger(__name__)
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.default_language = "English"
        self.translations_path = translations_path

        self.load_translations()

    def load_translations(self) -> None:
        """
        Load translations from JSON file.

        Raises:
            FileNotFoundError: If translations file doesn't exist
            JSONDecodeError: If translations file is invalid JSON
        """
        try:
            with open(self.translations_path, encoding="utf-8") as f:
                self.translations = json.load(f)

            self.logger.info(f"Loaded translations for {len(self.translations)} languages")
        except FileNotFoundError:
            self.logger.error(f"Translations file not found: {self.translations_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in translations file: {e}")
            raise

    def get(self, language: str, key: str, default: Optional[str] = None) -> str:
        """
        Get translation for a specific key and language with fallback.

        Args:
            language: Target language (e.g., "English", "Français")
            key: Translation key
            default: Default value if translation not found

        Returns:
            str: Translated text or default value
        """
        # Try to get translation for requested language
        if language in self.translations:
            if key in self.translations[language]:
                return self.translations[language][key]

        # Fallback to default language
        if self.default_language in self.translations:
            if key in self.translations[self.default_language]:
                self.logger.debug(
                    f"Translation '{key}' not found for '{language}', "
                    f"using {self.default_language}"
                )
                return self.translations[self.default_language][key]

        # Return default or key itself
        if default is not None:
            return default

        self.logger.warning(f"Translation not found: {language}.{key}")
        return key

    def get_all(self, language: str) -> Dict[str, Any]:
        """
        Get all translations for a specific language.

        Args:
            language: Target language

        Returns:
            dict: All translations for the language, or default language if not found
        """
        if language in self.translations:
            return self.translations[language]

        self.logger.warning(f"Language '{language}' not found, using {self.default_language}")
        return self.translations.get(self.default_language, {})

    def get_available_languages(self) -> List[str]:
        """
        Get list of all available languages.

        Returns:
            list: List of language names
        """
        return list(self.translations.keys())

    def language_exists(self, language: str) -> bool:
        """
        Check if a language is available.

        Args:
            language: Language to check

        Returns:
            bool: True if language exists
        """
        return language in self.translations

    def add_translation(self, language: str, key: str, value: str) -> None:
        """
        Add or update a translation (runtime only, doesn't save to file).

        Args:
            language: Target language
            key: Translation key
            value: Translation value
        """
        if language not in self.translations:
            self.translations[language] = {}

        self.translations[language][key] = value
        self.logger.debug(f"Added translation: {language}.{key}")

    def reload_translations(self) -> None:
        """Reload translations from file (useful for hot-reload in dev)."""
        self.load_translations()
        self.logger.info("Translations reloaded")


def load_translations(translations_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Simple function to load translations from JSON file.

    Args:
        translations_path: Path to translations JSON file

    Returns:
        dict: Translation dictionary
    """
    with open(translations_path, encoding="utf-8") as f:
        return json.load(f)
