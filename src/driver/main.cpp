#include <string>
#include <optional>
#include <iostream>

#include "Error.h"
#include "CLIParser.h"
#include "Preprocessor.h"



int main(int argc, char* argv[]) {
    //CLI Phase
    CLIParser cli = CLIParser();
    std::optional<Error> cli_err = cli.parse_arguments(argc, argv);

    if(cli_err) {
        cli_err->log();
        return 1;
    }
    if(cli.show_help()) {
        cli.print_help();
        return 0;
    }
    if(cli.show_version()) {
        std::optional<Error> version_err = cli.print_version();
        
        if(version_err) {
            version_err->log();
            return 1;
        }
        else return 0;
        
    }
    if(cli.show_ast_dump()) {
        cli.print_ast_dump();
        return 0;
    }

    //Preprocessing phase 
    Preprocessor preprocessor = Preprocessor(cli.get_input_file_name());
    preprocessor.preprocess();
    std::string preprocessed_file = preprocessor.get_processed_content();

    
    std::cout << "Compilation failed successfully" << std::endl;
    return 0;
}