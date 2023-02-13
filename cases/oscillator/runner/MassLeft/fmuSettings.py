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
    
fmu_file_name 		= '../../../FMUs/Oscillator.fmu'
output_file_name	= 'output/trajectory-Mass-Left.csv'
fmu_read_data_name	= 'force_in'
fmu_write_data_name	= 'force_out'
instance_name 		= 'instanceLeft'
    
parameter = {
    
	'mass.m': 		m_1,
	'spring_fixed.c': 	k_1,
	'spring_middle.c':	k_12
}    
    
initial_conditions = {
    
	'mass.u':	u0_1, 
	'mass.v':	v0_1, 
	'mass.a':	a0_1
    
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
