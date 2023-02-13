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

fmu_file_name 		= '../../../FMUs/Oscillator.fmu'
output_file_name	= 'output/trajectory-Mass-Right.csv'
fmu_read_data_name	= 'force_in'
fmu_write_data_name	= 'force_out'
instance_name 		= 'instanceRight'

parameter = {

	'mass.m': 		m_2,
	'spring_fixed.c': 	k_2,
	'spring_middle.c':	k_12
}    

initial_conditions = {

	'mass.u':	u0_2, 
	'mass.v':	v0_2, 
	'mass.a':	a0_2

}

checkpoint = {

	'mass.u':	None, 
	'mass.v':	None, 
	'mass.a':	None
}

output = {

	'mass.u':	None, 
	'mass.v':	None 
}
