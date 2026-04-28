#include <initializer_list>
#include <string>
#include <map>
#include <variant>
auto main() -> int {
auto my_data = std::map<std::string, std::variant<std::map<std::string, int>, int>>{
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::map<std::string, int>, int>>{
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
    (void)my_data;
    return 0;
}
