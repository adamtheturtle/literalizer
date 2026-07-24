#ifndef NAMED_TYPE_HPP
#define NAMED_TYPE_HPP

#include <string>
#include <vector>

struct NamedType {
    int id{};
    std::string label;
    bool enabled{};
    std::vector<int> related_ids;
};

#endif
