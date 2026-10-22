#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::variant<std::vector<std::variant<int, std::string>>, std::vector<int>>>>{
    std::vector<std::variant<std::vector<std::variant<int, std::string>>, std::vector<int>>>{std::vector<std::variant<int, std::string>>{1, "value"}, std::vector<int>{1, 2}, std::vector<int>{}},
    std::vector<std::variant<std::vector<std::variant<int, std::string>>, std::vector<int>>>{std::vector<int>{}, std::vector<int>{}, std::vector<int>{3, 4}},
};
    (void)my_data;
    return 0;
}
