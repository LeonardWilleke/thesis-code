## Notes on the current progress

- Case file is set up for coupling of 3 participants
- Spring and Controller are ready for coupling
- OpenFOAM exits because it cant find the pointDisplacement file. I added a respective file, but something else is still wrong.

The error reads

```bash
Cannot find file "points" in directory "polyMesh" in times "0" down to constant
```

and is connected to the function call 

```bash
Selecting dynamicFvMesh dynamicMotionSolverFvMesh
```

## Similar case from OpenFOAM tutorials

Have a look into this OpenFOAM tutorial. It seems to implement the Sicklinger case already. 

It has two major benefits over my current approach:
- the spring is internal to OpenFOAM, which means I can avoid multi-coupling
- instead of a cylinder, a wing is used. Maybe I can implement some case related to wind energy

I already have the case files locally. To go there, run:

```bash
cd ~/Thesis/openfoam/tutorials/incompressible/pimpleFoam/RAS/wingMotion/wingMotion2D_pimpleFoam
```

You need to use the Allrun script to run it, because some meshes need to be created before pimpleFoam can run. For future use

- Create a script to only run pimpleFoam with the necessary mesh build commands
- Find out how to run OF in parallel
- Never run for 5 seconds simulated time
- Always check stepsize before you run

! I currently dont know how the stepsize is set. Have a look at this.

You can also find the case online in the [OF tutorial repo](https://github.com/OpenFOAM/OpenFOAM-6/tree/master/tutorials/incompressible/pimpleFoam/RAS/wingMotion)
