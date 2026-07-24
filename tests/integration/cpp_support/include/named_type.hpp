#ifndef NAMED_TYPE_HPP
#define NAMED_TYPE_HPP

#include <string>
#include <vector>

struct NamedType {
    int id{};
    std::string description;
    bool is_done{};
    std::vector<int> blocks;
};

#endif
