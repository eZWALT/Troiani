#include "Preprocessor.h"

Preprocessor::Preprocessor(SourceFile& source_file) : source_file(source_file) {}

std::optional<Error> Preprocessor::load_file() {
    if (!source_file.is_loaded()) {
        std::optional<Error> err = source_file.load();
        if (err) {
            return err;
        }
    }
    return std::nullopt;
}

std::optional<Error> Preprocessor::preprocess() {
    // Load the file
    std::optional<Error> err = load_file();
    if (err) return err;

    // Remove comments
    err = remove_comments();
    if (err) return err;

    // Handle includes
    err = handle_inclusions();
    if (err) return err;

    // Handle macros
    err = handle_macros();
    return err;
}

std::optional<Error> Preprocessor::remove_comments() {
    std::string content = source_file.get_content();
    
    std::regex single_line_comm(R"((\/\/.*?$))", std::regex::multiline);
    std::regex multi_line_comm(R"((\/\*[\s\S]*?\*\/))");

    content = std::regex_replace(content, single_line_comm, "");
    content = std::regex_replace(content, multi_line_comm, "");

    // Update the content of SourceFile
    source_file.update_content(content);

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

SourceFile Preprocessor::get_processed_file() const {
    return this->source_file;
}

const std::string& Preprocessor::get_processed_content() const {
    return source_file.get_content();
}