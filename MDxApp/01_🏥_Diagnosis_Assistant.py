import json
import os
import sys
from pathlib import Path

import openai
import streamlit as st

# Add src directory to path for imports
path = os.path.dirname(__file__)
project_root = Path(path).parent
sys.path.insert(0, str(project_root))

# Import new components and utilities
from src.components.donation import (
    get_default_qr_path,
    render_inline_donation,
    render_sidebar_donation,
)
from src.components.language_selector import add_language_separator, render_language_selector
from src.utils.styling import load_main_styles

# Load translations from JSON file
with open(path + "/../Assets/translations.json") as f:
    transl = json.load(f)

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v
##

# Initialize OpenAI client for GPT-5 Mini
# Check if using new client or legacy
use_new_client = st.secrets.get("use_new_ai_client", False)

if use_new_client:
    # Modern OpenAI SDK v1.x for GPT-5 Mini
    from openai import OpenAI

    openai_client = OpenAI(api_key=st.secrets["openai_api_key"])

    def openai_create(prompt):
        """Create diagnosis using modern OpenAI SDK (supports GPT-5 Mini)."""
        try:
            # GPT-5 Mini requires temperature=1.0 (only supported value)
            # and doesn't support frequency/presence penalties
            response = openai_client.chat.completions.create(
                model=st.secrets.get("openai_api_model", "gpt-5-mini"),
                messages=[
                    {"role": "system", "content": st.secrets["prompt_canvas"]["prompt_system"]},
                    {"role": "user", "content": prompt},
                ],
                max_completion_tokens=int(st.secrets.get("openai_api_maxtok", 2000)),
                # Note: GPT-5 Mini only supports temperature=1.0 (default)
                # frequency_penalty and presence_penalty are not supported
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"OpenAI API Error: {str(e)}")
            return None

else:
    # Legacy OpenAI SDK v0.27.0 (for backward compatibility)
    openai.api_key = st.secrets["openai_api_key"]

    def openai_create(prompt):
        """Create diagnosis using legacy OpenAI SDK."""
        response = openai.ChatCompletion.create(
            model=st.secrets["openai_api_model"],
            messages=[
                {"role": "system", "content": st.secrets["prompt_canvas"]["prompt_system"]},
                {"role": "user", "content": prompt},
            ],
            temperature=float(st.secrets["openai_api_temp"]),
            max_tokens=int(st.secrets["openai_api_maxtok"]),
            frequency_penalty=int(st.secrets["openai_api_freqp"]),
            presence_penalty=float(st.secrets["openai_api_presp"]),
            stop=None,
        )
        return response["choices"][0]["message"]["content"]


st.set_page_config(page_title="Diagnosis_Assistant", page_icon="🏥", layout="wide")

# Load external CSS styles
load_main_styles(project_root)

# Language selection using component
lang = render_language_selector(transl, location="sidebar")

# Line separator for clarity
add_language_separator(location="sidebar")

# CSS now loaded from external file (pages/styles/main.css)

# Buy me a coffee - MDxApp support (using component)
with st.sidebar:
    render_sidebar_donation(
        username="geonosislaX",
        translations=transl,
        language=lang,
        qr_image_path=get_default_qr_path(project_root),
    )

# Use GitHub logo file
logo_name = path + "/../Materials/MDxApp_logo_v2_256.png"

# Define columns
t1, t2 = st.columns([1, 3], gap="large")
with t1:
    st.image(logo_name, caption="", width=256)
with t2:
    st.header("**{}**".format(transl[lang]["page1_header"]))
    st.write(
        '<p style="font-weight: bold; font-size:18px;">{}</p>'.format(
            transl[lang]["page1_subheader"]
        ),
        unsafe_allow_html=True,
    )

