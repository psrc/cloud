# List of machines to target
# cloud_list = ['aws-model03','aws-model04','aws-model05']
cloud_list = ['aws-model01']

# Soundcast config files
soundcast_config_source = 'vision_2050'

# List of Soundcast years to model
model_years = [2014,2025,2040,2050]

# Controls 
update_soundcast_repo = True
update_soundcast_config = True
update_urbansim_repo = True
update_urbansim_data_repo = True
copy_batch_files = True
copy_archive_skims = True

# Git
soundcast_branch = 'dev'
soundcast_tag = None  

urbansim_branch = 'dev'
urbansim_tag = None

urbansim_data_branch = 'dev'
urbansim_data_tag = None

# Skims
skims_archive_dir = r'L:\integrated\JF\skims\base'
skim_years = [2014,2025]