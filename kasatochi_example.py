# coding: utf-8
import os
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import seaborn as sns
import datetime
import numpy as np
import xarray as xr
from scipy.stats import poisson
#import kasatochi
from utilhysplit import concutils
from monetio.models import hysplit
from monetio.models import pardump
import utilhysplit.par2conc as par2conc

def getumass(letter):
    """
    values from Crawford 2016 JGR paper
    convert unit mass to grams
    """
    if letter == "A":
        mer = 2.8e4
    elif letter == "B":
        mer = 2.8e3
    elif letter == "C":
        mer = 2.8e5
    elif letter == "D":
        mer = 2.8e6
    # mer is in kg/s
    # return grams per hour
    unitmass = mer * 3600.0 * 1000
    return unitmass

def flatten_pdump(pdump,date,lev,poll,makeplot=False):
    """
    This sets height to the same value so would create a 2d field
    with points all at the same height. 
    """
    temp = process_pdump(pdump,date,lev,poll,makeplot)
    temp['ht'] = 1000
    return temp

def process_pdump(pdump, date,lev,poll, makeplot=False):
    temp = pdump[pdump.date ==date]
    temp = temp[temp.ht >=lev[0]]
    temp = temp[temp.ht <=lev[1]]
    temp = temp[temp.poll==poll]
    if makeplot:
        plt.scatter(temp.lon, temp.lat, c=temp.ht,s=1)
        plt.show()
    return temp

#def processcdump(cdump, key, mult):
#    kdate = datetime.datetime.strptime(key, "%Y%m%d%H%M")
#    cdump = cdump.p006
#    cdumpt = cdump.sel(time=kdate) 
    #cdumpmass = cdumpt.sum(dim='x')
    #cdumpmass = cdumpmass * mult
#    return cdumpt

