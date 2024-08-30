import time
from .plots import *
from tkinter import simpledialog, messagebox
from shapely.geometry import Point

'''This file contains all functions to navigate between the plots:
1) action_map pairs the keys of the buttons of each plot with functions
2) the definition of the functions are listed below the action map or are plot functions
   that are part of the class PlotManager
3) on_click connects the user clicking with the action map and enables line plots 
   for each country showing historic annual GHG emissions
4) the remaining functions are requests for user input and fail safes to catch invalid inputs'''

# Action map for all changes that are triggered by the textboxes on each figure
action_map = {
    'loc_start_plot': {
        'text1': ('Bar Plot Continental Emissions', lambda pm: ac_bar_new_year(pm)),
        'text2': ('Pie Plot Country Emissions', lambda pm: ac_pie_new_year(pm)),
        'text3': ('World-Heatmap of Emissions', lambda pm: ac_heatmap_new_year(pm)),
        'stay': ('stay', lambda pm: pm.start_figure()),
        'line_1': ("New countires can be added to the plot (on/off)", lambda pm: ac_line_add_to_fig(pm)),
        'line_2': ("New countries close the last line plot (on/off)", lambda pm: ac_line_close(pm)),

    },
    'loc_bar_plot': {
        'text1': ("Get back to the start", lambda pm: pm.start_figure()),
        'text2': ("Show a different year", lambda pm: ac_bar_new_year(pm)),
        'text3': ("Add a year", lambda pm: ac_bar_add_year(pm)),
        'text4': ("Sort years", lambda pm: ac_bar_sort_years(pm)),
        'stay': ('stay', lambda pm: pm.bar_contiental_emissions(pm.year_1)),
    },
    'loc_pie_plot': {
        'text1': ("Get back to the start", lambda pm: pm.start_figure()),
        'text2': ("Show a different year", lambda pm: ac_pie_new_year(pm)),
        'text3': ("Change cut off criteria", lambda pm: ac_pie_cut_off_criteria(pm)),
        'text4': ("Switch aggregation nat./cont.", lambda pm: ac_pie_aggregation(pm)),
        'stay': ('stay', lambda pm: pm.pie_plot(pm.year_1)),
    },
    'loc_heatmap_plot': {
        'text1': ("Get back to the start", lambda pm: pm.start_figure()),
        'text2': ("Show a different year", lambda pm: ac_heatmap_new_year(pm)),
        'text3': ("Switch heatmap <-> top polluters", lambda pm: ac_heatmap_aggregation(pm)),
        'text4': ("Change number of shown top poluters", lambda pm: ac_heatmap_num_top(pm)),
        'text5': ("Change between top polluters in the world or by continent", lambda pm: ac_heatmap_top_polluters_all_v_continent(pm)),
        'stay': ('stay', lambda pm: pm.world_heatmap(pm.year_1)),
        'line_1': ("New countires can be added to the plot (on/off)", lambda pm: ac_line_add_to_fig(pm)),
        'line_2': ("New countries close the last line plot (on/off)", lambda pm: ac_line_close(pm)),
    },
}

# select a year, check the input and call the bar plot function
def ac_bar_new_year(pm):
    year_add = check_year_in_range(pm)
    pm.year_1 = year_add
    pm.bar_contiental_emissions(year_add)

# select a year, check the input and call the pie plot function
def ac_pie_new_year(pm):
    year_add = check_year_in_range(pm)
    pm.year_1 = year_add
    pm.pie_plot(year_add)

# select a new year, check the input and call the heatmap plot function
def ac_heatmap_new_year(pm):
    year_add = check_year_in_range(pm)
    pm.year_1 = year_add
    pm.world_heatmap(year_add)

# select a year to add to the bar plot, check the input and call the bar plot function
def ac_bar_add_year(pm):
    year_add = check_year_in_range(pm)
    if isinstance(pm.year_1, int):
        pm.year_1 = [pm.year_1,year_add]
    else:
        pm.year_1.append(year_add)
    pm.bar_contiental_emissions(pm.year_1)

