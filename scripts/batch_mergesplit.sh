#!/bin/bash -l
#PBS -N mergesplit_hist
#PBS -A P93300313
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=6:00:00
#PBS -q casper
#PBS -m abe
#PBS -M tking@ucar.edu

module load nco/4.7.9

sh mergesplit_script
