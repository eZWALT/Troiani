#include "SourceFile.h"


SourceFile::SourceFile(const std::string& path): file_path(path) {}

std::optional<Error> SourceFile::load() {
    std::ifstream file(file_path);
    if (!file) {
        return Error(
                    ErrorType::Preprocessing::FileNotFound,
                    "Failed to open file: " + this->file_path + ". Reason: " + std::strerror(errno)
                );
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    content = buffer.str();
    loaded = true;
    return std::nullopt;
}

const std::string& SourceFile::get_content() const {
    return content;
}

void SourceFile::update_content(const std::string& new_content) {
    content = new_content;
}

bool SourceFile::is_loaded() const {
    return loaded;
}

const std::string& SourceFile::get_path() const {
    return file_path;
}