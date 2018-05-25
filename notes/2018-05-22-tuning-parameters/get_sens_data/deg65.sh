#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem3

python < deg65.py
