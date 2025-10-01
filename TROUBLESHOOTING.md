# MDxApp Troubleshooting Guide

**Version:** 2.0.0  
**Date:** October 1, 2025

---

## 🚨 Common Issues and Solutions

### Issue 1: "The server does not respond or is overloaded..." Error

**Symptoms:**
- Submit button shows spinner
- After waiting, shows error message
- No diagnosis displayed

**Common Causes & Solutions:**

#### **Cause A: Missing or Invalid API Key**

**Check:**
```bash
# Verify secrets file exists
ls -la .streamlit/secrets.toml
```

**Solution:**
Create or update `.streamlit/secrets.toml`:
```toml
openai_api_key = "sk-proj-YOUR_ACTUAL_KEY_HERE"
openai_api_model = "gpt-5-mini"

[prompt_canvas]
prompt_system = "You are a medical AI assistant..."
prompt_words = ["Patient: ", "Pregnant: ", "History: ", "Symptoms: ", "Exam: ", "Lab: ", "Provide diagnosis. ", "Include differentials. ", "Be specific. ", "Respond in "]
```

#### **Cause B: Wrong OpenAI SDK Version**

**Check:**
```bash
python -c "import openai; print(openai.__version__)"
```

**Solution:**
```bash
# If version is 0.27.0 and using GPT-5 Mini, upgrade:
pip install --upgrade openai

# Expected version: >=1.50.0
```

#### **Cause C: Model Name Mismatch**

**Check:** secrets.toml has correct model name

**Solution:**
```toml
# Change this:
openai_api_model = "gpt-3.5-turbo"  # ❌ Old

# To this:
openai_api_model = "gpt-5-mini"  # ✅ Correct
```

#### **Cause D: Feature Flag Mismatch**

**Problem:** Using modern model with legacy SDK

**Solution 1 - Enable New Client:**
```toml
# Add to secrets.toml
use_new_ai_client = true  # Required for GPT-5 Mini
```

**Solution 2 - Use Legacy Model Temporarily:**
```toml
# Revert to old model while testing
openai_api_model = "gpt-3.5-turbo"
use_new_ai_client = false
```

#### **Cause E: Invalid Prompt Configuration**

**Check:** Ensure `prompt_canvas` is configured

**Solution:**
```toml
[prompt_canvas]
prompt_system = "You are an experienced medical professional assistant. Provide diagnostic suggestions based on patient information. Be specific, evidence-based, and prioritize patient safety."

prompt_words = [
    "Patient: ",
    "Pregnant: ",
    "History: ",
    "Symptoms: ",
    "Examination: ",
    "Lab results: ",
    "Provide a medical diagnosis based on this information. ",
    "Include differential diagnoses. ",
    "Recommend next steps. ",
    "Respond in "
]
```

---

### Issue 2: Import Errors

**Error:** `ModuleNotFoundError: No module named 'src'`

**Solutions:**

1. **Verify you're in project root:**
   ```bash
   pwd
   # Should show: .../MDxApp
   ```

2. **Check src/ directory exists:**
   ```bash
   ls -la src/
   ```

3. **Ensure __init__.py files exist:**
   ```bash
   find src/ -name "__init__.py"
   ```

4. **Install missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

### Issue 3: CSS Not Loading

**Symptoms:**
- Page loads but styling is wrong
- Fonts are default size
- Layout looks broken

**Solutions:**

1. **Check CSS files exist:**
   ```bash
   ls -la MDxApp/pages/styles/
   # Should show: main.css, email_form.css
   ```

2. **Verify paths are correct:**
   ```python
   # In the app code, check:
   load_main_styles(project_root)
   # project_root should point to MDxApp root
   ```

3. **Clear Streamlit cache:**
   ```bash
   streamlit cache clear
   ```

4. **Clear browser cache:**
   - Chrome: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   - Firefox: Cmd+Shift+Delete (Mac) or Ctrl+Shift+Delete (Windows)

---

### Issue 4: Component Not Rendering

**Symptoms:**
- Donation buttons missing
- Language selector not showing
- QR code not displayed

**Solutions:**

1. **Check QR code image exists:**
   ```bash
   ls -la Materials/bmc_qr.png
   ```

2. **Verify translations loaded:**
   ```python
   # Check in code:
   print(len(transl))  # Should be 5 (languages)
   ```

3. **Check component imports:**
   ```python
   from src.components.donation import render_sidebar_donation
   # Should not error
   ```

---

### Issue 5: Pydantic Validation Errors

**Error:** `ValidationError: 1 validation error for PatientData`

**Solutions:**

1. **Check required fields:**
   - `gender`: Required
   - `age`: Required (0-150)
   - `symptoms`: Required (min 1 char)

2. **Verify data types:**
   ```python
   # Age must be int
   age = int(st.session_state.age)
   ```

3. **Check for None values:**
   ```python
   # Convert None to empty string
   history = patient_data.history or ""
   ```

