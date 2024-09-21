#include "Config.h"

Config::Config() {
    this->config_map["version"] = "1.0";
    this->config_map["optimization_level"] = "0";
    this->config_map["language_standard"] = "Troiani 1";
    this->config_map["warnings_as_errors"] = "0";
    this->config_map["debug_mode"] = "0";
    this->config_map["target_architecture"] = "x86_64";
}

void Config::set(const std::string& key, const std::string& value) {
    this->config_map[key] = value;
}

std::optional<std::string> Config::get(const std::string& key) const{
    auto it = this->config_map.find(key);
    if(it != this->config_map.end()) return it->second;
    else return std::nullopt;
}