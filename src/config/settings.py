"""
Centralized configuration management using Pydantic Settings.
Manages all application settings, secrets, and environment variables.
"""

from typing import List

import streamlit as st

from ..utils.logger import get_logger


class Settings:
    """
    Application settings loaded from Streamlit secrets or environment variables.
    Provides centralized access to all configuration values.
    """

    def __init__(self) -> None:
        """Initialize settings from Streamlit secrets."""
        # OpenAI Configuration
        self.openai_api_key: str = st.secrets.get("openai_api_key", "")
        self.openai_model: str = str(
            st.secrets.get("openai_api_model", "gpt-5.4-nano")
        )
        # Ignored for gpt-5* models (only default temperature supported)
        self.openai_temperature: float = float(st.secrets.get("openai_api_temp", 1.0))
        # GPT-5: reasoning tokens count toward this limit; use >= 8000 for structured output.
        self.openai_max_tokens: int = int(st.secrets.get("openai_api_maxtok", 8000))
        self.openai_frequency_penalty: float = float(st.secrets.get("openai_api_freqp", 0.0))
        self.openai_presence_penalty: float = float(st.secrets.get("openai_api_presp", 0.0))
        self.openai_timeout_seconds: float = float(st.secrets.get("openai_api_timeout", 120.0))
        _env = str(st.secrets.get("environment", "production"))
        self.log_openai_usage: bool = st.secrets.get("log_openai_usage", True)
        self.show_usage_in_ui: bool = st.secrets.get(
            "show_usage_in_ui", _env == "development"
        )

        # Application Configuration
        self.app_title: str = "MDxApp - Medical Diagnosis Assistant"
        self.app_version: str = str(st.secrets.get("app_version", "2.5.1"))
        self.app_icon: str = "🏥"

        # Contact Configuration
        self.email_address: str = st.secrets.get("email_address", "")

        # Prompt Configuration
        prompt_canvas = st.secrets.get("prompt_canvas", {})
        self.prompt_system: str = prompt_canvas.get("prompt_system", "")
        self.prompt_words: List[str] = prompt_canvas.get("prompt_words", [])

        # Feature Flags (GPT-5 Mini path enabled by default)
        self.use_new_ai_client: bool = st.secrets.get("use_new_ai_client", True)
        self.enable_logging: bool = st.secrets.get("enable_logging", True)
        self.enable_validation: bool = st.secrets.get("enable_validation", True)
        self.use_structured_outputs: bool = st.secrets.get("use_structured_outputs", True)
        self.use_gpt5_mini_prompts: bool = st.secrets.get("use_gpt5_mini_prompts", True)

        # Phase 2 feature flags
        self.enable_pdf_export: bool = st.secrets.get("enable_pdf_export", True)
        self.enable_evidence_fields: bool = st.secrets.get("enable_evidence_fields", True)
        # ICD-10 varies by region (WHO vs ICD-10-CM, etc.); off by default
        self.enable_icd10_codes: bool = st.secrets.get("enable_icd10_codes", False)
        self.enable_medical_imaging: bool = st.secrets.get("enable_medical_imaging", False)
        self.enable_drug_interactions: bool = st.secrets.get("enable_drug_interactions", True)

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

        if not self.prompt_system and not self.use_gpt5_mini_prompts:
            raise ValueError("System prompt is required when use_gpt5_mini_prompts is false")

        if not self.prompt_words and not self.use_gpt5_mini_prompts:
            raise ValueError("Prompt words are required when use_gpt5_mini_prompts is false")

        return True

    @property
    def is_gpt5_model(self) -> bool:
        """True when using a GPT-5 family model (reasoning shares completion token budget)."""
        return "gpt-5" in self.openai_model.lower()

    def effective_max_completion_tokens(self, *, structured: bool = False) -> int:
        """Minimum completion budget so GPT-5 reasoning does not exhaust structured output."""
        configured = self.openai_max_tokens
        if not self.is_gpt5_model:
            return configured
        floor = 8_000 if structured else 6_000
        return max(configured, floor)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        env = st.secrets.get("environment", "production")
        return str(env) == "development"


def get_settings() -> Settings:
    """
    Load settings from Streamlit secrets (fresh each call).

    Streamlit only reloads secrets.toml on server restart; after editing secrets,
    stop the app (Ctrl+C) and run ``streamlit run`` again.
    """
    settings = Settings()
    settings.validate()
    return settings


def log_openai_model_config() -> None:
    """Log configured model once per Streamlit session (helps verify secrets.toml)."""
    import streamlit as st
    import streamlit.config as st_config

    if st.session_state.get("mdx_openai_model_logged"):
        return
    settings = get_settings()
    logger = get_logger(__name__)
    try:
        secret_paths = st_config.get_option("secrets.files")
        logger.info("Streamlit secrets.toml search order (last wins): %s", secret_paths)
    except Exception:
        pass
    logger.info(
        "OpenAI model config: secrets[openai_api_model]=%s → using %s",
        st.secrets.get("openai_api_model", "<unset>"),
        settings.openai_model,
    )
    st.session_state["mdx_openai_model_logged"] = True
