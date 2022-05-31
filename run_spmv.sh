#!/bin/sh

#SBATCH --cpus-per-task=40
#SBATCH --export=ALL
#SBATCH --job-name="TRSV"
#SBATCH --mail-type=begin  # email me when the job starts
#SBATCH --mail-type=end    # email me when the job finishes
#SBATCH --nodes=1
#SBATCH --output="DDT.%j.%N.out"
#SBATCH -t 12:00:00

#### NOTE #####
# ######################################
# ######################################
# ######################################
# ######################################
# ######################################
# ######################################
#
# THIS SCRIPT ASSUMES THE BINARY FILES ARE COMPILED
#
# ######################################
# ######################################
# ######################################
# ######################################
# ######################################
# ######################################
# ######################################



BINPATH="singularity exec sparse.sif /source/codelet_mining/build/demo"
LOGS=./logs 
SCRIPTPATH=./
MAT_DIR=./mm
SPD_MAT_DIR=./SPD

CURRENT_TIME=$(date +%s)

mkdir $LOGS
bash $SCRIPTPATH/run_exp.sh "${BINPATH}/spmv_demo"  3 20  "${MAT_DIR}" "${SPD_MAT_DIR}" > $LOGS/spmv_$CURRENT_TIME.csv