"""
Orchestrates diagnosis requests: settings, prompts, AI client, and formatted output.
"""

from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

from ..config.settings import Settings, get_settings
from ..core.ai_client import DiagnosisAIClient, DiagnosisAPIResult, LegacyAIClient
from ..core.prompt_builder import PromptBuilder
from ..core.prompts import GPT5MiniPrompts, create_enhanced_prompts
from ..models.patient import PatientData
from ..utils.logger import get_logger

# Friendly messages for common OpenAI failures
_ERROR_HINTS = {
    "authentication": "Invalid OpenAI API key. Check your secrets configuration.",
    "rate_limit": "OpenAI rate limit reached. Please wait a moment and try again.",
    "connection": "Could not reach OpenAI. Check your network connection and try again.",
}


class DiagnosisResult(BaseModel):
    """Result of a diagnosis request for the UI layer."""

    success: bool = False
    html_content: Optional[str] = None
    error_message: Optional[str] = None
    is_structured: bool = False
    metadata: Optional[Dict[str, Any]] = None


class DiagnosisService:
    """Central service for running medical diagnosis through the AI stack."""

    def __init__(
        self,
        settings: Optional[Settings] = None,
        translations: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.translations = translations or {}
        self.logger = get_logger(__name__)
        self._client: Optional[Union[DiagnosisAIClient, LegacyAIClient]] = None
        self._prompt_builder: Optional[PromptBuilder] = None

    def _get_client(self) -> Union[DiagnosisAIClient, LegacyAIClient]:
        if self._client is None:
            if self.settings.use_new_ai_client:
                self._client = DiagnosisAIClient(
                    api_key=self.settings.openai_api_key,
                    model=self.settings.openai_model,
                    temperature=self.settings.openai_temperature,
                    max_tokens=self.settings.openai_max_tokens,
                    frequency_penalty=self.settings.openai_frequency_penalty,
                    presence_penalty=self.settings.openai_presence_penalty,
                    timeout_seconds=self.settings.openai_timeout_seconds,
                )
            else:
                self._client = LegacyAIClient(
                    api_key=self.settings.openai_api_key,
                    model=self.settings.openai_model,
                    temperature=self.settings.openai_temperature,
                    max_tokens=self.settings.openai_max_tokens,
                    frequency_penalty=self.settings.openai_frequency_penalty,
                    presence_penalty=self.settings.openai_presence_penalty,
                )
        return self._client

    def _get_prompt_builder(self) -> PromptBuilder:
        if self._prompt_builder is None:
            self._prompt_builder = PromptBuilder(
                prompt_words=self.settings.prompt_words,
                translations=self.translations,
            )
        return self._prompt_builder

    def _resolve_prompts(
        self, patient_data: PatientData, language: str, user_prompt: str
    ) -> tuple[str, str]:
        """Choose system/user prompts based on feature flags."""
        if self.settings.use_gpt5_mini_prompts:
            patient_dict = {
                "gender": patient_data.gender,
                "age": patient_data.age,
                "is_pregnant": patient_data.is_pregnant,
                "history": patient_data.history or "none",
                "symptoms": patient_data.symptoms,
                "exam_findings": patient_data.exam_findings or "none",
                "lab_results": patient_data.lab_results or "none",
            }
            return create_enhanced_prompts(
                patient_dict,
                language=language,
                use_structured=self.settings.use_structured_outputs,
            )
        system_prompt = self.settings.prompt_system
        if self.settings.use_structured_outputs:
            system_prompt = GPT5MiniPrompts.get_structured_system_prompt(language)
        return system_prompt, user_prompt

    @staticmethod
    def _friendly_error(raw: Optional[str]) -> str:
        if not raw:
            return "An unknown error occurred. Please try again."
        lower = raw.lower()
        if "authentication" in lower or "api key" in lower or "invalid_api_key" in lower:
            return _ERROR_HINTS["authentication"]
        if "rate limit" in lower or "rate_limit" in lower:
            return _ERROR_HINTS["rate_limit"]
        if "connection" in lower or "timeout" in lower:
            return _ERROR_HINTS["connection"]
        return raw

    def run(
        self,
        patient_data: PatientData,
        language: str,
        translations: Optional[Dict[str, str]] = None,
    ) -> DiagnosisResult:
        """
        Execute diagnosis for validated patient data.

        Args:
            patient_data: Validated patient information
            language: UI language key (e.g. English, Français)
            translations: Translation dict for current language (structured HTML labels)

        Returns:
            DiagnosisResult with HTML content or error message
        """
        from ..components.diagnosis_display import format_structured_diagnosis_html

        trans = translations or self.translations.get(language, {})
        builder = self._get_prompt_builder()
        user_prompt = builder.build_user_prompt(patient_data, language)
        system_prompt, user_prompt = self._resolve_prompts(patient_data, language, user_prompt)

        client = self._get_client()

        # Structured path (modern client with parse support)
        if self.settings.use_structured_outputs and self.settings.use_new_ai_client:
            structured_fn = getattr(client, "get_structured_diagnosis", None)
            if callable(structured_fn):
                api_result = structured_fn(system_prompt, user_prompt)
                if isinstance(api_result, DiagnosisAPIResult):
                    if api_result.success and api_result.structured:
                        html = format_structured_diagnosis_html(api_result.structured, trans)
                        return DiagnosisResult(
                            success=True,
                            html_content=html,
                            is_structured=True,
                        )
                    if api_result.error_message:
                        self.logger.warning(
                            "Structured diagnosis failed, falling back to plain: %s",
                            api_result.error_message,
                        )

        # Plain text path
        plain_result = client.get_diagnosis(system_prompt, user_prompt)
        if isinstance(plain_result, DiagnosisAPIResult):
            if plain_result.success and plain_result.content:
                cleaned = plain_result.content.replace("<|im_end|>", "").strip()
                return DiagnosisResult(success=True, html_content=cleaned, is_structured=False)
            return DiagnosisResult(
                success=False,
                error_message=self._friendly_error(plain_result.error_message),
            )

        if plain_result:
            cleaned = str(plain_result).replace("<|im_end|>", "").strip()
            return DiagnosisResult(success=True, html_content=cleaned, is_structured=False)

        return DiagnosisResult(
            success=False,
            error_message=self._friendly_error("Legacy OpenAI API call failed."),
        )


def get_diagnosis_service(
    translations: Optional[Dict[str, Dict[str, str]]] = None,
) -> DiagnosisService:
    """Factory for a configured DiagnosisService instance."""
    return DiagnosisService(translations=translations)
