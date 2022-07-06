#!/bin/sh



source common.sh


cat $LOGS/spmm_grp0.csv > $LOGS/spmm_all.csv
cat $LOGS/spmm_grp1.csv > $LOGS/spmm_all.csv
cat $LOGS/spmm_grp2.csv > $LOGS/spmm_all.csv
python3 plot_spmm.py $LOGS/spmm_all.csv


python3 plot_spmv.py $LOGS/spmv_all.csv
#python3 speedup_stacked_spmv.py $LOGS/spmv_all.csv


python3 plot_sptrsv.py $LOGS/sptrsv_all.csv
#python3 speedup_stacked_sptrsv.py $LOGS/sptrsv_$CURRENT_TIME.csv