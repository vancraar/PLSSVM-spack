## PLSSVM-Spack

This repository contains the [Spack](https://github.com/spack/spack#-spack) package for the [Parallel Least Squares Support Vector Machine -- PLSSVM](https://github.com/SC-SGS/PLSSVM)


### Modifications
- new package for fast_float
- new package for igor
- pocl: additional version
- dpcpp: TODO
- fmt: TODO

Additions and changes might eventually be submitted to the main spack repository! For now, this repo allows me to rapidly experiment with different builds on different machines until I get to the point where all PLSSVM features and relevant versions are working on the intended target platforms.

### Repo installation:

```sh
# spack install
git clone --depth=100 --branch=releases/v0.21.2 https://github.com/spack/spack.git /path/to/spack
cd /path/to/spack
. share/spack/setup-env.sh
# spack repo install
git clone git@github.com:vancraar/PLSSVM-spack.git /path/to/plssvm-spack
spack repo add /path/to/plssvm-spack
# use system packages
spack compiler find # search currently loaded compilers
spack external find cuda # replace cuda by desired packages or leave blank
# Check package availability and its variants:
spack info plssvm
```
