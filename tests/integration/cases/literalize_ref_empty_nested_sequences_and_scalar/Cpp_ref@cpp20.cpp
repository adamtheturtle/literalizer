#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto seed = 1;
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::vector<std::vector<std::nullptr_t>>, int>>{
    std::vector<std::vector<std::nullptr_t>>{},
    std::vector<std::vector<std::nullptr_t>>{std::vector<std::nullptr_t>{}},
    seed,
};
    (void)my_data;
    return 0;
}
