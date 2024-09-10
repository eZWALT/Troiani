cmake_minimum_required(VERSION 3.20)
project(Troiani 1.0)

### Set env variables for compilation
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_subdirectory(src)
add_subdirectory(tests)
add_subdirectory(examples)

include_directories(include)

### Set output directory 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

### Set installation rules and default install path
# Troiani exec
set(CMAKE_INSTALL_PREFIX /usr/local)
install(TARGETS Troiani DESTINATION bin)
# Custom libs
# install(TARGETS mylib DESTINATION lib)
# Headers
install(DIRECTORY include/ DESTINATION include)

# Find and include ANTLR & LLVM dependencies
#find_package(LLVM REQUIRED CONFIG)
#include_directories(${LLVM_INCLUDE_DIRS})
#link_directories(${LLVM_LIBRARY_DIRS})

#find_package(ANTLR REQUIRED)
#include_directories(${ANTLR_INCLUDE_DIR})


