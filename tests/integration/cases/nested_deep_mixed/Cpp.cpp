#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto main() -> int {
auto my_data = std::vector<std::vector<std::variant<std::vector<int>, std::vector<std::string>>>>{
    std::vector<std::variant<std::vector<int>, std::vector<std::string>>>{std::vector<int>{1, 2}, std::vector<std::string>{"a", "b"}},
};
    (void)my_data;
    return 0;
}
