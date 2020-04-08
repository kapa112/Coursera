#!/usr/bin/env python
# coding: utf-8

# CAPSTONE PROJECT

# In[206]:


#Importing libraries

import requests
from bs4 import BeautifulSoup
import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

#!conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

#!conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab
import folium # map rendering library


# In[207]:


#Scraping the Wikipedia using BeautifulSoup

res = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0] 
df = pd.read_html(str(table))
df = df[0]

#Checking whether it looks ok after scraping
df.head()


# In[208]:


#Getting rid of Not assigned Neighberhoods
df = df.set_index("Borough")
df = df.drop("Not assigned", axis=0)
df = df.reset_index()
columns_titles = ["Postal code","Borough","Neighborhood"]
df=df.reindex(columns=columns_titles)

#Replacing '/' with ',' in the neighborhood column
df['Neighborhood'] = df['Neighborhood'].str.replace(' /', ',')

#Sortking by postal code
df.sort_values('Postal code', axis = 0, ascending = True, inplace = True)

#Checking whether the data looks ok
df.head()


# In[209]:


#Dimenasions of the dataframe

df.shape


# In[210]:


#Reading the file with coordinates
geo = pd.read_csv('http://cocl.us/Geospatial_data')
geo.sort_values('Postal Code', axis = 0, ascending = True, inplace = True)
geo.head()


# In[211]:


#Adding coordinates to dataframe
df['Latitude'] = geo['Latitude']
df['Longitude'] = geo['Longitude']
df.head()


# In[212]:


#Sorting the values by index
df=df.sort_index()
df.head()


# In[213]:


#We replicate the same analysis as on NY data

#First we get coordinates of Toronto

address = 'Canada, Toronto'

geolocator = Nominatim(user_agent="to_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[215]:


# create map of Toronto using latitude and longitude values
neighborhoods = df
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(neighborhoods['Latitude'], neighborhoods['Longitude'], neighborhoods['Borough'], neighborhoods['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
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


# In[ ]:




