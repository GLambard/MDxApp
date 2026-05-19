"""Tests for PatientData validation."""

import pytest
from pydantic import ValidationError

from src.models.patient import PatientData


def test_valid_patient(sample_patient: PatientData) -> None:
    assert sample_patient.has_minimum_data()
    assert sample_patient.age == 35


def test_male_pregnancy_auto_corrected() -> None:
    patient = PatientData(
        gender="Male",
        age=30,
        is_pregnant="yes",
        symptoms="cough",
    )
    assert patient.is_pregnant == "no"


def test_symptoms_required() -> None:
    with pytest.raises(ValidationError):
        PatientData(gender="Female", age=25, symptoms="")


def test_age_bounds() -> None:
    with pytest.raises(ValidationError):
        PatientData(gender="Male", age=-1, symptoms="pain")
    with pytest.raises(ValidationError):
        PatientData(gender="Male", age=200, symptoms="pain")


def test_field_max_length() -> None:
    long_text = "x" * 2001
    with pytest.raises(ValidationError):
        PatientData(gender="Male", age=20, symptoms=long_text)
