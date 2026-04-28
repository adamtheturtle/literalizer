#include <initializer_list>
#include <string>
#include <unordered_map>
#include <vector>
#include <variant>
auto main() -> int {
auto my_data = std::unordered_map<std::string, std::variant<std::string, std::vector<int>>>{
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
    (void)my_data;
    return 0;
}
