#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::map<std::string, std::variant<std::string, int>>>>{
    {"id", 1},
    {"owner", std::map<std::string, std::variant<std::string, int>>{{"name", "Alice"}, {"age", 30}}},
};
(void)my_data;
my_data = std::map<std::string, std::variant<int, std::map<std::string, std::variant<std::string, int>>>>{
    {"id", 1},
    {"owner", std::map<std::string, std::variant<std::string, int>>{{"name", "Alice"}, {"age", 30}}},
};
    (void)my_data;
    return 0;
}
