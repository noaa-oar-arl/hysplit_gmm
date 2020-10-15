#!/bin/bash -f
##

cp ../C10gmm_apart_1.png ./
cp ../C4gmm_apart_1.png ./
cp ../C4gmm_together_1.png ./

fa=runCfit10gmm.png
fb=runCfit4gmm.png
fc=runCfit4gmm_together.png
pntsz=20
lfh=110

fd=C10gmm_apart_1.png
fe=C4gmm_apart_1.png
ff=C4gmm_together_1.png


convert $fa -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -$lfh+50 '(a) n=10' \
        fita.png
convert $fb -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -$lfh+50 '(b) n=4' \
        fitb.png
convert $fc -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -$lfh+50 '(c) n=4' \
        fitc.png
convert $fd -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -$lfh+50 '(d)' \
        fitd.png
convert $fe -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -$lfh+50 '(e)' \
        fite.png
convert $ff -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -$lfh+50 '(f)' \
        fitf.png



montage  -trim fita.png \
         -trim fitb.png \
         -trim fitc.png \
        -geometry 400x300 -tile 3x1 figfit_a.png

montage  -trim fita.png \
         -trim fitb.png \
         -trim fitc.png \
         -trim fitd.png \
         -trim fite.png \
         -trim fitf.png \
        -geometry 400x300 -tile 3x2 figfit_b.png


display figfit_a.png
display figfit_b.png
#exit 1

