
# coding: utf-8

# In[1]:


import re 
import csv
import pandas as pd
from itertools import islice


# In[2]:


srt_file=open("videos\DJI_0301.srt",'r')


# In[3]:


data=[['TimeStamp','Longitude','Latitude']] #Header for CSV file
myFile = open('SRT_converted.csv', 'wb')  #Creating a new CSV file
writer = csv.writer(myFile)
writer.writerows(data) #Appending header 


# In[4]:


regexTS=re.compile(r' \d\d:\d\d:\d\d,\d\d\d')#Matches the SRT time stamp (only end time)
regexLongLat=re.compile(r'(\d\d.\d+),(\d\d.\d+)') #Matches Longitude,Latitude pair


# In[5]:


def next_n_lines(file_opened, N): #this function returns 4 lines from the input file, these 4 lines contain the time stamp and the lat long pair and regex can be used on them to extract it
    return [x.strip() for x in islice(file_opened, N)]


# In[6]:


for index in range(1,sum(1 for line in srt_file)/4+1):
    
    if index==1:
        srt_file.seek(0) #since sum function sets the cursor to the end
    
    chunk=str(next_n_lines(srt_file,4))
    row=[(regexTS.findall(chunk)[0],regexLongLat.search(chunk).group(1),regexLongLat.search(chunk).group(2))]
    writer.writerows(row)
    
srt_file.close()    
myFile.close()

