# This script pulls all code, inputs, and spec files to a list of specified AWS servers to ensure consistency

import os, sys
import subprocess
import json
from shutil import copyfile
import configparser

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

def config_list(heading, var, config):
	"""
	Convert string to list from config settings
	"""
	raw = config[heading][var]
	raw = raw.split(',')
	return [i.strip() for i in raw]

def update_server(config):
# local working directory
	local_dir = os.getcwd()

	config = configparser.ConfigParser()
	config.read(config_name)

	cloud_list = config_list('global', 'cloud_list', config)
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
		if (config['global']['update_soundcast_repo'] or 
			config['global']['update_soundcast_config'] or 
			config['global']['copy_batch_files']):
			# Download a tagged version of Soundcast code to the cloud machine
			
			model_years = config_list('soundcast', 'model_years', config)
			for year in model_years:
				print year

				if config['global']['update_soundcast_repo']:
					
					# clone directory if it doesn't exist
					if not os.path.exists(os.path.join(src_dir,str(year))):
						os.chdir(src_dir)
						# clone repo if it doesn't exist
						git('clone','https://github.com/psrc/soundcast','-b',
							config['soundcast']['branch'],str(year))
					
					# checkout proper branch and tag
					print config['soundcast']['tag']

					if config['soundcast']['tag'] == None:
						'yes'
					checkout_tag(src_dir, str(year), config['soundcast']['branch'], config['soundcast']['tag'])

				if config['global']['update_soundcast_config']:
					# Copy configuration files to each Soundcast run year
					src = os.path.join(local_dir,'config','soundcast',config['soundcast']['config_source'], 
						str(year),'input_configuration.py')
					dst = os.path.join(src_dir,str(year),'input_configuration.py')
					copyfile(src, dst)

				if config['global']['copy_batch_files']:
					# Copy batch files for integrated run management
					src = os.path.join(local_dir,'batch','run_soundcast_'+str(year)+'.bat')
					dst = os.path.join(src_dir,'run_soundcast_'+str(year)+'.bat')
					copyfile(src, dst)

		# Add existing skim files to the root_dir if requested
		if config['global']['copy_archive_skims']:
			skim_years = config_list('skims', 'skim_years', config)
			for year in skim_years:
				src = os.path.join(config['skims']['skims_archive_dir'],str(year)+'-travelmodel.h5')
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

		# Export copy of config file to local server

def parse_config(config_name):

	config = configparser.ConfigParser()
	config.read(config_name)
	return config

def program(config_name):

	# config = parse_config(config_name)
	# config = configparser.ConfigParser()
	# # config.read(config_name)
	update_server(config_name)



if __name__ == "__main__":
    try:
        config_name = sys.argv[1]
    except IndexError:
        print "Usage: cloud_setup.py <config_file.ini>"
        sys.exit(1)

    # start the program
    program(config_name)