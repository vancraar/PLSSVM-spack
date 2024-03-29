# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
#     spack install plssvm
#
# You can edit this file again by typing:
#
#     spack edit plssvm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *

def default_cuda_arch(possible_archs):
    gpus=[]
    try:
        import ctypes

        driver = ctypes.cdll.LoadLibrary("libcuda.so")
        flags = ctypes.c_int(0)

        driver.cuInit(flags)
        count = ctypes.c_int(0)
        driver.cuDeviceGetCount(ctypes.pointer(count))

        for device in range(count.value):
            major = ctypes.c_int(0)
            minor = ctypes.c_int(0)
            driver.cuDeviceComputeCapability(
                    ctypes.pointer(major),
                    ctypes.pointer(minor),
                    device)
            target = "{}{}".format(major.value,minor.value)
            if target in possible_archs:
                gpus.append(major.value*10+minor.value)
    except:
        pass

    return "none" if not gpus else list(set(gpus))

def amd_arch():
    from pathlib import Path
    gpus = []
    try:
        nodes = Path('/sys/class/kfd/kfd/topology/nodes')
        for filename in nodes.glob('*/properties'):
            with filename.open() as f:
                for line in f:
                    label = 'gfx_target_version '
                    if not line.startswith(label):
                        continue
                    version = int(line[len(label):])
                    if not version:
                        break
                    major_version = version // 10000
                    minor_version = (version // 100) % 100
                    step_version = version % 100
                    target = 'gfx{:d}{:x}{:x}'.format(major_version, minor_version, step_version)
                    gpus.append(target)
    except:
        pass
    return "none" if not gpus else ",".join(gpus)

plssvm_unsupported_cuda_archs=[
    "10", "11", "12", "13",
    "20", "21",
    "30", "32", "35", "37"
]

class Plssvm(CMakePackage,CudaPackage, ROCmPackage):
    """Implementation of a parallel least squares support vector machine using multiple backends for different GPU vendors. """

    # FIXME: Add a proper url for your package's homepage here.
    git = "https://github.com/SC-SGS/PLSSVM.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar", "breyerml")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("MIT")

    # FIXME: Add proper versions here.
    version("develop", branch="test")




    variant("openmp", default=True, description="Enable OpenMP support")
    # variant("cuda", default=False, description="Enable CUDA support")
    # variant("cuda_arch", default=cuda_arch(), when="+cuda", description="CUDA architecture")
    supported_cuda_archs = [x for x in CudaPackage.cuda_arch_values ]#if x not in plssvm_unsupported_cuda_archs ]
    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs,
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+cuda",
    )

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        # values=ROCmPackage.amdgpu_targets,
        default=amd_arch(),
        multi=True,
        sticky=True,
        when="+rocm",
    )

    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs+["none"],
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+opencl",
    )

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        # values=ROCmPackage.amdgpu_targets,
        default=amd_arch(),
        multi=True,
        sticky=True,
        when="+opencl",
    )





    variant("python", default=False, description="Build with Python Bindings")
    variant("python_preferred_label_type", default="std::string", when="+python", values=("bool","char","signed char","unsigned char","short","unsigned short","int","unsigned int","long","unsigned long","long long","unsigned long long","float","double","long double","std::string"), multi=False, description="Prefered label type for python bindings")
    variant("test", default=False, description="Enable testing") # TODO: enable spack testing
    variant("test_file", default=False, when="+test", description="Generate custom test_file with a specific size")
    variant("test_file_num_data_points", default=5000, values=int, when="+test_file", description="Number of data points in the test file")
    variant("test_file_num_features", default=2000, values=int, when="+test_file", description="Number of features in the test file")
    variant("test_file_num_classes", default=5, values=int, when="+test_file", description="Number of different labels in the test file")
    variant("documentation", default=False, description="Enable documentation")

    variant("asserts", default=False, description="Enable asserts") # TODO: default enable with debug mode
    variant("real_type", default="double", values=("float","double"), multi=False, description="Real type to use for the SVM")
    variant("thread_block_size", default=8, values=int, description="Thread block size for the backend kernels")
    variant("internal_block_size", default=4, values=int, description="Block size for the internal caching of the backend kernels")

    variant("lto", default=True, description="Enable link time optimization")

    variant("enforce_max_mem_alloc_size", default=True, description="Enforce a maximum memory allocation size for the backends")

    variant("performance_tracking", default=False, description="Enable performance tracking")

    variant("opencl", default=False, description="Enable OpenCL support")

    variant("hipsycl", default=False, description="Enable HIP SYCL support")

    variant("sycl", default=False, description="Enable SYCL support")
    conflicts("+sycl", msg="SYCL support is not yet implemented")


    # FIXME: Add dependencies if required.

    depends_on("fmt@10.2.1:")
    depends_on("cxxopts@3.1.1:")
    depends_on("igor@master")
    depends_on("fast-float@3.10.0")
    depends_on("googletest@1.14.0:", when="+test")

    depends_on("cmake@3.21:", type="build")
    depends_on("opencl", when="+opencl")

    depends_on("pocl", when="+opencl")


    depends_on("python@3:", when="+python")
    depends_on("py-pybind11@2.11.1:", when="+python")

    depends_on("doxygen@1.9.8:+graphviz", when="+documentation")

    depends_on("py-scikit-learn", when="+test_file")
    depends_on("py-humanize", when="+test_file")
    depends_on("py-numpy", when="+test_file")

    depends_on("hipsycl@23.10.0:", when="+hipsycl~cuda~rocm")
    depends_on("hipsycl@23.10.0:+cuda", when="+hipsycl+cuda~rocm")

    variant("dpcpp", default=False, description="Enable SYCL integration.")
    variant(
        "sycl_target_arch", default="none",
        values=(("none", "intel", "nvidia") + CudaPackage.cuda_arch_values + ROCmPackage.amdgpu_targets),
        description=("GPU target for SYCL. Can be generic with \'intel\' and \'nvidia\', or target a "
                     "specific GPU arch (required for AMD GPUs, optional for NVIDIA GPUs, unavaible "
                     "for Intel GPUs - just select intel for those)."),
    )


    # Depend on compiler that is being used for sycl
    # This ensures that, for example, dpcpp supports the cuda backend
    # when a NVIDIA device is being used
    # depends_on("dpcpp@2023-03:", when="+dpcpp ")
    depends_on("dpcpp@2023-03: +cuda", when="+dpcpp")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on("dpcpp@2023-03: +cuda",
                   when="+dpcpp sycl_target_arch={0}".format(cuda_arch))
    for amdgpu_arch in ROCmPackage.amdgpu_targets:
        depends_on("dpcpp@2023-03: +hip hip-platform=AMD",
                   when="+dpcpp sycl_target_arch={0}".format(amdgpu_arch))


    # SYCL CUDA/HIP backends require target arch informations to
    # set the correct flags later on:
    conflicts("+dpcpp", when="sycl_target_arch=none",
              msg=("Additional information to select the correct sycl backend."
                   " Use either a specific nvidia/amdgpu GPU architecture "
                   "(useful for compiling the tests/examples), or \'nvidia\' "
                   "\'intel\' in case a specific architecture is not targeted."))



    # parallel = False

    @run_before('configure')
    def check_cuda_arch(self, arch):
        if not "cuda_arch=none" in self.spec:
            depends_on("cuda", when="+opencl")

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix + '/install/lib/')

    @property
    def build_targets(self):
        if "+documentation" in self.spec:
            return ["all","doc"]
        return ["all"]


    def cmake_args(self):
        args = []
        args += [self.define_from_variant("PLSSVM_ENABLE_OPENMP_BACKEND", "openmp")]
        args += [self.define_from_variant("PLSSVM_ENABLE_CUDA_BACKEND", "cuda")]


        args += [self.define_from_variant("PLSSVM_ENABLE_HIP_BACKEND", "rocm")]



        #args += [self.define("PLSSVM_ENABLE_TESTING", self.run_tests)]
        args += [self.define_from_variant("PLSSVM_ENABLE_TESTING", "test")]
        args += [self.define_from_variant("PLSSVM_ENABLE_ASSERTS", "asserts")]
        args += [self.define_from_variant("PLSSVM_ENABLE_LANGUAGE_BINDINGS", "python")]
        if "+python" in self.spec:
            args += [self.define("PLSSVM_PYTHON_BINDINGS_PREFERRED_LABEL_TYPE", self.spec.variants["python_preferred_label_type"].value)]
            args += [self.define_from_variant("PLSSVM_ENABLE_PYTHON_BINDINGS", "python")]

        args += [self.define_from_variant("PLSSVM_ENABLE_DOCUMENTATION", "documentation")]

        if "+test" in self.spec:
            args += [self.define_from_variant("PLSSVM_GENERATE_TEST_FILE", "test_file")]
            if "+test_file" in self.spec:
                args += [self.define("PLSSVM_TEST_FILE_NUM_DATA_POINTS", self.spec.variants["test_file_num_data_points"].value)]
                args += [self.define("PLSSVM_TEST_FILE_NUM_FEATURES", self.spec.variants["test_file_num_features"].value)]
                args += [self.define("PLSSVM_TEST_FILE_NUM_CLASSES", self.spec.variants["test_file_num_classes"].value)]



        if self.spec.variants["real_type"].value == "float":
            args += [self.define("PLSSVM_USE_FLOAT_AS_REAL_TYPE", "ON")]
        else:
            args += [self.define("PLSSVM_USE_FLOAT_AS_REAL_TYPE", "OFF")]



        args += [self.define("PLSSVM_THREAD_BLOCK_SIZE", self.spec.variants["thread_block_size"].value)]
        args += [self.define("PLSSVM_INTERNAL_BLOCK_SIZE", self.spec.variants["internal_block_size"].value)]

        args += [self.define_from_variant("PLSSVM_ENABLE_LTO", "lto")]

        args += [self.define_from_variant("PLSSVM_ENFORCE_MAX_MEM_ALLOC_SIZE", "enforce_max_mem_alloc_size")]

        args += [self.define_from_variant("PLSSVM_ENABLE_PERFORMANCE_TRACKING", "performance_tracking")]

        args += [self.define_from_variant("PLSSVM_ENABLE_OPENCL_BACKEND", "opencl")]

        args += [self.define_from_variant("PLSSVM_ENABLE_SYCL_BACKEND", "dpcpp")]

        args += [self.define_from_variant("PLSSVM_ENABLE_HIPSYCL_BACKEND", "hipsycl")]



        target_arch = []
        print(self.spec.variants["openmp"].value)
        print(type(self.spec.variants))
        if "cuda_arch" in self.spec.variants:
            target_arch += ["nvidia:sm_" + ",sm_".join(self.spec.variants["cuda_arch"].value)]
        if "amdgpu_target" in self.spec.variants and not "none" in self.spec.variants["amdgpu_target"].value:
            target_arch += ["amd:" + ",".join(self.spec.variants["amdgpu_target"].value)]
        if self.spec.variants["openmp"].value:
            target_arch += ["cpu"]
            print("CPU")

        args += [self.define("PLSSVM_TARGET_PLATFORMS", ";".join(target_arch))]


        # SYCL support requires compiling with dpcpp clang
        if "+dpcpp" in self.spec:
            # Set compiler to dpcpp
            args += [self.define("CMAKE_CXX_COMPILER",
                                 "{0}/bin/clang++".format(self.spec["dpcpp"].prefix))]



        return args

