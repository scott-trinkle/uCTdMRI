#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem1

python < deg25.py
