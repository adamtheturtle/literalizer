#include <cstddef>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<std::variant<std::vector<int>, std::vector<std::string>, std::vector<std::nullptr_t>>>, std::vector<std::map<std::string, std::variant<int, std::string>>>, std::map<std::string, std::vector<int>>>>{
    {"lists", std::vector<std::variant<std::vector<int>, std::vector<std::string>, std::vector<std::nullptr_t>>>{std::vector<int>{1}, std::vector<std::string>{"x"}, std::vector<std::nullptr_t>{}}},
    {"maps", std::vector<std::map<std::string, std::variant<int, std::string>>>{std::map<std::string, std::variant<int, std::string>>{{"x", 1}}, std::map<std::string, std::variant<int, std::string>>{{"x", "s"}}}},
    {"empties", std::map<std::string, std::vector<int>>{{"a", std::vector<int>{1}}, {"b", std::vector<int>{}}}},
};
    (void)my_data;
    return 0;
}
