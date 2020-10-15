#!/bin/bash -f
##


d1=080904
d2=081016
m1=particles_size_comparison_41.png

ma=fig41${d1}ht.png
mb=fig14${d1}ht.png

mc=fig41${d2}ht.png
md=fig14${d2}ht.png


na=fig41${d1}lat.png
nb=fig14${d1}lat.png

nc=fig41${d2}lat.png
nd=fig14${d2}lat.png


for nm in $m1 $ma $mb $mc $md $me $mf
do
  cp ../$nm ./
done

for nm in $na $nb $nc $nd $ne $nf
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


convert \( $ma $na  +append \) \
        \( $mb $nb  +append \) \
        \( $mc $nc  +append \) \
        \( $md $nd  +append \) \
        -append parsizeb.png
 
display parsizeb.png

cp $m1 parsizea.png

display parsizea.png

#convert -trim feature.png feature.png

