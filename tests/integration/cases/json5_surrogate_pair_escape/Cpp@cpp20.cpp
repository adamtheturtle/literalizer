#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int, std::vector<std::variant<std::string, int>>, std::map<std::string, std::string>>>{
    {"astral", "😀"},
    {"mixed", "a😀b"},
    {"count", 2},
    {"list", std::vector<std::variant<std::string, int>>{"😀", 1}},
    {"nested", std::map<std::string, std::string>{{"inner", "😀"}}},
};
    (void)my_data;
    return 0;
}
