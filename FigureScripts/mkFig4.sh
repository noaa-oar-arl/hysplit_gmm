#!/bin/bash -f
##

ma=mass_kasatochi_cdumpA.png
mb=mass_kasatochi_cdumpB.png
mc=mass_kasatochi_cdumpC.png
md=mass_kasatochi_cdumpD.png

mag=mass_kasatochi_gmm_A50.png
mbg=mass_kasatochi_gmm_B50.png
mbd=mass_kasatochi_gmm_D50.png

ha=hist_cdumpA.png
hb=hist_cdumpA_cdumpB.png
hd=hist_cdumpA_cdumpD.png
hag=hist_cdumpA_gmm_A50.png
hbg=hist_cdumpA_gmm_B50.png
hdg=hist_cdumpA_gmm_D50.png

for nm in $ha $hb $hd $hag $hbg $hdg
do
  cp ../$nm ./
done

for nm in $ma $mb $mc $md $mag $mbg $mbd
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
        -trim $ha \
        -trim $hb \
        -trim $hd \
        -trim $mag \
        -trim $mbg \
        -trim $mbd \
        -trim $hag \
        -trim $hbg \
        -trim $hdg \
        -geometry 350x200 -tile 3x5 kmass_comparison.png

convert -trim kmass_comparison.png kmass_comparison.png

display kmass_comparison.png
