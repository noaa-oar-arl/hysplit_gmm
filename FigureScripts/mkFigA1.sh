#!/bin/bash -f
##

#4 from captex2. All time periods 18z-21z with 5 minute time steps.
#3 from kasatochi. All time periods 12z-13z with 10 minute time step. Pollutant 2.
#  0.1x0s :.1x500m
#1 kasatochi. all time periods. All species. 0.25x0.25x1km 

mb=shotnoise1_poisson.png
ma=shotnoise3_poisson.png
md=shotnoise4_poisson.png

mbg=shotnoise1htlon.png
mag=shotnoise3htlon.png
mdg=shotnoise4htlon.png

hb=shotnoise1latlon.png
ha=shotnoise3latlon.png
hd=shotnoise4latlon.png

for nm in $ha $hb $hd $hag $hbg $hdg
do
  cp ../$nm ./
done

for nm in $ma $mb $mc $md $mag $mbg $mdg
do
  cp ../$nm ./
done

pntsz=20
pntsz2=35

aaa=20
bbb=-130

convert $ma -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(a)' \
        -gravity north\
        $ma

convert $mb -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(b)' \
        -gravity north\
        $mb

convert $md -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(c)' \
        -gravity north\
        $md

convert $mag -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(d)' \
        -gravity north\
        $mag

convert $mbg -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(e)' \
        -gravity north\
        $mbg

convert $mdg -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(f)' \
        -gravity north\
        $mdg

convert $ha -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(g)' \
        -gravity north\
        $ha

convert $hb -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(h)' \
        -gravity north\
        $hb

convert $hd -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $bbb+$aaa '(i)' \
        -gravity north\
        $hd

montage -trim $ma \
        -trim $mb \
        -trim $md \
        -trim $mag \
        -trim $mbg \
        -trim $mdg \
        -trim $ha \
        -trim $hb \
        -trim $hd \
        -geometry 350x200 -tile 3x3 shotnoise.png

convert -trim shotnoise.png shotnoise.png

display shotnoise.png
