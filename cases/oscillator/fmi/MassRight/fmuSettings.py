import numpy as np

m_2  = 1
k_2  = 4 * np.pi**2
k_12 = 16 * np.pi**2

# can change initial displacement
u0_1 = 1
u0_2 = 0

# cannot change initial velocity (allows to compare with analytical solution)
v0_2 = 0

# Calculate initial acceleration
f0 = k_12 * u0_1
a0_2 = (f0 - (k_2 + k_12) * u0_2) / m_2


### FMU setup

fmu_file_name 		= '../../../FMUs/MassRight.fmu'
fmu_read_data_name	= 'displacement'
fmu_write_data_name	= 'force'

parameter = {

	'mass2.m': 	m_2,
	'spring2.c': 	k_2
}    

initial_conditions = {

	'mass2.s':	u0_2, 
	'mass2.v':	v0_2, 
	'mass2.a':	a0_2

}

checkpoint = {

	'mass2.s':	None, 
	'mass2.v':	None, 
	'mass2.a':	None

}

# MassRight: Add initial Force to IC and checkpoint? Test if the results make sense!
# 'spring12.f': k_12 * u0_2 or similar
