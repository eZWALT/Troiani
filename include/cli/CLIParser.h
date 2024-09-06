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

        // Middle end targets
        bool emit_mlir;
        bool emit_llvm;

        // Back end targets

        // File identifiers
        std::string infile_name;
        std::string outfile_name;
        
        std::optional<Error> error;
        std::optional<Error> parse_arguments(int argc, char* argv[]);

    public:

    CLIParser(int argc, char* argv[]);
    ~CLIParser();
    std::optional<Error> get_error() const;

    /*** File management ***/
    std::string get_input_file_name() const;
    std::string get_output_file_name() const;

    /*** Flags queries ***/
    bool show_help() const;
    bool show_version() const;
    bool show_ast_dump() const;

    /*** Printing functions ***/
    void print_help() const;
    void print_version() const;
    void print_ast_dump() const;
    //Lacks AST as parameter

    
};

#endif