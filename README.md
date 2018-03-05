# skylarkDrones

**Greetings to the evaluator!**

It was indeed a pleasure working on the given task for the position of an intern at your esteemed company. Without further adeu, here is my approach to the problem.
 
**Task**:*For the video, rather than sending the actual video, I'm just going to send you the SRT file. That's basically like a subtitle file, that has the coordinates of the drone at all the different times in the video.*
 
**Solution** ***ConvertSRT_CSV.py***

* input: videos/DJI_0301.SRT

* Output: SRT_converted.csv
 
 This program takes the SRT files as input, uses regular expression and gives a CSV file **SRT_converted.csv** which looks like this:
 
 TimeStamp    | Longitude | Latitude
 ------------ | --------- | --------
 00:00:00,400 | 73.001330 | 19.15014
 00:00:00,500 | 73.001330 | 19.15017
 00:00:00,600 | 73.001323 | 19.15021
 ............ | ......... | ........
 
**Task**: *For every second in the video, I want a list of all the images that lie within 35 metres of the drone position.*

**Solution** ***MainTask_Solution.py***
 
* Input: SRT_converted.csv, images/
 
* Output: resultsDf.csv
 
* Time Complexity: O(n.m) n=images, m= video lat long pairs

This program takes the converted SRT file and the images as input and outputs a CSV file. I've used *vincenty Formulae* to calculate the distance between the latitude, longitude pair even though it takes twice as many mathemetical calculations as the *Great circle distance formula* because it gives more precise results and since we are dealing within meters, precision is an important factor.

The following images have no GPS data and have been handled(Error log.txt):
 
 1.image DJI_0061.jpg 

 2.image DJI_0377.jpg 

 3.image DJI_0452.jpg 

 4.image DJI_0605.jpg 

 5.image DJI_0061.jpg 

 6.image DJI_0377.jpg 

 7.image DJI_0452.jpg 
 
8.image DJI_0605.jpg 

The output CSV looks like this:


Time | Images
---- | ------
0	 | DJI_0010.JPG,DJI_0013.JPG....
1	 | DJI_0013.JPG,DJI_0014.JPG....
2    | DJI_0057.JPG,DJI_0048.JPG....
.	 | .............................


**Task**: *Along with that, I'll also give you an excel of some points of interest for the client. I want all images within 50 meters of these POIs.*

**Solution** ***POI_assests_solution.py***

* Input: assets.csv, images/

* Output: POI_results.csv

This program works similar to the main solution and outputs the desired images to a CSV file.

**Task**: *Also, if possible, give me a KML of the drone path from the video.*

**Solution** ***Create_KML.py***

* Input: SRT_converted.csv

* Output: dronePath.kml

![drone_path.jpeg](drone_path.jpeg)
A simple program which creates a kml path from the SRT file.


The flight parameters are dynamic and can be adjusted during runtime and any number of images can be handled.

That'll be all from my side. Would love feedback on my approach!

Thank you
