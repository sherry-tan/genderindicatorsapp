
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import row, WidgetBox
from bokeh.models.widgets import Select, CheckboxGroup, Div
from bokeh.models import Range1d, Panel
from bokeh.models.glyphs import MultiLine
from bokeh.palettes import Category20_12


def line_tab(df):
    
    cluster_indicators = df.columns[2:-1] 
    clusters = df['Country'].unique()
    
    #define function to create data set for plotting
    def create_dataset(data, indicator, selected_clusters):

        color_palette = Category20_12
        
        #set color dictionary mapping regions to colors
        colormap = {cluster:color_palette[i] for i,cluster in enumerate(data['Country'].unique())}

        #subset data by selected clusters
        subset = data[data['Country'].isin(selected_clusters)]

        #create datasource for plotting points
        source_point = ColumnDataSource({
        'year':subset['Year'],
        'cluster':subset['Country'],
        'value':subset[indicator], #values for selected indicator
        'colors': [colormap[cluster] for cluster in subset['Country']]
         }
        )

            #create datasource for plotting lines. for multiple line plotting, data source has to be a list of lists, each list being data points for each group
        xs = []
        ys = []
        colors = []
        for cluster in subset['Country'].unique():
            df_cluster = subset[subset['Country']==cluster]
            xs.append(list(df_cluster['Year']))
            ys.append(list(df_cluster[indicator])) 
            colors.append(colormap[cluster])

        source_line = ColumnDataSource({
        'year':xs,
        'value':ys,
        'cluster':list(subset['Country'].unique()),
        'colors':colors}
        )
        return source_point,source_line

    #define function to plot interactive line charts
    def create_plot(source_pt, source_line, y):

        #create plot figure
        p = figure(plot_width = 800, plot_height = 500, title = y,
                   x_axis_label = 'Year', y_axis_label = y, sizing_mode = 'scale_both')

        #plot lines
        p.multi_line('year', 'value', line_width = 1, color = 'colors', source=source_line, 
                    legend = 'cluster')
        
        #plot points
        p.circle('year', 'value', size = 3, fill_color = 'white', line_color = 'colors',
                 source=source_pt)

        #set plot aesthetics
        p.legend.label_text_font_size = '8pt'
        p.x_range = Range1d(2001, 2030)
        p.xaxis.minor_tick_line_color = None
        p.xgrid.grid_line_color = None
        p.title.text_font_size = '12pt'
        p.xaxis.axis_label_text_font_style = 'normal'
        p.yaxis.axis_label_text_font_style = 'normal'
        
        #add hovertool to show details for each data point
        hover = HoverTool(
            tooltips=[
                ("Cluster: ", "@cluster"),
                ("Value:", "$y{1.1}"),
            ])
        p.add_tools(hover)

        return p

    #update plot on user input
    def update(attr, old, new):

        #get current values of inputs
        y = y_select.value
        selected_clusters = [cluster_selection.labels[i] for i in  cluster_selection.active]
       
        #update sources
        new_source_pt,new_source_line = create_dataset(df, y,selected_clusters)
        source_pt.data = new_source_pt.data 
        source_line.data = new_source_line.data

        #update labels and titles
        p.title.text = y
        p.yaxis.axis_label = y
     
    #add selection widget
    y_select = Select(title="Select indicator", value=cluster_indicators[3], options=list(cluster_indicators))
    y_select.on_change('value',update)
    
    #add explanatory text for checkbox group
    text = Div(text="""Select cluster""")
    
    #add selection widget
    cluster_selection = CheckboxGroup(labels = list(clusters), active=[11]) 
    cluster_selection.on_change('active',update)
   
    #set initial values to current widget values
    y = y_select.value
    selected_clusters = [cluster_selection.labels[i] for i in cluster_selection.active]
    
    #get initial dataset and plot
    source_pt,source_line = create_dataset(df, y,selected_clusters)
    p = create_plot(source_pt, source_line, y)
    
    #layout widgets and plot
    controls = WidgetBox(y_select, text, cluster_selection, width = 400, sizing_mode='scale_both')
    layout = row(controls, p)

    tab = Panel(child=layout, title = 'Trends')

    return tab
