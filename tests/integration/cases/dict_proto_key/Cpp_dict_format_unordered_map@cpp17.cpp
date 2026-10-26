#include <string>
#include <unordered_map>
#include <variant>
int main() {
auto my_data = std::unordered_map<std::string, std::variant<std::unordered_map<std::string, int>, int>>{
    {"__proto__", std::unordered_map<std::string, int>{{"x", 1}}},
    {"n", std::unordered_map<std::string, int>{{"__proto__", 3}}},
    {"y", 2},
};
    (void)my_data;
    return 0;
}