# sort the years of the bar plot from small to big
def ac_bar_sort_years(pm):
    pm.year_1.sort()
    pm.bar_contiental_emissions(pm.year_1)

# switch between aggregation by continent and nation in the pie plot
def ac_pie_aggregation(pm):  
    pm.switch_mode = "continent" if pm.switch_mode == "nation" else "nation"
    pm.pie_plot(pm.year_1)   

# change the data aggregation setting of the pie plot and create a new pie plot
def ac_pie_cut_off_criteria(pm):
    change_cut_off_criteria(pm)
    pm.pie_plot(pm.year_1)

# switch the heatmaps setting from heatmap to highlight only each continent's n top polluters and generate a new plot
def ac_heatmap_aggregation(pm):  
    pm.switch_mode_heatmap = "highlight" if pm.switch_mode_heatmap == "heatmap" else "heatmap"
    pm.world_heatmap(pm.year_1)

# change the number of n top polluters for the heatmap plot. If your currently at the heatmap it will automatically switch to showing the top polluters
def ac_heatmap_num_top(pm):
    check_num_top_in_range(pm)
    pm.switch_mode_heatmap = "highlight"
    pm.world_heatmap(pm.year_1)

# switches between highlighting the top polluters in the world or by continent
def ac_heatmap_top_polluters_all_v_continent(pm): 
    pm.switch_mode_top_polluters_all = True if pm.switch_mode_top_polluters_all == False else False
    pm.world_heatmap(pm.year_1)

# switches between adding to the line plot or creating a separat line plot of a nation's historic GHG emissions
def ac_line_add_to_fig(pm):
    pm.add_to_fig = True if pm.add_to_fig == False else False
    if  pm.add_to_fig == True and pm.close_fig==True:
        pm.close_fig = False
        messagebox.showinfo('Conflict',
                            "You chose to add the next country to your current plot. " 
                            "Therefore, the last line plot will not be closed.")

# switches between closing and not closing the last line plot of a nation's historic GHG emissions
def ac_line_close(pm):
    pm.close_fig = True if pm.close_fig == False else False
    if pm.close_fig == True and pm.add_to_fig == True:
        pm.add_to_fig = False
        messagebox.showinfo('Conflict',
                            "You chose to close the last line plot when plotting a new country. " 
                            "Therefore, the new country will plotted in a separat figure.")

'''This function handles all interactive actions.
1) It searches the action map based on the current location indicating which plot is visible
   and a key representing the clicked textbox/butto(e.g., text3).
2) On top it blocks interactive actions when zooming.
3) Finally it enables to get plots when clicking on countries shown in the starting figure and the heatmap'''
def on_click(pm, event):

    # When in zooming mode all interactive utilities that are implemented are blocked
    if event.canvas.toolbar.mode == 'zoom rect':        
        return

    # Being at the heatmap plot the user can click countries to get their historic emissions
    if pm.location == 'loc_heatmap_plot' or pm.location =='loc_start_plot':
        # Get the x, y coordinates of the click
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # Convert clicked coordinates to longitude and latitude
            #lon, lat = pm.ax.transData.inverted().transform((x, y))
            lon = x
            lat = y
            # Check if the click was inside a country shape
            found_country = False
            for index, row in pm.data.iterrows():
                if row['geometry'].contains(Point(lon, lat)):
                    found_country = True
                    pm.country_name = row['name']
                    break  # Break the loop after finding the clicked country

            if found_country:
                try:
                    if pm.emission_table[pm.country_name].empty:
                        messagebox.showerror("Error", f"There is no data on {pm.country_name}.")
                        return
                    pm.line_plot()
                except KeyError:
                    messagebox.showerror("Error", f"Data for {pm.country_name} was not found in the emission database.")
                return  # Return early if a country was clicked

    # Loop through text elements to determine if any were clicked
    for key, text_obj in pm.text_elements.items():
        if text_obj.contains(event)[0]:  # Check if the click is on this text object
            _, action = action_map[pm.location][key]  # Get the associated action

            if action:
                action(pm)  # Execute the action associated with the text
            break  # Only one action should be executed per click

