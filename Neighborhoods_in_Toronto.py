#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# ## PART 1 scrape data and create dataframe

# In[1]:


#import libraries
import pandas as pd
import numpy as np
get_ipython().system('pip install lxml')


# In[4]:


#import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[5]:


#scrape data from wiki page
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
html_doc = urlopen(url)
soup = BeautifulSoup(html_doc, 'lxml')


# In[7]:


table = soup.find("table", class_="wikitable")

toronto_data = []
for items in table.find_all("tr")[:-1]:
    data = [' '.join(item.text.split()) for item in items.find_all(['th','td'])]
    
    toronto_data.append(data)
    
toronto_data


# In[10]:


#create dataframe with column names
df = pd.DataFrame(toronto_data, columns=['Postcode', 'Borough', 'Neighbourhoud'])
df.drop(0, axis=0, inplace=True)
df.head()


# In[11]:


#droping rows with Not assigned values
indexNames = df[ (df['Borough'] == 'Not assigned')].index
df.drop(indexNames , inplace=True)
df = df.reset_index(drop=True)
df.head()


# In[13]:


#print the number of rows of the dataframe
df.shape


# In[14]:


#If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.
#Replacing Not assigned cells with their values in Borough
df['Neighbourhoud']=df['Borough'].where(df['Neighbourhoud'].eq('Not assigned'),df['Neighbourhoud'])
df


# In[16]:


#rows will be combined into one row with the neighborhoods separated with a comma
df_stack = df.groupby('Postcode')['Neighbourhoud'].apply(', '.join)
df_stack = df_stack.reset_index()
df_stack


# In[21]:


#Merging df and df_stack
df_new = pd.merge(df_stack, df, on='Postcode', how='right')
df_new = df_new.drop_duplicates()
df_new


# In[22]:


#renaming, deleting Neighbourhoud_y column, rearrangements and dropping duplicates
df_new=df_new.drop('Neighbourhoud_y',axis=1)
column=['Postcode', 'Borough', 'Neighbourhoud_x']
df_new=df_new[column]
df_new = df_new.rename(columns={"Neighbourhoud_x": "Neighbourhoud"}).reset_index(drop=True)
df_new = df_new[['Postcode', 'Borough', 'Neighbourhoud']].drop_duplicates()
df_new


# In[23]:


df_new.shape


# ## PART TWO add location data

# In[24]:


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
get_ipython().system('conda install -c conda-forge geopy --yes')
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans
import requests
import json
from pandas.io.json import json_normalize

import matplotlib.cm as cm
import matplotlib.colors as colors
print('done')


# In[25]:


import urllib.request
url = 'http://cocl.us/Geospatial_data'
filename = 'geospatial_coordinates.csv'
urllib.request.urlretrieve(url, filename)


# In[26]:


df_coordinates = pd.read_csv(filename)
df_coordinates


# In[27]:


df_data = pd.merge(df_coordinates, df_new, left_on='Postal Code', right_on='Postcode')

df_data = df_data[['Postcode', 'Borough', 'Neighbourhoud', 'Latitude', 'Longitude']]

df_data


# ## PART 3 TORONTO Map

# In[28]:


place = 'Toronto'
geolocator = Nominatim(user_agent="explorer")
location = geolocator.geocode(place)
latitude = location.latitude
longitude = location.longitude
print('The coordinates of Tornoto: {}, {}.'.format(latitude, longitude))


# In[34]:


# create map of toronto
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)
for lat, lng, postalcode, borough, neighborhood in zip(df_data['Latitude'], df_data['Longitude'], df_data['Postcode'], df_data['Borough'], df_data['Neighbourhoud']):
    label = '{}; {}; {}'.format(postalcode, borough, neighborhood)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[33]:


df_data.loc[4, 'Neighbourhoud']


# In[35]:


neighbourhood_latitude = df_data.loc[4, 'Latitude'] 
neighbourhood_longitude = df_data.loc[4, 'Longitude']

neighbourhood_name = df_data.loc[4, 'Neighbourhoud'] 

print('Latitude and longitude of {}: {}, {}.'.format(neighbourhood_name, 
                                                               neighbourhood_latitude, 
                                                               neighbourhood_longitude))


# In[ ]:




