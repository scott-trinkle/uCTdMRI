#!/bin/bash
#SBATCH --job-name=jobname
#SBATCH --output=jobname.out
#SBATCH --error=jobname.err
#SBATCH --time=12:00:00
#SBATCH --partition=bigmem
#SBATCH --constraint=1024G
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=25000

module load ANTs/2.1
export ANTSPATH="/software/ANTs-2.1-el6-x86_64/bin"
