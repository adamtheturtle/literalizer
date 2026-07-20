#include <vector>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, std::vector<std::variant<bool, int, std::string>>>>{
    {"name", "Alice"},
    {"tags", std::vector<std::variant<bool, int, std::string>>{true, 42, "apple"}},
};
    (void)my_data;
    return 0;
}
