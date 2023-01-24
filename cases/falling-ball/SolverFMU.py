""" This example demonstrates how to use couple a FMU with another solver via precice """

from fmpy import read_model_description, extract
from fmpy.fmi3 import FMU3Slave
from fmpy.util import plot_result, download_test_file
import numpy as np
import shutil
import precice 


### precice setup

configuration_file_name = 'precice-config.xml'
participant_name = 'SolverFMU'
read_data_name = 'drag'
write_data_name = 'velocity'
mesh_name = 'MeshFMU'

num_vertices = 1  # Number of vertices

solver_process_index = 0
solver_process_size = 1

interface = precice.Interface(participant_name, configuration_file_name,
                              solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)

assert (interface.is_mesh_connectivity_required(mesh_id) is False)

dimensions = interface.get_dimensions()

vertices = np.zeros((num_vertices, dimensions))
read_data = np.zeros((num_vertices, dimensions))
write_data = np.zeros((num_vertices, dimensions))

vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)


### FMU setup

# define the model name
fmu_filepath = '../../FMUs/fmus/FallingBall.fmu'

# read the model description
model_description = read_model_description(fmu_filepath)

# collect the value references
vrs = {}
for variable in model_description.modelVariables:
    vrs[variable.name] = variable.valueReference

vr_v         = vrs['v']
vr_der_v     = vrs['der(v)']
vr_a_tot     = vrs['a_tot']
vr_a_drag    = vrs['a_drag']


# extract the FMU
unzipdir = extract(fmu_filepath)

# instantiate fmu object
fmu = FMU3Slave(guid=model_description.guid,
                unzipDirectory=unzipdir,
                modelIdentifier=model_description.coSimulation.modelIdentifier,
                instanceName='instance1')    
                                                    
fmu.instantiate()
fmu.enterInitializationMode(startTime=0)
fmu.exitInitializationMode()       


dt = interface.initialize()

time = 0
    
# main time loop 
while interface.is_coupling_ongoing():
    
    # write checkpoint
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())
    
    read_data = interface.read_block_vector_data(read_data_id, vertex_ids)
    
    drag = read_data[0,2]
    
    fmu.setFloat64([vr_a_drag], [drag])
        
    fmu.doStep(currentCommunicationPoint=time, communicationStepSize=dt)
        
    v = fmu.getFloat64([vr_v])
    
    write_data[0,2] = v[0]

    interface.write_block_vector_data(write_data_id, vertex_ids, write_data)
        
    dt = interface.advance(dt)
    
    print("calculated velocity: %f" % v[0])
    
    # read checkpoint
    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())
    
    # advance time if timestep complete        
    if interface.is_time_window_complete():
        time += dt 
        
    
interface.finalize()
fmu.terminate()
fmu.freeInstance()              

# clean up
shutil.rmtree(unzipdir, ignore_errors=True)


