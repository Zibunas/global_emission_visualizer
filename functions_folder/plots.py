import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
from tkinter import simpledialog, messagebox

'''This file contains all plot functions and corresponding data preporcessing
1) The initialization of the first figure activating the interactive nature of the tool (connection to def on_click)
2) The starting figure (a map of the world without any emission data shown
3) A bar plot for continental emissions
4) A pie plot for continental or national shares to the global emissions
5) A world map as heatmap for emissions with the posibility to higjlight each continents top polluters)'''

def init_figure(pm):
    #pm.fig = plt.figure(figsize=(19.2*6.5/10, (10.8-0.5)*5.5/10), dpi=100)
    pm.fig = plt.figure(figsize=(19.2*8/10, (10.8-0.5)*8/10), dpi=100)
    # Get the figure manager
    manager = plt.get_current_fig_manager()
    # Set the window position (x, y) on the screen
    manager.window.wm_geometry("+10+10") 
    pm.ax = pm.fig.add_subplot(111)  # '111' stands for 1x1 grid, first subplot
    pm.ax.set_facecolor((0.9, 0.9, 0.9))
    pm.fig.canvas.mpl_connect('button_press_event', lambda event: pm.on_click(event))

def start_figure(pm):
    pm.location = 'loc_start_plot'
    pm.fig.clear()
    pm.ax = pm.fig.add_subplot(111)
    
    pm.data.plot(column='continent', cmap='viridis', linewidth=1.2, ax=pm.ax, edgecolor='0',visible=True)
    
    # Add text boxes to enable navigation between plots and altering of settings for each plot
    pm.text_elements.clear() 
    pm.text_elements['text1'] = pm.ax.text(-175,12, "Bar Plot Continental Emissions",
                                           bbox=pm.bbox_properties,
                                           horizontalalignment='left',verticalalignment='center', rotation=0)
    pm.text_elements['text2'] = pm.ax.text(-175, 0, "Pie Plot Country Emissions",
                                           bbox=pm.bbox_properties,
                                           horizontalalignment='left',verticalalignment='center', rotation=0)
    pm.text_elements['text3'] = pm.ax.text(-175, -12, "World-Heatmap of Emissions",
                                           bbox=pm.bbox_properties,
                                           horizontalalignment='left',verticalalignment='center', rotation=0)
    
    # Plot limits
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    # Axis labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latidue')
    plt.title('Homescreen - Click on a country to see its GHG emissions history or choose another plot via the buttons on the left.')
    # Tight layout, so everything fits the figure size
    plt.tight_layout()
    # Show the plot
    plt.show(block=False)
    if pm.welcome:
        messagebox.showinfo("WELCOME to this GHG emission visualizer tool", f"Welcome to this interactive tool for exploring the history of global GHG emissions between 1960 and 2022. You can click on any country to explore its history of annual GHG emissions or you can click on the buttons on the left to explore other plots.\nHave fun. Best regards Christian!")
        pm.welcome = False
    plt.show()

def line_plot(pm):
    country_data = pm.data[pm.data['name'] == pm.country_name].iloc[0]
    country_data.index = pd.to_numeric(country_data.index, errors='coerce')
    filtered_data = country_data[country_data.index >= country_data.index.min()]

    if pm.add_to_fig: # If a figure already exists, use the current axis
        if hasattr(pm, 'fig_line') and pm.fig_line is not None and plt.fignum_exists(pm.fig_line.number):
            plt.figure(pm.fig_line.number)  # Activate the existing figure
            plt.sca(pm.ax_line)  # Set the current axis
        else:
            pm.fig_line = plt.figure()  # Create a new figure
            pm.ax_line = pm.fig_line.add_subplot(111)
            pm.fig_line.canvas.mpl_connect('button_press_event', lambda event: pm.on_click(event)) # connect user clicking for the new fig
            pm.min_line = 1000
            pm.max_line = 0

    elif pm.close_fig: # If a figure exists and it is specifyed by the user to close the last plot (not default) upon creating a new plot, generate new fig and ax
        plt.close(pm.fig_line) # close last line plot
        pm.fig_line = plt.figure()
        pm.ax_line = pm.fig_line.add_subplot(111)
        pm.fig_line.canvas.mpl_connect('button_press_event', lambda event: pm.on_click(event)) # connect user clicking for the new fig
    else:
        pm.fig_line = plt.figure() # If no figure exists or it is specifyed by the user to open a new plot (default), generate new fig and ax
        pm.ax_line = pm.fig_line.add_subplot(111)
        pm.fig_line.canvas.mpl_connect('button_press_event', lambda event: pm.on_click(event)) # connect user clicking for the new fig



    # Plot on the existing axis
    pm.ax_line.plot(filtered_data.index, filtered_data.values / 1000, marker='*', label=f'{pm.country_name}')
    pm.ax_line.set_xlabel('Years')
    pm.ax_line.set_ylabel('GHG emission in Gigatons per year')
    
    pm.ax_line.set_title(f'History of Annual GHG emissions.')

    # calculation to position the textboxes/buttons on the plot depending on the y data 
    if pm.add_to_fig:
        min_line = min(filtered_data.values/1000) # does not work if the line plot was closed
        # min_line = 0
        max_line = max(filtered_data.values/1000)
        pm.min_line = min(pm.min_line, min_line)
        pm.max_line = max(pm.max_line, max_line)
        for annotation in pm.ax_line.texts:
            annotation.remove()
        pm.fig_line.canvas.draw()
    else:
        pm.min_line = min(filtered_data.values/1000) # does not work if the line plot was closed
        #pm.min_line = 0
        pm.max_line = max(filtered_data.values/1000)
   

    y_positions = [(pm.max_line - pm.min_line)/10 * i + pm.min_line for i in [1,2]]

    # Add text boxes to enable navigation between plots and altering of settings for each plot
    pm.text_elements['line_1'] = pm.ax_line.text(2022, y_positions[0], "New countires can be added to the plot (on/off)", 
                                        bbox=pm.bbox_properties, 
                                        horizontalalignment='right',verticalalignment='center', rotation=0)

    pm.text_elements['line_2'] = pm.ax_line.text(2022, y_positions[1], "New countries close the last line plot (on/off)", 
                                        bbox=pm.bbox_properties,
                                        horizontalalignment='right',verticalalignment='center', rotation=0)
    
    plt.legend()
    plt.tight_layout()
    plt.show()