class KasatochiExample:

    def __init__(self):
        self.tdir = './RunFiles/runKX/'
        #self.dur = 60
        #self.tmave=60 #1 hours
        self.stime = datetime.datetime(2008,8,10,12)
        self.etime = datetime.datetime(2008,8,10,14)
        
        self.spid = ['p006','p020','p060','p200']

        self.minht = 1000 #ignore mass below this level.

        # these are for resolution of gmm grid output.
        self.dd=0.05
        self.dh=0.01
        self.buf=0.1

        # dictionary with cdump files.
        self.chash = {}

        # for plotting
        self.levels = np.arange(0.02,0.2,2)
        self.ticklocs = [10,5000,10000,15000,20000,25000]
        self.xlim=(-84,-80)
        self.ylim=(40,42.5)
        self.xticks = [-84,-83,-82,-81,-80]
        self.yticks = [40,41,42]
        #
        self.phash = {}
        self.chash = {}
        self.afithash = {}
        self.bfithash = {}

        # multiplication factor to use to change unit mass to g.
        # A, mer=2.8e4
        # B, mer=2.8e3
        # C, mer=2.8e5
        # D, mer=2.8e6 
        self.mult = getumass("C")

    def set_drange(self,stime,etime):
        self.stime = stime
        self.etime = etime

    def setmult(self,mult="A"):
        """
        Runs release unit mass every hour.
        This factor is used to convert unit mass / m3 to
        g/m3.
        """
        self.mult = getumass(mult)
        self.multstr = mult
        print('mult set ', self.mult)

    def get_cdump(self,tag,verbose=False):
        """
        reads data in cdump files into an xarray.
        stores in chash dictionary and returns xarray.
        """

        # B is 5,000 particles. SEED=-4
        # 24 hour run.
        # 0.05x0.1 concentration grid.
        # snapshot - 01 01 00
        d1 = self.stime
        d2 = self.etime
        base = 'cdump.'
        pname = os.path.join(self.tdir, base + str(tag))
        self.chash[tag] = hysplit.open_dataset(pname, century=2000,
                         drange=[d1,d2],verbose=verbose)
        return  self.chash[tag]

    def get_pdump(self, tag,verbose=False):
        """
        reads data in a PARDUMP file into a DataFrame and stores in phash
        dictionary. Returns the DataFrame.
        """
        d1 = self.stime
        d2 = self.etime
        base = 'PARDUMP.'
        century = int(d1.year/100) * 100
        pname = os.path.join(self.tdir, base + str(tag))
        self.phash[tag] = pardump.open_dataset(pname, century=century,
                         drange=[d1,d2],verbose=verbose)
        return  self.phash[tag]

    def fit_pdump(self,tag,nnn,method,minht=0,poll=4,wcp=1e3, massload=False):
        """
        wcp : float. weight concentration prior used for BGM.
        returns 
        mfit: a MassFit object from the par2fit function in par2conc.py
        temp: pandas DataFrame that was passed to par2fit 
        """
        temp = self.phash[tag]
        if massload:
           temp = flatten_pdump(temp, self.stime, [minht,20000],poll)
        else:
            temp = process_pdump(temp, self.stime, [minht,20000],poll)
        mfit = par2conc.par2fit(temp, method=method, nnn=nnn,wcp=wcp)
        return temp, mfit

  
    def plot_fit(self,concra):
        """
        creates plots
        """
        if self.multstr == 'C':
           vmin=0
           vmax=28
           levels = np.arange(0.2,30,0.2)
           levels = np.insert(levels,0,0.02)
           ticklocs = [0,5,10,15,20,25,30]
        else:
           vmin=0
           vmax=2.8
           levels = np.arange(0.2,3,0.2)
           levels = np.insert(levels,0,0.02)
           ticklocs = [0,1,2,3]

        sns.set()
        sns.set(font_scale=1.5)
        #ticklocs = [0,1,2,3]
        chash = {'ticks':ticklocs,
                 'label': 'g m$^{-2}$'}
        from matplotlib import colors
        temp = par2conc.threshold(concra, tval=0,tp='linear',fillna=True)
        temp.isel(z=0).plot.pcolormesh(x='longitude',
                                       y='latitude',
                                       vmin=vmin,vmax=vmax,
                                       cbar_kwargs=chash)
        plt.tight_layout()
        plt.xlim(-160,-135)
        plt.ylim(39,55)
        plt.title('')
      

    def slice_cdump(self, tag, lon, 
                   makeplot='mesh',
                   mult=0.001):
        """
        Takes a vertical slice of the cdump file.
        """

        # mult = 0.001 to convert to km
        from utilhysplit import concutils
        cdump = self.chash[tag]
        # convert to mg/m3
        cdump = cdump.p200 * self.mult * 1000
        z2sel = [x for x in cdump.z.values if x > self.minht]
        
        cdump = cdump.sel(z=z2sel)
        cslice = concutils.xslice(cdump.isel(time=0), lon)
        cslice = cslice.assign_coords(z=cslice.z * mult)
        if makeplot == 'mesh':
           chash={'label': 'mg m$^{-3}$'}
           cslice.plot.pcolormesh(x='latitude', y='z', cbar_kwargs=chash)
        elif makeplot == 'contour':
           chash={'label': 'mg m$^{-3}$'}
           xr.plot.contour(cslice, x='latitude', y='z',cmap='bone')
        return cslice

       
 
    def process_cdump(self,tag,poll=4):
        sns.set()
        sns.set(font_scale=1.5)

        if self.multstr == 'C':
           vmin=0
           vmax=28
           levels = np.arange(0.2,30,0.2)
           levels = np.insert(levels,0,0.02)
           ticklocs = [0,5,10,15,20,25,30]
        else:
           vmin=0
           vmax=2.8
           levels = np.arange(0.2,3,0.2)
           levels = np.insert(levels,0,0.02)
           ticklocs = [0,1,2,3]

        chash = {'ticks':ticklocs,
                 'label': 'g m$^{-2}$'}

        from matplotlib import colors
        #levels = self.levels
        #levels = np.arange(0.2,3,0.2)
        #levels = np.insert(levels,0,0.02)
        cdump = self.chash[tag]
        # Look at 20 um particles which have most of the mass.
        # convert to g/m3 
        if poll==4:
            cdump = cdump.p200 * self.mult
        elif poll==3:
            cdump = cdump.p060 * self.mult
            vmax=12
        elif poll==2:
            cdump = cdump.p020 * self.mult
            ticklocs = [0,1,2,3]
            vmax=4
        elif poll==1:
            cdump = cdump.p006 * self.mult
            vmin=0
            vmax=1
            ticklocs = [0,0.25,0.5,0.75,1]
        chash = {'ticks':ticklocs,
                 'label': 'g m$^{-2}$'}
        z2sel = [x for x in cdump.z.values if x > 2000]
        z2sel = [x for x in cdump.z.values if x > self.minht]
        #cdump = cdump.sel(z=z2sel)
        cdump = hysplit.hysp_massload(cdump, zvals=z2sel)
        #cdump.sel(time=self.stime).plot.pcolormesh(x='longitude',y='latitude',levels=levels)
        cdump.sel(time=self.stime).plot.pcolormesh(x='longitude',
                                                   y='latitude',
                                                   vmin=vmin,vmax=vmax,
                                                   cbar_kwargs=chash)
        plt.tight_layout()
        plt.xlim(-160,-135)
        plt.ylim(39,55)
        plt.title('')
        return cdump


#--------------------------------------------------------------



     


