#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
const auto my_data = std::vector<std::variant<std::vector<int>, std::vector<std::nullptr_t>, std::vector<std::string>>>{
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
    std::vector<std::string>{"a", "b"},
};
(void)my_data;
my_data = std::vector<std::variant<std::vector<int>, std::vector<std::nullptr_t>, std::vector<std::string>>>{
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
    std::vector<std::string>{"a", "b"},
};
    (void)my_data;
    return 0;
}
