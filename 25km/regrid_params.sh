#!/bin/bash 

# regrid RASM parameters using NN-mapping from 50km to 25 km 

# deal with 4-D variables

# hyperslab the 4-D variables based on a dimension 
# for this example, root_zone
# NOTE: keep xc, yc in output file so that cdo setgrid will work
ncks -O -v root_depth,xc,yc -d root_zone,1 vic_params_wr50a_vic5.0.dev_joe_8312017.nc root_depth_joe.nc 

# eliminate degenerate dimension
ncwa -a root_zone root_depth_joe.nc root_depth_joe_rootzone1.nc

# first modify attributes from Joe

# filenames to be used
filename="vic_params_wr50a_vic5.0.dev_joe_8312017.nc"
tmp="vic_params_mod.nc"
domain_file_25km="domain.lnd.wr25b_ar9v4.170413.nc"
new_filename="vic_params_wr50a_vic5.0.dev_joe_9122017.nc"
final_filename="vic_params_wr25b_vic5.0.dev_20170912.nc"

cp $filename $tmp

ncatted -O -a username,global,m,c,"gergel" $tmp
ncatted -O -a host,global,m,c,"Dianas-iMac.local" $tmp
ncatted -O -a comment,global,c,c,"nearest neighbor remapping from /home/gergel/vic5_inputdata/vic_params_wr50a_vic5.0.dev_20160328.nc" $tmp
ncatted -O -a CDI,global,d,c,"" $tmp

# remap NetCDF to 25km domain file
cdo remapnn,$domain_file_25km $new_filename $final_filename

rm $tmp $new_filename 

