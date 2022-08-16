#!/bin/bash
module load nco/4.7.9

#indir=/glade/campaign/cgd/ccr/jet/nanr_forKatie/3hrly/b.e13.B20TRC5CN.ne120_g16.003/*h3.PRECT*
#indir=/glade/campaign/cgd/ccr/jet/nanr_forKatie/3hrly/b.e13.B20TRC5CN.ne120_g16.003/*h3.PRECT.200[2-5]*
#indir=/glade/scratch/kdagon/FrontDetector/B20TRC5CN/*U300*
#indir=/glade/scratch/kdagon/FrontDetector/B20TRC5CN/*Z300*
indir=/glade/scratch/kdagon/FrontDetector/B20TRC5CN/*Z500*
outdir=/glade/campaign/cgd/ccr/kdagon/dlfront/B20TRC5CN

cd $outdir
map=/glade/work/nanr/mapfiles/map_ne120_to_0.23x0.31_bilinear.nc

for FILE in $indir
do filename=$(basename -- $FILE)
ncremap -m $map -i ${FILE} -o "${filename%.*}".regrid_0.23x0.31.nc
done
