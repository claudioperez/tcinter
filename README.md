

Info about original Tkinter license: https://web.archive.org/web/20170430142250/http://tkinter.unpythonic.net/wiki/Tkinter


```bash
conan install . --build=missing
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=generators\conan_toolchain.cmake
cmake --build . --config Release
