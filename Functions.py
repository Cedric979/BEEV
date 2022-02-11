# %%
from Libraries import *

# %% [markdown]
# ## **Interfaces**

# %% [markdown]
# ### Interface 1 

# %%
#Building the Data for maintenance_costs. We divide it by 10000 because we had too many 0's
url_dico = {'fuel_prices': "https://docs.google.com/spreadsheets/d/1M_e1ENe40v-G_HYYH7YTZT5yPMoxgk36FFNamtg12f8/edit?usp=sharing",
           'title_tax_cv': "https://docs.google.com/spreadsheets/d/1cOj98R9fGT89rG4-TxAPIgOrvDbrzxlLPd4Y5mUBD0g/edit?usp=sharing",
           'bonus_malus': "https://docs.google.com/spreadsheets/d/1RDIMbTGE3TBU4SXbRNKiqKQFakf0grVGKKLfu9L9dS4/edit?usp=sharing",
           'maintenance_costs': "https://docs.google.com/spreadsheets/d/1Hlhp4ubS-JFgYYx1S9oeL5A_011sSxvKzWiuS3bLqV8/edit?usp=sharing"}
def load_df(url_dico = url_dico):
    gc = gspread.service_account('app/beev-341010-50a2328de8c9.json')#The json key has to be defined by a google account in google API
    for key, url in url_dico.items():
        sht1 = gc.open_by_url(url)
        worksheet = sht1.sheet1
        name = key
        name = pd.DataFrame(worksheet.get_all_records())
        name.to_csv(key+'_db',header=True, index=False)

def maint_cost_coef(item):
    maintenance_costs = pd.read_csv('./app/maintenance_costs_db')
    if item in list(maintenance_costs['Brand'].value_counts().keys()):
        return maintenance_costs['Average Gas engine (€/km)'].iloc[maintenance_costs[maintenance_costs['Brand'] == item].index[0]]/10000
    else: return round(maintenance_costs['Average Gas engine (€/km)'].mean()/10000,2)
        
##For the EV cars
def EV_maint_cost_coef(item):
    maintenance_costs = pd.read_csv('./app/maintenance_costs_db')
    if item in list(maintenance_costs['Brand'].value_counts().keys()):
        return maintenance_costs['Average EV (€/km)'].iloc[maintenance_costs[maintenance_costs['Brand'] == item].index[0]]/10000
    else: return round(maintenance_costs['Average EV (€/km)'].mean()/10000,2)

# %% [markdown]
# ### Interface 2

# %%
#Calculating the taxes for the CO2 emission
def malus_calculation(item):
    bonus_malus = pd.read_csv('./app/bonus_malus_db')
    bonus_malus['Malus (€)'] = bonus_malus['Malus (€)'].apply(lambda item: item.replace(' ','') if type(item) == str else item)
    bonus_malus['Malus (€)'] = bonus_malus['Malus (€)'].astype(int)
    malus = 0
    if item < bonus_malus['g / km'].min():
        malus = 0
    elif item > bonus_malus['g / km'].max():
        malus = bonus_malus['Malus (€)'].max()
    else :
        malus_index = bonus_malus['Malus (€)'][bonus_malus['g / km'] == item].index[0]       
        malus = bonus_malus['Malus (€)'].iloc[malus_index]
    return malus


