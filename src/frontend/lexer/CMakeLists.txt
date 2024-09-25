#Define sources 
set(LEXER_SOURCES lexer.cpp)

#Create a static library 
add_library(lexer STATIC ${LEXER_SOURCES})

#Specify the lexer include dir 
target_include_directories(lexer PUBLIC ${CMAKE_CURRENTS_SOURCE_DIR})

target_link_libraries(lexer PRIVATE utils)