---

### Issue 6: Type Checking Errors

**Error:** Mypy reports type errors

**Solutions:**

1. **Update Python version:**
   ```bash
   python --version
   # Should be 3.9+ (configured for 3.10)
   ```

2. **Install type stubs:**
   ```bash
   pip install types-requests
   ```

3. **Run type check:**
   ```bash
   mypy src/
   ```

---

## 🔧 Configuration Checklist

### Required Files

- [ ] `.streamlit/secrets.toml` exists
- [ ] `Assets/translations.json` exists
- [ ] `Materials/bmc_qr.png` exists
- [ ] `MDxApp/pages/styles/main.css` exists
- [ ] All `src/` modules exist

### Required Secrets

```toml
# Minimum required configuration
openai_api_key = "sk-..."
openai_api_model = "gpt-5-mini"

[prompt_canvas]
prompt_system = "..."
prompt_words = ["...", ...]
```

### Optional Secrets (Recommended)

```toml
use_new_ai_client = true
use_structured_outputs = true
use_gpt5_mini_prompts = true
openai_api_temp = 0.7
openai_api_maxtok = 2000
openai_api_freqp = 0
openai_api_presp = 0
email_address = "your@email.com"
```

---

## 🧪 Testing Steps

### 1. Test Basic Imports

```python
# test_imports.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

try:
    from src.config import get_settings
    print("✅ Config import OK")
    
    from src.core import DiagnosisAIClient
    print("✅ Core import OK")
    
    from src.components.donation import render_sidebar_donation
    print("✅ Components import OK")
    
    print("\n✅ All imports successful!")
except Exception as e:
    print(f"❌ Import error: {e}")
```

### 2. Test Settings Loading

```python
# test_settings.py
from src.config import get_settings

try:
    settings = get_settings()
    print(f"✅ API Key: {settings.openai_api_key[:10]}...")
    print(f"✅ Model: {settings.openai_model}")
    print(f"✅ Temperature: {settings.openai_temperature}")
    print("\n✅ Settings loaded successfully!")
except Exception as e:
    print(f"❌ Settings error: {e}")
```

### 3. Test OpenAI Connection

```python
# test_openai.py
from openai import OpenAI

client = OpenAI(api_key="your-key")

try:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10
    )
    print(f"✅ OpenAI connection OK")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI error: {e}")
```

---

## 📝 Quick Fixes

### Fix 1: Reset Everything

```bash
# Clear all caches
streamlit cache clear

# Restart Streamlit
# Ctrl+C to stop, then:
streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py
```

### Fix 2: Use Legacy Mode

```toml
# .streamlit/secrets.toml
use_new_ai_client = false
openai_api_model = "gpt-3.5-turbo"
```

### Fix 3: Check Logs

```bash
# Run with logging
python -m streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py --logger.level=debug
```

### Fix 4: Verify Dependencies

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 🆘 Still Having Issues?

### Debug Mode

Add this to your app for debugging:

```python
# At top of 01_🏥_Diagnosis_Assistant.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Before openai_create call
st.write(f"Debug: Using model: {st.secrets.get('openai_api_model')}")
st.write(f"Debug: New client: {use_new_client}")
st.write(f"Debug: Prompt length: {len(question_prompt)}")
```

### Check API Status

1. Visit: https://status.openai.com/
2. Verify OpenAI API is operational
3. Check if you have API credits

### Verify API Key

```bash
# Test API key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 📞 Support Checklist

When reporting issues, include:

- [ ] Error message (exact text)
- [ ] OpenAI SDK version (`pip show openai`)
- [ ] Python version (`python --version`)
- [ ] Streamlit version (`pip show streamlit`)
- [ ] Feature flags in secrets
- [ ] Model name in secrets
- [ ] Whether API key is valid
- [ ] Recent code changes

---

## ✅ Quick Health Check

Run this to verify everything:

```bash
# 1. Check dependencies
pip list | grep -E "(openai|streamlit|pydantic)"

# 2. Check files exist
ls -la .streamlit/secrets.toml
ls -la src/core/ai_client.py
ls -la MDxApp/pages/styles/main.css

# 3. Run tests
pytest -q

# 4. Check secrets (without exposing key)
python -c "import streamlit as st; print('Keys:', list(st.secrets.keys()))"
```

---

**Most Common Fix:**

```toml
# .streamlit/secrets.toml
openai_api_key = "sk-proj-YOUR_REAL_KEY"
openai_api_model = "gpt-5-mini"
use_new_ai_client = true

[prompt_canvas]
prompt_system = "You are a medical AI assistant."
prompt_words = ["Patient: ", "Pregnant: ", "History: ", "Symptoms: ", "Exam: ", "Lab: ", "Diagnose. ", "Differentials. ", "Specific. ", "Language: "]
```

Then restart: `streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py`

