from __future__ import division

import argparse
import numpy as np
import precice
import csv
import os
from fmpy import read_model_description, extract
from fmpy.simulation import Input, Recorder, instantiate_fmu, apply_start_values
from fmpy.util import write_csv
import shutil
import sys
import json

### Load settings from json files

parser = argparse.ArgumentParser()
parser.add_argument("fmi_setting_file", help="Path to the fmi setting file.", type=str)
parser.add_argument("precice_setting_file", help="Path to the precice setting file for the FMU coupling.", type=str)
args = parser.parse_args()

fmi_setting_file 		= args.fmi_setting_file
precice_setting_file 	= args.precice_setting_file

folder = os.path.dirname(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]), fmi_setting_file))
path = os.path.join(folder, os.path.basename(fmi_setting_file))
read_file = open(path, "r")
fmi_data = json.load(read_file)

folder = os.path.dirname(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]), precice_setting_file))
path = os.path.join(folder, os.path.basename(precice_setting_file))
read_file = open(path, "r")
precice_data = json.load(read_file)

### FMU setup

fmu_file_name 				= precice_data["simulation_params"]["fmu_file_name"]
fmu_instance 				= precice_data["simulation_params"]["fmu_instance_name"]
model_description 			= read_model_description(fmu_file_name)

vrs = {}
for variable in model_description.modelVariables:
    vrs[variable.name] = variable.valueReference 

output_names		 		= precice_data["simulation_params"]["output"]

signal_names				= fmi_data["input_signals"]["names"]
signal_data					= fmi_data["input_signals"]["data"]

fmu_read_data_name			= precice_data["simulation_params"]["fmu_read_data_name"]
fmu_write_data_name 		= precice_data["simulation_params"]["fmu_write_data_name"]
vr_read  	 				= [vrs[fmu_read_data_name]]
vr_write 	 				= [vrs[fmu_write_data_name]]

can_get_and_set_fmu_state	= model_description.coSimulation.canGetAndSetFMUstate 

is_fmi1 					= (model_description.fmiVersion == '1.0')
is_fmi2 					= (model_description.fmiVersion == '2.0')
is_fmi3 					= (model_description.fmiVersion == '3.0')

unzipdir = extract(fmu_file_name)

# Instantiate FMU

fmu = instantiate_fmu(unzipdir=unzipdir, model_description=model_description, fmi_type="CoSimulation")


if is_fmi1:
	# Set initial parameters
	apply_start_values(fmu, model_description, fmi_data["initial_conditions"])
	apply_start_values(fmu, model_description, fmi_data["model_params"])
	# Get initial write data
	fmu_write_data_init = fmu.getReal(vr_write)
elif is_fmi2:
	# Set initial parameters
	fmu.enterInitializationMode()
	apply_start_values(fmu, model_description, fmi_data["initial_conditions"])
	apply_start_values(fmu, model_description, fmi_data["model_params"])
	fmu.exitInitializationMode()
	# Get initial write data
	fmu_write_data_init = fmu.getReal(vr_write)
elif is_fmi3:
	# Set initial parameters
	fmu.enterInitializationMode()
	apply_start_values(fmu, model_description, fmi_data["initial_conditions"])
	apply_start_values(fmu, model_description, fmi_data["model_params"])
	fmu.exitInitializationMode()
	# Get initial write data
	fmu_write_data_init = fmu.getFloat64(vr_write)

# Create input signals

dtype = []
for i in range(len(signal_names)):
	tpl = tuple([signal_names[i], type(signal_data[0][i])]) # not sure if the type() might cause problems
	dtype.append(tpl)

signals = np.array([tuple(i) for i in signal_data],dtype=dtype) # this should work fine
input 	= Input(fmu, model_description, signals)

### preCICE setup

interface = precice.Interface(
	precice_data["coupling_params"]["participant_name"],
	precice_data["coupling_params"]["config_file_name"], 
	precice_data["coupling_params"]["solver_process_index"], 
	precice_data["coupling_params"]["solver_process_size"]
	)

