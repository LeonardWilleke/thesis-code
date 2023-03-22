## Setup

This case solves the airflow around a cylinder and combines it with a control case. At the top and bottom of the cylinder, two jet streams are placed. These jets can produce a controlled airstream. The velocity of the stream is set by a second participant, a controller. The aim is to influence the airflow to reach a certain drag and lift force over the cylinder. The case is an adaption of [these cases](https://github.com/venturi123/DRLinFluids/tree/main/examples/active_flow_control) from [1].

## Available solvers

This tutorial is only available in Python and OpenFOAM. You need to have preCICE, OpenFOAM and the [Python bindings](https://www.precice.org/installation-bindings-python.html) installed on your system.

- *OpenFOAM*: 
- *Dummy*: A Python dummy used to test the coupling between OpenFOAM and the controller
- *FMI*: An example PID controller using FMU models for computation. This solver depends on the Python libraries `numpy` and `FMPy` which you can install with conda or pip, for example `pip3 install --user fmpy`. You also need the compiled FMU model `PIDcontroller.fmu`. The model for Linux is part of this repository in the folder [FMUs](../../FMUs). For other systems, please recompile the model from the provided [C-files](../../FMUs/cmake). If you want to change the model parameters, have a look inside the [setting files](controller-fmi/pid).

## Running the simulation

Currently, the OpenFOAM case can only be coupled with the dummy controller. To do so, open two seperate terminals and run the following commands:

```bash
cd fluid-openfoam
./run.sh
```

and

```bash
cd controller-dummy
./run.sh
```

## Post-processing

The OpenFOAM simulation creates result files every `0.1s`, which can be visualized with ParaView. The simplest way is as follows:

```bash
cd fluid-openfoam
paraFoam
```

Now you can apply the data from the simulation and animate the results. In the picture below, the velocity of the air flow is visualized at `t=0.1s`. The jet streams are clearly visible on top and below the cylinder.

![Results of a coupling of OpenFOAM with Dummy](images/flow-around-cylinder-controlled-result.eps)

## References

[1] Qiulei Wang (王秋垒), Lei Yan (严雷), Gang Hu (胡钢), Chao Li (李朝), Yiqing Xiao (肖仪清), Hao Xiong (熊昊), Jean Rabault, and Bernd R. Noack , "DRLinFluids: An open-source Python platform of coupling deep reinforcement learning and OpenFOAM", Physics of Fluids 34, 081801 (2022) https://doi.org/10.1063/5.0103113

## Contribution

Many thanks to Mosayeb Shams from Heriot-Watt University further adapted the test case for this use
