
# coding: utf-8

# In[54]:


import os
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.transform import subset_data
from scripts.scatter import scatter_tab
from scripts.line import line_tab


# In[39]:


path = os.getcwd()
file1 = "Gender_StatsEXCEL.xlsx"
file2 = "CLASS.xls"
filepath1  = os.path.join(path,'data',file1)
filepath2  = os.path.join(path,'data',file2)


# In[40]:


data1 = pd.read_excel(filepath1, sheet_name=0)
data2 = pd.read_excel(filepath2, sheet_name=0, skiprows=4, usecols = [2,5,6])


# In[41]:


data2.dropna(axis=0, inplace=True) #extract only rows that contain country-region pairs for mapping with data1 
data2=data2.iloc[1:] #drop blank first row


# In[42]:


countries = data2['Economy'].unique()
regions= data2['Region'].unique()
incomes = data2['Income group'].unique()
regions_incomes = np.append(regions, incomes)
regions_incomes = np.append(regions_incomes, "World")


# In[43]:


def dropcols(data, threshold):

    columns_to_drop = data.columns[(data.isnull().sum()/len(data)) > threshold]

    return data.drop(columns_to_drop, axis=1)


# In[44]:


# get country gender data for plotting by subsetting 
start = 2012
end = 2017
country_data = subset_data(data1,countries,start,end)

#map countries to geographical region (to facilitate scatterplot analysis), drop redundant columns
country_data = country_data.merge(data2[['Economy','Region']], how='left', left_on = 'Country', right_on = "Economy")
country_data.drop('Economy', inplace=True, axis=1) 

#fill NA values and sort by region (so the legend in plot is alphabetical)
#define new dataframe country_data_m for filled table
country_data_m = country_data.groupby('Country').apply(lambda x:x.fillna(method='pad')) 
country_data_m.sort_values(by='Region', inplace=True)

# Drop indicators for which there are still many NaNs despite forward filling. 
# Indicators with more than 50% NaN values are dropped as they will be less useful for scatterplots
threshold = 0.5
country_data_m = dropcols(country_data_m, threshold)


# In[45]:


# get cluster data by subsetting
start = 2001
end = 2017
cluster_data = subset_data(data1, regions_incomes, start, end)

#drop indicators with more than 20% NaN values
threshold = 0.2
cluster_data = dropcols(cluster_data, threshold)


# In[55]:

#get scatterplot
tab1 = scatter_tab(country_data_m)

#get line plot
tab2 = line_tab(cluster_data)

# display tabs in one doc
tabs = Tabs(tabs = [tab1, tab2])

curdoc().add_root(tabs)

