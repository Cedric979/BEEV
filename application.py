#import numpy as np
#import pandas as pd
#import streamlit as st
#import string
#from PIL import Image
#import datetime
import Libraries

#Changing the background with an image that has to be in the same folder
import base64
main_bg = "st_back_main3.jpeg"
main_bg_ext = "jpeg"

side_bg = "st_back_slider.jpeg"
side_bg_ext = "jpeg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
        background-size: 100% 100%
    }}
   .sidebar.sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        background-size: 100% 100%
    }}
    </style>
    
    """,
    unsafe_allow_html=True
)


### start streamlit
image = Image.open('BEEV_image.png')
st.image(image)    
#app.py
import Interface
import Interface2
import streamlit as st

PAGES = {
    "GEV car selection": Interface2,
    "Manual features selection": Interface
}
st.sidebar.title('How would you like to select your features ?')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()


