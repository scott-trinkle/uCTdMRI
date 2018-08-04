#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem4


outfile=to_8x_4.out

runhost="$(hostname | cut -f1 -d.)"
rundate="$(date '+ %m/%d/%y %H:%M')"
echo "Batch job started on $runhost on $rundate" > $outfile

python to_8x_4.py >> $outfile

echo "Batch job completed on $rundate" >> $outfile
