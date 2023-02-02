## FMI Runner

The script `runner.py` is a first approach towards a general preCICE-FMI Runner. Currently, it has the following limitations:

- Only works for models using FMI2, not for FMI1 and FMI3
- Can only read and write scalar data
- No logging of internal FMU data

### Preparing the simulation

The settings and parameters stored in two files: `fmuSettings.py` and `preciceSettings.py`. The files can be found in the subfolders `MassLeft` and `MassRight` for the respective partitions.

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

### Post-processing

The displacement of `mass1` is being recorded during simulation. The results can be visualized with a provided plot script:

```
bash plot-displacement.sh .
```
