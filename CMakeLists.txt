#Declaration
cmake_minimum_required(VERSION 3.20)
project(Troiani)

# Set env variables for compilation
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the main tree directory structure
add_subdirectory(src)           #Main source code
add_subdirectory(tests)         #Testing 
add_subdirectory(examples)      #Example programs

# Set output directory 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Set installation rules and default install path
set(CMAKE_INSTALL_PREFIX /usr/local)
install(TARGETS troiani DESTINATION bin)
