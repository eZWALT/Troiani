#include <string>
#include <optional>
#include <iostream>

#include "utils/Error.h"
#include "cli/CLIParser.h"


int main(int argc, char* argv[]) {
    CLIParser cli = CLIParser(argc, argv);
    std::optional<Error> cli_err = cli.get_error();

    if(cli_err) {
        cli_err->log();
        return 1;
    }

    if(cli.show_help()) {
        cli.print_help();
        return 0;
    }

    if(cli.show_version()) {
        cli.print_version();
        return 0;
    }

    if(cli.show_ast_dump()) {
        cli.print_ast_dump();
        return 0;
    }

    std::cout << "Compilation failed successfully" << std::endl;
    return 0;
}