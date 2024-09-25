#Define the sources
set(SEMANTIC_SOURCES Scope.cpp Semantic.cpp Symbols.cpp Types.cpp)

#Create a static library 
add_library(semantic STATIC ${SEMANTIC_SOURCES})

target_include_directories(semantic PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(lexer PRIVATE utils)