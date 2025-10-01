# Quick Setup Guide for GPT-5 Mini

**Goal:** Get MDxApp working with GPT-5 Mini in 5 minutes

---

## ⚡ Quick Start

### Step 1: Create Secrets File

Create `.streamlit/secrets.toml` (if it doesn't exist):

```bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
# OpenAI Configuration
openai_api_key = "sk-proj-YOUR_OPENAI_API_KEY_HERE"
openai_api_model = "gpt-5-mini"
openai_api_temp = 0.7
openai_api_maxtok = 2000
openai_api_freqp = 0
openai_api_presp = 0

# Feature Flags
use_new_ai_client = true

# Email Configuration
email_address = "your@email.com"

# Prompt Configuration
[prompt_canvas]
prompt_system = "You are an experienced medical professional assistant. Provide diagnostic suggestions based on patient information. Be specific, evidence-based, and prioritize patient safety."

prompt_words = [
    "Patient: ",
    "Pregnant: ",
    "History: ",
    "Symptoms: ",
    "Examination findings: ",
    "Laboratory results: ",
    "Provide a comprehensive medical diagnosis. ",
    "Include differential diagnoses. ",
    "Recommend specific next steps. ",
    "Respond in "
]
EOF
```

### Step 2: Update Your API Key

Edit `.streamlit/secrets.toml` and replace `YOUR_OPENAI_API_KEY_HERE` with your actual OpenAI API key.

**Get API key:** https://platform.openai.com/api-keys

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the App

```bash
streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py
```

---

## ✅ Verify It Works

1. App opens in browser
2. Select language (default: English)
3. Fill in patient information:
   - Gender: Male
   - Age: 35
   - Symptoms: "fever, cough, headache"
4. Click **SUBMIT**
5. Should see diagnosis appear

**Success:** Diagnosis displayed ✅  
**Failure:** See troubleshooting below

---

## 🔧 Quick Troubleshooting

### Error: "Server does not respond..."

**Most Common Fix:**
```toml
# In .streamlit/secrets.toml
use_new_ai_client = true  # ← Add this line!
```

Then restart Streamlit.

### Error: "ModuleNotFoundError: No module named 'src'"

**Fix:**
```bash
# Make sure you're in project root
cd /path/to/MDxApp
streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py
```

### Error: "Authentication Error"

**Fix:**
Check your API key is valid:
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 🎯 Configuration Options

### Minimal Configuration (Works immediately)

```toml
openai_api_key = "sk-..."
openai_api_model = "gpt-5-mini"
use_new_ai_client = true

[prompt_canvas]
prompt_system = "You are a medical AI assistant."
prompt_words = ["Patient: ", "Pregnant: ", "History: ", "Symptoms: ", "Exam: ", "Lab: ", "Diagnose. ", "List alternatives. ", "Recommend tests. ", "Language: "]
```

### Recommended Configuration (Best results)

```toml
openai_api_key = "sk-..."
openai_api_model = "gpt-5-mini"
openai_api_temp = 0.7
openai_api_maxtok = 2000
use_new_ai_client = true
use_structured_outputs = false  # Start false, enable later
use_gpt5_mini_prompts = false   # Start false, enable later

[prompt_canvas]
prompt_system = "You are an experienced medical professional assistant. Provide diagnostic suggestions based on patient information. Be specific, evidence-based, and prioritize patient safety."
prompt_words = ["Patient: ", "Pregnant: ", "History: ", "Symptoms: ", "Examination: ", "Lab: ", "Diagnose comprehensively. ", "Include differentials. ", "Recommend next steps. ", "Respond in "]
```

### Advanced Configuration (All features)

```toml
openai_api_key = "sk-..."
openai_api_model = "gpt-5-mini"
openai_api_temp = 0.7
openai_api_maxtok = 2000
openai_api_freqp = 0
openai_api_presp = 0

use_new_ai_client = true
use_structured_outputs = true  # ← Structured JSON
use_gpt5_mini_prompts = true   # ← Enhanced prompts
enable_logging = true

email_address = "your@email.com"

[prompt_canvas]
prompt_system = "You are an experienced medical professional assistant."
prompt_words = ["...", ...]
```

---

## 🚀 Upgrade Path

### Currently on GPT-3.5-Turbo?

**Step 1:** Just change model name
```toml
openai_api_model = "gpt-5-mini"  # Change this
use_new_ai_client = true          # Add this
```

**Step 2:** Test thoroughly

**Step 3:** Enable advanced features
```toml
use_gpt5_mini_prompts = true
use_structured_outputs = true
```

---

## 💡 Pro Tips

1. **Start Simple**
   - Use minimal config first
   - Test basic functionality
   - Then enable advanced features

2. **Monitor Costs**
   - Check OpenAI dashboard
   - GPT-5 Mini: $0.175/1M input, $1.5/1M output
   - Set usage limits if needed

3. **Use Feature Flags**
   - Enable one feature at a time
   - Test after each change
   - Easy to rollback

4. **Keep Backup**
   - Backup working secrets.toml
   - Can quickly revert if needed

---

## 🎯 Success Checklist

- [ ] .streamlit/secrets.toml created
- [ ] OpenAI API key added (starts with sk-)
- [ ] Model set to "gpt-5-mini"
- [ ] use_new_ai_client = true
- [ ] prompt_canvas configured
- [ ] Dependencies installed
- [ ] App runs without errors
- [ ] Can submit and get diagnosis
- [ ] All languages work
- [ ] Donation buttons visible

---

## 📞 Need Help?

1. **Check:** `TROUBLESHOOTING.md` for detailed solutions
2. **Review:** `notes/GPT5_MINI_UPGRADE.md` for full guide
3. **Read:** Error messages carefully (they usually tell you what's wrong)
4. **Test:** Each component separately

---

**Quick Fix for Most Issues:**

```bash
# 1. Stop Streamlit (Ctrl+C)
# 2. Clear cache
streamlit cache clear
# 3. Verify secrets
cat .streamlit/secrets.toml | grep "openai_api"
# 4. Restart
streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py
```

**That usually fixes it!** ✅

