#Scenario 1
#This script runs X1t and extracts the values of the model at various times for the last model node
#The residual from the concentration measurement is extracted for calculating SSWR
import os,sys
import numpy as np

## append full path to GWBplug in.py ...
sys.path.append("c:/program files/gwb/src")
## or relative path ...
sys.path.append(os.path.abspath('.'))
# import GWBplugin class
from GWBplugin import *

myPlugin = GWBplugin()

success = myPlugin.initialize("x1t", "", "-cd \"D:/Models/Errors\" -i \"D:/Models/Errors/time.x1t\"")

out = open("res.txt", "w")


for a in np.arange(1.5, 2.505, .005):

   out.write('{:8.3e}'.format(a) + "\t")

   for c in np.arange(.4, .6, .02):
      myPlugin.exec_cmd("discharge start " + '{:8.3e}'.format(a*c) + " pore_volumes")
      myPlugin.exec_cmd("interval end at " + '{:8.4e}'.format(c) + " day; go")

      conc = myPlugin.results("concentration original fluid", "mg/l", 99)
      for b in range(1,4):
         out.write('{:8.5e}'.format(conc[b]) + "\t")


   out.write("\n")

out.close()
