# ML-extremes
This repository provides code to investigate machine learning (ML)-based detection of weather features such as fronts, atmospheric rivers, and tropical cyclones in climate model simulations with the [Community Earth System Model (CESM)](https://github.com/ESCOMP/CESM), and analyze the association of these features with extreme precipitation.

The code for frontal analysis and frontal precipitation was developed as part of a publication Dagon et al. (2022):

Dagon, K., J. Truesdale, J.C. Biard, K.E. Kunkel, G.A. Meehl, and M.J. Molina (2022), Machine learning-based detection of weather fronts and associated extreme precipitation in historical and future climates, Journal of Geophysical Research: Atmospheres, 127, e2022JD037038, [doi:10.1029/2022JD037038](https://doi.org/10.1029/2022JD037038). 

## Python Environment

The `environment.yml` file can be used to create the conda environment that was used in this analysis.

## Notebooks

The `notebooks` folder contains code to analyze and visualize detected features in observations, reanalysis data, and CESM output. It also contains scripts to analyze related precipitation and circulation output from the climate model.

* The `DLFront` folder contains code to analyze detected fronts via [DL-FRONT](https://doi.org/10.5194/ascmo-5-147-2019).
  * `Boostrap_*.ipynb`: Conduct bootstrap resampling tests on changes in precipitation and frontal precipitation.
  * `DLFront_*.ipynb`: Analyze fronts with and without additional climate model output.
  * `PrecipExtremes.ipynb`: Analyze extreme precipitation output from CESM.
* The `PolarARs` folder contains code to train polar versions of CGNet to detect atmospheric rivers.
* Other notebooks include the following:
  * `cgnet_*.ipnb`: Training and evaluating [CGNet/ClimateNet](https://github.com/andregraubner/ClimateNet) to detect atmospheric rivers and tropical cyclones.
  * `ClimateNet*.ipynb`: Analyze detected atmospheric rivers and tropical cyclones with and without additional climate model output.
  * `Data_Processing_*.ipynb`: Process CESM output for input to CGNet.
  * `get_averages_and_standard_devs.ipynb`: Calculate means and standard deviations for input to CGNet.



## Scripts

The `scripts` folder contains code to post-process CESM output.

* `regrid_ne120.sh`: Regrid the CESM output via bilinear interpolation.
* `uvlev_func.ncl`: Extract CESM u/v winds on specific pressure levels.
* `zlev_func.ncl`: Extract CESM geopotential height on specific pressure levels.

  
## Trained Models

The `trained_models` folder contains config files and weights for different trained versions of CGNet.
