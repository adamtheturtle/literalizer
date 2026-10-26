#include <cstddef>
#include <string>
#include <tuple>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>, std::vector<std::variant<std::vector<std::nullptr_t>, std::tuple<int, std::string>>>>>{
    std::vector<std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>{std::make_tuple(1, "value"), std::vector<std::nullptr_t>{}},
    std::vector<std::variant<std::vector<std::nullptr_t>, std::tuple<int, std::string>>>{std::vector<std::nullptr_t>{}, std::make_tuple(2, "other")},
};
    (void)my_data;
    return 0;
}
