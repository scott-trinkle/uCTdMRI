#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem3

runhost="$(hostname | cut -f1 -d.)"
rundate="$(date '+ %m/%d/%y %H:%M')"
echo "Batch job started on $runhost on $rundate" > $outfile

regname=deformable_150
outfile=$regname.out 
mri=raw_data_masked_b0.nii.gz
xray=xray_150um_masked.nii.gz
threads=8
transform=s
precision=d

antsRegistrationSyN.sh -d 3 -f $mri -m $xray -o $regname -n $threads -t $transform -p $precision >> $outfile
