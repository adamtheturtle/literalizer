#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::variant<std::tuple<int, std::string>, std::vector<int>, std::vector<std::nullptr_t>>>, std::vector<std::vector<int>>>>{
    std::vector<std::variant<std::tuple<int, std::string>, std::vector<int>, std::vector<std::nullptr_t>>>{std::make_tuple(1, "value"), std::vector<int>{1, 2}, std::vector<int>{}},
    std::vector<std::vector<int>>{std::vector<int>{}, std::vector<int>{}, std::vector<int>{3, 4}},
};
    (void)my_data;
    return 0;
}
