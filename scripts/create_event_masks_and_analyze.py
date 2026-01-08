import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("/glade/work/tking/cgnet/ClimateNet")  # append path to ClimateNet repo
from climatenet.utils.data import ClimateDatasetLabeled, ClimateDataset
from climatenet.models import CGNet
from climatenet.utils.utils import Config
from climatenet.track_events import track_events
from climatenet.analyze_events import analyze_events
from climatenet.just_polar_plots_analyze_events import just_polar_plots_analyze_events
from climatenet.visualize_events import visualize_events

from os import path
import torch

os.chdir("/glade/work/tking/cgnet/ML-extremes/trained_models/config_062024_TMQ_new_mean_std/")

config = Config('config.json')
cgnet = CGNet(config)

train_path = '/glade/work/tking/cgnet/QA_xml/all_antarctic_converted_masks/split_files'

train = ClimateDatasetLabeled(path.join(train_path+'/train'), config)
test = ClimateDatasetLabeled(path.join(train_path+'/test'), config)

cgnet.load_model('/glade/work/tking/cgnet/ML-extremes/trained_models/trained_cgnet.032824_TMQ_unweighted_mean_std')
test_path = train_path+"/test"
test_data = ClimateDataset(test_path, config)
test_masks = cgnet.predict(test_data)
year=2000
inference_path = '/glade/derecho/scratch/tking/cgnet/high_lat_QC/from_nersc/2dlatlon/polar/renamed/tmq/formatted_for_inference/split_xy/'
inference = ClimateDataset(inference_path, config)

class_masks = cgnet.predict(inference) # takes ~40 min
class_masks.to_netcdf("/glade/derecho/scratch/tking/cgnet/masks_all_inference_data/class_masks_new_mean."+str(year)+".nc")

event_masks = track_events(class_masks) # TENDS TO TIME OUT HERE
event_masks.to_netcdf("/glade/derecho/scratch/tking/cgnet/masks_all_inference_data/event_masks_new_mean."+str(year)+".test.nc")

from importlib import reload
import climatenet.just_polar_plots_analyze_events

reload(climatenet.just_polar_plots_analyze_events)

climatenet.just_polar_plots_analyze_events.just_polar_plots_analyze_events(event_masks, class_masks, "/glade/derecho/scratch/tking/cgnet/")

# see results in /glade/derecho/scratch/tking/cgnet/

