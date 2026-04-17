#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
void check_() {
auto my_data = std::vector<std::vector<std::vector<std::nullptr_t>>>{
    std::vector<std::vector<std::nullptr_t>>{std::vector<std::nullptr_t>{}, std::vector<std::nullptr_t>{}},
};
my_data = std::vector<std::vector<std::vector<std::nullptr_t>>>{
    std::vector<std::vector<std::nullptr_t>>{std::vector<std::nullptr_t>{}, std::vector<std::nullptr_t>{}},
};
}
