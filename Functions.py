# %%
from Libraries import *

# %% [markdown]
# ## **Interfaces**

# %% [markdown]
# ### Interface 1 

# %%
#Building the Data for maintenance_costs. We divide it by 10000 because we had too many 0's
def maint_cost_coef(item, path_list):
    maintenance_costs = pd.read_csv(path_list[-8])
    if item in list(maintenance_costs['Brand'].value_counts().keys()):
        return maintenance_costs['Average Gas engine (€/km)'].iloc[maintenance_costs[maintenance_costs['Brand'] == item].index[0]]/10000
    else: return round(maintenance_costs['Average Gas engine (€/km)'].mean()/10000,2)
        
##For the EV cars
def EV_maint_cost_coef(item, path_list):
    maintenance_costs = pd.read_csv(path_list[-8])
    if item in list(maintenance_costs['Brand'].value_counts().keys()):
        return maintenance_costs['Average EV (€/km)'].iloc[maintenance_costs[maintenance_costs['Brand'] == item].index[0]]/10000
    else: return round(maintenance_costs['Average EV (€/km)'].mean()/10000,2)

# %% [markdown]
# ### Interface 2

# %%
#Calculating the taxes for the CO2 emission
def malus_calculation(item):
    bonus_malus = pd.read_csv('bonus_malus_db')
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


