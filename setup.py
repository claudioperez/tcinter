#!/usr/bin/env python
import sys
from glob import glob
from os.path import basename, splitext

import amoeba
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        cmdclass = {"build_ext": amoeba.BuildExtension},
        ext_modules = [
            amoeba.CMakeExtension(
                name = "rt",
                install_prefix="opensees",
                cmake_configure_options = [
                    "-G", "Unix Makefiles",
                    f"-DPYTHON_EXECUTABLE:FILEPATH={sys.executable}"
                ],
            )
        ]
    )

