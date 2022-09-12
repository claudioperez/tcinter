#!/usr/bin/env python3

import sys
import cmd
import tcinter._tcinter as _tkinter

__version__="0.0.0"

import tcinter.interp as interp

HELP = """\
usage: opensees <file> [args]...
"""

#PROMPT = "\033\\[01;32mopensees\033\\[0m > "
PROMPT = "\u001b[35mtcl\u001b[0m > "

# Path to Tcl script which loads commands
INIT_TCL = ""

def parse_args(args):
    opts = {"subproc": False, "verbose": False}
    files = []
    argi = iter(args[1:])
    for arg in argi:
        if arg[0] == "-":
            if arg == "-":
                files.append("-")
            if arg == "-h" or arg == "--help":
                print(HELP)
                sys.exit()
            elif arg == "--version":
                print(__version__)
                sys.exit()
        else:
            files.append(arg)
            break
    return files, opts, argi


from cmd import Cmd
import subprocess, queue, time, random
from threading import Thread

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class TclShell(cmd.Cmd):
    intro = """         
    TcInter - A Python wrapper for Tcl without Tk
"""
    prompt = PROMPT
    file = None
    def __init__(self, *args, **kwds):
        self.tcl_interp = interp.TclInterpreter()
        super().__init__(*args, **kwds)

    def do_exit(self, arg):
        return True

    def default(self, arg):
        try:
            value = self.tcl_interp.eval(arg)
            if value:
                print(value)
            return None
        #except _tkinter.TclError as e:
        except Exception as e:
            print(e)

    def precmd(self, line):
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def completedefault(self, text, line, begidx, endidx):
        print(text,line,begidx,endidx)
        return ["hi"]

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

if __name__ == "__main__":

    files, opts, argi = parse_args(sys.argv)
    if len(sys.argv) == 1:
        TclShell().cmdloop()
    else:
        import time
        tcl = interp.TclRuntime(verbose=opts["verbose"])
        tcl.eval(f"set argc {len(sys.argv) - 2}")
        tcl.eval(f"set argv {{{' '.join(argi)}}}")
        for filename in files:
            if filename == "-":
                tcl.eval(sys.stdin.read())
            else:
                try:
                    tcl.eval(open(filename).read())
                except:
                    pass
                #time.sleep(3)


