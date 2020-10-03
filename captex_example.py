# coding: utf-8
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import seaborn as sns
import xarray as xr
from monetio.models import hysplit
from monetio.models import pardump
import utilhysplit.par2conc as par2conc
import captex_util as captex



def min_conc_calculator(dh=0.05, dz=25, pnum=250000):
    """
    dh : float : horizontal resolution of grid in degrees
    dz : float : vertical resolution of grid in meters
    pnum : int : number of particles released per hour

    conc : float : concentration in g/m3 that would result from
                   one compuational particle in the volume

    """

    rate = 69333  # g per hour. release rate for captex1
    # pnum = 250000 #number particles released per houra
    # edur = 3      # 3 hour release
    g_per_par = rate / pnum  # each particle is that many grams.
    volume = dh * dh * 111e3 * 111e3 * np.cos(39.98 * np.pi / 180.0) * dz
    # volume = dh*dh*111e3*111e3* dz
    conc = g_per_par / volume
    return conc


def align_subA(cdump):
    # put lat and lon values back as x and y coordinates.
    latvals = cdump.latitude.values.T[0:][0]
    lonvals = cdump.longitude.values[0:][0]
    temp1 = [j - i for i, j in zip(latvals[:-1], latvals[1:])]
    temp2 = [j - i for i, j in zip(lonvals[:-1], lonvals[1:])]
    # print(set(temp1))
    # print(set(temp2))
    # print(latvals)
    # print(lonvals)
    temp = cdump.assign_coords(y=latvals)
    temp = temp.assign_coords(x=lonvals)
    return temp


def align_cdump(cdump1, cdump2, dd, tag1, tag2):
    cdump1 = align_subA(cdump1)
    cdump2 = align_subA(cdump2)
    minlat = np.min([np.min(cdump1.latitude.values), np.min(cdump2.latitude.values)])
    maxlat = np.max([np.max(cdump1.latitude.values), np.max(cdump2.latitude.values)])
    maxlon = np.max([np.max(cdump1.longitude.values), np.max(cdump2.longitude.values)])
    minlon = np.min([np.min(cdump1.longitude.values), np.min(cdump2.longitude.values)])

    # round to nearest hundred
    minlat = np.round(minlat * 100) / 100
    maxlat = np.round(maxlat * 100) / 100
    minlon = np.round(minlon * 100) / 100
    maxlon = np.round(maxlon * 100) / 100

    print(minlon, maxlon)
    print(minlat, maxlat)
    nlat = np.abs(np.ceil((maxlat - minlat) / dd)) + 1
    nlon = np.abs(np.ceil((maxlon - minlon) / dd)) + 1
    conc1 = par2conc.reindex(cdump1, minlat, minlon, nlat, nlon, dd, dd)
    conc2 = par2conc.reindex(cdump2, minlat, minlon, nlat, nlon, dd, dd)
    conc1 = conc1.drop("latitude")
    conc2 = conc2.drop("latitude")
    conc1 = conc1.drop("longitude")
    conc2 = conc2.drop("longitude")
    new1, new2 = xr.align(conc1, conc2, join="outer")
    new1.expand_dims("run")
    new1["run"] = tag1
    new2.expand_dims("run")
    new2["run"] = tag2
    return xr.concat([new1, new2], dim="run")


def compare_cdump(ara):

    # absolute difference
    diff = ara.isel(run=0) - ara.isel(run=1)
    # percent change
    diffa = diff / ara.isel(run=0)
    ticklocs = [-4, -2, -1, 0, 1, 2, 4]
    chash = {"ticks": ticklocs, "label": "pg m$^{-3}$"}
    levels = [-4, -2, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 2, 4]
    cmap = plt.get_cmap("coolwarm")
    # cmap=plt.get_cmap('winter')
    # norm = BoundaryNorm(levels,ncolors=cmap.N,clip=False)
    diffa.plot.pcolormesh(
        levels=levels, cmap=cmap, add_colorbar=True, cbar_kwargs=chash
    )
    ax = plt.gca()

    plt.show()
    levels = [-5000, -2500, -1000, -100, 0, 100, 1000, 2500, 5000]
    diff.plot.pcolormesh(levels=levels, cmap=cmap, add_colorbar=True)

    plt.show()
    # plt.xlim(self.xlim[0],self.xlim[1])
    # plt.ylim(self.ylim[0],self.ylim[1])


