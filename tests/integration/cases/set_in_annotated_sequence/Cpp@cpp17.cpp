#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::vector<int>>>{
    std::vector<std::nullptr_t>{},
    std::vector<int>{1, 2},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
