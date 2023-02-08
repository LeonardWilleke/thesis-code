from __future__ import division

import argparse
import numpy as np
from numpy.linalg import eig
import precice
from enum import Enum
import csv
import os
from fmpy import read_model_description, extract
from fmpy.fmi3 import FMU3Slave
import shutil



class Participant(Enum):
    MASS_LEFT = "Mass-Left"
    MASS_RIGHT = "Mass-Right"


parser = argparse.ArgumentParser()
parser.add_argument("participantName", help="Name of the solver.", type=str, choices=[p.value for p in Participant])
args = parser.parse_args()

participant_name = args.participantName

m_1, m_2 = 1, 1
k_1, k_2, k_12 = 4 * np.pi**2, 4 * np.pi**2, 16 * (np.pi**2)

M = np.array([[m_1, 0], [0, m_2]])
K = np.array([[k_1 + k_12, -k_12], [-k_12, k_2 + k_12]])

# system:
# m ddu + k u = f
# compute analytical solution from eigenvalue ansatz

eigenvalues, eigenvectors = eig(K)
omega = np.sqrt(eigenvalues)
A, B = eigenvectors

# can change initial displacement
u0_1 = 1
u0_2 = 0

# cannot change initial velocities!
v0_1 = 0
v0_2 = 0

c = np.linalg.solve(eigenvectors, [u0_1, u0_2])


if participant_name == Participant.MASS_LEFT.value:
    write_data_name = 'Displacement-Left'
    read_data_name = 'Displacement-Right'
    mesh_name = 'Mass-Left-Mesh'
    fmu_file_name = '../../../FMUs/Oscillator.fmu'
    
    model_description = read_model_description(fmu_file_name)  
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference 
    vr_m 	 = vrs['mass.m']
    vr_k 	 = vrs['spring_fixed.c']
    vr_k_12 	 = vrs['spring_middle.c']
    vr_u	 = vrs['mass.u']
    vr_v 	 = vrs['mass.v']
    vr_a 	 = vrs['mass.a']
    vr_read 	 = vrs['displacement']
    vr_write 	 = vrs['mass.u']
    
    k = k_1
    mass = m_1
    disp0 = u0_2
    
    # Calculate analytical solution for comparison
    stiffness = k_1 + k_12
    u0, v0, f0, d_dt_f0 = u0_1, v0_1, k_12 * u0_2, k_12 * v0_2
    def u_analytical(t): return c[0] * A[0] * np.cos(omega[0] * t) + c[1] * A[1] * np.cos(omega[1] * t)
    def v_analytical(t): return -c[0] * A[0] * omega[0] * np.sin(omega[0] * t) - \
        c[1] * A[1] * omega[1] * np.sin(omega[1] * t)

elif participant_name == Participant.MASS_RIGHT.value:
    read_data_name = 'Displacement-Left'
    write_data_name = 'Displacement-Right'
    mesh_name = 'Mass-Right-Mesh'
    fmu_file_name = '../../../FMUs/Oscillator.fmu'
    
    model_description = read_model_description(fmu_file_name)
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference 
    vr_m 	 = vrs['mass.m']
    vr_k 	 = vrs['spring_fixed.c']
    vr_k_12 	 = vrs['spring_middle.c']
    vr_u	 = vrs['mass.u']
    vr_v 	 = vrs['mass.v']
    vr_a 	 = vrs['mass.a']
    vr_read 	 = vrs['displacement']
    vr_write 	 = vrs['mass.u']
    
    k = k_2
    mass = m_2
    disp0 = u0_1
    
    # Calculate analytical solution for comparison
    stiffness = k_2 + k_12
    u0, v0, f0, d_dt_f0 = u0_2, v0_2, k_12 * u0_1, k_12 * v0_1
    def u_analytical(t): return c[0] * B[0] * np.cos(omega[0] * t) + c[1] * B[1] * np.cos(omega[1] * t)
    def v_analytical(t): return -c[0] * B[0] * omega[0] * np.sin(omega[0] * t) - \
        c[1] * B[1] * omega[1] * np.sin(omega[1] * t)

else:
    raise Exception(f"wrong participant name: {participant_name}")

### preCICE setup

num_vertices = 1  # Number of vertices

solver_process_index = 0 
solver_process_size = 1

configuration_file_name = "../precice-config.xml"

interface = precice.Interface(participant_name, configuration_file_name, solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)
dimensions = interface.get_dimensions()

vertex = np.zeros(dimensions)
read_data = np.zeros(num_vertices)
write_data = u0 * np.ones(num_vertices)

vertex_id = interface.set_mesh_vertex(mesh_id, vertex)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)

precice_dt = interface.initialize()
my_dt = precice_dt  # use my_dt < precice_dt for subcycling

# write initial data
if interface.is_action_required(precice.action_write_initial_data()):
    interface.write_scalar_data(write_data_id, vertex_id, write_data)
    interface.mark_action_fulfilled(precice.action_write_initial_data())

