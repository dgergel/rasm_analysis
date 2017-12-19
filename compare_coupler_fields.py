#!/bin/env python

import matplotlib.pyplot as plt
import os 
import numpy as np
import pandas as pd 
import xarray as xr
from tonic.io import read_config, read_configobj

# read configs for filenames and diagnostics to run
config_files = read_config(os.path.join(os.getcwd(), 
                                            'filenames.cfg'))
config_diag = read_configobj(os.path.join(os.getcwd(), 
                                       'diagnostics.cfg'))

# full list of l2x coupler fields 

l2x_vars = ['l2x_Sl_t', 'l2x_Sl_tref', 'l2x_Sl_qref', 
            'l2x_Sl_avsdr','l2x_Sl_anidr', 'l2x_Sl_avsdf', 
            'l2x_Sl_anidf', 'l2x_Sl_snowh', 'l2x_Sl_u10', 
            'l2x_Sl_fv', 'l2x_Sl_ram1', 'l2x_Sl_logz0', 'l2x_Fall_taux',
            'l2x_Fall_tauy', 'l2x_Fall_lat', 'l2x_Fall_sen', 
            'l2x_Fall_lwup', 'l2x_Fall_evap', 'l2x_Fall_swnet', 
            'l2x_Fall_flxdst1', 'l2x_Fall_flxdst2',
            'l2x_Fall_flxdst3', 'l2x_Fall_flxdst4', 
            'l2x_Flrl_rofliq', 'l2x_Flrl_rofice']

l2x_units = ['K', 'K', 'g/g', 'fraction', 'fraction', 'fraction', 
             'fraction', 'm', 'm/s', 'm/s', 's/m', 'm', 'N/m2', 
             'N/m2', 'W/m2', 'W/m2', 'W/m2', 'kg/m2s', 'W/m2', 
             'm/s', 'm/s', 'm/s', 'm/s', 'kg/m2s', 'kg/m2s']

#l2x_vars = ['l2x_Sl_avsdr']
#l2x_units = ['fraction']
# make plots

# get compset for plot name
if 'RI' in config_files['filenames']['vic4']:
    compset = 'RI'
elif 'RBR' in config_files['filenames']['vic4']:
    compset = 'RBR'
elif 'RB' in config_files['filenames']['vic4']:
    compset = 'RB'
else: 
    raise TypeError("file compset has not yet been defined in the diagnostic script")

# plot settings 
fs = 10
dpi = 50

# open files and check that they exist as in config file
vic4_file = os.path.join(os.getcwd(), 
                         'coupler_hist_files', 
                         config_files['filenames']['vic4'])
vic5_file = os.path.join(os.getcwd(),
                         'coupler_hist_files',
                         config_files['filenames']['vic5'])
if os.path.isfile(vic4_file) and os.path.isfile(vic5_file): 
    vic4 = xr.open_dataset(os.path.join(os.getcwd(), 
                                        'coupler_hist_files', 
                                        config_files['filenames']['vic4']))
    vic5 = xr.open_dataset(os.path.join(os.getcwd(), 
                                        'coupler_hist_files', 
                                        config_files['filenames']['vic5']))
else:
    raise IOError("Files Do Not Exist, Recheck Filenames Config File")


for plot_type in config_diag.items():
    for i, l2x_var in enumerate(l2x_vars):
        cbar_kwargs = {'label': l2x_units[i]}
        if plot_type[0] == "magnitudes" and config_diag['magnitudes']['options']['run']:
            print("plotting %s" %plot_type[0])
            fig, axs = plt.subplots(1, 2, figsize=(20, 8))
            vic4[l2x_var].plot(cmap='viridis', ax=axs[0], add_labels=False, cbar_kwargs=cbar_kwargs, 
                               robust=True)
            axs[0].set_title('VIC 4 %s CPL Hist File' %compset)
            vic5[l2x_var].plot(cmap='viridis', ax=axs[1], add_labels=False, cbar_kwargs=cbar_kwargs,
                               robust=True)
            axs[1].set_title('VIC 5 %s CPL Hist File' %compset)
        elif (plot_type[0] == "magnitudes_constrain_colorbar" and 
              config_diag['magnitudes_constrain_colorbar']['options']['run']):
            print("plotting %s" %plot_type[0])
            fig, axs = plt.subplots(1, 2, figsize=(20, 8))
            # get colorbar constraints
            if config_diag['magnitudes_constrain_colorbar']['options']['constrain_by'] == "vic4":
                vmin = vic4[l2x_var].min()
                vmax = vic4[l2x_var].max()
            elif config_diag['magnitudes_constrain_colorbar']['options']['constrain_by'] == "vic5":
                vmin = vic5[l2x_var].min()
                vmax = vic5[l2x_var].max()
            else: 
                raise TypeError("this colorbar constrain option is not yet an option, please reset config file")
            vic4[l2x_var].plot(cmap='viridis', ax=axs[0], add_labels=False, vmin=vmin, vmax=vmax, cbar_kwargs=cbar_kwargs)
            axs[0].set_title('VIC 4 %s CPL Hist File' %compset)
            vic5[l2x_var].plot(cmap='viridis', ax=axs[1], add_labels=False, vmin=vmin, vmax=vmax, cbar_kwargs=cbar_kwargs)
            axs[1].set_title('VIC 5 %s CPL Hist File' %compset)
        elif plot_type[0] == "difference" and config_diag['difference']['options']['run']:
            print("plotting %s" %plot_type[0])
            fig, axs = plt.subplots(1, 1, figsize=(10, 8))
            (vic5[l2x_var] - vic4[l2x_var]).plot(cmap='bwr', ax=axs, add_labels=False)
            axs.set_title('VIC 5 - VIC 4 %s CPL Hist Files' %compset, size=fs)
        elif plot_type[0] == "vic4" and config_diag['vic4']['options']['run']:
            print("plotting %s" %plot_type[0])
            fig, axs = plt.subplots(1, 1, figsize=(10, 8))
            vic4[l2x_var].plot(cmap='viridis', ax=axs, add_labels=False, cbar_kwargs=cbar_kwargs)
            axs.set_title('VIC 4 %s CPL Hist Files' %compset)
        elif plot_type[0] == "vic5" and config_diag['vic5']['options']['run']:
            print("plotting %s" %plot_type[0])
            fig, axs = plt.subplots(1, 1, figsize=(10, 8))
            vic5[l2x_var].plot(cmap='viridis', ax=axs, add_labels=False, cbar_kwargs=cbar_kwargs)
            axs.set_title('VIC 5 %s CPL Hist Files' %compset)
        
        plot_direc = os.path.join(os.getcwd(), 'RBR_runs', plot_type[0])
        os.makedirs(plot_direc, exist_ok=True)
        plt.suptitle('%s %s' % (l2x_var, vic5[l2x_var].long_name), size=15)
        plotname = '%s.png' %l2x_var
        savepath = os.path.join(plot_direc, plotname)
        plt.savefig(savepath, format='png', dpi=dpi, bbox_inches='tight')

