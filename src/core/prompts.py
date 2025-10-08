"""
Enhanced prompt templates for GPT-5 Mini.
Follows OpenAI's latest best practices for medical diagnosis.
Optimized for GPT-5 Mini's 400K context window and multimodal capabilities.
"""

from typing import Any, Dict


class GPT5MiniPrompts:
    """
    Optimized prompts for GPT-5 Mini following OpenAI best practices.
    Reference: https://platform.openai.com/docs/guides/prompt-engineering

    GPT-5 Mini Features:
    - 400,000 token context window
    - Multimodal (text + images)
    - Enhanced function calling
    - Better reasoning capabilities
    """

    @staticmethod
    def get_system_prompt(language: str = "English") -> str:
        """
        Get optimized system prompt for medical diagnosis.
        Following GPT-5 Mini best practices:
        - Clear role definition
        - Specific constraints
        - Output format guidance
        - Leverages 400K context window

        Args:
            language: Target language for responses

        Returns:
            str: System prompt
        """
        prompt = f"""You are an experienced medical AI assistant designed to help healthcare professionals with preliminary diagnostic assessments.

Your role:
- Analyze patient information comprehensively
- Provide evidence-based diagnostic suggestions
- Consider differential diagnoses
- Recommend appropriate next steps
- Highlight important clinical considerations

Guidelines:
1. Base your diagnosis on the provided patient information
2. Consider age, gender, pregnancy status, history, symptoms, examination findings, and lab results
3. Provide clear, actionable recommendations
4. Include differential diagnoses when appropriate
5. Highlight any urgent or critical findings
6. Note important contraindications or considerations
7. Respond in {language}

Important:
- This is a preliminary assessment tool
- All diagnoses should be confirmed by licensed medical professionals
- Consider patient safety as the top priority
- If information is insufficient, state what additional data is needed"""

        return prompt

    @staticmethod
    def get_user_prompt_enhanced(
        gender: str,
        age: int,
        is_pregnant: str,
        history: str,
        symptoms: str,
        exam_findings: str,
        lab_results: str,
        language: str = "English",
    ) -> str:
        """
        Build enhanced user prompt following OpenAI best practices for GPT-5 Mini.
        Uses clear structure and explicit instructions.
        Optimized for GPT-5 Mini's advanced reasoning capabilities.

        Args:
            gender: Patient gender
            age: Patient age
            is_pregnant: Pregnancy status
            history: Medical/environmental history
            symptoms: Patient symptoms
            exam_findings: Physical examination findings
            lab_results: Laboratory test results
            language: Target language for response

        Returns:
            str: Formatted user prompt
        """
        prompt = f"""Please provide a comprehensive medical diagnostic assessment for the following patient:

## Patient Demographics
- **Gender**: {gender}
- **Age**: {age} years old
- **Pregnancy Status**: {is_pregnant}

## Clinical Information

### History and Context
{history if history and history != "none" else "No relevant history provided"}

### Presenting Symptoms
{symptoms}

### Physical Examination Findings
{exam_findings if exam_findings and exam_findings != "none" else "No examination findings documented"}

### Laboratory Results
{lab_results if lab_results and lab_results != "none" else "No laboratory results available"}

## Required Assessment

Please provide a structured diagnostic assessment including:

1. **Primary Diagnosis**: Most likely diagnosis based on the information
2. **Differential Diagnoses**: List 2-4 alternative diagnoses to consider
3. **Recommended Next Steps**: Specific tests, treatments, or consultations needed
4. **Important Considerations**: Warnings, contraindications, or critical factors
5. **Confidence Level**: Your confidence in the primary diagnosis (high/medium/low)
6. **Clinical Reasoning**: Brief explanation of your diagnostic thinking

Respond in {language}. Be specific, evidence-based, and prioritize patient safety."""

        return prompt

    @staticmethod
    def get_structured_system_prompt(language: str = "English") -> str:
        """
        Get system prompt optimized for structured JSON outputs.
        Specifically designed for GPT-5 Mini structured outputs feature.

        Args:
            language: Target language for responses

        Returns:
            str: System prompt for structured outputs
        """
        prompt = f"""You are a medical diagnostic AI assistant providing structured diagnostic assessments.

Role: Analyze patient information and provide comprehensive diagnostic evaluations.

Output Requirements:
- Always provide a primary diagnosis
- Include 2-4 differential diagnoses
- List 3-5 recommended next steps
- Highlight 2-4 important clinical considerations
- Assess confidence level (high/medium/low)
- Provide clear clinical reasoning

Clinical Guidelines:
- Base assessments on evidence-based medicine
- Consider patient demographics (age, gender, pregnancy)
- Integrate all provided information (history, symptoms, exam, labs)
- Prioritize patient safety
- Note when information is insufficient
- Respond in {language}

Safety:
- This is a preliminary assessment tool
- Final diagnosis requires licensed medical professional
- Highlight urgent findings
- Consider contraindications"""

        return prompt


def create_enhanced_prompts(
    patient_data: Dict[str, Any], language: str = "English", use_structured: bool = True
) -> tuple[str, str]:
    """
    Create optimized prompts for GPT-5 Mini.

    Args:
        patient_data: Dictionary containing patient information
        language: Target language for responses
        use_structured: Whether to use structured output prompts

    Returns:
        tuple: (system_prompt, user_prompt)
    """
    prompts = GPT5MiniPrompts()

    if use_structured:
        system_prompt = prompts.get_structured_system_prompt(language)
    else:
        system_prompt = prompts.get_system_prompt(language)

    user_prompt = prompts.get_user_prompt_enhanced(
        gender=patient_data.get("gender", "Unknown"),
        age=patient_data.get("age", 0),
        is_pregnant=patient_data.get("is_pregnant", "no"),
        history=patient_data.get("history", "none"),
        symptoms=patient_data.get("symptoms", ""),
        exam_findings=patient_data.get("exam_findings", "none"),
        lab_results=patient_data.get("lab_results", "none"),
        language=language,
    )

    return system_prompt, user_prompt
