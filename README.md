# preCICE-FMI Runner

The [Functional Mock-Up Interface](https://fmi-standard.org/) (FMI) is a standard for the exchange of dynamic simulation models. Currently, it is the de-facto industry standard for co-simulation. The models implementing the FMI standard are called Functional Mock-Up Units (FMU).

This project aims to couple FMU models with other simulation tools with the coupling library [preCICE](https://precice.org/). To this end, a preCICE-FMI Runner is being developed (see image). The Runner serves as an importer for the FMU to steer the simulation. Additionally, it calls the preCICE library to communicate and coordinate with other solvers. 

![img](images/precice-fmi-runner-setup.png)

An open question is to what end the coupling can be generalized. Therefore, as a first milestone the Runner should be able to couple controller models with PDEs. In this scenario, the FMU contains a simple control algorithm like a PID controller. It is combined with simulation tools like OpenFOAM or FEniCs to simulate a Fluid-Structure Interaction.

A test case inspired by Sicklinger [1] is the air flow around a mounted cylinder. The vortex shedding of the flow brings the cylinder to oscillate in the y-direction. The oscillation can be counteracted by moving the root point of the spring. To adjust the root point accordingly, a PID controller is implemented. Here, OpenFOAM is used to simulate the air flow, the rigid cylinder and the spring-damper system, while the PID algorithm is calculated in a FMU. 

![img](images/test-case-setup.png)

## Dependencies

* [preCICE](https://github.com/precice/precice)
* [python bindings](https://github.com/precice/python-bindings)
* [FMPy](https://github.com/CATIA-Systems/FMPy)

## Run a simulation

* Clone the repository
* Check the [FMU models](FMUs). If you are not using a Linux-based system, you will have to recompile them from the provided files
* Select a [simulation case](cases)
* Run the provided solvers

All instructions are given for Linux.

## References

[1] Sicklinger, [Stabilized Co-Simulation of Coupled Problems including Fields and Signals](https://www.researchgate.net/publication/269705153_Stabilized_Co-Simulation_of_Coupled_Problems_Including_Fields_and_Signals), Technical University of Munich, Dissertation, 