st.markdown("", unsafe_allow_html=True)
"""
---
"""
st.write(
    '<p style="font-weight: bold; font-size:18px;">{}</p>'.format(transl[lang]["htu_0"])
    + '<p style="font-size:18px;">1. {}<br/>'.format(transl[lang]["htu_1"])
    + "2. {}<br/>".format(transl[lang]["htu_2"])
    + "3. {}</p>".format(transl[lang]["htu_3"]),
    unsafe_allow_html=True,
)

# All CSS now loaded from external file (pages/styles/main.css)

st.subheader(":black_nib: **{}**".format(transl[lang]["report_header"]))
# Define columns
col1, col2, col3 = st.columns(3, gap="large")

# Store initial values in session state
if "disabled" not in st.session_state:
    st.session_state.disabled = False
# Declare lists
genders_list = ["{}".format(transl[lang]["male"]), "{}".format(transl[lang]["female"])]
pregnant_list = ["{}".format(transl[lang]["no"]), "{}".format(transl[lang]["yes"])]
##

# Gender selector
with col1:
    if st.session_state["lang_changed"] and "gender" in st.session_state:
        del st.session_state["gender"]
    if "gender" not in st.session_state:
        st.session_state["gender"] = genders_list[0]
    st.radio("**{}**".format(transl[lang]["gender"]), genders_list, key="gender")
# Age selector
with col2:
    st.number_input(
        "**{}**".format(transl[lang]["age"]), min_value=0, max_value=99, step=1, key="age"
    )
# Pregnancy
if st.session_state.gender == "{}".format(transl[lang]["male"]):
    st.session_state.disabled = True
    if "pregnant" in st.session_state:
        st.session_state["pregnant"] = "{}".format(transl[lang]["no"])
else:
    st.session_state.disabled = False

with col3:
    if st.session_state["lang_changed"] and "pregnant" in st.session_state:
        del st.session_state["pregnant"]
    if "pregnant" not in st.session_state:
        st.session_state["pregnant"] = pregnant_list[0]
    st.radio(
        "**{}**".format(transl[lang]["pregnant"]),
        pregnant_list,
        disabled=st.session_state.disabled,
        key="pregnant",
    )

# Context
st.text_input(
    "**{}** *{}*".format(transl[lang]["history"], transl[lang]["hist_example"]),
    placeholder="{}".format(transl[lang]["hist_ph"]),
    key="context",
    max_chars=250,
    help=":green[**{}**]".format(transl[lang]["hist_help"]),
)

# List of symptoms
st.text_input(
    "**{}** *{}*".format(transl[lang]["symptoms"], transl[lang]["symp_example"]),
    placeholder="{}".format(transl[lang]["symp_ph"]),
    key="symptoms",
    max_chars=250,
    help=":green[**{}**]".format(transl[lang]["symp_help"]),
)

# List of observations at exam
st.text_input(
    "**{}** *{}*".format(transl[lang]["exam"], transl[lang]["exam_example"]),
    placeholder="{}".format(transl[lang]["exam_ph"]),
    key="exam",
    max_chars=250,
    help=":green[**{}**]".format(transl[lang]["exam_help"]),
)

# Laboratory test results
st.text_input(
    "**{}** *{}*".format(transl[lang]["lab"], transl[lang]["lab_example"]),
    placeholder="{}".format(transl[lang]["lab_ph"]),
    key="labresults",
    max_chars=250,
    help=":green[**{}**]".format(transl[lang]["lab_help"]),
)

st.subheader(":clipboard: **{}**".format(transl[lang]["summary"]))
# Diagnostic

report_list = [
    st.session_state.context,
    st.session_state.symptoms,
    st.session_state.exam,
    st.session_state.labresults,
]
corr_list = [
    "{}".format(transl[lang]["none"]),
    "{}".format(transl[lang]["none"]),
    "{}".format(transl[lang]["none"]),
    "{}".format(transl[lang]["none"]),
]
for ic in range(0, len(report_list)):
    if report_list[ic] == "":
        report_list[ic] = corr_list[ic]

