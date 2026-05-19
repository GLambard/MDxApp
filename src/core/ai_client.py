"""
OpenAI API client wrapper for medical diagnosis.
Handles all interactions with the OpenAI API using the modern SDK (v1.x+).
Optimized for GPT-5 Mini with structured outputs and latest best practices.
"""

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional

import openai
from openai import OpenAI
from pydantic import BaseModel, Field

from ..utils.logger import get_logger

DEFAULT_TIMEOUT_SECONDS = 120.0


@dataclass
class DiagnosisAPIResult:
    """Result of an OpenAI API call with optional error detail for the UI."""

    success: bool
    content: Optional[str] = None
    structured: Optional["StructuredDiagnosisOutput"] = None
    error_message: Optional[str] = None


class EvidenceItem(BaseModel):
    """Medical literature or guideline reference."""

    title: str = Field(description="Reference title")
    source: str = Field(description="Source name e.g. PubMed, WHO")
    url: Optional[str] = Field(default=None, description="Optional URL")
    pmid: Optional[str] = Field(default=None, description="PubMed ID if available")


class StructuredDiagnosisOutput(BaseModel):
    """
    Structured output format for medical diagnosis.
    Following OpenAI's structured outputs best practices for GPT-5 Mini.
    """

    primary_diagnosis: str = Field(
        description="The most likely medical diagnosis based on provided information"
    )
    differential_diagnoses: list[str] = Field(
        description="List of alternative possible diagnoses to consider", default_factory=list
    )
    recommended_next_steps: list[str] = Field(
        description="Recommended diagnostic tests, treatments, or consultations"
    )
    important_considerations: list[str] = Field(
        description="Important factors to consider, warnings, or contraindications"
    )
    confidence_level: Literal["high", "medium", "low"] = Field(
        description="Confidence level in the primary diagnosis"
    )
    reasoning: str = Field(description="Brief explanation of the diagnostic reasoning")
    # Phase 2B — evidence (optional)
    icd10_primary: Optional[str] = Field(default=None, description="ICD-10 for primary diagnosis")
    icd10_differentials: list[str] = Field(
        default_factory=list, description="ICD-10 codes for differentials"
    )
    evidence_items: list[EvidenceItem] = Field(
        default_factory=list, description="2-4 evidence-based references"
    )
    # Phase 2C — imaging (optional)
    imaging_findings: Optional[str] = Field(
        default=None, description="Findings from uploaded medical image if provided"
    )
    # Phase 2E — medications (optional)
    drug_interactions: list[str] = Field(
        default_factory=list, description="Medication interaction warnings"
    )
    medication_notes: Optional[str] = Field(
        default=None, description="Additional medication safety notes"
    )


