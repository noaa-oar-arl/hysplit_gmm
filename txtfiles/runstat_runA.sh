#!/bin/bash -f

##

##PRGMMR: Alice Crawford ORG: ARL

##ABSTRACT: This code tests HYSPLIT using captex tracer experiment 
##CTYPE: cshell script

##hdir should be changed to reflect where the HYSPLIT executable is found.

##directory where HYSPLIT executable is found
hdir=../../hysplit.v5.0.0/
## directory where output should be written
odir=./
#
cdir=../RunFiles/RunA/
name=cdump
stat_tag=HI
for cnum in 1 2 3 4 5 7 
do
   case=$cname_${stat_tag}
   cname=$cdir${name}.captex$cnum
   # this is the name of the file with measurement data.
   exp=../Data/captex$cnum
   # run c2datem to get model output from cdump file at measurements points.
   echo   ${hdir}/exec/c2datem -i${odir}$cname -omodel.txt -m${exp}.txt -c1.0E+12
   ${hdir}/exec/c2datem -i${odir}$cname -omodel.txt -z1 -m${exp}.txt -c1.0E+12

   # run statmain to get statistics
   echo "${hdir}/exec/statmain -d${exp}.txt -rmodel.txt -o1 -t0 -l10.0"
   ${hdir}/exec/statmain -d${exp}.txt -rmodel.txt -o1 -t0 -l10.0

   echo "dataA.txt ${case}_dataA.txt"
   mv dataA.txt ${case}_dataA.txt
   echo "mv statA.txt ${stat_tag}_statA.txt"
   mv statA.txt ${stat_tag}${cnum}_statA.txt
   echo "mv model.txt ${case}_model.txt"
   mv model.txt ${case}_model.txt

   echo " "
done
exit
