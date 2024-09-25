#Define the sources
set(PARSER_SOURCES Parser.cpp)

#Create a static library
add_library(parser STATIC ${PARSER_SOURCES})


target_include_directories(parser PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(lexer PRIVATE utils)