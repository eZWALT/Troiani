#include "utils/Error.h"

// ErrorType to_string functions
std::string ErrorType::to_string(CLI err_ty) {
    switch(err_ty) {
        case CLI::InvalidArgument: return "Invalid argument";
        case CLI::MissingArgument: return "Missing argument";
        default: return "Unknown CLI error";
    }
} 

std::string ErrorType::to_string(Preprocessing err_ty) {
    switch(err_ty) {
        case Preprocessing::FileNotFound: return "File not found";
        case Preprocessing::IncludeCycle: return "Include cycle";
        case Preprocessing::InvalidDirective: return "Invalid directive";
        default: return "Unknown Preprocessing error";
    }
}

std::string ErrorType::to_string(Syntax err_ty)  {
    switch(err_ty) {
        case Syntax::InvalidSyntax: return "Invalid syntax";
        default: return "Unknown Syntax error";
    }
}

std::string ErrorType::to_string(Semantic err_ty) {
    switch(err_ty) {
        case Semantic::TypeMismatch: return "Type mismtach";
        case Semantic::UndeclaredVariable: return "Undeclared variable";
        default: return "Unknown Semantic error";
    }
}

std::string ErrorType::to_string(CodeGeneration err_ty) {
    switch(err_ty) {
        case CodeGeneration::InvalidInstruction: return "Invalid instruction";
        default:  return "Unknown Code Generation error";
    }
}

std::string ErrorType::to_string(Optimization err_ty) {
    switch(err_ty) {
        case Optimization::OptimizationFailure: return "Optimization failure";
        default: return "Unknown Optimization error";
    }
}

std::string ErrorType::to_string(Linking err_ty) {
    switch(err_ty) {
        case Linking::UndefinedReference: return "Undefined reference";
        case Linking::MultipleDefinition: return "Multiple definition";
        default: return "Unknown Linking error";
    }
}

std::string ErrorType::to_string(Runtime err_ty) {
    switch(err_ty) {
        case Runtime::DivisionByZero: return "Division by zero";
        case Runtime::NullPointerDereference: return "Null pointer dereference";
        case Runtime::StackOverflow: return "Stack overflow";
        case Runtime::OutOfMemory: return "Out of memory";
        default: return "Unknown Runtime error";
    }
}


// Error implementation

Error::Error(ErrorType type, const std::string& msg):
type(type), msg(msg) {}

Error::~Error() {}


void Error::log() const {
    std::cerr << this->to_string() << std::endl;
}

std::string to_string() const {
    return "[E " +  ErrorType::to_string(this->type) + "]: " + this->msg;
}