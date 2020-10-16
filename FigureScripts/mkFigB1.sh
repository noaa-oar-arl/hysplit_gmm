#!/bin/bash -f
##

#4 from captex2. All time periods 18z-21z with 5 minute time steps.
#3 from kasatochi. All time periods 12z-13z with 10 minute time step. Pollutant 2.
#  0.1x0s :.1x500m
#1 kasatochi. all time periods. All species. 0.25x0.25x1km 

ma='scores_capC_capD_091900.png'
mb='scores_capC_capD_091903.png'

mc='score_kasD_kasC_090400.png'
md='score_kasD_kasC_101200.png'


for nm in $ma $mb $mc $md
do
  cp ../$nm ./
done

pntsz=20
pntsz=75

aaa=30
bbb=-550

convert $ma -gravity south\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(a)' \
        -gravity south\
        $ma

convert $mb -gravity south\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(b)' \
        -gravity south\
        $mb

convert $md -gravity south\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(d)' \
        -gravity south\
        $md

convert $mc -gravity south\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(c)' \
        -gravity south\
        $mc


montage -trim $ma \
        -trim $mb \
        -trim $mc \
        -trim $md \
        -geometry 800x450 -tile 2x2 AppendixB.png

#350x200
convert -trim AppendixB.png AppendixB.png

display AppendixB.png
