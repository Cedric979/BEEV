from Libraries import *
from Functions import maint_cost_coef, EV_maint_cost_coef, load_df
def app():
    #Condition to access the updating button
    password = st.text_input('If you want to update the data with the google sheet documents please enter the password', max_chars=10)
    if password == 'Semra':
        ############################ loadind & Saving the DATA FROM GOOGLE SHEET DOCUMENTS #####################
        #Adding a button to the sidebar to be able to manually actualize the data from the googlesheet files
        if st.button("Click here to update"):
            load_df()   
            
      ############################ loadind & Saving the DATA FROM GOOGLE SHEET DOCUMENTS##################################
   
    #Loading BEEV image
    image = Image.open('BEEV_image.png')
    st.image(image)
    #Application title
    st.title("Manual features selection for EV car")

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

    ############################DATA FROM GOOGLE SHEET DOCUMENTS##############################################
    #Building the Data for fuel prices and elec price for next calculation
    fuel_prices = pd.read_csv('fuel_prices_db')
    elec_price = float(fuel_prices[fuel_prices['Fuel type'] == 'Electricity']['Price France (€/litres) - KWh'])
    #Building the list of regions for the selectbox
    title_tax_cv = pd.read_csv('title_tax_cv_db')
    regions = list(title_tax_cv['Region'].unique())
    #Building the Data for maintenance_costs
    maintenance_costs = pd.read_csv('maintenance_costs_db')
    
    ############################DATA FROM GOOGLE SHEET DOCUMENTS##############################################

    #Code for EV DF
    df = pd.read_csv("Beev Electric Vehicle Specs Data.csv")
    df['Main Price'].fillna(62000.0, inplace = True)
    df['Range (km)'].fillna(235.0, inplace = True)
    df_model = pd.DataFrame(zip(df['Full Name'],df['Main Price'],df['Range (km)'], df['Category'],df['Useable Battery Capacity']))
    df_model.rename(columns = {0:'Full Name', 1:'Price (€)',2:'Range (Km)',3:'Category',4:'Useable Battery Capacity'}, inplace = True)
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

    #Defining the selectbox
    label1 = "Select the category of the car you would like"
    category_choosen = st.selectbox(label1,categories)
    #Defining the selectbox for the region ########### be careful need to add the DF and the regions variable before here
    label2 = "Select the region you are living in"
    region_choosen = st.selectbox(label2,regions)
 
    #Asking the user the Price and the Range
    # Add a slider to the sidebar:    
    range_slider = st.slider('Select a desired range (Kilometers that can be done with full charge)',200, 800, (250),step=50)
    price_slider = st.slider('How much are you planning to pay for your EV car ?',10000, 100000, (15000),step=2500)
    duration_slider = st.slider('How long do you plan on keeping your EV car (in months) ?',1, 120, (12))
    km_slider = st.slider("How many Km per year do you think you'll be doing ?",1000, 100000, (10000),step=1000)

    #Define the validation button
    if st.button('Get EV Cars recommendation'):
        df_model.style.format({'Price (€)': '{:.0f}', 'Range (Km)': '{:.0f}', 'Price with Incentive (€)': '{:.0f}'})

        if category_choosen != "ALL":
            df_model = df_model[df_model['Category'] == category_choosen].copy()
            X = df_model[['Price (€)', 'Range (Km)']]
            distanceKNN_cars = NearestNeighbors(n_neighbors=5).fit(X)
            result = distanceKNN_cars.kneighbors([[price_slider,range_slider]], 5, return_distance = False)
            
        else:   
            distanceKNN_cars = NearestNeighbors(n_neighbors=5).fit(df_model[['Price (€)', 'Range (Km)']])
            result = distanceKNN_cars.kneighbors([[price_slider,range_slider]], 5, return_distance = False)

        #Building the TCO
        df_TCO = df_model[['Full Name', 'Price (€)','Range (Km)','Category','Price with Incentive (€)','cost/100Km (€)']].iloc[result[0]]#.set_index('Full Name').copy()
        df_TCO['title_cost (€)'] = df_TCO['cost/100Km (€)'].apply(lambda item: title_tax_cv[title_tax_cv['Region'] == region_choosen]['Title Cost (€ / CV)']*1)
        df_TCO['consumption_cost (month)'] = df_TCO['cost/100Km (€)'].apply(lambda item: item/100*km_slider/12)
        df_TCO['maintenance_cost (month)'] = df_TCO['Full Name'].apply(lambda item: (EV_maint_cost_coef(item.split()[0]))*km_slider/12)#*0.0208)
        df_TCO['TCO_month'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1] + item[2],axis=1)
        df_TCO['TCO_year'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1]*12 + item[2]*12,axis=1)
        df_TCO['TCO_duration'] = df_TCO[['title_cost (€)','consumption_cost (month)','maintenance_cost (month)']].apply(lambda item: item[0] + item[1]*duration_slider + item[2]*duration_slider,axis=1)
        #Formating the result with choosen number (float)
        df_TCO.style.format({'Price (€)': '{:.0f}', 'Range (Km)': '{:.0f}', 'Price with Incentive (€)': '{:.0f}', 'cost/100Km (€)':'{:.0f}','TCO_year':'{:.1f}', 'TCO_duration': '{:.1f}'})
        result = df_TCO[['Full Name','Range (Km)','Category','Price with Incentive (€)','TCO_year','TCO_duration']].set_index('Full Name').copy()
        st.write(result)#df_TCO[['Range (Km)','Category','Price with Incentive (€)','TCO_year','TCO_duration']])


    ############################################### SAVING THE RESULT ###################################################    
        #Defining the date to add in the files names
        today = datetime.datetime.now().strftime('%d-%m-%Y')
        #Defining the parameters selected before downloading
        parameters = pd.DataFrame({"car range(km) choosen": [range_slider], "price(€) choosen":[price_slider], "Duration(month) choosen":[duration_slider], "KM done per year":[km_slider],"car category selected":[category_choosen], "region selected": [region_choosen]})
        #Saving the result
        st.download_button(
             label="Download result as CSV",
             data=result.to_csv(sep = ';').encode('utf-8'),
             file_name='ev_car_recommendation_'+today+'.csv',
             mime='text/csv',
         )

        #Saving the parameters
        st.download_button(
             label="Download parameters as CSV",
             data=parameters.to_csv(sep = ';').encode('utf-8'),
             file_name='parameters_car_recommendation_'+today+'.csv',
             mime='text/csv',
         )    
    ############################################### SAVING THE RESULT ###################################################    


