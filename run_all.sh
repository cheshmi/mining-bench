#!/bin/sh

sw=$1



if [ ! -f "sparse.sif" ] 
then
	echo "Downloading image ..."
	singularity pull sparse.sif library://kazem/kazem/artifact22:latest 
else
	echo "image is already there!"	
fi


if [ ! -d "mm" ] 
then
    python ssgetpy/dl_matrices.py
else
	echo "General matrices are already there!"
fi

if [ ! -d "SPD" ] 
then
    python ssgetpy/dl_SPD_matrices.py
else
	echo "SPD matrices are already there!"
fi



## check whether matrix folder is created
if [ -d "mm" ] && [ -d "SPD" ]
then
    echo "Matrix directory found, running kernels ..." 
else
    echo "Error: the matrix directories do not exist, terminating ..."
    exit 2
fi

if [ "$sw" ==  0 ]; then
	echo "Running SpTRSV job ..."
	bash run_sptrsv.sh

	echo "Running SpMV job ..."
	bash run_spmv.sh 

	echo "Running SpMM jobs ..."
	bash run_spmm.sh 0
	bash run_spmm.sh 1
	bash run_spmm.sh 2
else
echo "Submitting jobs ..."
	sbatch run_sptrsv.sh
	sbatch run_spmv.sh 
	sbatch run_spmm.sh 0
	sbatch run_spmm.sh 1
	sbatch run_spmm.sh 2
	echo "Jobs are running, you can come back in 7 hrs and run the plotting script to see graphs..."
fi	


