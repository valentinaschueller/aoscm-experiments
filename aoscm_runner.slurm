#!/bin/bash
#SBATCH -N 1 
#SBATCH --ntasks-per-node=2

#SBATCH -t 00:55:00
#SBATCH --job-name=mosaic
#SBATCH --mail-user=valentina.schuller@math.lu.se
#SBATCH --mail-type=BEGIN,END,FAIL

python mosaic_spring_ece4.py