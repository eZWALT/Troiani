#include "CLIParser.h"
#include <optional>
#include <regex>
#include <iostream>
#include <filesystem>


std::string get_filename_without_extension(const std::string& filename) {
    std::filesystem::path file_path(filename);
    return file_path.stem().string();
}

//Unix only
bool CLIParser::file_name_is_well_formed(const std::string& file_name) const {
    std::filesystem::path file_path(file_name);
    // Detect fake flags
    if (std::regex_match(file_name, std::regex("^--.*"))) {
        return false;  // Filename looks like a flag
    }
    // Check if the file has the correct extension
    std::string extension = file_path.extension().string();
    if (extension != ".troi" && extension != ".tr") {
        return false;
    }
    // Ensure the filename is not empty
    if (file_path.filename().empty()) {
        return false;
    }
    return true;
}

bool CLIParser::is_non_existent_flag(const std::string& flag) const {
    return (std::regex_match(flag, std::regex("^--.*")) 
            && valid_flags.find(flag) == valid_flags.end());

}

CLIParser::CLIParser() : 
help(false), version(false), ast_dump(false), 
infile_name(""), outfile_name(""), emit_llvm(false),
emit_mlir(false)  {
    this->config = Config();
}


std::optional<Error> CLIParser::parse_arguments(int argc, char* argv[]) {
    
    for(int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "--help") {
            this->help = true;
            return std::nullopt;
        }
        else if (arg == "--version"){
            this->version = true;
            return std::nullopt;
        }
        else if (arg == "--ast-dump") {
            this->ast_dump = true;
        }
        else if (arg == "--input") {
            if (i+1 < argc) {
                if(this->file_name_is_well_formed(argv[i+1])){
                    this->infile_name = argv[i+1];
                }
                else return Error(
                                ErrorType::CLI::InvalidArgument,
                                "The input file name is malformed. " 
                                + std::string(argv[i+1])
                            );
            }
            else return Error(
                            ErrorType::CLI::MissingArgument,
                            "No input file name given"
                        );
            ++i;
        }
        else if (arg == "--output") {
            if (i+1 < argc) this->outfile_name = argv[i+1];
            else return Error(
                        ErrorType::CLI::MissingArgument,
                        "No output file name given"
                        );
            ++i;
        }
        else {
            if(!this->file_name_is_well_formed(arg)){
                if(this->is_non_existent_flag(arg)){
                    return Error(
                                ErrorType::CLI::NonExistentFlag,
                                "The given flag is non existent: "
                                + std::string(arg)
                            );
                }
                return Error(
                            ErrorType::CLI::InvalidArgument,
                            "The input file name is malformed. "
                             + arg
                        );
            }
            else if(    
                this->lacks_input_file()  &&
                this->file_name_is_well_formed(arg)
                ) 
                this->infile_name = arg;
            else return Error(ErrorType::CLI::InvalidArgument, arg);
        }
    }

    if (this->lacks_input_file())
        return Error(ErrorType::CLI::MissingArgument, "No input file given"); 

    if (this->outfile_name.empty() && !this->infile_name.empty()) 
        this->outfile_name = get_filename_without_extension(this->infile_name);

    return std::nullopt;
}

CLIParser::~CLIParser() {}


/*** File management ***/
std::string CLIParser::get_input_file_name() const {
    return this->infile_name;
}

std::string CLIParser::get_output_file_name() const {
    return this->outfile_name;
}

bool CLIParser::lacks_input_file() const {
    return (!this->version 
            && !this->help 
            && this->infile_name.empty()
    );
}

/*** Flags queries ***/
bool CLIParser::show_help() const { return help; }
bool CLIParser::show_version() const { return version; }
bool CLIParser::show_ast_dump() const { return ast_dump; }

/*** Printing functions ***/
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
    std::cout << "--output FILE     Specify the output" << std::endl;
    std::cout << std::endl;

    std::cout << "EXAMPLES:" << std::endl;
    std::cout << "  Compile a file with a custom output name:" << std::endl;
    std::cout << "    ./troiani --input source.tr --output target.exe" << std::endl;
    std::cout << std::endl;

}

std::optional<Error> CLIParser::print_version() const {
    std::string key = "version";
    std::optional<std::string> version = this->config.get(key);
    if(version) {
        std::cout << "Version " << *version << std::endl;
        return std::nullopt;
    }
    else return Error(ErrorType::Configuration::NonExistentValue, key);
}

void CLIParser::print_ast_dump() const {        
    std::cout << "WIP :)" << std::endl;
}

