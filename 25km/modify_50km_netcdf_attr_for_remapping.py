#!/bin/env python

import netCDF4
import socket

filename = "vic_params_joe_copy.nc"

fh = netCDF4.Dataset(filename, 'r+')

# fix xv attributes
fh.variables['xv'].long_name = "longitude of grid cell verticies"
fh.variables['xv'].units = "degrees_east"

# fix yv attributes
fh.variables['yv'].long_name = "latitude of grid cell verticies"
fh.variables['yv'].units = "degrees_north"

# fix xc attributes
fh.variables['xc'].long_name = "longitude of grid cell center"
fh.variables['xc'].units = "degrees_east"
fh.variables['xc'].bounds = "xv"

# fix yc attributes
fh.variables['yc'].long_name = "latitude of grid cell center"
fh.variables['yc'].units = "degrees_north"
fh.variables['yc'].bounds = "yv"

# modify global attributes
fh.username="gergel"
fh.host = socket.gethostname()

fh.close() 
