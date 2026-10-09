#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::vector<std::variant<std::tuple<int, std::string>, std::vector<std::nullptr_t>>>{
    std::make_tuple(1, "value"),
    std::vector<std::variant<int, std::string>>{},
};
    (void)my_data;
    return 0;
}
