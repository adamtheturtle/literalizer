#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::initializer_list<std::nullptr_t>, std::initializer_list<int>, std::vector<std::nullptr_t>>>{
    std::initializer_list<std::nullptr_t>{},
    std::initializer_list<int>{1, 2},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