def processcdump(cdump, key, mult):
    kdate = datetime.datetime.strptime(key, "%Y%m%d%H%M")
    cdump = cdump.p006
    cdumpt = cdump.sel(time=kdate)
    # cdumpmass = cdumpt.sum(dim='x')
    # cdumpmass = cdumpmass * mult
    return cdumpt


# --------------------------------------------------------------
# captex 2 examples
# --------------------------------------------------------------
def CaptexExample2a():
    """
    captex2 
    """
    c2 = CaptexExample()
    c2.captex_number = 2
    c2.dur = 300
    c2.re_init()
    c2.stime = datetime.datetime(1983, 9, 26, 3)
    c2levels = np.arange(1, 22000, 100)
    c2.ticklocs = [10, 5000, 10000, 15000, 20000]
    c2.xlim = (-84, -80)
    c2.ylim = (40, 43.0)

    return c2


def CaptexExample2():
    """
    captex2 
    """
    c2 = CaptexExample()
    c2.captex_number = 2
    c2.dur = 600
    c2.re_init()
    # c2.stime = datetime.datetime(1983,9,26,3)
    c2.stime = datetime.datetime(1983, 9, 26, 9)
    c2.levels = np.arange(10, 10000, 100)
    c2.ticklocs = [10, 1000, 2500, 5000, 7500]
    c2.xlim = (-84, -75)
    c2.ylim = (40, 45.0)
    c2.xticks = list(np.arange(-84, -75, 2))
    c2.yticks = list(np.arange(40, 45, 1))
    return c2


