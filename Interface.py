#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import streamlit as st
import string
from PIL import Image

#LIBRARIES
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#Graphics
import matplotlib.pyplot as plt
import seaborn as sns
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

df = pd.read_csv("Beev Electric Vehicle Specs Data.csv")
df_new = pd.DataFrame(zip(df['Full Name'],df['Brand'], df['Model'], df['Main Price'], df['Category']))
df_new.rename(columns = {0:'Full Name', 1:'Brand', 2:'Model', 3:'Main Price',4: 'Category'}, inplace = True)
df_new['Main Price'].value_counts(dropna = False)   # We either drop the Nans or we fill with the average
df_new['Main Price'].fillna(df_new['Main Price'].mean(), inplace = True) 
X = df_new[['Main Price']]          
distanceKNN = NearestNeighbors(n_neighbors=3).fit(X)
distanceKNN.kneighbors([[60000]], 3, return_distance = False)
df[['Full Name', 'Main Price']].iloc[[148, 16, 57]]

image = Image.open('BEEV_image.png')
st.image(image)
st.title("Let's check which EV cars would suit to you")
lyrics_one = st.text_area("Paste the Lyrics")


st.write("The closest lyrical song contains",song2_len,"words")
st.write(df_lyrics['equal'].sum(),"words are at the exact same position")
# st.write("similar unique words",dict2)
st.write(round((df_lyrics['equal'].sum()/song2_len)*100,2), "% of your song is exactly the same")
st.write(round((len(dict3)/len(list_song2)) * 100, 2),"% of same words are used")
#st.write("please find below the list of the words present in your song with the number of appearence")
#st.write(value_dict_lyrics1,value_dict_lyrics2)
return similar_w_unique, similar_w_not_unique, max_similar, value_dict_lyrics1, value_dict_lyrics2


if st.button('Get info'):
  
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

