#!/bin/bash
#PBS -N veg_param
#PBS -q standard
#PBS -A NPSCA07935YF5
#PBS -l select=2:ncpus=32:mpiprocs=8
#PBS -l walltime=10:00:00
#PBS -j oe
#PBS -M gergel@uw.edu
#PBS -m abe

source /p/home/gergel/.bashrc
source activate pangeo_onyx 

python /p/home/gergel/scripts/make_25km_ascii_veg_params.py

