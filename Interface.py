#!/usr/bin/env python
# coding: utf-8

# In[4]:

import numpy as np
import pandas as pd
import streamlit as st
import string
from PIL import Image

#LIBRARIES
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#Graphics
#import matplotlib.pyplot as plt
#import seaborn as sns
#KNeighbors
from sklearn.neighbors import NearestNeighbors
#Scalers
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler
#Data selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.decomposition import PCA
#METRICS
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score, recall_score,accuracy_score
from sklearn.metrics import mean_squared_error
#RANDOM
import random as rd

#global link1

import base64
main_bg = "images_background.jpeg"
main_bg_ext = "jpeg"

side_bg = "images_background.jpeg"
side_bg_ext = "jpeg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)


#Code
df = pd.read_csv("Beev Electric Vehicle Specs Data.csv")
df['Main Price'].fillna(62000.0, inplace = True)
df['Range (km)'].fillna(235.0, inplace = True)
df_new = pd.DataFrame(zip(df['Full Name'],df['Main Price'],df['Range (km)'], df['Category']))
df_new.rename(columns = {0:'Full Name', 1:'Price (€)',2:'Range (Km)',3:'Category'}, inplace = True)
df_model = df_new
df_model['Price with Incentive (€)'] = df_model['Price (€)'].apply(lambda item: item - 6000)
df_model['Price (€)'] = df_model['Price (€)'].astype(int)
df_model['Price with Incentive (€)'] = df_model['Price with Incentive (€)'].astype(int)
df_model['Range (Km)'] = df_model['Range (Km)'].astype(int)

#distanceKNN.kneighbors([[60000]], 3, return_distance = False)
#df[['Full Name', 'Main Price']].iloc[[148, 16, 57]]
categories = list(df['Category'].unique())
categories.insert(0,"ALL")

#df_new[['Full Name', 'Price', 'Range', 'Category']].iloc[[66, 36, 47, 37, 64]]# result to display

### start streamlit
image = Image.open('BEEV_image.png')
st.image(image)
st.title("Let's check which EV cars would suit to you")
#value_one = st.text_area("text box")

#Defining the selectbox
label1 = "please select the category of the car you would like"
category_choosen = st.selectbox(label1,categories)
#st.write(category_choosen)

     


#Asking the user the Price and the Range
# Add a slider to the sidebar:
range_slider = st.sidebar.slider('Select a desired range in Kilometers',200, 800, (250))
price_slider = st.sidebar.slider('Select a desired price for the EV car',10000, 100000, (15000))

#X = pd.DataFrame()
#Define the validation button
if st.button('Get EV Cars recommendation'):
    df_model.style.format({'Price (€)': '{:.0f}', 'Range (Km)': '{:.0f}', 'Price with Incentive (€)': '{:.0f}'})
    #distanceKNN_cars = NearestNeighbors()
    #result = np.array([])
    if category_choosen != "ALL":
        df_model = df_model[df_model['Category'] == category_choosen].copy()
        X = df_model[['Price (€)', 'Range (Km)']]
        distanceKNN_cars = NearestNeighbors(n_neighbors=5).fit(X)
        result = distanceKNN_cars.kneighbors([[price_slider,range_slider]], 5, return_distance = False)
        #st.write(
    else:   
        distanceKNN_cars = NearestNeighbors(n_neighbors=5).fit(df_model[['Price (€)', 'Range (Km)']])
        result = distanceKNN_cars.kneighbors([[price_slider,range_slider]], 5, return_distance = False)
    
    st.write(df_model[['Full Name', 'Price (€)','Range (Km)','Category','Price with Incentive (€)']].iloc[result[0]].set_index('Full Name'))
    