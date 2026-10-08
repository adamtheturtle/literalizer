#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
int main() {
static auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::vector<int>, std::vector<std::variant<int, std::string, bool, std::nullptr_t>>>>{
    std::vector<std::nullptr_t>{},
    std::vector<int>{1},
    std::vector<int>{1, 2},
    std::vector<std::variant<int, std::string, bool, std::nullptr_t>>{1, "x", true, nullptr},
    std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8},
};
    (void)my_data;
    return 0;
}
