#Define sources
set(CLI_SOURCES CLIParser.cpp)

#Create static library
add_library(cli STATIC ${CLI_SOURCES})

#Specify public library
target_include_directories(cli PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

#Link cli and utils library
target_link_libraries(cli PRIVATE utils)