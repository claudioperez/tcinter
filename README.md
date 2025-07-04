# `tcinter`

The purpose of this package is to provide an interface to Tcl like that provided by the Python standard module `tkinter`,
on installations where `tkinter` is not included. Features from Tk are not supported. 

Info about original Tkinter license: https://web.archive.org/web/20170430142250/http://tkinter.unpythonic.net/wiki/Tkinter


```bash
conan install . --build=missing
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake
cmake --build . --config Release
```
