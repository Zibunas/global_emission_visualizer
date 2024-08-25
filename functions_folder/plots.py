import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
from tkinter import simpledialog, messagebox

'''This file contains all plot functions and corresponding data preporcessing'''

def init_figure(pm):
    pm.fig = plt.figure(figsize=(19*14/19, 10.8*14/19))
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
    plt.title('Homescreen - Click on a country to see its history of annual emissions or choose anoter plot by clicking the buttons on the left.')
    # Tight layout, so everything fits the figure size
    # plt.tight_layout(rect=[0, 0.1, 1, 1])
    plt.tight_layout()
    # Show the plot
    plt.show(block=False)
    if pm.welcome:
        messagebox.showinfo("Information", f"Welcome to this iteractive tool for exploring the history of global GHG emissions between 1960 and 2022.\nYou can click any country to explore its history of annual GHG emissions or you can click the buttons on the left to explore other plots.\nHave fun. Best regards Christian!")
        pm.welcome = False
    plt.show()

def line_plot(pm):
    country_data = pm.data[pm.data['name'] == pm.country_name].iloc[0]
    country_data.index = pd.to_numeric(country_data.index, errors='coerce')
    filtered_data = country_data[country_data.index >= country_data.index.min()]

    if pm.add_to_fig:
        # If a figure already exists, use the current axis
        plt.figure(pm.fig_line.number)
        plt.sca(pm.ax_line)

    elif pm.close_fig:
        plt.close(pm.fig_line)
        pm.fig_line = plt.figure()
        pm.ax_line = pm.fig_line.add_subplot(111)
        pm.fig_line.canvas.mpl_connect('button_press_event', lambda event: pm.on_click(event))
    else:
        pm.fig_line = plt.figure()
        pm.ax_line = pm.fig_line.add_subplot(111)
        pm.fig_line.canvas.mpl_connect('button_press_event', lambda event: pm.on_click(event))


    # Plot on the existing axis
    pm.ax_line.plot(filtered_data.index, filtered_data.values / 1000, marker='*', label=f'{pm.country_name}')
    pm.ax_line.set_xlabel('Years')
    pm.ax_line.set_ylabel('GHG emission in Gigatons per year')
    pm.ax_line.set_title(f'History of Annual GHG emissions of {pm.country_name}.')

    if pm.add_to_fig:
        min_line = min(filtered_data.values/1000)
        max_line = max(filtered_data.values/1000)
        pm.min_line = min(pm.min_line, min_line)
        pm.max_line = max(pm.max_line, max_line)
        for annotation in pm.ax_line.texts:
            annotation.remove()
        pm.fig_line.canvas.draw()
    else:
        pm.min_line = min(filtered_data.values/1000)
        pm.max_line = max(filtered_data.values/1000)

    # Add text boxes to enable navigation between plots and altering of settings for each plot
    y_positions = [(pm.max_line - pm.min_line)/10 * i + pm.min_line for i in [1,2]]
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
    plt.title('Annual emissions by continent in {}.'.format(', '.join(map(str, year))))
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
    
