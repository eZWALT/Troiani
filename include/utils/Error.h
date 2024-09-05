#ifndef ERROR_H
#define ERROR_H 

#include <string>
#include <iostream>

class ErrorType {
public:
    enum class CLI {
        InvalidArgument, 
        MissingArgument,
    };

    enum class Preprocessing {
        FileNotFound,
        IncludeCycle,
        InvalidDirective,
    };

    enum class Syntax {
        InvalidSyntax,
    };

    enum class Semantic {
        TypeMismatch,
        UndeclaredVariable,
    };

    enum class CodeGeneration {
        InvalidInstruction,
    };

    enum class Optimization {
        OptimizationFailure,
    };

    enum class Linking {
        UndefinedReference,
        MultipleDefinition,
    };

    enum class Runtime {
        DivisionByZero,
        NullPointerDereference,
        StackOverflow,
        OutOfMemory,
    };

    static std::string to_string(CLI err_ty);
    static std::string to_string(Preprocessing err_ty);
    static std::string to_string(Syntax err_ty);
    static std::string to_string(Semantic err_ty);
    static std::string to_string(CodeGeneration err_ty);
    static std::string to_string(Optimization err_ty);
    static std::string to_string(Linking err_ty);
    static std::string to_string(Runtime err_ty);
};


class Error {
private:
    ErrorType type;
    std::string msg;


public:
    Error(ErrorType type, const std::string& msg);
    ~Error();

    std::string to_string() const;

    void log() const;

};

#endif 