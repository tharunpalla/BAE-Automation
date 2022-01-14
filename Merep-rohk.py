import sys
import matplotlib
matplotlib.use('Agg')
import pygrib
from mpl_toolkits.basemap import Basemap
from pylab import *
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter


grbs=pygrib.open(sys.argv[1])
grb=grbs.select(name='Mean sea level pressure')[0]
lats,lons=grb.latlons()
mslp=grb.values
mslp2=np.empty(shape=mslp.shape)

uniform_filter(mslp,size=10,output=mslp2,mode='reflect') #Silendan valja
mslp2=0.01*mslp2 #Teen Paskaltest Hektopaskalid


###############  Joonistamine  ###############
map=Basemap(projection='stere',lat_0=90,lon_0=0,llcrnrlat=30,llcrnrlon=-30,urcrnrlat=60,urcrnrlon=70,resolution='l')

font = {'weight' : 'extra bold','size' : 8}
matplotlib.rc('font', **font)

x,y=map(lons,lats)
numbrid=[930,935,940,945,950,955,960,965,970,975,980,985,990,995,1000,1005,1010,1015,1020,1025,1030,1035,1040,1045,1050,1055,1060,1065,1070,1075,1080,1085,1090,1095,1100]

qw=map.contour(x,y,mslp2,numbrid,colors='0',linewidth=0.3,zorder=3, color='green')
plt.clabel(qw, inline=1,fmt = '%1.0f',ticks=numbrid, color='green')



fig = matplotlib.pyplot.gcf()
fig.set_size_inches(6.45995, 4.86743)

valjund=sys.argv[2]
savefig(valjund,dpi=100,bbox_inches='tight',pad_inches=0)





