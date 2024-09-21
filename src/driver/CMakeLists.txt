#Define the sources
set(DRIVER_SOURCES main.cpp)

#Create an executable 
add_executable(troiani ${DRIVER_SOURCES})

#Link against cli/utils
target_link_libraries(troiani PRIVATE cli utils preprocessing)