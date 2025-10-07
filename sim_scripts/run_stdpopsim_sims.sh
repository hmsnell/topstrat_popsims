#!/bin/bash

#SBATCH -J stdpopsim_neutral			# name
#SBATCH -N 1 						# all cores are on one node
#SBATCH -n 1                        # cores
#SBATCH -t 2-0 					    # time 2hrs per job days	
#SBATCH --mem 10G 				    # memory
#SBATCH --array=105            # array jobs

module load python
module load slim
source ~/venv/stdpopsim/bin/activate

python ../scripts/neutral_stdpopsim.py $SLURM_ARRAY_TASK_ID

