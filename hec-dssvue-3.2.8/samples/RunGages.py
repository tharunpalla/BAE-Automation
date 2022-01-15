# name=RunGages
# displayinmenu=false
# displaytouser=false
# displayinselector=true
from hec.script import *

glenFirArgs  = {"location" : "Glenfir", "version" : "OBS"}
execfile("C:/temp/GagePlot.py", {}, glenFirArgs)

madronArgs   = {"location" : "Madron", "version" : "OBS"}
execfile("C:/temp/GagePlot.py", {}, madronArgs)

oakTreeArgs   = {"location" : "Madron", "version" : "OBS"}
execfile("C:/temp/GagePlot.py", {}, oakTreeArgs)
