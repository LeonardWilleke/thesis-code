# FallingBall

The FallingBall implements the following system of equations:

```
der(v) = g
```

with the variables

| Variable | Start | Unit | Causality | Variability | Description
|:---------|------:|:-----|-----------|-------------|:---------------
| v        |     0 | m/s  | output    | continuous  | Velocity of the ball
| der(v)   |       | m/s2 | local     | continuous  | Derivative of v
| g        | -9.81 | m/s2 | parameter | fixed       | Gravity acting on the ball

