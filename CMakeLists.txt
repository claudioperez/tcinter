cmake_minimum_required(VERSION 3.20)

project(tcinter)

find_package(TCL REQUIRED)

find_package(Python COMPONENTS Interpreter Development)

add_library(tcinter SHARED)
target_link_libraries(tcinter PRIVATE 
  tcl::tcl 
# ${TCL_LIBRARY} 
  ${Python_LIBRARIES}
)

target_sources(tcinter PRIVATE _tkinter.c _tkinter.c.h tkinter.h)
set_target_properties(
    tcinter
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_tcinter"
        LINKER_LANGUAGE C
    )

target_include_directories(tcinter PRIVATE 
# tcl::tcl 
# ${TCL_LIBRARY} 
# ${TCL_INCLUDE_PATH} 
  ${Python_INCLUDE_DIRS}
)

install(TARGETS tcinter LIBRARY DESTINATION .)

