#define sources
set(AST_SOURCES ast.cpp)

#Create static library
add_library(ast STATIC ${AST_SOURCES})

target_include_directories(ast PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(ast PRIVATE utils)