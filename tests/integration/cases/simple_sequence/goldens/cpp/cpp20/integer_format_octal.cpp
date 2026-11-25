#include <cstddef>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, std::string, bool, std::nullptr_t>>{
    01,
    "hello",
    true,
    nullptr,
};
    (void)my_data;
    return 0;
}
