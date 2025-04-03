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

    return ["none"] if not gpus else list(set(gpus))

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
    return ["none"] if not gpus else list(set(gpus))

plssvm_unsupported_cuda_archs=[
    "10", "11", "12", "13",
    "20", "21",
    "30", "32", "35", "37"
]

class Plssvm(CMakePackage,CudaPackage,  ):
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


    variant("hip", default=False, description="Enable HIP support")


    variant("openmp", default=True, description="Enable OpenMP support")
    variant("cuda", default=False, description="Enable CUDA support")
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
        description="HIP GPU architecture",
        values=list(ROCmPackage.amdgpu_targets)+list(["none"]),
        default=amd_arch()[0],
        multi=True,
        sticky=True,
        when="+hip",
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
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs+["none"],
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+icpx",
    )

    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs+["none"],
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+hip",
    )

    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs+["none"],
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+adaptivecpp",
    )
    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs+["none"],
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+stdpar",
    )

    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=supported_cuda_archs+["none"],
        default=default_cuda_arch(supported_cuda_archs)[0],
        multi=True,
        sticky=True,
        when="+kokkos",
    )


    variant(
        "amdgpu_target",
        description="HIP GPU architecture",
        values=list(ROCmPackage.amdgpu_targets)+list(["none"]),
        default=amd_arch()[0],
        multi=True,
        sticky=True,
        when="+opencl",

    )

    variant(
        "amdgpu_target",
        description="HIP GPU architecture",
        values=list(ROCmPackage.amdgpu_targets)+list(["none"]),
        default=amd_arch()[0],
        multi=True,
        sticky=True,
        when="+icpx",
    )
    variant(
        "amdgpu_target",
        description="HIP GPU architecture",
        values=list(ROCmPackage.amdgpu_targets)+list(["none"]),
        default=amd_arch()[0],
        multi=True,
        sticky=True,
        when="+adaptivecpp",
    )
    variant(
        "amdgpu_target",
        description="HIP GPU architecture",
        values=list(ROCmPackage.amdgpu_targets)+list(["none"]),
        default=amd_arch()[0],
        multi=True,
        sticky=True,
        when="+stdpar",
    )

    variant(
        "amdgpu_target",
        description="HIP GPU architecture",
        values=list(ROCmPackage.amdgpu_targets)+list(["none"]),
        default=amd_arch()[0],
        multi=True,
        sticky=True,
        when="+kokkos",
    )


    with when("build_system=cmake"):
        variant(
                "build_type",
                default="Release",
                description="CMake build type",
                values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Coverage"),
            )

    variant("python", default=False, description="Build with Python Bindings")
    variant("python_preferred_label_type", default="std::string", when="+python", values=("bool","char","signed char","unsigned char","short","unsigned short","int","unsigned int","long","unsigned long","long long","unsigned long long","float","double","long double","std::string"), multi=False, description="Prefered label type for python bindings")
    variant("test", default=False, description="Enable testing") # TODO: enable spack testing
    variant("test_file", default=False, when="+test", description="Generate custom test_file with a specific size")
    variant("test_file_num_data_points", default=5000, values=int, when="+test_file", description="Number of data points in the test file")
    variant("test_file_num_features", default=2000, values=int, when="+test_file", description="Number of features in the test file")
    variant("test_file_num_classes", default=5, values=int, when="+test_file", description="Number of different labels in the test file")
    variant("reducing_label_types", default=False, when="+test", description="Tests with reduced label types")
    variant("documentation", default=False, description="Enable documentation")
    variant("fast-math", default=True, description="Enable fast math optimizations")


    variant("asserts", default=False, description="Enable asserts") # TODO: default enable with debug mode
    variant("real_type", default="double", values=("float","double"), multi=False, description="Real type to use for the SVM")
    variant("thread_block_size", default=8, values=int, description="Thread block size for the backend kernels")
    variant("internal_block_size", default=4, values=int, description="Block size for the internal caching of the backend kernels")

    variant("lto", default=True, description="Enable link time optimization")

    variant("enforce_max_mem_alloc_size", default=True, description="Enforce a maximum memory allocation size for the backends")

    variant("performance_tracking", default=False, description="Enable performance tracking")

    variant("opencl", default=False, description="Enable OpenCL support")

    variant("adaptivecpp", default=False, description="Enable AdaptiveCpp SYCL integration")
    conflicts("+adaptivecppp", when="+lto", msg="Adaptivecpp does not work with lto")
    variant("adaptivecpp_SSCP", when="+adaptivecpp", default=True, description="Use AdaptiveCpp's new SSCP compilation flow.")

    variant("dpcpp", default=False, description="Enable DPC++ SYCL integration.")
    variant("dpcpp_aot", when="+dpcpp", default=True, description="Enable Ahead-of-Time (AOT) compilation for the specified target platforms.")
    variant("dpcpp_level_zero", when="+dpcpp", default=True, description="Use DPC++'s Level-Zero backend instead of its OpenCL backend (only available if a CPU or Intel GPU is targeted).")

    variant("icpx", default=False, description="Enable Intel SYCL integration")


    variant("stdpar", default=False, description="Enable stdpar backend") # TODO: dependancies
    conflicts("+stdpar", when="+adaptivecpp", msg="AdaptiveCpp backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+dpcpp", msg="DPC++ backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+icpx", msg="Intel SYCL backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+opencl", msg="OpenCL backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+cuda", msg="CUDA backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+hip", msg="HIP backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+openmp", msg="OpenMP backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+kokkos", msg="Kokkos backend is not compatible with stdpar backend.")
    conflicts("+stdpar", when="+hpx", msg="HPX backend is not compatible with stdpar backend.")

    requires("thread_block_size=1", when="+kokkos", msg="Kokkos Backend requires thread_block_size=1")


    variant("stdparimplementation",
            when="+stdpar",
            default="adaptivecpp",
            values=("adaptivecpp", "icpx", "gnu-tbb", "nvhpc", "roc")
    )

    requires("cuda_arch=none", when="stdparimplementation=roc")
    requires("amdgpu_target=none", when="stdparimplementation=nvhpc")

    requires("+cuda", "+hip", "+adaptivecpp", "+dpcpp", "+stdpar", "+openmp", "+opencl", "+icpx", "+hpx", "+kokkos",
     policy="any_of",
     msg="PLSSVM requires at least one backend to be enabled")

    default_sycl_target_arch=default_cuda_arch(supported_cuda_archs)[0]

    variant("hpx", default=False, description="Enable HPX support")

    variant("kokkos", default=False, description="Enable Kokkos support") # TODO: intel GPUs
    # if "none" in default_sycl_target_arch:
    #     default_sycl_target_arch=amd_arch()[0]


    # variant(
    #     "sycl_target_arch", default=default_sycl_target_arch,
    #     values=(("none", "intel", "nvidia") + CudaPackage.cuda_arch_values + ROCmPackage.amdgpu_targets),
    #     when="+dpcpp",
    #     description=("GPU target for SYCL. Can be generic with \'intel\' and \'nvidia\', or target a "
    #                  "specific GPU arch (required for AMD GPUs, optional for NVIDIA GPUs, unavaible "
    #                  "for Intel GPUs - just select intel for those)."),
    # )

    # variant(
    #     "sycl_target_arch", default=default_sycl_target_arch,
    #     values=(("none", "intel", "nvidia") + CudaPackage.cuda_arch_values + ROCmPackage.amdgpu_targets),
    #     when="+adaptivecpp",
    #     description=("GPU target for SYCL. Can be generic with \'intel\' and \'nvidia\', or target a "
    #                  "specific GPU arch (required for AMD GPUs, optional for NVIDIA GPUs, unavaible "
    #                  "for Intel GPUs - just select intel for those)."),
    # )


     # TODO: variant cpu_target

    # FIXME: Add dependencies if required.
    depends_on("cxx", type="build")

    depends_on("fmt@11.0.2")
    depends_on("cxxopts@3.2.0")
    depends_on("igor@master")
    depends_on("fast-float@6.1.1")
    depends_on("googletest@1.16.0:", when="+test")


    requires("+test", when="build_type=Coverage")
    requires("~lto", when="build_type=Coverage", msg="Coverage build requires LTO to be disabled")

    depends_on("cmake@3.23:", type="build")
    depends_on("opencl", when="+opencl")

    # depends_on("pocl", when="+opencl") # TODO fix


    depends_on("python@3:", when="+python")
    depends_on("py-pybind11@2.11.1:", when="+python")

    depends_on("doxygen@1.9.8:+graphviz", when="+documentation")

    depends_on("py-scikit-learn", when="+test_file")
    depends_on("py-scikit-learn") # TODO: check why needed
    depends_on("py-humanize")  # TODO: check why needed
    depends_on("py-humanize", when="+test_file")
    depends_on("py-numpy", when="+test_file")

    depends_on("hip", when="+hip")
    # if not "amdgpu_target=none" in self.variant:


    depends_on("cuda", when="+cuda")
    depends_on("nvhpc", when="stdparimplementation=nvhpc", type="build")
    conflicts("nvhpc@24.5", msg="nvhpc 24.5 is not supported")
    conflicts("nvhpc@24.4", msg="nvhpc 24.4 is not supported")
    conflicts("stdparimplementation=nvhpc", when="~reducing_label_types", msg="nvhpc does not support long double in GPU kernel code")
    depends_on("adaptivecpp ~stdpar", when="+adaptivecpp") # TODO fix in adaptivecpp package
    depends_on("adaptivecpp +stdpar", when="stdparimplementation=adaptivecpp")
    depends_on("intel-tbb@:2020.3", when="stdparimplementation=adaptivecpp")
    depends_on("intel-tbb@:2020.3", when="stdparimplementation=gnu-tbb")
    depends_on("intel-tbb@:2020.3", when="stdparimplementation=icpx")
    depends_on("llvm", when="+adaptivecpp")

    depends_on("intel-oneapi-compilers@2025.0.0", when="+icpx")
    depends_on("intel-oneapi-compilers@2024.2.0", when="stdparimplementation=icpx")
    conflicts("intel-oneapi-compilers@2025.0.4+nvidia", msg="Intel oneAPI compilers 2025.0.4 cuda backend seems broken")

    depends_on("intel-oneapi-tbb", when="+icpx")
    depends_on("intel-tbb@:2020.3", when="stdparimplementation=icpx")
    depends_on("intel-oneapi-dpl@:2022.3.0", when="stdparimplementation=icpx")


    depends_on("boost@1.73.0:+atomic" , when="stdparimplementation=gnu-tbb")
    depends_on("boost@1.73.0:" , when="stdparimplementation=nvhpc")
    depends_on("boost@1.73.0:" , when="stdparimplementation=roc")
    depends_on("rocthrust" , when="stdparimplementation=roc")
    depends_on("rocprim" , when="stdparimplementation=roc")

    # depends_on("    llvm@roc-stdpar+clang~gold",
    #             patches="CLANG_LLVM.patch",
    #         #    patches=[patch(
    #         #     "https://github.com/ROCm/roc-stdpar/raw/ffb6e6e7ef8ee21dcc07793540fdca9b71921ca1/data/patches/LLVM/CLANG_LLVM.patch",
    #         #    sha256="8103bc75ea7b651174f4c1aaffe292f892e130c771811e27fdf7af3fc5610c3b")],
    #            when="stdparimplementation=roc")

    depends_on("roc-stdpar", when="stdparimplementation=roc")
    # TODO: depends_on("tbb", when="stdparimplementation=gnu-tbb")
    # TODO: depends_on("rocstdpar", when="stdparimplementation=roc")





    # requires(
    #     "%gcc@9:", "%clang@17:",
    #     policy="one_of"
    #     msg="PLSSVM builds only with GCC or Clang"
    # )



    conflicts("+icpx", when="+dpcpp", msg="Intel SYCL integration conflicts DPC++ SYCL integration.")
    conflicts("build_type=Debug", when="+fast-math", msg="Fast math optimizations are not allowed in debug mode.")


    # Depend on compiler that is being used for sycl
    # This ensures that, for example, dpcpp supports the cuda backend
    # when a NVIDIA device is being used
    depends_on("dpcpp@2023-03:", when="+dpcpp ")
    depends_on("dpcpp@2023-03+openmp", when="+dpcpp")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on("dpcpp@2023-03: +openmp +cuda",
                   when="+dpcpp cuda_arch={0}".format(cuda_arch))
        depends_on("cuda", when="+opencl cuda_arch={0}".format(cuda_arch))
        depends_on("adaptivecpp+cuda", when="+adaptivecpp cuda_arch={0}".format(cuda_arch))
        depends_on("adaptivecpp@24.10.00: +stdpar +cuda", when="+stdpar stdparimplementation=adaptivecpp cuda_arch={0}".format(cuda_arch))
        depends_on("intel-oneapi-compilers+nvidia", when="+icpx cuda_arch={0}".format(cuda_arch))
        depends_on("intel-oneapi-compilers+nvidia", when="+stdpar stdparimplementation=icpx cuda_arch={0}".format(cuda_arch))
        depends_on("hip+cuda~rocm", when="+hip cuda_arch={0}".format(cuda_arch))
        depends_on("cuda", when="+hip cuda_arch={0}".format(cuda_arch))
        depends_on("kokkos+cuda+wrapper cuda_arch={0} %gcc ".format(cuda_arch), when="+kokkos cuda_arch={0}".format(cuda_arch))
        conflicts("+lto", when="+kokkos cuda_arch={0}".format(cuda_arch), msg="kokkos Backend can not be build with lto")
    for amdgpu_arch in ROCmPackage.amdgpu_targets:
        depends_on("hip+rocm", when="+hip amdgpu_target={0}".format(amdgpu_arch))
        depends_on("rocm-opencl", when="+opencl amdgpu_target={0}".format(amdgpu_arch))
        depends_on("adaptivecpp+rocm", when="+adaptivecpp amdgpu_target={0}".format(amdgpu_arch))
        depends_on("adaptivecpp@24.10.00: +stdpar +rocm", when="+stdpar stdparimplementation=adaptivecpp amdgpu_target={0}".format(amdgpu_arch))
        depends_on("intel-oneapi-compilers+amd", when="+icpx amdgpu_target={0}".format(amdgpu_arch))
        depends_on("intel-oneapi-compilers+amd", when="+icpx stdparimplementation=icpx amdgpu_target={0}".format(amdgpu_arch))
        depends_on("dpcpp@2023-03:+openmp +rocm rocm-platform=AMD",
                   when="+dpcpp amdgpu_target={0}".format(amdgpu_arch))
        depends_on("kokkos+rocm amdgpu_target={0}".format(amdgpu_arch), when="+kokkos amdgpu_target={0}".format(amdgpu_arch))



    depends_on("hpx%gcc", when="+hpx%gcc")
    depends_on("hpx%clang", when="+hpx%clang")
    depends_on("hpx@1.9.1:", when="+hpx")

    depends_on("kokkos+openmp+serial", when="+kokkos")
    depends_on("kokkos+sycl", when="+kokkos %oneapi")

    # SYCL CUDA/HIP backends require target arch informations to
    # set the correct flags later on:
    # conflicts("+dpcpp", when="sycl_target_arch=none",
    #           msg=("Additional information to select the correct sycl backend."
    #                " Use either a specific nvidia/amdgpu GPU architecture "
    #                "(useful for compiling the tests/examples), or \'nvidia\' "
    #                "\'intel\' in case a specific architecture is not targeted."))



    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix + '/install/lib/')

    def setup_build_environment(self, env):
        try:
            env.append_path('LD_LIBRARY_PATH',self.spec['intel-oneapi-compilers'].prefix + "/tbb/latest/lib/intel64/gcc4.8" )
        except KeyError:
            pass

    @property
    def build_targets(self):
        if "+documentation" in self.spec:
            return ["all","doc"]
        if "build_type=Coverage" in self.spec:
            return ["coverage"]
        return ["all"]



    def cmake_args(self):
        args = []
        args += [self.define_from_variant("PLSSVM_ENABLE_OPENMP_BACKEND", "openmp")]
        args += [self.define_from_variant("PLSSVM_ENABLE_CUDA_BACKEND", "cuda")]


        args += [self.define_from_variant("PLSSVM_ENABLE_HIP_BACKEND", "hip")]



        #args += [self.define("PLSSVM_ENABLE_TESTING", self.run_tests)]
        args += [self.define_from_variant("PLSSVM_ENABLE_TESTING", "test")]
        if "+test" in self.spec:
            args += [self.define_from_variant("PLSSVM_TEST_WITH_REDUCED_LABEL_TYPES", "reducing_label_types")]
        args += [self.define_from_variant("PLSSVM_ENABLE_ASSERTS", "asserts")]
        args += [self.define_from_variant("PLSSVM_ENABLE_LANGUAGE_BINDINGS", "python")]
        if "+python" in self.spec:
            args += [self.define("PLSSVM_PYTHON_BINDINGS_PREFERRED_LABEL_TYPE", self.spec.variants["python_preferred_label_type"].value)]
            args += [self.define_from_variant("PLSSVM_ENABLE_PYTHON_BINDINGS", "python")]

        args += [self.define_from_variant("PLSSVM_ENABLE_DOCUMENTATION", "documentation")]
        args += [self.define_from_variant("PLSSVM_ENABLE_FAST_MATH", "fast-math")]

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

        # args += [self.define_from_variant("PLSSVM_ENABLE_SYCL_BACKEND", "dpcpp")]
        if "+adaptivecpp" in self.spec or "+dpcpp" in self.spec or "+icpx" in self.spec:
            args += [self.define("PLSSVM_ENABLE_SYCL_BACKEND", "ON")]
        else:
            args += [self.define("PLSSVM_ENABLE_SYCL_BACKEND", "OFF")]


        if "+adaptivecpp" in self.spec:
            args += [self.define_from_variant("PLSSVM_ENABLE_SYCL_ADAPTIVECPP_BACKEND", "adaptivecpp")]
            args += [self.define_from_variant("PLSSVM_SYCL_BACKEND_ADAPTIVECPP_USE_GENERIC_SSCP", "adaptivecpp_SSCP")]
            args += [self.define("PLSSVM_SYCL_ADAPTIVECPP_INCLUDE_DIR", "{0}/include".format(self.spec["adaptivecpp"].prefix))]# TODO
            args += [self.define("PLSSVM_SYCL_BACKEND_PREFERRED_IMPLEMENTATION", "adaptivecpp")]

        if "+dpcpp" in self.spec or "+icpx" in self.spec:
            args += [self.define("PLSSVM_ENABLE_SYCL_DPCPP_BACKEND", "ON")]
        if "+dpcpp" in self.spec:
            args += [self.define_from_variant("PLSSVM_SYCL_BACKEND_DPCPP_ENABLE_AOT", "dpcpp_aot")]
            args += [self.define_from_variant("PLSSVM_SYCL_BACKEND_DPCPP_USE_LEVEL_ZERO", "dpcpp_level_zero")]
            args += [self.define("PLSSVM_SYCL_DPCPP_INCLUDE_DIR", "{0}/include".format(self.spec["dpcpp"].prefix))]
        if "+icpx" in self.spec:
            args += [self.define("PLSSVM_SYCL_DPCPP_INCLUDE_DIR", "{0}/include".format(self.spec["intel-oneapi-compilers"].prefix))]



        target_arch = []
        if "cuda_arch" in self.spec.variants and  not "none" in self.spec.variants["cuda_arch"].value:
            target_arch += ["nvidia:sm_" + ",sm_".join(self.spec.variants["cuda_arch"].value)]
        if "amdgpu_target" in self.spec.variants and not "none" in self.spec.variants["amdgpu_target"].value:
            target_arch += ["amd:" + ",".join(self.spec.variants["amdgpu_target"].value)]

        if "+stdpar" in self.spec:
            if not target_arch  or "gnu-tbb" in self.spec.variants["stdparimplementation"].value:
                args += [self.define("PLSSVM_STDPAR_TARGET_PLATFORMS", "cpu")]
            else:
                args += [self.define("PLSSVM_STDPAR_TARGET_PLATFORMS", ";".join(target_arch))]
        if "+opencl" in self.spec:
            args += [self.define("PLSSVM_OPENCL_TARGET_PLATFORMS", ";".join(target_arch))] # TODO: add cpu if pocl is working

        target_arch += ["cpu"]

        if "+openmp" in self.spec:
            args += [self.define("PLSSVM_OPENMP_TARGET_PLATFORMS", "cpu")]

        if "+cuda" in self.spec:
            args += [self.define("PLSSVM_CUDA_TARGET_PLATFORMS", ["nvidia:sm_" + ",sm_".join(self.spec.variants["cuda_arch"].value)])]
        if "+hip" in self.spec:
            if not "none" in self.spec.variants["cuda_arch"].value:
                args += [self.define("PLSSVM_HIP_TARGET_PLATFORMS", ["nvidia:sm_" + ",sm_".join(self.spec.variants["cuda_arch"].value)])]
            if not "none" in  self.spec.variants["amdgpu_target"].value:
                args += [self.define("PLSSVM_HIP_TARGET_PLATFORMS", ["amd:" + ",".join(self.spec.variants["amdgpu_target"].value)])]
        if "+kokkos" in self.spec:
            if not "none" in self.spec.variants["cuda_arch"].value:
                args += [self.define("PLSSVM_KOKKOS_TARGET_PLATFORMS", ["nvidia:sm_" + ",sm_".join(self.spec.variants["cuda_arch"].value)])]
            if not "none" in  self.spec.variants["amdgpu_target"].value:
                args += [self.define("PLSSVM_KOKKOS_TARGET_PLATFORMS", ["amd:" + ",".join(self.spec.variants["amdgpu_target"].value)])]
        if "+icpx" in self.spec:
            # Set compiler to icpx
            args += [self.define("CMAKE_CXX_COMPILER", "{0}/compiler/latest/bin/icpx".format(self.spec["intel-oneapi-compilers"].prefix))]
            # args += [self.define("PLSSVM_SYCL_TARGET_PLATFORMS", "cpu:avx512" +";".join(target_arch))]
            if "cpu" in target_arch:
                target_arch.remove("cpu")
            if "+cuda" in self.spec:
                args += [self.define("CUDA_HOST_COMPILER", "icpx"), self.define("OpenMP_CXX_FLAGS", "-fopenmp"), self.define("OpenMP_CXX_LIB_NAMES", "libiomp5"), self.define("OpenMP_libiomp5_LIBRARY", "{0}/compiler/latest/lib/libiomp5.so".format(self.spec["intel-oneapi-compilers"].prefix))]
            args += [self.define("PLSSVM_SYCL_TARGET_PLATFORMS", ";".join(target_arch))]

        if "+dpcpp" in self.spec:
            # Set compiler to dpcpp
            args += [self.define("CMAKE_CXX_COMPILER",
                                 "{0}/bin/clang++".format(self.spec["dpcpp"].prefix))]
            if "cpu" in target_arch:
                target_arch.remove("cpu")

        if "+adaptivecpp" in self.spec:
            args += [self.define("PLSSVM_SYCL_TARGET_PLATFORMS", ";".join(target_arch))]


        if "+hpx" in self.spec:
            args += [self.define("PLSSVM_HPX_TARGET_PLATFORMS", "cpu")]




        if "+dpcpp" in self.spec:
            # Set compiler to dpcpp
            args += [self.define("CMAKE_CXX_COMPILER",
                                 "{0}/bin/clang++".format(self.spec["dpcpp"].prefix))]


        # args += [self.define("PLSSVM_TARGET_PLATFORMS", "cpu;nvidia:sm_80")]

        args += [self.define_from_variant("PLSSVM_ENABLE_STDPAR_BACKEND", "stdpar")]

        stdpar_keys = {
            "adaptivecpp": "ACPP",
            "icpx": "IntelLLVM",
            "gnu-tbb": "GNU_TBB",
            "nvhpc": "NVHPC",
            "roc": "roc-stdpar"
        }



        if "+stdpar" in self.spec:
            args += [self.define("PLSSVM_STDPAR_BACKEND_IMPLEMENTATION", stdpar_keys[self.spec.variants["stdparimplementation"].value])]

            if "stdparimplementation=adaptivecpp" in self.spec:
                args += [self.define("CMAKE_CXX_COMPILER", "{0}/bin/acpp".format(self.spec["adaptivecpp"].prefix))]
            if "stdparimplementation=icpx" in self.spec:
                args += [self.define("CMAKE_CXX_COMPILER", "{0}/compiler/latest/bin/icpx".format(self.spec["intel-oneapi-compilers"].prefix))]
            if "stdparimplementation=nvhpc" in self.spec:
                args += [self.define("CMAKE_CXX_COMPILER", "{0}/Linux_x86_64/{1}/compilers/bin/nvc++".format(self.spec["nvhpc"].prefix, self.spec["nvhpc"].version ))] # FIXME: other targets than Linux_x86_64

            if "stdparimplementation=roc" in self.spec:
                args += [self.define("CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(self.spec["llvm"].prefix))] # FIXME: ROC-stdpar package
                args += [self.define("PLSSVM_STDPAR_BACKEND_HIPSTDPAR_PATH", "{0}/include".format(self.spec["roc-stdpar"].prefix))]

            if "stdparimplementation=gnu-tbb" in self.spec:
                requires("%gcc", msg="GNU TBB backend requires GCC")
                args += [self.define("TBB_ROOT", "{0}".format(self.spec["intel-tbb"].prefix))]

        args += [self.define_from_variant("PLSSVM_ENABLE_HPX_BACKEND", "hpx")]
        args += [self.define_from_variant("PLSSVM_ENABLE_KOKKOS_BACKEND", "kokkos")]


        return args

