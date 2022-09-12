#!/usr/bin/env python
import sys
from glob import glob
from os.path import basename, splitext

import amoeba
import setuptools
import distutils.sysconfig as sysconfig


if __name__ == "__main__":
    setuptools.setup(
        cmdclass = {"build_ext": amoeba.BuildExtension},
        ext_modules = [
            amoeba.CMakeExtension(
                name = "rt",
                install_prefix="tcinter",
                cmake_configure_options = [
                    "-G", "Unix Makefiles",
                    f"-DPython_EXECUTABLE:FILEPATH={sys.executable}",
                    f"-DPython_ROOT_DIR:FILEPATH={sys.base_prefix}",
                    f"-DPython_INCLUDE_DIR:FILEPATH={sysconfig.get_python_inc()}",
                    f"-DPython_LIBRARY:FILEPATH={sysconfig.get_config_var('LIBDIR')}"
                ],
            )
        ]
    )

