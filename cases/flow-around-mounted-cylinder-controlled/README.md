## Parallel execution

To run OpenFOAM in parallel, run the following commands for the Fluid participant:

```bash
decomposePar
mpirun -np 2 pimpleFoam -parallel
```

This should reduce the runtime by ca 50%. However, I currently can't properly plot the results with ParaView.
But the watchpoint is still created as usual!

You can still run the case in serial with the usual

```bash
pimpleFoam
```


## Notes on the current progress

Current status:
- 3 way coupling works
- parameters fit with the case in Sicklinge
- implicit coupling with acceleration
- parallel execution of OpenFOAM is possible

Problem: Runtime
- A simulated time of 45s with delta_t = 1e-4 is necessary to recreate Sicklinger
- The simulation needs to run so long to get a locked-in cylinder movement, before then the controller is started at t=40s to counter this oscillation
- My computer is way to slow for this: to simulate 1s takes ca. 1h!


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