mesh_id 		= interface.get_mesh_id(precice_data["coupling_params"]["mesh_name"])
dimensions 		= interface.get_dimensions()
num_vertices 	= precice_data["coupling_params"]["num_vertices"]

vertices 		= np.zeros((num_vertices, dimensions))
read_data 		= np.zeros((num_vertices, dimensions))
write_data 		= np.zeros((num_vertices, dimensions))

# initial value for write data
# Currently, the same value is used for all vector entries --> change later
write_data 	= fmu_write_data_init * np.ones((num_vertices, dimensions))

vertex_ids 		= interface.set_mesh_vertices(mesh_id, vertices)
read_data_id 	= interface.get_data_id(precice_data["coupling_params"]["read_data_name"], mesh_id)
write_data_id 	= interface.get_data_id(precice_data["coupling_params"]["write_data_name"], mesh_id)

precice_dt = interface.initialize()
my_dt = precice_dt  # use my_dt < precice_dt for subcycling

# write initial data
if interface.is_action_required(precice.action_write_initial_data()):
    interface.write_block_vector_data(write_data_id, vertex_ids, write_data)
    interface.mark_action_fulfilled(precice.action_write_initial_data())

interface.initialize_data()

recorder = Recorder(fmu=fmu, modelDescription=model_description, variableNames=output_names)

t = 0

recorder.sample(t, force=False)

while interface.is_coupling_ongoing():
    if interface.is_action_required(precice.action_write_iteration_checkpoint()):
        
        # Check if model has the appropiate functionalities
        if is_fmi1:
        	raise Exception("Implicit coupling not possible because FMU model with FMI1 can't reset state. "\
        					"Please update model to FMI2 or FMI3. "\
        					"Alternatively, choose an explicit coupling scheme.")
        if not can_get_and_set_fmu_state:
        	raise Exception("Implicit coupling not possible because FMU model can't reset state. "\
        					"Please implement getFMUstate() and setFMUstate() in FMU "\
        					"and set the according flag in ModelDescription.xml. "\
        					"Alternatively, choose an explicit coupling scheme.")
        
        # Save checkpoint
        state_cp 	= fmu.getFMUState()
        t_cp 		= t
        
        interface.mark_action_fulfilled(precice.action_write_iteration_checkpoint())
	
    # Compute current time step size
    dt = np.min([precice_dt, my_dt])
    
    # Read data from other participant
    read_data = interface.read_block_vector_data(read_data_id, vertex_ids)
    
    # TEMPORARY - Turn vector into scalar
    read_data_scalar = np.mean(read_data)
    
    # Set input signals to FMU
    input.apply(t)
    
    # Compute next time step
    if is_fmi1 or is_fmi2: 
    	fmu.setReal(vr_read, [read_data_scalar])
    	fmu.doStep(t, dt)
    	result = fmu.getReal(vr_write)
    if is_fmi3:
    	fmu.setFloat64(vr_read, [read_data_scalar])
    	fmu.doStep(t, dt)
    	result = fmu.getFloat64(vr_write)

    # TEMPORARY - Turn scalar into vector
    write_data_scalar = result[0]
    write_data = write_data_scalar * np.ones((num_vertices, dimensions))

    interface.write_block_vector_data(write_data_id, vertex_ids, write_data)

    t = t + dt
    
    precice_dt = interface.advance(dt)

    if interface.is_action_required(precice.action_read_iteration_checkpoint()):
        
        fmu.setFMUState(state_cp)
        t = t_cp
        
        interface.mark_action_fulfilled(precice.action_read_iteration_checkpoint())
        
    else:
        # Save output data for completed timestep
        recorder.sample(t, force=False)


interface.finalize()

# create output directory
output_dir = os.path.dirname(precice_data["simulation_params"]["output_file_name"])
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# store final result
recorder.sample(t, force=False)
results = recorder.result()
write_csv(precice_data["simulation_params"]["output_file_name"], results)

# terminate FMU
fmu.terminate()
fmu.freeInstance()              
shutil.rmtree(unzipdir, ignore_errors=True)

