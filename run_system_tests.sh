# run system tests 

source activate vic_test_env

output_dir="/Users/diana/Dropbox/UW/Research/rasm/debug_albedo/system_test_output" 

output_dir_develop="/Users/diana/Dropbox/UW/Research/rasm/debug_albedo/system_test_output_develop"

data_dir="/Users/diana/Dropbox/UW/VIC_sample_data"

vic_albedo_exe="/Users/diana/Dropbox/UW/VIC/vic/drivers/image/vic_image.exe" 

vic_develop_exe="/Users/diana/Dropbox/UW/VIC/vic/drivers/image/vic_develop.exe"

nproc=4

# run vic for initialize albedo branch
#/Users/diana/Dropbox/UW/VIC/tests/run_tests.py system --image $vic_albedo_exe --output_dir $output_dir --data_dir $data_dir --nproc $nproc 

# run vic for develop branch and put output into a different directory

/Users/diana/Dropbox/UW/VIC/tests/run_tests.py system --image $vic_albedo_exe --output_dir $output_dir --data_dir $data_dir --nproc $nproc 
