#ifndef FRONTEND_H 
#define FRONTEND_H 

#include <string>

#include "Error.h"
#include "Lexer.h"
#include "Ast.h" 
#include "Parser.h"
#include "Semantic.h"

Class FrontEnd {
private:
    Lexer lexer;
    Parser parser;
    Semantic semantic;
public:


};

#endif