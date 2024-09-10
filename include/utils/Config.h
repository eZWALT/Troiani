#ifndef CONFIG_H
#define CONFIG_H

#include "utils/Error.h"
#include <string>
#include <map>
#include <expected>

class Config {
private:
    std::map<std::string, std::string> config_map;
public:
    Config();

    std::expected<std::string, Error> get(
        const std::string& key
    ) const;

    void set(const std::string& key, const std::string&  value) 
}

#endif 