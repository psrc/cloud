# This script pulls all code, inputs, and spec files to a list of specified AWS servers to ensure consistency

import os, sys, shutil, stat
import subprocess
import json
import time
import datetime
import socket
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

def update_server(config_name):
	# Record time
	ts = time.time()

	# local working directory
	local_dir = os.getcwd()

	config = configparser.ConfigParser()
	config.read(config_name)

	# Before anything happens, make sure the directory structure exists at the server root as expected
	# E -> soundcast_root -> src; E -> opusgit -> urbansim; E -> opusgit -> urbansim_data; 
	root_dir = config['global']['root_dir']
	if not os.path.exists(root_dir):
		os.makedirs(root_dir)

	src_dir = root_dir = config['global']['src_dir']
	if not os.path.exists(src_dir):
		os.makedirs(src_dir)

	opusgit_dir = root_dir = config['global']['opusgit_dir']
	if not os.path.exists(opusgit_dir):
		os.makedirs(opusgit_dir)

	# Proceed through each year if we are updating repositories or copying batch files
	if (config['global']['update_soundcast_repo'] in['true','True','TRUE'] or 
		config['global']['update_soundcast_config'] in['true','True','TRUE'] or 
		config['global']['copy_batch_files'] in['true','True','TRUE']):
		# Download a tagged version of Soundcast code to the cloud machine
		
		model_years = config_list('soundcast', 'model_years', config)
		for year in model_years:
			print(year)

			if config['global']['update_soundcast_repo'] in['true','True','TRUE']:
				print('Updating Soundcast code from remote repository')

				# delete existing repo and clone directory 
				if os.path.exists(os.path.join(src_dir,str(year))):
					os.system('rmdir /S /Q "{}"'.format(os.path.join(src_dir,str(year))))
				os.chdir(src_dir)
				
				# clone repo if it doesn't exist
				git('clone','https://github.com/psrc/soundcast','-b',
					config['soundcast']['branch'],str(year))
				
				# checkout proper branch and tag
				checkout_tag(src_dir, str(year), config['soundcast']['branch'], config['soundcast']['tag'])

			if config['global']['update_soundcast_config'] in['true','True','TRUE']:
				print('Updating Soundcast configuration files')

				src = os.path.join(local_dir,'config','soundcast',config['soundcast']['config_source'], 
					str(year),'input_configuration.py')
				dst = os.path.join(src_dir,str(year),'input_configuration.py')
				copyfile(src, dst)

			if config['global']['copy_batch_files'] in['true','True','TRUE']:
				print('Copying Soundcast batch files for integrated run management')

				src = os.path.join(local_dir,'batch','run_soundcast_'+str(year)+'.bat')
				dst = os.path.join(src_dir,'run_soundcast_'+str(year)+'.bat')
				copyfile(src, dst)

	# Add existing skim files to the root_dir if requested
	if config['global']['copy_archive_skims'] in['true','True','TRUE']:
		skim_years = config_list('skims', 'skim_years', config)
		for year in skim_years:
			print('Copying archived skims for: ' + str(year))
			src = os.path.join(config['skims']['skims_archive_dir'],str(year)+'-travelmodel.h5')
			dst = os.path.join(root_dir,str(year)+'-travelmodel.h5')
			copyfile(src, dst)

	if config['global']['update_urbansim_repo'] in['true','True','TRUE']:
		print('Updating urbansim from remote repository')

		if not os.path.exists(os.path.join(opusgit_dir,'urbansim')):
			os.chdir(opusgit_dir)
			git('clone','https://github.com/psrc/urbansim','-b',config['urbansim']['branch'])

		checkout_tag(opusgit_dir, 'urbansim', config['urbansim']['branch'], config['urbansim']['tag'])

	if config['global']['update_urbansim_data_repo'] in ['true','True','TRUE']:
		print('Updating urbansim_data from remote repository')
		
		if not os.path.exists(os.path.join(opusgit_dir,'urbansim_data')):
			os.chdir(opusgit_dir)
			git('clone','https://github.com/psrc/urbansim_data','-b',config['urbansim_data']['branch'])

		# Update urbansim_data code, and/or check out tag
		checkout_tag(opusgit_dir, 'urbansim_data', config['urbansim_data']['branch'], config['urbansim_data']['tag'])

	# Export copy of config file to local server
	log_dir = config['global']['log_dir']
	if os.path.exists(log_dir):
		shutil.rmtree(log_dir)
	os.makedirs(log_dir)

	src = os.path.join(local_dir,config_name)
	dst = os.path.join(os.path.join(log_dir, os.path.split(config_name)[-1]))
	print(src)
	print(dst)
	copyfile(src, dst)

	# Write a log file with info about this process
	sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d | %H:%M:%S')
	logfile = os.path.join(log_dir, 'log.txt')
	with open(logfile, 'w') as f:
		f.write('Config input: ' + config_name + '\n')
		f.write('Script initiated: ' + sttime + '\n')
		f.write('Hostname: ' + socket.gethostname() + '\n')
		f.write('Hostname directory: ' + local_dir)

def parse_config(config_name):

	config = configparser.ConfigParser()
	config.read(config_name)
	return config

def program(config_name):

	update_server(config_name)



if __name__ == "__main__":
    try:
        config_name = sys.argv[1]
    except IndexError:
        print("Usage: cloud_setup.py <config\global\config_file.ini>")
        sys.exit(1)

    # start the program
    print(config_name)
    program(config_name)