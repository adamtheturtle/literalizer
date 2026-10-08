#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, int>, int>>{
    {"__proto__", std::map<std::string, int>{{"x", 1}}},
    {"n", std::map<std::string, int>{{"__proto__", 3}}},
    {"y", 2},
};
    (void)my_data;
    return 0;
}
