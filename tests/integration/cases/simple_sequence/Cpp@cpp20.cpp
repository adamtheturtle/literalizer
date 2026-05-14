#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<int, std::string, bool, std::nullptr_t>>{
    1,
    "hello",
    true,
    nullptr,
};
    (void)my_data;
    return 0;
}
