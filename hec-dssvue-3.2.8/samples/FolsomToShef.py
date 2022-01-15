from hec.script import *
from hec.heclib.dss import *
from hec.dssgui import *
import java

#  Open the file and get the data
try:  
  dssFile = HecDss.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  precip = dssFile.get("/AMERICAN/FOLSOM/PRECIP-BASIN/01JAN2006/1DAY/OBS/")
  stor = dssFile.get("/AMERICAN/FOLSOM/ STOR-RES EOP/01JAN2006/1DAY/OBS/")
  topcon = dssFile.get("/AMERICAN/FOLSOM/TOP CON STOR/01JAN2006/1DAY/OBS/")
  sagca = dssFile.get("/AMERICAN/FOLSOM-SAGCA/TOP CON STOR/01JAN2006/1DAY/OBS/")
  inflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/")
  outflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")

#  Add Data
datasets = java.util.Vector()
datasets.add(precip)
datasets.add(stor)
datasets.add(topcon)
datasets.add(sagca)
datasets.add(inflow)
datasets.add(outflow)

ls = ListSelection.getMainWindow()
ls.setIsInteractive(1,0)  # Turn off popups
ls.exportShef("C:/temp/FolsomShefData.shef", datasets)

#ls.finish()  # Batch mode only
