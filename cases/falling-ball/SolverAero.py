from __future__ import division

import numpy as np
import precice

# Drag calculation

rho = 1.225        # air density
cd = 0.4           # drag coefficient
r = 0.1            # radius of the ball

# preCICE

configuration_file_name = 'precice-config.xml'
participant_name = 'SolverAero'
read_data_name = 'velocity'
write_data_name = 'drag'
mesh_name = 'MeshAero'

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

dt = interface.initialize()

while interface.is_coupling_ongoing():

    # write checkpoint
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    read_data = interface.read_block_vector_data(read_data_id, vertex_ids)
    
    v = read_data[0,2]
    
    drag = 0.5 * rho * np.pi * r * r * cd * v * v

    write_data[0,2] = drag

    interface.write_block_vector_data(write_data_id, vertex_ids, write_data)

    print("calculated drag: %f" % drag)
    dt = interface.advance(dt)
    
    # read checkpoint
    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())


interface.finalize()
print("Closing python solver Aero...")
