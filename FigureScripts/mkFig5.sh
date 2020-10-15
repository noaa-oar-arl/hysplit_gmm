#!/bin/bash -f
##

ma=cdumpA_slice151.png
mb=cdumpB_slice151.png
md=cdumpD_slice151.png

mag=concsA.png
mbg=concsB.png
mdg=concsD.png

ha=partA151.png
hb=partB151.png
hd=partD151.png

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
        -geometry 350x200 -tile 3x3 slice_comparison2.png

convert -trim slice_comparison2.png slice_comparison2.png

display slice_comparison2.png
