# This script pulls all code, inputs, and spec files to a list of specified AWS servers to ensure consistency

import os
import subprocess
import shutil
from shutil import copyfile
from cloud_setup_config import *


def git(*args):
	"""
	Call Git 
	"""
	return subprocess.check_call(['git'] + list(args))

# For a given machine
cloud_name = cloud_list[-1]
print cloud_name

# Delete existing files
root_dir = os.path.join(r"\\",cloud_name,"e$",'soundcast_root')
if os.path.exists(root_dir):
	shutil.rmtree(root_dir)
	
# Download a tagged version of Soundcast code to the cloud machine
# for year in model_years:
# 	# Pull code from Github
# 	cloud_dir = os.path.join(r"\\",cloud_name,"e$","soundcast_root","src")
# 	git("clone", "https://github.com/psrc/soundcast.git", "-b", 
# 		soundcast_branch, os.path.join(cloud_dir,str(year)))

# 	# Copy batch files
# 	copyfile(os.path.join(r'batch','run_soundcast_'+str(year)+'.bat'))

# Copy input_configuration to Soundcast runs

# Pull Urbansim code