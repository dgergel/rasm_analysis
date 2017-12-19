#!/bin/env python

import netCDF4
import sys

#print("The arguments are: " , str(sys.argv))
args = sys.argv

print(args[1])

filename = str(args[1])
variable = str(args[2])

#print("filename is %s") %filename
#print("variable is %s") %variable

fh = netCDF4.Dataset(filename, 'r+')

# fix xv attributes
fh.variables['xv'].long_name = "longitude of grid cell verticies"
fh.variables['xv'].units = "degrees_east"

# fix yv attributes
fh.variables['yv'].long_name = "latitude of grid cell verticies"
fh.variables['yv'].units = "degrees_north"

# fix xc attributes
fh.variables['xc'].long_name = "longitude of grid cell center"
fh.variables['xc'].bounds = "xv"

# fix yc attributes
fh.variables['yc'].long_name = "latitude of grid cell center"
fh.variables['yc'].bounds = "yv"

# make sure that variable coordinates are labeled "xc yc"
# NOTE: this is crucial for remapping curvilinear grids
fh.variables[variable].coordinates = "xc yc" 

fh.close() 
