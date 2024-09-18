cmake_minimum_required(VERSION 3.20)

project(tcinter)


if(WIN32)
  list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
  list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})
  
  if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/0.18.1/conan.cmake"
                  "${CMAKE_BINARY_DIR}/conan.cmake"
                  TLS_VERIFY ON)
  endif()
  
  include(${CMAKE_BINARY_DIR}/conan.cmake)

# conan_cmake_configure(REQUIRES tcl/8.6.11
#                       GENERATORS cmake ) # cmake_find_package)

  conan_cmake_autodetect(settings)

  conan_cmake_install(PATH_OR_REFERENCE ${CMAKE_SOURCE_DIR}
                      BUILD missing
                      REMOTE conancenter
                      SETTINGS ${settings})


  # Load Conan build info
  include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  conan_basic_setup()


  set(TCL_INCLUDE_DIRS "${CONAN_INCLUDE_DIRS_TCL}")
  set(TCL_INCLUDE_PATH "${CONAN_INCLUDE_DIRS_TCL}")
  set(TCL_LIBRARIES    "${CONAN_PKG_LIBS_TCL}")
  set(TCL_LIBRARY      "${CONAN_PKG_LIBS_TCL}")

else()
  find_package(TCL)
endif()

find_package(Python COMPONENTS Interpreter Development)

add_library(tcinter SHARED)
target_sources(tcinter PRIVATE _tkinter.c _tkinter.c.h tkinter.h)
set_target_properties(
    tcinter
    PROPERTIES
        PREFIX ""
        OUTPUT_NAME "_tcinter"
        LINKER_LANGUAGE C
    )

target_include_directories(tcinter PRIVATE 
  ${TCL_INCLUDE_PATH} 
  ${Python_INCLUDE_DIRS}
)
target_link_libraries(tcinter PRIVATE 
  ${TCL_LIBRARY} 
  ${Python_LIBRARIES}
)

install(TARGETS tcinter LIBRARY DESTINATION .)
