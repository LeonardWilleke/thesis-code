---
title: Oscillator
permalink: tutorials-oscillator.html
keywords: Python, ODE, FMI
summary: We solve an oscillator with two masses in a partitioned fashion. Each mass is solved by an independent ODE.
---

{% note %}
Get the [case files of this tutorial](https://github.com/precice/tutorials/tree/master/oscillator). Read how in the [tutorials introduction](https://www.precice.org/tutorials.html).
{% endnote %}

## Setup

This tutorial solves a simple mass-spring oscillator with two masses and three springs. The system is cut at the middle spring and solved in a partitioned fashion:

![Schematic drawing of oscillator example](images/tutorials-oscillator-schematic-drawing.png)

Note that this case applies a Schwarz-type coupling method and not (like most other tutorials in this repository) a Dirichlet-Neumann coupling. This results in a symmetric setup of the solvers. We will refer to the solver computing the trajectory of $m_1$ as `Mass-Left` and to the solver computing the trajectory of $m_2$ as `Mass-Right`. For more information, please refer to [1].

## Available solvers

This tutorial is only available in Python. You need to have preCICE and the Python bindings installed on your system.

- *Python*: An example solver using the preCICE [Python bindings](https://www.precice.org/installation-bindings-python.html). This solver also depends on the Python libraries `numpy`, which you can get from your system package manager or with `pip3 install --user <package>`.
- *FMI*: An example solver using FMU models for computation. This solver depends on the Python libraries `numpy` and `FMPy` which you can install with conda or pip, for example `pip3 install --user fmpy`. You also need the compiled FMU model `Oscillator.fmu`. The model for Linux is part of this repository in the folder [FMUs](../../FMUs). For other systems, please recompile the model from the provided [C-files](../../FMUs/cmake). If you want to change the model parameters or the initial conditions of the simulation, have a look inside the setting files for [MassLeft](fmi/MassLeft) and [MassRight](fmi/MassRight).

## Running the Simulation

You can either run both participants with one of the two solvers or use a separate solver for each participant.

### Python

Open two separate terminals and start both participants by calling:

```bash
cd python
./run.sh -l
```

and

```bash
cd python
./run.sh -r
```

### FMI

Open two separate terminals and start both participants by calling:

```bash
cd fmi
./run.sh -l
```

and

```bash
cd fmi
./run.sh -r
```

## Post-processing

Each simulation run creates two files containing position and velocity of the two masses over time. These files are called `trajectory-Mass-Left.csv` and `trajectory-Mass-Right.csv`. You can use the script `plot-trajectory.py` for post-processing. Type `python3 plot-trajectory --help` to see available options. You can, for example, plot the trajectory of the Python solver by running

```bash
python3 plot-trajectory.py python/output/trajectory-Mass-Left.csv TRAJECTORY
```

The solvers allow you to study the effect of different time stepping schemes on energy conservation. Newmark beta conserves energy:

![Trajectory for Newmark beta scheme](images/tutorials-oscillator-trajectory-newmark-beta.png)

Generalized alpha does not conserve energy:

![Trajectory for generalized alpha scheme](images/tutorials-oscillator-trajectory-generalized-alpha.png)

For details, refer to [1].

## References

[1] V. Schüller, B. Rodenberg, B. Uekermann and H. Bungartz, A Simple Test Case for Convergence Order in Time and Energy Conservation of Black-Box Coupling Schemes, in: WCCM-APCOM2022. [URL](https://www.scipedia.com/public/Rodenberg_2022a)

