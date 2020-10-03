import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import numpy as np

class Captex():
    """
    reads text files with CAPTEX measurements into Pandas DataFrame.
    provides some basic plotting functions and other utilities.
    """

    def __init__(self, num=2):
        """
        num : int (1,2,3,4,5,7)
        """
        fname = './Data/captex'
        fname += str(num) + '.txt'
        self.df  = pd.read_csv(fname, sep='\s+', header=[0], skiprows=1)
        self.df['date'] =  self.df.apply(lambda row: 
                          datetime.datetime(int(row['year']), int(row['mn']),
                                            int(row['dy']),
                                            int(int(row['shr'])/100)),axis=1)
         
    def timeplot(self, station):
        temp = self.df[self.df['stn']==station]
        plt.plot(temp['date'], temp['pmch'],'k.')
        plt.show()

    def get_points(self,date,dur):
        """
        date : datetime object
        dur  : integer (300 for 3 hour or 600 for 6 hour)
        returns
        list of longitude, latitude and measurements at that date
        with averaging time of dur.
        """
        temp = self.df[self.df['date']==date]
        temp = temp[temp['dur']==dur]
        return temp['lon'], temp['lat'], temp['pmch']

    def scatter(self,date,dur=300):
        xxx,yyy,zzz = self.get_points(date,dur)
        cmap, norm = getcmap(np.max(zzz))
        cb = plt.scatter(xxx,yyy,c=zzz, s=100,
                         cmap=cmap, norm=norm,edgecolors='#f2f0f0')
        plt.colorbar()
        plt.show()
        return cmap, norm

    def getmax(self):
        dmax = self.df[self.df.pmch==self.df.pmch.max()]
        lat = dmax['lat']
        lon = dmax['lon']
        date = dmax.date.values
        return lat,lon, convert_date(date)

def convert_date(nd64):
    dstr = str(nd64)[0:-10]
    strfmt = "%Y-%m-%dT%H:%M:%s"
    return datetime.datetime.strptime(dstr,strfmt)

def getcmap(maxval, step=100):
    levels = np.arange(0,maxval,step)
    cmap = plt.get_cmap('viridis')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    return cmap, norm

def plotcaptex1pts():
    plt.plot(-82.2,41.3,'ro')
    plt.plot(-82.6,41.27,'r.')
    plt.plot(-81.87,41.42,'r.')
    
    plt.plot(-83.12,41.33,'c.')
    plt.plot(-80.42,39.65,'c.')

    
