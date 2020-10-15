#!/bin/bash -f
##

fnn=B30gmm_apart_1.png
fii=B30gmm_together_1.png
#C10gmm_apart_1.png
fmm=C10gmm_together_1.png
fj10=C30gmm_apart_1.png
#C30gmm_together_1.png
fja=C4gmm_apart_1.png
fjb=C4gmm_together_1.png

#250,000 particles
fa=example1_0.png
#50,000 particles
fb=example1_1.png
#5,000 particles
fcc=example1_2.png

#blank
#50,000 particles low resolution
fd=example1_4.png

#5,0000 particles
fe=example1_3.png

cp ../A30gmm_together_1.png ./
cp ../B30gmm_together_1.png ./
cp ../C30gmm_together_1.png ./
cp ../C10gmm_together_1.png ./
cp ../A30gmm_apart_1.png ./
cp ../B30gmm_apart_1.png ./


#250,000
ff=A30gmm_together_1.png 
#50,000
fgg=B30gmm_together_1.png 
#5,000
fh=C30gmm_together_1.png 

#250,000
fii=A30gmm_apart_1.png 
#50,000
fj=B30gmm_apart_1.png 
#5,000
fk=C10gmm_together_1.png 

pntsz=20
pntsz2=30

convert $fa -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate -105+50 '(a) Run A' \
        -gravity north\
        -font Times-Roman -pointsize $pntsz2 -annotate +0+10 '250,000 particles' \
        fa.png

convert $fb -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate -105+50 '(b) Run B' \
        -gravity north\
        -font Times-Roman -pointsize $pntsz2 -annotate +0+10 '50,000 particles' \
        fb.png

convert $fcc -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate -105+50 '(c) Run C' \
        -gravity north\
        -font Times-Roman -pointsize $pntsz2 -annotate +0+10 '5,000 particles' \
        fc.png

convert $fd -gravity north\
        -font Times-Roman -pointsize $pntsz\
        -annotate -105+50 '(d) Run E' \
        fd.png

convert $fe -gravity north\
        -font Times-Roman -pointsize $pntsz -annotate -105+50 '(e) Run D' \
        fe.png

#--------------------------------------------------------------

convert $ff -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -90+50 '(f) GMM n=30' \
        ff.png

convert $fgg -gravity north\
        -font Times-Roman -pointsize $pntsz\
        -annotate -90+50 '(g) GMM n=30' \
        fgg.png


convert $fh -gravity north\
        -font Times-Roman -pointsize $pntsz\
        -annotate -90+50 '(h) GMM n=30' \
        fh.png

convert $fii -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -90+50 '(i) GMM n=30' \
        fii.png

convert $fj -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -90+50 '(j) GMM n=30' \
        fj.png

convert $fk -gravity north\
        -font Times-Roman -pointsize $pntsz \
        -annotate -90+50 '(k) GMM n=10' \
        fk.png







identify 
convert -size 432x288 xc:transparent blank.png
pntsz=32

montage -trim fa.png \
        -trim fb.png \
        -trim fc.png \
        -trim blank.png \
        -trim fd.png\
        -trim fe.png\
        -trim ff.png\
        -trim fgg.png\
        -trim fh.png\
        -trim fii.png\
        -trim fj.png\
        -trim fk.png\
        -geometry 300x200 -tile 3x4 captex1_comparison.png

display captex1_comparison.png
