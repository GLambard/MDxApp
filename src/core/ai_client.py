"""
OpenAI API client wrapper for medical diagnosis.
Handles all interactions with the OpenAI API using the modern SDK (v1.x+).
Optimized for GPT-5 Mini with structured outputs and latest best practices.
"""

from typing import Any, Dict, Literal, Optional

import openai
from openai import OpenAI
from pydantic import BaseModel, Field

from ..utils.logger import get_logger


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
    ):
        """
        Initialize the AI client with configuration.

        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-5-mini)
            temperature: Sampling temperature (default: 1.0 - only value supported by GPT-5 Mini)
            max_tokens: Maximum completion tokens (default: 2000)
            frequency_penalty: Frequency penalty (not supported by GPT-5 Mini)
            presence_penalty: Presence penalty (not supported by GPT-5 Mini)

        Note:
            GPT-5 Mini has specific parameter restrictions:
            - temperature: Only 1.0 is supported (default)
            - frequency_penalty: Not supported
            - presence_penalty: Not supported
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.is_gpt5_mini = "gpt-5" in model.lower()
        self.temperature = (
            temperature if not self.is_gpt5_mini else None
        )  # GPT-5 Mini doesn't support temperature
        self.max_completion_tokens = max_tokens
        self.frequency_penalty = frequency_penalty if not self.is_gpt5_mini else None
        self.presence_penalty = presence_penalty if not self.is_gpt5_mini else None
        self.logger = get_logger(__name__)

        if self.is_gpt5_mini:
            self.logger.info(
                f"Initialized DiagnosisAIClient with GPT-5 Mini (temperature=1.0 default only)"
            )
        else:
            self.logger.info(f"Initialized DiagnosisAIClient with model: {model}")

    def get_diagnosis(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> Optional[str]:
        """
        Get medical diagnosis from OpenAI API.

        Args:
            system_prompt: System-level instruction for AI behavior
            user_prompt: User query containing patient information
            **kwargs: Optional overrides for temperature, max_tokens, etc.

        Returns:
            str: AI-generated diagnosis text, or None if error occurs
        """
        # Allow per-request overrides
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)

        try:
            self.logger.info("Requesting diagnosis from OpenAI API")

            # Build parameters dict (GPT-5 Mini doesn't support temperature/penalties)
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_completion_tokens": max_completion_tokens,
            }

            # Only add these parameters for non-GPT-5 models
            if not self.is_gpt5_mini:
                if self.temperature is not None:
                    params["temperature"] = kwargs.get("temperature", self.temperature)
                if self.frequency_penalty is not None:
                    params["frequency_penalty"] = kwargs.get(
                        "frequency_penalty", self.frequency_penalty
                    )
                if self.presence_penalty is not None:
                    params["presence_penalty"] = kwargs.get(
                        "presence_penalty", self.presence_penalty
                    )

            response = self.client.chat.completions.create(**params)

            # Extract response content
            diagnosis = response.choices[0].message.content

            # Clean up any trailing tokens
            if diagnosis:
                cleaned = diagnosis.replace("<|im_end|>", "").strip()
                self.logger.info("Successfully received diagnosis from OpenAI API")
                return str(cleaned)
            
            return None

        except openai.AuthenticationError as e:
            self.logger.error(f"OpenAI authentication error: {e}")
            return None

        except openai.RateLimitError as e:
            self.logger.error(f"OpenAI rate limit exceeded: {e}")
            return None

        except openai.APIConnectionError as e:
            self.logger.error(f"OpenAI API connection error: {e}")
            return None

        except openai.APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None

        except Exception as e:
            self.logger.error(f"Unexpected error during OpenAI API call: {e}")
            return None

    def get_diagnosis_metadata(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Get diagnosis with metadata (usage, model info, etc.).

        Args:
            system_prompt: System-level instruction for AI behavior
            user_prompt: User query containing patient information
            **kwargs: Optional overrides for temperature, max_completion_tokens, etc.

        Returns:
            dict: Response with diagnosis and metadata, or None if error
        """
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)

        try:
            # Build parameters (GPT-5 Mini only supports specific params)
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_completion_tokens": max_completion_tokens,
            }

            # Only add temperature/penalties for non-GPT-5 models
            if not self.is_gpt5_mini:
                if self.temperature is not None:
                    params["temperature"] = kwargs.get("temperature", self.temperature)
                if self.frequency_penalty is not None:
                    params["frequency_penalty"] = kwargs.get(
                        "frequency_penalty", self.frequency_penalty
                    )
                if self.presence_penalty is not None:
                    params["presence_penalty"] = kwargs.get(
                        "presence_penalty", self.presence_penalty
                    )

            response = self.client.chat.completions.create(**params)

            diagnosis = response.choices[0].message.content
            if diagnosis:
                diagnosis = diagnosis.replace("<|im_end|>", "").strip()

            usage_data = {}
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
            self.logger.error(f"Error getting diagnosis with metadata: {e}")
            return None

    def get_structured_diagnosis(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> Optional[StructuredDiagnosisOutput]:
        """
        Get structured medical diagnosis using GPT-5 Mini with Pydantic output.
        Uses OpenAI's structured outputs feature for reliable JSON responses.

        Args:
            system_prompt: System-level instruction for AI behavior
            user_prompt: User query containing patient information
            **kwargs: Optional overrides for temperature, max_tokens, etc.

        Returns:
            StructuredDiagnosisOutput: Structured diagnosis with all components,
                                       or None if error occurs
        """
        max_completion_tokens = kwargs.get("max_completion_tokens", self.max_completion_tokens)

        try:
            self.logger.info("Requesting structured diagnosis from OpenAI API")

            # Build parameters for structured outputs (GPT-5 Mini restrictions apply)
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "response_format": StructuredDiagnosisOutput,
                "max_completion_tokens": max_completion_tokens,
            }

            # Only add temperature for non-GPT-5 models
            if not self.is_gpt5_mini and self.temperature is not None:
                params["temperature"] = kwargs.get("temperature", self.temperature)

            # Use structured outputs with response_format parameter
            completion = self.client.beta.chat.completions.parse(**params)

            # Extract structured output
            diagnosis_output = completion.choices[0].message.parsed

            self.logger.info("Successfully received structured diagnosis")
            return diagnosis_output

        except openai.AuthenticationError as e:
            self.logger.error(f"OpenAI authentication error: {e}")
            return None

        except openai.RateLimitError as e:
            self.logger.error(f"OpenAI rate limit exceeded: {e}")
            return None

        except openai.APIConnectionError as e:
            self.logger.error(f"OpenAI API connection error: {e}")
            return None

        except openai.APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None

        except Exception as e:
            self.logger.error(f"Unexpected error during structured diagnosis: {e}")
            return None

    def format_structured_diagnosis(
        self, diagnosis: StructuredDiagnosisOutput, language: str = "English"
    ) -> str:
        """
        Format structured diagnosis output as HTML for display.

        Args:
            diagnosis: Structured diagnosis output
            language: Language for formatting

        Returns:
            str: HTML-formatted diagnosis for Streamlit display
        """
        # Create formatted HTML output
        html_output = f"""
<div style="font-size: 16px; line-height: 1.6;">
    <h3 style="color: #1f77b4;">🔍 Primary Diagnosis</h3>
    <p style="font-size: 18px;"><strong>{diagnosis.primary_diagnosis}</strong></p>
    <p style="font-size: 14px; color: #666;">Confidence: {diagnosis.confidence_level.upper()}</p>

    <h3 style="color: #ff7f0e; margin-top: 20px;">🔬 Differential Diagnoses</h3>
    <ul>
"""
        for diff_dx in diagnosis.differential_diagnoses:
            html_output += f"        <li>{diff_dx}</li>\n"

        html_output += """    </ul>

    <h3 style="color: #2ca02c; margin-top: 20px;">📋 Recommended Next Steps</h3>
    <ol>
"""
        for step in diagnosis.recommended_next_steps:
            html_output += f"        <li>{step}</li>\n"

        html_output += """    </ol>

    <h3 style="color: #d62728; margin-top: 20px;">⚠️ Important Considerations</h3>
    <ul>
"""
        for consideration in diagnosis.important_considerations:
            html_output += f"        <li>{consideration}</li>\n"

        html_output += f"""    </ul>

    <h3 style="color: #9467bd; margin-top: 20px;">💡 Clinical Reasoning</h3>
    <p style="background-color: #f0f0f0; padding: 15px; border-radius: 5px;">
        {diagnosis.reasoning}
    </p>
</div>
"""
        return html_output


class LegacyAIClient:
    """
    Legacy OpenAI client using old SDK (v0.27.0) for backward compatibility.
    Maintains exact same interface as original implementation.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
        frequency_penalty: float,
        presence_penalty: float,
    ):
        """Initialize legacy client."""
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
            # Note: Using type ignore for legacy SDK compatibility
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
            self.logger.error(f"Legacy OpenAI API error: {e}")
            return None
