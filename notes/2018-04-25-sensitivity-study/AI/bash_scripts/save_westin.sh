#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem4

python < save_westin.py
