#!/bin/bash 

###########################################################################################################
#################################### HYPERSLAB 4-D VIC 5 PARAMETERS #######################################
###########################################################################################################

variable=$1

# 4-D variables that need to be hyperslabbed: `root_depth`, `root_fract`, `LAI`, `albedo`, `veg_rough` and `displacement`
# [veg_class, month, nj, ni] ones: displacement, albedo, LAI, veg_rough
# [veg_class, root_zone, nj, ni] ones: root_depth, root_fract

# define filenames
#hyperslabbed to degenerate dimension
tmp1="$variable.${i}.nc" 
#remove degenerate dimension
tmp2="$variable.${i}.50km.nc" 
# remapped to 25km
final="$variable.${i}.25km.nc" 
domain_file="domain.lnd.wr25b_ar9v4.170413.nc"
input_file="vic_params_wr50a_vic5.0.dev_joe_8312017.nc"

if [ $variable = "albedo" ] || [ $variable = "LAI" ] || [ $variable = "displacement" ] || [ $variable = "veg_rough" ]
then
    for i in `seq 0 11`
    do
        dim="month"
        #hyperslabbed to degenerate dimension
        tmp1="$variable.${i}.nc"
        #remove degenerate dimension
        tmp2="$variable.${i}.50km.nc"
        # remapped to 25km
        final="$variable.${i}.25km.nc"

        echo "processing $variable for $dim $i"
        # hyperslab specified dim
        ncks -O -v $variable,xc,yc,xv,yv -d $dim,$i $input_file $tmp1
        # remove degenerate dimension
        ncwa -a $dim $tmp1 $tmp2
        # modify attributes to make sure they're correct
        # NOTE: w/out this step, remapping is incorrect
        echo "tmp2 is $tmp2"
        echo "variable is $variable"
        python ./modify_netcdf_attributes_for_remapping.py $tmp2 $variable 
        # remap (in this case to 25 km) 
        cdo remapnn,$domain_file $tmp2 $final
        rm $tmp1 $tmp2
    done
elif [ $variable = "root_depth" ] || [ $variable = "root_fract" ]
then
    for i in `seq 0 2`
    do
        dim="root_zone"

        #hyperslabbed to degenerate dimension
        tmp1="$variable.${i}.nc"
        #remove degenerate dimension
        tmp2="$variable.${i}.50km.nc"
        # remapped to 25km
        final="$variable.${i}.25km.nc"

        echo "processing $variable for $dim $i"
        # hyperslab specified dim
        ncks -O -v $variable,xc,yc,xv,yv -d $dim,$i $input_file $tmp1
        # remove degenerate dimension
        ncwa -a $dim $tmp1 $tmp2
        # modify attributes to make sure they're correct
        # NOTE: w/out this step, remapping is incorrect
        echo "tmp2 is $tmp2"
        echo "variable is $variable"
        python ./modify_netcdf_attributes_for_remapping.py $tmp2 $variable
        # remap (in this case to 25 km) 
        cdo remapnn,$domain_file $tmp2 $final
        rm $tmp1 $tmp2
    done
else
    echo "this variable hasn't been defined in this hyperslabbing script"
fi 
