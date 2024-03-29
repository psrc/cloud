import os

##############################
# Input paths and model years
##############################
model_year = '2018'
base_year = '2018'
landuse_inputs = 'v3_RTP'
network_inputs = 'rtp_2018_final'
soundcast_inputs_dir = 'R:/e2projects_two/SoundCast/Inputs/dev'

##############################
# Initial Setup
##############################
run_accessibility_calcs = True
run_setup_emme_project_folders = True
run_setup_emme_bank_folders = True
run_copy_scenario_inputs = True
run_import_networks = True

##############################
# Model Procedures
##############################
run_skims_and_paths_free_flow = True
run_skims_and_paths = True
run_truck_model = True
run_supplemental_trips = True
run_daysim = True
run_summaries = True

##############################
# Modes and Path Types
##############################
include_av = False
include_tnc = True
tnc_av = False    # TNCs (if available) are AVs
include_tnc_to_transit = False # AV to transit path type allowed
include_knr_to_transit = False # Kiss and Ride to Transit
include_delivery = False

##############################
# Pricing
##############################
add_distance_pricing = False
distance_rate_dict = {'md': 8.5, 'ev': 8.5, 'am': 13.5, 'ni': 8.5, 'pm': 13.5}

##############################
# Other Controls
##############################
run_integrated = True
should_build_shadow_price = False
delete_banks = False