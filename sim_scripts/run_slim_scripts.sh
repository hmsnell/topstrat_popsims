#!/bin/bash

#SBATCH -J slim_admix_recomb		# name
#SBATCH -N 1 						# all cores are on one node
#SBATCH -n 1                        # cores
#SBATCH -t 2-0 					    # time 2hrs per job days	
#SBATCH --mem 20G 				    # memory
#SBATCH --array=1-100               # array jobs

module load python
module load slim
source ~/venv/stdpopsim/bin/activate

slim -d sim_num=$SLURM_ARRAY_TASK_ID -d N=1000 ../scripts/american_admixture_neutral.slim
#slim -d sim_num=$SLURM_ARRAY_TASK_ID ../scripts/2d_stepstone.slim