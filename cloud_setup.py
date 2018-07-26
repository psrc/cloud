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

# For each machine, pull tagged version of Soundcast code
for cloud_name in cloud_list:
	print cloud_name
	
	if update_soundcast:
		# Download a tagged version of Soundcast code to the cloud machine
		# for year in model_years:
		for year in model_years:
			print year
			# Pull code from Github
			cloud_dir = os.path.join(r'\\',cloud_name,'e$','soundcast_root','src')

			# create directory if it doesn't exist
			if not os.path.exists(os.path.join(cloud_dir,str(year))):
				os.chdir(cloud_dir)
				# clone repo if it doesn't exist
				git('clone','https://github.com/psrc/soundcast','-b',
					soundcast_branch,str(year))
			
			os.chdir(os.path.join(cloud_dir,str(year)))
			git('stash')    # assuming overwrite of existing runs/code
			git('checkout', soundcast_branch)
			git('checkout', 'tags/'+soundcast_tag)

	if update_urbansim:
		cloud_dir = os.path.join(r'\\',cloud_name,'e$','opusgit')

		# Pull urbansim data
		if not os.path.exists(os.path.join(cloud_dir,'urbansim')):
			git('clone','https://github.com/psrc/urbansim','-b',urbansim_branch)

		# os.chdir(os.path.join(cloud_dir,'urbansim'))
		checkout_tag(cloud_dir, 'urbansim', urbansim_branch, urbansim_tag)

		# Pull urbansim_data data
		if not os.path.exists(os.path.join(cloud_dir,'urbansim_data')):
			git('clone','https://github.com/psrc/urbansim_data','-b',urbansim_data_branch)

		# Update urbansim_data code, and/or check out tag
		checkout_tag(cloud_dir, 'urbansim_data', urbansim_data_branch, urbansim_data_tag)

	# Copy configuration files to Soundcast runs

# Move batch files to machines

# Add existing skim files if requested