from __future__ import division

import argparse
import numpy as np
import precice

parser = argparse.ArgumentParser()
parser.add_argument("configurationFileName",
                    help="Name of the xml config file.", type=str)

try:
    args = parser.parse_args()
except SystemExit:
    print("")
    print("Usage: python3 ./solverdummy.py precice-config")
    quit()

configuration_file_name = args.configurationFileName

participant_name = "Controller"
write_data_name = "Velocity"
read_data_name = "Force"
mesh_name = "Mesh-Controller"

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

for x in range(num_vertices):
    for y in range(0, dimensions):
        vertices[x, y] = x
        #read_data[x, y] = x
        write_data[x, y] = x


vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)

dt = interface.initialize()

while interface.is_coupling_ongoing():
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    read_data = interface.read_block_vector_data(read_data_id, vertex_ids)
    print(read_data)

    write_data[0,0] = 0
    write_data[0,1] = 100 * read_data[0,0]

    interface.write_block_vector_data(write_data_id, vertex_ids, write_data)

    print("DUMMY: Advancing in time")
    dt = interface.advance(dt)

    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())

interface.finalize()
print("DUMMY: Closing python solver dummy...")