class CaptexExample:
    def __init__(self):
        self.tdir = "./RunFiles/"
        self.captex_number = 1
        self.fname = "cdump.captex{}".format(self.captex_number)
        self.flist = self.cdumpfiles(self.fname)
        self.plist = self.pardumpfiles(self.captex_number)
        self.dur = 300
        self.tmave = self.dur / 100 * 60  # 3 hours
        self.stime = datetime.datetime(1983, 9, 18, 21)

        # these are for resolution of gmm grid output.
        self.dd = 0.05
        self.dh = 0.01
        self.buf = 0.1

        # dictionary with cdump files.
        self.chash = {}

        # for plotting
        self.levels = np.arange(10, 27000, 100)
        self.ticklocs = [10, 5000, 10000, 15000, 20000, 25000]
        self.xlim = (-84, -80)
        self.ylim = (40, 42.5)
        self.xticks = [-84, -83, -82, -81, -80]
        self.yticks = [40, 41, 42]
        #
        self.afithash = {}
        self.bfithash = {}

    def re_init(self):
        self.fname = "cdump.captex{}".format(self.captex_number)
        self.flist = self.cdumpfiles(self.fname)
        self.plist = self.pardumpfiles(self.captex_number)
        self.tmave = self.dur / 100 * 60  # 3 hours
        self.xticks = [-84, -83, -82, -81, -80]
        self.yticks = [40, 41, 42]

    def cdumpfiles(self, fname):
        flist = []
        # high resolution 250,000 particles
        # 0.05x0.05
        # 25m vertical resolution
        fdir = os.path.join(self.tdir, "runA")
        flist.append(os.path.join(fdir, fname))
        # high resolution 50,000 particles
        fdir = os.path.join(self.tdir, "RunB")
        flist.append(os.path.join(fdir, fname))
        # high resolution 5,000 particles
        fdir = os.path.join(self.tdir, "RunC")
        flist.append(os.path.join(fdir, fname))
        # high resolution 5,000 particles. different seed.
        fdir = os.path.join(self.tdir, "RunD")
        flist.append(os.path.join(fdir, fname))
        # low (regular) resolution 50,000 particles
        # 0.25x0.25
        # 100m
        # Difference from Fantine's runs are
        # delt=5
        # vinit=1
        # vscales = 5.0
        # kmix0 = 150
        fdir = os.path.join(self.tdir, "RunE")
        flist.append(os.path.join(fdir, fname))
        return flist

    def pardumpfiles(self, iii):
        # high resolution 5,000 particles
        base = "PARDUMP.cap"
        plist = []
        # high resolution 5,000 particles
        pdir = os.path.join(self.tdir, "RunC")
        plist.append(os.path.join(pdir, base + str(iii)))
        # high resolution 50,000 particles
        pdir = os.path.join(self.tdir, "RunB")
        plist.append(os.path.join(pdir, base + str(iii)))
        # high resolution 5,000 particles
        pdir = os.path.join(self.tdir, "RunD")
        plist.append(os.path.join(pdir, base + str(iii)))
        # high resolution 255,000 particles
        pdir = os.path.join(self.tdir, "RunA")
        plist.append(os.path.join(pdir, base + str(iii)))
        return plist

    def process_cdump(self, cdump):
        # unique to the captex runs.
        cdump = cdump.PMCH
        # change to picograms / m3
        cdump = cdump * 1e12
        # c value represents middle of level
        cdump = cdump.fillna(0)
        try:
            dz = (cdump.z.values[1] - cdump.z.values[0]) / 2.0
        except:
            dz = cdump.z.values[0] / 2.0
            # return cdump
        cdump = cdump.assign_attrs({"ztop": cdump.z.values})
        cdump = cdump.assign_coords(z=cdump.z.values - dz)
        return cdump

    # --------------------------------------------------------------
    def make_example1(self):
        # d1 = datetime.datetime(1983,9,19,0)
        # d1 = datetime.datetime(1983,9,18,21)
        d1 = self.stime
        d2 = d1 + datetime.timedelta(minutes=self.tmave)
        fnum = 1
        cap1 = captex.Captex(self.captex_number)
        capx, capy, capz = cap1.get_points(d1, dur=self.dur)
        for num in [0, 1, 2, 3, 4]:
            # for num in [2]:
            fig = plt.figure(fnum)
            cdump = self.get_cdump(num, drange=[d1, d2])
            self.plot_example1(cdump, capdata=(capx, capy, capz), thresh=1)
            plt.savefig("example1_" + str(num) + ".png")
            fnum += 1

    def get_ex_cdump(self, num):
        d1 = self.stime
        d2 = d1 + datetime.timedelta(minutes=self.tmave)
        cdump = self.get_cdump(num, drange=[d1, d2])
        return cdump

    def comparesub(self, cdump):
        ra = cdump.copy()
        if "z" in ra.dims:
            ra = ra.isel(z=0)
        if "time" in cdump.dims:
            # ra = ra.isel(time=0)
            ra = ra.mean(dim="time")
        return ra

    def comparetwo(cdump1, cdump2):
        ra1 = comparesub(cdump1)
        ra2 = comparesub(cdump2)
        diff = ra1 - ra2
        return diff

    def plot_example1(self, cdump, capdata=(None, None, None), thresh=None, log=False):
        levels = self.levels
        ticklocs = self.ticklocs
        chash = {"ticks": ticklocs, "label": "pg m$^{-3}$"}
        sns.set()
        sns.set_style("ticks")
        ra = cdump.copy()
        if "z" in ra.dims:
            ra = ra.isel(z=0)
        if "time" in cdump.dims:
            # ra = ra.isel(time=0)
            ra = ra.mean(dim="time")
        cmap = plt.get_cmap("viridis")
        # cmap=plt.get_cmap('Purples')
        if thresh:
            ra = par2conc.threshold(ra, thresh, "linear", fillna=False)
        if log:
            import matplotlib.colors as colors

            chash = {}
            # chash['norm']=colors.LogNorm(vmin=0.001, vmax=30000)
            norm = colors.LogNorm(vmin=0.001, vmax=30000)

            ra.plot.pcolormesh(
                x="longitude",
                y="latitude",
                levels=levels,
                norm=norm,
                cmap=cmap,
                add_colorbar=True,
                cbar_kwargs=chash,
            )
        else:
            ra.plot.pcolormesh(
                x="longitude",
                y="latitude",
                levels=levels,
                cmap=cmap,
                add_colorbar=True,
                cbar_kwargs=chash,
            )

        ax = plt.gca()
        plt.xlim(self.xlim[0], self.xlim[1])
        plt.ylim(self.ylim[0], self.ylim[1])
        ax.set_xticks(self.xticks, minor=False)
        ax.set_yticks(self.yticks, minor=False)
        maxval = np.max(ra)
        minval = np.min(ra)
        fig = plt.gcf()
        plt.title("")

        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=False)

        if np.any(capdata):
            temp = list(zip(capdata[0], capdata[1], capdata[2]))
            c1 = [x for x in temp if x[2] > 0]
            c2 = [x for x in temp if x[2] <= 0]
            capdata = list(zip(*c1))
            c2 = list(zip(*c2))

            cb = plt.scatter(
                capdata[0],
                capdata[1],
                c=capdata[2],
                s=70,
                cmap=cmap,
                norm=norm,
                edgecolors="#f2f0f0",
            )
            # plot measurements stations with 0.
            plt.scatter(c2[0], c2[1], s=70, edgecolors="#323633", facecolors="#fafcfb")
        return minval, maxval

    # --------------------------------------------------------------
    def get_cdump(self, num, drange=None):
        fl = self.flist[num]
        cdump = hysplit.open_dataset(fl, drange=drange, century=1900)
        cdump = self.process_cdump(cdump)
        self.chash[num] = cdump
        return cdump

    # --------------------------------------------------------------
    def test_pdump(self):
        num = 1
        d1 = self.stime
        d2 = d1 + datetime.timedelta(minutes=self.tmave)
        df = self.get_pdump(num, [d1, d2])
        pc = par2conc.Par2Conc(df)
        # look at particles up to 500m from time d1 to 3 hours later.
        df2 = pc.subsetdf(d1, self.tmave, htmax=500)
        # creates fit for each time in the dataframe.
        mlist = par2conc.fit_timeloop(df2, nnn=50, maxht=500, method="gmm")
        return mlist

    def get_pdump_example1_a(self):
        # fit to the 5,0000 particle simulation
        return self.get_pdump_example1(
            nnn=50, method="gmm", dd=self.dd, dh=self.dh, num=1, warm_start=False
        )

    def get_pdump_example1_a(self):
        # fit to the 50,0000 particle simulation
        return self.get_pdump_example1(
            nnn=50, method="gmm", dd=self.dd, dh=self.dh, num=2, warm_start=False
        )

    def get_pdump_example1_c(self):
        nnn = 50
        method = "gmm"
        dd = self.dd
        dh = self.dh
        return self.get_pdump_example1(nnn, method, dd, dh, num=2, warm_start=False)

    def get_pdump_example1_b(self):
        nnn = 20
        method = "gmm"
        dd = self.dd
        dh = self.dh
        return self.get_pdump_example1(nnn, method, dd, dh)

    def get_mlist(self, nnn, method, dd, dh):
        num = 1
        d1 = self.stime
        d2 = d1 + datetime.timedelta(minutes=self.tmave)
        df = self.get_pdump(num, [d1, d2])
        pc = par2conc.Par2Conc(df)
        # look at particles up to 500m from time d1 to 3 hours later.
        df2 = pc.subsetdf(d1, self.tmave, htmax=500)
        # creates fit for each time in the dataframe.
        mlist = par2conc.fit_timeloop(df2, nnn=nnn, maxht=500, method=method)
        return mlist

    def get_pdump_example1(
        self, nnn, method, dd, dh, num=1, warm_start=True, verbose=False
    ):
        """
        warm_start : boolean
            indicates whether to use fit from previous time as a starting point. 
        """
        d1 = self.stime
        d2 = d1 + datetime.timedelta(minutes=self.tmave)
        df = self.get_pdump(num, [d1, d2])
        pc = par2conc.Par2Conc(df)
        # look at particles up to 500m from time d1 to 3 hours later.
        df2 = pc.subsetdf(d1, 3 * 60, htmax=500)
        # creates fit for each time in the dataframe.
        mlist = par2conc.fit_timeloop(
            df2, nnn=nnn, maxht=500, method=method, warm_start=False
        )
        concra1 = par2conc.average_mfitlist(mlist, dd=dd, dh=dh, buf=0.01)
        # fit all the particles at all the times at once.
        mfit = par2conc.par2fit(df2, method=method, nnn=nnn)
        # need to divide mass by number of time periods included in the average.
        mult = 1 / len(set(df2.date.values))
        concra = mult * mfit.get_conc(dd=dd, dh=dh)

        # convert to pico-grams and
        # shift mass underground to first level
        concra1 = 1e12 * par2conc.shift_underground(concra1)
        concra = 1e12 * par2conc.shift_underground(concra)

        # first is from averaging fits to each time period
        # second is from fitting to all.
        if verbose:
            print("done")
        self.afithash[(nnn, method)] = mlist
        self.bfithash[(nnn, method)] = mfit

        return concra1, concra

    def plot_pdump_example1(self, c1, thresh=1, name="pdump_example1", log=False):
        d1 = self.stime
        cap1 = captex.Captex(self.captex_number)
        capx, capy, capz = cap1.get_points(d1, dur=self.dur)
        # use first two levels.
        conc = c1.isel(z=[0, 1]).mean(dim="z")
        self.plot_example1(conc, capdata=(capx, capy, capz), thresh=thresh, log=log)
        plt.savefig(name + "_" + str(self.captex_number) + ".png")
        plt.show()
        return conc

        # return df, df2, mfit, pc

    # def get_pdump_example2(self):
    #    num=1
    #    d1 = datetime.datetime(1983,9,20,6)
    #    d2 = datetime.datetime(1983,9,20,12)
    #    df = self.get_pdump(num, [d1,d2])
    #    pc = par2conc.Par2Conc(df)
    #    df2 = pc.subsetdf(d1, 6*60, htmax=500)
    #    return df, df2
    # --------------------------------------------------------------

    def get_pdump(self, num, drange=None, century=1900):
        fl = self.plist[num - 1]
        df = pardump.open_dataset(fl, drange, century=century)
        # capar = vp.VolcPar(self.fdir, fl)
        # capar.read_pardump(century=century)
        return df

    # def process_pdump1(self, htmax=None,nnn=None):
    #    """
    #    Obtains averages by fitting to all particles.
    #    """
    #    jjj, pdictall = vp.combine_pdict(self.pdict, self.stime, self.tmave)
    #    if htmax:
    #       pdictall = pdictall[pdictall['ht']<=htmax]
    #    mass = pdictall['pmass'].sum() / float(jjj)
    #    self.pdictall = pdictall
    #    self.mass = mass
    #    self.nnn = nnn
    #    self.htmax = htmax
    #    self.mfit = vp.par2fit(pdictall, nnn=nnn)
    #    mra = self.mfit.get_conc(dd=0.01,dh=0.005, buf=0.1, mass=mass)
    #    # move mass to first level.
    #    mra = vp.shift_underground(mra)
    #    self.mra =  km2m(mra)


    #def process_pdump2(self, htmax=None, nnn=None):
    #    """
    #    Obtains averages by fitting to each output time then
    #    averaging results.
    #    """
    #    pdictlist = vp.subset_pdict(self.pdict, self.stime, self.tmave)
    #    mfitlist = []
    #    masslist = []
    #    for pdn in pdictlist:
    #        if htmax:
    #            pdn = pdn[pdn["ht"] <= htmax]
    #        mfitlist.append(par2fit(pdn, nnn))
    #        masslist.append(pdn["pmass"].sum())
    #    self.mass2 = masslist
    #    self.nnn2 = nnn
    #    self.htmax2 = htmax
    #    self.mfitlist = mfitlist
    #    self.m2ra = vp.average_mfitlist(
    #        mfitlist, masslist, self.dd, self.dh, self.buf, None, None, None
    #    )
