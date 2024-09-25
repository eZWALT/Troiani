#ifndef SOURCEFILE_H
#define SOURCEFILE_H

#include <optional>
#include <string>
#include <fstream>
#include <sstream>
#include <cerrno>    // For errno
#include <cstring>   // For std::strerror
#include "Error.h"

class SourceFile {
private:
    std::string file_path;
    std::string content;
    bool loaded = false;

public:
    SourceFile(const std::string& path);

    std::optional<Error> load();
    const std::string& get_content() const;
    void update_content(const std::string& new_content);
    bool is_loaded() const;
    const std::string& get_path() const;
};

#endif 