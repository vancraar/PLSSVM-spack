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
#     spack install igor
#
# You can edit this file again by typing:
#
#     spack edit igor
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Igor(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    git = "https://github.com/bluescarni/igor.git"
    homepage = "https://github.com/bluescarni/igor"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar", "breyerml")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list.
    license("MIT")

    # FIXME: Add proper versions and checksums here.
    version("master", branch="master")

    variant("test", default=False, description="Build additional tests")

    # FIXME: Add dependencies if required.
    depends_on("cmake@3.8.0:", type="build")


    def cmake_args(self):
        args = []
        args += [self.define_from_variant("IGOR_BUILD_TESTS", "test")]
        return args






