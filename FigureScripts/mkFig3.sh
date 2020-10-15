#!/bin/bash -f
##



cp ../rank.png ./
cp ../FB.png ./
cp ../KS.png ./
cp ../Rauto.png ./
cp ../FMS.png ./
cp ../RMSE.png ./
cp ../rank_legenda.png ./
cp ../rank_legendb.png ./
cp ../rank_legendc.png ./

fa='rank.png'
fb='FB.png'
fe='Rauto.png'
fcc='KS.png'
fd='FMS.png'
ff='RMSE.png'

pntsz=20
pntsz2=30
lfh=+110

rm fa.png
rm fb.png
rm fc.png
rm fd.png
rm fe.png
rm ff.png
rm stats.png

convert $fa -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $lfh+50 '(a)' \
        fa.png

convert $fb -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $lfh+50 '(b)' \
        fb.png

convert $fcc -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $lfh+50 '(c)' \
        fc.png

convert $fd -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $lfh+50 '(d)' \
        fd.png

convert $fe -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $lfh+50 '(e)' \
        fe.png

convert $ff -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate $lfh+50 '(f)' \
        ff.png

#--------------------------------------------------------------
#--------------------------------------------------------------


#identify 
convert -size 432x288 xc:transparent blank.png
#pntsz=32

montage -trim fa.png \
        -trim fb.png \
        -trim fc.png \
        -trim fd.png\
        -trim fe.png\
        -trim ff.png\
        -geometry 600x350 -tile 2x3 stats.png

convert \( rank_legenda.png rank_legendb.png rank_legendc.png +append \) \
        legend.png

convert \( stats.png legend.png -append \) \
       out.png

display out.png

#display stats.png
