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


SW=$1


source common.sh



mkdir $LOGS
if [ "$SW" ==  0 ]; then
	echo "running group 0 of SpMM"
	bash $SCRIPTPATH/run_exp.sh "${BINPATH}/spmm_demo" 4 "${NUM_THREAD}"  "${MAT_DIR}" "${SPD_MAT_DIR}" > $LOGS/spmm_grp0.csv
fi

if [ "$SW" ==  1 ]; then
	echo "running group 1 of SpMM"
	bash $SCRIPTPATH/run_exp.sh "${BINPATH}/spmm_demo" 5 "${NUM_THREAD}"  "${MAT_DIR}" "${SPD_MAT_DIR}" > $LOGS/spmm_grp1.csv
fi

if [ "$SW" ==  2 ]; then
	echo "running group 2 of SpMM"
	bash $SCRIPTPATH/run_exp.sh "${BINPATH}/spmm_demo" 6 "${NUM_THREAD}"  "${MAT_DIR}" "${SPD_MAT_DIR}" > $LOGS/spmm_grp2.csv
fi
