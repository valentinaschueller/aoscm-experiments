#!/bin/bash
#SBATCH --job-name=top4    # create a short name for your job
#SBATCH -N 1 
#SBATCH --mail-user=valentina.schuller@math.lu.se
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH -t 00:35:00          # total run time limit (HH:MM:SS)

python3 mosaic_spring_ece4.py