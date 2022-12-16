# Test FMUs

A set of hand-coded FMUs for development, testing and debugging of the coupling of preCICE with models written in the [Functional Mock-up Interface](https://fmi-standard.org/).

- [FallingBall](FallingBall) - a falling ball model for coupling with an aerodynamic solver

## Run the FMUs with preCICE

After building the model successfully, copy the .fmu file to the respective case folder. For example, the compiled model `FallingBall.fmu` is needed in the case folder [falling-ball](../cases/falling-ball) to run the simulation. 

## Repository structure

`<model>`
- `config.h` - model specific types and definitions
- `FMI{1CS|1ME|2|3}.xml` - model descriptions
- `model.c` - implementation of the model

`include`
- `fmi{|2|3}Functions.h` - FMI header files
- `model.h` - generic model interface
- `cosimulation.h` - generic co-simulation interface

`src`
- `fmi{1|2|3}Functions.c` - FMI implementations
- `cosimulation.c` - generic co-simulation

## Build the FMUs

To build the FMUs you need [CMake](https://cmake.org/) and a supported [build tool](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html) e.g. Visual Studio &GreaterEqual; 2013 , Xcode or make:

- download or clone the repository

- open the [CMakeGUI](https://cmake.org/runningcmake/)

- click `Browse Source...` and select the cloned or downloaded and extracted repository (that contains `CMakeLists.txt`)

- click `Browse Build...` and select the folder where you want build the FMUs

- click `Configure` and select the generator for your IDE / build tool

- select the `FMI_VERSION` you want to build (in our case `FMI3`)

- select the `FMI_TYPE`you want to build (in our case `CS`) 

- click `Generate` to generate the project files

- click `Open Project` or open the project in your build tool

- build the project

The FMUs will be in the `fmus` folder inside the selected build folder.

## License and attribution

The models and cmake code are a fork of the [Reference FMUs](https://github.com/modelica/Reference-FMUs) from the Modelica Association Project "FMI". The [Reference FMUs](https://github.com/modelica/Reference-FMUs) themselves are a fork of the [Test FMUs](https://github.com/CATIA-Systems/Test-FMUs) by Dassault Syst&egrave;mes, which are a fork of the [FMU SDK](https://github.com/qtronic/fmusdk) by QTronic. All three are released under the 2-Clause BSD License.
