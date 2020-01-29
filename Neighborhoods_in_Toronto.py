#!/usr/bin/env python
# coding: utf-8

# ## Segmenting and Clustering Neighborhoods in Toronto

# In[1]:


import pandas as pd
import numpy as np
get_ipython().system('pip install lxml')


# In[2]:


df=pd.read_html('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M', header=None)
df


# In[ ]:




