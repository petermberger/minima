#Scenario 1
#This script runs X1t and extracts the values of the model at various times for the last model node
#The residual from the concentration measurement is weighted and combined with a time residual to
#minimize the error in multiple dimensions for calculating SSWRt

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
#1.102603801	0.565056119	1.848842436	7.822614124	10.97580209	19.05068259	53.45085281	37.62560523	65.18794941	54.08222126

#terr is the square of the time error bar (10 min expressed as fractions of a day)
terr = 4.85e-5
obs = [1.102603801, 0.565056119, 1.848842436, 7.822614124, 10.97580209, 19.05068259, 53.45085281, 37.62560523, 65.18794941, 54.08222126]
t   = [0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58]
min = [0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58]

for a in np.arange(1.5, 2.505, .005):

   out.write('{:8.3e}'.format(a) + "\t")

   for d in range(len(min)):
      min[d] = 99999999999.99

   for c in np.arange(.3, .701, .01):
      myPlugin.exec_cmd("discharge start " + '{:8.4e}'.format(a*c) + " pore_volumes")
      myPlugin.exec_cmd("interval end at " + '{:8.4e}'.format(c) + " day; go")

      conc = myPlugin.results("concentration original fluid", "mg/l", 99)
      for d in range(len(obs)):
         hold = obs[d] - conc[3]
         hold = hold * hold / 10.624 + (t[d] - c)*(t[d] - c)/terr
         if hold < min[d]:
            min[d] = hold
   for b in min:
      out.write('{:8.5e}'.format(b) + "\t")


   out.write("\n")

out.close()
