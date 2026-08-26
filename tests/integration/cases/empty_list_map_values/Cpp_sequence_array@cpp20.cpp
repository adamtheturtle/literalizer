#include <initializer_list>
#include <string>
#include <map>
#include <array>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::array<int, 2>, std::array<std::nullptr_t, 0>>>{
    {"a", std::array<int, 2>{1, 2}},
    {"b", std::array<std::nullptr_t, 0>{}},
};
    (void)my_data;
    return 0;
}
