import pandas as pd
import geopandas as gpd
from functions_folder.plot_class import *

'''MAIN SCRIPT:
This is the main script of a tool to visualize and interactively explore the history of GHG emission for each nation. 
The main script consists of the following steps:
1) import the historic GHG emissions of the world by country
2) merge the emission data with data for the nations' shapes to later plot maps
3) create a PlotManager object containing essential variables for the tool
4) start the tool by creating the starting figure'''

# Path to your Excel file
excel_file_path = "./data_sources/export_emissions.xlsx"

# Read the Excel file into a pandas DataFrame
emission_table  = pd.read_excel(excel_file_path, index_col=0)

# Load the world shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the emissions data for the selected year with the world DataFrame based on country names
world = world.merge(emission_table .transpose(), how='left', left_on='name', right_index=True)

manager = PlotManager(world,emission_table) #create a PlotManager object containing essential variables for the tool
manager.init_figure() #creates a figure and connects a navigation function to the user clicking on the figure
manager.start_figure() #creates the first plot to start with




