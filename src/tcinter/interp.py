# Claudio Perez
import os
import sys
import pathlib

import tcinter as tkinter


def TclInterpreter(verbose=False, tcl_lib=None, init='puts ""'):
    interp = tkinter.Tcl() # (init=init)
    return interp

def eval(script: str):
    interp = TclInterpreter()
    interp.eval(f"""

    {script}

    """)
    return interp



