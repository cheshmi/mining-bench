# mining-bench
Artifact Description for "vectorizing sparse matrix codes using partially strided codelets" at SC22.


# How to run the artifact

* The mining-bench repository should be cloned: 
```    
    git clone https://github.com/cheshmi/\\mining-bench.git
    cd mining-bench
```

* The singularity image should be pulled to the same directory that the code is cloned using: 
 ```
    singularity pull <link is provided in the AD>   
 ``` 
You can test the image by running the following command from the current directory:
```
singularity exec sparse.sif /source/codelet_mining/build/demo/spmv_demo --matrix ./LFAT5.mtx --numerical_operation SPMV --storage_format CSR

``` 
 The output is set of comma separated values such matrix specification and execution time of different tools. Also, plots will be created as PDF files upon completion of all experiments. 
    
    
* The datasets should be downloaded by calling:
```    
    python ssgetpy/dl_matrices.py
    python ssgetpy/dl_SPD_matrices.py
```    
Matrices are downloaded into the _mm_ and _SPD_ directories in the current directory (This might take several hours and requires internet connection).

* The SpMV experiment can be executed by emitting:
```
    bash run_spmv.sh
```
For running on compute node:
```
sbatch bash run_spmv.sh
```
You might need to update scripts with new absolute paths to the dataset and the image file.
    

* SpTRSV experiment can be done by running:
```
bash run_sptrsv.sh
```
    
* SpMM experiment can be reproduced by calling:
```
bash run_spmm.sh
```
    
* all results should be stored as CSV files under the _./logs/_ directory. Plots should be 
created in the current directory as PDF files. 