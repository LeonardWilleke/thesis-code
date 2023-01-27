# FallingBall

The FallingBall implements the following system of equations:

```
der(v) = a_tot
a_tot = g - a_drag
```

with the variables

| Variable | Start | Unit | Causality | Variability | Description
|:---------|------:|:-----|-----------|-------------|:---------------
| v        |     0 | m/s  | output    | continuous  | Velocity of the ball
| der(v)   |       | m/s2 | local     | continuous  | Derivative of v
| a_tot    |     0 | m/s2 | parameter | fixed       | Total acceleration acting on the ball
| g        | -9.81 | m/s2 | parameter | fixed       | Gravity acting on the ball
| a_drag   |     0 | m/s2 | parameter | fixed       | Acceleration by aerodynamic drag acting on the ball
