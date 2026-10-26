#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto shared = std::vector<std::variant<std::vector<int>, std::map<std::string, int>>>{
    std::vector<int>{1, 2},
    std::map<std::string, int>{{"value", 1}},
};
auto my_data = std::vector<std::vector<std::variant<std::vector<int>, std::map<std::string, int>>>>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
