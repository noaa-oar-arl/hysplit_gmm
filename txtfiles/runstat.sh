#!/bin/bash -f
##
# Runs statmain program.

##NAME runstat.sh
##PRGMMR: Alice Crawford ORG: ARL
##based on a script by Fantine Ngan.

##CTYPE: cshell script

##hdir should be changed to reflect where the HYSPLIT executable is found.

#Information about the captex tracer experiments can be found in the following publications.
#Jennifer Hegarty, R. R. Draxler, A. R. Stein, J. Brioude, M. Mountain, J. Eluskiewicz, T. Nehrkorn, F. Ngan, A. Andrews
#2013, "Evaluation of Lagrangian Particle Dispersion Models with Measurements from Controlled Tracer Releases"
#Journal of Applied Meteorology and Climatology, 52, pp2623-2637

#F. Ngan and A. F. Stein, (submitted 2017) "A Long-Term WRF meteorological arachive for dispersion simulations: Application to 
#Controlled Tracer experiments",  Journal of Applied Meteorology and Climatology.

#HYSPLIT model output is compared to measurements from tracer experiments using a cumulative score, rank, which consists of four
#equally weighted and normalized statistical parameters, the correlation coefficient, fraction bias, figure of merit in space, Kolmogorov-Smirnov
#parameter. The rank ranges from 0 to 4 with 4 being the best score.

#

##directory where HYSPLIT executable is found
hdir=../../hysplit.v5.0.0/
## directory where output should be written
odir=./


name=cdump

# Run statmain on output from GMM model.
for nnn in GG HH AA BB IC JJ4 JJ3 JJ2 JJ 
#for nnn in AA
do
for cnum in 2 3 4 5 7  
do
  cname=${name}.captex$cnum

  case=$cname

  exp=../Data/captex$cnum

  echo ${hdir}/exec/statmain -d${exp}.txt -rmodelmean${nnn}${cnum}.txt -o1 -t0 -l10.0
  ${hdir}/exec/statmain -d${exp}.txt -rmodelmean${nnn}${cnum}.txt -o1 -t0 -l10.0 -y5

# move files to another name
  mv dataA.txt ${nnn}${cnum}_dataA.txt
  mv statA.txt ${nnn}${cnum}_statA.txt
done
done
#endif


exit
