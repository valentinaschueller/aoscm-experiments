#!/bin/bash
#SBATCH --job-name=top4    # create a short name for your job
#SBATCH -N 1 
#SBATCH --mail-user=valentina.schuller@math.lu.se
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH -t 00:40:00          # total run time limit (HH:MM:SS)

python3 top_case_ece4.py