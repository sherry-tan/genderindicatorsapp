
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import row, WidgetBox
from bokeh.models.widgets import Slider, Select, Div
from bokeh.models import Panel
from bokeh.models import Legend
from bokeh.palettes import Dark2_8

#define function to plot interactive scatterplot and update on user input
def scatter_tab(df):
    
    available_indicators = list(df.columns[2:-1])#exclude Country, Year, Region columns
    min_year = df['Year'].min()
    max_year = df['Year'].max()
      
    #create dataset based on inputs for plotting
    def create_dataset(data, x, y, year):
        
        source_list=[]
        color_palette = Dark2_8
        
        #set color dictionary mapping regions to colors
        colormap = {region:color_palette[i] for i,region in enumerate(data['Region'].unique())}
       
        #set colors for each row
        data['colors'] = [colormap[region] for region in data['Region']]
        data['line_colors'] = [colormap[region] for region in data['Region']]

        #set size for each row
        data['size'] = [4 for i in np.arange(0,len(data))]

        
        #use black line color for Singapore for visibility on plot
        data['line_colors'].loc[data['Country']=='Singapore'] = 'black'
        data['size'].loc[data['Country']=='Singapore'] = 6
        
        #subset data according to chosen year
        subset = data[data['Year']==year]
        
        #create list of data sources, each corresponding to a different region, for interactive legend
        for region in subset['Region'].unique(): 
            
            region_data = subset[subset['Region']==region]

            r_source = ColumnDataSource({
            'Country':region_data['Country'],
            'Region':region_data['Region'],
            'x':region_data[x],
            'y':region_data[y],
            'colors': region_data['colors'],
            'line_colors': region_data['line_colors'],
            'GNI': region_data['GNI per capita(current US$)'],
            'size':region_data['size']
            }
            )
            
            source_list.append(r_source)
       
        return source_list

    #create plot from dataset. sources for each region need to be explicitly specified for interactive legend
    def create_plot(s1,s2,s3,s4,s5,s6,s7,x,y,year):

        sources = [s1,s2,s3,s4,s5,s6,s7]
        
        #create plot figure
        p = figure(plot_width = 800, plot_height = 500, title = 'Gender indicators in {}'.format(year),
                   x_axis_label = x, y_axis_label = y, sizing_mode='scale_both',
                   toolbar_location="right")
        
        #set aesthetics
        p.title.text_font_size = '12pt'
        p.xaxis.axis_label_text_font_style = 'normal'
        p.yaxis.axis_label_text_font_style = 'normal'

        #loop over source list and plot glyphs for each region
        p1,p2,p3,p4,p5,p6,p7 = [p.circle('x', 'y', size = 'size', fill_color = 'colors', 
                                          line_color = 'line_colors',
                                          fill_alpha = 0.8, source=source) for source in sources]

        #create manual legend (necessary to place legend outside plot)
        regions = [s.data['Region'].unique().item() for s in sources] #extract region from each source
        plots = [p1,p2,p3,p4,p5,p6,p7]
        legenditems = [(region, [plot]) for region,plot in zip(regions,plots)] 
        
        #set legend location and aesthetics
        legend = Legend(items=legenditems,location=(10,0))
        p.add_layout(legend,"right")
        p.legend.label_text_font_size = '8pt'  
        
        #set interactivity mode for legend i.e. click on region to hide/show its data points
        p.legend.click_policy="hide"
        
        #add hovertool to show details for each data point
        hover = HoverTool(
            tooltips=[
                ("Country", "@Country"),
                ("Region", "@Region"),
                ("x:", "$x{0.1}"),
                ("y:", "$y{0.1}"),
                ("GNI per capita(US$)","@GNI")
            ]
        )

        p.add_tools(hover)
           
        return p

    #update function to update plots on change
    def update(attr, old, new):
        
        #get current values of inputs
        year = year_select.value
        x = x_select.value
        y = y_select.value
        
        #update sources
        new_src_list = create_dataset(df, x, y, year)
        s1.data,s2.data,s3.data,s4.data,s5.data,s6.data,s7.data = [new_src.data for new_src in new_src_list]
        
        #update labels and titles
        p.title.text = 'Gender indicators in {}'.format(year)
        p.xaxis.axis_label = x
        p.yaxis.axis_label = y
        
    #add a slider widget to select year
    year_select = Slider(start = min_year, end = max_year, step = 1, value = max_year, title = "Select Year")
    year_select.on_change('value', update)
    
    #add dropdown widgets to select indicators for y and x axes
    y_select = Select(title="Select indicator for y-axis", value=available_indicators[8], options=list(available_indicators))
    y_select.on_change('value',update)
    
    x_select = Select(title="Select indicator for x-axis", value=available_indicators[1], options=list(available_indicators))
    x_select.on_change('value',update)

    #set initial values to current widget values
    x = x_select.value
    y = y_select.value
    year = year_select.value
    
    #add a paragraph of explanatory text for user
    text = Div(text="""<font size="-1"><i>Click on legend to toggle data points on/off. <br />Data points for Singapore, where available, are outlined in black and appear as larger points.</i></font>""")

    #get initial dataset and plot
    s1,s2,s3,s4,s5,s6,s7 = create_dataset(df, x, y, year)
    p = create_plot(s1,s2,s3,s4,s5,s6,s7, x, y, year)

    #layout widgets and plot
    controls = WidgetBox(year_select, y_select, x_select, text, width = 400, sizing_mode='scale_both')
    layout = row(controls, p)

    tab = Panel(child=layout, title = 'Gender indicators')


    return tab
