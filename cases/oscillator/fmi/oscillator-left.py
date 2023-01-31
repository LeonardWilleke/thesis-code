from __future__ import division

import argparse
import numpy as np
from numpy.linalg import eig
import precice
from enum import Enum
import csv
import os
from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
import shutil





m_1, m_2 = 1, 1
k_1, k_2, k_12 = 4 * np.pi**2, 4 * np.pi**2, 16 * (np.pi**2)

# can change initial displacement
u0_1 = 1
u0_2 = 0

# cannot change initial velocities!
v0_1 = 0
v0_2 = 0




### Calculate analytical solution for comparison

M = np.array([[m_1, 0], [0, m_2]])
K = np.array([[k_1 + k_12, -k_12], [-k_12, k_2 + k_12]])

# system:
# m ddu + k u = f
# compute analytical solution from eigenvalue ansatz

eigenvalues, eigenvectors = eig(K)
omega = np.sqrt(eigenvalues)
A, B = eigenvectors
c = np.linalg.solve(eigenvectors, [u0_1, u0_2])

stiffness = k_1 + k_12
u0, v0, f0, d_dt_f0 = u0_1, v0_1, k_12 * u0_2, k_12 * v0_2
a0 = a0_1 = (f0 - stiffness * u0) / m_1
def u_analytical(t): return c[0] * A[0] * np.cos(omega[0] * t) + c[1] * A[1] * np.cos(omega[1] * t)
def v_analytical(t): return -c[0] * A[0] * omega[0] * np.sin(omega[0] * t) - \
    c[1] * A[1] * omega[1] * np.sin(omega[1] * t)


### FMU setup

fmu_file_name = '../../../FMUs/MassLeft.fmu'
    
model_description = read_model_description(fmu_file_name)  
vrs = {}
for variable in model_description.modelVariables:
    vrs[variable.name] = variable.valueReference 


parameter_names		= ['mass1.m', 'spring1.c']
parameter_values		= [m_1, k_1]
parameter_vr 			= [vrs.get(key) for key in parameter_names]

initial_conditions_names	= ['mass1.s', 'mass1.v', 'mass1.a']
initial_conditions_values	= [u0_1, v0_1, a0_1]
initial_conditions_vr		= [vrs.get(key) for key in initial_conditions_names]

can_get_and_set_fmu_state	= model_description.coSimulation.canGetAndSetFMUstate
checkpoint_names		= ['mass1.s', 'mass1.v', 'mass1.a']
checkpoint_vr			= [vrs.get(key) for key in checkpoint_names]

fmu_read_data_name		= 'force'
fmu_write_data_name		= 'displacement'

vr_read  	 = vrs[fmu_read_data_name]
vr_write 	 = vrs[fmu_write_data_name]

unzipdir = extract(fmu_file_name)
fmu = FMU2Slave(guid=model_description.guid, unzipDirectory=unzipdir, modelIdentifier=model_description.coSimulation.modelIdentifier, instanceName='instance1')

fmu.instantiate()
fmu.setupExperiment()
fmu.enterInitializationMode()
fmu.exitInitializationMode()


# Set parameters 
fmu.setReal(parameter_vr, parameter_values)

# Set initial Conditions
fmu.setReal(initial_conditions_vr, initial_conditions_values)


### preCICE setup

participant_name = 'Mass-Left'
write_data_name = 'Displacement'
read_data_name = 'Force'
mesh_name = 'Mass-Left-Mesh'

num_vertices = 1  # Number of vertices

solver_process_index = 0 
solver_process_size = 1

configuration_file_name = "./precice-config.xml"

interface = precice.Interface(participant_name, configuration_file_name, solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)
dimensions = interface.get_dimensions()

vertex = np.zeros(dimensions)
read_data = np.zeros(num_vertices)
write_data = k_12 * u0 * np.ones(num_vertices) # initial force?

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

# Set variables for logging
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

if can_get_and_set_fmu_state:
    state_cp = fmu.getFMUstate()
elif len(checkpoint_names) == 0:
    raise Exception('Please provide variables for the checkpoint. The FMU model doesnt allow to get and set the FMU state automatically.')
    # Adapt this error to only be thrown if an implicit coupling is used

while interface.is_coupling_ongoing():
    if interface.is_action_required(precice.action_write_iteration_checkpoint()):
        
        if can_get_and_set_fmu_state:
            state_cp 	= fmu.getFMUstate()
        else:
            checkpoint = fmu.getReal(checkpoint_vr)
        t_cp = t
        
        interface.mark_action_fulfilled(precice.action_write_iteration_checkpoint())

        # store data for plotting and postprocessing
        positions += u_write
        velocities += v_write
        times += t_write

    # compute time step size for this time step
    dt = np.min([precice_dt, my_dt])
    
    read_data = interface.read_scalar_data(read_data_id, vertex_id)
    data = read_data
    fmu.setReal([vr_read], [data])
    
    fmu.doStep(t, dt)

    result = fmu.getReal([vr_write])

    write_data = result[0]

    interface.write_scalar_data(write_data_id, vertex_id, write_data)

    t_new = t + dt
    precice_dt = interface.advance(dt)

    if interface.is_action_required(precice.action_read_iteration_checkpoint()):
        
        if can_get_and_set_fmu_state:
            fmu.setFMUstate(state_cp)
        else:
            fmu.setReal(checkpoint_vr, checkpoint)
        
        t = t_cp
        interface.mark_action_fulfilled(precice.action_read_iteration_checkpoint())

        # empty buffers for next window
        u_write = []
        v_write = []
        t_write = []

    else:
        # Used for logging
        u = fmu.getReal([vrs['mass1.s']])[0]
        v = fmu.getReal([vrs['mass1.v']])[0]
        a = fmu.getReal([vrs['mass1.a']])[0]
        t = t_new

        # write data to buffers
        u_write.append(u)
        v_write.append(v)
        t_write.append(t)

# store final result
u = fmu.getReal([vrs['mass1.s']])[0]
v = fmu.getReal([vrs['mass1.v']])[0]
a = fmu.getReal([vrs['mass1.a']])[0]
u_write.append(u)
v_write.append(v)
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
