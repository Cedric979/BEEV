import numpy as np
import pandas as pd
import streamlit as st
import string
from PIL import Image

#LIBRARIES
import numpy as np # linear algebra
import pandas as pd # data processing
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
#IMPORTING LIBRAY TO GET GOOGLE SPREADSHEETS
import gspread

#global link1

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

#importing the googlesheet document named fuel prices
gc = gspread.service_account(filename='C:\Users\Utilizador\Documents\Streamlit app experiment\beev-335814-4e72d6b41e21S.json')
fuel_prices_url = 'https://docs.google.com/spreadsheets/d/1M_e1ENe40v-G_HYYH7YTZT5yPMoxgk36FFNamtg12f8/edit?usp=sharing'
sht4 = gc.open_by_url(fuel_prices_url)
#sht4.sheet1
worksheet = sht4.sheet1
fuel_prices = pd.DataFrame(worksheet.get_all_records())
elec_price = float(fuel_prices[fuel_prices['Fuel type'] == 'Electricity']['Price France (€/litres) - KWh'])


#Code for EV DF
df = pd.read_csv("Beev Electric Vehicle Specs Data.csv")
df['Main Price'].fillna(62000.0, inplace = True)
df['Range (km)'].fillna(235.0, inplace = True)
df_new = pd.DataFrame(zip(df['Full Name'],df['Main Price'],df['Range (km)'], df['Category'],df['Useable Battery Capacity']))
df_new.rename(columns = {0:'Full Name', 1:'Price (€)',2:'Range (Km)',3:'Category',4:'Useable Battery Capacity'}, inplace = True)
df_model = df_new
df_model['Price with Incentive (€)'] = df_model['Price (€)'].apply(lambda item: item - 6000)
df_model['Price (€)'] = df_model['Price (€)'].astype(int)
df_model['Price with Incentive (€)'] = df_model['Price with Incentive (€)'].astype(int)
df_model['Range (Km)'] = df_model['Range (Km)'].astype(int)
df_model['cost/100Km (€)'] = df_model[['Range (Km)','Useable Battery Capacity']].apply(lambda item: (item[1]/item[0])*100*elec_price, axis = 1)
#Building the categories for the choice in selectbox
categories = list(df['Category'].unique())
categories.insert(0,"ALL")

#DF Filtered
df_filtered = df[['Full Name', 'Model', 'Brand','Range (km)','Battery Capacity (kW)', 'Useable Battery Capacity','Category','Government Incentive Category for Help','Vehicle Consumption (Wh)','Charging Time 7,4 kW','Charging Time 11 kW','Main Price']].copy()
df_filtered['cost/100Km (€)'] = df_filtered[['Range (km)','Useable Battery Capacity']].apply(lambda item: (item[1]/item[0])*100*elec_price, axis = 1)
df_filtered['Price with Incentive'] = df_filtered['Main Price'].apply(lambda item: item - 6000)

#Getting the title_tax_cv and build the list of regions for the choice in the interface

#sh = gc.open(name of file)
#title_tax_cv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
title_tax_cv_url = "https://docs.google.com/spreadsheets/d/1cOj98R9fGT89rG4-TxAPIgOrvDbrzxlLPd4Y5mUBD0g/edit?usp=sharing"
sht1 = gc.open_by_url(title_tax_cv_url)
worksheet = sht1.sheet1
#Building the DF
title_tax_cv = pd.DataFrame(worksheet.get_all_records())
#Building the list of regions for the selectbox
regions = list(title_tax_cv['Region'].unique())


### start streamlit
image = Image.open('BEEV_image.png')
st.image(image)
st.title("Let's check which EV cars would suit to you")
#value_one = st.text_area("text box")

#Defining the selectbox
label1 = "please select the category of the car you would like"
category_choosen = st.selectbox(label1,categories)
#Defining the selectbox for the region ########### be careful need to add the DF and the regions variable before here
label2 = "please select the region you are from"
region_choosen = st.selectbox(label2,regions)

#st.write(category_choosen)


#Asking the user the Price and the Range
# Add a slider to the sidebar:
range_slider = st.sidebar.slider('Select a desired range in Kilometers',200, 800, (250))
price_slider = st.sidebar.slider('Select a desired price for the EV car',10000, 100000, (15000))
duration_slider = st.sidebar.slider('Select a desired duration for leasing or keeping EV car in months',1, 72, (12))
km_slider = st.sidebar.slider('Select Km done per year',1000, 100000, (10000))

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
    #Building the TCO
    df_TCO = df_model[['Full Name', 'Price (€)','Range (Km)','Category','Price with Incentive (€)','cost/100Km (€)']].iloc[result[0]].set_index('Full Name').copy()
    df_TCO['title_cost (€)'] = df_TCO['cost/100Km (€)'].apply(lambda item: title_tax_cv[title_tax_cv['Region'] == region_choosen]['Title Cost (€ / CV)']*1)
    df_TCO['consumption_cost (month)'] = df_TCO['cost/100Km (€)'].apply(lambda item: item/100*km_slider/12)
    df_TCO['maintenance_cost (month)'] = df_TCO['cost/100Km (€)'].apply(lambda item: km_slider/12*0.0208)
    df_TCO['TCO_month'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1] + item[2],axis=1)
    df_TCO['TCO_year'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1]*12 + item[2]*12,axis=1)
    df_TCO['TCO_duration'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1]*duration_slider + item[2]*duration_slider,axis=1)
    #Formating the result with choosen number (float)
    df_TCO.style.format({'Price (€)': '{:.0f}', 'Range (Km)': '{:.0f}', 'Price with Incentive (€)': '{:.0f}', 'cost/100Km (€)':'{:.0f}','TCO_year':'{:.1f}', 'TCO_duration': '{:.1f}'})
    st.write(df_TCO[['Range (Km)','Category','Price with Incentive (€)','TCO_year','TCO_duration']])