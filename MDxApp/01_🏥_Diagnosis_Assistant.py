import streamlit as st 
from streamlit.components.v1 import html
from streamlit_extras.buy_me_a_coffee import button

import os

import openai

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v 
##

#OpenAI API key as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["openai_api_key"]

def openai_create(prompt):

    response = openai.ChatCompletion.create(
    model=st.secrets["openai_api_model"],
    messages=[{"role": "system", "content": st.secrets["prompt_canvas"]["prompt_system"]}, 
              {"role": "user", "content": prompt}], 
    temperature=float(st.secrets["openai_api_temp"]), 
    max_tokens=int(st.secrets["openai_api_maxtok"]),
    frequency_penalty=int(st.secrets["openai_api_freqp"]),
    presence_penalty=float(st.secrets["openai_api_presp"]), 
    stop = None
    )

    return response['choices'][0]['message']['content']

st.set_page_config(
    page_title="Diagnosis_Assistant",
    page_icon="🏥",
    layout="wide"
)

# Font size and weight for the sidebar
# Works with streamlit==1.17.0
# TODO: Review class names for future versions
st.markdown("""
  <style>
      ul[class="css-j7qwjs e1fqkh3o7"]{
        position: relative;
        padding-top: 2rem;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
      }
      .css-17lntkn {
        font-weight: bold;
        font-size: 18px;
        color: grey;
      }
      .css-pkbazv {
        font-weight: bold;
        font-size: 18px;
      }
  </style>""", unsafe_allow_html=True)

path = os.path.dirname(__file__)

# Buy me a coffee - MDxApp support
button = f"""<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="geonosislaX" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>"""
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: black;'>Let's keep MDxApp free!</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left; color: black;'>By clicking here:</h4>", unsafe_allow_html=True)
    html(button, height=70, width=220)
    st.markdown("<h4 style='text-align: left; color: black;'>Or use this QR code:</h4>", unsafe_allow_html=True)
    qr_name = path+"/../Materials/bmc_qr.png"
    st.image(qr_name, caption= '', width = 220)

# Use GitHub logo file
logo_name = path+"/../Materials/MDxApp_logo_v2_256.png"

# Define columns
t1, t2 = st.columns([1,3], gap="large")
with t1: 
    st.image(logo_name, caption= '', width=256)
with t2:
    st.header("**Medical Diagnosis Assistant**")
    st.write("<p style=\"font-weight: bold; font-size:18px;\">Experience the future of healthcare with our ChatGPT-powered <br>medical diagnostic and symptom checking tool.</p>", 
                 unsafe_allow_html=True)    

st.markdown("", unsafe_allow_html=True)
"""
---
"""
st.write("<p style=\"font-weight: bold; font-size:18px;\">How to use this app:</p>"+ \
         "<p style=\"font-size:18px;\">1. Fill out the report below (some symptoms are at least required)<br/>"+ \
         "2. Check the summary of the report<br/>"+ \
         "3. Submit the report (None of the provided data are saved or shared)</p>", 
         unsafe_allow_html=True)

