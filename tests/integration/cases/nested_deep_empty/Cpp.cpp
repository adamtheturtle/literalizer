#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
const auto my_data = std::vector<std::vector<std::vector<std::nullptr_t>>>{
    std::vector<std::vector<std::nullptr_t>>{std::vector<std::nullptr_t>{}, std::vector<std::nullptr_t>{}},
};
    (void)my_data;
    return 0;
}
