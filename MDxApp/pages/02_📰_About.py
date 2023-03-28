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
    This app is designed to assist medical doctors and provide patients with a 
    fast diagnostic supported by the ChatGPT AI model of [OpenAI](https://openai.com/) based on relevant information such as age, 
    gender, pregnancy state, environmental and historical context, symptoms, observations, and test results conducted in laboratory.
    ### **Why should you buy me a coffee, i.e. donate ?**
    This app uses the ChatGPT AI model through the official API of OpenAI which has a cost. Also, this app is free to use and will 
    remain free to use for all if you support it by buying me a coffee (see the dedicated button and QR code on the left side). 
    Thank you very much in advance for making it possible !
    ### Coming features
    - Differential diagnosis :clipboard:
    - Multilingual interface 🇬🇧 🇨🇳 🇪🇸 🇧🇷 🇮🇩 🇷🇺 🇩🇪
    ### Versions
    :sparkles: **Current version: V1.121** (2023/03/28) :sparkles:  
    - Updates: Rolling out French and Japanese translations of the UI, bug fixes.

    Version history:
    - v1.11 (2023/03/07): Updates: **Highlight** in HTML format the **proposed diagnostic**, **caution message** added, bug fixes.
    - v1.10 (2023/03/02): Updates: **model gpt-3.5-turbo (ChatGPT) integration**, bug fixes, and performance improvements.
    - v1.01 (2023/01/30): Internal pre-release
    ### **Sources**
    - The source code of this app is available [here](https://github.com/GLambard/MDxApp)
    - Anonymous public cases taken from the Brown Hospital Medicine Twitter account [@BrownJHM](https://twitter.com/BrownJHM) 
    are used as illustrating examples on the main page of the app. 
    ### :rotating_light: **Caution message** :rotating_light:
    Please be aware that while the app is designed to assist medical decision-making and check symptoms, 
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

html(f"""
    <a class="github-button" href="https://github.com/GLambard/MDxApp" data-show-count="true" aria-label="Follow @GLambard on GitHub">Follow @GLambard</a>
    <script async defer src="https://buttons.github.io/buttons.js"></script>
    <a class="twitter-follow-button" href="https://twitter.com/gamlambard">Follow @gamlambard</a>
    <script async defer src="https://platform.twitter.com/widgets.js"></script>
    """)