# Install Dependencies

* [preCICE](https://github.com/precice/precice)
* [python bindings](https://github.com/precice/python-bindings)
* [FMPy](https://fmpy.readthedocs.io/en/latest/)

# Running a simulation

* Clone this repo
* Go to [FMUs](../../FMUs) and compile the `FallingBall` model
* Copy the compiled model into this directory 
* Run `SolverFMU.py` and `SolverAero.py` in two terminals
* Plot the results by running the `plot-watchpoint.sh` script. It takes the directory of the result files as an input argument, so run `./plot-watchpoint.sh .` from this directory. 
