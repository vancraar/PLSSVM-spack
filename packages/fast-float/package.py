
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
#     spack install fast-float
#
# You can edit this file again by typing:
#
#     spack edit fast-float
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class FastFloat(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    git = "https://github.com/fastfloat/fast_float.git"


    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar", "breyerml")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("MIT")

    # FIXME: Add proper versions and checksums here.
    version("0.1.0", tag="v0.1.0")
    version("0.2.0", tag="v0.2.0")
    version("0.3.0", tag="v0.3.0")
    version("0.4.0", tag="v0.4.0")
    version("0.5.0", tag="v0.5.0")
    version("0.6.0", tag="v0.6.0")
    version("0.7.0", tag="v0.7.0")
    version("0.8.0", tag="v0.8.0")
    version("0.9.0", tag="v0.9.0")
    version("1.0.0", tag="v1.0.0")
    version("1.1.0", tag="v1.1.0")
    version("1.1.1", tag="v1.1.1")
    version("1.1.2", tag="v1.1.2")
    version("2.0.0", tag="v2.0.0")
    version("3.0.0", tag="v3.0.0")
    version("3.1.0", tag="v3.1.0")
    version("3.2.0", tag="v3.2.0")
    version("3.4.0", tag="v3.4.0")
    version("3.5.0", tag="v3.5.0")
    version("3.5.1", tag="v3.5.1")
    version("3.6.0", tag="v3.6.0")
    version("3.7.0", tag="v3.7.0")
    version("3.8.0", tag="v3.8.0")
    version("3.8.1", tag="v3.8.1")
    version("3.8.2", tag="v3.8.2")
    version("3.9.0", tag="v3.9.0")
    version("3.10.0", tag="v3.10.0")
    version("3.10.1", tag="v3.10.1")
    version("3.11.0", tag="v3.11.0")
    version("4.0.0", tag="v4.0.0")
    version("5.0.0", tag="v5.0.0")
    version("5.1.0", tag="v5.1.0")
    version("5.2.0", tag="v5.2.0")
    version("5.3.0", tag="v5.3.0")
    version("6.0.0", tag="v6.0.0")
    version("6.1.0", tag="v6.1.0")


    variant("test", default=False, description="Build additional tests")
    variant("sanitize", default=False, description="Enable address sanitizer support")


    # FIXME: Add dependencies if required.
    depends_on("cmake@3.11.0:", type="build")

    def cmake_args(self):
        args = []
        args += [self.define_from_variant("FASTFLOAT_TEST", "test")]
        args += [self.define_from_variant("FASTFLOAT_SANITIZE", "sanitize")]

        return args


