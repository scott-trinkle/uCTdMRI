#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem4

python < r12.py
