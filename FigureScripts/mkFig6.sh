#!/bin/bash -f
##

ma=cdumpA_slice.png
mb=cdumpB_slice.png
md=cdumpD_slice.png

mag=slice_gmmA.png
mbg=slice_gmmB.png
mdg=slice_gmmD.png

ha=partA.png
hb=partB.png
hd=partD.png

for nm in $ha $hb $hd $hag $hbg $hdg
do
  cp ../$nm ./
done

for nm in $ma $mb $mc $md $mag $mbg $mdg
do
  cp ../$nm ./
done

pntsz=20
pntsz2=30

#convert $ma -gravity north\
#        -font Times-Roman -pointsize $pntsz -annotate -140+50 '(a)' \
#        -gravity north\
#        -font Times-Roman -pointsize $pntsz2 -annotate +0+10 'Run KA'\
#        $ma

identify 
convert -size 432x288 xc:transparent blank.png
pntsz=32

montage -trim $ma \
        -trim $mb \
        -trim $md \
        -trim $mag \
        -trim $mbg \
        -trim $mdg \
        -trim $ha \
        -trim $hb \
        -trim $hd \
        -geometry 350x200 -tile 3x3 slice_comparison.png

convert -trim slice_comparison.png slice_comparison.png

display slice_comparison.png
