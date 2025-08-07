import xarray as xr
import numpy as np
import dask.array as da
from dask import delayed, compute
from scipy.ndimage import zoom
import sys

def crop_zoom_2d(array, margin):
    """Crop around center and zoom back to original size."""
    ny, nx = array.shape
    cy, cx = ny // 2, nx // 2
    cropped = array[cy - margin:cy + margin, cx - margin:cx + margin]
    zoom_factors = (ny / (2 * margin), nx / (2 * margin))
    return zoom(cropped, zoom_factors, order=1)

@delayed
def process_single_time_step(array, time_val, var_name, dims, attrs, margin):
    cropped = crop_zoom_2d(array, margin)
    da_out = xr.DataArray(
        cropped,
        dims=dims,
        attrs=attrs,
        coords={"time": time_val},
        name=var_name,
    )
    return da_out

def main(input_path, output_path, margin=450):
    ds = xr.open_dataset(input_path, chunks={"time": 1})
    var_name = "ivt"
    var = ds[var_name]

    ny, nx = ds.sizes["lat"], ds.sizes["lon"]
    cy, cx = ny // 2, nx // 2

    # Crop and zoom lat/lon if 2D
    lat_cropped = lon_cropped = None
    if "lat" in ds and ds["lat"].ndim == 2:
        lat_cropped = crop_zoom_2d(ds["lat"].values, margin)
    elif "latitude" in ds and ds["latitude"].ndim == 2:
        lat_cropped = crop_zoom_2d(ds["latitude"].values, margin)

    if "lon" in ds and ds["lon"].ndim == 2:
        lon_cropped = crop_zoom_2d(ds["lon"].values, margin)
    elif "longitude" in ds and ds["longitude"].ndim == 2:
        lon_cropped = crop_zoom_2d(ds["longitude"].values, margin)

    # Launch parallel processing
    tasks = []
    for t in range(ds.dims["time"]):
        array_t = var.isel(time=t).load().values  # avoid lazy Dask chunks inside delayed
        time_val = ds["time"].isel(time=t).values
        task = process_single_time_step(
            array_t, time_val, var_name, dims=("lat", "lon"), attrs=var.attrs, margin=margin
        )
        tasks.append(task)

    results = compute(*tasks)
    ivt_cropped = xr.concat(results, dim="time")
    ivt_cropped["time"] = ds["time"]

    # Final dataset
    cropped_ds = xr.Dataset({var_name: ivt_cropped})
    cropped_ds.attrs = ds.attrs

    # Add lat/lon coordinates
    cropped_ds = cropped_ds.assign_coords({
      "latitude": (("lat", "lon"), lat_cropped),
      "longitude": (("lat", "lon"), lon_cropped)
    })

    if lat_cropped is not None:
        cropped_ds["latitude"] = (("lat", "lon"), lat_cropped)
        cropped_ds["latitude"].attrs = ds.get("lat", ds.get("latitude")).attrs
    if lon_cropped is not None:
        cropped_ds["longitude"] = (("lat", "lon"), lon_cropped)
        cropped_ds["longitude"].attrs = ds.get("lon", ds.get("longitude")).attrs

    cropped_ds.to_netcdf(output_path)
    print("saved to:")
    print(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input.nc output.nc [margin]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    margin = int(sys.argv[3]) if len(sys.argv) > 3 else 450

    main(input_file, output_file, margin)
