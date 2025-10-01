"""
Centralized configuration management using Pydantic Settings.
Manages all application settings, secrets, and environment variables.
"""

from functools import lru_cache
from typing import List

import streamlit as st


class Settings:
    """
    Application settings loaded from Streamlit secrets or environment variables.
    Provides centralized access to all configuration values.
    """

    def __init__(self):
        """Initialize settings from Streamlit secrets."""
        # OpenAI Configuration
        self.openai_api_key: str = st.secrets.get("openai_api_key", "")
        self.openai_model: str = st.secrets.get("openai_api_model", "gpt-4o-mini")
        self.openai_temperature: float = float(st.secrets.get("openai_api_temp", 0.7))
        self.openai_max_tokens: int = int(st.secrets.get("openai_api_maxtok", 1000))
        self.openai_frequency_penalty: float = float(st.secrets.get("openai_api_freqp", 0.0))
        self.openai_presence_penalty: float = float(st.secrets.get("openai_api_presp", 0.0))

        # Application Configuration
        self.app_title: str = "MDxApp - Medical Diagnosis Assistant"
        self.app_version: str = "2.0.0"
        self.app_icon: str = "🏥"

        # Contact Configuration
        self.email_address: str = st.secrets.get("email_address", "")

        # Prompt Configuration
        prompt_canvas = st.secrets.get("prompt_canvas", {})
        self.prompt_system: str = prompt_canvas.get("prompt_system", "")
        self.prompt_words: List[str] = prompt_canvas.get("prompt_words", [])

        # Feature Flags (for gradual migration)
        self.use_new_ai_client: bool = st.secrets.get("use_new_ai_client", False)
        self.enable_logging: bool = st.secrets.get("enable_logging", True)
        self.enable_validation: bool = st.secrets.get("enable_validation", False)

        # Donation Configuration
        self.bmc_username: str = "geonosislaX"

        # Path Configuration
        self.assets_path: str = "Assets"
        self.materials_path: str = "Materials"

    def validate(self) -> bool:
        """
        Validate that all required settings are present.
        Returns True if valid, raises ValueError if not.
        """
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")

        if not self.prompt_system:
            raise ValueError("System prompt is required")

        if not self.prompt_words:
            raise ValueError("Prompt words are required")

        return True

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return st.secrets.get("environment", "production") == "development"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses LRU cache to avoid recreating settings on every call.

    Returns:
        Settings: Cached settings instance
    """
    settings = Settings()
    settings.validate()
    return settings
