# Project scope
Electric vehicles have been on a rising trend and more and more people and car manifacturers are adhering to it. However, it is not always an easy process to purchase or pick the electric car that better fits a person's needs.
As such, Beev (our client) acts as a one-stop shop for EV cars, facilitating the process for both individual customers but also for manufacturer's fleet managers.

There are potential customers that would like to change their car or fleet of Gas engine vehicles to the better EV alternative, as well as getting some information about charging stations.
For Beev, this is still a somewhat lenghty process for the sales times, and as such, they would like to be quicker in estimating the total costs of the full transition and ownership, as they had no tools for it.

The requirement was then to create a predictive model to help the customer make the final leap to the electric car and to help fleet managers make the best decision regarding the replacement of their fleet, based on several parameters. We also were asked to calculate and compare the Total Cost of Ownership between GEV and EV cars.

The client provided us with:
- Electrical vehicle database
- Fuel prices
- Title tax for each French region
- CO2 emission tax values
- Government incentives

What we needed to find:
- Gas vehicle database
- French CV (Chevaux Vapeur) values
- Gas car prices



In order to fullfill the requirements we found for a way to get the GEV data. We scraped the data from an automobile website and built a dataframe with it
This allowed us to create the interface with the prediction model that does a recommendation of the best EV cars to replace your GEV as well as calculate and compare the Total Cost of Ownership of each


For the completion of this project we used the following tools:

-Python (for coding)
-Streamlit (to build the interface)
-Github (to easily share the folders and files)
-Docker (to deploy the app and send it to the client, so they don't have to install code-related programs)


NOTICE: For all these googlesheet, all the columns must have a name and all float values must be with a point and not a comma.
When updating these files, the values will be automatically updated in the solution if we re-run the code.

Created by : Alexandre Gomes and Cédric Pinel
