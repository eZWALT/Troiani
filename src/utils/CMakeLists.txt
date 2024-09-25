#Define the sources
set(UTILS_SOURCES Config.cpp Error.cpp SourceFile.cpp)

#Create static library
add_library(utils STATIC ${UTILS_SOURCES})

#Make the utils headers public
target_include_directories(utils PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
