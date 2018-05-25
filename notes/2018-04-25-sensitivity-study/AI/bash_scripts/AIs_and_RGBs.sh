#!/bin/sh
#$ -j y
#$ -cwd
#$ -V
#$ -l h=bigmem4

python < save_AIs_and_RGB.py
