#import ptvsd
#ptvsd.enable_attach(address=('localhost', 8501))
#ptvsd.wait_for_attach() # Only include this line if you always want to attach the debugger

# Write a streamlit web app. The main title is "Diagnostic Assistant". It contains a gender selector, an age selector from 0 to 99+ years old.
import streamlit as st 

# From https://github.com/blackary/st_pages
# Pages config in .streamlit/pages.toml
#from st_pages import show_pages_from_config
#show_pages_from_config()

import os
import openai

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v 
##

# Quick FIX for SSL certificate localization
# Remove if out of DMZ
os.environ["REQUESTS_CA_BUNDLE"] = '/usr/local/share/ca-certificates/extras/nims_proxy_copy.pem'
os.environ["SSL_CERT_FILE"] = '/usr/local/share/ca-certificates/extras/nims_proxy_copy.pem'

#if you have OpenAI API key as an environment variable, enable the below
openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
# From https://blog.streamlit.io/secrets-in-sharing-apps/
# secrets config in .streamlit/secrets.toml
openai.api_key = st.secrets["openai_api_key"]

def openai_create(prompt):

    response = openai.Completion.create(
    model="text-davinci-002", # text-davinci-003, text-curie-001, text-chat-davinci-002-20230126, text-chat-davinci-002-20221122
    prompt=prompt,
    temperature=0., # 0.7
    max_tokens=750,
    #top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6, 
    stop = None
    )

    return response.choices[0].text

st.set_page_config(
    page_title="Diagnosis_Assistant",
    page_icon="🏥",
    layout="wide"
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
div[class*="stTextArea"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)
####

# Diagnostic Assistant 
st.title("**Medical Diagnosis Support Tool (DxST)**")

st.subheader(":black_nib: **Report**")
# Define columns
col1, col2, col3 = st.columns(3, gap="large")

# Store initial values in session state
if "disabled" not in st.session_state:
    st.session_state.disabled = False

genders_list = ["Male", "Female"]
if "gender" in st.session_state:
    gender_id = genders_list.index(st.session_state.gender)
else:
    gender_id = 0

if "age" in st.session_state:
    age_val = st.session_state.age
else:
    age_val = 0

pregnant_list = ["No", "Yes"]
pregnant_id = 0
if "pregnant" in st.session_state:
    pregnant_id = pregnant_list.index(st.session_state.pregnant)

ctx_val = ""
if "context" in st.session_state:
    ctx_val = st.session_state.context
else: 
    ctx_val = ""

if "symptoms" in st.session_state:
    symp_val = st.session_state.symptoms
else:
    symp_val = ""

if "exam" in st.session_state:
    exam_val = st.session_state.exam
else:
    exam_val = ""

if "labresults" in st.session_state:
    lab_val = st.session_state.labresults
else:
    lab_val = ""
##

# Gender selector 
with col1:
    #st.session_state.gender = 
    st.radio("**Gender**", genders_list, key='gender')#, index=gender_id)
# Age selector 
with col2:
    #st.session_state.age = 
    st.number_input("**Age**", min_value= 0, max_value= 99, step=1, value=age_val)
# Pregnancy
if st.session_state.gender == 'Male':
    st.session_state.disabled = True
    st.session_state.pregnant = "No"
else: 
    st.session_state.disabled = False

with col3: 
    st.session_state.pregnant = st.radio("**Pregnant**", pregnant_list, disabled=st.session_state.disabled , index=pregnant_id)

# Context
st.session_state.context = st.text_area('**History** *(Example: gone to an outdoor music festival, shared drinks and cigarettes with friends with similar symptoms)*', 
              value=ctx_val, placeholder="none", 
              help=":green[**Enter patient's known background information, including their past medical conditions, medications, " + \
                   "family history, lifestyle, and other relevant information that can help in diagnosis and treatment**]")

# List of symptoms
st.session_state.symptoms = st.text_area("**Symptoms** *(Example: high-grade fever, lethargy, headache, and abdominal pain for two days)*", 
              value=symp_val, placeholder="none", 
              help=":green[**List all symptoms indicating the presence of an underlying medical condition**]")

# List of observations at exam
st.session_state.exam = st.text_area("**Examination findings** *(Example: petechial lesions on the palms of his hands and feet, bug bites)*", 
              value=exam_val, placeholder="none", 
              help=":green[**List all the information gathered through visual inspection, palpation, " + \
                   "percussion, and auscultation during the examination**]")

# Laboratory test results
st.session_state.labresults = st.text_area("**Laboratory test results** *(Example: w/IgE levels > 3000 IU/m)*", 
              value=lab_val, placeholder="none", 
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

vis_prompt = "<p style=\"font-size:18px;\">" + \
             "<b>Patient: </b>" + st.session_state.gender + ", " + str(st.session_state.age) + " years old.<br/>" + \
             "<b>Pregnancy: </b>" + st.session_state.pregnant + ".<br/>" + \
             "<b>History: </b>" + report_list[0] + ".<br/>" + \
             "<b>Symptoms: </b>" + report_list[1] + ".<br/>" + \
             "<b>Examination findings: </b>" + report_list[2] + ".<br/>" + \
             "<b>Laboratory test results: </b>" + report_list[3] + ".<br/> </p>"

st.write(vis_prompt, unsafe_allow_html=True) 

question_prompt = "Patient: " + st.session_state.gender + ", " + str(st.session_state.age) + " years old. " + \
                  "Pregnancy: " + st.session_state.pregnant + ". " + \
                  "History: " + report_list[0] + ". " + \
                  "Symptoms: " + report_list[1] + ". " + \
                  "Examination findings: " + report_list[2] + ". " + \
                  "Laboratory test results: " + report_list[3] + ". " + \
                  "What is the likely diagnosis ? " + \
                  "Then, insert '<br/><br/>' in your response. " + \
                  "And, propose a treatment formatted as an ordered list. " 
                  # Last two lines aren't often understandable by models other than DaVinci-003

st.subheader(":computer: :speech_balloon: :pill: **Diagnostic**")
if st.button('**Submit**'):
    if report_list[1] == "none":
        st.write("<p style=\"font-size:18px;\">Please, enter at least some symptoms before submission.</p>", 
                 unsafe_allow_html=True)
    else:
        with st.spinner('Please wait...'):
            try:
                diagnostic = openai_create(prompt=question_prompt)
                st.write(diagnostic.replace("<|im_end|>", ""), unsafe_allow_html=True)
            except: 
                st.write("<p style=\"font-size:18px;\">The server does not respond or is overloaded with requests... Try again.</p>", 
                         unsafe_allow_html=True)
else: 
    st.write("<p style=\"font-size:18px;\">No diagnostic yet, please click **Submit** above.</p>", 
             unsafe_allow_html=True)