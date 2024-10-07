#!/usr/bin/env python
import sys
from pathlib import Path
from glob import glob
from os.path import basename, splitext

import amoeba
import setuptools
import distutils.sysconfig as sysconfig

class Tcinter(amoeba.BuildExtension):
    def build_extension(self, ext):
        # Ensure Conan runs
        self.run_conan()
#       toolchain = str(Path(".").absolute()/f"{self.build_temp}_{ext.name}"/"generators"/"conan_toolchain.cmake")
        toolchain = str(Path(".").absolute()/"build"/"generators"/"conan_toolchain.cmake")
        ext.cmake_configure_options.append(
                f"-DCMAKE_TOOLCHAIN_FILE={toolchain}"
        )

        super().build_extension(ext)

    def run_conan(self):
        import subprocess
        subprocess.run([
            "conan", "install", ".",
            "--build=missing",
#           "--output-folder", self.build_temp
        ])


if __name__ == "__main__":
    setuptools.setup(
        cmdclass = {"build_ext": Tcinter},
        ext_modules = [
            amoeba.CMakeExtension(
                name = "rt",
                install_prefix="tcinter",
                cmake_configure_options = [
                    f"-DPython_EXECUTABLE:FILEPATH={sys.executable}",
                    f"-DPython_ROOT_DIR:FILEPATH={sys.base_prefix}",
                    f"-DPython_INCLUDE_DIR:FILEPATH={sysconfig.get_python_inc()}",
                    f"-DPython_LIBRARY:FILEPATH={sysconfig.get_config_var('LIBDIR')}"
                ],
            )
        ]
    )

