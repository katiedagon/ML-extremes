#!/bin/bash

set -e

for year in {2004..2005}; do
	echo ${year}
	ncrcat ${year}* ${year}_temp.nc
	ncatted -O -h -a history,global,o,c,"" ${year}_temp.nc
	ncks -x -v ch4vmr,co2vmr,f11vmr,f12vmr,n2ovmr,sol_tsi ${year}_temp.nc B20TRC5CN.PSL.TMQ.U850.V850.${year}010100Z-${year}123121Z.nc
	#rm -f ${year}*
done
