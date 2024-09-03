#!/bin/bash
#SBATCH --job-name=cex    # create a short name for your job
#SBATCH --mail-user=valentina.schuller@math.lu.se
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH -N 1 
#SBATCH -t 00:20:00          # total run time limit (HH:MM:SS)

python control_experiment_ece4.py