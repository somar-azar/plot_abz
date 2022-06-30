#!/usr/bin/env python
# coding: utf-8

# In[7]:


get_ipython().run_line_magic('matplotlib', 'inline')
#%matplotlib widget
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
from ipywidgets import interact, interactive, fixed, interact_manual, Button
import ipywidgets as widgets
from IPython.display import display, Javascript
import math



#import list of files
file_list = ['data/{0}'.format(f) for f in listdir("data") if isfile(join("data", f))]

#plotting function
def plotter(data_range, x, y, units_x, units_y, grid_x_spacing, grid_y_spacing):
    global fig1
    plt.rcParams["font.family"] = "Arial"
    fig1 = plt.figure(figsize=(8/2.52, 6/2.52))
    x_plot = data_array[x][:data_range]
    y_plot = data_array[y][:data_range]
    plt.plot(x_plot, y_plot, color='black',linewidth=1
            )
    x_label = r'$\mathbf{DD1}$' + r" $\mathbf{{[{0}]}}$".format(units_x)
    y_label = r'$\mathbf{Spannung}$ $\mathbf{\sigma}$'  + r" $\mathbf{{[{0}]}}$".format(units_y)
    plt.xlabel(x_label, fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.grid(visible='Yes', which='major', axis='both', color='black')
    plt.xlim([0,None])
    plt.xticks(np.arange(0, max(x_plot)+grid_x_spacing/2, grid_x_spacing))
    #plt.xticks(fontsize=13)
    plt.ylim([0,None])
    plt.yticks(np.arange(0, max(y_plot)+grid_y_spacing/2, grid_y_spacing))
    #plt.yticks(fontsize=13)
    plt.show()
    
def import_data(f, c_sect):
    global data_array 
    global headers
    #import data array to be plotted
    data_array = pd.read_table(f,skiprows=[1], delimiter=';', decimal=',')

    #import headers of data
    headers = pd.read_csv(f, nrows=1, delimiter=';').columns.tolist()

    #move force to origin point
    data_array['Kraft'] = data_array['Kraft'] - data_array['Kraft'][0]

    #add stress according to cross section
    data_array['Spannung'] = 1000*data_array['Kraft']/c_sect
    
    headers.append('Spannung')
    

    plot_min = math.floor(0.1*len(data_array))
    plot_max = math.floor(len(data_array))
    plot_def = math.floor(0.7*len(data_array))
    plot_step = math.floor(0.01*len(data_array))

    interact(plotter, data_range=widgets.IntSlider(min=plot_min, max=plot_max, step=plot_step, value=plot_def, style = style),
         x=widgets.Dropdown(options=headers, value=headers[3], style = style),
         y=widgets.Dropdown(options=headers, value=headers[-1], style = style),
         units_x = widgets.Text(value='‰', description='x units', style = style),
         units_y = widgets.Text(value='MPa', description='y units', style = style),
         grid_x_spacing = widgets.FloatText(value=2, description='grid x spacing', style = style),
         grid_y_spacing = widgets.FloatText(value=500, description='grid y spacing', style = style, step=250)
        ) 
    
    return(data_array)
    return(headers)
    
#widgets text style
style = {'description_width': 'initial'}
    
interact(import_data,
         f=widgets.Dropdown(options=file_list, value = file_list[1],style = style),
         c_sect=widgets.FloatText(value=3.62, description='fiber cross section', style = style)
        )

def save_fig_button(t):
    fig1.savefig("test.png", dpi=1200, bbox_inches = 
                'tight')


button = Button(description="Savefig")
display(button)

button.on_click(save_fig_button)


# In[ ]:






