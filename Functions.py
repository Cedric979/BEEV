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
#Calculating the taxes for the CO2 emission
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


