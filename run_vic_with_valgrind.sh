###################################################################
### RUN VIC WITH VALGRIND ###
###################################################################

# activate virtual environment
source activate vic_test_env

vic_exe="/Users/diana/Dropbox/UW/VIC/vic/drivers/image/vic_image.exe"

global_param="/Users/diana/Dropbox/UW/Research/rasm/debug_albedo/global_param.image.STEHE.txt"

# log_file="/Users/diana/Dropbox/UW/Research/rasm/debug_albedo/vicforce_log_global_read_state_file_initializealbedobranch.txt"

log_file="/Users/diana/Dropbox/UW/Research/rasm/debug_albedo/vic_log.txt"

# run vic normally 
$vic_exe -g $global_param

# run VIC 5 image driver with Valgrind 

# example from Yixin: 
# valgrind -v --leak-check=full /path_to_vic_executable/vic_classic.exe -g global >& log.global.txt

# my version
# valgrind -v --leak-check=full $vic_exe -g $global_param >& $log_file
