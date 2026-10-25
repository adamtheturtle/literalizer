#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::vector<std::nullptr_t>>>{
    1,
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
