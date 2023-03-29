## Notes on the current progress

- 3 way coupling works
- simulation crashes after some time, probably because the mesh around the cylinder is too fine
- another solution could be to use implicit coupling, this would help too

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