class DiagnosisAIClient:
    """
    Wrapper for OpenAI API interactions with error handling and retry logic.
    Uses the modern OpenAI SDK (v1.x+) with client-based architecture.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5-mini",
        temperature: float = 1.0,
        max_tokens: int = 2000,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    ):
        """
        Initialize the AI client with configuration.

        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-5-mini)
            temperature: Sampling temperature (ignored for GPT-5 models)
            max_tokens: Maximum completion tokens (default: 2000)
            frequency_penalty: Frequency penalty (not supported by GPT-5 Mini)
            presence_penalty: Presence penalty (not supported by GPT-5 Mini)
            timeout_seconds: HTTP timeout for API requests
        """
        self.client = OpenAI(api_key=api_key, timeout=timeout_seconds)
        self.model = model
        self.is_gpt5_mini = "gpt-5" in model.lower()
        self.temperature = temperature if not self.is_gpt5_mini else None
        self.max_completion_tokens = max_tokens
        self.frequency_penalty = frequency_penalty if not self.is_gpt5_mini else None
        self.presence_penalty = presence_penalty if not self.is_gpt5_mini else None
        self.logger = get_logger(__name__)

        if self.is_gpt5_mini:
            self.logger.info(
                "Initialized DiagnosisAIClient with GPT-5 Mini (temperature=1.0 default only)"
            )
        else:
            self.logger.info("Initialized DiagnosisAIClient with model: %s", model)

    @staticmethod
    def _error_message(exc: Exception) -> str:
        return str(exc)

    def _build_chat_params(
        self, system_prompt: str, user_prompt: str, max_completion_tokens: int, **kwargs: Any
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_completion_tokens": max_completion_tokens,
        }
        if not self.is_gpt5_mini:
            if self.temperature is not None:
                params["temperature"] = kwargs.get("temperature", self.temperature)
            if self.frequency_penalty is not None:
                params["frequency_penalty"] = kwargs.get(
                    "frequency_penalty", self.frequency_penalty
                )
            if self.presence_penalty is not None:
                params["presence_penalty"] = kwargs.get("presence_penalty", self.presence_penalty)
        return params

    def get_diagnosis(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> DiagnosisAPIResult:
        """
        Get medical diagnosis from OpenAI API.

        Returns:
            DiagnosisAPIResult with content or error_message
        """
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)

        try:
            self.logger.info("Requesting diagnosis from OpenAI API")
            params = self._build_chat_params(
                system_prompt, user_prompt, max_completion_tokens, **kwargs
            )
            response = self.client.chat.completions.create(**params)
            diagnosis = response.choices[0].message.content

            if diagnosis:
                cleaned = diagnosis.replace("<|im_end|>", "").strip()
                self.logger.info("Successfully received diagnosis from OpenAI API")
                return DiagnosisAPIResult(success=True, content=str(cleaned))

            return DiagnosisAPIResult(
                success=False, error_message="OpenAI returned an empty response."
            )

        except openai.AuthenticationError as e:
            self.logger.error("OpenAI authentication error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except openai.RateLimitError as e:
            self.logger.error("OpenAI rate limit exceeded: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except openai.APIConnectionError as e:
            self.logger.error("OpenAI API connection error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except openai.APIError as e:
            self.logger.error("OpenAI API error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except Exception as e:
            self.logger.error("Unexpected error during OpenAI API call: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))

    def get_diagnosis_metadata(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> Optional[Dict[str, Any]]:
        """Get diagnosis with metadata (usage, model info, etc.)."""
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)

        try:
            params = self._build_chat_params(
                system_prompt, user_prompt, max_completion_tokens, **kwargs
            )
            response = self.client.chat.completions.create(**params)

            diagnosis = response.choices[0].message.content
            if diagnosis:
                diagnosis = diagnosis.replace("<|im_end|>", "").strip()

            usage_data: Dict[str, int] = {}
            if response.usage:
                usage_data = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }

            return {
                "diagnosis": diagnosis,
                "model": response.model,
                "usage": usage_data,
                "finish_reason": response.choices[0].finish_reason,
            }

        except Exception as e:
            self.logger.error("Error getting diagnosis with metadata: %s", e)
            return None

    def get_structured_diagnosis(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> DiagnosisAPIResult:
        """
        Get structured medical diagnosis using GPT-5 Mini with Pydantic output.
        """
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)

        try:
            self.logger.info("Requesting structured diagnosis from OpenAI API")
            params = self._build_chat_params(
                system_prompt, user_prompt, max_completion_tokens, **kwargs
            )
            params["response_format"] = StructuredDiagnosisOutput

            if not self.is_gpt5_mini and self.temperature is not None:
                params["temperature"] = kwargs.get("temperature", self.temperature)

            completion = self.client.beta.chat.completions.parse(**params)
            diagnosis_output = completion.choices[0].message.parsed

            if diagnosis_output:
                self.logger.info("Successfully received structured diagnosis")
                return DiagnosisAPIResult(success=True, structured=diagnosis_output)

            return DiagnosisAPIResult(
                success=False, error_message="Structured parse returned no data."
            )

        except openai.AuthenticationError as e:
            self.logger.error("OpenAI authentication error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except openai.RateLimitError as e:
            self.logger.error("OpenAI rate limit exceeded: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except openai.APIConnectionError as e:
            self.logger.error("OpenAI API connection error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except openai.APIError as e:
            self.logger.error("OpenAI API error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))
        except Exception as e:
            self.logger.error("Unexpected error during structured diagnosis: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))

    def get_structured_diagnosis_with_image(
        self,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        mime_type: str = "image/jpeg",
        **kwargs: Any,
    ) -> DiagnosisAPIResult:
        """Structured diagnosis with one vision image (GPT-5 Mini multimodal)."""
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)
        data_url = f"data:{mime_type};base64,{image_base64}"

        try:
            self.logger.info("Requesting multimodal structured diagnosis")
            params: Dict[str, Any] = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {"type": "image_url", "image_url": {"url": data_url}},
                        ],
                    },
                ],
                "response_format": StructuredDiagnosisOutput,
                "max_completion_tokens": max_completion_tokens,
            }
            completion = self.client.beta.chat.completions.parse(**params)
            diagnosis_output = completion.choices[0].message.parsed
            if diagnosis_output:
                return DiagnosisAPIResult(success=True, structured=diagnosis_output)
            return DiagnosisAPIResult(
                success=False, error_message="Multimodal structured parse returned no data."
            )
        except Exception as e:
            self.logger.error("Multimodal diagnosis error: %s", e)
            return DiagnosisAPIResult(success=False, error_message=self._error_message(e))

    def format_structured_diagnosis(
        self,
        diagnosis: StructuredDiagnosisOutput,
        translations: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Format structured diagnosis output as HTML (delegates to diagnosis_display).

        Deprecated: prefer format_structured_diagnosis_html from components.
        """
        from ..components.diagnosis_display import format_structured_diagnosis_html

        return format_structured_diagnosis_html(diagnosis, translations)


class LegacyAIClient:
    """Legacy OpenAI client using old SDK (v0.27.0) for backward compatibility."""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
        frequency_penalty: float,
        presence_penalty: float,
    ):
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.logger = get_logger(__name__)

    def get_diagnosis(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> Optional[str]:
        """Get diagnosis using legacy OpenAI SDK."""
        try:
            response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=None,
            )
            content = response["choices"][0]["message"]["content"]
            return str(content) if content else None
        except Exception as e:
            self.logger.error("Legacy OpenAI API error: %s", e)
            return None
