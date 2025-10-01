"""
Unit tests for patient data models.
Tests validation logic and data handling.
"""

import pytest
from src.models.patient import PatientData, DiagnosisRequest, DiagnosisResponse


class TestPatientData:
    """Test cases for PatientData model."""
    
    def test_valid_patient_data(self):
        """Test creating a valid patient data instance."""
        patient = PatientData(
            gender="Female",
            age=35,
            is_pregnant="no",
            symptoms="Headache, fever",
            history="Recent travel",
            exam_findings="Temperature 38.5°C",
            lab_results="WBC elevated"
        )
        
        assert patient.gender == "Female"
        assert patient.age == 35
        assert patient.symptoms == "Headache, fever"
    
    def test_pregnancy_auto_correction_for_males(self):
        """Test that male patients cannot be marked as pregnant."""
        patient = PatientData(
            gender="Male",
            age=30,
            is_pregnant="yes",  # Should be auto-corrected to "no"
            symptoms="Cough"
        )
        
        assert patient.is_pregnant == "no"
    
    def test_minimum_required_fields(self):
        """Test that only gender, age, and symptoms are required."""
        patient = PatientData(
            gender="Female",
            age=25,
            symptoms="Nausea"
        )
        
        assert patient.gender == "Female"
        assert patient.age == 25
        assert patient.symptoms == "Nausea"
        assert patient.history is None
        assert patient.exam_findings is None
        assert patient.lab_results is None
    
    def test_age_validation(self):
        """Test age validation constraints."""
        with pytest.raises(ValueError):
            PatientData(
                gender="Male",
                age=-5,  # Negative age should fail
                symptoms="Fever"
            )
        
        with pytest.raises(ValueError):
            PatientData(
                gender="Male",
                age=200,  # Age > 150 should fail
                symptoms="Fever"
            )
    
    def test_symptoms_required(self):
        """Test that symptoms field is required."""
        with pytest.raises(ValueError):
            PatientData(
                gender="Female",
                age=30
                # Missing symptoms
            )
    
    def test_has_minimum_data(self):
        """Test has_minimum_data method."""
        patient_with_symptoms = PatientData(
            gender="Male",
            age=40,
            symptoms="Chest pain"
        )
        assert patient_with_symptoms.has_minimum_data() is True
        
        # Empty symptoms will fail validation, so test with minimal symptoms
        patient_minimal_symptoms = PatientData(
            gender="Male",
            age=40,
            symptoms=" "  # Single space - will pass validation but fail has_minimum_data
        )
        assert patient_minimal_symptoms.has_minimum_data() is False
    
    def test_to_summary_dict(self):
        """Test conversion to summary dictionary."""
        patient = PatientData(
            gender="Female",
            age=28,
            symptoms="Fatigue",
            history="Athlete"
        )
        
        translations = {
            "vissum_yrsold": " years old",
            "none": "none"
        }
        
        summary = patient.to_summary_dict(translations)
        
        assert "patient" in summary
        # Check for age in patient string (may have extra spaces)
        assert "28" in summary["patient"]
        assert "years old" in summary["patient"]
        assert summary["symptoms"] == "Fatigue"


class TestDiagnosisResponse:
    """Test cases for DiagnosisResponse model."""
    
    def test_successful_diagnosis(self):
        """Test creating a successful diagnosis response."""
        response = DiagnosisResponse(
            diagnosis="Possible viral infection",
            model_used="gpt-4o-mini",
            success=True
        )
        
        assert response.success is True
        assert response.diagnosis == "Possible viral infection"
        assert response.error_message is None
    
    def test_failed_diagnosis(self):
        """Test creating a failed diagnosis response."""
        response = DiagnosisResponse(
            diagnosis=None,
            success=False,
            error_message="API error"
        )
        
        assert response.success is False
        assert response.diagnosis is None
        assert response.error_message == "API error"