st.write(
    """<style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

## Font size configs
st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)
st.markdown(
    """<style>
div[class*="stNumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)
st.markdown(
    """<style>
div[class*="stTextInput"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)
####

st.subheader(":black_nib: **Report**")
# Define columns
col1, col2, col3 = st.columns(3, gap="large")

# Store initial values in session state
if "disabled" not in st.session_state:
    st.session_state.disabled = False
# Declare lists
genders_list = ["Male", "Female"]
pregnant_list = ["No", "Yes"]
##

# Gender selector 
with col1:
    st.radio("**Gender**", genders_list, key='gender')
# Age selector 
with col2:
    st.number_input("**Age**", min_value= 0, max_value= 99, step=1, key="age")
# Pregnancy
if st.session_state.gender == 'Male':
    st.session_state.disabled = True
    if "pregnant" in st.session_state:
        st.session_state.pregnant = "No"
else: 
    st.session_state.disabled = False

with col3: 
    st.radio("**Pregnant**", pregnant_list, disabled=st.session_state.disabled, key="pregnant")

# Context
st.text_input('**History** *(Example: gone to an outdoor music festival, shared drinks and cigarettes with friends with similar symptoms)*', 
             placeholder="none", key="context", max_chars=100, 
             help=":green[**Enter patient's known background information, including their past medical conditions, medications, " + \
                  "family history, lifestyle, and other relevant information that can help in diagnosis and treatment**]")

# List of symptoms
st.text_input("**Symptoms** *(Example: high-grade fever, lethargy, headache, and abdominal pain for two days)*", 
             placeholder="none", key="symptoms", max_chars=100, 
             help=":green[**List all symptoms indicating the presence of an underlying medical condition**]")

# List of observations at exam
st.text_input("**Examination findings** *(Example: petechial lesions on the palms of his hands and feet, bug bites)*", 
             placeholder="none", key="exam", max_chars=100, 
             help=":green[**List all the information gathered through visual inspection, palpation, " + \
                  "percussion, and auscultation during the examination**]")

# Laboratory test results
st.text_input("**Laboratory test results** *(Example: w/IgE levels > 3000 IU/m)*", 
             placeholder="none", key="labresults", max_chars=100, 
             help=":green[**List output of tests performed on samples of bodily fluids, tissues, " + \
                  "or other substances to help diagnose, monitor, or treat medical conditions. " + \
                  "These tests can include blood tests, urine tests, imaging tests, biopsies, " + \
                  "and other diagnostic procedures**]")

st.subheader(":clipboard: **Summary**")
# Diagnostic

report_list = [st.session_state.context, st.session_state.symptoms, 
               st.session_state.exam, st.session_state.labresults]
corr_list = ["none", "none", "none", "none"]
for ic in range(0,len(report_list)):
    if report_list[ic] == "":
        report_list[ic] = corr_list[ic]

vis_summary = "<p style=\"font-size:18px;\">" + \
              "<b>Patient: </b>" + st.session_state.gender + ", " + str(st.session_state.age) + " years old.<br/>" + \
              "<b>Pregnancy: </b>" + st.session_state.pregnant + ".<br/>" + \
              "<b>History: </b>" + report_list[0] + ".<br/>" + \
              "<b>Symptoms: </b>" + report_list[1] + ".<br/>" + \
              "<b>Examination findings: </b>" + report_list[2] + ".<br/>" + \
              "<b>Laboratory test results: </b>" + report_list[3] + ".<br/> </p>"

st.write(vis_summary, unsafe_allow_html=True) 

prompt_words = st.secrets["prompt_canvas"]["prompt_words"]
question_prompt = prompt_words[0] + st.session_state.gender + ", " + str(st.session_state.age) + " years old. " + \
                  prompt_words[1] + st.session_state.pregnant + ". " + \
                  prompt_words[2] + report_list[0] + ". " + \
                  prompt_words[3] + report_list[1] + ". " + \
                  prompt_words[4] + report_list[2] + ". " + \
                  prompt_words[5] + report_list[3] + ". " + \
                  prompt_words[6] + \
                  prompt_words[7] + \
                  prompt_words[8] 

st.write('')
submit_button = st.button('**SUBMIT**', help=":green[**Submit the report for diagnostic**]")
st.write('')

st.subheader(":computer: :speech_balloon: :pill: **Diagnostic**")
if submit_button:
    if report_list[1] == "none":
        st.write("<p style=\"font-weight: bold; font-size:18px;\">Please, enter at least some symptoms before submission.</p>", 
                 unsafe_allow_html=True)
    else:
        with st.spinner('Please wait...'):
            try:
                st.session_state.diagnostic = openai_create(prompt=question_prompt)
                st.write('')
                st.write(st.session_state.diagnostic.replace("<|im_end|>", ""), unsafe_allow_html=True)
            except: 
                st.write("<p style=\"font-weight: bold; font-size:18px;\">The server does not respond or is overloaded with requests... Try again.</p>", 
                         unsafe_allow_html=True)
else: 
    if "diagnostic" in st.session_state:
        st.write(st.session_state.diagnostic.replace("<|im_end|>", ""), unsafe_allow_html=True)
    else: 
        st.write("<p style=\"font-weight: bold; font-size:18px;\">No diagnostic yet. Please fill out the report and click SUBMIT above.</p>", 
                 unsafe_allow_html=True)