#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include <optional>
#include <string>
#include <fstream>
#include <sstream>
#include <regex>

#include "Error.h"
#include "SourceFile.h"

class Preprocessor {
private:
    SourceFile source_file;
public:
    Preprocessor(SourceFile& source_file);
    std::optional<Error> preprocess();

    std::optional<Error> load_file();
    std::optional<Error> remove_comments();
    std::optional<Error> handle_inclusions();
    std::optional<Error> handle_macros();

    SourceFile get_processed_file() const;
    const std::string& get_processed_content() const;
};

#endif