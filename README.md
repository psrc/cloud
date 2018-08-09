# cloud

Configure model servers with a common set of version-controlled code and settings. 

# Usage

Specify settings in `*.ini` file in config/global.
Each `*.in` file represents a single global configuration for cloud machines.
These control which machines are updated, which components are refreshed,
and the source of inputs for Soudndcast config files and skims. 

To call the script:
`python cloud_setup.py <config_file_name.ini>`

For example, to set up servers for running Vision 2050 inputs:
`python cloud_setup.py config\global\vision2050.ini`

Within the `config\global\vision2050.ini` file are settings that
represent input sources and code configuration for Vision 2050. 

This script can perform the following tasks (which are controled through the `*.ini` files:
- create directory structure for integrated modeling,
- clone or pull the latest soundcast repository, using a defined branch and tag
- clone or pull the latest urbansim and urbansim_data, repositories, with defined branches and tags for each repo
- copy soundcast input configuration files from this repository (see `config\soundcast`) for examples
    - these are copied into the soundcast repositories clones\pulled from github
- copy batch files required for integrated runs
- copy skim files inputs for integrated runs, to reduce full soundcast run requirements for all years (e.g., 2014)
- save local log information that contains the global config file and information on build specs

Together, these processes build a consistent modeling machine that works for independent and integrated Soundcast and Urbansim runs.

----

For more information, visit:
# [Managing and Creating Servers Wiki](https://github.com/psrc/cloud/wiki/cloud)
