"""PatientData validation and minimum-data checks."""

from src.components.patient_form import format_patient_validation_error
from src.models.patient import PatientData
from pydantic import ValidationError


def test_empty_symptoms_allowed_while_editing() -> None:
    patient = PatientData(gender="male", age=30, symptoms="")
    assert not patient.has_minimum_data()


def test_symptoms_required_for_minimum_data() -> None:
    patient = PatientData(gender="female", age=25, symptoms="  fever  ")
    assert patient.has_minimum_data()


def test_format_validation_error_symptoms_friendly() -> None:
    trans = {"submit_warning": "Add symptoms first."}
    err = ValidationError.from_exception_data(
        "PatientData",
        [
            {
                "type": "string_too_short",
                "loc": ("symptoms",),
                "msg": "too short",
                "input": "",
                "ctx": {"min_length": 1},
            }
        ],
    )
    assert format_patient_validation_error(trans, err) == "Add symptoms first."
