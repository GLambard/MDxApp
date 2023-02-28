import streamlit as st
import os
from PIL import Image

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v
##

st.set_page_config(
    page_title="Contact",
    page_icon="✉️",
)

""" with st.sidebar.container():
    image = Image.open('/Users/guillaumelambard/Documents/OpenAI/Projects/MDxApp/Materials/MDxApp_logo_v2_64.png')
    st.image(image, width=64, use_column_width=True) """

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('/Users/guillaumelambard/Documents/OpenAI/Projects/MDxApp/Materials/MDxApp_logo_v2_64.png');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

st.header("Contact")

contact_form = """
<form action="https://formsubmit.co/{}" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
""".format(st.secrets["email_address"])

st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    path = os.path.dirname(__file__)
    file_name = path+"/"+file_name
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/email_style.css")