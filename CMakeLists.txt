cmake_minimum_required(VERSION 3.24)
project(tcinter)

add_library(tcinter SHARED)
target_sources(tcinter PRIVATE _tkinter.c)

set_target_properties(
    tcinter
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_tcinter"
        LINKER_LANGUAGE C
    )

find_package(TCL REQUIRED)
find_package(Python REQUIRED COMPONENTS Interpreter Development)

message("Python : ${Python_INCLUDE_DIRS}")
message("Tcl:     ${TCL_INCLUDE_PATH}")

target_include_directories(tcinter PRIVATE ${TCL_INCLUDE_PATH} ${Python_INCLUDE_DIRS})
target_link_libraries(tcinter PRIVATE ${TK_LIBRARY} ${TCL_LIBRARY} ${Python_LIBRARIES})

