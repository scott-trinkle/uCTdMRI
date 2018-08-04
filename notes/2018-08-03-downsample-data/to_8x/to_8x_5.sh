#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bignode3


outfile=to_8x_5.out

runhost="$(hostname | cut -f1 -d.)"
rundate="$(date '+ %m/%d/%y %H:%M')"
echo "Batch job started on $runhost on $rundate" > $outfile

python to_8x_5.py >> $outfile

echo "Batch job completed on $rundate" >> $outfile
