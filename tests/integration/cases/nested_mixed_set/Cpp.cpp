#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::initializer_list<std::variant<bool, int, std::string>>>>{
    {"name", "Alice"},
    {"tags", std::initializer_list<std::variant<bool, int, std::string>>{true, 42, "apple"}},
};
    (void)my_data;
    return 0;
}
