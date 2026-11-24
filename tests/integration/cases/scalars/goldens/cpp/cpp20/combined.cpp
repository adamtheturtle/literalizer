#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<int, double, bool, std::string>>{
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
(void)my_data;
my_data = std::vector<std::variant<int, double, bool, std::string>>{
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
    (void)my_data;
    return 0;
}
