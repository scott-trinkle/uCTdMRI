#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=HOSTNAME

runhost="$(hostname | cut -f1 -d.)"
rundate="$(date '+ %m/%d/%y %H:%M')"
echo "Batch job started on $runhost on $rundate" > $outfile
