# This script pulls all code, inputs, and spec files to a list of specified AWS servers to ensure consistency

import os
import subprocess
import shutil
from shutil import copyfile
from cloud_setup_config import *

def git(*args):
	'''
	Call Git 
	'''
	return subprocess.check_call(['git'] + list(args))

def checkout_tag(main_dir, repo_name, branch, tag=None):
	"""
	Stash existing repository data and check out specific branch and/or tag
	"""
	os.chdir(os.path.join(main_dir,repo_name))
	git('stash')
	git('checkout', branch)
	if tag:
		git('checkout', 'tags/'+tag)

# Thought:
# Load a global config file - pass in command line, like python cloud_setup.py -config config\global\vision_2050.py
# This global file will have all the info from input_configuration.py, and we will know the source of each machine's creation
# Write a copy of this file to each machine too?

# For each machine, pull tagged version of Soundcast code
for cloud_name in cloud_list:
	print cloud_name

	# Before anything happens, make sure the directory structure exists at the cloud root as expected
	# E -> soundcast_root -> src 
	root_dir = os.path.join(r'\\',cloud_name,'e$','soundcast_root')
	if not os.path.exists(root_dir):
		os.makedirs(root_dir)

	src_dir = os.path.join(r'\\',cloud_name,'e$','soundcast_root','src')
	if not os.path.exists(src_dir):
		os.makedirs(src_dir)
	
	# Proceed through each year if we are updating repositories or copying batch files
	if update_soundcast_repo or update_soundcast_config or copy_batch_files:
		# Download a tagged version of Soundcast code to the cloud machine
		
		for year in model_years:
			print year

			if update_soundcast_repo:
				
				# clone directory if it doesn't exist
				if not os.path.exists(os.path.join(src_dir,str(year))):
					os.chdir(src_dir)
					# clone repo if it doesn't exist
					git('clone','https://github.com/psrc/soundcast','-b',
						soundcast_branch,str(year))
				
				# checkout proper branch and tag
				os.chdir(os.path.join(src_dir,str(year)))
				git('stash')    # assuming overwrite of existing runs/code
				git('checkout', soundcast_branch)
				git('checkout', 'tags/'+soundcast_tag)

			if update_soundcast_config:
				# Copy configuration files to each Soundcast run year
				src = os.path.join(os.getcwd(),'config','soundcast',soundcast_config_source, str(year),'input_configuration.py')
				dst = os.path.join(src_dir,str(year),'input_configuration.py')
				copyfile(src, dst)

			if copy_batch_files:
				# Copy batch files for integrated run management
				src = os.path.join(os.getcwd(),'batch','run_soundcast_'+str(year)+'.bat')
				dst = os.path.join(src_dir,'run_soundcast_'+str(year)+'.bat')
				copyfile(src, dst)

	# Add existing skim files to the root_dir if requested
	if copy_archive_skims:
		for year in skim_years:
			src = os.path.join(skims_archive_dir,str(year)+'-travelmodel.h5')
			dst = os.path.join(root_dir,str(year)+'-travelmodel.h5')
			copyfile(src, dst)

	if update_urbansim_repo:

		# Pull urbansim data
		if not os.path.exists(os.path.join(src_dir,'urbansim')):
			git('clone','https://github.com/psrc/urbansim','-b',urbansim_branch)

		# os.chdir(os.path.join(src_dir,'urbansim'))
		checkout_tag(src_dir, 'urbansim', urbansim_branch, urbansim_tag)

	if update_urbansim_data_repo:
		# Pull urbansim_data data
		if not os.path.exists(os.path.join(src_dir,'urbansim_data')):
			git('clone','https://github.com/psrc/urbansim_data','-b',urbansim_data_branch)

		# Update urbansim_data code, and/or check out tag
		checkout_tag(src_dir, 'urbansim_data', urbansim_data_branch, urbansim_data_tag)




