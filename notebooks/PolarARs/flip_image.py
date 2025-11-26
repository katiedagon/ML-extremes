import xarray as xr
import sys

def flip_horizontally(input_file, output_file):
    # Open the dataset
    ds = xr.open_dataset(input_file)

    # Flip all 2D or 3D data variables along the last (horizontal) dimension
    flipped_vars = {}
    for var in ds.data_vars:
        data = ds[var]
        if data.ndim >= 2:
            flipped_vars[var] = data.isel({data.dims[-1]: slice(None, None, -1)})
        else:
            flipped_vars[var] = data  # Leave 1D variables untouched

    # Create new dataset
    ds_flipped = ds.copy()
    for var, data in flipped_vars.items():
        ds_flipped[var] = data

    # Write to output
    ds_flipped.to_netcdf(output_file)
    print(f"Saved flipped file to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flip_image.py <input_file.nc> <output_file.nc>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    flip_horizontally(input_file, output_file)
