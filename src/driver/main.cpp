#include <string>
#include <optional>
#include <iostream>

#include "Error.h"
#include "CLIParser.h"
#include "Preprocessor.h"
#include "SourceFile.h"



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

    SourceFile source_file = SourceFile(cli.get_input_file_name());
    Preprocessor preprocessor = Preprocessor(source_file);

    std::optional<Error> pre_err = preprocessor.preprocess();
    if(pre_err) {
        pre_err->log();
        return 1;
    }
    SourceFile preprocessed_file = preprocessor.get_processed_file();
    std::cout << preprocessed_file.get_content() << std::endl;


    std::cout << "Compilation failed successfully" << std::endl;
    return 0;
}