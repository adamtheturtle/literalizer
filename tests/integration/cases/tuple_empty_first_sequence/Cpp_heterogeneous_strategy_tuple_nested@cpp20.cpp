#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::nullptr_t>, std::tuple<int, std::string>>>{
    std::vector<std::nullptr_t>{},
    std::make_tuple(1, "value"),
    std::make_tuple(2, "other"),
};
    (void)my_data;
    return 0;
}
