#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::map<std::string, std::variant<int, std::string>>>>{
    {"rows", std::vector<std::map<std::string, std::variant<int, std::string>>>{std::map<std::string, std::variant<int, std::string>>{{"x", 1}, {"y", "a"}}, std::map<std::string, std::variant<int, std::string>>{{"x", 2}, {"y", "b"}}}},
};
    (void)my_data;
    return 0;
}
