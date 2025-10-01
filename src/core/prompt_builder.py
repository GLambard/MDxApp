"""
Prompt builder for constructing AI queries.
Handles the construction of prompts from patient data and templates.
"""

from typing import Dict, List, Optional
from ..models.patient import PatientData
from ..utils.logger import get_logger


class PromptBuilder:
    """
    Builds prompts for AI diagnosis from patient data and templates.
    Supports multiple languages and customizable prompt templates.
    """
    
    def __init__(self, prompt_words: List[str], translations: Dict[str, Dict[str, str]]):
        """
        Initialize the prompt builder with templates.
        
        Args:
            prompt_words: List of prompt template words/phrases
            translations: Translation dictionary for all supported languages
        """
        self.prompt_words = prompt_words
        self.translations = translations
        self.logger = get_logger(__name__)
    
    def build_user_prompt(
        self,
        patient_data: PatientData,
        language: str = "English"
    ) -> str:
        """
        Build the user prompt from patient data.
        
        Args:
            patient_data: Patient information
            language: Target language for the response
        
        Returns:
            str: Formatted user prompt for AI
        """
        # Get translations for the selected language
        trans = self.translations.get(language, self.translations["English"])
        
        # Get default values for missing data
        none_text = trans.get("none", "none")
        years_old_text = trans.get("vissum_yrsold", " years old")
        
        # Replace None/empty values with "none" text
        history = patient_data.history if patient_data.history else none_text
        symptoms = patient_data.symptoms
        exam = patient_data.exam_findings if patient_data.exam_findings else none_text
        lab = patient_data.lab_results if patient_data.lab_results else none_text
        
        # Ensure we have enough prompt words (default templates if not)
        if len(self.prompt_words) >= 10:
            # Use configured prompt words
            prompt = (
                f"{self.prompt_words[0]}{patient_data.gender}, "
                f"{patient_data.age}{years_old_text}. "
                f"{self.prompt_words[1]}{patient_data.is_pregnant}. "
                f"{self.prompt_words[2]}{history}. "
                f"{self.prompt_words[3]}{symptoms}. "
                f"{self.prompt_words[4]}{exam}. "
                f"{self.prompt_words[5]}{lab}. "
                f"{self.prompt_words[6]}"
                f"{self.prompt_words[7]}"
                f"{self.prompt_words[8]}"
                f"{self.prompt_words[9]}{language}. "
            )
        else:
            # Fallback to simple template
            prompt = self._build_default_prompt(
                patient_data, 
                language, 
                years_old_text, 
                history, 
                symptoms, 
                exam, 
                lab
            )
        
        self.logger.debug(f"Built user prompt for language: {language}")
        return prompt
    
    def _build_default_prompt(
        self,
        patient_data: PatientData,
        language: str,
        years_old_text: str,
        history: str,
        symptoms: str,
        exam: str,
        lab: str
    ) -> str:
        """
        Build a default prompt when prompt_words are not configured.
        
        Args:
            patient_data: Patient information
            language: Target language
            years_old_text: Translation for "years old"
            history: Patient history text
            symptoms: Patient symptoms text
            exam: Examination findings text
            lab: Lab results text
        
        Returns:
            str: Default formatted prompt
        """
        prompt = f"""Patient Information:
- Gender: {patient_data.gender}
- Age: {patient_data.age}{years_old_text}
- Pregnant: {patient_data.is_pregnant}
- History: {history}
- Symptoms: {symptoms}
- Examination: {exam}
- Lab Results: {lab}

Please provide a medical diagnosis based on this information.
Respond in {language}.
Include:
1. Most likely diagnosis
2. Differential diagnoses
3. Recommended next steps
4. Important considerations
"""
        return prompt
    
    def build_visual_summary(
        self,
        patient_data: PatientData,
        language: str = "English"
    ) -> str:
        """
        Build a formatted HTML summary of patient data for display.
        
        Args:
            patient_data: Patient information
            language: Language for labels
        
        Returns:
            str: HTML-formatted summary
        """
        trans = self.translations.get(language, self.translations["English"])
        
        # Get default values
        none_text = trans.get("none", "none")
        years_old_text = trans.get("vissum_yrsold", " years old")
        
        # Replace empty values
        history = patient_data.history if patient_data.history else none_text
        exam = patient_data.exam_findings if patient_data.exam_findings else none_text
        lab = patient_data.lab_results if patient_data.lab_results else none_text
        
        summary = (
            '<p style="font-size:18px;">'
            f'<b>{trans.get("vissum_patient", "Patient: ")}</b>'
            f'{patient_data.gender}, {patient_data.age}{years_old_text}<br/>'
            f'<b>{trans.get("vissum_pregnancy", "Pregnancy: ")}</b>{patient_data.is_pregnant}<br/>'
            f'<b>{trans.get("vissum_history", "History: ")}</b>{history}<br/>'
            f'<b>{trans.get("vissum_symp", "Symptoms: ")}</b>{patient_data.symptoms}<br/>'
            f'<b>{trans.get("vissum_exam", "Examination findings: ")}</b>{exam}<br/>'
            f'<b>{trans.get("vissum_lab", "Laboratory test results: ")}</b>{lab}<br/>'
            '</p>'
        )
        
        return summary
    
    def validate_prompt_configuration(self) -> bool:
        """
        Validate that prompt configuration is complete.
        
        Returns:
            bool: True if configuration is valid
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.prompt_words:
            raise ValueError("Prompt words are not configured")
        
        if not self.translations:
            raise ValueError("Translations are not configured")
        
        if len(self.prompt_words) < 10:
            self.logger.warning(
                f"Prompt words has only {len(self.prompt_words)} items, "
                "expected at least 10. Using default prompt template."
            )
        
        return True

