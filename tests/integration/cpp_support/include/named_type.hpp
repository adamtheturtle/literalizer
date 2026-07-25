#ifndef NAMED_TYPE_HPP
#define NAMED_TYPE_HPP

#include <map>
#include <string>
#include <vector>

struct NamedType {
    int id{};
    std::string label;
    bool enabled{};
    std::vector<int> related_ids;
};

using ExternalRecordShape = std::map<std::string, std::string>;

#endif
