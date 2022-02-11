from Libraries import *
import Interface_docker
import Interface2_docker
#Changing the background with an image that has to be in the same folder
import base64
main_bg = './app/Background.png'
main_bg_ext = "png"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
        background-size: 100% 100%
    }}
    </style>
    
    """,
    unsafe_allow_html=True
)

### start streamlit
image = Image.open('./app/BEEV_image.png')
st.image(image)    

PAGES = {
    "GEV car selection": Interface2_docker,
    "Manual features selection": Interface_docker
}
st.sidebar.title('How would you like to select your features ?')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()


