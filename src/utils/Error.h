//===----- Error.h Provides a functional-like Error -----===/
//
// This class provides an interface for error handling and a classification
// of the plausible set of errors (ErrorType). Thus errors can be 
// treated such as in other functional languages such as Haskell / Rust.
// If a function cannot return an error, then it shouldn't raise 
// any kind of error.
//
//===----------------------------------------------------===/

#ifndef ERROR_H
#define ERROR_H 

#include <string>
#include <iostream>
#include <variant>


class ErrorType {
public:
    enum class CLI {
        InvalidArgument, 
        MissingArgument,
        NonExistentFlag,
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

    enum class Configuration {
        NonExistentValue,
    };

    static std::string to_string(CLI err_ty);
    static std::string to_string(Preprocessing err_ty);
    static std::string to_string(Syntax err_ty);
    static std::string to_string(Semantic err_ty);
    static std::string to_string(CodeGeneration err_ty);
    static std::string to_string(Optimization err_ty);
    static std::string to_string(Linking err_ty);
    static std::string to_string(Runtime err_ty);
    static std::string to_string(Configuration err_ty);
};

class Error {
public:
    using ErrorVariant = std::variant<
        ErrorType::CLI,
        ErrorType::Preprocessing,
        ErrorType::Syntax,
        ErrorType::Semantic,
        ErrorType::CodeGeneration,
        ErrorType::Optimization,
        ErrorType::Linking,
        ErrorType::Runtime,
        ErrorType::Configuration
    >;

private:
    ErrorVariant error_type;
    std::string msg;

public:
    Error(ErrorVariant error_type, const std::string& msg);
    ~Error();

    std::string to_string() const;
    void log() const;
};

#endif // ERROR_H
