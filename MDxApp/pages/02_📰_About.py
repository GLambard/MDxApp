import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.buy_me_a_coffee import button
import os

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v
##

st.set_page_config(
    page_title="About",
    page_icon="📰",
    layout="wide"
)

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
    qr_name = path+"/../../Materials/bmc_qr.png"
    st.image(qr_name, caption= '', width = 220)

st.header("About")

st.markdown(
    """
    ### **Brief description of the web app**
    This app is designed to assist medical doctors in finding a 
    right diagnostic by allowing them to enter relevant information such as age, 
    gender, pregnancy state, environmental context, symptoms, observations, and 
    pre-treatment information.
    ### Versions
    :sparkles: Current version: V1.01 (2023/01/30) :sparkles:
    ### :rotating_light: **Caution message** :rotating_light:
    Please be aware that while the app is designed to assist medical professionals, 
    the final diagnosis should be made by a licensed medical professional. We recommend 
    seeking additional evaluations and opinions before making any treatment decisions.
    ### **Message from the developer**
    > Dear community,  
    > 
    > I am proud to announce the deployment of this free app that provides medical diagnosis assistance to those in need.  
    > 
    > I want to take this moment to thank the open-source community for their unwavering support in making this project a reality. 
    > Your contributions, in any form, have allowed me to bring this tool to all.  
    > 
    > I hope this app will positively impact people's lives, and I am grateful for the opportunity to serve the community in this way.  
    > 
    > Thank you for your continued support.  
    > 
    > Best,  
    > 
    > Guillaume Lambard  
    > AI solutions designer and developer  
    > *(who developed this tool in his spare time)*
    >  
    >  
    """, 
    unsafe_allow_html=True
)