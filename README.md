# cloud

Configure a set of servers with a common set of code and settings. 

Specify settings in *.ini file in config/global.
Each *.in file represents a single global configuration for cloud machines.
These control which machines are updated, which components are refreshed,
and the source of inputs for Soudndcast config files and skims. 

To call the script:
`python cloud_setup.py <config_file_name.ini>`

For example, to set up servers for running Vision 2050 inputs:
`python cloud_setup.py vision2050.ini`

Within the `config\global\vision2050.ini` file are settings that
represent input sources and code configuration for Vision 2050. 