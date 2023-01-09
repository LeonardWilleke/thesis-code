# FMUs

A set of hand-coded FMUs for development, testing and debugging of the coupling of preCICE with models written in the [Functional Mock-up Interface](https://fmi-standard.org/).

- [FallingBall](FallingBall) - a falling ball model for coupling with an aerodynamic solver

## Build the FMUs with CMake

To build the FMUs you need [CMake](https://cmake.org/) &GreaterEqual; 3.16 and a supported [build tool](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html) e.g. Visual Studio &GreaterEqual; 2013 , Xcode or make.

Generate the build files with the following commands:

```
mkdir build
cd build
cmake -DFMI_TYPE=CS -DFMI_VERSION=3 ..

```
Then run `make` or your preferred build tool to create the FMUs. They will be in the `fmus` folder inside `build`. 

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

## License and attribution

The models and cmake code are a fork of the [Reference FMUs](https://github.com/modelica/Reference-FMUs) from the Modelica Association Project "FMI". The [Reference FMUs](https://github.com/modelica/Reference-FMUs) themselves are a fork of the [Test FMUs](https://github.com/CATIA-Systems/Test-FMUs) by Dassault Syst&egrave;mes, which are a fork of the [FMU SDK](https://github.com/qtronic/fmusdk) by QTronic. All three are released under the 2-Clause BSD License.
