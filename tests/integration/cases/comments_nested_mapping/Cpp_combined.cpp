#include <initializer_list>
#include <string>
#include <map>
#include <variant>
void check_() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, int>, int>>{
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
my_data = std::map<std::string, std::variant<std::map<std::string, int>, int>>{
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
}
