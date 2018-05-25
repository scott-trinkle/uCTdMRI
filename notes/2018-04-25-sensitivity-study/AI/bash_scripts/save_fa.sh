#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem3

python < save_FA.py
