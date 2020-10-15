#!/bin/bash -f
##

ma=tfitht.00.png
mb=tfitht.06.png
mc=tfitht.12.png
md=tfitht.18.png
me=tfitht.23.png

na=tfitlat.00.png
nb=tfitlat.06.png
nc=tfitlat.12.png
nd=tfitlat.18.png
ne=tfitlat.23.png

ta=track.png
tb=3dtrack.png
tc=feature_legend.png



for nm in $ma $mb $mc $md $me $mf
do
  cp ../$nm ./
done
for nm in $na $nb $nc $nd $ne $nf
do
  cp ../$nm ./
done
for nm in $ta $tb $tc
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


convert \( $na $nc $ne +append \) \
        \( $ma $mc $me +append \) \
        \( $ta $tb $tc +append \) \
        -append feature.png
 


#convert -trim feature.png feature.png

display feature.png
