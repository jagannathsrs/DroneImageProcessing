
# coding: utf-8

# In[101]:


#Simple program to craete a KML file from the given lat long pairs of the SRT file

import csv
import simplekml

inputfile = csv.reader(open('SRT_converted2.csv','r'))
next(inputfile) #to skip header 
kml=simplekml.Kml()


# In[102]:


for row in inputfile:
    kml.newpoint(name=row[0],coords=[(float(row[1]),float(row[2]))])
    
kml.save('dronePath.kml')

