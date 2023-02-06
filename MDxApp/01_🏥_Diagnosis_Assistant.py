#import ptvsd
#ptvsd.enable_attach(address=('localhost', 8501))
#ptvsd.wait_for_attach() # Only include this line if you always want to attach the debugger

# Write a streamlit web app. The main title is "Diagnostic Assistant". It contains a gender selector, an age selector from 0 to 99+ years old.
import streamlit as st 

st.set_page_config(
    page_title="Diagnosis_Assistant",
    page_icon="🏥",
)

# From https://github.com/blackary/st_pages
# Pages config in .streamlit/pages.toml
#from st_pages import show_pages_from_config
#show_pages_from_config()

import os
import openai

# Quick FIX for SSL certificate localization
# Remove if out of DMZ
#os.environ["REQUESTS_CA_BUNDLE"] = '/usr/local/share/ca-certificates/extras/nims_proxy_copy.pem'
#os.environ["SSL_CERT_FILE"] = '/usr/local/share/ca-certificates/extras/nims_proxy_copy.pem'

#if you have OpenAI API key as an environment variable, enable the below
openai.api_key = os.getenv("OPENAI_API_KEY")

#if you have OpenAI API key as a string, enable the below
# From https://blog.streamlit.io/secrets-in-sharing-apps/
# secrets config in .streamlit/secrets.toml
openai.api_key = st.secrets["openai_api_key"]

def openai_create(prompt):

    response = openai.Completion.create(
    model="text-chat-davinci-002-20221122", # text-davinci-003, text-curie-001, text-chat-davinci-002-20230126, text-chat-davinci-002-20221122
    prompt=prompt,
    temperature=0., # 0.7
    max_tokens=750,
    #top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6, 
    stop = None
    )

    return response.choices[0].text

# Diagnostic Assistant 
st.title("Medical Diagnosis Support Tool (DxST)")

st.subheader("Report: ")
# Define columns
col1, col2, col3 = st.columns(3, gap="large")

# Gender selector 
with col1:
    gender = st.radio("**Gender**", ("Male", "Female"))
# Age selector 
with col2:
    age = st.number_input("**Age**", min_value= 0, max_value= 99, step=1)
# Pregnancy
with col3: 
    pregnant = st.radio("**Pregnant**", ("No", "Yes"))

# Context
context = st.text_input('**History** *(Example: gone to an outdoor music festival, shared drinks and cigarettes with friends with similar symptoms)*', 
                        value="", placeholder="none")

# List of symptoms
symptoms = st.text_input("**Symptoms** *(Example: high grade fever, lethargy, headache, abdominal pain)*", 
                         value="", placeholder="none") 

# Duration of symptoms
symptoms_duration = st.text_input("**Duration of symptoms** *(Example: 2 hours/days)*", 
                                  value="", placeholder="unknown") 

# List of observations at exam
exam = st.text_input("**Observations** *(Example: petechial lesions on the palms of his hands and feet, bug bites)*", 
                     value="", placeholder="none")

# Existing pre-treatment
pretreatment = st.text_input("**Existing treatment(s)** *(Example: compliant to HIV medications)*", 
                             value="", placeholder="none")

st.subheader("Summary: ")
# Diagnostic
if context == "":
    context = "none"
if symptoms == "": 
    symptoms = "none"
if symptoms_duration == "": 
    symptoms_duration = "unknown"
if exam == "":
    exam = "none"
if pretreatment == "":
    pretreatment = "none"

vis_prompt = "<b>Patient: </b>" + gender + ", " + str(age) + " years old.<br/>" + \
             "<b>Pregnancy: </b>" + pregnant + ".<br/>" + \
             "<b>History: </b>" + context + ".<br/>" + \
             "<b>Symptoms: </b>" + symptoms + " during " + symptoms_duration + ".<br/>" + \
             "<b>Observations: </b>" + exam + ".<br/>" + \
             "<b>Existing pre-treatment: </b>" + pretreatment + ".<br/>"

st.write(vis_prompt, unsafe_allow_html=True) 

question_prompt = "Patient: " + gender + ", " + str(age) + " years old. " + \
                  "Pregnancy: " + pregnant + ". " + \
                  "History: " + context + ". " + \
                  "Symptoms: " + symptoms + " during " + symptoms_duration + ". " + \
                  "Observations: " + exam + ". " + \
                  "Existing pre-treatment: " + pretreatment + ". " + \
                  "What is the likely diagnosis ? " + \
                  "Then, insert '<br/><br/>' in your response. " + \
                  "And, propose a treatment formatted as an ordered list. " 
                  # Last two lines aren't often understandable by models other than DaVinci-003

st.subheader("Diagnostic: ")
if st.button('**Submit**'):
    if symptoms == "none":
        st.write("Please, enter some symptoms before submission.")
    else:
        with st.spinner('Please wait...'):
            try:
                diagnostic = openai_create(prompt=question_prompt)
                st.write(diagnostic, unsafe_allow_html=True)
            except: 
                st.write("The server do not respond or is overloaded with requests... Try again.")
else: 
    st.write("No diagnostic yet, please click **Submit**.")