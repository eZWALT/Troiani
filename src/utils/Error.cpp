#include "Error.h"

// Implementations of ErrorType to_string functions
std::string ErrorType::to_string(CLI err_ty) {
    switch (err_ty) {
        case CLI::InvalidArgument: return "CLI: Invalid argument";
        case CLI::MissingArgument: return "CLI: Missing argument";
        case CLI::NonExistentFlag: return "CLI: Non existent flag";
        default: return "CLI: Unknown CLI error";
    }
}

std::string ErrorType::to_string(Preprocessing err_ty) {
    switch (err_ty) {
        case Preprocessing::FileNotFound: return "PRE: File not found";
        case Preprocessing::IncludeCycle: return "PRE: Include cycle";
        case Preprocessing::InvalidDirective: return "PRE: Invalid directive";
        default: return "PRE: Unknown Preprocessing error";
    }
}

std::string ErrorType::to_string(Syntax err_ty) {
    switch (err_ty) {
        case Syntax::InvalidSyntax: return "SYN: Invalid syntax";
        default: return "SYN: Unknown Syntax error";
    }
}

std::string ErrorType::to_string(Semantic err_ty) {
    switch (err_ty) {
        case Semantic::TypeMismatch: return "SEM: Type mismatch";
        case Semantic::UndeclaredVariable: return "SEM: Undeclared variable";
        default: return "SEM: Unknown Semantic error";
    }
}

std::string ErrorType::to_string(CodeGeneration err_ty) {
    switch (err_ty) {
        case CodeGeneration::InvalidInstruction: return "CDG: Invalid instruction";
        default: return "CDG: Unknown Code Generation error";
    }
}

std::string ErrorType::to_string(Optimization err_ty) {
    switch (err_ty) {
        case Optimization::OptimizationFailure: return "OPT: Optimization failure";
        default: return "OPT: Unknown Optimization error";
    }
}

std::string ErrorType::to_string(Linking err_ty) {
    switch (err_ty) {
        case Linking::UndefinedReference: return "LNK: Undefined reference";
        case Linking::MultipleDefinition: return "LNK: Multiple definition";
        default: return "LNK: Unknown Linking error";
    }
}

std::string ErrorType::to_string(Runtime err_ty) {
    switch (err_ty) {
        case Runtime::DivisionByZero: return "RT: Division by zero";
        case Runtime::NullPointerDereference: return "RT: Null pointer dereference";
        case Runtime::StackOverflow: return "RT: Stack overflow";
        case Runtime::OutOfMemory: return "RT: Out of memory";
        default: return "RT: Unknown Runtime error";
    }
}

std::string ErrorType::to_string(Configuration err_ty) {
    switch (err_ty) {
        case Configuration::NonExistentValue: return "CFG: Non-existent value";
        default: return "CFG: Unknown Configuration error";
    }
}

// Error implementation

Error::Error(ErrorVariant error_type, const std::string& msg)
    : error_type(error_type), msg(msg) {}

Error::~Error() {}

void Error::log() const {
    std::cerr << this->to_string() << std::endl;
}

std::string Error::to_string() const {
    return "[Error-" + std::visit([](const auto& err) -> std::string {
        return ErrorType::to_string(err);
    }, error_type) + "]" + ": " + msg;
}
