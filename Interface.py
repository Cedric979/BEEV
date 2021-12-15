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

#Code
df = pd.read_csv("Beev Electric Vehicle Specs Data.csv")
df['Main Price'].fillna(62000.0, inplace = True)
df['Range (km)'].fillna(235.0, inplace = True)
df_new = pd.DataFrame(zip(df['Full Name'],df['Brand'], df['Model'], df['Main Price'], df['Category']))
df_new.rename(columns = {0:'Full Name', 1:'Brand', 2:'Model', 3:'Main Price',4: 'Category'}, inplace = True)
df_model = df_new
df_model['Main Price'] = df_model['Main Price'].apply(lambda item: item + 6000)

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

#Filtering before fitting the model to have NN macthing the user choice
if category_choosen!= "ALL":
    X = df_model[df_model['Category'] == category_choosen][['Price', 'Range']]
else: 
    X = df_model[['Price', 'Range']]       

distanceKNN = NearestNeighbors(n_neighbors=5).fit(X)

#Asking the user the Price and the Range
# Add a slider to the sidebar:
range_slider = st.sidebar.slider('Select a desired range in Kilometers',200.0, 800.0, (25.0, 75.0))
price_slider = st.sidebar.slider('Select a desired price for the EV car',10000.0, 100000.0, (25.0, 75.0))


#Define the validation button
if st.button('Get info'):
    
  st.write(value_one)
  #  for i in range(1, 1000): #len(df_lyrics_final['Lyric'])):
   #   
    #    lyrics_comparator(punct(lyrics_one), punct(df_lyrics_final['Lyric'][i]))
     #   final_dict[i] = [max_similar,similar_w_unique, similar_w_not_unique]

  #  lyrics_report(punct(lyrics_one), punct(df_lyrics_final['Lyric'][dict_sum(final_dict)]))
   # st.write(df_lyrics_final.iloc[dict_sum(final_dict)][['Artist','Song']]) #veribal 
    #link1 = df_lyrics_final.iloc[dict_sum(final_dict)][['SLink']][0]
    #st.write(type(link1))


    #st.write(link1)
   # url = f"https://www.vagalume.com.br{link1}"
   # st.write(url)




