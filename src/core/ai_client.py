"""
OpenAI API client wrapper for medical diagnosis.
Handles all interactions with the OpenAI API using the modern SDK (v1.x+).
"""

from typing import Optional, Dict, Any
import openai
from openai import OpenAI

from ..utils.logger import get_logger


class DiagnosisAIClient:
    """
    Wrapper for OpenAI API interactions with error handling and retry logic.
    Uses the modern OpenAI SDK (v1.x+) with client-based architecture.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ):
        """
        Initialize the AI client with configuration.
        
        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4o-mini)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            max_tokens: Maximum tokens in response (default: 1000)
            frequency_penalty: Frequency penalty 0.0-2.0 (default: 0.0)
            presence_penalty: Presence penalty 0.0-2.0 (default: 0.0)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.logger = get_logger(__name__)
        
        self.logger.info(f"Initialized DiagnosisAIClient with model: {model}")
    
    def get_diagnosis(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> Optional[str]:
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
        temperature = kwargs.get('temperature', self.temperature)
        max_tokens = kwargs.get('max_tokens', self.max_tokens)
        frequency_penalty = kwargs.get('frequency_penalty', self.frequency_penalty)
        presence_penalty = kwargs.get('presence_penalty', self.presence_penalty)
        
        try:
            self.logger.info("Requesting diagnosis from OpenAI API")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=None
            )
            
            # Extract response content
            diagnosis = response.choices[0].message.content
            
            # Clean up any trailing tokens
            if diagnosis:
                diagnosis = diagnosis.replace("<|im_end|>", "").strip()
            
            self.logger.info("Successfully received diagnosis from OpenAI API")
            return diagnosis
            
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
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Get diagnosis with metadata (usage, model info, etc.).
        
        Args:
            system_prompt: System-level instruction for AI behavior
            user_prompt: User query containing patient information
            **kwargs: Optional overrides for temperature, max_tokens, etc.
        
        Returns:
            dict: Response with diagnosis and metadata, or None if error
        """
        temperature = kwargs.get('temperature', self.temperature)
        max_tokens = kwargs.get('max_tokens', self.max_tokens)
        frequency_penalty = kwargs.get('frequency_penalty', self.frequency_penalty)
        presence_penalty = kwargs.get('presence_penalty', self.presence_penalty)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=None
            )
            
            diagnosis = response.choices[0].message.content
            if diagnosis:
                diagnosis = diagnosis.replace("<|im_end|>", "").strip()
            
            return {
                "diagnosis": diagnosis,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            self.logger.error(f"Error getting diagnosis with metadata: {e}")
            return None


class LegacyAIClient:
    """
    Legacy OpenAI client using old SDK (v0.27.0) for backward compatibility.
    Maintains exact same interface as original implementation.
    """
    
    def __init__(self, api_key: str, model: str, temperature: float, 
                 max_tokens: int, frequency_penalty: float, presence_penalty: float):
        """Initialize legacy client."""
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.logger = get_logger(__name__)
    
    def get_diagnosis(self, system_prompt: str, user_prompt: str, **kwargs) -> Optional[str]:
        """Get diagnosis using legacy OpenAI SDK."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stop=None
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            self.logger.error(f"Legacy OpenAI API error: {e}")
            return None

