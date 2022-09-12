cmake_minimum_required(VERSION 3.21)

project(tcinter)

add_library(tcinter SHARED)
target_sources(tcinter PRIVATE _tkinter.c _tkinter.c.h tkinter.h)

set_target_properties(
    tcinter
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_tcinter"
        LINKER_LANGUAGE C
    )

find_package(TCL)
find_package(Python COMPONENTS Interpreter Development)

message("Python : ${Python_INCLUDE_DIRS}")
message("Tcl:     ${TCL_TCLSH}")

target_include_directories(tcinter PRIVATE ${TCL_INCLUDE_PATH} ${Python_INCLUDE_DIRS})
target_link_libraries(tcinter PRIVATE 
  ${TCL_LIBRARY} 
  ${Python_LIBRARIES})

install(TARGETS tcinter LIBRARY DESTINATION .)
