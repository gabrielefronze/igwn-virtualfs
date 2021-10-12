# igwn-virtualfs

This is a WIP prototype to demonstrate the idea of a virtualfs made of symlinks and directories, aimed at decoupling the user representation of the IGWN data namespace and the actual underlying technology.

This is not a proper FS and relies on the fact CVMFS is correctly setup and working.
To start using this reorganized data organization simply clone the repo and, optionally, run `mkdir /igwnfs && ln -s ./igwnfs /igwnfs`.

The `setup.py` script is intended to be a script capable of generating programmatically the symlink tree in `igwnfs` ingesting the `framePaths.yml` file.

It is a good tool for creting forks specific to some computing centres, since in this case the process is simplified:
1. fork the repo
2. edit the `framePaths.yml` file to reflect what is locally available in your CC
3. run `setup.py`
4. commit and push
