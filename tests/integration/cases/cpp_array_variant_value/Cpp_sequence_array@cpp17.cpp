#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::string, std::array<int, 2>, std::map<std::string, std::string>>>{
    {"a", 1},
    {"b", "x"},
    {"e", std::array<int, 2>{1, 2}},
    {"f", std::map<std::string, std::string>{{"g", "h"}}},
};
    (void)my_data;
    return 0;
}
