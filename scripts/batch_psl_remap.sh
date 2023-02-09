#!/bin/bash -l
#PBS -N remap_psl
#PBS -A P93300313
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=6:00:00
#PBS -q casper
#PBS -m abe
#PBS -M tking@ucar.edu

# This script can be used to submit batch ncremap scripts, such as those in the example psl_remap_script.
# Check the status of this script after it is submitted with `qstat -u tking`.
# Please use your own account after `-A`, and update with your email to get notifications.
# It is also recommended to update the name of the script and jobname when submitting for other variables.
 
module load nco/4.7.9

sh psl_remap_script
