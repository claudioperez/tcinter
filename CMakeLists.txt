cmake_minimum_required(VERSION 3.20)

project(tcinter)

find_package(TCL REQUIRED)

find_package(Python COMPONENTS Interpreter Development)

add_library(tcinter SHARED)
target_link_libraries(tcinter PRIVATE 
  tcl::tcl 
  ${Python_LIBRARIES}
)

target_sources(tcinter PRIVATE _tkinter.c _tkinter.c.h tkinter.h)
target_include_directories(tcinter PRIVATE ${Python_INCLUDE_DIRS})

set_target_properties(
    tcinter
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_tcinter"
        LINKER_LANGUAGE C
    )

if (WIN32)
  set_target_properties(tcinter PROPERTIES SUFFIX ".pyd")
  install(TARGETS tcinter RUNTIME DESTINATION .)
else()
  set_target_properties(tcinter PROPERTIES SUFFIX ".so")
  install(TARGETS tcinter LIBRARY DESTINATION .)
endif()



