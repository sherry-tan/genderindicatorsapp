
# coding: utf-8

# In[54]:


import os
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.scatter import scatter_tab
from scripts.line import line_tab


# In[39]:


#path = os.getcwd()
file1 = "countrydata.csv"
file2 = "clusterdata.csv"
#filepath1  = os.path.join(path,'data',file1)
#filepath2  = os.path.join(path,'data',file2)
filepath1 = "data/"+file1
filepath2 = "data/"+file2

# In[40]:

countrydata = pd.read_csv(filepath1)
clusterdata = pd.read_csv(filepath2)

# In[41]:

#get scatterplot
tab1 = scatter_tab(countrydata)

#get line plot
tab2 = line_tab(clusterdata)

# display tabs in one doc
tabs = Tabs(tabs = [tab1, tab2])

curdoc().add_root(tabs)

