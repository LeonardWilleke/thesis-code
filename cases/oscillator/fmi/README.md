## FMI Runner

The script `runner.py` is a first approach towards a general preCICE-FMI Runner. Currently, it has the following limitations:

- Only works for models using FMI2, not for FMI1 and FMI3
- Can only read and write scalar data

### Set parameters

The settings and parameters for the FMU model are saved in `fmuSettings.py`. Equally, all variables needed to set up preCICE can be found in `preciceSettings.py`. For the simulation of the left mass, these files are provided in `MassLeft`. The files for the right mass are in `MassRight`, respectively.

### Running the simulation

Open two separate terminals and start both participants by calling:

```
python runner.py ./MassLeft
```
and

```
python runner.py ./MassRight
```

The `runner` script takes the path to the folder of the two setting files as input. 
