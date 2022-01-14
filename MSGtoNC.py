import numpy as np
import pygrib
import matplotlib
matplotlib.use('AGG')
from mpl_toolkits.basemap import Basemap
from pylab import *
import sys
from mpop.imageo.geo_image import GeoImage
from mpop import *
from mpop.satellites import GeostationaryFactory
from mpop.projector import get_area_def
from scipy.interpolate import griddata
from netCDF4 import Dataset

################  Funktsioonid  ################
def MSGtoNC(satdata,grupp,fieldname,xdim,ydim,uhikud):
	satdata=satdata.filled(fill_value=-100)
	values=np.reshape(satdata,(satdata.shape[0]*satdata.shape[1],1))
	gridded=griddata(points,values,(Ygrid,Xgrid),method='nearest',fill_value=nan)
	gridded=gridded[:,:,0]
	field=grupp.createVariable(fieldname,"f4",[xdim,ydim])
	field[:]=gridded
	field.missing_value=-100.0
	field.units=uhikud


def MSGtoNC2(satdata,grupp,fieldname,dim,uhikud):
	field=grupp.createVariable(fieldname,"f4",[dim,])
	field[:]=satdata
	field.units=uhikud
################################################

#################  ETA projektsioon  ##################
suurus=2 #Mitu korda pilt peab olema suurem, kui 774x490 pikslit

llcrnrx=-37.5 #-13.5
llcrnry=-30.9 #-13.9
urcrnrx=39.8 #23
urcrnry=18 #14
ulatusH=774 #Pildi suurus pikslites
ulatusV=490
#dpi=50.0

map=Basemap(projection='rotpole', llcrnrx=llcrnrx, llcrnry=llcrnry, urcrnrx=urcrnrx, urcrnry=urcrnry, lon_0=0, o_lat_p=30, o_lon_p=0, resolution='l')
#######################################################


#################  Satelliidi sisselugemine  ##################
sataeg=sys.argv[1]
yyyy=int(sataeg[0:4])
mm=int(sataeg[4:6])
dd=int(sataeg[6:8])
hh=int(sataeg[8:10])
MM=int(sataeg[10:12])

time_slot = datetime.datetime(yyyy, mm, dd, hh, MM)
global_data = GeostationaryFactory.create_scene("meteosat", "10", "seviri", time_slot)
europe = get_area_def("EuropeCanary")
global_data.load([0.6,0.8,1.6,3.9,6.2,7.3,8.7,9.7,10.8,12.0,13.4], area_extent=europe.area_extent)

globalX_data = global_data.project("EuropeCanary")
geograafia=globalX_data.area.get_lonlats()
VIS006=globalX_data[0.6].data
VIS008=globalX_data[0.8].data
IR016=globalX_data[1.6].data
IR039=globalX_data[3.9].data
WV062=globalX_data[6.2].data
WV073=globalX_data[7.3].data
IR087=globalX_data[8.7].data
IR097=globalX_data[9.7].data
IR108=globalX_data[10.8].data
IR120=globalX_data[12.0].data
IR134=globalX_data[13.4].data
##############################################################


###########  Reprojetseerimine ja kirjutamine  ###########
satX,satY=map(geograafia[0],geograafia[1])
np.putmask(satX,satX>urcrnrx+1,satX-360)

Ygrid,Xgrid=np.mgrid[llcrnry:urcrnry:(ulatusV*suurus)*1j,llcrnrx:urcrnrx:(ulatusH*suurus)*1j]
satX2=np.reshape(satX,(satX.shape[0]*satX.shape[1],1))
satY2=np.reshape(satY,(satY.shape[0]*satY.shape[1],1))
points=np.concatenate((satY2,satX2),axis=1)

Latitude=Ygrid[:,0]
Latitude=np.round(Latitude,decimals=2)
Longitude=Xgrid[0,:]
Longitude=np.round(Longitude,decimals=2)

rootgrp = Dataset("MSG.nc", "w", format="NETCDF4")
x=rootgrp.createDimension("x",Xgrid.shape[1])
y=rootgrp.createDimension("y",Xgrid.shape[0])

MSGtoNC2(Longitude,rootgrp,"x","x","degrees_east")
MSGtoNC2(Latitude,rootgrp,"y","y","degrees_north")
MSGtoNC(VIS006,rootgrp,"VIS006","y","x","per_cent")
MSGtoNC(VIS008,rootgrp,"VIS008","y","x","per_cent")
MSGtoNC(IR016,rootgrp,"IR016","y","x","per_cent")
MSGtoNC(IR039,rootgrp,"IR039","y","x","Kelvin")
MSGtoNC(WV062,rootgrp,"WV062","y","x","Kelvin")
MSGtoNC(WV073,rootgrp,"WV073","y","x","Kelvin")
MSGtoNC(IR087,rootgrp,"IR087","y","x","Kelvin")
MSGtoNC(IR097,rootgrp,"IR097","y","x","Kelvin")
MSGtoNC(IR108,rootgrp,"IR108","y","x","Kelvin")
MSGtoNC(IR120,rootgrp,"IR120","y","x","Kelvin")
MSGtoNC(IR134,rootgrp,"IR134","y","x","Kelvin")

rootgrp.close()






