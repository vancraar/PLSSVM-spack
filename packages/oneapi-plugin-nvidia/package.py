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



class OneapiPluginNvidia(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://developer.codeplay.com/products/oneapi/nvidia/home/"


    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("vancraar")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("https://intel.ly/393CijO", checked_by="github_user1")

    def url_for_version(self, version):
        url = "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=nvidia&version={0}&filters[]={1}&filters[]=linux"
        return url.format(version.up_to(3), str(version).split("-")[1])

    version("2024.5.0-12.0", sha256="264a43d2e07c08eb31d6483fb1c289a6b148709e48e9a250efc1b1e9a527feb6",expand=False)
    version("2024.2.0-12.0", sha256="0622df0054364b01e91e7ed72a33cb3281e281db5b0e86579f516b1cc5336b0f",expand=False)
    version("2024.1.2-12.0", sha256="5a0d1e5eeee5713b6f7c259ef87c044ab4e1bf7bb0b4651da9cde81fd16e43bc",expand=False)
    version("2024.1.0-12.0", sha256="36560ed0f2af951241d7551134b52902efd13abb249922e661dd0913f098ceca",expand=False)
    version("2024.0.2-12.0", sha256="ccc173e1c7eced6793aa81bfdf12608eed1e83c077e48485b0e770688451bc8e",expand=False)
    version("2024.0.1-12.0", )


    depends_on("intel-oneapi-compilers@2025.0.0", when="@2025.0.0")
    depends_on("intel-oneapi-compilers@2024.2.0", when="@2024.2.0")
    depends_on("intel-oneapi-compilers@2024.1.2", when="@2024.1.2")
    depends_on("intel-oneapi-compilers@2024.1.0", when="@2024.1.0")
    depends_on("intel-oneapi-compilers@2024.0.2", when="@2024.0.2")
    depends_on("intel-oneapi-compilers@2024.0.1", when="@2024.0.1")

    depends_on("cuda@12.0", when="@2024.5.0-12.0")
    depends_on("cuda@12.0", when="@2024.2.0-12.0")
    depends_on("cuda@12.0", when="@2024.1.2-12.0")
    depends_on("cuda@12.0", when="@2024.1.0-12.0")
    depends_on("cuda@12.0", when="@2024.0.2-12.0")
    depends_on("cuda@12.0", when="@2024.0.1-12.0")

    phases = ["inst"]

    # extends("intel-oneapi-compilers")

    def inst(self, spec, prefix):
        # FIXME: Unknown build

        # install_script= EXECUTABLE("./download?product=oneapi&variant=amd&version=2024.1.0&filters[]=5.4.3&filters[]=linux")
        exe = "./download?product=oneapi&variant=nvidia&version={0}&filters[]={1}&filters[]=linux".format(self.version.up_to(3), str(self.version).split("-")[1])
        Executable("chmod")("+x",exe)
        install_script= Executable(exe)
        install_script("-y","-i","{0}".format(self.spec["intel-oneapi-compilers"].prefix),ignore_quotes=True)
