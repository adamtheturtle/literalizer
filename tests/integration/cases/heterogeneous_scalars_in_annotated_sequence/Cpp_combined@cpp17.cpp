#include <initializer_list>
#include <cstddef>
#include <string>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<bool, double, std::nullptr_t, std::string, std::vector<std::nullptr_t>>>{
    true,
    1.5,
    nullptr,
    "2020-01-01",
    "2020-01-01T00:00:00+00:00",
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<std::variant<bool, double, std::nullptr_t, std::string, std::vector<std::nullptr_t>>>{
    true,
    1.5,
    nullptr,
    "2020-01-01",
    "2020-01-01T00:00:00+00:00",
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