class ShotNoiseTest(KasatochiExample):

    def __init__(self):
        super().__init__()


    def getdata(self,tag,nrange=[1,51]):
        for num in np.arange(nrange[0],nrange[1],1):
            tag2 = '{}{}'.format(tag,num)
            self.get_pdump(tag2,verbose=False) 

    def example3(self,ht,bwidth=5):
        lat = 47
        lon = -165
        dd = 0.25
        dh = 1000
        poll=None
        stime = None
        numdist = self.get_num_dist(lat,lon,ht,dd,dh,poll,stime)
        self.compare_numdist(numdist,bwidth=bwidth)


    def example2(self,ht,bwidth=5):
        #large volume
        lat = 45.67-0.50/2.0
        lon = -151-0.50/2.0
        #ht=6000
        dd = 0.50
        dh = 5000
        poll=None
        stime = datetime.datetime(2008,8,10,12)
        numdist = self.get_num_dist(lat,lon,ht,dd,dh,poll,stime)
        self.compare_numdist(numdist,bwidth=bwidth)

    def example1(self,ht,bwidth=1):
        #small volume
        lat = 45.67-0.25/2.0
        lon = -151-0.25/2.0
        #ht=6000
        dd = 0.25
        dh = 1000
        poll=None
        stime = datetime.datetime(2008,8,10,12)
        numdist = self.get_num_dist(lat,lon,ht,dd,dh,poll,stime)
        self.compare_numdist(numdist,bwidth=bwidth)

    def get_parnumdf(self,df,lat,lon,ht,dd,dh,
                   poll=None,
                   stime=None):
        df2 = df[df.lat >= lat]
        df2 = df2[df2.lon >= lon]
        df2 = df2[df2.lon <= lon+dd]
        df2 = df2[df2.lat <= lat+dd]
        df2 = df2[df2.ht >= ht]
        df2 = df2[df2.ht <= ht+dh]
        if poll:
            df2 = df2[df2.poll==poll]
        if stime:
        #stime = datetime.datetime(2008,8,10,12)
            df2 = df2[df2.date ==stime]
        return df2

    def get_parnum(self,df,lat,lon,ht,dd,dh,
                   poll=None,
                   stime=None):
        return len(self.get_parnumdf(df,lat,lon,ht,dd,dh,poll,stime))
       
    def compare_numdist(self, numdist,bwidth=1,name='junk'):
        #sns.set_style('whitegrid')
        sns.set(font_scale=1)
        sns.set_style('white')
        mu = np.mean(numdist)
        nmin = np.min(numdist)
        nmax = np.max(numdist)
        print('Mean', mu)
        print('Min, Max', nmin,nmax)
        test = poisson(mu)
        fr = 1
        #binmax = int(mu) + np.ceil(fr * mu)
        binmax = np.max(numdist) + int(0.01*np.max(numdist))
        binmin = np.min(numdist) - int(0.25*np.min(numdist))
        bincenter = int(mu) - int(0.5*bwidth)
        binmin = bincenter - bwidth * np.ceil((bincenter-nmin)/bwidth)
        #binmin = np.max([0,int(mu) - np.ceil(fr * mu)])
        bins = np.arange(binmin,binmax,bwidth)
        #print(bins)
        print(binmin, binmax, bincenter)
        plt.hist(numdist,bins=bins-0.5,histtype='bar',
                 color='b',rwidth=0.9,density=True,align='mid')

        bins = np.arange(binmin,binmax,1)
        plt.plot(bins, test.pmf(bins),'-k.') 
        ax = plt.gca()
        fs=10
        plt.text(0.7,0.8,'Mean {}'.format(mu),transform=ax.transAxes,
                horizontalalignment='center',verticalalignment='center',
                fontsize=fs)
        plt.text(0.7,0.75,'Min {}'.format(nmin),transform=ax.transAxes,
                horizontalalignment='center',verticalalignment='center',
                fontsize=fs)
        plt.text(0.7,0.7,'Max {}'.format(nmax),transform=ax.transAxes,
                horizontalalignment='center',verticalalignment='center',
                fontsize=fs)
        plt.xlabel('Number of Particles in Volume', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('{}{}.{}'.format(name,'_poisson','png'))
        plt.show() 
        
    def get_num_dist(self,lat,lon,ht,dd,dh,poll=None,stime=None):
        #numdist = [self.get_parnum(x,lat,lon,ht,dd,dh) for x in self.phash.values()]
        numdist = [self.get_parnum(x,lat,lon,ht,dd,dh,poll,stime) for x in self.phash.values()]
        return numdist

    def fit_dist(self, numdist):
        mean = np.mean(numdist)
        testdist = poisson(mean)
