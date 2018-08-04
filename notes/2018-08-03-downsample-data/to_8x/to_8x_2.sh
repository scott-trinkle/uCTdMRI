#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem2


outfile=to_8x_2.out

runhost="$(hostname | cut -f1 -d.)"
rundate="$(date '+ %m/%d/%y %H:%M')"
echo "Batch job started on $runhost on $rundate" > $outfile

python to_8x_2.py >> $outfile

echo "Batch job completed on $rundate" >> $outfile
