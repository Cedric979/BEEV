def app():
    import numpy as np
    import pandas as pd
    import streamlit as st
    import string
    from PIL import Image
    import datetime
    import seaborn as sns

    #LIBRARIES
    import numpy as np # linear algebra
    import pandas as pd # data processing
    from sklearn.neighbors import NearestNeighbors
    #Scalers
    from sklearn import preprocessing
    #RANDOM
    import random as rd
    #IMPORTING LIBRAY TO GET GOOGLE SPREADSHEETS
    import gspread
    #Defining gc to be able to read the googlesheet files
    gc = gspread.service_account(filename='../../Wild_Code_School/keys/beev-335814-edfca510cf50.json')

    #Condition to access the updating button
    password = st.text_input('If you want to update the data with the google sheet documents please enter the password', max_chars=10)
    if password == 'Semra':
        ############################ loadind & Saving the DATA FROM GOOGLE SHEET DOCUMENTS##############################################

        #Adding a button to the sidebar to be able to manually actualize the data from the googlesheet files
        if st.button("Click here to update"):
            #importing the googlesheet document named fuel prices
            fuel_prices_url = 'https://docs.google.com/spreadsheets/d/1M_e1ENe40v-G_HYYH7YTZT5yPMoxgk36FFNamtg12f8/edit?usp=sharing'
            sht4 = gc.open_by_url(fuel_prices_url)
            #sht4.sheet1
            worksheet = sht4.sheet1
            fuel_prices = pd.DataFrame(worksheet.get_all_records())
            fuel_prices.to_csv('fuel_prices_db',header=True, index=False)

            #Getting the title_tax_cv and build the list of regions for the choice in the interface
            title_tax_cv_url = "https://docs.google.com/spreadsheets/d/1cOj98R9fGT89rG4-TxAPIgOrvDbrzxlLPd4Y5mUBD0g/edit?usp=sharing"
            sht1 = gc.open_by_url(title_tax_cv_url)
            worksheet = sht1.sheet1
            #Building the DF
            title_tax_cv = pd.DataFrame(worksheet.get_all_records())
            title_tax_cv.to_csv('title_tax_cv_db',header=True, index=False)

            #importing the googlesheet document named BONUS/MALUS 2022
            bonus_malus_url = "https://docs.google.com/spreadsheets/d/1RDIMbTGE3TBU4SXbRNKiqKQFakf0grVGKKLfu9L9dS4/edit?usp=sharing"
            sht1 = gc.open_by_url(bonus_malus_url)
            worksheet = sht1.sheet1
            #Building the DF
            bonus_malus = pd.DataFrame(worksheet.get_all_records())
            bonus_malus.to_csv('bonus_malus_db',header=True, index=False)

            #importing the googlesheet document named maintenance costs
            maintenance_costs_url = "https://docs.google.com/spreadsheets/d/1Hlhp4ubS-JFgYYx1S9oeL5A_011sSxvKzWiuS3bLqV8/edit?usp=sharing"
            sht1 = gc.open_by_url(maintenance_costs_url)
            worksheet = sht1.sheet1
            #Building the DF
            maintenance_costs = pd.DataFrame(worksheet.get_all_records())
            maintenance_costs.to_csv('maintenance_costs_db',header=True, index=False)


        ############################ loadind & Saving the DATA FROM GOOGLE SHEET DOCUMENTS##############################################


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
    st.title("GEV car selection")


    ############################DATA FROM GOOGLE SHEET DOCUMENTS##############################################
    #Building the Data for fuel prices and elec price for next calculation
    fuel_prices = pd.read_csv('fuel_prices_db')
    elec_price = float(fuel_prices[fuel_prices['Fuel type'] == 'Electricity']['Price France (€/litres) - KWh'])
    petrol_price = float(fuel_prices[fuel_prices['Fuel type'] == 'Regular gasoline']['Price France (€/litres) - KWh'])
    diesel_price = float(fuel_prices[fuel_prices['Fuel type'] == 'Diesel']['Price France (€/litres) - KWh'])

    #Building the list of regions for the selectbox
    title_tax_cv = pd.read_csv('title_tax_cv_db')
    regions = list(title_tax_cv['Region'].unique())

    #Building the Data for bonus_malus
    bonus_malus = pd.read_csv('bonus_malus_db')
    bonus_malus['Malus (€)'] = bonus_malus['Malus (€)'].apply(lambda item: item.replace(' ','') if type(item) == str else item)
    bonus_malus['Malus (€)'] = bonus_malus['Malus (€)'].astype(int)
    def malus_calculation(item):
        malus = 0
        if item < bonus_malus['g / km'].min():
            malus = 0
        elif item > bonus_malus['g / km'].max():
            malus = bonus_malus['Malus (€)'].max()
        else :
            malus_index = bonus_malus['Malus (€)'][bonus_malus['g / km'] == item].index[0]       
            malus = bonus_malus['Malus (€)'].iloc[malus_index]
        return malus

    #Building the Data for maintenance_costs
    maintenance_costs = pd.read_csv('maintenance_costs_db')
    def maint_cost_coef(item):
        if item in list(maintenance_costs['Brand'].value_counts().keys()):
            return maintenance_costs['Average Gas engine (€/km)'].iloc[maintenance_costs[maintenance_costs['Brand'] == item].index[0]]/10000
        else: return round(maintenance_costs['Average Gas engine (€/km)'].mean()/10000,2)
        
    def EV_maint_cost_coef(item):
        if item in list(maintenance_costs['Brand'].value_counts().keys()):
            return maintenance_costs['Average EV (€/km)'].iloc[maintenance_costs[maintenance_costs['Brand'] == item].index[0]]/10000
        else: return round(maintenance_costs['Average EV (€/km)'].mean()/10000,2)
        

    ############################DATA FROM GOOGLE SHEET DOCUMENTS##############################################

    #Code for GEV_BEEV data frame
    df_gev_beev = pd.read_csv("df_gev_beev2.csv")
    brand_choice = list(df_gev_beev['Brand'].unique())
    brand_choosen = st.selectbox("Select your GEV car's brand",brand_choice)
    model_choice = list(df_gev_beev['Model'][df_gev_beev['Brand'] == brand_choosen].unique())
    model_choosen = st.selectbox("Select your GEV car's model",model_choice)
    c1 = df_gev_beev['Brand'] == brand_choosen
    c2 = df_gev_beev['Model'] == model_choosen
    engine_choice = list(df_gev_beev['Modification (Engine)'][c1&c2].unique())
    engine_choosen = st.selectbox("Select your GEV car's engine",engine_choice)
    c3 = df_gev_beev['Modification (Engine)'] == engine_choosen
    GEV_carprice_choosen = st.slider('How much did you pay or are you planning to pay for your GEV car ?',10000, 100000, (15000),step=2500)
    price_slider = GEV_carprice_choosen
    EV_index = df_gev_beev['Category'][c1&c2&c3].index[0]
    GEV_car_category = df_gev_beev['Category'].iloc[df_gev_beev['Category'][c1&c2&c3].index[0]]
    GEV_car_possession = st.slider('How long do you plan on keeping your GEV car (in months) ?',1, 120, (12))
    duration_slider = GEV_car_possession
    GEV_car_km_slider = st.slider("How many Km per year do you think you'll be doing ?",1000, 100000, (10000),step=1000)
    km_slider = GEV_car_km_slider
    GEV_car_range = df_gev_beev['Range (km)'].iloc[df_gev_beev['Category'][c1&c2&c3].index[0]]
    
    #Adding calculated columns --->these have been removed to the gev_TCO because it was very slow to calculate over the whole DF
    #df_gev_beev['Malus (€)'] = df_gev_beev['CO2 emissions (g/km)'].dropna().apply(lambda item: malus_calculation(int(item)) if item != 'N/A' else 'N/A')
    #df_gev_beev['fuel_cost/100Km (€)'] = df_gev_beev[['Fuel Type','Fuel consumption - combined (l/100km)']].apply(lambda item: round(item[1]*petrol_price,2) if item[0] == 'Petrol (Gasoline)' else round(item[1]*diesel_price,2) if item[0] == 'Diesel' else 'nope', axis = 1)
    #df_gev_beev['maint_cost/100Km (€)'] = df_gev_beev['Brand'].apply(lambda item: maint_cost_coef(item)/10)

    
    #st.write(brand_choosen, model_choosen, engine_choosen, GEV_car_category, GEV_car_km_slider) 

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
    df_model['elec_cost/100Km (€)'] = df_model[['Range (Km)','Useable Battery Capacity']].apply(lambda item: (item[1]/item[0])*100*elec_price, axis = 1)
    #Building the categories for the choice in selectbox
    EV_car_categories = list(df['Category'].unique())
    EV_car_categories.insert(0,"ALL")
    EV_car_categories.insert(0,"Same as my GEV car")

    #DF Filtered
    df_filtered = df[['Full Name', 'Model', 'Brand','Range (km)','Battery Capacity (kW)', 'Useable Battery Capacity','Category','Government Incentive Category for Help','Vehicle Consumption (Wh)','Charging Time 7,4 kW','Charging Time 11 kW','Main Price']].copy()
    df_filtered['elec_cost/100Km (€)'] = df_filtered[['Range (km)','Useable Battery Capacity']].apply(lambda item: (item[1]/item[0])*100*elec_price, axis = 1)
    df_filtered['Price with Incentive'] = df_filtered['Main Price'].apply(lambda item: item - 6000)


    #st.title("Let's select together some parameters to calculate precisely the TCO")

    #Defining the selectbox
    label1 = "Select the category of the EV car you would like to have"
    category_choosen = st.selectbox(label1,EV_car_categories)
    if category_choosen == "Same as my GEV car":
        category_choosen = GEV_car_category
    else: category_choosen = category_choosen
    #st.write(category_choosen)

    #Defining the selectbox for the region ########### be careful need to add the DF and the regions variable before here
    label2 = "Select the region you are from"
    region_choosen = st.selectbox(label2,regions)

    #Defining the range selection for the EV car
    range_choice = st.radio(
         "Do you want your EV car range to be the same as your GEV car ?",
         ('Yes', 'No'))
    if range_choice == 'No':
        range_slider = st.slider('Select a desired range in Kilometers for the EV car',200, 800, (250),step=50)
    else: range_slider = GEV_car_range


    #Asking the user the Price and the Range
    # Add a slider to the sidebar:    
    #range_slider = st.sidebar.slider('Select a desired range in Kilometers',200, 800, (250),step=50)
    #price_slider = st.sidebar.slider('Select a desired price for the EV car',10000, 100000, (15000),step=2500)
    #duration_slider = st.sidebar.slider('Select a desired duration for leasing or keeping EV car in months',1, 72, (12))
    #km_slider = st.sidebar.slider('Select Km done per year',1000, 100000, (10000),step=1000)

    #Define the validation button
    if st.button('Get EV cars recommendation'):
        df_model.style.format({'Price (€)': '{:.0f}', 'Range (Km)': '{:.0f}', 'Price with Incentive (€)': '{:.0f}'})

        if category_choosen != "ALL":
            df_model = df_model[df_model['Category'] == category_choosen].copy()
            X = df_model[['Price (€)', 'Range (Km)']]
            distanceKNN_cars = NearestNeighbors(n_neighbors=5).fit(X)
            result = distanceKNN_cars.kneighbors([[price_slider,range_slider]], 5, return_distance = False)
            #st.write(
        else:   
            distanceKNN_cars = NearestNeighbors(n_neighbors=5).fit(df_model[['Price (€)', 'Range (Km)']])
            result = distanceKNN_cars.kneighbors([[price_slider,range_slider]], 5, return_distance = False)

        #st.write(df_model[['Full Name', 'Price (€)','Range (Km)','Category','Price with Incentive (€)']].iloc[result[0]].set_index('Full Name'))
        
        #Building the TCO for EV
        df_TCO = df_model[['Full Name', 'Price (€)','Range (Km)','Category','Price with Incentive (€)','elec_cost/100Km (€)']].iloc[result[0]]#.set_index('Full Name').copy()
        df_TCO['title_cost (€)'] = df_TCO['elec_cost/100Km (€)'].apply(lambda item: title_tax_cv[title_tax_cv['Region'] == region_choosen]['Title Cost (€ / CV)']*1)
        df_TCO['consumption_cost (month)'] = df_TCO['elec_cost/100Km (€)'].apply(lambda item: item/100*km_slider/12)
        #df_TCO['maintenance_cost (month)'] = df_TCO['elec_cost/100Km (€)'].apply(lambda item: km_slider/12*0.0208)
        df_TCO['maintenance_cost (month)'] = df_TCO['Full Name'].apply(lambda item: (EV_maint_cost_coef(item.split()[0]))*km_slider/12)#*0.0208)         #############
        df_TCO['TCO_month'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1] + item[2],axis=1)
        df_TCO['TCO_year'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1]*12 + item[2]*12,axis=1)
        df_TCO['TCO_duration'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1]*duration_slider + item[2]*duration_slider,axis=1)
        #Formating the result with choosen number (float)
        df_TCO.style.format({'Price (€)': '{:.0f}', 'Range (Km)': '{:.0f}', 'Price with Incentive (€)': '{:.0f}', 'elec_cost/100Km (€)':'{:.0f}','TCO_year':'{:.1f}', 'TCO_duration': '{:.1f}'})
        #Adding the title of the DF below
        st.title("Total Cost of Ownership for the recommended EV cars")
        result = df_TCO[['Full Name','Category','Range (Km)','Price with Incentive (€)','TCO_year','TCO_duration','title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].set_index('Full Name').copy()
        st.write(result)#df_TCO[['Full Name','Range (Km)','Category','Price with Incentive (€)','TCO_year','TCO_duration','title_cost (€)','consumption_cost (month)']].set_index('Full Name').copy()
        
        #Building the TCO for GEV
        df_gev_TCO = pd.DataFrame(df_gev_beev.iloc[EV_index]).T
        #Calculating columns for the TCO
        df_gev_TCO['Malus (€)'] = df_gev_TCO['CO2 emissions (g/km)'].dropna().apply(lambda item: malus_calculation(int(item)) if item != 'N/A' else 'N/A')
        df_gev_TCO['fuel_cost/100Km (€)'] = df_gev_TCO[['Fuel Type','Fuel consumption - combined (l/100km)']].apply(lambda item: round(item[1]*petrol_price,2) if item[0] == 'Petrol (Gasoline)' else round(item[1]*diesel_price,2) if item[0] == 'Diesel' else round(item[1]*petrol_price*0.8,2), axis = 1)
        df_gev_TCO['maint_cost/100Km (€)'] = df_gev_TCO['Brand'].apply(lambda item: maint_cost_coef(item)*100)
        df_gev_TCO['title_cost (€)'] = df_gev_TCO['CV'].apply(lambda item: title_tax_cv[title_tax_cv['Region'] == region_choosen]['Title Cost (€ / CV)']*item)
        
        df_gev_TCO['consumption_cost (month)'] = df_gev_TCO['fuel_cost/100Km (€)'].apply(lambda item: item/100*km_slider/12)
        #df_TCO['maintenance_cost (month)'] = df_TCO['elec_cost/100Km (€)'].apply(lambda item: km_slider/12*0.0208)
        df_gev_TCO['maintenance_cost (month)'] = df_gev_TCO['Brand'].apply(lambda item: (maint_cost_coef(item))*km_slider/12)
        df_gev_TCO['TCO_month'] = df_gev_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1] + item[2],axis=1)
        df_gev_TCO['TCO_year'] = df_gev_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)','Malus (€)']].apply(lambda item: item[0] + item[1]*12 + item[2]*12 + item[3],axis=1)
        df_gev_TCO['TCO_duration'] = df_gev_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)','Malus (€)']].apply(lambda item: item[0] + item[1]*duration_slider + item[2]*duration_slider + item[3],axis=1)
        df_gev_TCO['Price (€)'] = price_slider
        st.title("Total Cost of Ownership for your GEV car")
        df_gev_selected = df_gev_TCO[['Brand', 'Model', 'Modification (Engine)','Fuel Type','Category','Range (km)','Price (€)','Malus (€)','TCO_year','TCO_duration','consumption_cost (month)','maintenance_cost (month)','title_cost (€)']]#.iloc[EV_index]).T  #df_gev_TCO instead of beev thus pd.DataFrame( removed
        df_gev_selected.style.format({'Malus (€)': '{:.0f}', 'fuel_cost/100Km (€)': '{:.0f}', 'maint_cost/100Km (€)': '{:.0f}'})
        st.write(df_gev_selected)
        
        
    ############################################### SAVING THE RESULT ###################################################    
        #Defining the date to add in the files names
        today = datetime.datetime.now().strftime('%d-%m-%Y')
        #Defining the parameters selected before downloading
        parameters = pd.DataFrame({"Brand": df_gev_TCO['Brand'],"Model": df_gev_TCO['Model'],"Engine": df_gev_TCO['Modification (Engine)'],"car range(km) choosen": [range_slider], "price(€) choosen":[price_slider], "Duration(month) choosen":[duration_slider], "KM done per year":[km_slider],"car category selected":[category_choosen], "region selected": [region_choosen]})
        #Saving the result
        st.download_button(
             label="Download result as CSV",
             data=result.to_csv().encode('utf-8'),
             file_name='ev_car_recommendation_'+today+'.csv',
             mime='text/csv',
         )

        #Saving the parameters
        st.download_button(
             label="Download parameters as CSV",
             data=parameters.to_csv().encode('utf-8'),
             file_name='parameters_car_recommendation_'+today+'.csv',
             mime='text/csv',
         )  
        
        #Saving the GEV DataFrame with TCO costs
        st.download_button(
             label="Download GEV TCO as CSV",
             data=df_gev_selected.to_csv().encode('utf-8'),
             file_name='gev_car_TCO_'+today+'.csv',
             mime='text/csv',
         )    
    ############################################### SAVING THE RESULT ###################################################    
        
        
        ########################### Plotting the TCO comparison #####################
        chart_data = pd.DataFrame({"GEV": range(int(df_gev_TCO['Price (€)']),
                           int(df_gev_TCO['Price (€)'])+11*int(df_gev_TCO['TCO_year']),
                           int(df_gev_TCO['TCO_year'])),
              "EV": range(int(df_TCO['Price with Incentive (€)'].iloc[0]),
                          int(df_TCO['Price with Incentive (€)'].iloc[0])+11*int(df_TCO['TCO_year'].iloc[0]),
                          int(df_TCO['TCO_year'].iloc[0]))})
        st.title("TCO comparison between the first EV recommendation and your GEV car for 10 years duration")
        st.line_chart(chart_data)
        
        #st.write(sns.scatterplot(x=range(0,11) ,y=(range(int(df_gev_TCO['Price (€)']),int(df_gev_TCO['Price (€)'])+11*int(df_gev_TCO['TCO_year']),int(df_gev_TCO['TCO_year'])))))
        #st.write(sns.scatterplot(x=range(0,11) ,y=(range(int(df_TCO['Price with Incentive (€)'].iloc[0]),int(df_TCO['Price with Incentive (€)'].iloc[0])+11*int(df_TCO['TCO_year'].iloc[0]),int(df_TCO['TCO_year'].iloc[0])))))
