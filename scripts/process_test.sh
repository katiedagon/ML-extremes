#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Process timestep files into single year files with all 4 variables
ncrcat 2003* 2003_temp.nc # slow

# Remove long string of history attribute
ncatted -O -h -a history,global,o,c,"" 2003_temp.nc # fast

# Remove unnecessary variables and finalize file name
ncks -x -v ch4vmr,co2vmr,f11vmr,f12vmr,n2ovmr,sol_tsi 2003_temp.nc B20TRC5CN.PSL.TMQ.U850.V850.2003010100Z-2003123121Z.nc # slow

# Remove temp/timestep files
rm -f 2003*
