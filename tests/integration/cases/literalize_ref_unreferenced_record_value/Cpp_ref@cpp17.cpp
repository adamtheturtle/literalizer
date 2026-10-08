#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
const auto* other = "true";
auto my_data = std::map<std::string, std::map<std::string, std::variant<int, std::string>>>{
    {"main", std::map<std::string, std::variant<int, std::string>>{{"x", 1}, {"y", "s"}}},
};
    (void)my_data;
    return 0;
}
