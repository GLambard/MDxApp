# MDxApp Source Code

This directory contains the refactored, modular source code for MDxApp.

## Directory Structure

```
src/
├── __init__.py              # Package initialization
├── config/                  # Configuration management
│   ├── __init__.py
│   └── settings.py         # Centralized settings using Streamlit secrets
├── core/                    # Core business logic
│   ├── __init__.py
│   ├── ai_client.py        # OpenAI API client (modern v1.x SDK)
│   └── prompt_builder.py   # Prompt construction from patient data
├── models/                  # Data models
│   ├── __init__.py
│   └── patient.py          # Patient data models with Pydantic validation
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── i18n.py             # Internationalization helpers
│   └── logger.py           # Logging configuration
└── components/              # Reusable UI components (future)
    └── __init__.py
```

## Module Overview

### `config/`
**Purpose:** Centralized configuration management

- `settings.py`: Manages all application settings loaded from Streamlit secrets
  - OpenAI API configuration
  - Application metadata
  - Feature flags for gradual migration
  - Prompt templates

**Usage:**
```python
from src.config import get_settings

settings = get_settings()
api_key = settings.openai_api_key
```

### `core/`
**Purpose:** Core business logic for medical diagnosis

- `ai_client.py`: Wrapper for OpenAI API interactions
  - `DiagnosisAIClient`: Modern client using OpenAI SDK v1.x+
  - `LegacyAIClient`: Backward-compatible client using SDK v0.27.0
  - Comprehensive error handling
  - Logging and metadata support

- `prompt_builder.py`: Constructs AI prompts from patient data
  - Template-based prompt generation
  - Multi-language support
  - HTML summary generation for UI
  - Validation of prompt configuration

**Usage:**
```python
from src.core.ai_client import DiagnosisAIClient
from src.core.prompt_builder import PromptBuilder

# Create AI client
client = DiagnosisAIClient(api_key="...", model="gpt-4o-mini")

# Build prompt
builder = PromptBuilder(prompt_words, translations)
user_prompt = builder.build_user_prompt(patient_data, language="English")

# Get diagnosis
diagnosis = client.get_diagnosis(system_prompt, user_prompt)
```

### `models/`
**Purpose:** Data models with validation

- `patient.py`: Patient data models using Pydantic
  - `PatientData`: Patient information with validation
  - `DiagnosisRequest`: Complete diagnosis request
  - `DiagnosisResponse`: Diagnosis response with metadata
  - Automatic validation (age range, pregnancy logic, etc.)

**Usage:**
```python
from src.models.patient import PatientData

patient = PatientData(
    gender="Female",
    age=35,
    symptoms="Headache, fever",
    history="Recent travel"
)

# Automatic validation
assert patient.age >= 0 and patient.age <= 150
```

### `utils/`
**Purpose:** Utility functions and helpers

- `i18n.py`: Internationalization management
  - Load translations from JSON
  - Get translations with fallback support
  - Language availability checks
  - Runtime translation addition

- `logger.py`: Logging configuration
  - Structured logging setup
  - Console and file handlers
  - JSON and text formatting options

**Usage:**
```python
from src.utils.i18n import I18n
from src.utils.logger import get_logger

# Internationalization
i18n = I18n(Path("Assets/translations.json"))
text = i18n.get("English", "greeting")

# Logging
logger = get_logger(__name__)
logger.info("Processing diagnosis request")
```

### `components/` (Future)
**Purpose:** Reusable Streamlit UI components

Planned components:
- Donation button
- Language selector
- Patient form
- Diagnosis display

## Design Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- `config`: Settings and configuration
- `core`: Business logic
- `models`: Data structures and validation
- `utils`: Cross-cutting utilities
- `components`: UI components

### 2. Type Safety
- All functions have type hints
- Pydantic models for data validation
- Mypy-compatible type checking

### 3. Testability
- Pure functions where possible
- Dependency injection for testability
- Comprehensive test coverage

### 4. Logging
- All major operations are logged
- Different log levels for different scenarios
- Structured logging for better debugging

### 5. Error Handling
- Graceful error handling with user-friendly messages
- Never expose internal errors to users
- Comprehensive exception catching

### 6. Documentation
- Clear docstrings for all public functions
- Type hints for better IDE support
- README files in each major directory

## Migration Strategy

The new modules can be used alongside the existing code:

1. **Feature Flag Approach**: Use `settings.use_new_ai_client` flag
2. **Gradual Migration**: Replace one component at a time
3. **Backward Compatibility**: Legacy client available for fallback
4. **Testing**: Extensive tests before full migration

## Example: Full Integration

```python
from pathlib import Path
from src.config import get_settings
from src.core.ai_client import DiagnosisAIClient
from src.core.prompt_builder import PromptBuilder
from src.models.patient import PatientData
from src.utils.i18n import I18n

# Load configuration
settings = get_settings()

# Load translations
i18n = I18n(Path("Assets/translations.json"))
translations = i18n.translations

# Create patient data
patient = PatientData(
    gender="Female",
    age=35,
    symptoms="Headache, fever",
    history="Recent travel"
)

# Build prompt
builder = PromptBuilder(settings.prompt_words, translations)
system_prompt = settings.prompt_system
user_prompt = builder.build_user_prompt(patient, language="English")

# Get diagnosis
client = DiagnosisAIClient(
    api_key=settings.openai_api_key,
    model=settings.openai_model,
    temperature=settings.openai_temperature,
    max_tokens=settings.openai_max_tokens
)

diagnosis = client.get_diagnosis(system_prompt, user_prompt)
```

## Testing

Run tests for the new modules:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_patient_model.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run only unit tests
pytest -m unit
```

## Future Enhancements

- [ ] Async support for OpenAI API calls
- [ ] Caching layer for repeated requests
- [ ] Rate limiting and retry logic
- [ ] Advanced error recovery
- [ ] Performance monitoring
- [ ] A/B testing framework

