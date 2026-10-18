#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::array<std::array<int, 2>, 1>, std::array<std::array<int, 1>, 1>>>{
    {"a", std::array<std::array<int, 2>, 1>{std::array<int, 2>{1, 2}}},
    {"b", std::array<std::array<int, 1>, 1>{std::array<int, 1>{3}}},
};
    (void)my_data;
    return 0;
}
