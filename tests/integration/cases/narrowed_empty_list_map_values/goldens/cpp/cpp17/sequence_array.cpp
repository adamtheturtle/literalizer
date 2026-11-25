#include <array>
#include <cstddef>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::array<int, 1>, std::array<std::nullptr_t, 0>>>{
    {"a", std::array<int, 1>{1}},
    {"b", std::array<std::nullptr_t, 0>{}},
};
    (void)my_data;
    return 0;
}