interface.initialize_data()

### FMU setup

unzipdir = extract(fmu_file_name)
fmu = FMU3Slave(guid=model_description.guid, unzipDirectory=unzipdir, modelIdentifier=model_description.coSimulation.modelIdentifier, instanceName='instance1')

fmu.instantiate()

# Set parameters and IC
fmu.enterInitializationMode()

fmu.setFloat64([vr_m], [mass])
fmu.setFloat64([vr_k], [k])
fmu.setFloat64([vr_k_12], [k_12])

a0 = (f0 - stiffness * u0) / mass
fmu.setFloat64([vr_u], [u0])
fmu.setFloat64([vr_v], [v0])
fmu.setFloat64([vr_a], [a0])

fmu.exitInitializationMode()

u = u0
v = v0
a = a0
t = 0


positions = []
velocities = []
times = []

u_write = [u]
v_write = [v]
t_write = [t]

n_iterations = 0


while interface.is_coupling_ongoing():
    if interface.is_action_required(precice.action_write_iteration_checkpoint()):
        #data_cp 	= fmu.getReal([vr_read])
        #u_cp 		= fmu.getReal([vr_u])
        #v_cp 		= fmu.getReal([vr_v])
        #a_cp 		= fmu.getReal([vr_a])
        state_cp 	= fmu.getFMUState()
        t_cp 		= t
        interface.mark_action_fulfilled(precice.action_write_iteration_checkpoint())

        # store data for plotting and postprocessing
        positions += u_write
        velocities += v_write
        times += t_write

    # compute time step size for this time step
    dt = np.min([precice_dt, my_dt])
    
    print("Data before reading")
    print("u: ", fmu.getFloat64([vr_u]))
    print("v: ", fmu.getFloat64([vr_v]))
    print("a: ", fmu.getFloat64([vr_a]))
    print("read: ", fmu.getFloat64([vr_read]))
    print("write: ", fmu.getFloat64([vr_write]))
    
    read_data = interface.read_scalar_data(read_data_id, vertex_id)
    data = read_data
    
    fmu.setFloat64([vr_read], [data])
    
    print("Data after reading")
    print("u: ", fmu.getFloat64([vr_u]))
    print("v: ", fmu.getFloat64([vr_v]))
    print("a: ", fmu.getFloat64([vr_a]))
    print("read: ", fmu.getFloat64([vr_read]))
    print("write: ", fmu.getFloat64([vr_write]))
    
    fmu.doStep(t, dt)
    
    print("Data after step")
    print("u: ", fmu.getFloat64([vr_u]))
    print("v: ", fmu.getFloat64([vr_v]))
    print("a: ", fmu.getFloat64([vr_a]))
    print("read: ", fmu.getFloat64([vr_read]))
    print("write: ", fmu.getFloat64([vr_write]))
    
    result = fmu.getFloat64([vr_write])
    u_new = fmu.getFloat64([vr_u])
    v_new = fmu.getFloat64([vr_v])
    a_new = fmu.getFloat64([vr_a])
    t_new = t + dt

    write_data = result[0]

    interface.write_scalar_data(write_data_id, vertex_id, write_data)

    precice_dt = interface.advance(dt)

    if interface.is_action_required(precice.action_read_iteration_checkpoint()):
        #fmu.setReal([vr_read], data_cp)
        #fmu.setReal([vr_u], u_cp)
        #fmu.setReal([vr_v], v_cp)
        #fmu.setReal([vr_a], a_cp)
        fmu.setFMUState(state_cp)
        t = t_cp
        interface.mark_action_fulfilled(precice.action_read_iteration_checkpoint())

        # empty buffers for next window
        u_write = []
        v_write = []
        t_write = []
        
        n_iterations += 1
        #if n_iterations == 5:
        #    raise Exception("Stop for testing")

    else:
        u = u_new
        v = v_new
        a = a_new
        t = t_new

        # write data to buffers
        u_write.append(u[0])
        v_write.append(v[0])
        t_write.append(t)

# store final result
u = u_new
v = v_new
a = a_new
u_write.append(u[0])
v_write.append(v[0])
t_write.append(t)
positions += u_write
velocities += v_write
times += t_write

interface.finalize()
fmu.terminate()
fmu.freeInstance()              
# clean up FMU
shutil.rmtree(unzipdir, ignore_errors=True)

# print errors
error = np.max(abs(u_analytical(np.array(times)) - np.array(positions)))
print("Error w.r.t analytical solution:")
print(f"{my_dt},{error}")

# output trajectory
if not os.path.exists("output"):
    os.makedirs("output")

with open(f'output/trajectory-{participant_name}.csv', 'w') as file:
    csv_write = csv.writer(file, delimiter=';')
    csv_write.writerow(['time', 'position', 'velocity'])
    for t, u, v in zip(times, positions, velocities):
        csv_write.writerow([t, u, v])
