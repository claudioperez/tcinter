import os
import sys
import pathlib
try:
    import tkinter
except:
    import tcinter as tkinter


def TclInterpreter(verbose=False, tcl_lib=None):
    interp = tkinter.Tcl()
    return interp

def eval(script: str):
    interp = TclInterpreter()
    interp.eval(f"""

    {script}

    """)
    return interp


class TclRuntime:
    def __init__(self,  model=None, verbose=False):
        from functools import partial
        self._partial = partial
        self._c_domain = None
        self._c_rt = None
        self._interp = TclInterpreter(verbose=verbose)
        if model is not None:
            self.send(model)
    
    def model(self, ndm, ndf, **kwds):
        self.eval(f"model basic -ndm {ndm} -ndf {ndf}")


    def send(self, obj, ndm=2, ndf=3, **kwds):
        self.model(ndm=ndm, ndf=ndf)

        m = dumps(obj)

        if isinstance(m, str):
            try:
                self.eval(m)
            except Exception as e:
                print(e, file=sys.stderr)
        else:
            self.eval(m.getIndex())
            from . import OpenSeesPyRT as libOpenSeesRT
            _builder = libOpenSeesRT.get_builder(self._interp.interpaddr())
            for ident,obj in m.python_objects.items():
                tag = self.eval(f"set {ident.tclstr()}")
                _builder.addPythonObject(tag, obj)

            self.eval(m.getScript())

    @property
    def _rt(self):
        if self._c_rt is None:
            from . import OpenSeesPyRT as libOpenSeesRT
            self._c_rt = libOpenSeesRT.getRuntime(self._interp.tk.interpaddr())
        return self._c_rt

    @property
    def _domain(self):
        if self._c_domain is None:
            from . import OpenSeesPyRT as libOpenSeesRT
            self._c_domain = libOpenSeesRT.get_domain(self._rt)
        return self._c_domain

    def getNodeResponse(self, node, typ):
        return np.array(self._domain.getNodeResponse(node, typ))

    def getTime(self):
        return self._domain.getTime()

    time = getTime


    @classmethod
    def _as_tcl_arg(cls, arg):
        if isinstance(arg, list):
            return f"{{{''.join(TclRuntime._as_tcl_arg(a) for a in arg)}}}"
        elif isinstance(arg, dict):
            return "{\n" + "\n".join([
              f"{cmd} " + " ".join(TclRuntime._as_tcl_arg(a) for a in val)
                  for cmd, val in kwds
        ]) + "}"
        else:
            return str(arg)

    def _tcl_call(self, arg, *args, **kwds):
        tcl_args = [TclRuntime._as_tcl_arg(arg) for arg in args]
        tcl_args += [
          f"-{key} " + TclRuntime._as_tcl_arg(val)
              for key, val in kwds.items()
        ]
        ret = self._interp.tk.eval(
            f"{arg} " + " ".join(tcl_args))
        return ret if ret != "" else None

    def eval(self, string):
        try:
            return self._interp.tk.eval(string)
        except tkinter._tkinter.TclError as e:
            self._interp.tk.eval("puts $errorInfo;")
            raise e

    def __getattr__(self, attr):
        return self._partial(self._tcl_call, attr)

