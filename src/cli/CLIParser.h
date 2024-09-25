#ifndef CLI_PARSER_H
#define CLI_PARSER_H 

#include <string>
#include <optional>
#include <set>
#include <regex>
#include <iostream>
#include <filesystem>

#include "Error.h"
#include "Config.h"


class CLIParser {

    private:

        // Flags
        bool help;
        bool version;
        bool ast_dump;
        bool hard_warnings;
        bool optimization;
        bool triple;
        bool debug = true;
        bool release;
        std::set<std::string> valid_flags = {
            "--help", "--version", "--ast-dump",
            "--input", "--output", "--emit-llvm",
            "--emit-mlir", "--emit--assembly",
            "--hard-warnings", "--triple",
            "--optimization", "--debug", "--release"
        };

        // Middle end targets
        bool emit_assembly;
        bool emit_mlir;
        bool emit_llvm;

        // Compilation triple ()
        std::string comp_triple;

        // File identifiers
        std::string infile_name;
        std::string outfile_name;

        //Optimization level & others
        unsigned int optimization_lvl;

        // Configuration singleton
        Config config;
        
    public:

    CLIParser();
    ~CLIParser();
    std::optional<Error> parse_arguments(int argc, char* argv[]);

    /*** File management ***/
    std::string get_input_file_name() const;
    std::string get_output_file_name() const;
    bool lacks_input_file() const;

    /*** String handling ***/
    bool file_name_is_well_formed(const std::string& file_name) const;
    bool is_non_existent_flag(const std::string& flag) const;

    /*** Flags queries ***/
    bool show_help() const;
    bool show_version() const;
    bool show_ast_dump() const;


    /*** Printing functions ***/
    void print_help() const;
    std::optional<Error> print_version() const;
    void print_ast_dump() const;
    //Lacks AST as parameter

    
};

#endif