#Define sources
set(PREPROCESSING_SOURCES Preprocessor.cpp)

#Create static library
add_library(preprocessing STATIC ${PREPROCESSING_SOURCES})

#Specify the PREPROCESSING include dir
target_include_directories(preprocessing PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(preprocessing PRIVATE utils)
