#!/bin/bash 

direc="/raid2/jhamman/projects/VIC5/release_data/RASM/results"

for year in $(seq 1959 1978)
do 

	new_filename="/raid/gergel/rasm/gcc_prep/${year}.nc"

	echo "concatenating $year"
	ncrcat -O $direc/*h0.${year}*.nc $new_filename
done 
