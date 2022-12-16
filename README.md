# FMI-Runner

preCICE-Runner for models written in the FMI standard

# Install Dependencies

* [preCICE](https://github.com/precice/precice)
* [python bindings](https://github.com/precice/python-bindings)
* [FMPy](https://github.com/CATIA-Systems/FMPy)

# Run a simulation

* Build the [FMU model](FMUs) you want to couple 
* Copy the compiled model over to the respective case directory
* Run each solver in a seperate terminal 

# Build the FMUs

To build the FMUs you need [CMake](https://cmake.org/) and a supported [build tool](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html) e.g. Visual Studio &GreaterEqual; 2013 , Xcode or make:

- download or clone the repository

- open the [CMakeGUI](https://cmake.org/runningcmake/)

- click `Browse Source...` and select the `FMUs` folder of the repository (that contains `CMakeLists.txt`)

- click `Browse Build...` and select the folder where you want build the FMUs

- click `Configure` and select the generator for your IDE / build tool

- select the `FMI_VERSION` you want to build (in our case `FMI3`)

- select the `FMI_TYPE`you want to build (in our case `CS`) 

- click `Generate` to generate the project files

- click `Open Project` or open the project in your build tool

- build the project

The FMUs will be in the `fmus` folder inside the selected build folder.
