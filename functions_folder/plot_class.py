from .plots import *
from .utilities import on_click

'''This file contains the class definition of PlotManager
The class is used to carry information from plot to plot, e.g., the fig and ax so that the window size remains constant
when switching between different plots.
The classes plot functions refer to functions from the file plots. Thereby the class defintion becomes simpler'''

class PlotManager:
    def __init__(self,data,emission_table):
        self.fig = None
        self.ax = None
        self.location = None
        self.text_elements = {}
        self.data = data
        self.emission_table = emission_table
        self.bbox_properties = dict(facecolor=(87/255, 171/255, 39/255), edgecolor='black', boxstyle='round,pad=0.5')
        self.switch_mode_heatmap = "heatmap"
        self.num_polluters = 2
        self.first_heatmap = True
        self.first_top_polluter = True
        self.switch_mode= "nation"
        self.cut_off_sum_limit = 33
        self.cut_off_limit = 2
        self.is_zooming = False
        self.welcome = True
        self.year_1 = []
        self.text_input_cancelled= ("Cancelled", "You cancelled the input. Please choose a new action.")
        self.add_to_fig = False
        self.close_fig = False
 
    def init_figure(self):
        init_figure(self)  # Use the imported function

    def start_figure(self):
        start_figure(self)  # Use the imported function

    def bar_contiental_emissions(self,year):
        bar_contiental_emissions(self,year)

    def pie_plot(self,year):
        pie_plot(self,year)

    def world_heatmap (self,year):
        world_heatmap (self,year)

    def line_plot(self):
        line_plot(self)
    
    def on_click(self,event):
        on_click(self,event)  # Use the imported function


