#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem2

python < deg45.py
