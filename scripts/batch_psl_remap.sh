#!/bin/bash -l
#PBS -N remap_psl
#PBS -A P93300313
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=6:00:00
#PBS -q casper
#PBS -m abe
#PBS -M tking@ucar.edu


#module load conda
module load nco/4.7.9
#/ncar/usr/jupyterhub.hpc.ucar.edu/jupyterhub-20220511/condabin/conda activate cgnet
#conda activate cgnet
#which conda

sh psl_remap_script
