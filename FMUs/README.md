## FMUs

A set of FMU models for development and testing of the preCICE-FMI Runner. The models follow the [Functional Mock-up Interface](https://fmi-standard.org/) standard and are created using the [OpenModelica Editor](/OpenModelica) or [CMake](/cmake).

- FallingBall - a falling ball model for coupling with an aerodynamic solver
- FeedBack - PID controller with a second order function as "plant" to control
- OscillatorMonolith - 1D-Oscillator consisting of two masses and three springs
- MassLeft - Left part of 1D-Oscillator for partitioned simulation
- MassRight - Right part of 1D-Oscillator for partitioned simulation
- Oscillator - Partition of 1D-Oscillator which can be used as left and right side during partitioned simulation
- PIDcontrollerOM - PID controller exported from OpenModelica
