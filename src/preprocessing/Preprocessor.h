#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include "Error.h"
#include <optional>
#include <string>

class Preprocessor {
private:
    std::string file_name;
    std::string file_contents;
public:
    Preprocessor(const std::string& file_name);
    std::optional<Error> preprocess();

    std::optional<Error> load_file();
    std::optional<Error> remove_comments();
    std::optional<Error> handle_inclusions();
    std::optional<Error> handle_macros();

    const std::string& get_processed_content() const;
};

#endif