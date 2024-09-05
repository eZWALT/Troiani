cmake_minimum_required(VERSION 3.20)
project(Troiani)

# Set env variables for compilation
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set output directory 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Set compiler flags?

# Find and include ANTLR & LLVM dependencies
find_package(LLVM REQUIRED CONFIG)
include_directories(${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIRS})

find_package(ANTLR REQUIRED)
include_directories(${ANTLR_INCLUDE_DIR})

# Add source files
file(GLOB SOURCES "src/**/*.cpp")
file(GLOB HEADERS "include/**/*.h")

# Add final executable 
add_executable(Troiani ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(Troiani ${LLVM_LIBRARIES} ${ANTLR_LIBRARIES})