def bar_contiental_emissions(pm,year):
    pm.location = 'loc_bar_plot'
    world = pm.data

    # Ensure 'year' is a list
    if isinstance(year, int):
        year = [year]

    # Group by continent
    grouped_by_continent = world.groupby('continent')

    # Get the sum of emissions for each continent
    continent_emissions = grouped_by_continent[year].sum()

    # Plot the emissions for each continent
    pm.fig.clear()
    pm.ax = pm.fig.add_subplot(111)

    continent_emissions_Gt = continent_emissions/1000
    continent_emissions_Gt[(continent_emissions != 0).any(axis=1)].plot(kind='bar', legend=True, ax=pm.ax, cmap='viridis')
    plt.xlabel('Continent')
    plt.ylabel('Annual GHG emissions in Gigatons per year')
    # plt.title('Emissions by Continent in {}'.format(year))
    plt.title('Annual GHG emissions by continent in {}.'.format(', '.join(map(str, year))))
    plt.xticks(rotation=45)
    # Add text to the plot

    # Calculate the y positions based on the y-axis limits
    ylim = pm.ax.get_ylim()[1]
    y_positions = [ylim - (ylim * i) for i in [0.1, 0.2, 0.3, 0.4]]

    # Add text boxes to enable navigation between plots and altering of settings for each plot
    pm.text_elements.clear() 
    pm.text_elements['text1'] = pm.ax.text(-0.25, y_positions[0], "Get back to the start", 
                                        bbox=pm.bbox_properties, 
                                        horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text2'] = pm.ax.text(-0.25, y_positions[1], "Show a different year", 
                                        bbox=pm.bbox_properties,
                                        horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text3'] = pm.ax.text(-0.25, y_positions[2], "Add a year", 
                                        bbox=pm.bbox_properties, 
                                        horizontalalignment='left',verticalalignment='center', rotation=0)
    pm.text_elements['text4'] = pm.ax.text(-0.25, y_positions[3], "Sort years", 
                                        bbox=pm.bbox_properties, 
                                        horizontalalignment='left',verticalalignment='center', rotation=0)

    # Tight layout, so everything fits the figure size
    plt.tight_layout()
    # Show the plot
    plt.show()
    
