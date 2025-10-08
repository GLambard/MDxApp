import os
import sys
from pathlib import Path

import streamlit as st

# Add src directory to path for imports
path_dir = os.path.dirname(__file__)
project_root = Path(path_dir).parent.parent
sys.path.insert(0, str(project_root))

# Import new utilities
from src.utils.styling import load_main_styles

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v

st.set_page_config(
    page_title="Contact",
    page_icon="✉️",
)

# Load external CSS styles
load_main_styles(project_root)

st.header("Contact")

contact_form = """
<form action="https://formsubmit.co/{}" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
""".format(
    st.secrets["email_address"]
)

st.markdown(contact_form, unsafe_allow_html=True)


# Use Local CSS File
def local_css(file_name):
    path = os.path.dirname(__file__)
    file_name = path + "/" + file_name
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles/email_form.css")
