import pygrib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import shiftgrid
import numpy as np

file = 'grib/nam.t00z.conusnest.hiresf00.tm00.grib2'

plt.figure()
grbs=pygrib.open(file)

grb = grbs.select(name='Total Precipitation')[0]
data=grb.values
lat,lon = grb.latlons()

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
  urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
  resolution='c')

x, y = m(lon,lat)

cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

plt.colorbar(cs,orientation='vertical')
plt.title('Example 2: NWW3 Significant Wave Height from GRiB')
plt.show()

