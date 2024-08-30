from .plots import *
from .utilities import on_click


'''This file contains the class definition of PlotManager
1 ) The class is used to carry information from plot to plot, e.g.,
    the fig and ax so that the window size remains constant when switching between different plots.
    or default values for some parameters
2) The classes plot functions refer to functions from the file plots. Thereby the class defintion is more concise'''


class PlotManager:
    def __init__(self,data,emission_table):
        self.fig = None
        self.ax = None
        self.location = None # which plot is currently open --> helps navigating
        self.text_elements = {} # for the textboxes which deal as buttons for navigation
        self.data = data # full data set of geomtry data and emission data
        self.emission_table = emission_table # emission data with countries and years 
        self.bbox_properties = dict(facecolor=(87/255, 171/255, 39/255), edgecolor='black', boxstyle='round,pad=0.5')
        self.switch_mode_heatmap = "heatmap" # to switch between the classical heatmap and highlighting of each continents top polluters
        self.num_polluters = 10 # default value of top polluters
        self.highlight_color = (255/255, 141/255, 27/255) # color for highlights in the heatmap
        self.welcome = True #to check if this is the first visit of the starting figure for a pop up window
        self.first_heatmap = True  #to check if this is the first visit of the heatmap for a pop up window
        self.first_line_plot = True  #to check if this is the first line plot for a pop up window
        self.first_top_polluter = True #to check if this is the first visit of the top polluters plot for a pop up window
        self.switch_mode= "nation" # to switch between aggregation by nation or continents in the pie plot
        self.cut_off_sum_limit = 33 # in %, maximum amout of cut off values (aggregation to 'rest') in the pie plot; this setting can overrule the cut_off_limit
        self.cut_off_limit = 2 # in %, minimum share to global emissions (otherwise aggregated to 'rest') in the pie plot
        self.is_zooming = False # deacivates buttons when zooming
        self.year_1 = [] # stores the years that shall be visualized 
        self.text_input_cancelled= ("Cancelled", "You cancelled the input. Please choose a new action.") # text for pop up window after a user closed a window for user input
        self.add_to_fig = True # whether a line plot is added to the previous or put into a new figure
        self.close_fig = False # whether or not the last line plot is closed
        self.switch_mode_top_polluters_all = True #highlight top polluters in the world or of each continent
 
    def init_figure(self):
        init_figure(self)  # Use the imported function

    def start_figure(self):
        start_figure(self)  # Use the imported function

    def bar_contiental_emissions(self,year):
        bar_contiental_emissions(self,year) # Use the imported function

    def pie_plot(self,year):
        pie_plot(self,year) # Use the imported function

    def world_heatmap (self,year):
        world_heatmap (self,year) # Use the imported function

    def line_plot(self):
        line_plot(self) # Use the imported function
    
    def on_click(self,event):
        on_click(self,event)  # Use the imported function