'''This function asked the user to select a year for further assessment.
In addition invalid user inputs for the selected year are caught by fail safe fucntions'''
def check_year_in_range(pm):
    input = simpledialog.askstring("User-Input", "Please choose a year between 1960 and 2022")
    try: # in case the input is not a number
        year_add= int(input)
    except ValueError:
        if input is None: # stay at the current figure if the input was cancelled
            messagebox.showinfo(*pm.text_input_cancelled)
            action = action_map[pm.location]['stay']
            action(pm)
        else: # if it is not an int
            messagebox.showerror("Error","Your input was NOT an INTEGER between 1960 and 2022, please choose again") 
            return check_year_in_range(pm) #for invalid input returning the function again
    else:
        if year_add in range(1960,2023): # if it is not out of range
            return year_add
        else: # in case the input is not in the range of the data
            messagebox.showerror("Error","Your desired year was not between 1960 and 2022, please choose again")
            return check_year_in_range(pm) #for invalid input returning the function again

'''This function asks the user to select a number of top polluters that shall be highlighted for each continent.
In addition, some fail safes ensure handling of invalid inputs and input cancelation'''
def check_num_top_in_range(pm):
    input = simpledialog.askstring("User-Input", "How many top polluters do you want to see highlighted")
    try:
        pm.num_polluters = int(input)
    except:
        if input is None: # stay at the current figure if the input was cancelled
            messagebox.showinfo(*pm.text_input_cancelled)
            action = action_map[pm.location]['stay']
            action(pm)
        else:
            messagebox.showerror("Error","Please type in an INTEGER e.g., 3")
            return check_num_top_in_range(pm)

'''Wrapper for changing the criteria of the aggregation in the pie plot, so called cut off criteria'''
def change_cut_off_criteria(pm):
    figure = pm.ax.get_figure()  # Get the figure associated with the axes
    canvas = figure.canvas.get_tk_widget()  # Get the Tkinter widget associated with the figure
    pm.cut_off_limit = get_cutoff_limits(pm,
                                         "Choose X, e.g, 2.5 for 2.5%. Only slices bigger than X% will be explicitly shown, "
                                         "all others will be aggregated in rest. (In addition, in the next window you are going to " 
                                         "define the maximum amount of aggregated values.)",
                                         parent=canvas)
    pm.cut_off_sum_limit = get_cutoff_limits(pm,
                                             "Choose Y, e.g., 33 for 33%. The aggregated rest will be Y% at maximum."
                                             "This will overrule the previous criterium in case there are too many small values.", 
                                             parent=canvas)

'''User input and fail safe for changing the criteria of the aggregation in the pie plot'''
def get_cutoff_limits(pm, text, parent = None):
    input = simpledialog.askstring("User-Input", text, parent=parent)
    try:
        # Try to convert the input to an integer
        cut_off_limit = int(input)
    except:
        try:
            # If it fails, try to convert it to a float
            cut_off_limit = float(input)
        except:
            if input is None: # stay at the current figure if the input was cancelled
                messagebox.showinfo(*pm.text_input_cancelled)
                action = action_map[pm.location]['stay']
                action(pm)
            else: # If both conversions fail, raise an error or set a default value
                messagebox.showerror("Error","Please type in either an integer e.g., 5 or a float e.g., 5.2")
                return get_cutoff_limits(pm, text)
    if cut_off_limit < 0 or cut_off_limit > 100:
        messagebox.showerror("Error","Your input was smaller that 0 or bigger than 100, which makes no sense for a cut off")
        return get_cutoff_limits(pm, text)
    return cut_off_limit                           