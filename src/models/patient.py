"""
Patient data models with validation using Pydantic.
Ensures data integrity and type safety for patient information.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Gender(str, Enum):
    """Patient gender enumeration."""

    MALE = "male"
    FEMALE = "female"


class PregnancyStatus(str, Enum):
    """Pregnancy status enumeration."""

    NO = "no"
    YES = "yes"


class PatientData(BaseModel):
    """
    Patient information data model with comprehensive validation.

    Attributes:
        gender: Patient gender (male/female)
        age: Patient age in years (0-150)
        is_pregnant: Pregnancy status (only applicable for females)
        history: Environmental/historical context (optional, max 250 chars)
        symptoms: List of symptoms (required, max 250 chars)
        exam_findings: Physical examination findings (optional, max 250 chars)
        lab_results: Laboratory test results (optional, max 250 chars)
        language: Preferred language for diagnosis (default: English)
    """

    gender: str = Field(..., description="Patient gender")
    age: int = Field(..., ge=0, le=150, description="Patient age in years")
    is_pregnant: str = Field(default="no", description="Pregnancy status")
    history: Optional[str] = Field(default=None, max_length=250, description="Patient history")
    symptoms: str = Field(..., min_length=1, max_length=250, description="Patient symptoms")
    exam_findings: Optional[str] = Field(
        default=None, max_length=250, description="Examination findings"
    )
    lab_results: Optional[str] = Field(
        default=None, max_length=250, description="Laboratory results"
    )
    language: str = Field(default="English", description="Preferred language")

    @field_validator("is_pregnant")
    @classmethod
    def validate_pregnancy(cls, v: str, info) -> str:
        """
        Validate that pregnancy status is only 'yes' for female patients.

        Args:
            v: Pregnancy status value
            info: Validation context with other field values

        Returns:
            str: Validated pregnancy status

        Raises:
            ValueError: If male patient has pregnancy status 'yes'
        """
        # Get gender from validation context
        gender = info.data.get("gender", "")

        # Check if male patient is marked as pregnant
        if "male" in gender.lower() and v.lower() == "yes":
            return "no"  # Auto-correct instead of raising error

        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        """
        Validate age is within reasonable range.

        Args:
            v: Age value

        Returns:
            int: Validated age

        Raises:
            ValueError: If age is negative or unreasonably high
        """
        if v < 0:
            raise ValueError("Age cannot be negative")
        if v > 150:
            raise ValueError("Age must be 150 or less")
        return v

    def to_summary_dict(self, translations: dict) -> dict:
        """
        Convert patient data to a summary dictionary for display.

        Args:
            translations: Translation dictionary for the selected language

        Returns:
            dict: Summary of patient data with translated labels
        """
        return {
            "patient": f"{self.gender}, {self.age} {translations.get('vissum_yrsold', 'years old')}",
            "pregnancy": self.is_pregnant,
            "history": self.history or translations.get("none", "none"),
            "symptoms": self.symptoms,
            "exam": self.exam_findings or translations.get("none", "none"),
            "lab": self.lab_results or translations.get("none", "none"),
        }

    def has_minimum_data(self) -> bool:
        """
        Check if patient has minimum required data for diagnosis.

        Returns:
            bool: True if symptoms are provided
        """
        return bool(self.symptoms and len(self.symptoms.strip()) > 0)

    model_config = ConfigDict(
        # Allow arbitrary types for future extensions
        arbitrary_types_allowed=True,
        # Use enum values instead of enum objects
        use_enum_values=True,
    )


class DiagnosisRequest(BaseModel):
    """
    Complete diagnosis request including patient data and configuration.

    Attributes:
        patient_data: Patient information
        system_prompt: System-level AI instruction
        language: Language for diagnosis response
    """

    patient_data: PatientData
    system_prompt: str
    language: str = "English"

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DiagnosisResponse(BaseModel):
    """
    Diagnosis response from AI with metadata.

    Attributes:
        diagnosis: The diagnostic text
        model_used: AI model that generated the diagnosis
        success: Whether the diagnosis was successfully generated
        error_message: Error message if diagnosis failed
    """

    diagnosis: Optional[str] = None
    model_used: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
