[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medicaldiagnosticassistant.streamlit.app)

# :tv: Welcome to the MDxApp page :hospital:

Here, we want to make the access to a large knowledge in 
medical diagnosis available to an as broad as possible community of 
medical professionals and individuals seeking access to a fast medical diagnosis tool.  

For this, we have developed the **MDxApp** that's using **GPT-5.4-nano** 
(OpenAI's GPT-5 family model with structured outputs and a large context window) to assist you in proposing 
a quick diagnostic according to a patient's demographics, a recent environmental context, 
a list of symptoms, recent and relevant observations on the patient's state, and any existing 
chronic condition(s) followed by indications on any existing treatment(s).

**Current (v2.5.1):** GPT-5.4-nano, structured diagnosis, PDF export, 15 languages, educational references, and medication safety notes.

## Configuration

1. Copy [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) to `.streamlit/secrets.toml`.
2. Set your `openai_api_key` and `openai_api_model` (default: `gpt-5.4-nano`).
3. Enable feature flags (defaults in the example):
   - `use_new_ai_client = true`
   - `use_structured_outputs = true`
   - `use_gpt5_mini_prompts = true`

**Streamlit Cloud:** paste the same keys in your app **Settings → Secrets** (see the example file for the full template).

Run locally:

```bash
pip install -r requirements.txt
streamlit run "MDxApp/01_🏥_Diagnosis_Assistant.py"
```

Patient's demographics, context, symptoms, observations, chronic conditions added to any relevant information 
can all be entered in plain text in the app. The medical jargon with known abbreviations is fully supported. 
More information on a patient may help to propose a more precise medical diagnostic. 

The use of the app is straightforward with examples shown to the user for guidance. 

The time response of the app may vary with the traffic of requests, the speed of your internet connection, and 
finally the disponibility of the OpenAI API. If this happens, try again later. 

For any requests, comments, questions on the app, please use the email form accessible from the contact page in the 
app, or post them right here in the issues. 

And last, but not the least, we would appreciate that, if you find this app useful, you share it around you by any 
channel you may prefer. 

Finally, support the further developments and maintenances of this app by buying me a coffee. This app uses 
the ChatGPT AI model through the official API of OpenAI which has a cost. Also, this app is free to use and will remain 
free to use for all if you support it by buying me a coffee (see the dedicated button below). 

Thank you very much in advance for making it possible !

## Support the app

If you find this app useful, consider supporting it by making a donation.

<a href="https://www.buymeacoffee.com/geonosislaX"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=geonosislaX&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

Thank you for supporting the development and maintenance of this app!
