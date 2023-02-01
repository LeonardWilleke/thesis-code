import numpy as np


m_1  = 1
k_1  = 4 * np.pi**2
k_12 = 16 * np.pi**2 # necessary for a0_1

# can change initial displacement
u0_1 = 1
u0_2 = 0 # necessary for a0_1

# cannot change initial velocity (allows for comparison with analytic solution)
v0_1 = 0

# Calculate initial acceleration
f0 = k_12 * u0_2
a0_1 = (f0 - (k_1 + k_12) * u0_1) / m_1
    
    
### FMU setup
    
fmu_file_name 		= '../../../FMUs/MassLeft.fmu'
fmu_read_data_name	= 'force'
fmu_write_data_name	= 'displacement'
    
parameter = {
    
	'mass1.m': 	m_1,
	'spring1.c': 	k_1
}    
    
initial_conditions = {
    
	'mass1.s':	u0_1, 
	'mass1.v':	v0_1, 
	'mass1.a':	a0_1
    
}
    
checkpoint = {
    
	'mass1.s':	None, 
	'mass1.v':	None, 
	'mass1.a':	None
    
}
