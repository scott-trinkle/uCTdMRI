#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem4

python < deg75.py
