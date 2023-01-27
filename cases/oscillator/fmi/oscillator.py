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
    write_data_name = 'Force-Left'
    read_data_name = 'Force-Right'
    mesh_name = 'Mass-Left-Mesh'
    fmu_file_name = '../../../FMUs/MassLeft.fmu'
    
    model_description = read_model_description(fmu_file_name)  
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference 
    #vr_m = 
    #vr_k =
    #vr_k_12 = 
    vr_u = vrs['mass1.s']
    vr_v = vrs['mass1.v']
    vr_a = vrs['mass1.a']
    vr_f_set = vrs['u']
    #vr_f_set = vrs['spring12.flange_b.s']
    vr_f_get = vrs['mass1.flange_b.f']
    
    k = k_1
    
    # Better idea: Include spring12 only in one FMU and cut the model at the interface of mass and spring. This suits my setup with FMU components much better.
    # The current force exchange is written for the calculation with the python script. 

    # Calculate analytical solution for comparison
    mass = m_1
    stiffness = k_1 + k_12
    u0, v0, f0, d_dt_f0 = u0_1, v0_1, k_12 * u0_2, k_12 * v0_2
    def u_analytical(t): return c[0] * A[0] * np.cos(omega[0] * t) + c[1] * A[1] * np.cos(omega[1] * t)
    def v_analytical(t): return -c[0] * A[0] * omega[0] * np.sin(omega[0] * t) - \
        c[1] * A[1] * omega[1] * np.sin(omega[1] * t)

elif participant_name == Participant.MASS_RIGHT.value:
    read_data_name = 'Force-Left'
    write_data_name = 'Force-Right'
    mesh_name = 'Mass-Right-Mesh'
    fmu_file_name = '../../../FMUs/MassRight.fmu'
    
    model_description = read_model_description(fmu_file_name)
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable.valueReference 
    #vr_m = 
    #vr_k =
    #vr_k12 = 
    vr_u = vrs['mass2.s']
    vr_v = vrs['mass2.v']
    vr_a = vrs['mass2.a']
    vr_f_set = vrs['u']
    #vr_f_set = vrs['spring12.flange_a.s']
    vr_f_get = vrs['mass2.flange_a.f']
    
    k = k_2
    
    # Calculate analytical solution for comparison
    mass = m_2
    stiffness = k_2 + k_12
    u0, v0, f0, d_dt_f0 = u0_2, v0_2, k_12 * u0_1, k_12 * v0_1
    def u_analytical(t): return c[0] * B[0] * np.cos(omega[0] * t) + c[1] * B[1] * np.cos(omega[1] * t)
    def v_analytical(t): return -c[0] * B[0] * omega[0] * np.sin(omega[0] * t) - \
        c[1] * B[1] * omega[1] * np.sin(omega[1] * t)

else:
    raise Exception(f"wrong participant name: {participant_name}")

# preCICE setup

num_vertices = 1  # Number of vertices

# What do they do? Check in manual
solver_process_index = 0 
solver_process_size = 1

configuration_file_name = "../precice-config.xml"

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

# FMU setup
unzipdir = extract(fmu_file_name)
fmu = FMU2Slave(guid=model_description.guid, unzipDirectory=unzipdir, modelIdentifier=model_description.coSimulation.modelIdentifier, instanceName='instance1')

fmu.instantiate()
fmu.setupExperiment()
fmu.enterInitializationMode()
fmu.exitInitializationMode()

# Set parameters m, k, k12 - not now
#fmu.setReal([vr_m], [mass])
#fmu.setReal([vr_k], [k])
#fmu.setReal([vr_k_12], [k_12])

# Initial Conditions
a0 = (f0 - stiffness * u0) / mass

fmu.setReal([vr_u], [u0])
fmu.setReal([vr_v], [v0])
fmu.setReal([vr_a], [a0])

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

while interface.is_coupling_ongoing():
    if interface.is_action_required(precice.action_write_iteration_checkpoint()):
        f_cp = fmu.getReal([vr_f_get])
        u_cp = fmu.getReal([vr_u])
        v_cp = fmu.getReal([vr_v])
        a_cp = fmu.getReal([vr_a])
        t_cp = t
        interface.mark_action_fulfilled(precice.action_write_iteration_checkpoint())

        # store data for plotting and postprocessing
        positions += u_write
        velocities += v_write
        times += t_write

    # compute time step size for this time step
    dt = np.min([precice_dt, my_dt])
    
    read_data = interface.read_scalar_data(read_data_id, vertex_id)
    f = read_data
    print("Read data from other solver: ", read_data)
    fmu.setReal([vr_f_set], [f])
    print("Data in FMU: ", fmu.getReal([vr_f_set])[0])
    
    fmu.doStep(t, dt)
    
    f_new = fmu.getReal([vr_f_get])
    u_new = fmu.getReal([vr_u])
    v_new = fmu.getReal([vr_v])
    a_new = fmu.getReal([vr_a])
    t_new = t + dt
    
    print("New force calculated: ", f_new[0])

    # !!! Does this mean I have to take spring12 out of the models? --> read about and try different options with force exchange
    #write_data = k_12 * u_new[0]
    #write_data = u_new[0]
    write_data = f_new[0]
    #print(write_data)

    interface.write_scalar_data(write_data_id, vertex_id, write_data)

    precice_dt = interface.advance(dt)

    if interface.is_action_required(precice.action_read_iteration_checkpoint()):
        f = f_cp
        u = u_cp
        v = v_cp
        a = a_cp
        t = t_cp
        interface.mark_action_fulfilled(precice.action_read_iteration_checkpoint())

        # empty buffers for next window
        u_write = []
        v_write = []
        t_write = []

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