#include "driver/CLIParser.h"

// WIP: Implement error types instead of just void or bool


std::string get_filename_without_extension(const std::string& filename) {
    size_t last_dot = filename.rfind('.');
    size_t last_slash = filename.rfind('/');

    if (last_dot != std::string::npos &&
       (last_slash == std::string::npos || last_dot > last_slash)) 
    {
        return filename.substr(0, last_dot);
    }
    // If no dot is found, return the original filename
    return filename;
}

CLIParser::CLIParser(int argc, char* argv[]) : 
help(false), version(false), ast_dump(false), 
infile_name(""), outfile_name("")  {
    this->error = parse_arguments(argc, argv);
}

std::optional<Error> CLIParser::get_error() { return this->error; }

std::optional<Error> CLIParser::parse_arguments(int argc, char* argv[]) {
    
    for(int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "--help") {
            this->help = true;
        }
        else if (arg == "--version"){
            this->version = true;
        }
        else if (arg == "--ast-dump") {
            this->ast_dump = true;
        }
        else if (arg == "input") {
            if (i+1 < argc) this->infile_name = argv[i+1];
            else return Error(CLI::MissingArgument, "No input file given");
        }
        else if (arg == "output") {
            if (i+1 < argc) this->outfile_name = argv[i+1];
            else return Error(CLI::MissingArgument, "No output file name given");
        }
        else {
            if (this->infile_name == "") {
                this->infile_name = arg;
            }
            else return Error(CLI::InvalidArgument, arg);
        }
    }

    if (this->infile_name.empty())
        return Error(CLI::MissingArgument, "No input file given"); 

    if (this->outfile_name.empty()) 
        this->outfile_name = get_filename_without_extension(this->infile_name);
}

// Boolean flag functions
bool CLIParser::show_help() const { return help; }

bool CLIParser::show_version() const { return version; }

bool CLIParser::show_ast_dump() const { return ast_dump; }

// Print functions
void CLIParser::print_help() const {
    std::cout << "The Troiani Compiler" << std::endl;
    std::cout << "=====================" << std::endl;
    std::cout << "A simple language for complex problems." << std::endl;
    std::cout << std::endl;


    std::cout << "USAGE:" << std::endl;
    std::cout << "./troiani [OPTIONS] INPUT?" << std::endl;
    std::cout << std::endl;

    std::cout << "OPTIONS:" << std::endl;
    std::cout << "--help            Show a help message" << std::endl;
    std::cout << "--version         Show the version" << std::endl;
    std::cout << "--ast-dump        Display the parsed AST" << std::endl;
    std::cout << "--input FILE      Specify the input" << std::endl;
    std::cout << "--output FILE     Specify the output" << std::endl
    std::cout << endl;

    std::cout << "EXAMPLES:" << std::endl;
    std::cout << "  Compile a file with a custom output name:" << std::endl;
    std::cout << "    ./troiani --input source.tr --output target.exe" << std::endl;
    std::cout << std::endl;

}

void CLIParser::print_version() const {
    std::cout << "Version 1.0" << std::endl;
}

void CLIParser::print_ast_dump() const {        
    std::cout << "WIP :)" << std::endl;
}

