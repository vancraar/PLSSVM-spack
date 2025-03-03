# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install adaptivecpp
#
# You can edit this file again by typing:
#
#     spack edit adaptivecpp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
from spack.compiler import Compiler


class Adaptivecpp(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://adaptivecpp.github.io/"
    git  = "https://github.com/AdaptiveCpp/AdaptiveCpp"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar", "breyerml")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("BSD-2-Clause", checked_by="vancraar")

    # FIXME: Add proper versions and checksums here.
    version("24.10.0", commit="7677cf6eefd8ab46d66168cd07ab042109448124", submodules=True)
    version("24.06.0", commit="fc51dae9006d6858fc9c33148cc5f935bb56b075", submodules=True)
    version("24.02.0", commit="974adc33ea5a35dd8b5be68c7a744b37482b8b64", submodules=True)
    version("23.10.0", commit="3952b468c9da89edad9dff953cdcab0a3c3bf78c", submodules=True)

    variant("cuda", default=False, description="Enable CUDA backend for SYCL kernels")
    variant("rocm", default=False, description="Enable ROCm backend for SYCL kernels")
    variant("opencl", default=False, description="Enable OpenCL backend for SYCL kernels")
    variant("level-zero", default=False, description="Enable Level Zero backend for SYCL kernels")

    variant("omp-library-only", default=False, description="Only build the OpenMP library")
    variant("omp-accelerated", default=True, description="Build the OpenMP library with accelerated kernels")
    conflicts("omp-library-only", when="+omp-accelerated", msg="Cannot build the OpenMP library with accelerated kernels and only the OpenMP library")
    variant("cuda-integrated-multipass", default=False, description="Enable CUDA integrated multi-pass")
    variant("cuda-explicit-multipass", default=False, description="Enable CUDA explicit multi-pass")
    conflicts("cuda-explicit-multipass", when="cuda-explicit-multipass", msg="Cannot enable CUDA explicit multi-pass with CUDA integrated multi-pass")
    variant("cuda-nvcxx", default=False, description="Enable CUDA nvcxx")
    conflicts("cuda-nvcxx", when="~cuda", msg="Cannot enable CUDA nvcxx without CUDA")
    conflicts("cuda-nvcxx", when="+cuda-integrated-multipass", msg="Cannot enable CUDA nvcxx with CUDA integrated multi-pass")
    conflicts("cuda-nvcxx", when="+cuda-explicit-multipass", msg="Cannot enable CUDA nvcxx with CUDA explicit multi-pass")
    variant("hip-integrated-multipass", default=False, description="Enable HIP integrated multi-pass")
    variant("hip-explicit-multipass", default=False, description="Enable HIP explicit multi-pass")
    conflicts("hip-explicit-multipass", when="+hip-integrated-multipass", msg="Cannot enable HIP explicit multi-pass with HIP integrated multi-pass")
    conflicts("hip-integrated-multipass", when="+cuda-integrated-multipass", msg="Cannot enable HIP integrated multi-pass with CUDA integrated multi-pass")
    variant("generic", default=True, sticky=True, description="Generic build")
    variant("stdpar", default=False, description="Enable stdpar")
    conflicts("stdpar", when="+omp-library-only", msg="Cannot enable stdpar wit omp-library-only")
    conflicts("stdpar", when="+cuda-nvcxx", msg="Cannot enable stdpar wit nvcxx")




    conflicts("%gcc") #TODO enable omp-library-only with gcc


    depends_on("llvm") # remove if bug with llvm 18 is fixed

    # FIXME: Add dependencies if required.
    depends_on("python@3:")
    depends_on("cmake@3.9:", type="build")
    depends_on("boost +fiber+context+atomic+filesystem")
    depends_on("llvm@11: +clang", when="+omp-accelerated")
    depends_on("cuda@10:", when="+cuda-integrated-multipass")
    depends_on("llvm@10:", when="+cuda-integrated-multipass")
    depends_on("cuda@10:", when="+cuda-explicit-multipass")
    depends_on("llvm@13:", when="+cuda-explicit-multipass")
    depends_on("llvm@13:", when="+hip-explicit-multipass")
    depends_on("nvhpc", when="+cuda-nvcxx")
    depends_on("hip@4:", when="+hip-integrated-multipass")
    depends_on("cuda@10:", when="+cuda")

    depends_on("hip@5.3:", when="+rocm+generic")
    depends_on("llvm@14:", when="hip@5.0:") #TODO Version
    depends_on("llvm@15:", when="hip@5.2:") #TODO Version
    depends_on("llvm@16:", when="hip@5.4:") #TODO Version
    depends_on("llvm@17:", when="hip@6.0:") #TODO Version
    depends_on("llvm@18:", when="hip@6.2:") #TODO Version
    # depends_on("llvm compiler-rt=project    ", when="+rocm+generic")




    depends_on("llvm@14: +clang+llvm_dylib", when="+generic")
    # depends_on("hip@5.3:", when="+generic") TODO amd
    depends_on("llvm@14:", when="+cuda+generic")
    depends_on("llvm@14:", when="+stdpar")
    depends_on("llvm@14:", when="+stdpar+cuda")





    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        args += [self.define_from_variant("WITH_ACCELERATED_CPU", "omp-accelerated")]
        if "+cuda" in self.spec or "+nvhpc" in self.spec:
            args += [self.define("WITH_CUDA_BACKEND", "ON")]
        else:
            args += [self.define("WITH_CUDA_BACKEND", "OFF")]
        if "+cuda-nvcxx" in self.spec:
            args += [self.define("NVCXX_COMPILER","{0}/bin/nvc++".format(self.spec["nvhpc"].prefix))]
        if self.version <= Version("24.06.0"):
            args += [self.define_from_variant("WITH_SSCP_COMPILER", "generic")]
            args += [self.define_from_variant("WITH_SDTPAR_COMPILER", "stdpar")]
            if "+omp-library-only" in self.spec or "+omp-accelerated" in self.spec or "+generic" in self.spec:
                args += [self.define("WITH_ACCELERATED_CPU", "ON")]
            else:
                args += [self.define("WITH_ACCELERATED_CPU", "OFF")]
        else:
            args += [self.define_from_variant("SSCP", "generic")]
            args += [self.define_from_variant("stdpar", "stdpar")]
            if "+omp-library-only" in self.spec or "+omp-accelerated" in self.spec or "+generic" in self.spec:
                args += [self.define("accelerated cpu", "ON")]
            else:
                args += [self.define("accelerated cpu", "OFF")]



        # args += [self.define("CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(self.spec["llvm"].prefix))]
        # args += [self.define("CMAKE_C_COMPILER", "{0}/bin/clang".format(self.spec["llvm"].prefix))]
        if "llvm-admgpu" in self.spec:
            args += [self.define("LLVM_DIR", "{0}".format(self.spec["llvm-admgpu"].prefix))]
        elif "llvm" in self.spec:
            args += [self.define("LLVM_DIR", "{0}/lib/cmake/llvm".format(self.spec["llvm"].prefix))]

        args += [self.define_from_variant("WITH_ROCM_BACKEND", "rocm")] #TODO
        args += [self.define_from_variant("WITH_OPENCL_BACKEND", "opencl")] #TODO
        args += [self.define_from_variant("WITH_LEVEL_ZERO_BACKEND", "level-zero")] #TODO
        # args += [self.define("HIP_PATH", "{0}".format(self.spec["hip"].prefix))]

        return args
