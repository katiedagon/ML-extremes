import matplotlib as mpl
import glob
#mpl.use('Agg')
import os
#os.environ['PROJ_LIB'] = "/global/homes/a/amahesh/.conda/envs/plotting_env/share/proj"
import matplotlib.pyplot as plt
import h5py as h5
import mpl_toolkits as tk
import numpy as np
import netCDF4 as nc
import h5py as h5
from matplotlib.colors import ListedColormap
import pandas as pd
from mpl_toolkits.basemap import Basemap
import metpy.calc
from datetime import date
from datetime import datetime
import stat
from datetime import timedelta
import random
import stat

dpi = 96

def plot_mask_double(namedir, img_array, img_array2, storm_mask, plt_title, 
    my_cmap=None,my_cmap2=None, my_cmap3=None, u_wind=None, v_wind=None, 
    v_max=None, v_min=None,v_max2=None, v_min2=None, line=None, land=True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    #d = np.roll(d,[0,1152//2])
    
    d2 = img_array2
    #d2 = np.roll(d2,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(0, 360,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='npstere', boundinglat = 35, llcrnrlat=min(lats), lon_0=np.median(longs),
              llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c', fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contour(x_map,y_map,d,line,cmap=my_cmap, vmax=v_max, vmin=v_min)
        my_map.contourf(x_map,y_map,d2,64,cmap=my_cmap2, vmax=v_max2, vmin=v_min2)
        my_map.drawmeridians(np.arange(0, 360, 60), labels=[0,0,0,1])
        my_map.drawparallels(np.arange(-90, 90, 30), labels =[1,0,0,0])
        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap3)

        if (not land):
            # alpha was at 0.5 - SK change
            my_map.fillcontinents(alpha=0.1) 
        mask_ex = plt.gcf()
        path = namedir + "/" + plt_title
        mask_ex.savefig(path, dpi=dpi, quality=100,pad_inches = 0)
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH)
        plt.clf()

    # do_fig((1152/dpi,768/dpi))
    do_fig((1152/dpi,1152/dpi))

""" This is Sean's plotting function """
def plot_mask_flat(namedir ,img_array, storm_mask, plt_title, my_cmap=None, 
    my_cmap2 = None, u_wind=None, v_wind=None, 
    v_max=None, v_min=None, land=True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    #d = np.roll(d,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(0, 360,1152)

    def do_fig(figsize):

        fig = plt.figure(figsize=figsize,dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='npstere', boundinglat = 35, llcrnrlat=min(lats), lon_0=np.median(longs),
              llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c', fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contourf(x_map,y_map,d,64,cmap=my_cmap, vmax=v_max, vmin=v_min)
        my_map.drawmeridians(np.arange(0, 360, 60), labels=[0,0,0,1])
        my_map.drawparallels(np.arange(-90, 90, 30), labels =[1,0,0,0])
        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            gap = 10
            norm = mpl.colors.Normalize(vmin=0, vmax=20)
            my_map.quiver(x_map[::gap,::gap],y_map[::gap,::gap], u_wind[::gap,::gap], v_wind[::gap,::gap], wind_speed[::gap,::gap],
                alpha=0.9, cmap=my_cmap2, norm=norm, width=0.001, scale=650)
        
        if (not land):
             # alpha was at 0.5 - SK change
            my_map.fillcontinents(alpha=0.1)
        mask_ex = plt.gcf()
        path = namedir + "/" + plt_title
        mask_ex.savefig(path ,dpi=dpi,quality=100,pad_inches = 0)
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH)
        plt.clf()

    # do_fig((1152/dpi,768/dpi))
    do_fig((1152/dpi,1152/dpi))



""" Select files from folder to convert """

source_channels = ['ivt', 'prw', 'psl', 'u850', 'v850']
sourceName = ['windhusavi', 'prw', 'psl', 'ua850', 'va850']
sourceDir_path = '/global/project/projectdirs/ClimateNet/data/'
source = dict()
for c in source_channels:
    nc_fps_tmq = glob.glob(sourceDir_path + c + '/*.nc')
    nc_fps_tmq.sort()
    source[c] = nc_fps_tmq

output_channels = ['ivt', 'tmq', 'psl', 'psl_ivt', 'tmq_wind_850']
outputDir_path = '/global/project/projectdirs/ClimateNet/Images_polar/arctic/'

index = glob.glob('/global/project/projectdirs/ClimateNet/image_scripts/2003.txt')
# 2001 done
index.sort()

print(index)

for i, idx_txt in enumerate(index): # 2001 - 2003
    
    data_in_ivt = nc.Dataset(source['ivt'][i])
    IVT = data_in_ivt['windhusavi']
    data_in_prw = nc.Dataset(source['prw'][i])
    TMQ = data_in_prw['prw']
    data_in_psl = nc.Dataset(source['psl'][i])
    PSL = data_in_psl['psl']
    data_in_u850 = nc.Dataset(source['u850'][i])
    U850 = data_in_u850['ua850']
    data_in_v850 = nc.Dataset(source['v850'][i])
    V850 = data_in_v850['va850']

    f = open(idx_txt,"r")
    f1 = f.readlines()

    for x in f1:
        print(x)
        i, fn = x.split()
        """ plot IVT """
        plot_mask_flat(outputDir_path + 'ivt', IVT[int(i)], np.zeros((768, 1152)), fn, 
                       'viridis', v_max=1400,v_min=0, land=False)
        """ plot TMQ """
        plot_mask_flat(outputDir_path + 'tmq', TMQ[int(i)-1], np.zeros((768, 1152)), fn, 
                       'viridis', v_max=80,v_min=0, land=False)
        """ plot PSL """
        plot_mask_flat(outputDir_path + 'psl', PSL[int(i)-1], np.zeros((768, 1152)), fn, 
                       'viridis', v_max=101500,v_min=99000, land=False)
        """ plot IVT contour map + PSL contour line """
        plot_mask_double(outputDir_path + 'psl_ivt', PSL[int(i)-1], IVT[int(i)],
                        np.zeros((768, 1152)), fn, 'cool', 'viridis',
                        v_max=101500,v_min=99000,v_max2=1400, v_min2=0,
                        land=False, line=9)
        """ plot TMQ contour map + Wind quiver"""
        plot_mask_flat(outputDir_path + 'tmq_wind_850', TMQ[int(i)-1], 
                        np.zeros((768, 1152)), fn, 'viridis', my_cmap2=mpl.cm.autumn,
                        u_wind=U850[int(i)-1][0], v_wind=V850[int(i)-1][0], 
                        v_max=80,v_min=0, land=False)

    print("finish one yr", i)

