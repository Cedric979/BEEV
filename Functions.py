# %% [markdown]
# ## **Web Scraping**

# %%
#Function to get the models inside each brand
from Libraries import *
bonus_malus = pd.read_csv('bonus_malus_db')
bonus_malus['Malus (€)'] = bonus_malus['Malus (€)'].apply(lambda item: item.replace(' ','') if type(item) == str else item)
bonus_malus['Malus (€)'] = bonus_malus['Malus (€)'].astype(int)
def model_of_each_brand(brand_url):
    models_list = []
    html2 = requests.get(brand_url, headers={'User-Agent': navigator})
    soup2 = BeautifulSoup(html2.text, 'html.parser')
    models = soup2.find_all('a', {'class' : 'modeli'}) 
    models_list_final = re.findall('en/(\S+)', str(models))
    return [x[:-1] for x in models_list_final]


#Creating function to scrap the generation names for each models
def generation_of_each_model(model_url):
    gens_list = []
    html3 = requests.get(model_url, headers={'User-Agent': navigator})
    soup3 = BeautifulSoup(html3.text, 'html.parser')
    gens = soup3.find_all('a', {'class' : 'position'}) 
    gens_list_final = re.findall('en/(\S+)', str(gens))
    return [x[:-1] for x in gens_list_final]

#Creating a function to scrap for the modifications of each generation
def modifications_of_each_generation(gen_url):
    mods_list = []
    html4 = requests.get(gen_url, headers={'User-Agent': navigator})
    soup4 = BeautifulSoup(html4.text, 'html.parser')
    mods = soup4.find_all('table', {'class' : 'carlist'}) 
    gens_list_final = re.findall('en/(\S+)', str(mods))


#Getting the specifications for each car
def specifications_of_each_car(mods_url):
    if mods_url[-3:] == 'nan':
        return pd.DataFrame()
    else:
        specs = pd.read_html(mods_url)
        if len(specs)>=2:
            i=1
        elif len(specs)==1:
            return specs[0].drop_duplicates().T.reset_index(drop =True)
        else:
            return pd.DataFrame()
        specs = specs[i].drop_duplicates()
        specs.rename(columns = {'General information' : ''}, inplace = True)
        specs.set_index([''], inplace = True)
        return specs.T.reset_index(drop =True)

# %% [markdown]
# ## **Final dataframe**

# %%
#Getting the standard/norm part of the CO2
def co2_grab(dfserie):
    return " ".join(dfserie.name.split()[2:])


#Function to split the CO2 values that have extra characters
def split_bin(value):
    if value.find('-') != -1:
        value = value.split('-')
        value[0] = float(value[0])
        if len(value[1])>1:
            value[1] = float(value[1])
        else: value[1] = float(value[0])
        return value
    elif value.find('+') != -1:
        value = value.split('+')
        value[0] = float(value[0])
        value[1] = float(value[1])
        return value
    else: return value
    
#Function to split the fuel values that have extra characters
def basic_split_bin(value):
    if value.find('-') != -1:
        value = value.split('-')
        if len(value[1])==0:
            value[1] = value[0]
        return value
    elif value.find('+') != -1:
        value = value.split('+')
        return value
    else: return value

#Getting only the standard(norm) used to calculate the fuel
def norm_fuel_grab(dfserie):
    return " ".join(dfserie.name.split()[3:]).replace('-','').rstrip().lstrip()

#Removing the combined word in fuel
def fuel_clean(dfserie):
    return " ".join(dfserie.split()[0:1]).replace('combined','')


# Fixing the weird values in the data
def fixpoints(item):
    if type(item) == str:
        item = item.replace('..', '.')
        item = item.split()[0]
        if len(item)> 5 and item.count('.')==2:
            item = item.split('.')[0]+'.'+item.split('.')[1][0]+ "-"+item.split('.')[1][1:]+'.'+item.split('.')[2]
            return item
    return item


### Function to get rid of list values and make them all float for fuel consumption
def remove_list_fuel(value):
    if type(value) == list:
        if len(value) == 1 or '' in value:
            value = value[0]
            return float(value)
        elif len(value) == 2:
            return(sum([float(x)/2 for x in value]))
    else:
        return float(value)


### Remove list values and make them float for tank capacity
def remove_list_tank(item):
    if type(item) == list:
        if len(item) == 2:
            return(sum([float(x)/2 for x in item]))
    else:
        return float(item)


### Function to convert every value in CO2 emissions column to float
def float_co2(value):
    if type(value) == str and value != 'N/A' and value!="LEV3":
        return(float(value))
    elif value == 'LEV3':
        return 'N/A'
    else:
        return value 


## Function to convert the categories
def category_conversion(item):
    for keys in dicto_gev.keys():
        if item == keys:
            return dicto_cat[dicto_gev[keys]]

# %% [markdown]
# ## **Interfaces**

# %% [markdown]
# ### Interface 1 

# %%
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

# %% [markdown]
# ### Interface 2

# %%
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

### Updating the values from the google sheet documents and replacing the DF used in the code    
#List of url to read
url_dico = {'fuel_prices': 'https://docs.google.com/spreadsheets/d/1M_e1ENe40v-G_HYYH7YTZT5yPMoxgk36FFNamtg12f8/edit?usp=sharing',
           'title_tax_cv': "https://docs.google.com/spreadsheets/d/1cOj98R9fGT89rG4-TxAPIgOrvDbrzxlLPd4Y5mUBD0g/edit?usp=sharing",
           'bonus_malus': "https://docs.google.com/spreadsheets/d/1RDIMbTGE3TBU4SXbRNKiqKQFakf0grVGKKLfu9L9dS4/edit?usp=sharing",
           'maintenance_costs': "https://docs.google.com/spreadsheets/d/1Hlhp4ubS-JFgYYx1S9oeL5A_011sSxvKzWiuS3bLqV8/edit?usp=sharing"}

gc = gspread.service_account(filename='../../Wild_Code_School/keys/beev-335814-edfca510cf50.json')#The json key has to be defined by a google account in google API platform accessible here 'https://console.developers.google.com/'
def load_df(url_dico = url_dico):
    for key, url in url_dico.items():
        sht1 = gc.open_by_url(url)
        worksheet = sht1.sheet1
        name = key
        name = pd.DataFrame(worksheet.get_all_records())
        name.to_csv(key+'_db',header=True, index=False)

