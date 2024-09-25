#ifndef TOKEN_H
#define TOKEN_H

#include <string>

Class TokenType {
private:

public:
    TokenType();

};

Class Token {
private:
    TokenType type;
    std::string content;
public:
    Token();
};

#endif