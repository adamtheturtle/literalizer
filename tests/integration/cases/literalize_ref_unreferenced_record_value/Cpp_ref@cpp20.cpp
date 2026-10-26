#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::variant<int, std::string>>>{
    {"main", std::map<std::string, std::variant<int, std::string>>{{"x", 1}, {"y", "s"}}},
};
    (void)my_data;
    return 0;
}
