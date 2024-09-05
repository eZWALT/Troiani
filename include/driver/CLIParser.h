#ifndef CLI_PARSER_H
#define CLI_PARSER_H 

#include <string>
#include <optional>
#include "utils/Error.h"

//Expected<T,E> or Optional<T>

class CLIParser {

    private:

        // Flags
        bool help;
        bool version;
        bool ast_dump;

        bool emit_mlir;
        bool emit_llvm;

        // Strings
        /*
        std::string backend_target;
        */
        std::string infile_name;
        std::string outfile_name;

        std::optional<Error> error;
        std::optional<Error> parse_arguments(int argc, char* argv[]);

    public:

    CLIParser(int argc, char* argv[]);
    ~CLIParser();

    std::optional<Error> get_error();

    bool show_help() const;

    bool show_version() const;

    bool show_ast_dump() const;

    void print_help() const;

    void print_version() const;

    //Lacks ast as parameter
    void print_ast_dump() const;

    
};

#endif