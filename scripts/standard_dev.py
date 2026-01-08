import xarray as xr
import numpy as np

inference_path = '/glade/derecho/scratch/tking/cgnet/high_lat_QC/from_nersc/2dlatlon/polar/renamed/tmq/formatted_for_inference/'
ds = xr.open_mfdataset(inference_path+"*.nc", concat_dim='time', combine='nested', parallel=True)
std = ds['tmq'].std().compute()


with open("/glade/u/home/tking/work/cgnet/ML-extremes/scripts/std.txt", "w") as file1:
    file1.write("{} \n".format(std))

print("standard deviation is:")
print(std)
