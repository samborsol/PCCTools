####Instructions for producing veto list
From Danek (https://hypernews.cern.ch/HyperNews/CMS/get/pixel-commissioning/2841.html) 

1) Identify a run number associated with the fill. 
For example for fill 4634 run 262081. 

2) Login to srv-c2f38-16-01. (Requires cmsusr account/login first.) 
Look into the file 
/pixel/data0/Run_262000/Run_262081/PixelConfigurationKey.txt 
and note the configuration key number, in this case: 
100965

Note that new runs appear first on 
/pixelscratch/pixelscratch/data0 
after a while they are copied to 
/pixel/data0

3) Search the file 
/pixelscratch/pixelscratch/config/Pix/configurations.txt 
for the string “key 100965” and note the detconfig version which is just below. 
 
In this case: 

key 100965 
detconfig   95 

This identifies the version of the detconfig file = 95.  

4) You can see the disabled modules in the file 
/pixelscratch/pixelscratch/config/Pix/detconfig/95/detectconfig.dat 
 
Now you can search for the module with the “noAnalogSignal” string. 

