#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto std = std::map<std::string, int>{
    {"a", 1},
};
auto arena = std::map<std::string, int>{
    {"a", 1},
};
auto allocator = std::map<std::string, int>{
    {"a", 1},
};
auto my_data = std::vector<std::map<std::string, int>>{
    std::move(std),
    std::move(arena),
    std::move(allocator),
};
    (void)my_data;
    return 0;
}
