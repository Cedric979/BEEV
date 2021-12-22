# BEEV
Beev_project
The project consist in recommending an EV car based on specified features like Range, category and price.
This project has been built with jupiter notebook, visual studio and streamlit
The following librairies have been used and are mandatory to be installed.



#LIBRARIES
#data processing
import pandas as pd 
#Graphics
import matplotlib.pyplot as plt
import seaborn as sns
#KNeighbors
from sklearn.neighbors import NearestNeighbors
#Importing librairy to manage access to google spreadsheets
import gspread
#Building the interface
import streamlit as st
#Web Scrapping
from bs4 import BeautifulSoup

For this project we based some calculation on values provided by the client like:
price of fuel
price of electricity
table with values to calculate the bonus malus of EV or GEV cars
the formula to calculate the TCO
The data for GEV cars have been scrapped on websites provided by the client because it satisfyied their needs
## For all these googlesheet, all the columns must have a name and all float values must be with a point and not a comma.
When updating these files, the values will be updated if we re-run the code.
