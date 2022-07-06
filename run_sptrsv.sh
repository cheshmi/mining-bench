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



source common.sh

mkdir $LOGS
bash run_exp.sh 

bash "${SCRIPTPATH}"/run_exp.sh "${BINPATH}"/sptrsv_demo   2 "${NUM_THREAD}"  "${MAT_DIR}" "${SPD_MAT_DIR}" > $LOGS/sptrsv_all.csv
echo "Done SpTRSV"