def world_heatmap (pm,year): # TDi leerzeichen zwischen funktionsnamen und klammern geht zwar da der python das automatisch entfernt, aber würd ich nicht empfehlen :D 
    print(pm.switch_mode_heatmap)
    pm.location = "loc_heatmap_plot"
    world = pm.data
    if pm.switch_mode_heatmap == "heatmap": # TDi variblenname ist hier nicht so sprechend
    
        # Plot the choropleth map
        pm.fig.clear()
        pm.ax = pm.fig.add_subplot(111)
        # fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        plot_hm = world.plot(column=year, cmap=plt.get_cmap('autumn').reversed(), linewidth=1.2, ax=pm.ax, edgecolor='0', legend=True,missing_kwds={
            "color": "0.6",
            "edgecolor": "black",
            "hatch": "x",
            "label": "Missing values"})
        
        # cbar = plot_hm.get_legend().get_colorbar()
        # cbar.set_label('GHG emissions in Gigatons per year')
        
        plt.title(f"Emission heatmap in {year}. Click on a country to see its history of annual emissions.")

    elif pm.switch_mode_heatmap == "highlight":

        top_polluters = world.groupby('continent').apply(lambda x: x.nlargest(pm.num_polluters, 2008))
        # Plot the map with countries colored by continent
        pm.fig.clear()
        pm.ax = pm.fig.add_subplot(111)
        world.plot(column='continent', cmap='viridis', linewidth=1.2, ax=pm.ax, edgecolor='0')
        
        # Define the colors for the colormap
        colors = [ (0.2, 0.2, 0.2), (0.7, 0.7, 0.7)] 
        # Create the colormap
        custom_cmap = LinearSegmentedColormap.from_list('custom_gray', colors)

        # Plot the top polluters with the generated shades of continent colors
        # Iterate over continents
        for continent, continent_data in top_polluters.groupby(level=0): # TDi wenn du den continent nicht brauchst kannst du auch ein "_" schreiben, also for _, continent_data in top_polluters.groupby(level=0):. Das macht dann direkt klar dass du den wert nicht brauchst.
            # Sort the top polluters by emissions
            continent_data = continent_data.sort_values(by=year, ascending=False)
            
            # Assign colors to top polluters
            colors_assigned = custom_cmap(np.linspace(0, 1, len(continent_data)))
            
            # Plot top polluters with assigned colors
            for i, (idx, country) in enumerate(continent_data.iterrows()): # TDi same as above mit idx
                world[world['name'] == country['name']].plot(ax=pm.ax, color=colors_assigned[i], edgecolor="darkred", linewidth=1.2)            
                pm.ax.text(country.geometry.centroid.x, country.geometry.centroid.y, str(i + 1), fontsize=10, ha='center', va='center', color='white',fontweight= 'bold',path_effects=[path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])

        plt.title(f"Top {pm.num_polluters} polluters of each continent in {year}. Click on a country to see its history of annual emissions.")

    # Add text to the plot
    pm.text_elements.clear() 
    pm.text_elements['text1'] = pm.ax.text(-175, 18, "Get back to the start", 
                                            bbox=pm.bbox_properties,
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text2'] = pm.ax.text(-175, 6, "Show a different year", 
                                            bbox=pm.bbox_properties,
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text3'] = pm.ax.text(-175, -6, "Switch heatmap <-> top polluters", 
                                            bbox=pm.bbox_properties, 
                                            horizontalalignment='left',verticalalignment='center', rotation=0)

    pm.text_elements['text4'] = pm.ax.text(-175, -18, "Change number of shown top polluters", 
                                            bbox=pm.bbox_properties, 
                                            horizontalalignment='left',verticalalignment='center', rotation=0)
    pm.ax.set_facecolor((0.9, 0.9, 0.9))
    # Set the limits of the plot
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)  # Adjusted to match the y-axis range
    plt.xlabel('Longitude')
    plt.ylabel('Latidue')
    plt.tight_layout()
    
    if pm.first_heatmap == True and pm.switch_mode_heatmap == "heatmap":
        messagebox.showinfo("Information", "You can click on a country in the heatmap to see its historic annual emissions.")
        pm.first_heatmap = False
    elif pm.first_top_polluter == True and pm.switch_mode_heatmap == "highlight":
        messagebox.showinfo("Information", "Also when top polluters are highlighted, you can click on a country in the heatmap to see its historic annual emissions.")
        pm.first_top_polluter = False
    # Tight layout, so everything fits the figure size
    
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
    # TDi könnte acuh eine eigene funktion sein wenn dus schon so variabel machen willst
    column_to_move = "rest"

    # Extract the column to be moved
    column_to_append = sorted_percentages.pop(column_to_move)

    # Append the extracted column to the DataFrame
    sorted_percentages[column_to_move] = column_to_append

    # Create a pie chart
    pm.fig.clear()
    pm.ax = pm.fig.add_subplot(111)
    # fig.canvas.mpl_connect('button_press_event', on_click)
    # plt.pie(sorted_percentages, labels=sorted_percentages.index,fontsize=7, autopct='%1.1f%%')
    # Generate colors from the viridis colormap
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
