//===----- Config.h Configuration map class -----===/
//
// This class provides a singleton interface for retrieving
// configuration values such as version or default values
//
//===--------------------------------------------===/


#ifndef CONFIG_H
#define CONFIG_H

#include "Error.h"
#include <string>
#include <map>
#include <optional>

class Config {
private:
    std::map<std::string, std::string> config_map;
public:
    Config();

    std::optional<std::string> get(
        const std::string& key
    ) const;

    void set(const std::string& key, const std::string&  value);
};

#endif 