vis_summary = (
    '<p style="font-size:18px;">'
    + "<b>{}</b>".format(transl[lang]["vissum_patient"])
    + st.session_state.gender
    + ", "
    + str(st.session_state.age)
    + "{}<br/>".format(transl[lang]["vissum_yrsold"])
    + "<b>{}</b>".format(transl[lang]["vissum_pregnancy"])
    + st.session_state.pregnant
    + "<br/>"
    + "<b>{}</b>".format(transl[lang]["vissum_history"])
    + report_list[0]
    + "<br/>"
    + "<b>{}</b>".format(transl[lang]["vissum_symp"])
    + report_list[1]
    + "<br/>"
    + "<b>{}</b>".format(transl[lang]["vissum_exam"])
    + report_list[2]
    + "<br/>"
    + "<b>{}</b>".format(transl[lang]["vissum_lab"])
    + report_list[3]
    + "<br/> </p>"
)

st.write(vis_summary, unsafe_allow_html=True)

prompt_words = st.secrets["prompt_canvas"]["prompt_words"]
question_prompt = (
    prompt_words[0]
    + st.session_state.gender
    + ", "
    + str(st.session_state.age)
    + "{}. ".format(transl[lang]["vissum_yrsold"])
    + prompt_words[1]
    + st.session_state.pregnant
    + ". "
    + prompt_words[2]
    + report_list[0]
    + ". "
    + prompt_words[3]
    + report_list[1]
    + ". "
    + prompt_words[4]
    + report_list[2]
    + ". "
    + prompt_words[5]
    + report_list[3]
    + ". "
    + prompt_words[6]
    + prompt_words[7]
    + prompt_words[8]
    + prompt_words[9]
    + lang
    + ". "
)

st.write("")
submit_button = st.button(
    "**{}**".format(transl[lang]["submit"]),
    help=":green[**{}**]".format(transl[lang]["submit_help"]),
)
st.write("")

st.subheader(":computer: :speech_balloon: :pill: **{}**".format(transl[lang]["diagnostic"]))
if submit_button:
    if report_list[1] == "{}".format(transl[lang]["none"]):
        st.write(
            '<p style="font-weight: bold; font-size:18px;">{}</p>'.format(
                transl[lang]["submit_warning"]
            ),
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("{}".format(transl[lang]["submit_wait"])):
            try:
                diagnosis_result = openai_create(prompt=question_prompt)

                if diagnosis_result:
                    st.session_state.diagnostic = diagnosis_result
                    st.write("")
                    st.write(
                        st.session_state.diagnostic.replace("<|im_end|>", ""),
                        unsafe_allow_html=True,
                    )
                else:
                    # Error already displayed by openai_create
                    st.write(
                        '<p style="font-weight: bold; font-size:18px;">{}</p>'.format(
                            transl[lang]["no_response"]
                        ),
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    """
                            ### :rotating_light: **{}** :rotating_light:
                            {}
                            """.format(
                        transl[lang]["caution"], transl[lang]["caution_message"]
                    ),
                    unsafe_allow_html=True,
                )

                # Buy me a coffee - MDxApp support (using component)
                render_inline_donation(
                    username="geonosislaX",
                    translations=transl,
                    language=lang,
                    qr_image_path=get_default_qr_path(project_root),
                    show_separator=True,
                    invest_message=True,
                )
            except Exception:
                # st.write(e)
                st.write(
                    '<p style="font-weight: bold; font-size:18px;">{}</p>'.format(
                        transl[lang]["no_response"]
                    ),
                    unsafe_allow_html=True,
                )
else:
    if "diagnostic" in st.session_state:
        st.write(st.session_state.diagnostic.replace("<|im_end|>", ""), unsafe_allow_html=True)
    else:
        st.write(
            '<p style="font-weight: bold; font-size:18px;">{}</p>'.format(
                transl[lang]["no_diagnostic"]
            ),
            unsafe_allow_html=True,
        )
