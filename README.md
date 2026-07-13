# ML-extremes
This repository provides code to investigate machine learning (ML)-based detection of weather features such as fronts, atmospheric rivers, and tropical cyclones in climate model simulations with the [Community Earth System Model (CESM)](https://github.com/ESCOMP/CESM), and analyze the association of these features with extreme precipitation.

The code for frontal analysis and frontal precipitation was developed as part of a publication Dagon et al. (2022):

Dagon, K., J. Truesdale, J.C. Biard, K.E. Kunkel, G.A. Meehl, and M.J. Molina (2022), Machine learning-based detection of weather fronts and associated extreme precipitation in historical and future climates, Journal of Geophysical Research: Atmospheres, 127, e2022JD037038, [doi:10.1029/2022JD037038](https://doi.org/10.1029/2022JD037038). 

The code for atmospheric river analysis was developed as part of a pre-print manuscript:

Dagon, K., T. King, C.A. Shields, J. Truesdale, S. Kim, K. Mayer, A. Graubner, A. Greiner, L. Kapp-Schwoerer, and K. Kashinath (Under Review), Investigating Western North America Atmospheric Rivers with Machine Learning-Based Detection, [doi:10.22541/essoar.15005316/v1](https://doi.org/10.22541/essoar.15005316/v1).

## Python Environment
The `envs` folder contains files that can be used to create the conda environments used in this analysis.
* `environment.yml` was used for frontal analysis
* `environment_v2.yml` was used for AR analysis

## Notebooks
The `notebooks` folder contains code to analyze and visualize detected features in observations, reanalysis data, and CESM output. It also contains scripts to analyze related precipitation and circulation output from the climate model.

* The `DLFront` folder contains code to analyze detected fronts via [DL-FRONT](https://doi.org/10.5194/ascmo-5-147-2019).
  * `Boostrap_*.ipynb`: Conduct bootstrap resampling tests on changes in precipitation and frontal precipitation.
  * `DLFront_*.ipynb`: Analyze fronts with and without additional climate model output.
  * `PrecipExtremes.ipynb`: Analyze extreme precipitation output from CESM.
* The `CGNet` folder contains code to generate and analyze atmospheric rivers (ARs) and tropical cyclones (TCs) via [CGNet/ClimateNet](https://github.com/andregraubner/ClimateNet).
  * `cgnet_*.ipynb`: Preprocessing, training, inference, evaluation, and tracking with CGNet.
  * `ClimateNet_*.ipynb`: Analyze and visualize detected ARs and TCs in climate model output and reanalysis products.
  * `Data_Processing_*.ipynb`: Process CESM output for input to CGNet.
* The `PolarARs` folder contains code to train polar versions of CGNet to detect atmospheric rivers (work in progress).

## Scripts
The `scripts` folder contains code to post-process CESM output including regridding, renaming, splitting by time, and other tasks.
  
## Trained Models
The `trained_models` folder contains config files and weights for different trained versions of CGNet.
