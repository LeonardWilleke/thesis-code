# PID Controller

The PID Controller implements the following system of equations:

```
e = r - y
u = kp*e + ki*e*dt + kd*(e-e_ls)*(1/dt)
```

with the variables

| Variable | Start | Causality | Variability | Description
|:---------|------:|-----------|-------------|:---------------
| u        |     0 | output    | continuous  | Control output
| y        |     0 | parameter | tunable     | Control input
| r        |     0 | parameter | tunable     | Reference value
| e        |     - | local     | continuous  | Error between input and reference
| e_ls     |     - | local     | continuous  | Error between input and reference from last time step
| kp       |     0 | parameter | tunable     | Proportional gain
| ki       |     0 | parameter | tunable     | Integral gain
| kd       |     0 | parameter | tunable     | Derivative gain
| dt       |  1e-2 | parameter | tunable     | Solver step size

