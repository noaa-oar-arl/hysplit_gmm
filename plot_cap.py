import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def readstat(fname):
    """
    fname : str
    read output of statmain program.
    """
    dhash = {}
    #print('opening ', fname)
    with open(fname, 'r', encoding="ISO-8859-1") as fid:
         for line in fid:
             if "Correlation coefficient" in line:
                 temp = line.split()
                 dhash['R'] = float(temp[0])
             if "Average bias" in line:
                 temp = line.split()
                 dhash['bias'] = (float(temp[0]))**2
             #if "Average bias" in line:
             #    temp = line.split()
             #    dhash['bias'] = float(temp[0])
             if "Fractional bias" in line:
                 temp = line.split()
                 dhash['FB'] = float(temp[0])
             if "Fig of merit" in line:
                 temp = line.split()
                 dhash['FMS'] = float(temp[0])
             if "Kolmogorov" in line:
                 temp = line.split()
                 dhash['KSP'] = float(temp[0])
             if "rank" in line:
                 temp = line.split()
                 dhash['rank'] = float(temp[0])
             if "Root mean" in line:
                 temp = line.split()
                 dhash['RMSE'] = float(temp[0])
    return dhash

class MultRuns:
    """
    Plots output from multiple statmain output files.
    """
    def __init__(self,taglist):
        self.taglist = taglist
        self.fhash = {}  #key is tag
                         #value is dictionary from CapRun
        self.makeflist()
        self.chash = {}  #key is tag, value is color
        self.lwhash={}   #key is tag, value is linewidth
        self.offsethash={}

    def test(self):
        print(self.taglist)

    def makeflist(self, base= './txtfiles/NNN_statA.txt'):
        numlist = ['1','2','3','4','5','7']
        for tag in self.taglist:
            flist = []
            #print('HERE', flist)
            for num in numlist:
                fname = base.replace('NNN',tag+num) 
                flist.append(fname) 
            #return flist
            caprun = CapRun(flist)
            dhash = caprun.getvalues()
            self.fhash[tag] = dhash 

    def add_color(tag,clr):
        self.chash[tag] = clr


    def plot(self, statkey, figname=None):
        sns.set()
        sns.set_style('white')
        for tag in self.taglist:
            ## These are from cdump.

            ## VV is from captexV directory 
            ## 5000 particles
            ## 0.25x0.25 and 100m in vertical

            ## UU is from captexG directory (higher resolution grid)
            ## 50,0000 particles
            ## 0.1x0.1 and 100m in vertical.

            ##TT is from captexNew directory. (control run)
            if tag in self.chash.keys():
               marker = self.chash[tag] 
            elif tag == 'TT':
               marker = '-ks'
               lw=3
            elif tag in ['UU']:
               marker = '--k.'
               lw=1
            elif tag in ['VV']:
               marker = '-k.'
               lw=1
            else:
               marker='-b.'
               lw=1
            if tag in self.lwhash.keys():
               lw = self.lwhash[tag]
            else:
               lw = 1
            if tag in self.offsethash.keys():
               offset = self.offsethash[tag]
            else:
               offset=0
            title=statkey
            xval = np.array([1,2,3,4,5,7]) + offset
            if statkey=='FB rank':
                skey = 'FB'
                plt.plot(xval,
                     1-np.abs(np.array(self.fhash[tag][skey])/2), 
                     marker, LineWidth = lw, label=tag)
                title = '1-|FB/2|'
            elif statkey=='R':
                plt.plot(xval, np.array((self.fhash[tag][statkey]))**2, 
                #plt.plot(xval, np.array((self.fhash[tag][statkey])), 
                     marker, LineWidth = lw, label=tag)
                title = '$R^2$'
            elif statkey=='KSP rank':
                skey='KSP'
                plt.plot(xval, 
                         1-np.array(self.fhash[tag][skey])/100, 
                         marker, LineWidth = lw, label=tag)
                title = '1- KSP/100'
            elif statkey=='FMS':
                skey='FMS'
                plt.plot(xval, 
                         np.array(self.fhash[tag][skey])/100, 
                         marker, LineWidth = lw, label=tag)
                title = 'FMS/100'
            else:
                plt.plot(xval, 
                     self.fhash[tag][statkey], 
                     marker, LineWidth = lw, label=tag)
            ax = plt.gca()
            ax.set_ylabel(title)
            ax.set_xlabel('CAPTEX number')
            ax.yaxis.grid(True)
        if figname: plt.savefig(figname)


class CapRun: 
    def __init__(self,flist):
        self.flist = flist 
        self.fhash = {} #key refers to statistic
                        #value is list cooresponding to value
                        #found in each file.
    def getvalues(self):
        iii=0
        for fname in self.flist:
            dhash = readstat(fname)
            for key in dhash.keys():
                if key not in self.fhash:
                   self.fhash[key] = []
                self.fhash[key].append(dhash[key]) 
        return self.fhash     


