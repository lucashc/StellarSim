# StellarSim
For truly stellar simulations

## What is it?
This repository aims to simulate galaxies in a realistic manner. To this end, we use Barnes-Hut, Gravity Softening and LeapFrog integratin to fascilitate the simulation. Additionally, a Dark Matter potential can be enabled.

## How to use
First install the reuirements:
* A C++ compiler, preferably `g++`
* Python 3, specifically CPython, pypy and others will not work
* Then install the requirements: `pip install -r requirements.txt`

After this, the C++ library can be built: `cd barneshut_cpp && make build_cython && cd ..`
Finally, to run a scenario use: `python -m Scenarios.<Scenario name>`

### Save file types
The C++ library allows one to save BodyList3 objects and Result objects. The preferred extension for bodylists is `.bin` and for Result objects `.binv`. These files can later be loaded by the library. Also, `.binv` files can be 'played' by `intvis`, a visualization module based on Panda3D.

### Visualization
To visualize a `.bin` or `.binv`, use: ```python -m helper_files.intvis <filename>```
Additional options can be found by issuing: ```python -m helper_files.intvis --help```