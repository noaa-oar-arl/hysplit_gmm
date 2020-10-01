# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
import datetime
import os
import sys
from  utilhysplit.hcontrol import HycsControl
from  utilhysplit.hcontrol import NameList

# run script to create 100 runs with different seeds.
# CONTROL.C is from captex 2 for run B with a shorter run time.


def write_setup(fname, tag, num):
    setup = NameList(fname)
    setup.read()
    setup.add('POUTF', "'PARDUMP.{}'".format(tag))
    if 'S' in tag:
        setup.add('PINPF', "'PARDUMP.BB{}'".format(num))
    setup.add('SEED',str(-1*num))
    setup.rename('SETUP.' + tag)
    setup.write()

def write_control(fname, tag):
    #read in control file to be copied
    control = HycsControl(fname=fname)
    control.read()
    #rename cdump files
    for cg in control.concgrids:
        cg.outfile += '.' + tag 
    control.rename('CONTROL.' + tag) 
    control.write()

def shot_run(tag1): 
    hdir = '/hysplit-users/alicec/hysplit_dev/exec/hycs_std'
    ocontrol = 'CONTROL.{}'.format(tag1)
    osetup = 'SETUP.{}'.format(tag1)
    #arange = np.arange(1,51,1)
    arange = np.arange(51,101,1)
    #taglist = ['D1','D2','D3','D5','D7','D8','D9','D10']
    for num in arange:
        tag = '{}{}'.format(tag1,num)
        write_control(ocontrol, tag)
        write_setup(osetup, tag,num)
     
         
shot_run('C')










