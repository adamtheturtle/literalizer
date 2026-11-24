#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<std::map<std::string, std::variant<int, std::string>>>>>{
    {"name", "box"},
    {"items", std::vector<std::map<std::string, std::variant<int, std::string>>>{std::map<std::string, std::variant<int, std::string>>{{"id", 1}, {"label", "first"}}, std::map<std::string, std::variant<int, std::string>>{{"id", 2}, {"label", "second"}}}},
};
    (void)my_data;
    return 0;
}
