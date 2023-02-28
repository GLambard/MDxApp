import streamlit as st
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

# Use Local logo File
path = os.path.dirname(__file__)
file_name = path+"/../../Materials/MDxApp_logo_v2_256.png"
st.sidebar.image(file_name, caption= '', width=256)

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