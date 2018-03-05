
# coding: utf-8

# In[36]:


import piexif #for accessing EXIF information from a image
from geopy.distance import vincenty #For calculating the distance between a Latitude longitude pair
from datetime import datetime #For converting a string to Datatime object for easier manipulation
import pandas as pd #For manipulating dataframes
import os #For accessing the images 
import glob #For manipulating file names
import numpy as np #For manipulating arrays


# In[9]:


get_float = lambda x: float(x[0]) / float(x[1])

def convert_to_degrees(value):
    
    #Formula: degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    return get_float(value[0]) + (get_float(value[1]) / 60.0) + (get_float(value[2]) / 3600.0)

def get_lat_lon(info):
    
    try:
        gps_latitude = info[2]
        gps_latitude_ref = info[1]
        gps_longitude = info[4]
        gps_longitude_ref =info[3]
        lat = convert_to_degrees(gps_latitude)
        if gps_latitude_ref != "N":
            lat *= -1

        lon = convert_to_degrees(gps_longitude)
        if gps_longitude_ref != "E":
            lon *= -1
        return lon, lat
    
    except KeyError:
        
        return None


# In[32]:


def get_images_range(df,Range):
    
    for index in range(0,len(inputfile)): #iterating thorugh all the lat long pairs in the video SRT file

        image_list=[]

        if len(glob.glob('images\*.JPG'))!=0: #iterating through all JPG files in images folder

            for filename in glob.iglob('images\*.JPG'):

                try:
                    
                    if vincenty(get_lat_lon(piexif.load(filename)['GPS']),(inputfile['longitude'][index],inputfile['latitude'][index])).meters<Range:#using vincety's formulae to calculate distance(for more precision vs. Great ciricle distance)
                        
                        image_list.append(os.path.basename(filename)) #appending each image name which satisfies the range criteria

                except:
                    print "file has no GPS data"

        df.assest_name[index]=inputfile['asset_name'][index] #appending to dataframe
        df.Images[index]=image_list

    df.to_csv("POI_results.csv")
    
    print "Process completed, check POI_results.csv"


# In[38]:


video_file_input= raw_input("Enter assets file name(.csv)[For the given task, enter assests.csv]: ")

inputfile = pd.read_csv("assets.csv",'r',delimiter=',')

df = pd.DataFrame(np.nan,index=range(0,len(inputfile)),columns=['assest_name','Images']) #Creating a dataFrame

Range=input("Enter range in meters[For the given task, enter 50]:")

get_images_range(df,Range)

