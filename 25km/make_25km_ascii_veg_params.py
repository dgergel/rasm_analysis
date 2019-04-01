#!/bin/env python 

import numpy as np
import argparse
import subprocess
from scipy.spatial import cKDTree
import os
from netCDF4 import Dataset, default_fillvals

# define fill value 
FILL_VALUE = -9999
NC_DOUBLE = 'f8'
FILLVALUE_F = default_fillvals[NC_DOUBLE]

import pandas as pd
import xarray as xr

from collections import OrderedDict

# import NetCDF params file
direc = '/p/home/gergel/data/25km'
ncparams_25km_filename = "vic_params_wr25b_vic4.dev_20180307.nc"
ncparams_25km = os.path.join(direc, ncparams_25km_filename)

soil_50km = pd.read_csv(os.path.join(direc, 'rasm.vic.soil.1090.20140818'), 
                       delim_whitespace=True, 
                       index_col=None,
                       header=None
                       )

veg_50km = pd.read_csv(os.path.join(direc,
                                      'veg_param_wr50a.100924'),
                       sep='\t',
                       header=None)

domain_25km_filename = 'domain.lnd.wr25b_ar9v4.170413.nc'
domain_25km = xr.open_dataset(os.path.join('/p/home/gergel/data/RASM_land_masks', 
                                           domain_25km_filename))
lon_25km = domain_25km['xc'].values
lat_25km = domain_25km['yc'].values
mask_25km = domain_25km['mask'].values

domain_50km_filename = 'domain.lnd.wr50a_ar9v4.100920.nc'
domain_50km = xr.open_dataset(os.path.join('/p/home/gergel/data/RASM_land_masks', 
                                           domain_50km_filename))
lon_50km = domain_50km['xc'].values
lat_50km = domain_50km['yc'].values
mask_50km = domain_50km['mask'].values

def lon_lat_to_cartesian(lon, lat, R = 1):
    """
    calculates lon, lat coordinates of a point on a sphere with
    radius R
    """
    lon_r = np.radians(lon)
    lat_r = np.radians(lat)

    x = R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)

    return x, y, z

# lon, lat from coarser res data
xs, ys, zs = lon_lat_to_cartesian(lon_50km.flatten(), lat_50km.flatten()) 

# lon, lat from higher res data
xt, yt, zt = lon_lat_to_cartesian(lon_25km.flatten(), lat_25km.flatten())

# build KD tree
zipped_50km = np.dstack(([xs, ys, zs]))[0]
tree = cKDTree(zipped_50km)

# find indices of the nearest neighbors in the flattened array 
zipped_25km = np.dstack(([xt, yt, zt]))[0]
d, inds = tree.query(zipped_25km, k=1)

num_columns = len(soil_50km.columns)
for column in range(num_columns):
    var_50km = soil_50km[soil_50km.columns[column]].values.reshape(205, 275)
    nearest_var = var_50km.flatten()[inds]

# create gridcell numbers array for first column of soil parameters
gridcell_nums_25km = np.linspace(1, len(nearest_var), num=len(nearest_var), dtype='int')

# create veg parameter file
veg_50km_split = veg_50km.iloc[:, 0].str.split(' ', expand=True)
veg_50km_split.rename(columns={ veg_50km_split.columns[0]: "gridcell_number" }, inplace=True)

veg_params = OrderedDict()

# array of 25km gridcell nums: gridcell_nums_25km
# array of nearest neighbor indices: inds
# veg param gridcells go from 1-56375. So nearest neighbor gridcells are inds + 1
nn_gridcells = inds + 1

veg_params_row_count = 0
for i, num_gc_25km in enumerate(gridcell_nums_25km):
    nn_gc = nn_gridcells[i]
    
    if nn_gc <= 34: 
        veg_params[veg_params_row_count] = np.array('%s 0' %num_gc_25km)
        veg_params_row_count += 1
    elif (nn_gc > 34):
        row_num = veg_50km_split[veg_50km_split['gridcell_number'].values == str(nn_gc)].index[0]
        active_veg_types = veg_50km.values[row_num][0].split()[1]
        
        if active_veg_types == '0':
            veg_params[veg_params_row_count] = np.array('%s 0' %num_gc_25km)
            veg_params_row_count += 1
        else: 
            veg_params[veg_params_row_count] = np.array('%s %s' %(num_gc_25km, active_veg_types))
            veg_params_row_count += 1
            param_loop_num = row_num + 1
            while len(veg_50km.values[param_loop_num][0].split()) > 2:
                veg_params[veg_params_row_count] = veg_50km.values[param_loop_num][0]
                param_loop_num += 1
                veg_params_row_count += 1

df_veg_params = pd.DataFrame.from_dict(veg_params, orient='index')

direc = '/p/home/gergel/data/25km'
df_veg_params.to_csv(os.path.join(direc, 'veg_params_20190327.txt'), index=False, header=False)
print("finished making veg parameter file")
