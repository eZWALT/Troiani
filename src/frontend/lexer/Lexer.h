#ifndef LEXER_H
#define LEXER_H 

#include <unordered_map>
#include <string>
#include <regex>

#include "Error.h"
#include "Token.h"


Class Lexer {
private:
    std::string input;
    unsigned int position;
    unsigned int line;
    unsigned int column;

public:
    Lexer();
};
#endif 