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
#     spack install roc-stdpar
#
# You can edit this file again by typing:
#
#     spack edit roc-stdpar
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class RocStdpar(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    git = "https://github.com/ROCm/roc-stdpar.git"


    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar", "breyerml")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("MIT", checked_by="vancrar")

    # FIXME: Add proper versions here.
    version("main", branch="main")

    # FIXME: Add dependencies if required.
    depends_on("intel-tbb@:2020.3")


    depends_on("llvm@roc-stdpar+clang~gold",
                patches="CLANG_LLVM.patch",)

    patch("include.patch")

    # def install(self, spec, prefix):
    #     # FIXME: Unknown build system
    #     make()
    #     make("install")

    def cmake_args(self):
        args = []

        args += [self.define("CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(self.spec["llvm"].prefix))]

        return args