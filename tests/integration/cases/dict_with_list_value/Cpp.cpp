#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<int>>>{
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
    (void)my_data;
}