def world_heatmap(pm,year): 
    pm.location = "loc_heatmap_plot"
    world = pm.data.copy()
    pm.text_elements.clear() 
    if pm.switch_mode_heatmap == "heatmap":
    
        # Plot the choropleth map
        pm.fig.clear()
        pm.ax = pm.fig.add_subplot(111)

        # Divide the values for the selected year by 1000
        world[year] = world[year] / 1000
        
        # Plot the choropleth map without the automatic colorbar (legend)
        plot_hm = world.plot(
            column=year, 
            cmap=plt.get_cmap('copper').reversed(), 
            linewidth=1.2, 
            ax=pm.ax, 
            edgecolor='0', 
            legend=False,  # Disable the automatic legend
            missing_kwds={
                "color": "0.6",
                "edgecolor": "black",
                "hatch": "x",
                "label": "Missing values"
            }
        )
            
        # Retrieve the colorbar instance
        cbar = plot_hm.get_figure().colorbar(plot_hm.collections[0], ax=pm.ax)

        # Set the label on the left side of the colorbar
        cbar.set_label(f"GHG emissions in {year} in Gigatons per year", rotation=90, labelpad=10)
        cbar.ax.yaxis.set_label_position('left')  # Move the label to the left

        plt.title(f"GHG emission heatmap in {year}.")

    
    elif pm.switch_mode_heatmap == "highlight" and pm.switch_mode_top_polluters_all:
        pm.fig.clear()
        pm.ax = pm.fig.add_subplot(111)
        # pm.ax.set_aspect('equal', 'box')
        # pm.ax.set_aspect('auto')

        # Identify the top polluters globally
        top_polluters_global = world.nlargest(pm.num_polluters, year)
        
        # Plot the map with countries colored by continent

        world.plot(column='continent', cmap='viridis', linewidth=1.2, ax=pm.ax, edgecolor='0')
        
        # Define the colors for the colormap & Create the colormap
        colors = [ (0.2, 0.2, 0.2), (0.7, 0.7, 0.7)] 
        custom_cmap = LinearSegmentedColormap.from_list('custom_gray', colors)

        # Assign colors to top polluters globally
        colors_assigned = custom_cmap(np.linspace(0, 1, len(top_polluters_global)))

        # Plot top polluters with assigned colors
        for i, (idx, country) in enumerate(top_polluters_global.iterrows()):
            world[world['name'] == country['name']].plot(ax=pm.ax, color=colors_assigned[i], edgecolor="darkred", linewidth=1.2)
            pm.ax.text(country.geometry.centroid.x, country.geometry.centroid.y, str(i + 1), fontsize=10, ha='center', va='center', color='white', fontweight='bold', path_effects=[path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])               

        plt.title(f"Top {pm.num_polluters} polluters of the world in {year}.")

        pm.text_elements['text5'] = pm.ax.text(-175, -30, "Top polluters in the world <-> by continent", 
                                            bbox=pm.bbox_properties, 
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    elif pm.switch_mode_heatmap == "highlight" and not pm.switch_mode_top_polluters_all:

        pm.fig.clear()
        pm.ax = pm.fig.add_subplot(111)
        # pm.ax.set_aspect('equal', 'box')
        pm.ax.set_aspect('auto')

        top_polluters = world.groupby('continent').apply(lambda x: x.nlargest(pm.num_polluters, 2008))
        # Plot the map with countries colored by continent

        world.plot(column='continent', cmap='viridis', linewidth=1.2, ax=pm.ax, edgecolor='0')
        
        # Define the colors for the colormap & Create the colormap
        colors = [ (0.2, 0.2, 0.2), (0.7, 0.7, 0.7)] 
        custom_cmap = LinearSegmentedColormap.from_list('custom_gray', colors)

        # Plot the top polluters with the generated shades of continent colors
        for _, continent_data in top_polluters.groupby(level=0): 
            # Sort the top polluters by emissions
            continent_data = continent_data.sort_values(by=year, ascending=False)
            
            # Assign colors to top polluters
            colors_assigned = custom_cmap(np.linspace(0, 1, len(continent_data)))
            
            # Plot top polluters with assigned colors
            for i, (idx, country) in enumerate(continent_data.iterrows()): # 
                world[world['name'] == country['name']].plot(ax=pm.ax, color=colors_assigned[i], edgecolor="darkred", linewidth=1.2)            
                pm.ax.text(country.geometry.centroid.x, country.geometry.centroid.y, str(i + 1), fontsize=10, ha='center', va='center', color='white',fontweight= 'bold',path_effects=[path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])

        plt.title(f"Top {pm.num_polluters} polluters of each continent in {year}.")

        pm.text_elements['text5'] = pm.ax.text(-175, -30, "Change between top polluters in the world or by continent", 
                                            bbox=pm.bbox_properties, 
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    # Add text to the plot
    pm.text_elements['text1'] = pm.ax.text(-175, 18, "Get back to the start", 
                                            bbox=pm.bbox_properties,
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text2'] = pm.ax.text(-175, 6, "Show a different year", 
                                            bbox=pm.bbox_properties,
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text3'] = pm.ax.text(-175, -6, "Switch heatmap <-> top polluters", 
                                            bbox=pm.bbox_properties, 
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text4'] = pm.ax.text(-175, -18, "Change number of highlighted top polluters", 
                                            bbox=pm.bbox_properties, 
                                            horizontalalignment='left',verticalalignment='center', rotation=0)
    
    pm.ax.set_facecolor((0.9, 0.9, 0.9))

    # Plot limits
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    # Axis labels
    plt.xlabel('Longitude')
    plt.ylabel('Latidue')
    # tight layout before the pop up windows otherwise it looks odd
    # Rescale the plot after everything is drawn
    pm.ax.set_aspect('auto')
    pm.ax.relim()  # Recalculate the limits
    pm.ax.autoscale_view()

    plt.tight_layout()

    if pm.first_heatmap == True and pm.switch_mode_heatmap == "heatmap":
        messagebox.showinfo("Information", "You can click on a country in the heatmap to see its historic annual emissions.")
        pm.first_heatmap = False
    elif pm.first_top_polluter == True and pm.switch_mode_heatmap == "highlight":
        messagebox.showinfo("Information", "Also when top polluters are highlighted, you can click on a country in the heatmap to see its historic annual emissions.")
        pm.first_top_polluter = False
    
    # Show the plot
    plt.show()

def pie_plot(pm,year):
    world=pm.data
    pm.location = 'loc_pie_plot'
    data = pm.emission_table
    if pm.switch_mode == "nation":
        data_local = data.copy()
    elif pm.switch_mode == "continent":     
        # Identify the year columns (assuming they are integers)
        year_columns = [col for col in world.columns if isinstance(col, int)]

        # Step 1: Group by continent and sum the emissions for each year
        grouped_by_continent = world.groupby('continent')[year_columns].sum()
        data_local = grouped_by_continent.T
    
    # Calculate percentages
    total = data_local.loc[year,:].sum()
    percentages = (data_local.loc[year,:] / total) * 100
    percentages = percentages.fillna(0)  
    cut_off_sum=0
    
    while cut_off_sum <= pm.cut_off_sum_limit and (percentages.drop('rest', errors='ignore').min() < pm.cut_off_limit):
        # Exclude the 'rest' column from the minimum search
        min_value = percentages.drop('rest', errors='ignore').min()
        min_index = percentages[percentages == min_value].index[0]
        
        # Check if adding the next min_value would exceed the cut_off_sum_limit
        if cut_off_sum + percentages[min_index] > pm.cut_off_sum_limit:
            break  # Exit the loop if it would exceed the limit

        # Update 'rest' column in data
        if 'rest' in data_local.columns:
            data_local.loc[year, 'rest'] += data_local.loc[year, min_index]
        else:
            data_local.loc[year, 'rest'] = data_local.loc[year, min_index]
        
        # Update 'rest' value in percentages
        if 'rest' in percentages.index:
            percentages['rest'] += percentages[min_index]
        else:
            percentages['rest'] = percentages[min_index]
        
        # Drop the minimum value column from data and percentages
        data_local.drop(columns=[min_index], inplace=True)
        percentages.drop(index=[min_index], inplace=True)
    
        # Update the smaller_than_5 variable
        cut_off_sum = percentages['rest']

    sorted_percentages = percentages[percentages.sort_values(ascending=False).index]

    # Specify the column you want to move to the end
    column_to_move = "rest"

    # Extract the column to be moved
    column_to_append = sorted_percentages.pop(column_to_move)

    # Append the extracted column to the DataFrame
    sorted_percentages[column_to_move] = column_to_append

    # Create a pie chart
    pm.fig.clear()
    pm.ax = pm.fig.add_subplot(111)

    cmap = plt.get_cmap("viridis")
    colors1 = cmap(np.linspace(0, 1, len(sorted_percentages.index)))

    # Create a pie chart
    # fig, ax = plt.subplots()
    pm.ax.pie(sorted_percentages, labels=sorted_percentages.index, autopct='%1.1f%%', colors=colors1,
           textprops={'fontsize': 8, 'fontweight': 'bold'},  # autopct text properties
    labeldistance=1.1  # distance of labels from the center
    )

    plt.title(f'Emissions distribution by {pm.switch_mode} in {year}.\n In this year the total emissions were about {int(total/1000)} Gigatons.')
    
    # Add text boxes to enable navigation between plots and altering of settings for each plot
    pm.text_elements.clear() 
    pm.text_elements['text1'] = pm.ax.text(0, 0.21, "Get back to the start", 
                                       bbox=pm.bbox_properties,
                                       horizontalalignment='center',verticalalignment='center', rotation=0)

    pm.text_elements['text2'] = pm.ax.text(0, 0.07, "Show a different year", 
                                       bbox=pm.bbox_properties,
                                       horizontalalignment='center',verticalalignment='center', rotation=0)

    pm.text_elements['text3'] = pm.ax.text(0, -0.07, "Change cut off criteria", 
                                       bbox=pm.bbox_properties,
                                       horizontalalignment='center',verticalalignment='center', rotation=0)

    pm.text_elements['text4'] = pm.ax.text(0, -0.21, "Switch aggregation nat./cont.", 
                                        bbox=pm.bbox_properties,
                                        horizontalalignment='center',verticalalignment='center', rotation=0)

    plt.tight_layout()
    plt.show()
