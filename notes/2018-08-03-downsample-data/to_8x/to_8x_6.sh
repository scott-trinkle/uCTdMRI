#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bignode4


outfile=to_8x_6.out

runhost="$(hostname | cut -f1 -d.)"
rundate="$(date '+ %m/%d/%y %H:%M')"
echo "Batch job started on $runhost on $rundate" > $outfile

python to_8x_6.py >> $outfile

echo "Batch job completed on $rundate" >> $outfile
