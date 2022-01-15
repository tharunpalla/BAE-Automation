'''
This script downloads time-series data from CDEC using HEC-DSSVue CDEC plugin. 
Initially written by HEC and modified for Feather HEC-RTS by Bibek Joshi
9/1/2021
'''
from hec.script import MessageBox
from hec.heclib.dss import HecDss
#from hec.plugins import *
from hec.plugins.cdec import CdecControlFrame
from hec2.rts.client import  RTS
import os
import sys
import java
import string
import time
from javax.swing import JOptionPane
###########################################
proj_dir = RTS.getBrowserFrame().getWatershedLocation().getProjectDirectory()
print('PROJECT DIR:', proj_dir )
rts_data = proj_dir.replace('watershed', 'database') 
########################################### 
def main() : 
  frame = RTS.getBrowserFrame()
  s = JOptionPane.showInputDialog(frame, "Enter number of days back to retrieve", "Retrieve Data", JOptionPane.QUESTION_MESSAGE)
  if s is None :
     return
  tw = "T-" + s + "D, T+1D"
  print tw
  try :     
     print "This is data home = "+ rts_data
     dssName = rts_data + "/Feather_CDEC_Observed2.dss"
     cdecName = rts_data + "/Feather.cdec"
     dssFile = HecDss.open(dssName, tw)
     cdec = CdecControlFrame(dssFile)
     cdec.loadStations(cdecName)
     cdec.cleanPrecip()
     istat = cdec.retrieveData()   
     dssFile.close()
     if istat == 0 :
       MessageBox.showError("Unable to retrieve data from CDEC", "Error retrieving data")
       return
  except java.lang.Exception, e :
     MessageBox.showError(e.getMessage(), "Error retrieving data")
     print "Error during data retrieval: " + e.toString()
     return
  frame.getCurrentMode().updatePlotIcons()
  MessageBox.showPlain("Data retrieval complete", "CDEC Real-Time Retrieval")
main()
