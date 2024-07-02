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
#     spack install oneapi-plugin-amd
#
# You can edit this file again by typing:
#
#     spack edit oneapi-plugin-amd
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *



class OneapiPluginAmd(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://developer.codeplay.com/products/oneapi/amd/home/"


    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

    def url_for_version(self, version):
        url = "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=amd&version={0}&filters[]={1}&filters[]=linux"
        return url.format(version.up_to(3), str(version).split("-")[1])
        # return url.format("2024.1.0", "5.4.3")

    version("2024.1.0.5.4.3", sha256="b045a6c108d4699a3bb2a6e487e85d393decd6334e93bbb715cb770617287119", expand=False)
    # version("2024.1.0-4.5.2", )
    version("2024.0.2-5.4.3", sha256="3608fdf41161257b3230bfa62b0c207b8c5ee5784f1ef3744a4ec9ce80eabf52", expand=False)
    # version("2024.0.2-4.5.2", )
    # version("2024.0.1-5.4.3", )
    # version("2024.0.1-4.5.2", )

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    depends_on("intel-oneapi-compilers@2024.1.0", when="@2024.1.0")
    depends_on("intel-oneapi-compilers@2024.0.2", when="@2024.0.2")
    # depends_on("intel-oneapi-compilers@2024.0.1", when="@2024.0.1")

    depends_on("hip@5.4.3")
    # depends_on("hip@5.4.3", when="@2024.0.2-5.4.3")
    # depends_on("hip@5.4.3", when="@2024.0.1-5.4.3")

    # depends_on("hip@4.5.2", when="@2024.1.0-4.5.2")
    # depends_on("hip@4.5.2", when="@2024.0.2-4.5.2")
    # depends_on("hip@4.5.2", when="@2024.0.1-4.5.2")
    # depends_on("cmake")
    phases = ["inst"]

    def inst(self, spec, prefix):
        # FIXME: Unknown build

        # install_script= EXECUTABLE("./download?product=oneapi&variant=amd&version=2024.1.0&filters[]=5.4.3&filters[]=linux")
        # exe = "./download?product=oneapi&variant=amd&version={0}&filters[]={1}&filters[]=linux".format(self.version.up_to(3), str(self.version).split("-")[1])
        exe = "./download?product=oneapi&variant=amd&version={0}&filters[]={1}&filters[]=linux".format(self.version.up_to(3), str(self.version).split("-")[1])
        Executable("chmod")("+x",exe)
        install_script= Executable(exe)
        # install_script("-y","-i","{0}".format(self.spec["intel-oneapi-compilers"].prefix),ignore_quotes=True)
