
# coding: utf-8

# In[4]:


import piexif #for accessing EXIF information from a image
from geopy.distance import vincenty #For calculating the distance between a Latitude longitude pair
from datetime import datetime #For converting a string to Datatime object for easier manipulation
import pandas as pd #For manipulating dataframes
import os #For accessing the images 
import glob #For manipulating file names
import numpy as np 


# In[5]:


'''The following function returns Latitude and Longitude from the the EXIF information obtained from a image
The EXIF['GPS'] data looks like this:

{0: (2, 3, 0, 0),                       GPS tag version
 1: 'N',                                North or South Latitude GPSLatitudeRef
 2: ((19, 1), (9, 1), (188978, 10000)), GPSLatitude
 3: 'E',                                East or west Longitude GPSLongitudeRef
 4: ((73, 1), (0, 1), (191383, 10000)), GPSLongitude
 5: 0,                                  Altitude Reference
 6: (63739, 1000)}                      GPSAltitude
 
 '''

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


# In[16]:


'''This function takes two arguments: 
    1.df: dataFrame to populate the data 
    2. Range (in meters): list of all the images that lie within 35 metres(Range) of the drone position 
    
    It returns a CSV file with  First column, time in seconds. Second column, all the images that lie within Range.
'''
def get_images_range(df,Range):
    
    for index in range(0,len(inputfile)): #iterating thorugh all the lat long pairs in the video SRT file

        image_list=[]

        if len(glob.glob('images\*.JPG'))!=0: #iterating through all JPG files in images folder

            for filename in glob.iglob('images\*.JPG'):

                try:
                    image_lat_long=get_lat_lon(piexif.load(filename)['GPS']) #using piexif to obtain the lat long pair
                    video_lat_long=(inputfile['Longitude'][index],inputfile['Latitude'][index]) #lat long pair from the SRT file
                    
                    if vincenty(image_lat_long,video_lat_long).meters<Range:#using vincety's formulae to calculate distance(for more precision vs. Great ciricle distance)
                        
                        image_list.append(os.path.basename(filename)) #appending each image name which satisfies the range criteria
                    

                except:
                    print "no GPS data"

        df.Time[index]=inputfile['TimeStamp'][index].second #appending to dataframe
        df.Images[index]=(image_list)

    #The below code groups the dataframe by time(since there are multiple lat long pairs for a second),selects unique images from them and saves them to a CSV file
    df=df.groupby('Time',as_index=False).Images.sum()
    df.Images=list(list(map(set,df.Images)))
    df.Images=df.Images.apply(list)   
    df.to_csv("resultsDf2.csv")
    
    print "Process completed, check resultsDf.csv"


# In[18]:


video_file_input= raw_input("Enter video SRT file name(.csv)[For the given task, enter SRT_converted.csv]: ")

inputfile = pd.read_csv(video_file_input,'r',delimiter=',')

for index in range(0,len(inputfile)):
    
    inputfile.TimeStamp[index]=datetime.strptime(inputfile.TimeStamp[index],' %H:%M:%S,%f') #converting into dataTime object for easier manipulation

df = pd.DataFrame(np.nan,index=range(0,len(inputfile)),columns=['Time','Images']) #Creating a dataFrame

Range=input("Enter range in meters[For the given task, enter 35]:")

get_images_range(df,Range)

