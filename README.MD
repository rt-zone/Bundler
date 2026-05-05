# Bundler scripts

This script requires 'pibody_libs' repository as its neighbor. 

This script is very raw, only made as fast solution to a PiBody November 2025 version. 

This script requires work, but has great potential as it combines pibody_libs and firmware.uf2 in single pibody.uf2

TODO:

1) Create a build folder and re-write scripts so that they will output everything to a build folder
2) Change the way how script gets source files (namely, firmware.uf2 and pibody_libs). Maybe the pre-requisite is to locate this repo alongside with the raw_files. Or have an src folder.
3) store all .py files in the same folder. Only makefile should be exposed
