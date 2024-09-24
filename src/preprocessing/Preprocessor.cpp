#include "Preprocessor.h"
#include <fstream>
#include <sstream>
#include <regex>

//There are 5 types of streams in modern c++: in/infile/out/outfile/string
Preprocessor::Preprocessor(const std::string& file_name):
file_name(file_name) {}

std::optional<Error> Preprocessor::load_file() {
    std::ifstream file(this->file_name);
    if(!file) { 
        return Error(ErrorType::Preprocessing::FileNotFound,
        "Failed to open file: " + this->file_name);
    }

    std::stringstream buff;
    buff << file.rdbuf();
    file_contents = buff.str();
    return std::nullopt;
}

std::optional<Error> Preprocessor::preprocess() {
    //Load the file
    std::optional<Error> err = load_file();
    if(err) return err;

    err = remove_comments();
    if(err) return err;

    err = handle_inclusions();
    if(err) return err;

    err = handle_macros();
    return err;
}

std::optional<Error> Preprocessor::remove_comments() {
    std::regex single_line_comm(R"((\/\/.*?$))", std::regex::multiline);
    std::regex multi_line_comm(R"((\/\*[\s\S]*?\*\/))");

    this->file_contents = std::regex_replace(
        this->file_contents,single_line_comm, ""
    );

    this->file_contents = std::regex_replace(
        this->file_contents,multi_line_comm, ""
    );

    return std::nullopt;
}


std::optional<Error> Preprocessor::handle_inclusions() {
    // TODO: Implement include handling
    return std::nullopt;
}

std::optional<Error> Preprocessor::handle_macros() {
    // TODO: Implement macro expansion
    return std::nullopt;
}



const std::string& Preprocessor::get_processed_content() const {
    return file_contents;
}